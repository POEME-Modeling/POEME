from poeme import Element, ModelSession, RealT, StringVarT


class PIV(Element):
    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "PIV", session=session)
        self.type = "PIV"

        self.desc = (
            "PIV - This element is a PIV controller.  It senses a value from the\n"
        )
        self.desc += (
            "system, which is represented by the string value DPi, and adjustes the\n"
        )
        self.desc += (
            "contolled value in the system, represented by the string value DPo.\n"
        )
        self.desc += "This element is meant to run is a transient mode only.\n"
        self.desc += (
            "It does this by checking the model to find all the inlets, nozzles\n"
        )
        self.desc += (
            "and burners in the model.  From these elements it will calculcale\n"
        )
        self.desc += (
            "the overall values of total gross thrust, ram drag, net thrust, SFC\n"
        )
        self.desc += "and fuel flow.\n\n"

        # variables
        self.P = RealT(self, units="none", desc="P - scalar applied to current error")
        self.I = RealT(
            self,
            units="none",
            desc="I - scalar applied to curreny integral of the error",
        )
        self.D = RealT(
            self, units="none", desc="D - scalare applied to the derivative of the term"
        )
        self.G = RealT(
            self, units="none", desc="G - desired value of the controlled value"
        )
        self.elast = RealT(self, units="none", desc="Error term from last time step")
        self.e = RealT(self, units="none", desc="Error term")
        self.Inte = RealT(self, units="none", desc="Inte")
        self.DPi = StringVarT(self, desc="Sensed value")
        self.DPo = StringVarT(self, desc="Set value")
        self.timeLast = RealT(self, units="time", desc="Last time this g ran")
        self.type = "PIV"

    def calc(self):
        # if stepping in time them caclulate new conditions
        if self.session.solver.time.v > self.timeLast.v:
            self.e = self.G - self.DPi.get()
            self.DPo.set_val(
                self.DPo.get()
                + (
                    self.P * self.e
                    + self.D * (self.e - self.elast) / self.session.solver.dtime
                    + self.I * (self.Inte + self.e * self.session.solver.dtime)
                )
            )
            self.timeLast = self.session.solver.time

    def step(self):
        # step in time
        self.elast = self.e
        self.Inte = self.Inte + self.e.v * self.session.solver.dtime

    def dump(self, output_file):
        output_file.write(f"{self.name1} PIV\n")
        super().real_print(output_file)
