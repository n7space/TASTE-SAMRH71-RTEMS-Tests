#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
import pytest
from pygdbmi.gdbcontroller import GdbController


@pytest.mark.skipif(
    not os.getenv("SAMRH71_RTEMS_SERIAL_ENABLED"),
    reason="Serial is not enabled on current platform",
)
def test_samrh71_rtems_twin_serial():
    common.do_clean_build("samrh71-rtems-twin-serial")
    remote_gdb_server = os.getenv("SAMRH71_REMOTE_GDBSERVER", default="127.0.0.1")
    build = common.do_build("samrh71-rtems-twin-serial", ["samrh71", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write("file samrh71-rtems-twin-serial/work/binaries/partition_2")
        common.target_extended_reset(gdbmi)
        gdbmi.write("load")
        gdbmi.write("continue")

        # Wait for remote gdb
        time.sleep(2)

        expected = [
            "Got response from UART3: 1",
            "Got response from UART3: 2",
            "Got response from UART1: 3",
            "Got response from UART1: 4",
        ]

        errors = common.do_execute(
            "samrh71-rtems-twin-serial", expected, test_exe="work/binaries/partition_1"
        )
    finally:
        gdbmi.exit()
    assert not errors, "\n".join(errors)


if __name__ == "__main__":
    test_samrh71_rtems_twin_serial()
