from UserDict import UserDict

from wire_def import generic_io # special case

class Pin(object):
    """ pin interface declaration.
        * name is the name of the pin
        * ready, enabled and io all create a (* .... *) prefix
        * action changes it to an "in" if true
    """

    def __init__(self, name,
                 ready=True,
                 enabled=True,
                 io=False,
                 action=False,
                 bitspec=None):
        self.name = name
        self.ready = ready
        self.enabled = enabled
        self.io = io
        self.action = action
        self.bitspec = bitspec if bitspec else '1'

    def ifacefmt(self, fmtfn=None):
        res = '    '
        status = []
        if self.ready:
            status.append('always_ready')
        if self.enabled:
            status.append('always_enabled')
        if self.io:
            status.append('result="io"')
        if status:
            res += '(*'
            res += ','.join(status)
            res += '*)'
        res += " method "
        if self.io:
            res += "\n                      "
        name = fmtfn(self.name)
        if self.action:
            res += " Action "
            res += name
            res += ' (Bit#(%s) in)' % self.bitspec
        else:
            res += " Bit#(%s) " % self.bitspec
            res += name
        res += ";"
        return res

    def ifacedef(self, fmtoutfn=None, fmtinfn=None, fmtdecfn=None):
        res = '      method '
        if self.action:
            fmtname = fmtinfn(self.name)
            res += "Action  "
            res += fmtdecfn(self.name)
            res += '(Bit#(%s) in);\n' % self.bitspec
            res += '         %s<=in;\n' % fmtname
            res += '      endmethod'
        else:
            fmtname = fmtoutfn(self.name)
            res += "%s=%s;" % (self.name, fmtname)
        return res

    def wirefmt(self, fmtoutfn=None, fmtinfn=None, fmtdecfn=None):
        res = '      Wire#(Bit#(%s)) ' % self.bitspec
        if self.action:
            res += '%s' % fmtinfn(self.name)
        else:
            res += '%s' % fmtoutfn(self.name)
        res += "<-mkDWire(0);"
        return res


class Interface(object):
    """ create an interface from a list of pinspecs.
        each pinspec is a dictionary, see Pin class arguments
    """

    def __init__(self, ifacename, pinspecs):
        self.ifacename = ifacename
        self.pins = []
        self.pinspecs = pinspecs
        for p in pinspecs:
            _p = {}
            _p.update(p)
            if p.get('outen') is True:  # special case, generate 3 pins
                del _p['outen']
                for psuffix in ['out', 'outen', 'in']:
                    _p['name'] = "%s_%s" % (self.pname(p['name']), psuffix)
                    _p['action'] = psuffix != 'in'
                    self.pins.append(Pin(**_p))
            else:
                _p['name'] = self.pname(p['name'])
                self.pins.append(Pin(**_p))

    def pname(self, name):
        return '%s{0}_%s' % (self.ifacename, name)

    def wirefmt(self, *args):
        res = '\n'.join(map(self.wirefmtpin, self.pins)).format(*args)
        res += '\n'
        for p in self.pinspecs:
            name = self.pname(p['name']).format(*args)
            res += "      GenericIOType %s_io = GenericIOType{\n" % name
            params = []
            if p.get('outen') is True:
                outname = self.ifacefmtoutfn(name)
                params.append('outputval:%s_out,' % outname)
                params.append('output_en:%s_outen,' % outname)
                params.append('input_en:~%s_outen,' % outname)
            elif p.get('action'):
                outname = self.ifacefmtoutfn(name)
                params.append('outputval:%s,' % outname)
                params.append('output_en:1,')
                params.append('input_en:0,')
            else:
                params.append('outputval:0,')
                params.append('output_en:0,')
                params.append('input_en:1,')
            params += ['pullup_en:0,', 'pulldown_en:0,',
                       'pushpull_en:0,', 'drivestrength:0,',
                       'opendrain_en:0']
            for param in params:
                res += '                 %s\n' % param
            res += '      };\n'
        return '\n' + res

    def ifacefmt(self, *args):
        res = '\n'.join(map(self.ifacefmtdecpin, self.pins)).format(*args)
        return '\n' + res

    def ifacefmtdecfn(self, name):
        return name

    def ifacefmtdecfn2(self, name):
        return name

    def ifacefmtoutfn(self, name):
        return "wr%s" % name

    def ifacefmtinfn(self, name):
        return "wr%s" % name

    def wirefmtpin(self, pin):
        return pin.wirefmt(self.ifacefmtoutfn, self.ifacefmtinfn,
                           self.ifacefmtdecfn2)

    def ifacefmtdecpin(self, pin):
        return pin.ifacefmt(self.ifacefmtdecfn)

    def ifacefmtpin(self, pin):
        return pin.ifacedef(self.ifacefmtoutfn, self.ifacefmtinfn,
                            self.ifacefmtdecfn2)

    def ifacedef(self, *args):
        res = '\n'.join(map(self.ifacefmtpin, self.pins))
        res = res.format(*args)
        return '\n' + res + '\n'


