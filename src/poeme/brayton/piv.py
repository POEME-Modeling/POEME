from poeme import Element, ModelSession, RealT, StringVarT


class PIV(Element):
    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "PIV", session=session)
        self.type = "PIV"

        # variables
        self.P = RealT(self, units="none", desc="P")
        self.I = RealT(self, units="none", desc="I")
        self.D = RealT(self, units="none", desc="D")
        self.G = RealT(self, units="none", desc="G")
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
