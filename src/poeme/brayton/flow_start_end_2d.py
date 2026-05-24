from poeme import (
    BooleanT,
    Dependent,
    Element,
    ModelSession,
    RealT,
    StringT,
)

from .fn import FN


class FlowStartEnd2D(Element):
    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "FlowStart", session=session)
        self.type = "FlowStart"

        self.desc = "Start a Flow stream."

        # variables
        self.comp = StringT(self, desc="Composition of the stream.")
        self.Pt = RealT(self, units="lbm/in2", desc="Pressure")
        self.ht = RealT(self, units="Btu/lbm", desc="Specfic enthalpy")
        self.W = RealT(self, units="lbm/sec", desc="Weight flow")
        self.size = BooleanT(
            self, desc="Determine if the element is in design mode or not"
        )

        # fluid locations
        self.FNi = FN(self, io="out", desc="Incoming flow")
        self.FNo = FN(self, io="out", desc="Outgoing flow")

        # solver stuff
        self.dep_ht = Dependent(
            self,
            d1name="ht",
            d2name="FNi.ht",
            active=True,
            desc="Insure the enthalpy loop closes",
        )
        self.depPt = Dependent(
            self,
            d1name="Pt",
            d2name="FNi.Pt",
            active=True,
            desc="Insure the pressue loop closes",
        )
        self.depW = Dependent(
            self,
            d1name="W",
            d2name="FNi.W",
            active=False,
            desc="Insure the pressue loop closes",
        )

    def calc(self):

        # set the flow conditions
        self.FNo.comp = self.comp
        self.FNo.set_hp(self.ht, self.Pt)
        self.FNo.set_w(self.W)

    def dump(self, output_file):
        # dump output variables
        output_file.write(f"{self.name1} FlowStart\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        output_file.write(
            f"{'FSE2D'[:10]:12s}{self.name1[:10]:12s}{('W:' + str(self.W))[:10]:12s}"
            f"{('Pt:' + str(self.FNo.Pt))[:10]:12s}"
            f"{('Tt:' + str(self.FNo.Tt))[:10]:12s}\n"
        )
