import os.path

try:
    from UserDict import UserDict
except ImportError:
    from collections import UserDict

from bsv.wire_def import generic_io  # special case
from bsv.wire_def import muxwire  # special case


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
                 bitspec=None,
                 outenmode=False):
        self.name = name
        self.ready = ready
        self.enabled = enabled
        self.io = io
        self.action = action
        self.bitspec = bitspec if bitspec else 'Bit#(1)'
        self.outenmode = outenmode

    # bsv will look like this (method declaration):
    """
    (*always_ready,always_enabled*) method Bit#(1) io0_cell_outen;
    (*always_ready,always_enabled,result="io"*) method
                       Action io0_inputval (Bit#(1) in);
    """
    def ifacefmt(self, fmtfn):
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
            res += ' (%s in)' % self.bitspec
        else:
            res += " %s " % self.bitspec
            res += name
        res += ";"
        return res

    # sample bsv method definition :
    """
    method Action  cell0_mux(Bit#(2) in);
        wrcell0_mux<=in;
    endmethod
    """
    def ifacedef(self, fmtoutfn, fmtinfn, fmtdecfn):
        res = '      method '
        if self.action:
            fmtname = fmtinfn(self.name)
            res += "Action  "
            res += fmtdecfn(self.name)
            res += '(%s in);\n' % self.bitspec
            res += '         %s<=in;\n' % fmtname
            res += '      endmethod'
        else:
            fmtname = fmtoutfn(self.name)
            res += "%s=%s;" % (self.name, fmtname)
        return res
    #sample bsv wire (wire definiton):
    """
    Wire#(Bit#(2)) wrcell0_mux<-mkDWire(0);
    """
    def wirefmt(self, fmtoutfn, fmtinfn, fmtdecfn):
        res = '      Wire#(%s) ' % self.bitspec
        if self.action:
            res += '%s' % fmtinfn(self.name)
        else:
            res += '%s' % fmtoutfn(self.name)
        res += "<-mkDWire(0);"
        return res


class Interface(object):
    """ create an interface from a list of pinspecs.
        each pinspec is a dictionary, see Pin class arguments
        single indicates that there is only one of these, and
        so the name must *not* be extended numerically (see pname)
    """
    #sample interface object:
    """
    twiinterface_decl = Interface('twi',
                                  [{'name': 'sda', 'outen': True},
                                   {'name': 'scl', 'outen': True},
                                   ])
    """
    def __init__(self, ifacename, pinspecs, ganged=None, single=False):
        self.ifacename = ifacename
        self.ganged = ganged or {}
        self.pins = [] # a list of instances of class Pin
        self.pinspecs = pinspecs # a list of dictionary
        self.single = single
        for p in pinspecs:
            _p = {}
            _p.update(p)
            if p.get('outen') is True:  # special case, generate 3 pins
                del _p['outen']
                for psuffix in ['out', 'outen', 'in']:
                    # changing the name (like sda) to (twi_sda_out)
                    _p['name'] = "%s_%s" % (self.pname(p['name']), psuffix)
                    _p['action'] = psuffix != 'in'
                    self.pins.append(Pin(**_p))
                    #will look like {'name': 'twi_sda_out', 'action': True}
                    # {'name': 'twi_sda_outen', 'action': True}
                    #{'name': 'twi_sda_in', 'action': False}
                    # NOTice - outen key is removed
            else:
                _p['name'] = self.pname(p['name'])
                self.pins.append(Pin(**_p))

    # sample interface object:
    """
        uartinterface_decl = Interface('uart',
                                   [{'name': 'rx'},
                                    {'name': 'tx', 'action': True},
                                    ])
    """
    """
    getifacetype is called multiple times in actual_pinmux.py
    x = ifaces.getifacetype(temp), where temp is uart_rx, spi_mosi
    Purpose is to identify is function : input/output/inout
    """
    def getifacetype(self, name):
        for p in self.pinspecs:
            fname = "%s_%s" % (self.ifacename, p['name'])
            #print "search", self.ifacename, name, fname
            if fname == name:
                if p.get('action'):
                    return 'out'
                elif p.get('outen'):
                    return 'inout'
                return 'input'
        return None

    def pname(self, name):
        """ generates the interface spec e.g. flexbus_ale
            if there is only one flexbus interface, or
            sd{0}_cmd if there are several.  string format
            function turns this into sd0_cmd, sd1_cmd as
            appropriate.  single mode stops the numerical extension.
        """
        if self.single:
            return '%s_%s' % (self.ifacename, name)
        return '%s{0}_%s' % (self.ifacename, name)

    def busfmt(self, *args):
        """ this function creates a bus "ganging" system based
            on input from the {interfacename}.txt file.
            only inout pins that are under the control of the
            interface may be "ganged" together.
        """
        if not self.ganged:
            return '' # when self.ganged is None
        #print self.ganged
        res = []
        for (k, pnames) in self.ganged.items():
            name = self.pname('%senable' % k).format(*args)
            decl = 'Bit#(1) %s = 0;' % name
            res.append(decl)
            ganged = []
            for p in self.pinspecs:
                if p['name'] not in pnames:
                    continue
                pname = self.pname(p['name']).format(*args)
                if p.get('outen') is True:
                    outname = self.ifacefmtoutfn(pname)
                    ganged.append("%s_outen" % outname)  # match wirefmt

            gangedfmt = '{%s} = duplicate(%s);'
            res.append(gangedfmt % (',\n  '.join(ganged), name))
        return '\n'.join(res) + '\n\n'

    def wirefmt(self, *args):
        res = '\n'.join(map(self.wirefmtpin, self.pins)).format(*args)
        res += '\n'
        return '\n' + res

    def ifacefmt(self, *args):
        res = '\n'.join(map(self.ifacefmtdecpin, self.pins)).format(*args)
        return '\n' + res # pins is a list

    def ifacefmtdecfn(self, name):
        return name # like: uart

    def ifacefmtdecfn2(self, name):
        return name # like: uart

    def ifacefmtdecfn3(self, name):
        """ HACK! """
        return "%s_outen" % name #like uart_outen

    def ifacefmtoutfn(self, name):
        return "wr%s" % name #like wruart

    def ifacefmtinfn(self, name):
        return "wr%s" % name

    def wirefmtpin(self, pin):
        return pin.wirefmt(self.ifacefmtoutfn, self.ifacefmtinfn,
                           self.ifacefmtdecfn2)

    def ifacefmtdecpin(self, pin):
        return pin.ifacefmt(self.ifacefmtdecfn)

    def ifacefmtpin(self, pin):
        decfn = self.ifacefmtdecfn2
        outfn = self.ifacefmtoutfn
        #print pin, pin.outenmode
        if pin.outenmode:
            decfn = self.ifacefmtdecfn3
            outfn = self.ifacefmtoutenfn
        return pin.ifacedef(outfn, self.ifacefmtinfn,
                            decfn)

    def ifacedef(self, *args):
        res = '\n'.join(map(self.ifacefmtpin, self.pins))
        res = res.format(*args)
        return '\n' + res + '\n'


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


