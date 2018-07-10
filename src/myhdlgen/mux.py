# mux.py

from math import log
from myhdl import *

period = 20  # clk frequency = 50 MHz


class Inputs(object):
    def __init__(self, ins):
        self.ins = ins
        self.in_a = ins[0]
        self.in_b = ins[1]
        self.in_c = ins[2]
        self.in_d = ins[3]


class Selectors(object):
    def __init__(self, sels):
        self.sels = sels
        self.sel_a = sels[0]
        self.sel_b = sels[1]
        self.sel_c = sels[2]
        self.sel_d = sels[3]


@block
def mux4(clk, ins,
         selector, out):

    (in_a, in_b, in_c, in_d) = ins
    print repr(clk), ins, repr(selector), repr(out)

    @always(selector, in_a, in_b, in_c, in_d)
    def make_out():
        out.next = bool(in_a if selector == 0 else False) | \
            bool(in_b if selector == 1 else False) | \
            bool(in_c if selector == 2 else False) | \
            bool(in_d if selector == 3 else False)

    return instances()  # return all instances


@block
def pmux1(clk, in_a,
          sel_a, out):

    @always(sel_a,
            in_a)
    def make_out():
        if sel_a:
            out.next = in_a
        else:
            out.next = False

    return instances()  # return all instances


@block
def pmux2(clk, in_a, in_b,
          sel_a, sel_b, out):

    @always(sel_a, sel_b,
            in_a, in_b)
    def make_out():
        if sel_a:
            out.next = in_a
        elif sel_b:
            out.next = in_b
        else:
            out.next = False

    return instances()  # return all instances


@block
def pmux3(clk, in_a, in_b, in_c,
          sel_a, sel_b, sel_c, out):

    @always(sel_a, sel_b, sel_c,
            in_a, in_b, in_c)
    def make_out():
        if sel_a:
            out.next = in_a
        elif sel_b:
            out.next = in_b
        elif sel_c:
            out.next = in_c
        else:
            out.next = False

    return instances()  # return all instances


@block
def pmux4(clk, ins, sels, out):

    @always(*list(sels.sels) + list(ins.ins))
    def make_out():
        if sels.sel_a:
            out.next = ins.in_a
        elif sels.sel_b:
            out.next = ins.in_b
        elif sels.sel_c:
            out.next = ins.in_c
        elif sels.sel_d:
            out.next = ins.in_d
        else:
            out.next = False

    i = instances()
    print dir(i), i
    return i  # return all instances


