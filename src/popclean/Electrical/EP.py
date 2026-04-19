from Atom import Atom
from ComplexT import ComplexT
from RealT import RealT
import g


class EP(Atom):
    def __init__(e, p, **kwargs):

        e.parent = p
        e.name1 = ""
        # variables
        e.VIDL = list()
        e.__dict__.update(kwargs)

        # engineering variables
        e.freq = RealT(e, units="hz", desc="frequency")
        e.freq.name1 = "freq"
        e.I = ComplexT(e, units="amps", desc="Amperage")
        e.I.name1 = "I"
        e.Ii = RealT(e, units="amps", desc="Imaginary amperage")
        e.Ii.name1 = "Ii"
        e.Ir = RealT(e, units="amps", desc="Real amperage")
        e.Ir.name1 = "Ir"
        e.V = ComplexT(e, units="volts", desc="Voltage")
        e.V.name1 = "V"
        e.Vr = RealT(e, units="volts", desc="Real voltage")
        e.Vr.name1 = "Vr"
        e.Vi = RealT(e, units="volts", desc="Imaginary voltage")
        e.Vi.name1 = "Vi"

        p.addVID(e)
        e.type = "EP"

    def isa(e, type):
        if type == "EP":
            return True
        else:
            return False

    # set the conditions in this port and connected port
    def setIV(e, I, V):
        e.I.set(I)
        e.V.set(V)
        e.other.I.set(I)
        e.other.V.set(V)
        e.Vr.set(e.V.v.real)
        e.Vi.set(e.V.v.imag)
        e.Ir.set(e.I.v.real)
        e.Ii.set(e.I.v.imag)
        e.other.Vr.set(e.V.v.real)
        e.other.Vi.set(e.V.v.imag)
        e.other.Ir.set(e.I.v.real)
        e.other.Ii.set(e.I.v.imag)

    def addVID(self, v):
        self.VIDL.append(v)

    # link this port to another port
    def linkEP(e, EP):
        e.other = EP
        EP.other = e

    def linkE(e, E):
        E.linkE(e)

    def dump(e):
        print(e.parent.name1, e.name1, e.V.v, e.I.v, file=g.out)

    def hover(e):
        return e.parent.name1 + " " + e.name1 + " " + str(e.V.v) + " " + str(e.I.v)

    def savePrint(e):
        return ""

    def pretty(e):
        print(
            f"{e.parent.name1[:8]:12s}{e.name1[:8]:12s}Vr:{str(e.Vr.v)[:8]:12s}Vi:{str(e.Vi.v)[:8]:12s}Ir:{str(e.Ir.v)[:8]:12s}Ii:{str(e.Ii.v)[:8]:12s}",
            file=g.pretty,
        )
