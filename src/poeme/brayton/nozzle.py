from poeme import (
    BooleanT,
    Dependent,
    Element,
    ModelSession,
    RealT,
    StringVarT,
)
from poeme.brayton import FN


class Nozzle(Element):
    """Nozzle element for Brayton cycle exhaust expansion.

    A conventional nozzle calculation where the flow is expanded to input
    static pressure represented by the string reference PsExh. In sizing
    mode the element will determine the throat area to pass the flow given
    by the cycle. In fixed mode the nozzle will create a solver dependent
    that will measure the error between the actual nozzle area and the area
    that would be required to pass the flow that the nozzle is seeing during
    this current solver pass. The user can apply a Cfg value that will be
    applied to the ideal thrust calculated.

    Parameters
    ----------
    name : str
        Name of the nozzle element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    Cfg : RealT
        Coefficient of gross thrust.
    PsExh : StringVarT
        Exhaust pressure reference.
    Anoz : RealT
        Throat area (in²).
    Fg : RealT
        Gross thrust (lbf).
    FNi : FN
        Incoming flow port.
    FNo : FN
        Outgoing flow port (internal, not a port).
    dep_NA : Dependent
        Nozzle area error dependent.
    size : BooleanT
        Determines if nozzle is in sizing mode or not.
    """

    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Duct", session=session)
        self.type = "Nozzle"

        # element description
        self.desc = "Nozzle - This is a convential nozzle calculation. The flow is "
        "expanded to input static pressure represented by the string reference PsExh. "
        "In sizing mode the element will determine the throat area to pass the flow "
        "given by the cycle. In fixed mode the nozzle will create a solver dependent "
        "that will the error between the actual nozzle area and the area that would be "
        "required to pass the flow that nozzle is seeing during this current solver "
        "pass. The user can apply a Cfg value that will be applied to the ideal thrust"
        "calculated."

        # variables
        self.Cfg = RealT(self, v=1.0, units="non", desc="Coefficient of gross thrust")
        self.PsExh = StringVarT(self, desc="Exhaust pressure")
        self.Anoz = RealT(self, units="in2", desc="Throat area")
        self.Fg = RealT(self, units="blf", desc="Gross thrust")

        # flow connections
        self.FNi = FN(self, io="in", desc="Incoming flow")
        self.FNo = FN(self, io="out", desc="Outgoing flow", isPort=False)

        # dependents
        self.dep_NA = Dependent(
            self, d1name="Anoz", d2name="FNo.A", active=False, desc="Nozzle area error"
        )
        self.size = BooleanT(
            self, v=True, desc="determines if nozzle is in sizing mode or not"
        )

        self.initial_list()

    def precheck(self):
        """Activate or deactivate the area dependent based on sizing mode.

        In sizing mode, the area dependent is deactivated because the
        throat area is computed directly. In fixed mode, the dependent
        is activated so the solver can adjust the area to match flow.
        """

        # if we are in sizing mode there is no dependent
        if self.size.v == True:
            self.dep_NA.active = False
        # if we are not is sizinig mode than there is a dependent
        else:
            self.dep_NA.active = True

    def calc(self):
        """Calculate nozzle exit conditions and gross thrust.

        Checks for invalid pressure ratio, copies inlet flow to exit,
        sets exit to Mach 1 if downstream pressure allows, computes
        required throat area in sizing mode or adjusts area in fixed
        mode, and calculates gross thrust including momentum and
        pressure terms.

        The gross thrust is computed as::

            Fg = Cfg * (W * V / 32.17 + A * 144 * (Ps - Ps_exh))
        """

        if self.FNo.Pt < self.PsExh.get():
            self.session.errors += "\n" + self.name1 + "nozzle pressure ratio < 1"
        # copy the inlet flow to the exit
        self.FNo.copy(self.FNi)

        # set the exit conditions to Mach 1.
        self.FNo.size = True
        self.FNo.MN = 1.0
        self.FNo.set_tp(self.FNo.Tt, self.FNo.Pt)
        if self.FNo.Ps > self.PsExh.get():
            # if we are in sizing mode then set the area
            if self.size == True:
                self.Anoz = self.FNo.A
        else:
            self.FNo.Ps = self.PsExh.get()
            self.FNo.ps_calc()
            if self.size == True:
                self.Anoz = self.FNo.A

        # calculate gross thrust
        self.Fg = self.Cfg * (
            self.FNo.W * self.FNo.V / 32.17
            + self.FNo.A * 144.0 * (self.FNo.Ps - self.PsExh.get())
        )

    def dump(self, output_file):
        """Dump nozzle state to an output file.

        Parameters
        ----------
        output_file : file-like
            File object to write the nozzle state to.
        """
        output_file.write(f"{self.name1} Nozzle\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Print a formatted summary of the nozzle state.

        Parameters
        ----------
        output_file : file-like
            File object to write the pretty-printed output to.
        """
        output_file.write(
            f"{'Nozzle'[:10]:12s}{self.name1[:10]:12s}"
            f"{('Fg:' + str(self.Fg))[:10]:12s}\n"
        )
