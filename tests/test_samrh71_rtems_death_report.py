#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
from pygdbmi.gdbcontroller import GdbController


def test_samrh71_rtems_death_report():
    common.do_clean_build("samrh71-rtems-death-report/samrh71-fault")
    common.do_clean_build("samrh71-rtems-death-report/samrh71-verify-fault")
    remote_gdb_server = os.getenv("SAMRH71_REMOTE_GDBSERVER", default="127.0.0.1")
    build = common.do_build(
        "samrh71-rtems-death-report/samrh71-fault", ["samrh71", "debug"]
    )
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write(
            "file samrh71-rtems-death-report/samrh71-fault/work/binaries/partition_1"
        )
        common.target_extended_reset(gdbmi)
        gdbmi.write("load")
        gdbmi.write("continue")

        # Wait for remote gdb
        time.sleep(2)
    finally:
        gdbmi.exit()

    build = common.do_build(
        "samrh71-rtems-death-report/samrh71-verify-fault", ["samrh71", "debug"]
    )
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    common.run_verification_project(
        remote_gdb_server,
        "samrh71-rtems-death-report/samrh71-verify-fault/work/binaries/partition_1",
        "function_1.c",
        "57",
    )


if __name__ == "__main__":
    test_samrh71_rtems_death_report()
