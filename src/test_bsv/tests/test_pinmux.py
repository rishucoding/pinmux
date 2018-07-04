# Simple tests for an pinmux module
import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure
#from pinmux_model import pinmux_model
import random


""" dut is design under test """

"""
for gpio2, there are three ports at peripheral side:
    peripheral_side_gpioa_a2_out_in
    peripheral_side_gpioa_a2_outen_in
    peripheral_side_gpioa_a2_in
"""


@cocotb.test()
def pinmux_gpio2(dut):
    """Test for GPIO2"""
    yield Timer(2)
    # mux selection lines, each input two bit wide
    dut.mux_lines_cell2_mux_in = 0
    yield Timer(2)
    # enable input for mux
    dut.EN_mux_lines_cell0_mux = 0
    dut.EN_mux_lines_cell1_mux = 0
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
    #
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

    dut._log.info("Ok!, gpio2 passed")


@cocotb.test()
def pinmux_uart(dut):
    """Test for UART"""
    yield Timer(2)
    # mux selection lines, each input two bit wide
    dut.mux_lines_cell0_mux_in = 1
    yield Timer(2)
    # enable input for mux
    dut.EN_mux_lines_cell0_mux = 1
    dut.EN_mux_lines_cell1_mux = 0
    dut.EN_mux_lines_cell2_mux = 0

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

    dut._log.info("Ok!, uart passed")


@cocotb.test()
def pinmux_twi_scl(dut):
    """Test for I2C SCL"""
    yield Timer(2)
    # mux selection lines, each input two bit wide
    dut.mux_lines_cell2_mux_in = 2
    yield Timer(2)
    # enable input for mux
    dut.EN_mux_lines_cell0_mux = 0
    dut.EN_mux_lines_cell1_mux = 0
    dut.EN_mux_lines_cell2_mux = 1

    yield Timer(2)

    # Test for out for twi_scl
    dut.peripheral_side_twi_scl_out_in = 0
    dut.peripheral_side_twi_scl_outen_in = 1
    yield Timer(2)

    if dut.iocell_side_io2_cell_out != 0:
        raise TestFailure(
            "twi_scl=0/mux=0/out=1 %s iocell_io2 != 0" %
            str(dut.iocell_side_io2_cell_out))

    dut.peripheral_side_twi_scl_out_in = 1
    yield Timer(2)

    if dut.iocell_side_io2_cell_out != 1:
        raise TestFailure(
            "twi_scl=0/mux=0/out=1 %s iocell_io2 != 0" %
            str(dut.iocell_side_io2_cell_out))

    dut._log.info("twi_scl_in %s" % dut.peripheral_side_twi_scl_in)

    # Test for in
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

    dut._log.info("Ok!, twi_scl passed")


@cocotb.test()
def pinmux_twi_sda(dut):
    """Test for I2C"""
    yield Timer(2)
    # mux selection lines, each input two bit wide
    dut.mux_lines_cell1_mux_in = 2
    yield Timer(2)
    # enable input for mux
    dut.EN_mux_lines_cell0_mux = 0
    dut.EN_mux_lines_cell1_mux = 1
    dut.EN_mux_lines_cell2_mux = 0

    # TWI
    yield Timer(2)
    # define input variables
    dut.peripheral_side_twi_sda_out_in = 0
    dut.peripheral_side_twi_sda_outen_in = 1

    yield Timer(2)

    dut._log.info("io1_out %s" % dut.iocell_side_io1_cell_out)
    # Test for out for twi_sda
    if dut.iocell_side_io1_cell_out != 0:
        raise TestFailure(
            "twi_sda=0/mux=0/out=1 %s iocell_io1 != 0" %
            str(dut.iocell_side_io1_cell_out))

    dut.peripheral_side_twi_sda_out_in = 1
    yield Timer(2)

    if dut.iocell_side_io1_cell_out != 1:
        raise TestFailure(
            "twi_sda=1/mux=0/out=1 %s iocell_io1 != 1" %
            str(dut.iocell_side_io1_cell_out))

    dut._log.info("twi_sda_in %s" % dut.peripheral_side_twi_sda_in)

    # Test for in
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
            "iocell_io1=1/mux=0/out=0 %s twi_sda != 1" %
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

    dut._log.info("Ok!, twi_sda passed")


