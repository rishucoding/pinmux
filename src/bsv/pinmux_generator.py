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
import os
import os.path
import time
import math

# project module imports
from bsv.interface_decl import Interfaces, mux_interface, io_interface
from parse import Parse
from bsv.actual_pinmux import init
from bsv.bus_transactors import axi4_lite

copyright = '''
/*
   This BSV file has been generated by the PinMux tool available at:
   https://bitbucket.org/casl/pinmux.

   Authors: Neel Gala, Luke
   Date of generation: ''' + time.strftime("%c") + '''
*/
'''
header = copyright + '''
package pinmux;

   typedef struct{
      Bit#(1) outputval;      // output from core to pad                bit7
      Bit#(1) output_en;      // output enable from core to pad         bit6
      Bit#(1) input_en;       // input enable from core to io_cell      bit5
      Bit#(1) pullup_en;      // pullup enable from core to io_cell     bit4
      Bit#(1) pulldown_en;    // pulldown enable from core to io_cell   bit3
      Bit#(1) drivestrength;  // drivestrength from core to io_cell     bit2
      Bit#(1) pushpull_en;    // pushpull enable from core to io_cell   bit1
      Bit#(1) opendrain_en;   // opendrain enable form core to io_cell  bit0
   } GenericIOType deriving(Eq,Bits,FShow);

'''
footer = '''
     endinterface;
   endmodule
endpackage
'''


def pinmuxgen(pth=None, verify=True):
    """ populating the file with the code
    """

    p = Parse(pth, verify)
    ifaces = Interfaces(pth)
    ifaces.ifaceadd('io', p.N_IO, io_interface, 0)
    init(p, ifaces)

    bp = 'bsv_src'
    if pth:
        bp = os.path.join(pth, bp)
    if not os.path.exists(bp):
        os.makedirs(bp)

    bus = os.path.join(bp, 'busenable.bsv')
    pmp = os.path.join(bp, 'pinmux.bsv')
    ptp = os.path.join(bp, 'PinTop.bsv')
    bvp = os.path.join(bp, 'bus.bsv')

    write_pmp(pmp, p, ifaces)
    write_ptp(ptp, p, ifaces)
    write_bvp(bvp, p, ifaces)
    write_bus(bus, p, ifaces)


def write_bus(bus, p, ifaces):
    # package and interface declaration followed by
    # the generic io_cell definition
    with open(bus, "w") as bsv_file:
        ifaces.busfmt(bsv_file)


def get_cell_bit_width(p):
    max_num_cells = 0
    for cell in p.muxed_cells:
            max_num_cells = max(len(cell)-1, max_num_cells)
    return int(math.log(max_num_cells, 2))

def write_pmp(pmp, p, ifaces):
    # package and interface declaration followed by
    # the generic io_cell definition
    with open(pmp, "w") as bsv_file:
        bsv_file.write(header)

        bsv_file.write('''\
   interface MuxSelectionLines;

      // declare the method which will capture the user pin-mux
      // selection values.The width of the input is dependent on the number
      // of muxes happening per IO. For now we have a generalized width
      // where each IO will have the same number of muxes.''')

        for cell in p.muxed_cells:
            cnum = 'Bit#(' + str(int(math.log(len(cell) - 1, 2))) + ')'
            bsv_file.write(mux_interface.ifacefmt(cell[0], cnum))

        bsv_file.write('''
      endinterface

      interface PeripheralSide;
      // declare the interface to the IO cells.
      // Each IO cell will have 8 input field (output from pin mux
      // and on output field (input to pinmux)''')
        # ==============================================================

        # == create method definitions for all peripheral interfaces ==#
        ifaces.ifacefmt(bsv_file)

        # ==============================================================

        # ===== finish interface definition and start module definition=======
        bsv_file.write('''
   endinterface

   interface Ifc_pinmux;
      interface MuxSelectionLines mux_lines;
      interface PeripheralSide peripheral_side;
   endinterface
   (*synthesize*)
   module mkpinmux(Ifc_pinmux);
''')
        # ====================================================================

        # ======================= create wire and registers =================#
        bsv_file.write('''
      // the followins wires capture the pin-mux selection
      // values for each mux assigned to a CELL
''')
        cell_bit_width = 'Bit#(%d)' % get_cell_bit_width(p)
        for cell in p.muxed_cells:
            bsv_file.write(mux_interface.wirefmt(
                cell[0], cell_bit_width))

        ifaces.wirefmt(bsv_file)

        bsv_file.write("\n")
        # ====================================================================
        # ========================= Actual pinmuxing ========================#
        bsv_file.write('''
      /*====== This where the muxing starts for each io-cell======*/
''')
        bsv_file.write(p.pinmux)
        bsv_file.write('''
      /*============================================================*/
''')
        # ====================================================================
        # ================= interface definitions for each method =============#
        bsv_file.write('''
    interface mux_lines = interface MuxSelectionLines
''')
        for cell in p.muxed_cells:
            bsv_file.write(
                mux_interface.ifacedef(
                    cell[0], cell_bit_width))
        bsv_file.write('''
    endinterface;
    interface peripheral_side = interface PeripheralSide
''')
        ifaces.ifacedef(bsv_file)
        bsv_file.write(footer)
        print("BSV file successfully generated: bsv_src/pinmux.bsv")
        # ======================================================================


