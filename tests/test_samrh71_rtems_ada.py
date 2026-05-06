#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
import pytest
from pygdbmi.gdbcontroller import GdbController


@pytest.mark.skipif(
    not os.getenv("SAMRH71_RTEMS_ADA_ENABLED"),
    reason="Ada is not enabled on current platform",
)
def test_samrh71_rtems_ada():
    common.do_clean_build("samrh71-rtems-ada")
    remote_gdb_server = os.getenv("SAMRH71_REMOTE_GDBSERVER", default="127.0.0.1")

    build = common.do_build("samrh71-rtems-ada", ["samrh71", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    common.run_verification_project(remote_gdb_server, 'samrh71-rtems-ada/work/binaries/partition_1', 'pinger.c', '22')

if __name__ == "__main__":
    test_samrh71_rtems_ada()
