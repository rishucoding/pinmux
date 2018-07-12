#!/usr/bin/env python

from spec.base import PinSpec

from spec.ifaceprint import display, display_fns, check_functions
from spec.ifaceprint import display_fixed


def pinspec():
    pinbanks = {
        'B': 28,
    }
    fixedpins = {
        'CTRL_SYS': [
            'TEST',
            'JTAG_SEL',
            'UBOOT_SEL',
            'NMI#',
            'RESET#',
            'CLK24M_IN',
            'CLK24M_OUT',
            'PLLTEST',
            'PLLREGIO',
            'PLLVP25',
            'PLLDV',
            'PLLVREG',
            'PLLGND',
        ],
        'POWER_GPIO': [
            'VDD_GPIOB',
            'GND_GPIOB',
        ]}
    function_names = {'EINT': 'External Interrupt',
                      'FB': 'MC68k FlexBus',
                      'IIS': 'I2S Audio',
                      'JTAG0': 'JTAG (same as JTAG1, JTAG_SEL=LOW)',
                      'JTAG1': 'JTAG (same as JTAG0, JTAG_SEL=HIGH)',
                      'LCD': '24-pin RGB/TTL LCD',
                      'RG': 'RGMII Ethernet',
                      'MMC': 'eMMC 1/2/4/8 pin',
                      'PWM': 'PWM (pulse-width modulation)',
                      'SD0': 'SD/MMC 0',
                      'SD1': 'SD/MMC 1',
                      'SD2': 'SD/MMC 2',
                      'SPI0': 'SPI (Serial Peripheral Interface) 0',
                      'SPI1': 'SPI (Serial Peripheral Interface) 1',
                      'QSPI': 'Quad SPI (Serial Peripheral Interface) 1',
                      'TWI0': 'I2C 0',
                      'TWI1': 'I2C 1',
                      'TWI2': 'I2C 2',
                      'UARTQ0': 'UART (TX/RX/CTS/RTS) 0',
                      'UARTQ1': 'UART (TX/RX/CTS/RTS) 1',
                      'UART0': 'UART (TX/RX) 0',
                      'UART1': 'UART (TX/RX) 1',
                      'UART2': 'UART (TX/RX) 2',
                      'ULPI0': 'ULPI (USB Low Pin-count) 0',
                      'ULPI1': 'ULPI (USB Low Pin-count) 1',
                      'ULPI2': 'ULPI (USB Low Pin-count) 2',
                      }

    ps = PinSpec(pinbanks, fixedpins, function_names)

    # Bank B, 16-47
    ps.gpio("", ('B', 0), 0, 0, 28)
    ps.rgbttl("", ('B', 0), 1, limit=23)
    ps.spi("0", ('B', 10), 2)
    ps.quadspi("", ('B', 4), 2)
    ps.uart("0", ('B', 16), 2)
    ps.i2c("1", ('B', 18), 2)
    ps.pwm("", ('B', 21), 2, 0, 3)
    ps.sdmmc("0", ('B', 22), 3)
    ps.eint("", ('B', 0), 3, 0, 4)
    ps.eint("", ('B', 20), 2, 4, 1)
    ps.eint("", ('B', 23), 1, 5, 1)
    ps.sdmmc("1", ('B', 4), 3)
    ps.jtag("1", ('B', 10), 3)
    ps.uartfull("0", ('B', 14), 3)
    ps.uartfull("1", ('B', 18), 3)
    ps.jtag("0", ('B', 24), 2)
    ps.spi("1", ('B', 24), 1)
    ps.i2c("0", ('B', 0), 2)
    ps.uart("1", ('B', 2), 2)
    ps.uart("2", ('B', 14), 2)

    # Scenarios below can be spec'd out as either "find first interface"
    # by name/number e.g. SPI1, or as "find in bank/mux" which must be
    # spec'd as "BM:Name" where B is bank (A-F), M is Mux (0-3)
    # EINT and PWM are grouped together, specially, but may still be spec'd
    # using "BM:Name".  Pins are removed in-order as listed from
    # lists (interfaces, EINTs, PWMs) from available pins.

    minitest = ['ULPI0/8', 'ULPI1', 'MMC', 'SD0', 'UART0',
                'TWI0', 'SPI0', 'B3:SD1', ]
    minitest_eint = ['EINT_0', 'EINT_1', 'EINT_2', 'EINT_3', 'EINT_4']
    minitest_pwm = ['B2:PWM_0']
    descriptions = {
        'MMC': 'internal (on Card)',
        'SD0': 'user-facing: internal (on Card), multiplexed with JTAG1\n'
        'and UART2, for debug purposes',
        'TWI2': 'I2C.\n',
        'E2:SD1': '',
        'SPI1': '',
        'UART0': '',
        'B1:LCD/22': '18-bit RGB/TTL LCD',
        'ULPI0/8': 'user-facing: internal (on Card), USB-OTG ULPI PHY',
        'ULPI1': 'dual USB2 Host ULPI PHY'
    }

    ps.add_scenario("MiniTest", minitest, minitest_eint, minitest_pwm,
                    descriptions)

    return ps
