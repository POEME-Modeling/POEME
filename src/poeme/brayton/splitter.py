from poeme import (
    BooleanT,
    Element,
    Independent,
    ModelSession,
    RealT,
)
from .fn import FN


class Splitter(Element):
    """Splitter element for Brayton cycle flow division.

    Splits a stream into two exit streams. In non-sizing mode, the bypass
    ratio becomes a value controlled by the solver.

    Parameters
    ----------
    name : str
        Name of the splitter element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    BPR : RealT
        Bypass ratio, W2/W1 (dimensionless).
    FNi : FN
        Incoming flow port.
    FNo1 : FN
        Outgoing flow, stream 1 port.
    FNo2 : FN
        Outgoing flow, stream 2 port.
    size : BooleanT
        Determines if the element is in design mode or not.
    ind_BPR : Independent
        Independent variable for bypass ratio variation.
    """

    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Splitter", session=session)
        self.type = "Splitter"

        # desciption
        self.desc = "Splitter - this element splits a stream into two exit streams. In "
        "non-sizing mode, the bypass ratio becomes a value controlled by the solver."

        # Variables
        self.BPR = RealT(self, v=1.0, units="none", desc="Bypass ratio, W2/W1")

        # Fluid locations
        self.FNi = FN(self, io="in", desc="Incoming flow")
        self.FNo1 = FN(self, io="out", desc="Outgoing flow, stream 1")
        self.FNo2 = FN(self, io="out", desc="Outgoing flow, stream 2")
        self.size = BooleanT(
            self, v=True, desc="Determine if the element is in design mode or not"
        )

        # solver stuff
        self.ind_BPR = Independent(
            self,
            indname="BPR",
            perturb=0.05,
            scale=100,
            perturb_type="Relative",
            active=False,
            desc="Bypass Ratio",
        )

        self.initial_list()

    def calc(self):
        """Calculate splitter exit flows based on bypass ratio.

        Copies incoming flow to both exit streams, then divides mass
        flow according to the bypass ratio (BPR). Stream 1 receives
        W / (BPR + 1) and stream 2 receives W * BPR / (BPR + 1).
        Total pressure and temperature remain constant across the split.
        """
        # pass incoming flow information
        self.FNo1.copy(self.FNi)
        self.FNo2.copy(self.FNi)

        # keep Pt and Tt constant, only massflow changes
        self.FNo1.set_w(self.FNi.W * 1.0 / (self.BPR + 1.0))
        self.FNo2.set_w(self.FNi.W * self.BPR / (self.BPR + 1.0))

        # self.FNo.set_hp( self.FNo.ht + self.Q/self.FNi.W, self.FNo.Pt*( 1.- self.dP))
        # self.FNo1.set_hp( self.FNi.ht, self.FNi.Pt )
        # self.FNo2.set_hp( self.FNi.ht, self.FNi.Pt )

    def precheck(self):
        """Activate or deactivate bypass ratio independent based on sizing mode.

        In sizing mode, the BPR independent is deactivated because the
        bypass ratio is fixed. In fixed mode, it is activated so the
        solver can adjust the BPR.
        """

        # design point turn off solver stuff
        if self.size == True:
            self.ind_BPR.active = False
        # off design turn on solver stuff
        else:
            self.ind_BPR.active = True

    def dump(self, output_file):
        """Dump splitter state to an output file.

        Parameters
        ----------
        output_file : file-like
            File object to write the splitter state to.
        """
        output_file.write(f"{self.name1} Splitter\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Print a formatted summary of the splitter state.

        Parameters
        ----------
        output_file : file-like
            File object to write the pretty-printed output to.
        """
        output_file.write(
            f"{'Splitter'[:10]:12s}{self.name1[:10]:12s}"
            f"{('BPR:' + str(self.BPR))[:10]:12s}\n",
        )
