#!/usr/bin/env python

from spec.base import PinSpec

from spec.ifaceprint import display, display_fns, check_functions
from spec.ifaceprint import display_fixed


def pinspec():
    pinbanks = {
        'A': 4,
    }
    fixedpins = {
        'CTRL_SYS': [
            'NMI#',
            'RESET#',
        ],
        'POWER_GPIO': [
            'VDD_GPIOA',
            'GND_GPIOA',
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

    # Bank A, 0-3
    ps.gpio("", ('A', 0), 0, 0, 3)
    ps.uart("", ('A', 0), 1)
    #ps.uart("0", ('A', 0), 1)
    #ps.uart("1", ('A', 2), 1)
    ps.i2c("", ('A', 1), 2)
    ps.i2c("", ('A', 0), 3, limit=1)
    #ps.i2c("0", ('A', 1), 2)
    #ps.i2c("1", ('A', 2), 4)

    microtest = ['UART', 'TWI', ]
    microtest_eint = []
    microtest_pwm = []
    descriptions = {
        'TWI0': 'I2C',
        'E2:SD1': '',
        'SPI1': '',
        'UART0': '',
        'B1:LCD/22': '18-bit RGB/TTL LCD',
        'ULPI0/8': 'user-facing: internal (on Card), USB-OTG ULPI PHY',
        'ULPI1': 'dual USB2 Host ULPI PHY'
    }

    ps.add_scenario("MicroTest", microtest, microtest_eint, microtest_pwm,
                    descriptions)

    return ps
