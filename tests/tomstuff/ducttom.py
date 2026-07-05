from poeme import BooleanT, Element, ModelSession, RealT
from poeme.brayton import FN


class DuctTom(Element):
    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Duct", session=session)
        self.type = "Duct"

        self.desc = "Duct - this element applies a pressure loss to the flow. The "
        "pressure loss is input in terms of the fractional pressure loss versus the "
        "incoming pressure. The duct is designed to take in bleed node and provide a "
        "secondary exit bleed node."

        # Variables
        self.dPqP = RealT(
            self,
            v=0.0,
            units="none",
            desc="Non-dimensional (fractional) total pressure loss",
        )
        self.dPqPdes = RealT(
            self, v=0.0, units="none", desc="Design non-dimensional total pressure loss"
        )
        self.dPswitch = "constant"
        self.Q = RealT(self, v=0.0, units="BTU/s", desc="Heat added to the duct")
        self.Wbldfrac = RealT(self, v=0.0, io="out", desc="Bleed flow fraction")
        self.WcDes = RealT(self, v=0.0, units="lbm/s", desc="Corrected flow at design")

        # Fluid locations
        self.FNi = FN(self, io="in", desc="Incoming flow")
        self.FNo = FN(self, io="out", desc="Outgoing flow")
        self.FNibld = FN(self, io="out", desc="Bleed in flow", isPort=False)
        self.FNobld = FN(self, io="out", desc="Bleed out flow")

        self.size = BooleanT(
            self, v=True, desc="Determine if the element is in design mode or not"
        )
        self.initial_list()

    def calc(self):
        # pass incoming flow information

        self.FNo.copy(self.FNi)
        self.FNi.add(self.FNibld)
        self.FNobld.copy(self.FNo)

        # corrected flow
        Wc = self.FNi.W * (self.FNi.Tt / 518.67) ** 0.5 / (self.FNi.Pt / 14.696)

        # save design value of corrected flow
        if self.size == True:
            self.WcDes = Wc

        # pressure loss is either constant or varies parabolically with Wc
        if self.dPswitch == "varies":
            self.dPqP = self.dPqPdes * (Wc / self.WcDes) ** 2.0
        else:
            self.dPqP = self.dPqPdes

        # exit total pressure
        PtExit = self.FNi.Pt * (1.0 - self.dPqP)

        # exit specific enthalpy, Q is applied to the entire flow
        htExit = self.FNi.ht + self.Q / self.FNi.W

        # set the exit states; flow and ht, Pt
        self.FNo.set_w(self.FNi.W * (1.0 - self.Wbldfrac))
        self.FNobld.set_w(self.FNi.W * (self.Wbldfrac))

        self.FNo.set_hp(htExit, PtExit)
        self.FNobld.set_hp(htExit, PtExit)

    def precheck(self):

        if self.Wbldfrac < 0.0000001:
            self.FNobld.isPort = False

    def dump(self, output_file):
        output_file.write(f"{self.name1} Duct\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        output_file.write(
            f"{'Duct':12s}{self.name1[:10]:12s}{('dP:' + str(self.dPqP))[:10]:12s}"
            f"{('Q:' + str(self.Q))[:10]:12s}\n"
        )
