# https://www.cs.kent.edu/~farrell/dist/ref/Netperf.html#0.2.2Z141Z1.SUJSTF.9R2DBD.S
sudo apt install netperf

# latency (req/res perf)
netperf -H 128.110.218.90 -t TCP_RR -l 5

# throughput 
etperf -H 128.110.218.90 -t TCP_STREAM -l 5

# https://blog.jtouzi.net/measuring-network-throughput-netperf-iperf/