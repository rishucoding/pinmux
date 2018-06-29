import math
from string import digits
try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans


# ============== common bsv templates ============ #
# first argument is the io-cell number being assigned.
# second argument is the mux value.
# Third argument is the signal from the pinmap file
mux_wire = '''\
      rule assign_{2}_on_cell{0}(wrcell{0}_mux=={1});
        {2}<=cell{0}_mux_in;
      endrule
'''
dedicated_wire = '''
      rule assign_{1}_on_cell{0};
        {1}<=cell{0}_mux_in;
      endrule
'''
# ============================================================
digits = maketrans('0123456789', ' ' * 10)  # delete space later


def get_cell_bit_width(p):
    max_num_cells = 0
    for cell in p.muxed_cells:
        max_num_cells = max(len(cell) - 1, max_num_cells)
    return int(math.log(max_num_cells + 1, 2))


def cn(idx):  # idx is an integer
    return "cell%s_mux" % str(idx)


def transfn(temp):
    """ removes the number from the string of signal name.
    """
    temp = temp.split('_')
    if len(temp) == 2:
        temp[0] = temp[0].translate(digits)
        temp[0] = temp[0] .replace(' ', '')
    return '_'.join(temp)


# XXX this needs to move into interface_decl.py
# and made to use ifaceoutfmtfn and ifaceinfmtfn
def fmt(ifaces, cells, idx, suffix=None):
    """ blank entries need to output a 0 to the pin (it could just as
        well be a 1 but we choose 0).  reason: blank entries in
        the pinmap.txt file indicate that there's nothing to choose
        from.  however the user may still set the muxer to that value,
        and rather than throw an exception we choose to output... zero.

        NOTE: IMPORTANT.  when a function is an output-only there
        is a special-case assumption that:
        * (a) GPIO is always the first mux entry
        * (b) GPIO's outen is also used to set the pad
        the reason for this is that it is assumed better that
        multiple pads be switched simutaneously to outputs
        by setting the GPIO direction rather than having them
        set arbitrarily by changing the muxer registers.
    """
    idx += 1
    if idx < len(cells):
        cell = cells[idx]
    else:
        cell = ''
    if not cell:
        return '0'
    temp = transfn(cell)
    x = ifaces.getifacetype(temp)
    if x == 'input':
        return '0'  # inputs don't get passed through to the out mux
    if suffix == '_outen' and x == 'out':
        return "wr%s%s" % (cells[1], suffix or '') # USE GPIO FOR SELECTION
    return "wr%s%s" % (cell, suffix or '')

# XXX this needs to move into interface_decl.py


def mkcomment(ifaces, cell, idx, outenmode=False):
    """ returns a comment string for the cell when muxed
    """
    idx += 1
    if idx >= len(cell):
        return ' // unused'
    cname = cell[idx]
    if not cname:
        return ' // unused'
    temp = transfn(cname)
    x = ifaces.getifacetype(temp)
    #print (cname, x)
    if x == 'input':
        return ' // %s is an input' % cname
    if outenmode and x == 'inout':
        return ' // bi-directional'
    if outenmode and x == 'out':
        return ' // %s is an output' % cname

    return ""


def mkmux(p, ifaces, cell, suffix, outenmode):
    """ creates a straight many-to-one muxer that accepts
        multiple inputs and, based on an "address" routes
        a given indexed input through to the (one) output
    """
    comment = 'outen' if outenmode else 'output'
    fmtstr = "\t\t\twr%s==%d?%s:%s\n"  # mux-selector format
    ret = ''
    ret += "      // %s muxer for cell idx %s\n" % (comment, cell[0])
    ret += "      %s%s=\n" % (cn(cell[0]), suffix)
    for i in range(
            0, (1 << p.cell_bitwidth) - 1):  # full mux range (minus 1)
        comment = mkcomment(ifaces, cell, i, outenmode)
        cf = fmt(ifaces, cell, i, suffix)
        ret += fmtstr % (cn(cell[0]), i, cf, comment)
    comment = mkcomment(ifaces, cell, i + 1, outenmode)
    ret += "\t\t\t" + fmt(ifaces, cell, i + 1, suffix)  # last line
    ret += ";%s\n" % comment

    return ret


def init(p, ifaces):
    """ generates the actual output pinmux for each io-cell.  blank lines
        need to output "0" to the iopad, if there is no entry in
        that column.

        text is outputted in the format:
            x_out =
                muxer_sel==0 ? a :
                muxer_sel==1 ? b :
                muxer_sel==2 ? 0 :
                d

        last line doesn't need selector-logic, obviously.

        note that it's *important* that all muxer options be covered
        (hence going up to 1<<cell_bitwidth) even if the muxer cells
        are blank (no entries), because muxer selection could be to
        the last one, and we do not want the "default" (last line)
        to be the output.
    """
    p.cell_bitwidth = get_cell_bit_width(p)
    p.pinmux = ' '
    global dedicated_wire
    for cell in p.muxed_cells:

        # first do the outputs
        p.pinmux += mkmux(p, ifaces, cell, '_out', False)
        p.pinmux += "\n"

        # now do the output enablers (outens)
        p.pinmux += mkmux(p, ifaces, cell, '_outen', True)

        # ======================================================== #

        # check each cell if "peripheral input/inout" then assign its wire
        # Here we check the direction of each signal in the dictionary.
        # We choose to keep the dictionary within the code and not user-input
        # since the interfaces are always standard and cannot change from
        # user-to-user. Plus this also reduces human-error as well :)
        p.pinmux += "\n"
        p.pinmux += "      // priority-in-muxer for cell idx %s\n" % (cell[0])
        for i in range(0, len(cell) - 1):
            cname = cell[i + 1]
            if not cname:  # skip blank entries, no need to test
                continue
            temp = transfn(cname)
            x = ifaces.getifacetype(temp)
            #print (cname, temp, x)
            assert x is not None, "ERROR: The signal : " + \
                str(cname) + \
                " of pinmap.txt isn't present \nin the current" + \
                " dictionary. Update dictionary or fix-typo."
            if x == "input":
                p.pinmux += \
                    mux_wire.format(cell[0], i, "wr" + cname) + "\n"
            elif x == "inout":
                p.pinmux += \
                    mux_wire.format(cell[0], i, "wr" + cname +
                                                "_in") + "\n"
    # ============================================================ #

    # ==================  Logic for dedicated pins ========= #
    p.pinmux += "\n      /*=========================================*/\n"
    p.pinmux += "      // dedicated cells\n\n"
    for cell in p.dedicated_cells:
        p.pinmux += "      // dedicated cell idx %s\n" % (cell[0])
        p.pinmux += "      %s_out=%s_io;\n" % (cn(cell[0]), cell[1])
        temp = transfn(cell[1])
        x = ifaces.getifacetype(temp)
        #print cell, temp, x
        if x == "input":
            p.pinmux += \
                dedicated_wire.format(cell[0], "wr" + cell[1]) + "\n"
        elif x == "inout":
            p.pinmux += \
                dedicated_wire.format(cell[0], "wr" + cell[1] + "_in") + "\n"
        else:
            p.pinmux += "\n"
    # =======================================================#
