#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
import pygdbmi
import pytest
from pygdbmi.gdbcontroller import GdbController


def is_breakpoint_hit(response, function):
    return (
        response["type"] == "notify"
        and response["message"] == "stopped"
        and "payload" in response
        and "reason" in response["payload"]
        and response["payload"]["reason"] == "breakpoint-hit"
        and "frame" in response["payload"]
        and "func" in response["payload"]["frame"]
        and response["payload"]["frame"]["func"] == function
    )


def wait_for_breakpoint(gdbmi, timeout, function):
    start_time = time.time()
    elapsed_time = 0
    breakpoint_hit = False
    try:
        while not breakpoint_hit:
            resp = gdbmi.get_gdb_response(timeout_sec=timeout - elapsed_time)
            if [response for response in resp if is_breakpoint_hit(response, function)]:
                return True
            elapsed_time = time.time() - start_time
    except pygdbmi.constants.GdbTimeoutError:
        pass
    return False


@pytest.mark.skipif(
    not os.getenv("SAMRH71_RTEMS_CAN_ENABLED"),
    reason="CAN is not enabled on current platform",
)
def test_samrh71_rtems_can_simple():
    remote_gdb_server = os.getenv("SAMRH71_REMOTE_GDBSERVER", default="127.0.0.1")
    common.do_clean_build("samrh71-rtems-can/samrh71-rtems-can-simple")
    build = common.do_build(
        "samrh71-rtems-can/samrh71-rtems-can-simple", ["samrh71", "debug"]
    )
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write(
            "file samrh71-rtems-can/samrh71-rtems-can-simple/work/binaries/partition_1"
        )
        common.target_extended_reset(gdbmi)
        gdbmi.write("load")
        gdbmi.write("-break-insert cubesat_PI_alive", timeout_sec=2)
        gdbmi.write("-exec-continue", timeout_sec=2)

        expected = [
            "  can0  RX - -  000000CE   [2]  00 00",
            "  can0  RX - -  000000CE   [2]  00 01",
            "  can0  RX - -  000000CE   [2]  00 02",
            "  can0  RX - -  000000CE   [2]  00 03",
            "  can0  RX - -  000000CE   [2]  00 04",
        ]

        errors = common.do_execute(
            "samrh71-rtems-can",
            expected,
            test_exe="test_samrh71_rtems_can_simple.sh",
        )

        assert not errors, "\n".join(errors)

        expected = ["Frame sent"]
        errors = common.do_execute(
            "samrh71-rtems-can",
            expected,
            test_exe="test_samrh71_rtems_can_simple_recv.sh",
        )

        assert not errors, "\n".join(errors)

        assert wait_for_breakpoint(gdbmi, 10, "cubesat_PI_alive")

    finally:
        gdbmi.exit()


@pytest.mark.skipif(
    not os.getenv("SAMRH71_RTEMS_CAN_ENABLED"),
    reason="CAN is not enabled on current platform",
)
def test_samrh71_rtems_can_static():
    remote_gdb_server = os.getenv("SAMRH71_REMOTE_GDBSERVER", default="127.0.0.1")
    common.do_clean_build("samrh71-rtems-can/samrh71-rtems-can-static")
    build = common.do_build(
        "samrh71-rtems-can/samrh71-rtems-can-static", ["samrh71", "debug"]
    )
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write(
            "file samrh71-rtems-can/samrh71-rtems-can-static/work/binaries/partition_1"
        )
        common.target_extended_reset(gdbmi)
        gdbmi.write("load")
        gdbmi.write("-break-insert cubesat_PI_alive", timeout_sec=2)
        gdbmi.write("-exec-continue", timeout_sec=2)

        expected = [
            "  can0  RX - -  0BB   [2]  00 00",
            "  can0  RX - -  0BB   [2]  00 01",
            "  can0  RX - -  0BB   [2]  00 02",
            "  can0  RX - -  0BB   [2]  00 03",
            "  can0  RX - -  0BB   [2]  00 04",
        ]

        errors = common.do_execute(
            "samrh71-rtems-can",
            expected,
            test_exe="test_samrh71_rtems_can_static.sh",
        )

        assert not errors, "\n".join(errors)

        expected = ["Frame sent"]
        errors = common.do_execute(
            "samrh71-rtems-can",
            expected,
            test_exe="test_samrh71_rtems_can_static_recv.sh",
        )

        assert not errors, "\n".join(errors)

        assert wait_for_breakpoint(gdbmi, 10, "cubesat_PI_alive")

    finally:
        gdbmi.exit()


