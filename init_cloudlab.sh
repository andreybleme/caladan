sudo apt-get update
sudo apt install build-essential libnuma-dev clang autoconf autotools-dev m4 automake libevent-dev  libpcre++-dev libtool ragel libev-dev moreutils parallel cmake python3 python3-pip libjemalloc-dev libaio-dev libdb5.3++-dev numactl hwloc libmnl-dev libnl-3-dev libnl-route-3-dev uuid-dev libssl-dev libcunit1-dev pkg-config
sudo apt install make gcc cmake pkg-config libnl-3-dev libnl-route-3-dev libnuma-dev uuid-dev libssl-dev libaio-dev libcunit1-dev libclang-dev libncurses-dev python3-pyelftools

git clone https://github.com/andreybleme/caladan.git
cd caladan

# install ninja
sudo apt install ninja-build

# install python 3.7+
# Meson works correctly only with python 3.7+. You have python 3.6.9 (default, Mar 10 2023, 16:46:00)
# TODO: try to install from source code https://www.howtogeek.com/install-latest-python-version-on-ubuntu/
scp Downloads/Python-3.12.2.tgz lbleme@ms0804.utah.cloudlab.us:/users/lbleme/
tar xvf Python-3.12.2.tgz
cd Python-3.12.2
./configure --enable-optimizations
sudo make install
# exit and ssh again
python3 --version

# install meson
# upgrading meson version (0.45 doesn't work to build DPDK)
mkdir meson
git clone https://github.com/mesonbuild/meson.git meson
# USE ABSOLUTE PATH!!
#sudo mv /usr/bin/meson /usr/bin/meson-0.56.2 (this was the version apt had previously installed for me)
sudo ln -s /users/lbleme/meson/meson.py /usr/bin/meson


# building DPDK fails DPDK 22.03.0
# meson.build:4:0: ERROR: Function does not take keyword arguments

# buildtools/meson.build:52:8: ERROR: Problem encountered: missing python module: elftools
sudo apt-get install -y python3-pyelftools python-pyelftools
pip3 install pyelftools

# CONFIG_MLX4=y
# CONFIG_DEBUG=y
vi build/config

# (OK) build caladan modules
make submodules

# (OK) build IOKernel (not using MLX3-MLX4)
make clean && make
pushd ksched
make clean && make
popd
sudo ./scripts/setup_machine.sh

# install rust
bash
export PATH="$HOME/.cargo/bin:$PATH"
curl https://sh.rustup.rs -sSf | sh
rustup default nightly

# build syntetic apps (1.79.0-nightly)
# error[E0635]: unknown feature `integer_atomics`
cd apps/synthetic
cargo clean
cargo update
cargo build --release