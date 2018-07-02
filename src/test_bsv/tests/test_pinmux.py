# Simple tests for an pinmux module
import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure
#from pinmux_model import pinmux_model
import random


@cocotb.test()
def pinmux_basic_test(dut):
    """Test for 5 + 10"""
    yield Timer(2)

    dut.mux_lines_cell0_mux_in = 1
    dut.mux_lines_cell1_mux_in = 2
    dut.mux_lines_cell2_mux_in = 0
    yield Timer(2)
    dut.EN_mux_lines_cell0_mux = 1
    dut.EN_mux_lines_cell1_mux = 1
    dut.EN_mux_lines_cell2_mux = 1

    yield Timer(2)

    # GPIO
    dut.peripheral_side_gpioa_a2_out_in = 0
    dut.peripheral_side_gpioa_a2_outen_in = 1

    yield Timer(2)

    if dut.iocell_side_io2_cell_out != 0:
        raise TestFailure(
            "gpioa_a2=0/mux=0/out=1 %s iocell_io2 != 0" % \
                    str(dut.iocell_side_io2_cell_out ))

    dut.peripheral_side_gpioa_a2_out_in = 1

    yield Timer(2)

    if dut.iocell_side_io2_cell_out != 1:
        raise TestFailure(
            "gpioa_a2=0/mux=0/out=1 %s iocell_io2 != 1" % \
                    str(dut.iocell_side_io2_cell_out ))

    # UART
    yield Timer(2)
    dut.peripheral_side_uart_tx_in = 1
    dut.peripheral_side_gpioa_a0_outen_in = 1

    yield Timer(2)

    if dut.iocell_side_io0_cell_out != 1:
        raise TestFailure(
            "uart_tx=1/mux=0/out=1 %s iocell_io0 != 1" % \
                    str(dut.iocell_side_io0_cell_out ))

    dut.peripheral_side_uart_tx_in = 0

    yield Timer(2)

    if dut.iocell_side_io0_cell_out != 0:
        raise TestFailure(
            "uart_tx=0/mux=0/out=1 %s iocell_io0 != 0" % \
                    str(dut.iocell_side_io0_cell_out ))

    dut._log.info("Ok!")
    yield Timer(2)


@cocotb.test()
def pinmux_randomised_test(dut):
    """Test for adding 2 random numbers multiple times"""

    return

    yield Timer(2)

    for i in range(10):
        A = random.randint(0, 15)
        B = random.randint(0, 15)

        dut.A = A
        dut.B = B

        yield Timer(2)

        if int(dut.X) != pinmux_model(A, B):
            raise TestFailure(
                "Randomised test failed with: %s + %s = %s" %
                (int(dut.A), int(dut.B), int(dut.X)))
        else:  # these last two lines are not strictly necessary
            dut._log.info("Ok!")
