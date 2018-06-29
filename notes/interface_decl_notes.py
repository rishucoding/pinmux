class MuxInterface(Interface):

    def wirefmt(self, *args):
        return muxwire.format(*args)

class IOInterface(Interface):

    def ifacefmtoutenfn(self, name):
        return "cell{0}_mux_outen"

    def ifacefmtoutfn(self, name):
        """ for now strip off io{0}_ part """
        return "cell{0}_mux_out"

    def ifacefmtinfn(self, name):
        return "cell{0}_mux_in"

    def wirefmt(self, *args):
        return generic_io.format(*args)

 mux_interface = MuxInterface('cell', [{'name': 'mux', 'ready': False,
                                       'enabled': False,
                                       'bitspec': '{1}', 'action': True}])


 io_interface = IOInterface(
    'io',
    [{'name': 'cell_out', 'enabled': False, },
     {'name': 'cell_outen', 'enabled': False, 'outenmode': True, },
     {'name': 'inputval', 'action': True, 'io': True}, ])

 muxwire = '''
      Wire#({1}) wrcell{0}_mux<-mkDWire(0);'''

generic_io = '''
      Wire#(Bit#(1)) cell{0}_mux_out<-mkDWire(0);
      Wire#(Bit#(1)) cell{0}_mux_outen<-mkDWire(0);
      Wire#(Bit#(1)) cell{0}_mux_in<-mkDWire(0);
'''
    """
    twiinterface_decl = Interface('twi',
                                  [{'name': 'sda', 'outen': True},
                                   {'name': 'scl', 'outen': True},
                                   ])
    """

    """
        uartinterface_decl = Interface('uart',
                                   [{'name': 'rx'},
                                    {'name': 'tx', 'action': True},
                                    ])
    """