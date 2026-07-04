from poeme import (
    Element,
    ModelSession,
    RealT,
)


class Perf(Element):
    """Performance element for Brayton cycle overall engine metrics.

    Determines the overall engine performance by checking the model to find
    all the inlets, nozzles and burners in the model. From these elements it
    will calculate the overall values of total gross thrust, ram drag, net
    thrust, SFC and fuel flow.

    Parameters
    ----------
    name : str
        Name of the performance element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    alt : RealT
        Altitude (ft).
    Fg : RealT
        Gross thrust (lbf).
    Fn : RealT
        Net thrust (lbf).
    MN : RealT
        Mach number.
    SFC : RealT
        Specific fuel consumption (lbm/(lbf·hr)).
    Wfuel : RealT
        Fuel flow (lbm/s).
    Fram : RealT
        Ram drag (lbf).
    """

    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Shaft", session=session)
        self.type = "Perf"

        self.desc = "Perf - This element determines the overall engine performance. It "
        "does this by checking the model to find all the inlets, nozzles and burners "
        "in the model.  From these elements it will calculcale the overall values of "
        "total gross thrust, ram drag, net thrust, SFC and fuel flow."

        # variables
        self.alt = RealT(self, units="ft", desc="Altitude")
        self.Fg = RealT(self, units="lbf", desc="Gross thrust")
        self.Fn = RealT(self, units="lbf", desc="Net thrust")
        self.MN = RealT(self, desc="Mach number")
        self.SFC = RealT(self, units="lbm/(lbf-hr)", desc="Specifc fuel consumption")
        self.Wfuel = RealT(self, units="lbm/s", desc="Fuel flow")
        self.Fram = RealT(self, units="lbf", desc="Ram drag")

        # self.FnTarget = RealT(self, units="lbf", desc="Net thrust target")
        # self.FnRatio = RealT(self, units="none", desc="Ratio of current Fn to max Fn")

        self.initial_list()

    def calc(self):
        """Calculate overall engine performance metrics.

        Loops through all elements in the session to find nozzles,
        burners, and inlets, accumulating gross thrust, fuel flow,
        and ram drag. Then computes net thrust and specific fuel
        consumption (SFC).

        The metrics are computed as::

            Fn = Fg - Fram
            SFC = Wfuel / Fn * 3600.0
        """

        self.Fg = 0.0
        self.Wfuel = 0.0
        self.Fram = 0.0

        # loop through elements to find the nozzles and burners
        for e in self.session.elements:
            if e.type == "Nozzle":
                self.Fg = self.Fg + e.Fg
            if e.type == "Burner":
                self.Wfuel = self.Wfuel + e.Wfuel
            if e.type == "Inlet":
                self.Fram = self.Fram + e.Fram
            if e.type == "FlightConditionsSMJ":
                self.alt = e.alt
                self.MN = e.MN

        # calculate SFC
        self.Fn = self.Fg - self.Fram
        self.SFC = self.Wfuel / self.Fn * 3600.0

    def dump(self, output_file):
        """Dump performance state to an output file.

        Parameters
        ----------
        output_file : file-like
            File object to write the performance state to.
        """
        output_file.write(f"{self.name} Shaft\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Print a formatted summary of the performance metrics.

        Parameters
        ----------
        output_file : file-like
            File object to write the pretty-printed output to.
        """
        output_file.write(
            f"{'Performance'[:10]:12s}{self.name1[:10]:12s}"
            f"{('alt:' + str(self.alt))[:10]:12s}{('MN:' + str(self.MN))[:10]:12s}"
            f"{('Fn:' + str(self.Fn))[:10]:12s}{('SFC:' + str(self.SFC))[:10]:12s}"
            f"{('Fg:' + str(self.Fg))[:10]:12s}{('Fram:' + str(self.Fram))[:10]:12s}"
            f"{('Wfuel:' + str(self.Wfuel))[:10]:12s} \n"
        )
