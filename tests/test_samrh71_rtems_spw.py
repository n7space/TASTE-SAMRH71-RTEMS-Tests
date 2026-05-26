#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
from pygdbmi.gdbcontroller import GdbController

REMOTE_PINGER_GDB_SERVER = "100.124.226.3:2331"
REMOTE_PONGER_GDB_SERVER = "100.116.197.30:2331"
PINGER_PARTITION_PATH = 'samrh71-rtems-spw/work/binaries/partition_1'
PONGER_PARTITION_PATH = 'samrh71-rtems-spw/work/binaries/partition_2'

def test_samrh71_rtems_spw():
    common.do_clean_build("samrh71-rtems-spw")

    build = common.do_build("samrh71-rtems-spw", ["samrh71", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    # Step 1 – prepare pinger: reset, load binary and arm breakpoint, but do not
    # continue yet.

    pinger_gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    pinger_gdbmi.write(f"target extended-remote {REMOTE_PINGER_GDB_SERVER}")
    pinger_gdbmi.write(f"file {PINGER_PARTITION_PATH}")
    pinger_gdbmi.write("mon reset")
    pinger_gdbmi.write("load")
    pinger_gdbmi.write(f"b pinger.c:58")

    # Step 2 – prepare ponger: reset, load binary and start it.
    ponger_gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        ponger_gdbmi.write(f"target extended-remote {REMOTE_PONGER_GDB_SERVER}")
        ponger_gdbmi.write(f"file {PONGER_PARTITION_PATH}")
        ponger_gdbmi.write("mon reset")
        ponger_gdbmi.write("load")
        ponger_gdbmi.write("continue", timeout_sec=2)
        time.sleep(1)
        ponger_gdbmi.write("detach")
    finally:
        ponger_gdbmi.exit()

    time.sleep(1)

    # Step 3 – release pinger and wait for the test_result breakpoint.
    common.do_continue_and_verify(pinger_gdbmi)

    # Step 4 – stop the ponger.
    ponger_stop_gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        ponger_stop_gdbmi.write(f"target extended-remote {REMOTE_PONGER_GDB_SERVER}")
        ponger_stop_gdbmi.write("-exec-interrupt")
    finally:
        ponger_stop_gdbmi.exit()

if __name__ == "__main__":
    test_samrh71_rtems_spw()
