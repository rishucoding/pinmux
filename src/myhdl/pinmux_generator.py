from parse import Parse

def pinmuxgen(pth=None, verify=True):
    p = Parse(pth, verify)
    print p, dir(p)

