from poeme import Element, ModelSession, RealT, Table1d
from .fn import FN


class Inlet(Element):
    """Inlet element for Brayton cycle ram compression and pressure recovery.

    Applies an inlet recovery to the flow. The recovery value is the amount
    of total pressure left after exiting the inlet. A value of 1.0 indicates
    no loss at all. Supports input tables and Mil-Spec pressure recovery curves.

    Parameters
    ----------
    name : str
        Name of the inlet element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    Fram : RealT
        Ram drag (lbf).
    rec : RealT
        Inlet recovery (fraction of total pressure retained).
    recoverySwitch : str
        Recovery mode: "Input", "Table", or "Mil-Spec".
    s_rec : RealT
        Scale factor on inlet recovery.
    RECtable : Table1d
        Table of total pressure recovery versus flight Mach number.
    FNi : FN
        Incoming flow port.
    FNo : FN
        Outgoing flow port.
    """

    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Inlet", session=session)
        self.type = "Inlet"
        self.desc = "Inlet - this element applies an inlet recovery to the flow. The "
        "recovery value is the ammount of total pressure left after exiting the inlet. "
        "A value of 1.0 indicates no loss at all."

        # Variables
        self.Fram = RealT(self, units="lbf", desc="Ram drag")
        self.rec = RealT(self, v=1.0, units="none", desc="Inlet recovery")
        self.recoverySwitch = "Input"
        self.s_rec = RealT(
            self, v=1.0, units="none", desc="Scale factor on inlet recovery"
        )

        self.RECtable = Table1d(
            self, desc="Table of total pressure recovery versus flight Mach number"
        )

        # Fluid locations
        self.FNi = FN(self, io="in", desc="Incoming flow")
        self.FNo = FN(self, io="out", desc="Outgoing flow")

        self.initial_list()

    def calc(self):
        """Calculate inlet exit conditions and ram drag.

        Passes incoming flow information to the exit, computes ram drag,
        determines pressure recovery from input table or Mil-Spec curve,
        and sets the exit state with constant enthalpy and recovered
        total pressure.

        The ram drag is computed as::

            Fram = V_in * W_in / 32.174

        For Mil-Spec recovery (MN > 1)::

            rec = 1 - 0.075 * (MN - 1)^1.35
            rec = 800 / (MN^4 + 935.52)   (for MN > 5)

        Exit conditions are set with::

            ht_out = ht_in
            Pt_out = Pt_in * rec
        """
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
            # note: 0.523249 added to 935 term to prevent slight discontinuity there
            if self.FNi.MN.v <= 1.0:
                self.rec = 1.0
            elif self.FNi.MN.v <= 5.0:
                self.rec = 1.0 - 0.075 * ((self.FNi.MN.v - 1.0) ** 1.35)
            else:
                self.rec = 800.0 / ((self.FNi.MN.v**4.0) + 935.523249)

            # apply scale factor
            self.rec = self.rec * self.s_rec

        # exit state: keep enthalpy constant and apply the pressure drop
        htOut = self.FNi.ht
        PtOut = self.FNi.Pt * self.rec
        self.FNo.set_hp(htOut, PtOut)

    def dump(self, output_file):
        """Dump inlet state to an output file.

        Parameters
        ----------
        output_file : file-like
            File object to write the inlet state to.
        """
        output_file.write(f"{self.name1} Duct\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Print a formatted summary of the inlet state.

        Parameters
        ----------
        output_file : file-like
            File object to write the pretty-printed output to.
        """
        output_file.write(
            f"{'Inlet':12s}{self.name1[:10]:12s}{('rec:' + str(self.rec))[:10]:12s}\n"
        )
