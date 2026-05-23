from popclean import (
    Element,
    ModelSession,
    RealT,
)


class Perf(Element):
    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Shaft", session=session)
        self.type = "Perf"

        self.desc = "Simple overall performance calculation"

        # variables
        self.alt = RealT(self, units="ft", desc="Altitude")
        self.Fg = RealT(self, units="lbf", desc="Gross thrust")
        self.Fn = RealT(self, units="lbf", desc="Net thrust")
        self.MN = RealT(self, desc="Mach number")
        self.SFC = RealT(self, units="??", desc="Specifc fuel consumption")
        self.Wfuel = RealT(self, units="lbm/s", desc="Fuel flow")
        self.Fram = RealT(self, units="lbf", desc="Ram drag")

        self.initial_list()

    def calc(self):

        self.Fg = 0.0
        self.Wfuel = 0.0
        self.Fram = 0.0

        # loop through elements to find the nozzles and burners
        for e in self.session.elements:
            if e.type == "Nozzle":
                self.Fg = self.Fg + e.Fg
            if e.type == "Burner":
                self.Wfuel = self.Wfuel + e.Wfuel
            if e.type == "FlightConditionsSMJ":
                self.Fram = self.Fram + e.Fram
                self.alt = e.alt
                self.MN = e.MN

        # calculate SFC
        self.Fn = self.Fg - self.Fram
        self.SFC = self.Wfuel / self.Fn * 3600.0

    def dump(self, output_file):
        output_file.write(f"{self.name} Shaft\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        output_file.write(
            f"{'Performance'[:10]:12s}{self.name1[:10]:12s}"
            f"{('alt:' + str(self.alt))[:10]:12s}{('MN:' + str(self.MN))[:10]:12s}"
            f"{('Fn:' + str(self.Fn))[:10]:12s}{('SFC:' + str(self.SFC))[:10]:12s}"
            f"{('Fg:' + str(self.Fg))[:10]:12s}{('Fram:' + str(self.Fram))[:10]:12s}"
            f"{('Wfuel:' + str(self.Wfuel))[:10]:12s} \n"
        )
