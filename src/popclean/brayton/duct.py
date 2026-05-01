from popclean import Element, RealT, g

from .fn import FN


class Duct(Element):
    def __init__(self, name):
        super().__init__(name, "Duct")
        self.type = "Duct"

        self.desc = "Applies a constant enthalpy pressure drop"

        # Variables
        self.dP = RealT(self, v=0.0, units="none", desc="Pressure loss (fractional)")
        self.Q = RealT(self, v=0.0, units="BTU", desc="Heat added to the duct")
        self.Wbldfrac = RealT(self, io="out", desc="Bleed flow fraction")

        # Fluid locations
        self.FNi = FN(self, io="in", desc="Incoming flow")
        self.FNo = FN(self, io="out", desc="Outgoing flow")
        self.FNobld = FN(self, io="out", desc="Bleed flow")

        self.initialList()

    def calc(self):
        # pass incoming flow information
        self.FNo.copy(self.FNi)
        # keep enthalpy constant and apply a pressure drop
        self.FNo.set_hp(
            self.FNo.ht + self.Q / self.FNi.W, self.FNo.Pt * (1.0 - self.dP)
        )
        self.FNobld.copy(self.FNi)
        self.FNo.set_w(self.FNi.W * (1.0 - self.Wbldfrac))
        self.FNobld.set_w(self.FNi.W * (self.Wbldfrac))

    def dump(self):
        print(self.name1, "Duct", file=g.out)
        super().realPrint()

    def pretty(self):
        print(
            f"{'Duct':12s}{self.name1[:10]:12s}{('dP:' + str(self.dP))[:10]:12s}"
            f"{('Q:' + str(self.Q))[:10]:12s}",
            file=g.pretty,
        )
