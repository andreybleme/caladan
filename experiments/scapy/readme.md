sudo python3 perf.py \
  --iface ens1f1np1 \
  --dst-mac 9c:dc:71:5d:51:21 \
  --dst-ip 128.110.218.80 \
  --dst-port 5000 \
  --dur 20 \
  --pps 50000 \
  --payload 128

sudo python3 two_flows_latency_probe.py \
  --iface ens1f1np1 \
  --dst-mac 9c:dc:71:5d:51:21 \
  --dst-ip 128.110.218.80 \
  --dst-port 5000 \
  --dur 20 \
  --pps 50000 \
  --payload 128