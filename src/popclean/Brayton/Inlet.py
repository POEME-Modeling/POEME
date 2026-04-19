from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from StringT import StringT
from FN import FN
from Table1d import Table1d
import g


class Inlet(Element):

    def __init__(i, name):
        super().__init__(name, "Inlet")
        i.type = "Inlet"
        i.desc = "Inlet with simple recovery"

        # Variables
        i.rec = RealT(i, v=0.0, units="none", desc="Inlet recovery")

        # Fluid locations
        i.FNi = FN(i, io="in", desc="Incoming flow")
        i.FNo = FN(i, io="out", desc="Outgoing flow")

        i.initialList()

    def calc(i):
        # pass incoming flow information
        i.FNo.copy(i.FNi)
        # keep enthalpy constant and apply a pressure drop
        i.FNo.set_hP(i.FNo.ht, i.FNo.Pt * (i.rec))

    def dump(i):
        print(i.name1, "Duct", file=g.out)
        super().realPrint()

    def pretty(i):
        print(
            f"{"Inlet":12s}{i.name1[:10]:12s}{("rec:"+str(i.rec))[:10]:12s}",
            file=g.pretty,
        )
