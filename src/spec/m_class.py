#!/usr/bin/env python

from spec.base import PinSpec


def pinspec():
    pinbanks = {'A': 16,
                'B': 28,
                'C': 24,
                'D': 24,
                'E': 24,
                'F': 10,
                'G': 32,
                }
    fixedpins = {
        'DDR3': [
            'SDQ0', 'SDQ1', 'SDQ2', 'SDQ3',
            'SDQ4', 'SDQ5', 'SDQ6', 'SDQ7',
            'SDQ8', 'SDQ9', 'SDQ10', 'SDQ11',
            'SDQ12', 'SDQ13', 'SDQ14', 'SDQ15',
            'SDQ16', 'SDQ17', 'SDQ18', 'SDQ19',
            'SDQ20', 'SDQ21', 'SDQ22', 'SDQ23',
            'SDQ24', 'SDQ25', 'SDQ26', 'SDQ27',
            'SDQ28', 'SDQ29', 'SDQ30', 'SDQ31',
            'SVREF0', 'SVREF1', 'SVREF2', 'SVREF3',
            'SDQS0', 'SDQS0#', 'SDQS1', 'SDQS1#',
            'SDQS2', 'SDQS2#', 'SDQS3', 'SDQS3#',
            'SDQM0', 'SDQM1', 'SDQM2', 'SDQM3',
            'SCK#', 'SCK', 'SCKE0', 'SCKE1',
            'SA0', 'SA1', 'SA2', 'SA3',
            'SA4', 'SA5', 'SA6', 'SA7',
            'SA8', 'SA9', 'SA10', 'SA11',
            'SA12', 'SA13', 'SA14',
            'SBA0', 'SBA1', 'SBA2',
            'SWE', 'SCAS', 'SRAS', 'SCS0',
            'SCS1', 'SZQ', 'SRST',
            'SDBG0', 'SDBG1', 'ADBG',
            'ODT0', 'ODT1'],
        'CTRL_SYS': [
            'TEST', 'JTAG_SEL', 'UBOOT_SEL',
            'NMI#', 'RESET#', 'CLK24M_IN', 'CLK24M_OUT',
            'PLLTEST', 'PLLREGIO', 'PLLVP25',
            'PLLDV', 'PLLVREG', 'PLLGND',
        ],
        'POWER_DRAM': [
            'VCC0_DRAM', 'VCC1_DRAM', 'VCC2_DRAM', 'VCC3_DRAM',
            'VCC4_DRAM', 'VCC5_DRAM', 'VCC6_DRAM', 'VCC7_DRAM',
            'VCC8_DRAM', 'VCC9_DRAM',
            'GND0_DRAM', 'GND1_DRAM', 'GND2_DRAM', 'GND3_DRAM',
            'GND4_DRAM', 'GND5_DRAM', 'GND6_DRAM', 'GND7_DRAM',
            'GND8_DRAM', 'GND9_DRAM',
        ],
        'POWER_CPU': [
            'VDD0_CPU', 'VDD1_CPU', 'VDD2_CPU',
            'VDD3_CPU', 'VDD4_CPU', 'VDD5_CPU',
            'GND0_CPU', 'GND1_CPU', 'GND2_CPU',
            'GND3_CPU', 'GND4_CPU', 'GND5_CPU',
        ],
        'POWER_DLL': [
            'VDD0_DLL', 'VDD1_DLL', 'VDD2_DLL',
            'GND0_DLL', 'GND1_DLL', 'GND2_DLL',
        ],
        'POWER_INT': [
            'VDD0_INT', 'VDD1_INT', 'VDD2_INT', 'VDD3_INT', 'VDD4_INT',
            'VDD5_INT', 'VDD6_INT', 'VDD7_INT', 'VDD8_INT', 'VDD9_INT',
            'GND0_INT', 'GND1_INT', 'GND2_INT', 'GND3_INT', 'GND4_INT',
            'GND5_INT', 'GND6_INT', 'GND7_INT', 'GND8_INT', 'GND9_INT',
        ],
        'POWER_GPIO': [
            'VDD_GPIOA', 'VDD_GPIOB', 'VDD_GPIOC',
            'VDD_GPIOD', 'VDD_GPIOE', 'VDD_GPIOF',
            'VDD_GPIOG',
            'GND_GPIOA', 'GND_GPIOB', 'GND_GPIOC',
            'GND_GPIOD', 'GND_GPIOE', 'GND_GPIOF',
            'GND_GPIOG',
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
                      'TWI0': 'I2C 1',
                      'TWI1': 'I2C 2',
                      'TWI2': 'I2C 3',
                      'UARTQ0': 'UART (TX/RX/CTS/RTS) 0',
                      'UARTQ1': 'UART (TX/RX/CTS/RTS) 1',
                      'UART0': 'UART (TX/RX) 0',
                      'UART1': 'UART (TX/RX) 1',
                      'UART2': 'UART (TX/RX) 2',
                      'ULPI0': 'ULPI (USB Low Pin-count) 1',
                      'ULPI1': 'ULPI (USB Low Pin-count) 2',
                      'ULPI2': 'ULPI (USB Low Pin-count) 3',
                      }

    ps = PinSpec(pinbanks, fixedpins, function_names)

    # Bank A, 0-15
    ps.gpio("", ('A', 0), 0, 0, 16)
    ps.spi("0", ('A', 0), 3)
    ps.uartfull("1", ('A', 0), 2)
    ps.i2c("0", ('A', 4), 2)
    ps.emmc("", ('A', 0), 1)
    #ps.uart("0", ('A', 14), 1)
    ps.spi("1", ('A', 6), 2)
    ps.eint("", ('A', 10), 1, start=0, limit=6)
    ps.eint("", ('A', 4), 3, start=0, limit=6)
    ps.sdmmc("0", ('A', 10), 2)
    ps.jtag("0", ('A', 10), 3)
    ps.uart("0", ('A', 14), 3)

    # Bank B, 16-47
    ps.gpio("", ('B', 0), 0, 0, 28)
    ps.rgbttl("0", ('B', 0), 1)
    ps.spi("0", ('B', 12), 2)
    ps.quadspi("", ('B', 4), 2, limit=4)
    ps.uart("1", ('B', 16), 2)
    ps.i2c("2", ('B', 18), 2)
    ps.pwm("", ('B', 9), 2, start=0, limit=1)
    ps.pwm("", ('B', 20), 2, start=1, limit=2)
    ps.sdmmc("0", ('B', 22), 2)
    ps.eint("", ('B', 0), 3, start=6, limit=4)
    ps.flexbus2("", ('B', 4), 3)
    ps.i2c("0", ('B', 0), 2)
    ps.uart("0", ('B', 2), 2)
    ps.uart("2", ('B', 10), 2)

    # Bank C, 48-71
    ps.gpio("", ("C", 0), 0, 0, 24)
    ps.ulpi("0", ('C', 0), 1)
    ps.ulpi("1", ('C', 12), 1)
    ps.spi("1", ('C', 8), 2)
    #ps.spi("1", ('C', 28), 2)
    ps.uartfull("0", ('C', 20), 3)
    ps.eint("", ('C', 0), 3, start=10, limit=8)
    ps.jtag("1", ('C', 8), 3)
    ps.eint("", ('C', 12), 3, start=22, limit=8)
    ps.uart("0", ('C', 22), 2)
    ps.i2s("", ('C', 13), 2)
    ps.pwm("", ('C', 21), 2, start=2, limit=1)

    # Bank D, 72-96

    # see comment in spec.interfaces.PinGen, this is complicated.
    flexspec = {
        'FB_TS': ('FB_ALE', 2),
        'FB_CS2': ('FB_BWE2', 2),
        'FB_A0': ('FB_BWE2', 3),
        'FB_CS3': ('FB_BWE3', 2),
        'FB_A1': ('FB_BWE3', 3),
        'FB_TBST': ('FB_OE', 2),
        'FB_TSIZ0': ('FB_BWE0', 2),
        'FB_TSIZ1': ('FB_BWE1', 2),
    }
    #ps.mcu8080("", 72, 1)
    ps.gpio("", ('D', 0), 0, 0, 24)
    ps.flexbus1("", ('D', 0), 1, spec=flexspec)
    ps.i2c("1", ('D', 8), 3)
    ps.pwm("", ('D', 21), 1, start=0, limit=3)
    ps.i2c("0", ('D', 10), 3)
    ps.i2c("2", ('D', 19), 2)
    ps.uartfull("0", ('D', 0), 2)
    ps.uart("1", ('D', 21), 2)
    ps.uart("2", ('D', 13), 2)
    ps.eint("", ('D', 19), 3, start=18, limit=4)
    ps.eint("", ('D', 23), 3, start=9, limit=1)
    ps.eint("", ('D', 13), 3, start=5, limit=4)
    ps.eint("", ('D', 0), 3, start=30, limit=2)
    ps.i2c("1", ('D', 2), 3)
    ps.sdmmc("1", ('D', 4), 2)

    # Bank E
    ps.gpio("", ('E', 0), 0, 0, 24)
    ps.flexbus2("", ('E', 0), 1)
    ps.sdmmc("1", ('E', 0), 2)
    ps.sdmmc("2", ('E', 8), 2)
    ps.quadspi("", ('E', 18), 2)
    ps.uartfull("1", ('E', 14), 2)
    ps.i2c("1", ('E', 6), 2)
    ps.eint("", ('E', 0), 3, start=10, limit=8)
    ps.eint("", ('E', 8), 3, start=22, limit=6)
    ps.emmc("", ('E', 14), 3)

    # Bank F
    ps.gpio("", ('F', 0), 0, 0, 10)
    ps.i2s("", ('F', 0), 1)
    ps.i2c("0", ('F', 6), 2)
    ps.pwm("", ('F', 8), 2, start=0, limit=1)
    ps.pwm("", ('F', 9), 2, start=1, limit=1)
    ps.uart("2", ('F', 8), 1)
    ps.sdmmc("2", ('F', 0), 2)
    ps.eint("", ('F', 0), 3, start=18, limit=4)
    ps.pwm("", ('F', 4), 3, start=2, limit=1)
    ps.eint("", ('F', 5), 3, start=7, limit=1)
    ps.eint("", ('F', 6), 3, start=28, limit=4)

    # Bank G
    ps.gpio("", ('G', 0), 0, 0, 32)
    ps.rgmii("", ('G', 0), 1)
    ps.ulpi("2", ('G', 20), 1)
    ps.rgbttl("1", ('G', 0), 2)
    ps.quadspi("", ('G', 26), 3)
    ps.flexbus2("", ('G', 0), 3)
    ps.sdmmc("1", ('G', 24), 3, limit=2)
    ps.sdmmc("1", ('G', 28), 2, start=2)

    # EOMA68 scenario.  not totally complete (some GPIO needed for PMIC)
    # One interface to be connected to the MCU to give RTC and boot/dbg
    # VBUS_EN, OTG_ID etc. are all not included below, there is plenty
    # of spare GPIO.

    eoma68 = ['B1:LCD/22', 'ULPI0/8', 'ULPI1', 'MMC', 'SD0', 'UART1',
              'TWI2', 'SPI1', 'E2:SD1', ]
    eoma68_eint = ['EINT_16', 'EINT_17', 'EINT_18', 'EINT_19']
    eoma68_pwm = ['D1:PWM_2']
    descriptions = {
        'MMC': 'internal (on Card)',
        'SD0': 'user-facing: internal (on Card), multiplexed with JTAG0\n'
        'and UART0, for debug purposes',
        'TWI2': 'EOMA68-compliance: must be entirely free of devices.\n'
        'Address 0x51 used (externally) for EOMA68 EEPROM Id',
        'E2:SD1': 'EOMA68-compliance',
        'SPI1': 'EOMA68-compliance',
        'UART1': 'EOMA68-compliance',
        'B1:LCD/22': 'EOMA68-compliance, 18-bit RGB/TTL LCD',
        'ULPI0/8': 'user-facing: internal (on Card), USB-OTG ULPI PHY',
        'ULPI1': 'EOMA68-compliance: dual USB2 Host ULPI PHY'
    }

    ps.add_scenario("EOMA68", eoma68, eoma68_eint, eoma68_pwm, descriptions)

    # Industrial scenario.  not totally complete (some GPIO needed for PMIC)
    # One interface to be connected to the MCU to give RTC, boot/dbg,
    # option of CAN Bus, ADC, DAC, OWB, more GPIO, more PWM etc. etc.
    # Focus is on getting as many UARTs, SPIs and TWIs as possible.
    # OTG_ID (if to be used) would require dropping some functions in order
    # to free up GPIO.  LCD could be reduced to 15-bit (freeing 3).
    # MMC could be reduced to 4-bit-wide, used as SD/MMC (freeing 4).
    # QSPI could be used in 1-bit (MOSI/MISO) mode (freeing up 2 more).

    industrial = ['D1:FB/17', 'E1:FB/8', 'B1:LCD/22', 'ULPI0/8', 'ULPI1/8',
                  'MMC', 'B2:SD0',
                  'JTAG0', 'A3:UART0', 'E2:UARTQ1', 'C3:UARTQ0',
                  'F2:TWI0', 'D2:TWI1', 'D2:TWI2', 'SPI1', 'QSPI', 'F2:SD2']
    industrial_pwm = ['F2:PWM_0', 'F2:PWM_1', 'D1:PWM_2']
    industrial_eint = ['EINT_24', 'EINT_25', 'EINT_26', 'EINT_27',
                       'EINT_20', 'EINT_21', 'EINT_22', 'EINT_23']

    ps.add_scenario("Industrial", industrial, industrial_eint,
                    industrial_pwm, None)

    # Industrial scenario, using an SPI-based LCD instead of RGB/TTL
    # not totally complete (some GPIO needed for PMIC)
    # One interface to be connected to the MCU to give RTC, boot/dbg,
    # option of CAN Bus, ADC, DAC, OWB, more GPIO, more PWM etc. etc.
    # Focus is on getting as many UARTs, SPIs and TWIs as possible,
    # leaving some GPIO spare from the RGB/TTL bank (SPI CS#)
    # also possibility of freeing up FlexBus CS# with a little reorg.

    industrial = ['D1:FB/17', 'E1:FB/8', 'B2:SPI0', 'ULPI0/8', 'ULPI1/8',
                  'MMC', 'B2:SD0',
                  'JTAG0',
                  'A3:UART0', 'E2:UARTQ1', 'C3:UARTQ0', 'B2:UART2', 'B2:UART1',
                  'F2:TWI0', 'D2:TWI1', 'D2:TWI2', 'SPI1', 'QSPI', 'F2:SD2']
    industrial_pwm = ['F2:PWM_0', 'F2:PWM_1', 'D1:PWM_2']
    industrial_eint = ['EINT_24', 'EINT_25', 'EINT_26', 'EINT_27',
                       'EINT_20', 'EINT_21', 'EINT_22', 'EINT_23']
    ind_descriptions = {
        'B2:SPI0': 'Used for 320x240 or 640x480 etc. SPI-based LCD.\n'
        'Frees up large numbers of GPIO from RGB/TTL bank'
    }

    ps.add_scenario("Industrial with SPI-LCD",
                    industrial, industrial_eint, industrial_pwm,
                    ind_descriptions)

    # Smartphone / Tablet - basically the same thing

    tablet = ['B1:LCD/22', 'ULPI0/8', 'ULPI1/8',
              'MMC', 'SD0',
              'F1:IIS',  # I2C Audio
              'TWI1',   # I2C Audio
              'E2:UARTQ1',  # WIFI/BT
              'E2:SD1',   # WIFI
              'C3:UARTQ0',  # GPS
              'D2:UART1',
              'D2:UART2',
              'D3:TWI0', 'D2:TWI2', 'SPI1', 'QSPI']
    tablet_pwm = ['F2:PWM_0',  # LCD_BACKLIGHT
                  'F2:PWM_1', 'D1:PWM_2']
    tablet_eint = ['EINT_24',  # BT_HOST_WAKE
                   'EINT_25',  # WIFI_HOST_WAKE
                   'EINT_26',  # CTP_INT
                   'EINT_27',  # GSENSOR_INT
                   'EINT_8',  # GPS_INT
                   'EINT_7',  # TILT_SENSOR_INT
                   'EINT_22',  # COMPASS_INT
                   'EINT_23',  # MCU_INT
                   'EINT_16',  # PMIC_INT
                   'EINT_17',  # PWR_BUTTON_INT
                   'EINT_30',  # OTG_ID
                   'EINT_31',
                   ]
    descriptions = {
        'B1:LCD/22':
        'RGB/TTL LCD, 800x480 or use SN75LVDS83b for up to 1440x900',
        'MMC': 'eMMC: main internal storage',
        'ULPI0/8': 'USB-OTG, connect to ULPI OTG PHY (for charging)\n'
                   'as well as USB Host or USB Device',
        'ULPI1/8': 'USB2 Host, connect to ULPI PHY w/and 4-port USB2 Hub\n'
        'for example GL850G or FE1.1. '
        'Connects to 2/3/4G/LTE Modem, 2x USB-Camera (VC0345)',
        'SD0': 'internal, multiplexed with JTAG0\n'
               'and UART0, for debug purposes',
        'F1:IIS': 'I2C Audio, connect to AC97 Audio IC',
        'TWI1': 'Connect to AC97 Audio IC',
        'E2:UARTQ1': 'Connect to BT on AP6234/AP6335',
        'E2:SD1': 'Connect to WIFI on AP6234/AP6335',
        'QSPI': 'Boot Storage (connection to companion / debug / boot MCU)\n'
                'Only actually needs MISO/MOSI, bootstrap loader v. small\n'
                'Bootstrap loader checks eMMC, USB-OTG, SD/MMC, SPI, etc.',
        'SPI1': 'Spare? SPI, connect to higher-speed sensor?',
        'D2:UART1': 'Spare? UART (or 2 extra GPIO / EINT)',
        'D2:UART2': 'Spare? UART (or 2 extra GPIO)',
        'D3:TWI0': 'Connect to PMIC',
        'D2:TWI2': 'Connect to sensors (Trackpad? CTP GSENSOR TILT COMPASS)',
        'GPIO': '9 spare GPIO pins for miscellaneous functions:\n'
                'wake-up of BT, WIFI, LCD power, sensor power etc.\n'
                '4 GPIO may be needed for PWM Audio from Modem.\n'
                'LED lights for camera will be needed.\n'
                'Some phones may have clam-shell or lid switch.\n'
                'Some Modems have spare GPIO (over AT commandset).\n'
                'AXP209 PMIC has 4x GPIO, accessible over I2C.\n'
                'SPI1, UART1-4, PWM1-2 may also be spare (10 extra GPIO).\n'
                'If more needed, companion MCU may be used (48+ pin variant)\n'
                'which also includes ADC, DAC, more PWM etc.',
        'F2:PWM_0': 'LCD Backlight',
        'F2:PWM_1': 'Spare? PWM (or extra GPIO / EINT)',
        'D1:PWM_2': 'Spare? PWM (or extra GPIO / EINT)',
        'EINT_24': 'BT_HOST_WAKE',
        'EINT_25': 'WIFI_HOST_WAKE',
        'EINT_26': 'CTP_INT',
        'EINT_27': 'GSENSOR_INT',
        'EINT_8': 'GPS_INT',
        'EINT_7': 'TILT_SENSOR_INT',
        'EINT_22': 'COMPASS_INT',
        'EINT_23': 'MCU_INT',
        'EINT_16': 'PMIC_INT',
        'EINT_17': 'PWR_BUTTON_INT',
        'EINT_30': 'OTG_ID',
        'EINT_31': 'Spare?',
    }

    ps.add_scenario("Smartphone / Tablet",
                    tablet, tablet_eint, tablet_pwm,
                    descriptions)

    # Laptop

    laptop = ['D1:FB/17', 'E1:FB/8', 'B1:LCD/22', 'ULPI0/8', 'ULPI1/8',
              'MMC', 'SD0',
              'F1:IIS',  # I2C Audio
              'TWI1',   # I2C Audio
              'E2:UARTQ1',  # WIFI/BT
              'E2:SD2',   # WIFI
              'D2:TWI2', 'QSPI']
    laptop_pwm = ['F2:PWM_0',  # LCD_BACKLIGHT
                  ]
    laptop_eint = ['EINT_20',  # BT_HOST_WAKE
                   'EINT_21',  # WIFI_HOST_WAKE
                   'EINT_9',  # MCU_INT
                   'EINT_31',  # PMIC_INT
                   ]
    descriptions = {
        'D1:FB/17': 'FlexBus.  Connect to DM9000 or AX99896A MCU-style Bus\n'
        '10/100 Ethernet PHY.',
        'E1:FB/8': 'FlexBus bus bits 8-15, needed to make a 16-bit bus width',
        'B1:LCD/22': 'RGB/TTL LCD, use SN75LVDS83b for '
                     'LVDS or SSD2828 for MIPI,\n'
        'or a Chrontel CH7039, CH7038, CH7034 or CH7018 for dual\n'
        'display output (eDP/LVDS and HDMI/VGA) '
        'conversion.',
        'MMC': 'eMMC: main internal storage',
        'ULPI0/8': 'USB-OTG, connect to ULPI OTG PHY (for charging)\n'
        'as well as USB Host or USB Device',
        'ULPI1/8': 'USB2 Host, connect to ULPI PHY w/and 4-port USB2 Hub\n'
        'for example GL850G or FE1.1. '
        'Connects to USB-Camera (VC0345 and 3x external USB Ports)',
        'SD0': 'internal, multiplexed with JTAG0\n'
        'and UART0, for debug purposes',
        'F1:IIS': 'I2C Audio, connect to AC97 Audio IC',
        'TWI1': 'Connect to AC97 Audio IC',
        'E2:UARTQ1': 'Connect to BT on AP6234/AP6335',
        'E2:SD2': 'Connect to WIFI on AP6234/AP6335',
        'QSPI': 'Boot Storage (connection to companion / debug / boot MCU)\n'
        'Only actually needs MISO/MOSI, bootstrap loader v. small\n'
        'Bootstrap loader checks eMMC, USB-OTG, SD/MMC, SPI, etc.\n'
        'MCU implements keyboard-matrix for keyboard (also trackpad?)',
        'D2:TWI2': 'Connect to PMIC',
        'GPIO': 'Plenty of spare GPIO pins for miscellaneous functions\n'
        'MCU EINT-capable GPIO may be used to generate extra EINTs\n'
        'on the single MCU_INT line, if really needed',
        'F2:PWM_0': 'LCD Backlight',
        'EINT_20': 'BT_HOST_WAKE',
        'EINT_21': 'WIFI_HOST_WAKE',
        'EINT_9': 'MCU_INT',
        'EINT_31': 'PMIC_INT',
    }
    ps.add_scenario("Laptop / Netbook",
                    laptop, laptop_eint, laptop_pwm,
                    descriptions)

    # IoT

    iot = ['B1:LCD', 'ULPI1/8', 'ULPI0/8',
           'MMC', 'SD0',
           'F1:IIS',  # I2C Audio
           #'TWI1',   # I2C Audio
           'C3:UARTQ0',  # HSPA UART
           'E2:UARTQ1',  # BT UART
           'C2:SPI1',  # HSPI SPI
           'E2:SD2',   # WIFI
           'D3:TWI0',  # sensors CTP,
           'D2:TWI2', 'QSPI']
    iot_pwm = ['F2:PWM_0',  # LCD_BACKLIGHT
               ]
    iot_eint = ['EINT_5',  # 'HSPA_MST_RDY',
                'EINT_6',  # 'HSPA_SL_RDY',
                'EINT_7',  # 'HSPA_RING',
                'EINT_8',  # 'WL_PMU_EN',
                'EINT_9',  # HSPA_GPIO1
                'EINT_10',  # IR_DT
                'EINT_11',  # 'BT_PCM_CLK',
                'EINT_12',  # 'BT_PCM_DIN',
                'EINT_13',  # 'BT_PCM_SYNC',
                'EINT_14',  # 'BT_PCM_DOUT',
                'EINT_16',  # 'USB_DRVVBUS',
                'EINT_17',  # 'USB_VBUSDET',
                'EINT_21',  # 'USB_ID',
                'EINT_30',  # 'CTP_INT',
                'EINT_31',  # 'SD_DET#',
                ]
    descriptions = {
        'B1:LCD':
        'RGB/TTL LCD, use SN75LVDS83b for LVDS or SSD2828 for MIPI,\n'
        'or a Chrontel CH7039, CH7038, CH7034 or CH7018 for dual\n'
        'display output (eDP/LVDS and HDMI/VGA) '
        'conversion.',
        'MMC': 'eMMC: main internal storage',
        'F1:IIS': 'I2C Audio, connect to AC97 Audio IC',
        'ULPI1/8': 'USB-OTG, connect to ULPI OTG PHY (for charging)\n'
                   'as well as USB Host or USB Device',
        'ULPI0/8': 'USB2 Host, connect to ULPI PHY',
        'SD0': 'internal, multiplexed with JTAG0\n'
               'and UART0, for debug purposes',
        'C3:UARTQ0': 'Connect to HSPA UART',
        'E2:UARTQ1': 'Connect to BT UART',
        'E2:SD2': 'Connect to WIFI',
        'C2:SPI1': 'HSPA SPI',
        'QSPI': 'Boot Storage (connection to companion / debug / boot MCU)\n'
                'Only actually needs MISO/MOSI, bootstrap loader v. small\n'
                'Bootstrap loader checks eMMC, USB-OTG, SD/MMC, SPI, etc.\n'
                'MCU implements keyboard-matrix for keyboard (also trackpad?)',
        'D2:TWI2': 'Connect to PMIC',
        'D3:TWI0': 'Connect to sensors CTP',
        'GPIO': 'Plenty of spare GPIO pins for miscellaneous functions\n'
                'MCU EINT-capable GPIO may be used to generate extra EINTs\n'
                'on the single MCU_INT line, if really needed',
        'F2:PWM_0': 'LCD Backlight',
        'GPIOD_D4': 'WL_WAKE_AP',
        'GPIOD_D5': 'BT_WAKE_AP',
        'GPIOD_D6': 'AP_WAKE_BT',
        'GPIOD_D7': 'AP_CK32KO',
        'GPIOD_D8': 'HSPA_PWRON',
        'GPIOD_D9': 'BT_RST_N',
        'GPIOE_E5': 'HSPA_ON_OFF',
        'GPIOD_D2': 'HSPA_SHUTDOWN',
        'GPIOD_D3': 'CTP_RST',
        'GPIOD_D12': 'LCD_RDN',
        'GPIOD_D17': 'LCD_WRN',
        'GPIOD_D18': 'LCD_RS',
        'GPIOD_D21': 'LCD_CSN',

        'EINT_5': 'HSPA_MST_RDY',
        'EINT_6': 'HSPA_SL_RDY',
        'EINT_7': 'HSPA_RING',
        'EINT_8': 'WL_PMU_EN',
        'EINT_9': 'HSPA_GPIO1',
        'EINT_10': 'IR_DT',
        'EINT_11': 'BT_PCM_CLK',
        'EINT_12': 'BT_PCM_DIN',
        'EINT_13': 'BT_PCM_SYNC',
        'EINT_14': 'BT_PCM_DOUT',

        'EINT_16': 'USB_DRVVBUS',
        'EINT_17': 'USB_VBUSDET',
        'EINT_21': 'USB_ID',
        'EINT_30': 'CTP_INT',
        'EINT_31': 'SD_DETN',
    }
    ps.add_scenario("IoT",
                    iot, iot_eint, iot_pwm,
                    descriptions)

    return ps
