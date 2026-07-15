from poeme import BooleanT, Element, ModelSession, RealT

from .fn import FN


class Burner(Element):
    """Burner element for Brayton cycle combustion calculations.

    A conventional burner that adds fuel to an incoming flow and performs
    a combustion calculation. The user can either input the desired fuel-to-air
    ratio (FAR) or the desired fuel flow rate. A switch (WFset) determines which
    mode is active. If running with an equilibrium thermo package like Cantera,
    the input LHV represents the energy of the fuel including the heat of formation;
    in that case hydrocarbon fuel would have a negative LHV value similar to what
    is seen with CEA, and the input efficiency must be 1.0.

    Parameters
    ----------
    name : str
        Name of the burner element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    dP : RealT
        Pressure loss (fractional).
    eff : RealT
        Burner efficiency.
    FAR : RealT
        Fuel-to-air ratio.
    LHV : RealT
        Fuel enthalpy (BTU/lbm).
    WFset : BooleanT
        If True the user is setting fuel flow.
    Tout : RealT
        Exit temperature (R).
    Wfuel : RealT
        Fuel flow (lbm/s).
    FNi : FN
        Incoming flow port.
    FNo : FN
        Outgoing flow port.
    """

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
        self.LHV = RealT(self, units="BTU/lbm", desc="Fuel LHV")
        self.hFuel = RealT(self, units="BTU/lbm", desc="Fuel enthalpy")
        self.WFset = BooleanT(
            self, v=False, desc="If true the user is setting fuel flow"
        )
        self.Tout = RealT(self, units="R", desc="Exit temperature")
        self.Wfuel = RealT(self, units="lbm/s", desc="Fuel flow")

        # element description
        self.desc = "Burner - This is a conventional buner. It takes a flow and "
        "performs a combustion calculation. The user can either input desired fuel to "
        "air ratio or the desired fuel flow. WFset is a true or false switch. It is "
        "set the true then the element runs to the input fuel flow. It is set to then "
        "it runs to the user input FAR.\nIf the user is running an equilbrium thermo "
        "package like cantera then the input LHV actual represents the energy of the "
        "fuel including the heat of formation. In this case hydrocaron fuel would have "
        "a negative LHV value simliar to what is seen with CEA. In this case the input "
        "efficiecny must be 1.0."

        self.initial_list()

    def calc(self):
        """Calculate burner exit conditions and fuel-to-air ratio.

        Passes incoming flow information to the exit, determines whether
        to run to input fuel flow or FAR based on WFset, computes the exit
        enthalpy and pressure, and sets the exit state.

        The fuel flow is computed as::

            Wfuel = W * FAR   (if WFset is False)
            FAR = Wfuel / W   (if WFset is True)

        The exit enthalpy is computed as::

            htout = (ht_in * W_in + Wfuel * LHV) / W_out

        and the exit state is set with::

            FNo.set_hp(htout, Pt_in * (1 - dP))
        """

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
        htout = (
            self.FNi.ht * self.FNi.W + self.Wfuel * self.LHV + self.Wfuel * self.hFuel
        ) / self.FNo.W
        self.FNo.set_hp(htout, self.FNo.Pt * (1 - self.dP))

    def dump(self, output_file):
        """Dump burner state to an output file.

        Parameters
        ----------
        output_file : file-like
            File object to write the burner state to.
        """
        output_file.write(f"{self.name1} Burner\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Print a formatted summary of the burner state.

        Parameters
        ----------
        output_file : file-like
            File object to write the pretty-printed output to.
        """
        output_file.write(
            f"{'Burner'[:10]:12s}{self.name1[:10]:12s}"
            f"{('FAR:' + str(self.FAR))[:10]:12s}"
            f"{('Tout:' + str(self.Tout))[:10]:12s}"
            f"{('Wfuel:' + str(self.Wfuel))[:10]:12s}"
            f"{('dP:' + str(self.dP))[:10]:12s}\n"
        )
