Regular Caladan, without using two queues and without caching ip_to_procs. Base repo cloned poiting to commit `001d4a0bca0581952d772e6368d3d7ee5872e053`.

Log data generated with synthetic application using a bimodal distribution:
(99% light reqs 83 fake work, 1% heavy reqs 918 fake work)

```
$ sudo ./apps/synthetic/target/release/synthetic 128.110.218.140:5000 --config client.config --mode runtime-client --start_mpps=0.005 --mpps=4.00 --samples=20 --rampup=4 --intersample_sleep=2 --distspec=bimodal:0.99:83:918
```

Bucket logs generated with the flag `--output=buckets`