# testbench
@block
def pmux_tb4():

    clk = Signal(bool(0))
    in_a = Signal(bool(0))
    in_b = Signal(bool(0))
    in_c = Signal(bool(0))
    in_d = Signal(bool(0))
    sel_a = Signal(bool(0))
    sel_b = Signal(bool(0))
    sel_c = Signal(bool(0))
    sel_d = Signal(bool(0))
    out = Signal(bool(0))

    sels = Selectors((sel_a, sel_b, sel_c, sel_d))
    ins = Inputs((in_a, in_b, in_c, in_d))
    mux_inst = pmux4(clk, ins, sels, out)

    @instance
    def clk_signal():
        while True:
            sel_set = False
            clk.next = not clk
            if clk:
                in_a.next = not in_a
                if in_a:
                    in_b.next = not in_b
                    if in_b:
                        in_c.next = not in_c
                        if in_c:
                            in_d.next = not in_d
                            if in_d:
                                sel_set = True
            if sel_set:
                sel_a.next = not sel_a
                if sel_a:
                    sel_b.next = not sel_b
                    if sel_b:
                        sel_c.next = not sel_c
                        if sel_c:
                            sel_d.next = not sel_d
            yield delay(period // 2)

    # print simulation data on screen and file
    file_data = open("pmux.csv", 'w')  # file for saving data
    # # print header on screen
    s = "{0},{1},{2},{3},{4},{5},{6},{7},{8}".format(
        "in_a", "in_b", "in_c", "in_d",
        "sel_a", "sel_b", "sel_c", "sel_d",
        "out")
    print(s)
    # # print header to file
    file_data.write(s)
    # print data on each clock

    @always(clk.posedge)
    def print_data():
        # print on screen
        # print.format is not supported in MyHDL 1.0
        print ("%s,%s,%s,%s,%s,%s,%s,%s,%s" %
               (in_a, in_b,
                in_c, in_d,
                sel_a, sel_b,
                sel_c, sel_d, out))

        if sel_a:
            assert out == in_a
        elif sel_b:
            assert out == in_b
        elif sel_c:
            assert out == in_c
        elif sel_d:
            assert out == in_d
        # print in file
        # print.format is not supported in MyHDL 1.0
        #file_data.write(s + "\n")

    return instances()

# testbench


@block
def mux_tb():

    clk = Signal(bool(0))
    in_a = Signal(bool(0))
    in_b = Signal(bool(0))
    in_c = Signal(bool(0))
    in_d = Signal(bool(0))
    selector = Signal(intbv(0)[2:0])
    out = Signal(bool(0))

    mux_inst = mux4(clk, in_a, in_b, in_c, in_d, selector, out)

    @instance
    def clk_signal():
        while True:
            clk.next = not clk
            if clk:
                in_a.next = not in_a
                if in_a:
                    in_b.next = not in_b
                    if in_b:
                        in_c.next = not in_c
                        if in_c:
                            in_d.next = not in_d
                            if in_d:
                                if selector == 3:
                                    selector.next = 0
                                else:
                                    selector.next = selector + 1
            yield delay(period // 2)

    # print simulation data on screen and file
    file_data = open("mux.csv", 'w')  # file for saving data
    # # print header on screen
    s = "{0},{1},{2},{3},{4},{5}".format("in_a", "in_b", "in_c", "in_d",
                                         "selector", "out")
    print(s)
    # # print header to file
    file_data.write(s)
    # print data on each clock

    @always(clk.posedge)
    def print_data():
        # print on screen
        # print.format is not supported in MyHDL 1.0
        print ("%s,%s,%s,%s,%s,%s" %
               (in_a, in_b,
                in_c, in_d,
                selector, out))

        if selector == 0:
            assert out == in_a
        elif selector == 1:
            assert out == in_b
        elif selector == 2:
            assert out == in_c
        elif selector == 3:
            assert out == in_d
        # print in file
        # print.format is not supported in MyHDL 1.0
        #file_data.write(s + "\n")

    return instances()


def test_mux():

    clk = Signal(bool(0))
    in_a = Signal(bool(0))
    in_b = Signal(bool(0))
    in_c = Signal(bool(0))
    in_d = Signal(bool(0))
    selector = Signal(intbv(0)[2:0])
    out = Signal(bool(0))

    mux_v = mux4(clk, in_a, in_b, in_c, in_d, selector, out)
    mux_v.convert(hdl="Verilog", initial_values=True)

    # test bench
    tb = mux_tb()
    tb.convert(hdl="Verilog", initial_values=True)
    # keep following lines below the 'tb.convert' line
    # otherwise error will be reported
    tb.config_sim(trace=True)
    tb.run_sim(66 * period)  # run for 15 clock cycle


def test_pmux4():

    clk = Signal(bool(0))
    in_a = Signal(bool(0))
    in_b = Signal(bool(0))
    in_c = Signal(bool(0))
    in_d = Signal(bool(0))
    sel_a = Signal(bool(0))
    sel_b = Signal(bool(0))
    sel_c = Signal(bool(0))
    sel_d = Signal(bool(0))
    out = Signal(bool(0))

    sels = Selectors((sel_a, sel_b, sel_c, sel_d))
    ins = Inputs((in_a, in_b, in_c, in_d))
    pmux_v = pmux4(clk, ins, sels, out)
    pmux_v.convert(hdl="Verilog", initial_values=True)

    # test bench
    tb = pmux_tb4()
    tb.convert(hdl="Verilog", initial_values=True)
    # keep following lines below the 'tb.convert' line
    # otherwise error will be reported
    tb.config_sim(trace=True)
    tb.run_sim(4 * 66 * period)  # run for 15 clock cycle


if __name__ == '__main__':
    # test_mux()
    print "test pmux"
    test_pmux4()
