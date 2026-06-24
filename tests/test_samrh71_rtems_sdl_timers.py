#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
from pygdbmi.gdbcontroller import GdbController


def test_samrh71_rtems_sdl_timers():
    common.do_clean_build("samrh71-rtems-sdl-timers")
    remote_gdb_server = os.getenv("SAMRH71_REMOTE_GDBSERVER", default="127.0.0.1")

    build = common.do_build("samrh71-rtems-sdl-timers", ["samrh71", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    common.run_verification_project(remote_gdb_server, 'samrh71-rtems-sdl-timers/work/binaries/partition_1', 'testfunction.c', '30')

if __name__ == "__main__":
    test_samrh71_rtems_sdl_timers()
