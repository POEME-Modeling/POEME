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


class Turbine(Element):
    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Turbine", session=session)
        self.type = "Turbine"

        self.desc = (
            "Basic turbine.  This turbine read in maps of efficiency "
            + "and corrected weight flow as a function of corrected speed and "
            + "pressure ratio.  The element also has two bleed input ports."
        )

        # tables
        self.effTable = Table2d(
            self, desc="Table of efficiency versus corrected speed and pressure ratio"
        )
        self.WcTable = Table2d(
            self,
            units="lbm/sec",
            desc="Table of corrected weight flow versus corrected speed and pressure "
            "ratio",
        )

        # fluid locations
        self.FN41 = FN(self, desc="Station 41 after bleed 1")
        self.FN42 = FN(self, desc="Station 42 before bleed 2")
        self.FNi = FN(self, io="in", desc="Primary input flow")
        self.FNiBld1 = FN(self, io="in", desc="First bleed flow (before turbine)")
        self.FNiBld2 = FN(self, io="in", desc="Second bleed flow (after turbine)")
        self.FNideal = FN(self, desc="Ideal flow conditions")
        self.FNo = FN(self, io="out", desc="Primary outlet floe")

        # mechanical connections
        self.MP = MP(self, io="out", desc="Connection to shaft")

        # solver stuff
        self.ind_TPR = Independent(
            self,
            indname="PR",
            perturb=0.05,
            perturb_type="Relative",
            active=True,
            desc="Varies pressure ratio",
        )
        self.dep_TW = Dependent(
            self, d1name="Wc", d2name="WcMap", active=False, desc="Handles flow error"
        )

        # variables
        self.eff = RealT(self, units="none", desc="Efficiency")
        self.effDes = RealT(self, units="none", desc="Desired deisgn efficiency")
        self.effMap = RealT(self, units="none", desc="Efficiency read from map")
        self.effScale = RealT(self, units="none", desc="Scale factor on efficiency")
        self.Nc = RealT(self, units="RPM", desc="Corrected speed")
        self.NcMap = RealT(self, units="RPM", desc="Speed used to read map")
        self.NcMapDes = RealT(self, units="RPM", desc="Design speed map location")
        self.NcScale = RealT(self, units="none", desc="Scale factor on corrected speed")
        self.PR = RealT(self, units="none", desc="Pressure ratio")
        self.PRmap = RealT(self, units="none", desc="Pressure ratio read from map")
        self.PRmapDes = RealT(self, units="none", desc="Design pressure ratio on map")
        self.PRmapScale = RealT(self, units="none", desc="Scale on map pressure ratio")
        self.Wc = RealT(self, units="lbm/sec", desc="Correctef flow")
        self.WcDes = RealT(self, units="lbm/sec", desc="Design corrected flow")
        self.WcMap = RealT(self, units="lbm/sec", desc="Corrected flow read from map")
        self.WcScale = RealT(self, units="none", desc="scale factor of corrected flow")

        self.size = BooleanT(
            self, v=True, desc="determines if the turbine is in sizing mode or not"
        )
        self.initial_list()

    def calc(self):

        # add in the first bleed flow

        self.FN41.copy(self.FNi)
        self.FN41.add(self.FNiBld1)

        # calculate corrected conditions
        self.Nc = self.MP.N / (self.FNi.Tt) ** 0.5
        self.Wc = self.FNi.W * (self.FNi.Tt) ** 0.5 / self.FNi.Pt

        # if we are in sizing mode calculate scalars
        if self.size == True:
            self.NcScale = self.NcMapDes / self.Nc
            self.PRmapScale = (self.PRmapDes.v - 1.0) / (self.PR.v - 1.0)
            self.WcDes = self.Wc

        # set the map independents
        self.NcMap = self.NcScale * self.Nc
        self.PRmap = self.PRmapScale * (self.PR - 1.0) + 1.0

        # read the tables
        self.effMap = self.effTable.calc(self.NcMap, self.PRmap)
        self.WcMap = self.WcTable.calc(self.NcMap, self.PRmap)

        # if in sizing mode calculate scalars
        if self.size == True:
            self.effScale = self.effDes / self.effMap
            self.WcScale = self.WcDes / self.WcMap

        # scale the map results
        self.eff = self.effMap * self.effScale
        self.WcMap = self.WcMap * self.WcScale

        # calculate the expansions conditions
        self.FNideal.copy(self.FN41)
        self.FNideal.set_sp(self.FN41.s, self.FN41.Pt / self.PR)
        ht_out = self.FNi.ht + (self.FNideal.ht - self.FNi.ht) * self.eff
        self.FN42.copy(self.FN41)
        self.FN42.set_hp(ht_out, self.FNideal.Pt)

        # add in the second bleed flow
        self.FNo.copy(self.FN42)
        self.FNo.add(self.FNiBld2)

        # set the horse power on the mechanical port
        self.MP.set_hp(
            -1 * (self.FN42.ht - self.FN41.ht) * self.FN41.W * 3600.0 / 2545.0
        )

    def precheck(self):

        # if we are sizing mode dont add in the weight flow error
        if self.size.v == True:
            self.ind_TPR.active = True
            self.dep_TW.active = False

        # if we are not in sizing mode then add in weight flow error
        else:
            self.ind_TPR.active = True
            self.dep_TW.active = True

    def dump(self, output_file):
        output_file.write(f"{self.name1} Turbine\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        output_file.write(
            f"{'Turbine'[:10]:12s}{self.name1[:10]:12s}"
            f"{('PR:' + str(self.PR))[:10]:12s}{('eff:' + str(self.eff))[:10]:12s}"
            f"{('PRmap:' + str(self.PRmap))[:10]:12s}"
            f"{('NcMap:' + str(self.NcMap))[:10]:12s}\n"
        )
