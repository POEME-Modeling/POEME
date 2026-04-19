from Atom import Atom
from ComplexT import ComplexT
from RealT import RealT
import g


class Fp(Atom):
    def __init__(f, p, io, desc):

        # variables
        f.VIDL = list()
        f.name1 = ""
        f.desc = desc
        f.parent = p
        f.io = io

        # engineering variables
        f.F = RealT(f, units="lbf", desc="Force")
        f.x = RealT(f, units="ft", desc="x location")
        f.V = RealT(f, units="ft/sec", desc="velocity")

        p.addVID(f)
        f.type = "Fp"
        f.other = 0

    def isa(e, type):
        if type == "Fp":
            return True
        else:
            return False

    # set the conditions in this port and connected port
    def setxV(f, x, V):
        f.x.v = x.v
        if isinstance(V, float):
            f.V.v = V
        else:
            f.V.v = V.v
        f.other.x.v = f.x.v
        f.other.V.v = f.V.v

    # set the conditions in this port and connected port
    def setF(f, F):
        f.F.v = F.v
        f.other.F.v = F.v

    def addVID(f, v):
        f.VIDL.append(v)

    # link this port to another port
    def linkFp(f, Fp):
        f.other = Fp
        Fp.other = f

    def dump(f):
        print(f.parent.name1, f.name1, f.x, f.V, file=g.out)

    def hover(f):
        return f.parent.name1 + " " + f.name1 + str(f.x.v) + " " + str(f.V.v)

    def pretty(f):
        print(
            f"{"Fp"[:10]:12s}{f.name1[:10]:12s}{("F:"+str(f.F))[:10]:12s}{("F:"+str(d.F))[:10]:12s}{("x:"+str(f.x))[:10]:12s}{("V:"+str(f.V))[:10]:12s}",
            file=g.pretty,
        )
