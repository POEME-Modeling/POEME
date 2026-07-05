from poeme import (
    BooleanT,
    Dependent,
    Element,
    ModelSession,
    RealT,
    StringT,
)
from .fn import FN


class FlowStartEnd2D(Element):
    """Flow start/end 2D element for closed-loop flow initialization.

    Starts a fluid stream given user input values of Pt, Tt, and W.
    Since there is a closed-loop element, there is an input node in
    addition to the exit node. The element has three dependents that
    are automatically created to ensure that the incoming Pt, Tt, and
    weight flow match the exit values.

    Parameters
    ----------
    name : str
        Name of the flow start/end 2D element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    comp : StringT
        Composition of the stream.
    Pt : RealT
        Total pressure (lbm/in²).
    ht : RealT
        Specific enthalpy (Btu/lbm).
    W : RealT
        Weight flow (lbm/sec).
    size : BooleanT
        Determines if the element is in design mode or not.
    FNi : FN
        Incoming flow port.
    FNo : FN
        Outgoing flow port.
    dep_ht : Dependent
        Dependent to ensure enthalpy loop closes.
    depPt : Dependent
        Dependent to ensure pressure loop closes.
    depW : Dependent
        Dependent to ensure weight flow loop closes.
    """

    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "FlowStart", session=session)
        self.type = "FlowStart"

        self.desc = "FlowStartEnd2d - this element starts a fluid stream given user "
        "input values of Pt, Tt, and W. If the static conditions are desired, the user "
        "can provide a Mach number of flow area.\nSince there is closed loop element, "
        "there is an input node in addition to the exit node. The element has three "
        "dependents that are automatically created to ensure the the incoming Pt, Tt, "
        "and weight flow match the exit values."

        # variables
        self.comp = StringT(self, desc="Composition of the stream.")
        self.Pt = RealT(self, units="lbm/in2", desc="Pressure")
        self.ht = RealT(self, units="Btu/lbm", desc="Specfic enthalpy")
        self.W = RealT(self, units="lbm/sec", desc="Weight flow")
        self.size = BooleanT(
            self, desc="Determine if the element is in design mode or not"
        )

        # fluid locations
        self.FNi = FN(self, io="out", desc="Incoming flow")
        self.FNo = FN(self, io="out", desc="Outgoing flow")

        # solver stuff
        self.dep_ht = Dependent(
            self,
            d1name="ht",
            d2name="FNi.ht",
            active=True,
            desc="Insure the enthalpy loop closes",
        )
        self.depPt = Dependent(
            self,
            d1name="Pt",
            d2name="FNi.Pt",
            active=True,
            desc="Insure the pressue loop closes",
        )
        self.depW = Dependent(
            self,
            d1name="W",
            d2name="FNi.W",
            active=False,
            desc="Insure the pressue loop closes",
        )

    def calc(self):
        """Set flow start/end 2D exit conditions and close loop.

        Copies composition to the outgoing flow, sets specific enthalpy,
        total pressure, and mass flow on the exit node. The incoming node
        is automatically updated by the three dependents (dep_ht, depPt,
        depW) to ensure the loop closes.
        """

        # set the flow conditions
        self.FNo.comp = self.comp
        self.FNo.set_hp(self.ht, self.Pt)
        self.FNo.set_w(self.W)

    def dump(self, output_file):
        """Dump flow start/end 2D state to an output file.

        Parameters
        ----------
        output_file : file-like
            File object to write the flow start/end 2D state to.
        """
        # dump output variables
        output_file.write(f"{self.name1} FlowStart\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Print a formatted summary of the flow start/end 2D state.

        Parameters
        ----------
        output_file : file-like
            File object to write the pretty-printed output to.
        """
        output_file.write(
            f"{'FSE2D'[:10]:12s}{self.name1[:10]:12s}{('W:' + str(self.W))[:10]:12s}"
            f"{('Pt:' + str(self.FNo.Pt))[:10]:12s}"
            f"{('Tt:' + str(self.FNo.Tt))[:10]:12s}\n"
        )
