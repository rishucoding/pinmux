# Simple tests for an pinmux module
import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure
#from pinmux_model import pinmux_model
import random


""" dut is design under test """


@cocotb.test()
def pinmux_basic_test(dut):
    """Test for 5 + 10"""
    yield Timer(2)
    # mux selection lines, each input two bit wide
    dut.mux_lines_cell0_mux_in = 1
    dut.mux_lines_cell1_mux_in = 2
    dut.mux_lines_cell2_mux_in = 0
    yield Timer(2)
    # enable input for mux
    dut.EN_mux_lines_cell0_mux = 1
    dut.EN_mux_lines_cell1_mux = 1
    dut.EN_mux_lines_cell2_mux = 1

    yield Timer(2)

    # GPIO2-out test
    # GPIO is inout peripheral
    dut.peripheral_side_gpioa_a2_out_in = 0
    dut.peripheral_side_gpioa_a2_outen_in = 1

    yield Timer(2)

    if dut.iocell_side_io2_cell_out != 0:  # output of iopad
        raise TestFailure(
            "gpioa_a2=0/mux=0/out=1 %s iocell_io2 != 0" %
            str(dut.iocell_side_io2_cell_out))

    dut.peripheral_side_gpioa_a2_out_in = 1

    yield Timer(2)

    if dut.iocell_side_io2_cell_out != 1:
        raise TestFailure(
            "gpioa_a2=0/mux=0/out=1 %s iocell_io2 != 1" %
            str(dut.iocell_side_io2_cell_out))

    # GPIO2-in test (first see if it's tri-state)
    if str(dut.peripheral_side_gpioa_a2_in) != "x":
        raise TestFailure(
            "gpioa_a2=0/mux=0/out=1 %s gpio_a2_in != x" %
            str(dut.peripheral_side_gpioa_a2_in))

    dut.peripheral_side_gpioa_a2_outen_in = 0
    dut.iocell_side_io2_cell_in_in = 0
    yield Timer(2)

    if dut.peripheral_side_gpioa_a2_in != 0:
        raise TestFailure(
            "iocell_io2=0/mux=0/out=0 %s gpioa_a2 != 0" %
            str(dut.peripheral_side_gpioa_a2_in))

    dut.iocell_side_io2_cell_in_in = 1
    yield Timer(2)

    if dut.peripheral_side_gpioa_a2_in != 1:
        raise TestFailure(
            "iocell_io2=1/mux=0/out=0 %s gpioa_a2 != 1" %
            str(dut.peripheral_side_gpioa_a2_in))

    dut.peripheral_side_gpioa_a2_outen_in = 1
    dut.iocell_side_io2_cell_in_in = 0
    yield Timer(2)
    dut._log.info("gpioa_a2_in %s" % dut.peripheral_side_gpioa_a2_in)

    if dut.iocell_side_io2_cell_out != 1:
        raise TestFailure(
            "gpioa_a2=0/mux=0/out=1 %s iocell_io2 != 1" %
            str(dut.iocell_side_io2_cell_out))

    # UART
    yield Timer(2)
    dut.peripheral_side_uart_tx_in = 1
    dut.peripheral_side_gpioa_a0_outen_in = 1

    yield Timer(2)

    if dut.iocell_side_io0_cell_out != 1:
        raise TestFailure(
            "uart_tx=1/mux=0/out=1 %s iocell_io0 != 1" %
            str(dut.iocell_side_io0_cell_out))

    dut.peripheral_side_uart_tx_in = 0

    yield Timer(2)

    if dut.iocell_side_io0_cell_out != 0:
        raise TestFailure(
            "uart_tx=0/mux=0/out=1 %s iocell_io0 != 0" %
            str(dut.iocell_side_io0_cell_out))

    yield Timer(2)

    # TWI
    yield Timer(2)
    # define input variables
    dut.peripheral_side_twi_sda_out_in = 0
    dut.peripheral_side_twi_sda_outen_in = 1

    yield Timer(2)
    # Test for out for twi_sda
    if dut.iocell_side_io1_cell_out != 0:
        raise TestFailure(
            "twi_sda=0/mux=0/out=1 %s iocell_io1 != 0" %
            str(dut.iocell_side_io1_cell_out))

    dut.peripheral_side_twi_sda_out_in = 1

    if dut.iocell_side_io1_cell_out != 1:
        raise TestFailure(
            "twi_sda=0/mux=0/out=1 %s iocell_io1 != 0" %
            str(dut.iocell_side_io1_cell_out))

    # Test for in
    # first check for tristate
    if str(dut.peripheral_side_twi_sda_in) != "x":
        raise TestFailure(
            "twi_sda=0/mux=0/out=1 %s twi_sda_in != x" %
            str(dut.peripheral_side_twi_sda_in))

    dut.peripheral_side_twi_sda_outen_in = 0
    dut.iocell_side_io1_cell_in_in = 0
    yield Timer(2)

    if dut.peripheral_side_twi_sda_in != 0:
        raise TestFailure(
            "iocell_io1=0/mux=0/out=0 %s twi_sda != 0" %
            str(dut.peripheral_side_twi_sda_in))

    dut.iocell_side_io1_cell_in_in = 1
    yield Timer(2)

    if dut.peripheral_side_twi_sda_in != 1:
        raise TestFailure(
            "iocell_io1=0/mux=0/out=0 %s twi_sda != 0" %
            str(dut.peripheral_side_twi_sda_in))

    dut.peripheral_side_twi_sda_outen_in = 1
    dut.iocell_side_io1_cell_in_in = 0
    yield Timer(2)
    dut._log.info("twi_sda_in %s" % dut.peripheral_side_twi_sda_in)

    if dut.iocell_side_io1_cell_out != 1:
        raise TestFailure(
            "twi_sda=0/mux=0/out=1 %s iocell_io1 != 1" %
            str(dut.iocell_side_io1_cell_out))

    yield Timer(2)

    # Test for out for twi_scl
    dut.peripheral_side_twi_scl_out_in = 0
    dut.peripheral_side_twi_scl_outen_in = 1
    if dut.iocell_side_io2_cell_out != 0:
        raise TestFailure(
            "twi_scl=0/mux=0/out=1 %s iocell_io2 != 0" %
            str(dut.iocell_side_io2_cell_out))

    dut.peripheral_side_twi_scl_out_in = 1

    if dut.iocell_side_io2_cell_out != 1:
        raise TestFailure(
            "twi_scl=0/mux=0/out=1 %s iocell_io2 != 0" %
            str(dut.iocell_side_io2_cell_out))

    # Test for in
    # first check for tristate
    if str(dut.peripheral_side_twi_scl_in) != "x":
        raise TestFailure(
            "twi_scl=0/mux=0/out=1 %s twi_scl_in != x" %
            str(dut.peripheral_side_twi_scl_in))

    dut.peripheral_side_twi_scl_outen_in = 0
    dut.iocell_side_io2_cell_in_in = 0
    yield Timer(2)

    if dut.peripheral_side_twi_scl_in != 0:
        raise TestFailure(
            "iocell_io2=0/mux=0/out=0 %s twi_scl != 0" %
            str(dut.peripheral_side_twi_scl_in))

    dut.iocell_side_io2_cell_in_in = 1
    yield Timer(2)

    if dut.peripheral_side_twi_scl_in != 1:
        raise TestFailure(
            "iocell_io2=1/mux=0/out=0 %s twi_scl != 1" %
            str(dut.peripheral_side_twi_scl_in))

    dut.peripheral_side_twi_scl_outen_in = 1
    dut.iocell_side_io2_cell_in_in = 0
    yield Timer(2)
    dut._log.info("twi_scl_in %s" % dut.peripheral_side_twi_scl_in)

    if dut.iocell_side_io2_cell_out != 1:
        raise TestFailure(
            "twi_scl=0/mux=0/out=1 %s iocell_io2 != 1" %
            str(dut.iocell_side_io2_cell_out))

    yield Timer(2)

    dut._log.info("Ok!")

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