@cocotb.test()
def pinmux_twi_sda2(dut):
    """Test for I2C multi-input (route 2 inputs to same function)
    """
    yield Timer(2)
    # mux selection lines, each input two bit wide
    dut.mux_lines_cell1_mux_in = 2
    yield Timer(2)
    # enable input for mux
    dut.EN_mux_lines_cell0_mux = 0
    dut.EN_mux_lines_cell1_mux = 1
    dut.EN_mux_lines_cell2_mux = 0

    # TWI
    yield Timer(2)
    # Test for in
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
            "iocell_io1=1/mux=0/out=0 %s twi_sda != 1" %
            str(dut.peripheral_side_twi_sda_in))

    dut.iocell_side_io1_cell_in_in = 0
    yield Timer(2)
    dut._log.info("twi_sda_in %s" % dut.peripheral_side_twi_sda_in)

    if dut.peripheral_side_twi_sda_in != 0:
        raise TestFailure(
            "iocell_io1=1/mux=0/out=0 %s twi_sda != 0" %
            str(dut.peripheral_side_twi_sda_in))

    # ok now set up gpioa0, set it to the opposite of twi_sda (0) i.e. gpioa0=1
    # and test that... then switch over pin0/mux=3
    dut.peripheral_side_gpioa_a0_outen_in = 1
    dut.mux_lines_cell0_mux_in = 0
    dut.EN_mux_lines_cell0_mux = 1
    dut.iocell_side_io0_cell_in_in = 1  # twi_sda=0, so gpioa0 should be 1
    yield Timer(2)

    if dut.peripheral_side_gpioa_a0_in != 1:  # output of iopad
        raise TestFailure(
            "iocell_io0=1/mux=0/out=0 %s gpio_a0 != 1" %
            str(dut.peripheral_side_gpioa_a0_in))

    # also twi_sda should also = 0, because.. because...
    # pin1 is still routed to it, and pin1 is still set to 0...
    if dut.peripheral_side_twi_sda_in != 0:
        raise TestFailure(
            "iocell_io0=1/mux=0/out=0 %s twi_sda != 0" %
            str(dut.peripheral_side_twi_sda_in))

    # ok flip over to test 3
    dut.mux_lines_cell0_mux_in = 3
    yield Timer(2)

    # ok now this should drop to 0 because the muxer's no longer
    # routing iopad0 to gpioa0...
    if dut.peripheral_side_gpioa_a0_in != 0:  # output of iopad
        raise TestFailure(
            "iocell_io0=1/mux=0/out=0 %s gpio_a0 != 0" %
            str(dut.peripheral_side_gpioa_a0_in))

    # AND, at the same time, twi_sda should also = 1, because.. because...
    # pin1 is no longer routed to it, because of the priority muxer
    # now points pin *0* at twi_sda: that's the point of a priority
    # muxer, pin0 and pin1 are both pointint to twi_sda but pin0
    # gets precedence.
    if dut.peripheral_side_twi_sda_in != 1:
        raise TestFailure(
            "iocell_io0=1/mux=0/out=0 %s twi_sda != 1" %
            str(dut.peripheral_side_twi_sda_in))

    # ok so now set cell1 muxer to point to gpioa1...
    dut.mux_lines_cell1_mux_in = 0
    yield Timer(2)

    # now we test twi sda again (it shouldn't change)
    if dut.peripheral_side_twi_sda_in != 1:
        raise TestFailure(
            "iocell_io0=1/mux=0/out=0 %s twi_sda != 1" %
            str(dut.peripheral_side_twi_sda_in))

    dut.iocell_side_io1_cell_in_in = 1  # now try setting cell1 to 0
    yield Timer(2)

    # now we test twi sda again after changing io0, it *still* shouldn't change
    if dut.peripheral_side_twi_sda_in != 1:
        raise TestFailure(
            "iocell_io0=1/mux=0/out=0 %s twi_sda != 1" %
            str(dut.peripheral_side_twi_sda_in))

    # ok that's probably enough, we could check here that actually gpioa1
    # was what got set, or we could flip cell1 mux back to 2
    # and set cell0 mux back to 0 but things are probably tested
    # enough by now

    dut._log.info("Ok!, twi_sda test2 passed")
