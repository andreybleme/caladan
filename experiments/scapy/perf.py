# two_flows_latency_probe.py
#
# Requirements:
#   - Scapy (sudo pip install scapy)
#   - A server that ECHOs packets back (payload unchanged) on DST_PORT
# Notes:
#   - Uses RTT (send->receive) timing based on perf_counter_ns()
#   - Python/Scapy timing is jittery; not suitable for precise sub-µs latency
#   - Expect difficulty exceeding a few 100 Kpps in pure Python

from scapy.all import *
from threading import Thread, Event
from collections import defaultdict, deque
import struct, os, time, math, argparse
try:
    import numpy as np
except ImportError:
    np = None

# ---------------- Configuration via CLI ----------------
parser = argparse.ArgumentParser(description="Two-flow Scapy load + RTT latency probe")
parser.add_argument("--iface",      default="ens1f1np1")
parser.add_argument("--dst-mac",    required=True, help="Server NIC MAC (e.g., DPDK port MAC)")
parser.add_argument("--dst-ip",     required=True)
parser.add_argument("--dst-port",   type=int, default=5000)
parser.add_argument("--vlan",       type=int, default=None)
parser.add_argument("--dur",        type=float, default=20.0, help="Duration (seconds)")
parser.add_argument("--pps",        type=int, default=50000,   help="Total PPS budget across both flows")
parser.add_argument("--payload",    type=int, default=64)
parser.add_argument("--tcp-second", action="store_true", help="Make 2nd flow TCP SYNs (not recommended for RTT)")
parser.add_argument("--no-pin",     action="store_true", help="Skip CPU affinity pinning")
args = parser.parse_args()

IFACE      = args.iface
SERVER_MAC = args.dst_mac
RUNTIME_IP = args.dst_ip
DST_PORT   = args.dst_port
VLAN_ID    = args.vlan
DUR_S      = args.dur
TOTAL_PPS  = max(1, args.pps)
PAYLOAD_SZ = max(0, args.payload)
USE_TCP_B  = args.tcp_second

# Split PPS between flows
PPS_A = TOTAL_PPS // 2
PPS_B = TOTAL_PPS - PPS_A

# ---------------- Helpers ----------------
MAGIC = 0xC0DEFACECAFEBEEF  # 8 bytes identifier to filter our packets in the sniffer
HDR_FMT = "!QQQ"            # magic(8) | seq(8) | t_send_ns(8)
HDR_LEN = 8 + 8 + 8

def l2_hdr():
    eth = Ether(src=get_if_hwaddr(IFACE), dst=SERVER_MAC)
    if VLAN_ID is None:
        return eth
    else:
        return eth / Dot1Q(vlan=VLAN_ID)

def now_ns():
    return time.perf_counter_ns()

def pin_this_thread(cpu: int):
    if args.no_pin:
        return
    try:
        # Linux CPU affinity
        os.sched_setaffinity(0, {cpu})
    except Exception:
        pass

# ---------------- Shared state ----------------
stop_ev = Event()

# seq -> send_time_ns (per flow)
send_times = {
    "A": {},
    "B": {}
}

# Collected RTTs (ns)
latencies_ns = {
    "A": deque(),
    "B": deque(),
}

tx_counts = {"A": 0, "B": 0}
rx_counts = {"A": 0, "B": 0}

# ---------------- Sender ----------------
def make_pkt(flow_name, sport, use_tcp):
    # Build payload: [MAGIC|SEQ|TS|FILL...]
    # We'll fill SEQ and TS per packet quickly using bytes slicing
    base_payload = bytearray(PAYLOAD_SZ)
    # Put MAGIC at start
    struct.pack_into("!Q", base_payload, 0, MAGIC)
    # SEQ at +8, TS at +16 (filled later)
    # The rest can be random noise (optional)
    # os.urandom is slow per packet; leave zeros for speed

    ip = IP(src=get_if_addr(IFACE), dst=RUNTIME_IP, ttl=64)
    if use_tcp:
        l4 = TCP(sport=sport, dport=DST_PORT, flags="S")
    else:
        l4 = UDP(sport=sport, dport=DST_PORT)

    return l2_hdr() / ip / l4, base_payload

def send_flow(flow_name, sport, pps, use_tcp=False, cpu_pin=None):
    if cpu_pin is not None:
        pin_this_thread(cpu_pin)

    pkt_l3l4, payload = make_pkt(flow_name, sport, use_tcp)
    seq = 0

    # Token-bucket-ish pacing
    inter_ns = int(1e9 / pps) if pps > 0 else 0
    next_send = now_ns()

    s = conf.L2socket(iface=IFACE)

    end_ts = time.time() + DUR_S
    while not stop_ev.is_set() and time.time() < end_ts:
        # pace
        if inter_ns > 0:
            t = now_ns()
            if t < next_send:
                # spin (busy-wait) a little for tighter pacing
                # small sleep to yield occasionally
                if next_send - t > 200_000:  # >0.2 ms
                    time.sleep(0.0001)
                continue
            next_send += inter_ns

        # fill hdr
        seq += 1
        t_send = now_ns()
        struct.pack_into("!QQ", payload, 8, seq, t_send)

        pkt = pkt_l3l4 / Raw(bytes(payload))
        s.send(bytes(pkt))   # faster than sendp(pkt, ...)

        send_times[flow_name][seq] = t_send
        tx_counts[flow_name] += 1

    s.close()

