# mux.py

from myhdl import *
from myhdl._block import _Block
from mux import mux4
from functools import wraps, partial
import inspect

period = 20  # clk frequency = 50 MHz


class IO(object):
    def __init__(self, typ, name, inp=None, out=None, dirn=None):
        self.typ = typ
        self.name = name
        if typ == 'in' or typ == 'inout':
            self.inp = inp # Signal(bool(0))
        if typ == 'out' or typ == 'inout':
            self.out = out # Signal(bool(0))
        if typ == 'inout':
            self.dirn = dirn # Signal(bool(0))


class Mux(object):
    def __init__(self, sel):#bwidth=2):
        self.sel = sel


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


def create_test(npins=2, nfns=4):
    x = """\
from myhdl import block
@block
def test(testfn, clk, num_pins, num_fns, {0}):
    args = ({0})
    return testfn(clk, num_pins, num_fns, args)
"""

    args = []
    for pnum in range(npins):
        args.append("sel%d" % pnum)
        args.append("pin%d" % pnum)
    for pnum in range(nfns):
        args.append("fn%d" % pnum)
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
def test2(clk, num_pins, num_fns, args):
    muxes = []
    pins = []
    fns = []
    args = list(args)
    for i in range(num_pins):
        muxes.append(args.pop(0))
        pins.append(args.pop(0))
    for i in range(num_fns):
        fns.append(args.pop(0))

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
    dirs = []
    fins = []
    fouts = []
    fdirs = []
    args = []
    for i in range(2):
        sel = Signal(intbv(0)[2:0])
        m = Mux(sel)
        muxes.append(m)
        muxvals.append(sel)
        args.append(m)
        inp = Signal(bool(0))
        out = Signal(bool(0))
        dirn = Signal(bool(0))
        pin = IO("inout", "name%d" % i, inp=inp, out=out, dirn=dirn)
        pins.append(pin)
        args.append(pin)
        ins.append(inp)
        outs.append(out)
        dirs.append(dirn)
    fns = []
    for i in range(4):
        inp = Signal(bool(0))
        out = Signal(bool(0))
        dirn = Signal(bool(0))
        fn = IO("inout", "fnname%d" % i, inp=inp, out=out, dirn=dirn)
        fns.append(fn)
        fins.append(inp)
        fouts.append(out)
        fdirs.append(dirn)
        args.append(fn)
    clk = Signal(bool(0))

    mux_inst = test(test2, clk, 2, 4, *args)

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
    dirs = []
    fins = []
    fouts = []
    fdirs = []
    args = []
    for i in range(2):
        sel = Signal(intbv(0)[2:0])
        m = Mux(sel)
        muxes.append(m)
        muxvals.append(sel)
        args.append(m)
        inp = Signal(bool(0))
        out = Signal(bool(0))
        dirn = Signal(bool(0))
        pin = IO("inout", "name%d" % i, inp=inp, out=out, dirn=dirn)
        pins.append(pin)
        args.append(pin)
        ins.append(inp)
        outs.append(out)
        dirs.append(dirn)
    fns = []
    for i in range(4):
        inp = Signal(bool(0))
        out = Signal(bool(0))
        dirn = Signal(bool(0))
        fn = IO("inout", "fnname%d" % i, inp=inp, out=out, dirn=dirn)
        fns.append(fn)
        fins.append(inp)
        fouts.append(out)
        fdirs.append(dirn)
        args.append(fn)
    clk = Signal(bool(0))

    mux_inst = test(test2, clk, 2, 4, *args)
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
