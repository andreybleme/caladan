Regular Caladan, without using two queues and without caching ip_to_procs. Base repo cloned poiting to commit `001d4a0bca0581952d772e6368d3d7ee5872e053`.

Log data generated with synthetic application:

```
$ sudo ./apps/synthetic/target/release/synthetic 128.110.218.185:5000 --config client.config --mode runtime-client --start_mpps=0.005 --mpps=2.5 --samples=20 --rampup=4 --intersample_sleep=2
```

Bucket logs generated with the flag `--output=buckets`