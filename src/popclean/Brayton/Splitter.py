from Element import Element
from RealT import RealT
from BooleanT import BooleanT
from ComplexT import ComplexT
from StringT import StringT
from FN import FN
from Dependent import Dependent
from Independent import Independent

# from Table1d import Table1d
import g


class Splitter(Element):

    def __init__(spl, name):
        super().__init__(name, "Splitter")
        spl.type = "Splitter"

        spl.desc = "Divides an incoming flow into 2 streams"

        # Variables
        spl.BPR = RealT(spl, v=1.0, units="none", desc="Bypass ratio, W2/W1")

        # Fluid locations
        spl.FNi = FN(spl, io="in", desc="Incoming flow")
        spl.FNo1 = FN(spl, io="out", desc="Outgoing flow, stream 1")
        spl.FNo2 = FN(spl, io="out", desc="Outgoing flow, stream 2")
        spl.size = BooleanT(
            spl, v=True, desc="Determine if the element is in design mode or not"
        )

        # solver stuff
        spl.ind_BPR = Independent(
            spl,
            indname="BPR",
            perturb=0.05,
            scale=100,
            perturb_type="Relative",
            active=False,
            desc="Bypass Ratio",
        )

        spl.initialList()

    def calc(spl):
        # pass incoming flow information
        spl.FNo1.copy(spl.FNi)
        spl.FNo2.copy(spl.FNi)

        # keep Pt and Tt constant, only massflow changes
        spl.FNo1.setW(spl.FNi.W * 1.0 / (spl.BPR + 1.0))
        spl.FNo2.setW(spl.FNi.W * spl.BPR / (spl.BPR + 1.0))

        # spl.FNo.set_hP( spl.FNo.ht + spl.Q/spl.FNi.W, spl.FNo.Pt*( 1.- spl.dP ) )
        # spl.FNo1.set_hP( spl.FNi.ht, spl.FNi.Pt )
        # spl.FNo2.set_hP( spl.FNi.ht, spl.FNi.Pt )

    def precheck(spl):

        # design point turn off solver stuff
        if spl.size == True:
            spl.ind_BPR.active = False
        # off design turn on solver stuff
        else:
            spl.ind_BPR.active = True

    def dump(spl):
        print(spl.name1, "Splitter", file=g.out)
        super().realPrint()

    def pretty(s):
        print(
            f"{"Splitter"[:10]:12s}{s.name1[:10]:12s}{("BPR:"+str(s.BPR))[:10]:12s}",
            file=g.pretty,
        )