@pytest.mark.skipif(
    not os.getenv("SAMRH71_RTEMS_CAN_ENABLED"),
    reason="CAN is not enabled on current platform",
)
def test_samrh71_rtems_can_escaper():
    remote_gdb_server = os.getenv("SAMRH71_REMOTE_GDBSERVER", default="127.0.0.1")
    common.do_clean_build("samrh71-rtems-can/samrh71-rtems-can-escaper")
    build = common.do_build(
        "samrh71-rtems-can/samrh71-rtems-can-escaper", ["samrh71", "debug"]
    )
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write(
            "file samrh71-rtems-can/samrh71-rtems-can-escaper/work/binaries/partition_1"
        )
        common.target_extended_reset(gdbmi)
        gdbmi.write("load")
        gdbmi.write("-break-insert cubesat_PI_alive", timeout_sec=2)
        gdbmi.write("-exec-continue", timeout_sec=2)

        expected = [
            "  can0  RX - -  141   [8]  00 FE 00 FE 00 FE 00 BB",
            "  can0  RX - -  141   [8]  FE 00 CC FE 00 DD FE 00",
            "  can0  RX - -  141   [2]  EE FF",
            "  can0  RX - -  141   [8]  00 FE 00 01 FE 00 BB FE",
            "  can0  RX - -  141   [8]  00 CC FE 00 DD FE 00 EE",
            "  can0  RX - -  141   [1]  FF",
        ]

        errors = common.do_execute(
            "samrh71-rtems-can",
            expected,
            test_exe="test_samrh71_rtems_can_escaper.sh",
        )

        assert not errors, "\n".join(errors)

        expected = ["Frame sent"]
        errors = common.do_execute(
            "samrh71-rtems-can",
            expected,
            test_exe="test_samrh71_rtems_can_escaper_recv.sh",
        )

        assert not errors, "\n".join(errors)

        assert wait_for_breakpoint(gdbmi, 10, "cubesat_PI_alive")

    finally:
        gdbmi.exit()

@pytest.mark.skipif(
    not os.getenv("SAMRH71_RTEMS_CAN_ENABLED"),
    reason="CAN is not enabled on current platform",
)
def test_samrh71_rtems_can_adapter():
    remote_gdb_server = os.getenv("SAMRH71_REMOTE_GDBSERVER", default="127.0.0.1")
    common.do_clean_build("samrh71-rtems-can/samrh71-rtems-can-adapter")
    build = common.do_build(
        "samrh71-rtems-can/samrh71-rtems-can-adapter", ["samrh71", "debug"]
    )
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write(
            "file samrh71-rtems-can/samrh71-rtems-can-adapter/work/binaries/partition_1"
        )
        common.target_extended_reset(gdbmi)
        gdbmi.write("load")
        gdbmi.write("-break-insert cubesat_PI_alive", timeout_sec=2)
        gdbmi.write("-exec-continue", timeout_sec=2)

        expected = [
            "  can0  TX - -  142   [1]  00",
            "  can0  RX - -  065   [2]  01 00",
            "  can0  TX - -  142   [3]  01 03 05",
            "  can0  RX - -  065   [2]  03 09",
            "  can0  TX - -  142   [2]  CC CC",
            "  can0  RX - -  065   [2]  02 99",
        ]

        errors = common.do_execute(
            "samrh71-rtems-can",
            expected,
            test_exe="test_samrh71_rtems_can_adapter.sh",
        )

        assert not errors, "\n".join(errors)

    finally:
        gdbmi.exit()

@pytest.mark.skipif(
    not os.getenv("SAMRH71_RTEMS_CAN_ENABLED"),
    reason="CAN is not enabled on current platform",
)
def test_samrh71_rtems_can_sizes():
    remote_gdb_server = os.getenv("SAMRH71_REMOTE_GDBSERVER", default="127.0.0.1")
    common.do_clean_build("samrh71-rtems-can/samrh71-rtems-can-sizes")
    build = common.do_build(
        "samrh71-rtems-can/samrh71-rtems-can-sizes", ["samrh71", "debug"]
    )
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write(
            "file samrh71-rtems-can/samrh71-rtems-can-sizes/work/binaries/partition_1"
        )
        common.target_extended_reset(gdbmi)
        gdbmi.write("load")
        gdbmi.write("-break-insert cubesat_PI_alive", timeout_sec=2)
        gdbmi.write("-exec-continue", timeout_sec=2)

        expected = [
            "  can0  TX - -  099   [0] ",
            "  can0  RX - -  0A0   [0] ",
            "  can0  TX - -  098   [1]  01",
            "  can0  RX - -  0A0   [1]  01",
            "  can0  TX - -  097   [2]  01 02",
            "  can0  RX - -  0A0   [2]  01 02",
            "  can0  TX - -  096   [3]  01 02 03",
            "  can0  RX - -  0A0   [3]  01 02 03",
            "  can0  TX - -  095   [4]  01 02 03 04",
            "  can0  RX - -  0A0   [4]  01 02 03 04",
            "  can0  TX - -  094   [5]  01 02 03 04 05",
            "  can0  RX - -  0A0   [5]  01 02 03 04 05",
            "  can0  TX - -  093   [6]  01 02 03 04 05 06",
            "  can0  RX - -  0A0   [6]  01 02 03 04 05 06",
            "  can0  TX - -  092   [7]  01 02 03 04 05 06 07",
            "  can0  RX - -  0A0   [7]  01 02 03 04 05 06 07",
            "  can0  TX - -  091   [8]  01 02 03 04 05 06 07 08",
            "  can0  RX - -  0A0   [8]  01 02 03 04 05 06 07 08",
        ]

        errors = common.do_execute(
            "samrh71-rtems-can",
            expected,
            test_exe="test_samrh71_rtems_can_sizes.sh",
        )

        assert not errors, "\n".join(errors)

    finally:
        gdbmi.exit()


if __name__ == "__main__":
    test_samrh71_rtems_can_simple()
    test_samrh71_rtems_can_static()
    test_samrh71_rtems_can_escaper()
    test_samrh71_rtems_can_adapter()
    test_samrh71_rtems_can_sizes()
