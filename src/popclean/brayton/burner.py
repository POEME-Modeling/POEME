from popclean import BooleanT, Element, RealT

from .fn import FN


class Burner(Element):
    def __init__(self, name):
        super().__init__(name, "Burner")
        self.type = "Burner"

        self.desc = "Adds fuel to fuel and burns it."

        # fluid locations/ports
        self.FNi = FN(self, io="in", desc="Incoming flow")
        self.FNo = FN(self, io="out", desc="Outgoing flow")

        # Variables
        self.dP = RealT(self, units="none", desc="Pressure loss (fractional)")
        self.eff = RealT(self, v=1.0, units="none", desc="Burner efficiency")
        self.FAR = RealT(self, units="none", desc="Fuel to air ratio")
        self.LHV = RealT(self, units="BTU/lbm", desc="Fuel enthalpy")
        self.WFset = BooleanT(
            self, v=False, desc="If true the user is setting fuel flow"
        )
        self.Tout = RealT(self, units="R", desc="Exit temperature")
        self.Wfuel = RealT(self, units="lbm/s", desc="Fuel flow")

        self.initial_list()

    def calc(self):

        # pass incoming flow information along
        self.FNo.copy(self.FNi)

        # determine if we are running to input fuel flow or FAR
        if self.WFset == False:
            self.Wfuel = self.FNi.W * self.FAR
        else:
            self.FAR = self.Wfuel / self.FNi.W

        # `set the exit conditions
        self.FNo.set_w(self.FNi.W + self.Wfuel)
        self.FNo.FAR = self.FAR
        htout = (self.FNi.ht * self.FNi.W + self.Wfuel * self.LHV) / self.FNo.W
        self.FNo.set_hp(htout, self.FNo.Pt * (1 - self.dP))

    def dump(self, output_file):
        output_file.write(f"{self.name1} Burner\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        output_file.write(
            f"{'Burner'[:10]:12s}{self.name1[:10]:12s}"
            f"{('FAR:' + str(self.FAR))[:10]:12s}"
            f"{('Tout:' + str(self.Tout))[:10]:12s}"
            f"{('Wfuel:' + str(self.Wfuel))[:10]:12s}"
            f"{('dP:' + str(self.dP))[:10]:12s}\n"
        )
