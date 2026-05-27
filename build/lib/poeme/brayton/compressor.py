from poeme import (
    BooleanT,
    Dependent,
    Element,
    Independent,
    ModelSession,
    RealT,
    Table2d,
)

from .fn import FN
from .mp import MP


class Compressor(Element):
    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Compressor", session=session)
        self.type = "Compressor"

        self.desc = (
            "Basic compressor.  This compressor reads in maps of effeciency, "
            + "correct flow and pressure ratio as a function of R-line and correctec "
            + "speed.  The element enables two bleed flows to be taken off."
        )

        # tables
        self.effTable = Table2d(
            self, desc="Table of efficiency versus corrected speed and Rline"
        )
        self.PRtable = Table2d(
            self, desc="Table of pressure ratio versus corrected speed and flow"
        )
        self.WcTable = Table2d(
            self,
            units="lbm/sec",
            desc="Table of corrected flow versus corrected speed and flow",
        )

        # fluid locations/ports
        self.FNi = FN(self, io="in", desc="Incoming fluid flow")
        self.FNideal = FN(self, desc="Ideal exit conditions")
        self.FNo = FN(self, io="out", desc="Outgoing fluid flow")
        self.FNoBld1 = FN(self, io="out", desc="Bleed flow 1")
        self.FNoBld2 = FN(self, io="out", desc="Bleed flow 2")

        # mechanical connections
        self.MP = MP(self, io="out", desc="Mechanicl port connectio")

        # solver stuff
        self.ind_CR = Independent(
            self,
            indname="Rline",
            perturb=0.05,
            scale=100,
            perturb_type="Relative",
            active=False,
            desc="Varies R-line",
        )
        self.dep_CW = Dependent(
            self,
            d1name="Wc",
            d2name="WcMap",
            active=False,
            desc="Handles weight flow error",
        )

        # variables
        self.eff = RealT(self, units="none", desc="Efficiency")
        self.effDes = RealT(self, units="none", desc="Design efficiency")
        self.effMap = RealT(self, units="none", desc="Efficiency read from table")
        self.effScale = RealT(self, units="none", desc="Scalar on efficiency map")
        self.hfract1 = RealT(
            self,
            units="BTU/lbm",
            desc="Enthalpy fraction that determines how down the compressor the bleed "
            "is taken",
        )
        self.hfract2 = RealT(
            self,
            units="BTU/lbm",
            desc="Enthalpy fraction that determines how down the compressor the bleed "
            "is taken",
        )
        self.Nc = RealT(self, units="RPM/R**.5", desc="Corrected speed")
        self.NcMap = RealT(
            self, units="RPM/R**.5", desc="Corrected speed used to read the map"
        )
        self.NcMapDes = RealT(
            self, units="RPM/R**.5", desc="Design point corrected speed"
        )
        self.NcScale = RealT(self, units="none", desc="Scalar on corrected speed")
        self.PR = RealT(self, units="none", desc="Pressure ratio")
        self.PRdes = RealT(self, units="none", desc="Design pressure ratio")
        self.PRmap = RealT(self, units="none", desc="Pressure ratio read from table")
        self.PRscale = RealT(self, units="none", desc="Scalar on pressure ratio map")
        self.Rline = RealT(self, units="none", desc="Current R-line")
        self.RlineDes = RealT(self, units="none", desc="Design point R-line")
        self.SMN = RealT(
            self, units="none", desc="stall margin based on corrected speed"
        )
        self.Wc = RealT(self, units="lbm/sec", desc="Corrected flow")
        self.WcDes = RealT(self, units="lbm/sec", desc="Design corrected flow")
        self.WcMap = RealT(self, units="lbm/sec", desc="Map corrected flow")
        self.WcScale = RealT(self, units="none", desc="Scalar on corrected flow")
        self.Wfrac1 = RealT(
            self, units="none", desc="Weight flow fraction for bleed flow 1"
        )
        self.Wfrac2 = RealT(
            self, units="none", desc="Weight flow fraction for bleed flow 2"
        )

        self.size = BooleanT(
            self, v=True, desc="Determine if the element is in design mode or not"
        )
        self.initial_list()

    def calc(self):

        # copy incoming flow to other ports
        self.FNo.copy(self.FNi)
        self.FNoBld1.copy(self.FNi)
        self.FNoBld1.set_w(0.0)
        self.FNoBld2.copy(self.FNi)
        self.FNoBld2.set_w(0.0)
        self.FNideal.copy(self.FNi)

        # calculate corrected speed amd corrected flow
        self.Nc = self.MP.N / (self.FNi.Tt) ** 0.5
        self.Wc = self.FNi.W * (self.FNi.Tt) ** 0.5 / self.FNi.Pt
        self.Wc = self.FNi.W * (self.FNi.Tt) ** 0.5 / self.FNi.Pt

        # if we are in design mode set the conditions
        if self.size == True:
            self.NcScale = self.NcMapDes / self.Nc
            self.WcDes = self.Wc
            self.Rline = self.RlineDes

        # scale the corrected speed
        self.NcMap = self.NcScale * self.Nc

        # read the maps
        self.effMap = self.effTable.calc(self.NcMap, self.Rline)
        self.PRmap = self.PRtable.calc(self.NcMap, self.Rline)
        self.WcMap = self.WcTable.calc(self.NcMap, self.Rline)

        # if in desing mode determine the scale factors
        if self.size == True:
            self.effScale = self.effDes / self.effMap
            self.PRscale = (self.PRdes-1. )/( self.PRmap-1. )
            self.WcScale = self.WcDes / self.WcMap

        # scale the map values
        self.eff = self.effMap * self.effScale
        self.PR = ( self.PRmap-1.) * self.PRscale + 1.
        self.WcMap = self.WcScale * self.WcMap
        self.SMN = (self.PRmap - self.PRtable.calc(self.NcMap, self.Rline)) / self.PRmap

        # determine the ideal conditions
        self.FNideal.set_sp(self.FNi.s, self.PR * self.FNi.Pt)

        # determine the actual exit conditions
        ht_out = self.FNi.ht + (self.FNideal.ht - self.FNi.ht) / self.eff
        self.FNo.set_hp(ht_out, self.PR * self.FNi.Pt)

        # set the bleed exit conditions
        if self.Wfrac1 > 0.0:
            self.FNoBld1.set_w(self.Wfrac1 * self.FNi.W)
            self.FNoBld1.set_hp(
                self.FNi.ht + self.hfract1 * (self.FNo.ht - self.FNi.ht),
                self.hfract1 * (self.FNo.Pt - self.FNi.Pt),
            )
        if self.Wfrac2 > 0.0:
            self.FNoBld2.set_w(self.Wfrac2 * self.FNi.W)
            self.FNoBld2.set_hp(
                self.FNi.ht + self.hfract2 * (self.FNo.ht - self.FNi.ht),
                self.hfract2 * (self.FNo.Pt - self.FNi.Pt),
            )

        self.FNo.set_w(self.FNo.W - self.FNoBld1.W - self.FNoBld2.W)

        # set the exit conditions
        self.MP.set_hp(
            -1.0
            * (
                (self.FNo.ht - self.FNi.ht) * self.FNo.W * 3600.0 / 2545.0
                + (self.FNoBld1.ht - self.FNi.ht) * self.FNoBld1.W * 3600.0 / 2545.0
                + (self.FNoBld2.ht - self.FNi.ht) * self.FNoBld2.W * 3600.0 / 2545.0
            )
        )

    def precheck(self):

        # design point turn off solver stuff
        if self.size == True:
            self.ind_CR.active = False
            self.dep_CW.active = False
        # off design turn on solver stuff
        else:
            self.ind_CR.active = True
            self.dep_CW.active = True

    def dump(self, output_file):
        # dump output variables
        output_file.write(f"{self.name1} Compressor\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        output_file.write(
            f"{'Compressor'[:10]:12s}{self.name1[:10]:12s}"
            f"{('PR:' + str(self.PR))[:10]:12s}"
            f"{('eff:' + str(self.eff))[:10]:12s}"
            f"{('Rline:' + str(self.Rline))[:10]:12s}"
            f"{('NcMap:' + str(self.NcMap))[:10]:12s}\n"
        )
