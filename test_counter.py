import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles, ReadOnly
from cocotb_tools.runner import get_runner

LANGUAGE = os.getenv("TOPLEVEL_LANG","verilog").lower().strip()

@cocotb.test()
async def counter(dut):
    dut.enable.value = 0
    dut.rst_n.value = 0

    clock = Clock(dut.clk, 10, unit="us")
    clock.start(start_high=False)

    await ClockCycles(dut.clk, 2) 
    dut.rst_n.value = 1 
    await RisingEdge(dut.clk)

    dut.enable.value = 1
    await ClockCycles(dut.clk, 10)
    await ReadOnly()
    assert dut.dout.value == 0, f"dout = {dut.dout.value}, expected 0"
    assert dut.carry.value == 1, f"carry = {dut.carry.value}, expected 1"

def test_counter_runner():
    sim = os.getenv("SIM", "icarus")      # 我只在这台机器上找到了 verilator，没找到 iverilog
    proj_path = Path(__file__).resolve().parent

    sources = [proj_path / "counter.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="top_counter",          # 模块名，不是文件名
        always=True,
        timescale=("1ns", "1ps"),
        waves=True,
    )
    runner.test(
        hdl_toplevel="top_counter",
        test_module="test_counter",          # 这个 .py 文件的名字（不带 .py）
        waves=True,
    )


if __name__ == "__main__":
    test_counter_runner()