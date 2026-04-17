# TASTE-SAMRH71-RTEMS-Tests

A test suite used for the internal validation of TASTE SAMRH71 RTEMS Runtime, created as a part of "Model-Based Execution Platform for Space Applications (MBEP)" project, funded by ESA, Contract 4000146882/24/NL/KK.

The repository organization is as follows:
- tests/* - contains folders with TASTE projects
- (TODO) scripts/* - helper scripts that need to be copied/installed in the test environment
- Makefile - main entry point to launch the 50+ tests and generate reports
- (TODO) traces.csv - CSV file with requirement to test mapping

# Test environment setup

* Prepare test board
 * Using SSH start JLink in one terminal

* Prepare linux machine
 * Execute in terminal `export SAMRH71_REMOTE_GDBSERVER=<test board ip>:2331`

# Executing tests

To execute tests simply execute `make`

## Example test run

    $ make
    python3 -mvenv env
    ./env/bin/pip install -r requirements.txt
    Requirement already satisfied: iniconfig==2.3.0 in ./env/lib/python3.13/site-packages (from -r requirements.txt (line 1)) (2.3.0)
    Requirement already satisfied: packaging==25.0 in ./env/lib/python3.13/site-packages (from -r requirements.txt (line 2)) (25.0)
    Requirement already satisfied: pexpect==4.9.0 in ./env/lib/python3.13/site-packages (from -r requirements.txt (line 3)) (4.9.0)
    Requirement already satisfied: pluggy==1.6.0 in ./env/lib/python3.13/site-packages (from -r requirements.txt (line 4)) (1.6.0)
    Requirement already satisfied: ptyprocess==0.7.0 in ./env/lib/python3.13/site-packages (from -r requirements.txt (line 5)) (0.7.0)
    Requirement already satisfied: pygdbmi==0.11.0.0 in ./env/lib/python3.13/site-packages (from -r requirements.txt (line 6)) (0.11.0.0)
    Requirement already satisfied: Pygments==2.19.2 in ./env/lib/python3.13/site-packages (from -r requirements.txt (line 7)) (2.19.2)
    Requirement already satisfied: pytest==8.4.2 in ./env/lib/python3.13/site-packages (from -r requirements.txt (line 8)) (8.4.2)
    Requirement already satisfied: pyserial==3.5 in ./env/lib/python3.13/site-packages (from -r requirements.txt (line 9)) (3.5)
    make -C tests
    make[1]: Entering directory '/home/taste/projects/TASTE-SAMRH71-RTEMS-Tests/tests'
    ../env/bin/pytest -vvrxXs
    ================================================================ test session starts =================================================================
    platform linux -- Python 3.13.5, pytest-8.4.2, pluggy-1.6.0 -- /home/taste/projects/TASTE-SAMRH71-RTEMS-Tests/env/bin/python3
    cachedir: .pytest_cache
    rootdir: /home/taste/projects/TASTE-SAMRH71-RTEMS-Tests/tests
    collected 1 item

    test_samrh71_rtems_cpu_usage.py::test_samrh71_rtems_cpu_usage PASSED                                                                           [100%]

    ================================================================= 1 passed in 26.82s =================================================================
    make[1]: Leaving directory '/home/taste/projects/TASTE-SAMRH71-RTEMS-Tests/tests'
    $

# (TODO) Testing Serial support

All the tests which require Serial (UART) connection  are disabled by default.
These tests require a development board with configured serial dongle.

## Executing tests

    SAMRH71_RTEMS_SERIAL_ENABLED=1 make

# (TODO) Testing CAN bus support

All the tests which require CAN are disabled by default.
These tests require a development board with configured CAN dongle. To configure dongle on rpi, execute the following command.

	sudo ip link set can1 up type can bitrate 1000000 fd off sample-point 0.875

It is also required to setup ssh-key to ssh without password prompt. If ssh-key is secured by passphrase, then ssh-agent shall be used.

## Executing tests

    SAMRH71_RTEMS_CAN_ENABLED=1 make
