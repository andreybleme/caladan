# Script tested on xl170 Cloudlab machine (https://docs.cloudlab.us/hardware.html)

# Ubuntu 22.04.2 LTS (GNU/Linux 5.15.0-86-generic x86_64)
# ssh -i ~/.ssh/id_cloudlab lbleme@hp109.utah.cloudlab.us
sudo apt-get update
sudo apt install -y build-essential libnuma-dev clang autoconf autotools-dev m4 automake libevent-dev  libpcre++-dev libtool ragel libev-dev moreutils parallel cmake python3 python3-pip libjemalloc-dev libaio-dev libdb5.3++-dev numactl hwloc libmnl-dev libnl-3-dev libnl-route-3-dev uuid-dev libssl-dev libcunit1-dev pkg-config
sudo apt install -y make gcc cmake pkg-config libnl-3-dev libnl-route-3-dev libnuma-dev uuid-dev libssl-dev libaio-dev libcunit1-dev libclang-dev libncurses-dev python3-pyelftools

# Install MLNX OFED driver (https://network.nvidia.com/products/infiniband-drivers/linux/mlnx_ofed/)
scp Downloads/MLNX_OFED_LINUX-5.8-5.1.1.2-ubuntu22.04-x86_64.tgz lbleme@hp092.utah.cloudlab.us:/users/lbleme/
tar -xvzf MLNX_OFED_LINUX-5.8-5.1.1.2-ubuntu22.04-x86_64.tgz
sudo ./mlnxofedinstall --upstream-libs --dpdk

# Update RSS config for MLX4 (https://docs.nvidia.com/networking/display/mlnxofedv461000/rss+support)
sudo ethtool -X eno49np0 hfunc xor
sudo ethtool --show-rxfh eno49np0
# ethtool commands (https://docs.nvidia.com/networking/display/mlnxofedv461000/ethtool#src-12013419_Ethtool-EthtoolSupportedOptionsTable)
sudo ethtool -i eno49np0


# install ninja
sudo apt install -y ninja-build

# step can be skipped if Python version is already 3.7+
# install python 3.7+
# Meson works correctly only with python 3.7+. You have python 3.6.9 (default, Mar 10 2023, 16:46:00)
# install from source code https://www.howtogeek.com/install-latest-python-version-on-ubuntu/
scp Downloads/Python-3.12.2.tgz lbleme@hp144.utah.cloudlab.us:/users/lbleme/
tar xvf Python-3.12.2.tgz
cd Python-3.12.2
./configure --enable-optimizations
sudo make install
# exit and ssh again
python3 --version

# install meson from source
# upgrading meson version (0.45 doesn't work to build DPDK)
mkdir meson
git clone https://github.com/mesonbuild/meson.git meson
# USE ABSOLUTE PATH!!
sudo ln -s /users/lbleme/meson/meson.py /usr/bin/meson


# building DPDK fails DPDK 22.03.0
# meson.build:4:0: ERROR: Function does not take keyword arguments

# buildtools/meson.build:52:8: ERROR: Problem encountered: missing python module: elftools
sudo apt-get install -y python3-pyelftools python-pyelftools
pip3 install pyelftools

git clone https://github.com/andreybleme/caladan.git
cd caladan
git pull
git checkout feature/iokernels

# update server.config with IP address $ ip a
vi server.config

# update client.config
vi client.config

# update build config to DEBUG and MLX5 driver
# CONFIG_MLX5=y - build/shared.mk:56: *** mlx4 support is not available currently.  Stop.
# CONFIG_DEBUG=y
vi build/config

# update DPDK to use port 1
# L260 dp.port = 1;
vi iokernel/dpdk.c

# (OK) build caladan modules
make submodules

# (OK) build IOKernel
make clean && make # gcc -T ./base/base.ld -rdynamic -o tests/test_runtime_timer tests/test_runtime_timer.o ./libruntime.a ./libnet.a ./libbase.a -lpthrea
pushd ksched
make clean && make
popd
sudo ./scripts/setup_machine.sh

# install rust
bash
curl https://sh.rustup.rs -sSf | sh
export PATH="$HOME/.cargo/bin:$PATH"
rustup default nightly

# ===== IOKernel 2 =====
mkdir caladan-b
git clone https://github.com/andreybleme/caladan.git
cd caladan
git pull
git checkout feature/iokernels
# use iok_b.c files
rm iokernel/control_iok_b.c
rm iokernel/sched_iok_b.c
rm iokernel/rx_iok_b.c
rm iokernel/tx_iok_b.c
rm iokernel/dp_clients_iok_b.c
rm iokernel/dpdk_iok_b.c
rm iokernel/main_iok_b.c

rm iokernel/control.c
rm iokernel/sched.c
rm iokernel/rx.c
rm iokernel/tx.c
rm iokernel/dp_clients.c
rm iokernel/dpdk.c
rm iokernel/main.c

mv iokernel/control_iok_b.c iokernel/control.c
mv iokernel/sched_iok_b.c iokernel/sched.c
mv iokernel/rx_iok_b.c iokernel/rx.c
mv iokernel/tx_iok_b.c iokernel/tx.c
mv iokernel/dp_clients_iok_b.c iokernel/dp_clients.c
mv iokernel/dpdk_iok_b.c iokernel/dpdk.c
mv iokernel/main_iok_b.c iokernel/main.c

# copy app/sysnthetic from original caladan
cd caladan
rm -fr apps/synthetic/
cp -r ../caladan-original/caladan/apps/synthetic/ apps/

# build syntetic apps (1.79.0-nightly)
cd apps/synthetic
cargo clean
cargo update
cargo build --release
# if error[E0635]: unknown feature `integer_atomics`
# remove line  #![feature(integer_atomics)]
# vi src/main.rs:1:12 

# start iokerneld
sudo ./iokerneld
# run server app
sudo ./apps/synthetic/target/release/synthetic 128.110.218.219:5000 --config server.config --mode spawner-server

# run client app (always use IP from server node)
sudo ./apps/synthetic/target/release/synthetic 128.110.218.219:5000 --config client.config --mode runtime-client

# server (node-0): 128.110.218.219/21 (multi iokernels)
# client (node-1): 128.110.218.118/21

# iok A
# sched: dataplane on 10, control on 0
# sched: iokernel a using 10 CPU

# iok B
# sched: dataplane on 9, control on 19
# sched: iokernel b using 10 CPU