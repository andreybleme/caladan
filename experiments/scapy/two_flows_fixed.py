# two_flows_fixed.py
from scapy.all import *
from threading import Thread
import os, time

IFACE     = "ens1f1np1"                     # client experiment NIC eno49np0 and ens1f1np1
SERVER_MAC= "9c:dc:71:5d:51:21"            # <-- DPDK port1 MAC from server log
RUNTIME_IP= "128.110.218.80"                     # <-- IP the server runtime registered with IOKernel
DST_PORT  = 5000
VLAN_ID   = None                           # e.g., 123 if your experiment LAN is VLAN-tagged
DUR_S, PPS, PAYLOAD = 20, 5000, 128

def l2_hdr():
    eth = Ether(src=get_if_hwaddr(IFACE), dst=SERVER_MAC)
    if VLAN_ID is None:
        return eth                              # <-- no extra Raw()
    else:
        return eth / Dot1Q(vlan=VLAN_ID)        # <-- 802.1Q tag when needed


def send_flow(name, sport, use_tcp=False):
    payload = os.urandom(PAYLOAD)
    l3 = IP(src=get_if_addr(IFACE), dst=RUNTIME_IP)
    l4 = TCP(sport=sport, dport=DST_PORT, flags="S") if use_tcp else UDP(sport=sport, dport=DST_PORT)
    pkt = l2_hdr() / l3 / l4 / Raw(payload)

    inter = 1.0 / PPS
    t_end = time.time() + DUR_S
    sent = 0
    while time.time() < t_end:
        sendp(pkt, iface=IFACE, verbose=False)
        sent += 1
        if inter > 0: time.sleep(inter)
    print(f"{name} sent ~{sent} pkts on {IFACE} -> {RUNTIME_IP}:{DST_PORT}")

if __name__ == "__main__":
    t1 = Thread(target=send_flow, args=("flowA", 40001, False))  # UDP
    t2 = Thread(target=send_flow, args=("flowB", 50002, True))   # TCP
    t1.start(); t2.start(); t1.join(); t2.join()
