# from Table1d import Table1d
from popclean import (
    BooleanT,
    Element,
    Independent,
    RealT,
)

from .fn import FN


class Splitter(Element):
    def __init__(self, name):
        super().__init__(name, "Splitter")
        self.type = "Splitter"

        self.desc = "Divides an incoming flow into 2 streams"

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

        # design point turn off solver stuff
        if self.size == True:
            self.ind_BPR.active = False
        # off design turn on solver stuff
        else:
            self.ind_BPR.active = True

    def dump(self, output_file):
        output_file.write(f"{self.name1} Splitter\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        output_file.write(
            f"{'Splitter'[:10]:12s}{self.name1[:10]:12s}"
            f"{('BPR:' + str(self.BPR))[:10]:12s}\n",
        )
