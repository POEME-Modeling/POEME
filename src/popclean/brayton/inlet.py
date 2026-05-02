from popclean import Element, RealT, g

from .fn import FN


class Inlet(Element):
    def __init__(self, name):
        super().__init__(name, "Inlet")
        self.type = "Inlet"
        self.desc = "Inlet with simple recovery"

        # Variables
        self.rec = RealT(self, v=0.0, units="none", desc="Inlet recovery")

        # Fluid locations
        self.FNi = FN(self, io="in", desc="Incoming flow")
        self.FNo = FN(self, io="out", desc="Outgoing flow")

        self.initial_list()

    def calc(self):
        # pass incoming flow information
        self.FNo.copy(self.FNi)
        # keep enthalpy constant and apply a pressure drop
        self.FNo.set_hp(self.FNo.ht, self.FNo.Pt * (self.rec))

    def dump(self):
        print(self.name1, "Duct", file=g.out)
        super().real_print()

    def pretty(self):
        print(
            f"{'Inlet':12s}{self.name1[:10]:12s}{('rec:' + str(self.rec))[:10]:12s}",
            file=g.pretty,
        )
