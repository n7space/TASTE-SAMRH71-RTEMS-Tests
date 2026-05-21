#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
from pygdbmi.gdbcontroller import GdbController


def test_samrh71_rtems_boot_reason():
    common.do_clean_build("samrh71-rtems-boot-reason/samrh71-rtems-fault")
    common.do_clean_build("samrh71-rtems-boot-reason/samrh71-rtems-boot-reason")

    remote_gdb_server = os.getenv("SAMRH71_REMOTE_GDBSERVER", default="127.0.0.1")
    build = common.do_build(
        "samrh71-rtems-boot-reason/samrh71-rtems-fault", ["samrh71", "debug"]
    )
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write(
            "file samrh71-rtems-boot-reason/samrh71-rtems-fault/work/binaries/partition_1"
        )
        common.target_extended_reset(gdbmi)
        gdbmi.write("load")
        gdbmi.write("continue")

        # Wait for remote gdb
        time.sleep(2)
    finally:
        gdbmi.exit()

    build = common.do_build(
        "samrh71-rtems-boot-reason/samrh71-rtems-boot-reason", ["samrh71", "debug"]
    )
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    common.run_verification_project(
        remote_gdb_server,
        "samrh71-rtems-boot-reason/samrh71-rtems-boot-reason/work/binaries/partition_1",
        "function_1.c",
        "24",
    )


if __name__ == "__main__":
    test_samrh71_rtems_boot_reason()
