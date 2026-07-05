from poeme import BooleanT, Element, ModelSession, RealT

from .fn import FN


class Duct(Element):
    """Duct element for Brayton cycle pressure loss and bleed flow.

    A duct that applies a pressure loss to the flow. The pressure loss is
    input in terms of the fractional pressure loss versus the incoming
    pressure. The duct is designed to take in a bleed node and provide a
    secondary exit bleed node.

    Parameters
    ----------
    name : str
        Name of the duct element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    dPqP : RealT
        Non-dimensional (fractional) total pressure loss.
    dPqPdes : RealT
        Design non-dimensional total pressure loss.
    dPswitch : str
        Switch for pressure loss mode: "constant" or "varies".
    Q : RealT
        Heat added to the duct (BTU/s).
    Wbldfrac : RealT
        Bleed flow fraction.
    WcDes : RealT
        Corrected flow at design (lbm/s).
    FNi : FN
        Incoming flow port.
    FNo : FN
        Outgoing flow port.
    FNibld : FN
        Bleed in flow port.
    FNobld : FN
        Bleed out flow port.
    size : BooleanT
        Determines if the element is in design mode or not.
    """

    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Duct", session=session)
        self.type = "Duct"

        self.desc = "Duct - this element applies a pressure loss to the flow. The "
        "pressure loss is input in terms of the fractional pressue loss versus the "
        "incoming pressure. The duct is designed to take in bleed node and provide a "
        "secondary exit bleed node."

        # Variables
        self.dPqP = RealT(
            self,
            v=0.0,
            units="none",
            desc="Non-dimensional (fractional) total pressure loss",
        )
        self.dPqPdes = RealT(
            self, v=0.0, units="none", desc="Design non-dimensional total pressure loss"
        )
        self.dPswitch = "constant"
        self.Q = RealT(self, v=0.0, units="BTU/s", desc="Heat added to the duct")
        self.Wbldfrac = RealT(self, v=0.0, io="out", desc="Bleed flow fraction")
        self.WcDes = RealT(self, v=0.0, units="lbm/s", desc="Corrected flow at design")

        # Fluid locations
        self.FNi = FN(self, io="in", desc="Incoming flow")
        self.FNo = FN(self, io="out", desc="Outgoing flow")
        self.FNibld = FN(self, io="out", desc="Bleed in flow", isPort=False)
        self.FNobld = FN(self, io="out", desc="Bleed out flow")

        self.size = BooleanT(
            self, v=True, desc="Determine if the element is in design mode or not"
        )
        self.initial_list()

    def calc(self):
        """Calculate duct exit conditions and pressure loss.

        Passes incoming flow information to the exit, computes corrected
        flow, applies pressure loss (constant or parabolic with corrected
        flow), adds heat if specified, and sets the exit states for both
        the main exit and bleed exit flows.

        The corrected flow is computed as::

            Wc = W_in * (Tt_in / 518.67)^0.5 / (Pt_in / 14.696)

        In design mode, the corrected flow is saved as ``WcDes``. The
        pressure loss is applied as::

            dPqP = dPqPdes * (Wc / WcDes)^2   (if dPswitch == "varies")
            dPqP = dPqPdes                    (otherwise)

        Exit conditions are set with::

            Pt_exit = Pt_in * (1 - dPqP)
            ht_exit = ht_in + Q / W_in
        """
        # pass incoming flow information

        self.FNo.copy(self.FNi)
        self.FNi.add(self.FNibld)
        self.FNobld.copy(self.FNo)

        # corrected flow
        Wc = self.FNi.W * (self.FNi.Tt / 518.67) ** 0.5 / (self.FNi.Pt / 14.696)

        # save design value of corrected flow
        if self.size == True:
            self.WcDes = Wc

        # pressure loss is either constant or varies parabolically with Wc
        if self.dPswitch == "varies":
            self.dPqP = self.dPqPdes * (Wc / self.WcDes) ** 2.0
        else:
            self.dPqP = self.dPqPdes

        # exit total pressure
        PtExit = self.FNi.Pt * (1.0 - self.dPqP)

        # exit specific enthalpy, Q is applied to the entire flow
        htExit = self.FNi.ht + self.Q / self.FNi.W

        # set the exit states; flow and ht, Pt
        self.FNo.set_w(self.FNi.W * (1.0 - self.Wbldfrac))
        self.FNobld.set_w(self.FNi.W * (self.Wbldfrac))

        self.FNo.set_hp(htExit, PtExit)
        self.FNobld.set_hp(htExit, PtExit)

    def precheck(self):
        """Check bleed flow fraction and deactivate port if negligible.

        If the bleed flow fraction is near zero, sets the bleed out
        port's ``isPort`` attribute to False so it is ignored by the solver.
        """

        if self.Wbldfrac < 0.0000001:
            self.FNobld.isPort = False

    def dump(self, output_file):
        """Dump duct state to an output file.

        Parameters
        ----------
        output_file : file-like
            File object to write the duct state to.
        """
        output_file.write(f"{self.name1} Duct\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Print a formatted summary of the duct state.

        Parameters
        ----------
        output_file : file-like
            File object to write the pretty-printed output to.
        """
        output_file.write(
            f"{'Duct':12s}{self.name1[:10]:12s}{('dP:' + str(self.dPqP))[:10]:12s}"
            f"{('Q:' + str(self.Q))[:10]:12s}\n"
        )
