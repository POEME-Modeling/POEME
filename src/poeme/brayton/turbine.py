from poeme import (
    BooleanT,
    Dependent,
    Element,
    Independent,
    ModelSession,
    RealT,
    Table2d,
)

from poeme.brayton import FN
from poeme.brayton import MP


class Turbine(Element):
    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Turbine", session=session)
        self.type = "Turbine"
        
        self.desc  = "Turbine - This element is a conventional map based adiabatic turbine.\n"
        self.desc += "The user inputs a design point efficiency.  At the sizing point, there\n"
        self.desc += "is a solver independent created that varies the turbine pressure ratio\n"
        self.desc += "to match the shaft power.  The users also supplies a turbine map.  The\n"
        self.desc += "map provides weight flow and efficiency as a function of pressure ratio\n"
        self.desc += "and corrected speed.  In sizind mode, the map is anchored to the user\n"
        self.desc += "supplied conditions.  In non-sizing mode, the turbine pressure map pressure\n"
        self.desc += "is varied to match the power and weight flow that the turbine can take in\n"
        self.desc += "according the the map.  There is a solver dependent that determins the error\n"
        self.desc += "the flow that the turbine is seeing and what the maps says it will allow\n\n"
        self.desc += "The turbine has two bleed port that will take cooling flow in, FNiBld1 (which\n"
        self.desc += "is added before the flow is expanded through the turbine) and FNiBld2 (which\n"
        self.desc += "is added after the turbine expansion.\n"
       

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
        self.FN41 = FN(self, desc="Station 41 after bleed 1", isPort=False)
        self.FN42 = FN(self, desc="Station 42 before bleed 2", isPort=False)
        self.FNi = FN(self, io="in", desc="Primary input flow")
        self.FNiBld1 = FN(self, io="in", desc="First bleed flow (before turbine)", isPort=False)
        self.FNiBld2 = FN(self, io="in", desc="Second bleed flow (after turbine)", isPort=False)
        self.FNideal = FN(self, desc="Ideal flow conditions", isPort=False)
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
            self.PRmapScale = (self.PRmapDes - 1.0) / (self.PR - 1.0)
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
