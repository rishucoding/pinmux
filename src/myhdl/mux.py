# mux.py

from math import log
from myhdl import *

period = 20  # clk frequency = 50 MHz


@block
def mux4(clk, in_a, in_b, in_c, in_d,
         selector, out):

    @always(selector, in_a, in_b, in_c, in_d)
    def make_out():
        out.next = bool(in_a if selector == 0 else False) | \
            bool(in_b if selector == 1 else False) | \
            bool(in_c if selector == 2 else False) | \
            bool(in_d if selector == 3 else False)

    return instances()  # return all instances


def pmux1(clk, in_a,
          selector_a, out):

    @always(selector_a,
            in_a)
    def make_out():
        if selector_a:
            out.next = in_a
        else:
            out.next = False

    return instances()  # return all instances


def pmux2(clk, in_a, in_b,
          selector_a, selector_b, out):

    @always(selector_a, selector_b,
            in_a, in_b)
    def make_out():
        if selector_a:
            out.next = in_a
        elif selector_b:
            out.next = in_b
        else:
            out.next = False

    return instances()  # return all instances


def pmux3(clk, in_a, in_b, in_c,
          selector_a, selector_b, selector_c, out):

    @always(selector_a, selector_b, selector_c,
            in_a, in_b, in_c)
    def make_out():
        if selector_a:
            out.next = in_a
        elif selector_b:
            out.next = in_b
        elif selector_c:
            out.next = in_c
        else:
            out.next = False

    return instances()  # return all instances


def pmux4(clk, in_a, in_b, in_c, in_d,
          selector_a, selector_b, selector_c, selector_d, out):

    @always(selector_a, selector_b, selector_c, selector_d,
            in_a, in_b, in_c, in_d)
    def make_out():
        if selector_a:
            out.next = in_a
        elif selector_b:
            out.next = in_b
        elif selector_c:
            out.next = in_c
        elif selector_d:
            out.next = in_d
        else:
            out.next = False

    return instances()  # return all instances


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


def main():

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


if __name__ == '__main__':
    main()
