# (OK) build IOKernel
make clean && make
cd ksched
make clean && make
cd ..
sudo ./scripts/setup_machine.sh