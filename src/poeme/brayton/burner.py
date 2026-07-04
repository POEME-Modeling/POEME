from poeme import BooleanT, Element, ModelSession, RealT

from poeme.brayton import FN


class Burner(Element):
    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Burner", session=session)
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
        
        #element description
        self.desc = "Burner - This is a conventional buner.  It takes a flow and performs a\n"
        self.desc +="a combustion calculation.  The user can either input desired fuel to air\n"
        self.desc +="ratio or the desired fuel flow.  WFset is a true or false switch.  It is\n"
        self.desc +="set the true then the element runs to the input fuel flow.  It is set to\n"
        self.desc +="then it runs to the user input FAR.\n\n"
        self.desc +="If the user is running an equilbrium thermo package like cantera then the\n"
        self.desc +="input LHV actual represents the energy of the fuel including the heat of\n"
        self.desc +="formation.  In this case hydrocaron fuel would have a negative LHV value\n"
        self.desc +="simliar to what is seen with CEA.  In this case the input efficiecny must\n"
        self.desc +="be 1.0.\n\n"
        

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
