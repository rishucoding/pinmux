import os
import sys
from parse import Parse
from myhdlgen.pins import IO
from ifacebase import InterfacesBase
try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans

# XXX hmmm duplicated from src/bsc/actual_pinmux.py
digits = maketrans('0123456789', ' ' * 10)  # delete space later

# XXX hmmm duplicated from src/bsc/actual_pinmux.py


def transfn(temp):
    """ removes the number from the string of signal name.
    """
    temp = temp.split('_')
    if len(temp) == 2:
        temp[0] = temp[0].translate(digits)
        temp[0] = temp[0] .replace(' ', '')
    return '_'.join(temp)


class Interface(object):
    """ create an interface from a list of pinspecs.
        each pinspec is a dictionary, see Pin class arguments
        single indicates that there is only one of these, and
        so the name must *not* be extended numerically (see pname)
    """
    # sample interface object:
    """
    twiinterface_decl = Interface('twi',
                                  [{'name': 'sda', 'type': 'in'},
                                   {'name': 'scl', 'type': 'inout'},
                                   ])
    """

    def __init__(self, ifacename, pinspecs, ganged=None, single=False):
        self.ifacename = ifacename
        self.ganged = ganged or {}
        self.pins = []  # a list of instances of class Pin
        self.pinspecs = pinspecs  # a list of dictionary
        self.single = single
        for p in pinspecs:
            _p = {}
            _p['name'] = self.pname(p['name'])
            _p['typ'] = self.pname(p['type'])
            self.pins.append(IO(**_p))

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


class Interfaces(InterfacesBase):
    """ contains a list of interface definitions
    """

    def __init__(self, pth=None):
        InterfacesBase.__init__(self, Interface, pth)

def create_module(p, ifaces):
    x = """\
from myhdl import block
@block
def pinmux(muxfn, clk, p, ifaces, {0}):
    args = [{0}]
    return muxfn(clk, p, ifaces, args)
"""

    args = []
    for cell in p.muxed_cells:
        args.append("sel%d" % int(cell[0]))
        args.append("io%d" % int(cell[0]))
    print args
    kl = ifaces.keys()
    kl.sort()
    for k, count in ifaces.ifacecount:
        i = ifaces[k]
        for c in range(count):
            print k
            args.append("%s%d" % (k, c))
    args = ',\n\t\t'.join(args)
    x = x.format(args)
    path = os.path.abspath(__file__)
    fname = os.path.split(path)[0]
    fname = os.path.join(fname, "myhdlautogen.py")

    with open(fname, "w") as f:
        f.write(x)
    x = "from myhdlgen.myhdlautogen import pinmux"
    code = compile(x, '<string>', 'exec')
    y = {}
    exec code in y
    x = y["pinmux"]

    return x


def init(p, ifaces):
    for cell in p.muxed_cells:

        for i in range(0, len(cell) - 1):
            cname = cell[i + 1]
            if not cname:  # skip blank entries, no need to test
                continue
            temp = transfn(cname)
            x = ifaces.getifacetype(temp)
            print (cname, temp, x)


def pinmuxgen(pth=None, verify=True):
    p = Parse(pth, verify)
    print (p, dir(p))
    ifaces = Interfaces(pth)
    init(p, ifaces)
    create_module(p, ifaces)
