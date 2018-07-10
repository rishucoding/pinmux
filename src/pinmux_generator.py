# ================================== Steps to add peripherals ============
# Step-1:   create interface declaration for the peripheral to be added.
#           Remember these are interfaces defined for the pinmux and hence
#           will be opposite to those defined at the peripheral.
#           For eg. the output TX from the UART will be input (method Action)
#           for the pinmux.
#           These changes will have to be done in interface_decl.py
# Step-2    define the wires that will be required to transfer data from the
#           peripheral interface to the IO cell and vice-versa. Create a
#           mkDWire for each input/output between the peripheral and the
#           pinmux. Also create an implicit wire of GenericIOType for each cell
#           that can be connected to a each bit from the peripheral.
#           These changes will have to be done in wire_def.py
# Step-3:   create the definitions for each of the methods defined above.
#           These changes will have to be done in interface_decl.py
# ========================================================================

# default module imports
import getopt
import os.path
import sys
from spec import modules, specgen, dummytest

from bsv.pinmux_generator import pinmuxgen as bsvgen
from myhdl.pinmux_generator import pinmuxgen as myhdlgen


def printhelp():
    print ('''pinmux_generator.py [-o outputdir] [-v|--validate] [-h|--help]
                                  [-t outputtype] [-s|--spec spec]
    -s | spec       : generate from spec (python module)
    -t | outputtype : outputtype, defaults to bsv
    -o outputdir    : defaults to bsv_src.  also location for reading pinmux.txt
                      interfaces.txt and *.txt
    -v | --validate : runs some validation on the pinmux
    -h | --help     : this help message
''')


if __name__ == '__main__':
    try:
        options, remainder = getopt.getopt(
            sys.argv[1:],
            'o:vht:s:',
            ['output=',
             'validate',
             'test',
             'outputtype=',
             'spec=',
             'help',
             'version=',
             ])
    except getopt.GetoptError as err:
        print ("ERROR: %s" % str(err))
        printhelp()
        sys.exit(1)

    output_type = 'bsv'
    output_dir = None
    validate = False
    spec = None
    pinspec = None
    testing = False
    for opt, arg in options:
        if opt in ('-o', '--output'):
            output_dir = arg
        elif opt in ('-s', '--spec'):
            pinspec = arg
        elif opt in ('-t', '--outputtype'):
            output_type = arg
        elif opt in ('-v', '--validate'):
            validate = True
        elif opt in ('--test',):
            testing = True
        elif opt in ('-h', '--help'):
            printhelp()
            sys.exit(0)

    if pinspec:
        if pinspec not in modules:
            print ("ERROR: spec type '%s' does not exist" % pinspec)
            printhelp()
            sys.exit(1)
        module = modules[pinspec]

        fname = os.path.join(output_dir or '', "%s.mdwn" % pinspec)
        d = os.path.split(fname)[0]
        if not os.path.exists(d):
            os.makedirs(d)
        with open(fname, "w") as of:
            ps = module.pinspec()
            pinout, bankspec, pinspec, fixedpins = ps.write(of)
            if testing:
                dummytest(ps, output_dir, output_type)
            else:
                specgen(of, output_dir, pinout, bankspec, pinspec, fixedpins)
    else:
        gentypes = {'bsv': bsvgen, 'myhdl': myhdlgen }
        if output_type not in gentypes:
            print ("ERROR: output type '%s' does not exist" % output_type)
            printhelp()
            sys.exit(0)
        gentypes[output_type](output_dir, validate)
