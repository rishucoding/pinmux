try:
    from UserDict import UserDict
except ImportError:
    from collections import UserDict


class Wire(object):
    """ a wire which can be hi, lo or tri-state
    """

    def __init__(self, wires, name):
        self.wires = wires
        self.wires[name] = self
        self.name = name
        self.val = 'x'


class TestPin(object):
    """ a test pin can be an output, input or in-out
        and it stores the state in an associated wire
    """


class Wires(UserDict):
    """ a set of wires
    """

    def __init__(self):
        UserDict.__init__(self)


def dummytest(ps, output_dir, output_type):
    print (ps, output_dir, output_type)
    print (dir(ps))
    print (ps.fnspec)

    # basically we need to replicate the entirety of the
    # verilog module's inputs and outputs, so that we can
    # set inputs hi/lo and then test expected outputs hi/lo.
    # so, set up some wires by going through the interfaces
    w = Wires()
