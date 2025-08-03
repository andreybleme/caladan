# lscpu: command to get general L1/L2 cache info

# install perf
sudo apt install linux-intel-iotg-tools-common
sudo apt install linux-tools-5.15.0-131-generic

# ask cloudlab admin to disable turboboost

# run perf to measure L1/L2 cache performance
# https://www.kernel.org/doc/html/latest/admin-guide/perf-usage.html
sudo perf stat -r5 \
  -e cycles \
  -e instructions \
  -e L1-dcache-loads \
  -e L1-dcache-load-misses \
  -e l2_rqsts.references \
  -e l2_rqsts.miss \
  -e LLC-loads \
  -e LLC-load-misses \
  -- ./iokerneld

sudo perf stat \
  -e cycles \
  -e instructions \
  -e L1-dcache-loads \
  -e L1-dcache-load-misses \
  -e l2_rqsts.references \
  -e l2_rqsts.miss \
  -e LLC-loads \
  -e LLC-load-misses \
  -- ./iokerneld