class IOInterface(Interface):

    def ifacefmtoutfn(self, name):
        """ for now strip off io{0}_ part """
        return "cell{0}_mux_out.%s" % name[6:]

    def ifacefmtinfn(self, name):
        return "cell{0}_mux_in"

    def wirefmt(self, *args):
        return generic_io.format(*args)


class Interfaces(UserDict):
    """ contains a list of interface definitions
    """

    def __init__(self):
        self.ifacecount = []
        UserDict.__init__(self, {})
        with open('interfaces.txt', 'r') as ifile:
            for l in ifile.readlines():
                l = l.strip()
                l = l.split("\t")
                name = l[0]
                count = int(l[1])
                spec = self.read_spec(name)
                self.ifaceadd(name, count, Interface(name, spec))

    def ifaceadd(self, name, count, iface, at=None):
        if at is None:
            at = len(self.ifacecount)
        self.ifacecount.insert(at, (name, count))
        self[name] = iface

    def read_spec(self, name):
        spec = []
        with open('%s.txt' % name, 'r') as sfile:
            for l in sfile.readlines():
                l = l.strip()
                l = l.split("\t")
                d = {'name': l[0]}
                if l[1] == 'out':
                    d['action'] = True
                elif l[1] == 'inout':
                    d['outen'] = True
                spec.append(d)
        return spec

    def ifacedef(self, f, *args):
        for (name, count) in self.ifacecount:
            for i in range(count):
                f.write(self.data[name].ifacedef(i))

    def ifacefmt(self, f, *args):
        comment = '''
          // interface declaration between %s-{0} and pinmux'''
        for (name, count) in self.ifacecount:
            for i in range(count):
                c = comment % name.upper()
                f.write(c.format(i))
                f.write(self.data[name].ifacefmt(i))

    def wirefmt(self, f, *args):
        comment = '\n      // following wires capture signals ' \
                  'to IO CELL if %s-{0} is\n' \
                  '      // allotted to it'
        for (name, count) in self.ifacecount:
            for i in range(count):
                c = comment % name
                f.write(c.format(i))
                f.write(self.data[name].wirefmt(i))


# ========= Interface declarations ================ #

mux_interface = Interface('cell', [{'name': 'mux', 'ready': False,
                                    'enabled': False,
                                    'bitspec': '{1}', 'action': True}])

io_interface = IOInterface('io',
                           [{'name': 'outputval', 'enabled': False},
                            {'name': 'output_en', 'enabled': False},
                               {'name': 'input_en', 'enabled': False},
                               {'name': 'pullup_en', 'enabled': False},
                               {'name': 'pulldown_en', 'enabled': False},
                               {'name': 'drivestrength', 'enabled': False},
                               {'name': 'pushpull_en', 'enabled': False},
                               {'name': 'opendrain_en', 'enabled': False},
                               {'name': 'inputval', 'action': True, 'io': True},
                            ])

# == Peripheral Interface definitions == #
# these are the interface of the peripherals to the pin mux
# Outputs from the peripherals will be inputs to the pinmux
# module. Hence the change in direction for most pins

# ======================================= #

# basic test
if __name__ == '__main__':

    uartinterface_decl = Interface('uart',
                                   [{'name': 'rx'},
                                    {'name': 'tx', 'action': True},
                                    ])

    twiinterface_decl = Interface('twi',
                                  [{'name': 'sda', 'outen': True},
                                   {'name': 'scl', 'outen': True},
                                   ])

    def _pinmunge(p, sep, repl, dedupe=True):
        """ munges the text so it's easier to compare.
            splits by separator, strips out blanks, re-joins.
        """
        p = p.strip()
        p = p.split(sep)
        if dedupe:
            p = filter(lambda x: x, p)  # filter out blanks
        return repl.join(p)

    def pinmunge(p):
        """ munges the text so it's easier to compare.
        """
        # first join lines by semicolons, strip out returns
        p = p.split(";")
        p = map(lambda x: x.replace('\n', ''), p)
        p = '\n'.join(p)
        # now split first by brackets, then spaces (deduping on spaces)
        p = _pinmunge(p, "(", " ( ", False)
        p = _pinmunge(p, ")", " ) ", False)
        p = _pinmunge(p, " ", " ")
        return p

    def zipcmp(l1, l2):
        l1 = l1.split("\n")
        l2 = l2.split("\n")
        for p1, p2 in zip(l1, l2):
            print repr(p1)
            print repr(p2)
            print
            assert p1 == p2

    ifaces = Interfaces()

    ifaceuart = ifaces['uart']
    print ifaceuart.ifacedef(0)
    print uartinterface_decl.ifacedef(0)
    assert ifaceuart.ifacedef(0) == uartinterface_decl.ifacedef(0)

    ifacetwi = ifaces['twi']
    print ifacetwi.ifacedef(0)
    print twiinterface_decl.ifacedef(0)
    assert ifacetwi.ifacedef(0) == twiinterface_decl.ifacedef(0)
