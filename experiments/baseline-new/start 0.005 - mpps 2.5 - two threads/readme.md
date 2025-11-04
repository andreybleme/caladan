Log data generated with synthetic application:

```
$ sudo ./apps/synthetic/target/release/synthetic 128.110.218.185:5000 --config client.config --mode runtime-client --start_mpps=0.005 --mpps=2.5 --samples=20 --rampup=4 --intersample_sleep=2 --threads 2 --transport udp
```

Bucket logs generated with the flag `--output=buckets`