# ---------------- Sniffer ----------------
def sniff_responder(cpu_pin=None):
    if cpu_pin is not None:
        pin_this_thread(cpu_pin)

    # We look for packets coming from server IP and dport == source ports used,
    # but simpler: filter by our MAGIC in payload to avoid false positives.
    # Use a custom prn to parse payload.
    bpf = f"ether dst {get_if_hwaddr(IFACE)} and ip src {RUNTIME_IP}"
    # AsyncSniffer is fine, but here we block in a loop so we can stop cleanly
    snif = AsyncSniffer(
        iface=IFACE,
        filter=bpf,
        prn=handle_packet,
        store=False
    )
    snif.start()
    # run until stop_ev is set
    end_ts = time.time() + (DUR_S + 5.0)  # grace window
    while not stop_ev.is_set() and time.time() < end_ts:
        time.sleep(0.05)
    snif.stop()

def handle_packet(pkt):
    try:
        if Raw not in pkt:
            return
        data = bytes(pkt[Raw].load)
        if len(data) < HDR_LEN:
            return
        magic = struct.unpack_from("!Q", data, 0)[0]
        if magic != MAGIC:
            return
        seq, t_send = struct.unpack_from("!QQ", data, 8)
        t_recv = now_ns()

        # determine flow by source/dest ports
        flow_name = None
        if UDP in pkt:
            sport = pkt[UDP].dport  # echo path: server->client dport == original sport
            if sport == 40001:
                flow_name = "A"
            elif sport == 50002:
                flow_name = "B"
        elif TCP in pkt:
            sport = pkt[TCP].dport
            if sport == 40001:
                flow_name = "A"
            elif sport == 50002:
                flow_name = "B"

        if flow_name is None:
            return

        t0 = send_times[flow_name].pop(seq, None)
        if t0 is None:
            return
        rtt = t_recv - t0
        latencies_ns[flow_name].append(rtt)
        rx_counts[flow_name] += 1
    except Exception:
        # swallow errors to keep sniffer hot
        pass

# ---------------- Percentile reporting ----------------
def ns_to_us(ns): return ns / 1000.0
def fmt_us(ns):   return f"{ns_to_us(ns):.2f} µs"

def percentiles(vals_ns, labels=(50,90,99,99.9)):
    if not vals_ns:
        return {}
    arr = np.array(vals_ns) if np else sorted(vals_ns)
    results = {}
    for p in labels:
        if np:
            results[p] = float(np.percentile(arr, p))
        else:
            # manual
            k = (p/100.0)*(len(arr)-1)
            f = math.floor(k); c = math.ceil(k)
            if f == c: results[p] = arr[int(k)]
            else: results[p] = arr[f] + (arr[c]-arr[f])*(k-f)
    return results

# ---------------- Main ----------------
def main():
    print(f"[i] iface={IFACE} dst_mac={SERVER_MAC} dst_ip={RUNTIME_IP} vlan={VLAN_ID}")
    print(f"[i] duration={DUR_S}s total_pps={TOTAL_PPS} -> flowA={PPS_A}pps, flowB={PPS_B}pps")
    print(f"[i] dst_port={DST_PORT} payload={PAYLOAD_SZ}B (plus headers)")

    # Start sniffer pinned (optional)
    sniffer_t = Thread(target=sniff_responder, kwargs={"cpu_pin": None}, daemon=True)
    sniffer_t.start()

    # Start two senders; pin them to different CPUs if you want
    tA = Thread(target=send_flow, args=("A", 40001, PPS_A, False, None))
    tB = Thread(target=send_flow, args=("B", 50002, PPS_B, USE_TCP_B, None))

    t0 = time.time()
    tA.start(); tB.start()
    tA.join();  tB.join()
    stop_ev.set()
    sniffer_t.join()
    t1 = time.time()

    elapsed = max(1e-9, t1 - t0)
    tx_total = tx_counts["A"] + tx_counts["B"]
    rx_total = rx_counts["A"] + rx_counts["B"]

    print("\n=== Summary ===")
    print(f"Elapsed: {elapsed:.3f}s")
    print(f"TX: flowA={tx_counts['A']}  flowB={tx_counts['B']}  total={tx_total}  => {tx_total/elapsed:.0f} pps")
    print(f"RX: flowA={rx_counts['A']}  flowB={rx_counts['B']}  total={rx_total}  => {rx_total/elapsed:.0f} pps")

    for name in ("A", "B"):
        vals = list(latencies_ns[name])
        pct = percentiles(vals)
        if not vals:
            print(f"\nFlow {name}: no replies captured (echo app running on server?)")
            continue
        avg = sum(vals)/len(vals)
        print(f"\nFlow {name} RTT stats (ns): count={len(vals)}")
        print(f"  avg={fmt_us(avg)}  P50={fmt_us(pct.get(50, float('nan')))}  "
              f"P90={fmt_us(pct.get(90, float('nan')))}  "
              f"P99={fmt_us(pct.get(99, float('nan')))}  "
              f"P99.9={fmt_us(pct.get(99.9, float('nan')))}")

if __name__ == "__main__":
    main()
