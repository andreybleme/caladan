# https://www.cs.kent.edu/~farrell/dist/ref/Netperf.html#0.2.2Z141Z1.SUJSTF.9R2DBD.S
sudo apt install netperf

# latency (req/res perf)
netperf -H 128.110.218.59 -p 5000 -t TCP_RR -l 5

# throughput 
etperf -H 128.110.218.59 -p 5000 -t TCP_STREAM -l 5

# https://blog.jtouzi.net/measuring-network-throughput-netperf-iperf/


### Run netperf DPDK app ===========================
export RTE_SDK=/users/lbleme/caladan/dpdk

# copy from caladan/apps to dpdk submodule folder (use helloword Makefile as reference)
cd ~/caladan/dpdk/examples/dpdk_netperf
cp -r ../../../apps/dpdk_netperf/ .
# create meson.build file

meson configure -Dexamples=dpdk_netperf
ninja

# run the built version
cd ~/caladan/dpdk/build
# server
sudo ./examples/dpdk-dpdk_netperf -l2 --socket-mem=128 -- UDP_SERVER 128.110.218.59
# client
sudo ./examples/dpdk-dpdk_netperf -l2 --socket-mem=128 -- UDP_CLIENT 128.110.218.44 128.110.218.59 50000 8001 10 8 50
