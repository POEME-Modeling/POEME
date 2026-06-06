from poeme import Element, ModelSession, RealT, BooleanT, Table1d

from .fn import FN


class Inlet(Element):
    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Inlet", session=session)
        self.type = "Inlet"
        self.desc = "Inlet with simple recovery"

        # Variables
        self.Fram = RealT(self, units="lbf", desc="Ram drag")
        self.rec = RealT(self, v=1.0, units="none", desc="Inlet recovery")
        self.recoverySwitch = "Input"
        self.s_rec = RealT(self, v=1.0, units="none", desc="Scale factor on inlet recovery")

        self.RECtable = Table1d( self, desc="Table of total pressure recovery versus flight Mach number" )

        # Fluid locations
        self.FNi = FN(self, io="in", desc="Incoming flow")
        self.FNo = FN(self, io="out", desc="Outgoing flow")


        self.initial_list()

    def calc(self):
        # pass incoming flow information
        self.FNo.copy(self.FNi)

        # inlet ram drag
        self.Fram = self.FNi.V * self.FNi.W / 32.174

        # inlet recovery switch: input (default), Table, or Mil-Spec

        if self.recoverySwitch == "Table":
           # use table to get recovery
           self.rec = self.RECtable.calc(self.FNi.MN)

           # apply scale factor
           self.rec = self.rec * self.s_rec

        if self.recoverySwitch == "Mil-Spec":
           # Mil-Spec pressure recovery 
           # note: 0.523249 added to 935 term to prevent slight discontinuity at that point
           if self.FNi.MN.v <= 1.0:
              self.rec = 1.0
           elif self.FNi.MN.v <= 5.0:
              self.rec = 1.0 - 0.075*((self.FNi.MN.v - 1.)** 1.35)
           else:
              self.rec = 800.0/((self.FNi.MN.v**4.) + 935.523249)

           # apply scale factor
           self.rec = self.rec * self.s_rec


        # exit state: keep enthalpy constant and apply the pressure drop
        htOut = self.FNi.ht
        PtOut = self.FNi.Pt * self.rec
        self.FNo.set_hp( htOut, PtOut )

    def dump(self, output_file):
        output_file.write(f"{self.name1} Duct\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        output_file.write(
            f"{'Inlet':12s}{self.name1[:10]:12s}{('rec:' + str(self.rec))[:10]:12s}\n"
        )