def write_ptp(ptp, p, ifaces):
    with open(ptp, 'w') as bsv_file:
        bsv_file.write(copyright + '''
package PinTop;
    import pinmux::*;
    interface Ifc_PintTop;
        method ActionValue#(Bool) write(Bit#({0}) addr, Bit#({1}) data);
        method Tuple2#(Bool,Bit#({1})) read(Bit#({0}) addr);
        interface PeripheralSide peripheral_side;
    endinterface

    module mkPinTop(Ifc_PintTop);
        // instantiate the pin-mux module here
        Ifc_pinmux pinmux <-mkpinmux;

        // declare the registers which will be used to mux the IOs
'''.format(p.ADDR_WIDTH, p.DATA_WIDTH))

        cell_bit_width = str(get_cell_bit_width(p))
        for cell in p.muxed_cells:
            bsv_file.write('''
                Reg#(Bit#({0})) rg_muxio_{1} <-mkReg(0);'''.format(
                cell_bit_width, cell[0]))

        bsv_file.write('''
        // rule to connect the registers to the selection lines of the
        // pin-mux module
        rule connect_selection_registers;''')

        for cell in p.muxed_cells:
            bsv_file.write('''
          pinmux.mux_lines.cell{0}_mux(rg_muxio_{0});'''.format(cell[0]))

        bsv_file.write('''
        endrule
        // method definitions for the write user interface
        method ActionValue#(Bool) write(Bit#({2}) addr, Bit#({3}) data);
          Bool err=False;
          case (addr[{0}:{1}])'''.format(p.upper_offset, p.lower_offset,
                                         p.ADDR_WIDTH, p.DATA_WIDTH))
        index = 0
        for cell in p.muxed_cells:
            bsv_file.write('''
            {0}: rg_muxio_{1}<=truncate(data);'''.format(index, cell[0]))
            index = index + 1

        bsv_file.write('''
            default: err=True;
          endcase
          return err;
        endmethod''')

        bsv_file.write('''
        // method definitions for the read user interface
        method Tuple2#(Bool,Bit#({3})) read(Bit#({2}) addr);
          Bool err=False;
          Bit#(32) data=0;
          case (addr[{0}:{1}])'''.format(p.upper_offset, p.lower_offset,
                                         p.ADDR_WIDTH, p.DATA_WIDTH))
        index = 0
        for cell in p.muxed_cells:
            bsv_file.write('''
                {0}: data=zeroExtend(rg_muxio_{1});'''.format(index, cell[0]))
            index = index + 1

        bsv_file.write('''
            default:err=True;
          endcase
          return tuple2(err,data);
        endmethod
        interface peripheral_side=pinmux.peripheral_side;
    endmodule
endpackage
''')


def write_bvp(bvp, p, ifaces):
    # ######## Generate bus transactors ################
    with open(bvp, 'w') as bsv_file:
        bsv_file.write(axi4_lite.format(p.ADDR_WIDTH, p.DATA_WIDTH))
    # ##################################################