class Interfaces(UserDict):
    """ contains a list of interface definitions
    """

    def __init__(self, pth=None):
        self.pth = pth
        self.ifacecount = []
        UserDict.__init__(self, {})
        if not pth:
            return
        ift = 'interfaces.txt'
        if pth:
            ift = os.path.join(pth, ift)
        with open(ift, 'r') as ifile:
            for ln in ifile.readlines():
                ln = ln.strip()
                ln = ln.split("\t")
                name = ln[0] # will have uart
                count = int(ln[1]) # will have count of uart
                #spec looks like this:
                """
                [{'name': 'sda', 'outen': True},
                 {'name': 'scl', 'outen': True},
                ]
                """
                spec, ganged = self.read_spec(pth, name)
                iface = Interface(name, spec, ganged, count == 1)
                self.ifaceadd(name, count, iface)

    def getifacetype(self, fname):
        # finds the interface type, e.g sd_d0 returns "inout"
        for iface in self.values():
            typ = iface.getifacetype(fname)
            if typ:
                return typ
        return None

    def ifaceadd(self, name, count, iface, at=None):
        if at is None:
            at = len(self.ifacecount)# ifacecount is a list
        self.ifacecount.insert(at, (name, count))# appends the list
        # with (name,count) *at* times
        self[name] = iface

    """
    will check specific files of kind peripheral.txt like spi.txt,
    uart.txt in test directory
    """
    def read_spec(self, pth, name):
        spec = []
        ganged = {}
        fname = '%s.txt' % name
        if pth:
            ift = os.path.join(pth, fname)
        with open(ift, 'r') as sfile:
            for ln in sfile.readlines():
                ln = ln.strip()
                ln = ln.split("\t")
                name = ln[0]
                d = {'name': name}# here we start to make the dictionary
                if ln[1] == 'out':
                    d['action'] = True # adding element to the dict
                elif ln[1] == 'inout':
                    d['outen'] = True
                    if len(ln) == 3:
                        bus = ln[2]
                        if bus not in ganged:
                            ganged[bus] = []
                        ganged[bus].append(name)
                spec.append(d)
        return spec, ganged

    def ifacedef(self, f, *args):
        for (name, count) in self.ifacecount:
            for i in range(count):
                f.write(self.data[name].ifacedef(i))

    def busfmt(self, f, *args):
        f.write("import BUtils::*;\n\n")
        for (name, count) in self.ifacecount:
            for i in range(count):
                bf = self.data[name].busfmt(i)
                f.write(bf)

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

mux_interface = MuxInterface('cell', [{'name': 'mux', 'ready': False,
                                       'enabled': False,
                                       'bitspec': '{1}', 'action': True}])

io_interface = IOInterface(
    'io',
    [{'name': 'cell_out', 'enabled': True, },
     {'name': 'cell_outen', 'enabled': True, 'outenmode': True, },
     {'name': 'cell_in', 'action': True, 'io': True}, ])

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
            print (repr(p1))
            print (repr(p2))
            print ()
            assert p1 == p2

    ifaces = Interfaces()

    ifaceuart = ifaces['uart']
    print (ifaceuart.ifacedef(0))
    print (uartinterface_decl.ifacedef(0))
    assert ifaceuart.ifacedef(0) == uartinterface_decl.ifacedef(0)

    ifacetwi = ifaces['twi']
    print (ifacetwi.ifacedef(0))
    print (twiinterface_decl.ifacedef(0))
    assert ifacetwi.ifacedef(0) == twiinterface_decl.ifacedef(0)
