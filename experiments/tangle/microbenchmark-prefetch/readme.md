1. Run IOKernels without the prefetch in rx_burst function.
2. Start the IOKernel in the server with perf stat:

```
sudo perf stat -e cycles   -e instructions   -e L1-dcache-loads   -e L1-dcache-load-misses   -e l2_rqsts.references   -e l2_rqsts.miss   -e LLC-loads   -e LLC-load-misses   -- ./iokerneld
```

3. Run the Synthetic traffic generator in client:
```
sudo ./apps/synthetic/target/release/synthetic 128.110.218.116:5000 --config client.config --mode runtime-client --start_mpps=0.005 --mpps=2.5 --samples=20 --rampup=4
```