# mux.py

from myhdl import *
from myhdl._block import _Block
from mux import mux4
from functools import wraps, partial
import inspect

period = 20  # clk frequency = 50 MHz


class IO(object):
    def __init__(self, typ, name):
        self.typ = typ
        if typ == 'in' or typ == 'inout':
            self.inp = Signal(bool(0))
        if typ == 'out' or typ == 'inout':
            self.out = Signal(bool(0))
        if typ == 'inout':
            self.dirn = Signal(bool(0))


class Mux(object):
    def __init__(self, bwidth=2):
        self.sel = Signal(intbv(0)[bwidth:0])


def f(obj):
    print('attr =', obj.attr)


@classmethod
def cvt(self, *args, **kwargs):
    print('args', self, args, kwargs)
    return block(test2)(*self._args).convert(*args, **kwargs)


def Test(*args):
    Foo = type(
        'Foo',
        (block,),
        {
            'test2': test2,
            'convert': cvt,
            '_args': args
        }
    )
    return Foo(test2)


def create_test():
    x = """\
from myhdl import block
@block
def test(testfn, {0}):
    args = ({0})
    return testfn(args)
"""
    args = ['clk', 'muxes', 'pins', 'fns']
    args = ','.join(args)
    x = x.format(args)
    print x
    print repr(x)
    with open("testmod.py", "w") as f:
        f.write(x)
    x = "from testmod import test"
    code = compile(x, '<string>', 'exec')
    y = {}
    exec code in y
    x = y["test"]

    def fn(*args):
        return block(x)
    return x


def proxy(func):
    def wrapper(*args):
        return func(args[0], args[1], args[2], args[3])
    return wrapper


@block
def test2(args):
    (clk, muxes, pins, fns) = args

    muxinst = []

    inputs = []
    for i in range(4):
        inputs.append(fns[i].inp)

    for i in range(len(muxes)):
        mux = muxes[i]
        pin = pins[i]
        inst = mux4(clk, inputs, mux.sel, pin.out)
        muxinst.append(inst)

    return muxinst


# testbench


@block
def mux_tb():

    muxvals = []
    muxes = []
    pins = []
    ins = []
    outs = []
    for i in range(2):
        m = Mux()
        muxes.append(m)
        muxvals.append(m.sel)
        pin = IO("inout", "name%d" % i)
        pins.append(pin)
        ins.append(pin.inp)
        outs.append(pin.out)
    fns = []
    for i in range(4):
        fns.append(IO("inout", "fnname%d" % i))
    clk = Signal(bool(0))

    mux_inst = test(test2, clk, muxes, pins, fns)

    @instance
    def clk_signal():
        while True:
            clk.next = not clk
            yield delay(period // 2)

    @always(clk.posedge)
    def print_data():
        # print on screen
        # print.format is not supported in MyHDL 1.0
        for i in range(len(muxes)):
            sel = muxvals[i]
            out = outs[i]
            print ("%d: %s %s" % (i, sel, out))

    return instances()


class Deco(object):
    def __init__(self):
        self.calls = 0


def test_mux():

    muxvals = []
    muxes = []
    pins = []
    ins = []
    outs = []

    for i in range(2):
        m = Mux()
        muxes.append(m)
        muxvals.append(m.sel)
        pin = IO("inout", "name%d" % i)
        pins.append(pin)
        ins.append(pin.inp)
        outs.append(pin.out)
    fns = []
    for i in range(4):
        fns.append(IO("inout", "fnname%d" % i))
    clk = Signal(bool(0))

    mux_inst = test(test2, clk, muxes, pins, fns)
    mux_inst.convert(hdl="Verilog", initial_values=True)
    #mux_inst = Test(clk, muxes, pins, fns)
    #toVerilog(mux_inst, clk, muxes, pins, fns)
    #deco = Deco()
    #b = _Block(mux_inst, deco, "test", "test.py", 1, clk, muxes, pins, fns)
    #b.convert(hdl="Verilog", name="test", initial_values=True)
    mux_inst.convert(hdl="Verilog", initial_values=True)
    #block(mux_inst).convert(hdl="Verilog", initial_values=True)

    # test bench
    tb = mux_tb()
    tb.convert(hdl="Verilog", initial_values=True)
    # keep following lines below the 'tb.convert' line
    # otherwise error will be reported
    tb.config_sim(trace=True)
    tb.run_sim(66 * period)  # run for 15 clock cycle

test = create_test()


if __name__ == '__main__':
    test_mux()
