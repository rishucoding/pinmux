from parse import Parse
from ifacebase import InterfacesBase
try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans

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


class Interface(object):
    """ create an interface from a list of pinspecs.
        each pinspec is a dictionary, see Pin class arguments
        single indicates that there is only one of these, and
        so the name must *not* be extended numerically (see pname)
    """
    # sample interface object:
    """
    twiinterface_decl = Interface('twi',
                                  [{'name': 'sda', 'outen': True},
                                   {'name': 'scl', 'outen': True},
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
            _p.update(p)
            if p.get('outen') is True:  # special case, generate 3 pins
                del _p['outen']
                for psuffix in ['out', 'outen', 'in']:
                    # changing the name (like sda) to (twi_sda_out)
                    _p['name'] = "%s_%s" % (self.pname(p['name']), psuffix)
                    _p['action'] = psuffix != 'in'
                    self.pins.append(Pin(**_p))
                    # will look like {'name': 'twi_sda_out', 'action': True}
                    # {'name': 'twi_sda_outen', 'action': True}
                    #{'name': 'twi_sda_in', 'action': False}
                    # NOTice - outen key is removed
            else:
                _p['name'] = self.pname(p['name'])
                self.pins.append(Pin(**_p))

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
    print p, dir(p)
    ifaces = Interfaces(pth)
    init(p, ifaces)
