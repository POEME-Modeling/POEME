from popclean import (
    BooleanT,
    Element,
    Independent,
    ModelSession,
    RealT,
    StringT,
)

from .fn import FN


class FlowStart(Element):
    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "FlowStart", session=session)
        self.type = "FlowStart"

        self.desc = "Start a Flow stream."

        # variables
        self.comp = StringT(self, desc="Composition of the stream.")

        self.Pt = RealT(self, units="lbm/in2", desc="Pressure")
        self.Tt = RealT(self, units="R", desc="Temperature")
        self.W = RealT(self, units="lbm/sec", desc="Weight")
        self.size = BooleanT(
            self, v=True, desc="Determine if the element is in design mode or not"
        )

        # fluid locations
        self.FNo = FN(self, io="out", desc="Outgoing flow")

        # solver stuff
        self.ind_1 = Independent(
            self,
            indname="W",
            perturb=0.05,
            scale=100,
            perturb_type="Relative",
            active=False,
            desc="Vary mass flow",
        )

    def calc(self):

        # set the flow conditions
        self.FNo.comp = self.comp
        self.FNo.set_tp(self.Tt, self.Pt)
        self.FNo.set_w(self.W)

    def precheck(self):

        # design point turn off solver stuff
        if self.size == True:
            self.ind_1.active = False
        # off design turn on solver stuff
        else:
            self.ind_1.active = True

    def dump(self, output_file):
        # dump output variables
        output_file.write(f"{self.name1} FlowStart\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        output_file.write(
            f"Start {self.name1[:10]:15s} W:{str(self.W)[:4]:10s} "
            f"Tt:{str(self.W)[:4]:10s}  Pt:{str(self.Pt)[:4]:10s}\n"
        )
