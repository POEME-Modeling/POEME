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
            "Basic compressor.  This compressor reads in maps of efficiency, "
            + "corrected flow and pressure ratio as a function of R-line (index) "
            + "and corrected speed.  This element allows two bleed flows."
        )

        # tables
        self.effTable = Table2d(
            self, desc="Table of efficiency versus corrected speed and R-line"
        )
        self.PRtable = Table2d(
            self, desc="Table of pressure ratio versus corrected speed and R-line"
        )
        self.WcTable = Table2d(
            self,
            units="lbm/sec",
            desc="Table of corrected flow versus corrected speed and R-line",
        )

        # fluid locations/ports
        self.FNi = FN(self, io="in", desc="Incoming fluid flow" )
        self.FNideal = FN(self, desc="Ideal exit conditions",isPort=False)
        self.FNo = FN(self, io="out", desc="Outgoing fluid flow")
        self.FNoBld1 = FN(self, io="out", desc="Bleed flow 1")
        self.FNoBld2 = FN(self, io="out", desc="Bleed flow 2")

        # mechanical connections
        self.MP = MP(self, io="out", desc="Mechanical port connection")

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
            desc="Weight flow error between incoming fluid node and map value",
        )

        # variables
        self.eff = RealT(self, units="none", desc="Adiabatic efficiency")
        self.effDes = RealT(self, units="none", desc="Design adiabatic efficiency")
        self.effMap = RealT(self, units="none", desc="Efficiency read from the map table")
        self.effScale = RealT(self, units="none", desc="Scalar on the efficiency map")
        self.hfract1 = RealT(self, units="BTU/lbm", desc="Enthalpy fraction (0=entrance, 1=exit) for the location of bleed flow 1")
        self.hfract2 = RealT(self, units="BTU/lbm", desc="Enthalpy fraction (0=entrance, 1=exit) for the location of bleed flow 2")
        self.Nc = RealT(self, units="RPM", desc="Corrected speed")
        self.NcMap = RealT(self, units="RPM", desc="Corrected speed used to read the map")
        self.NcMapDes = RealT(self, units="RPM", desc="Design point map corrected speed")
        self.NcScale = RealT(self, units="none", desc="Scalar on corrected speed")
        self.PR = RealT(self, units="none", desc="Pressure ratio")
        self.PRdes = RealT(self, units="none", desc="Design pressure ratio")
        self.PRmap = RealT(self, units="none", desc="Pressure ratio read from the map table")
        self.PRscale = RealT(self, units="none", desc="Scalar on the pressure ratio map")
        self.Rline = RealT(self, units="none", desc="R-line index value")
        self.RlineDes = RealT(self, units="none", desc="Design point R-line value")
        self.RlineStall= RealT(self, v=1., units="none", desc="The Rline value that representns the stall line")
        self.SMN = RealT( self, units="none", desc="Stall margin based on corrected speed")
        self.Wc = RealT(self, units="lbm/sec", desc="Corrected flow")
        self.WcDes = RealT(self, units="lbm/sec", desc="Design corrected flow")
        self.WcMap = RealT(self, units="lbm/sec", desc="Corrected flow read from the map table")
        self.WcScale = RealT(self, units="none", desc="Scalar on corrected flow map")
        self.Wfrac1 = RealT(self, units="none", desc="Weight flow fraction for bleed flow 1")
        self.Wfrac2 = RealT(self, units="none", desc="Weight flow fraction for bleed flow 2")

        self.size = BooleanT(
            self, v=True, desc="Determine if the element is in design mode or not"
        )
        self.initial_list()

    def calc(self):

        # copy incoming flow to other ports to set their initial composition and state
        self.FNo.copy(self.FNi)
        self.FNideal.copy(self.FNi)
        self.FNoBld1.copy(self.FNi)
        self.FNoBld2.copy(self.FNi)


        # calculate corrected speed amd corrected flow
        self.Nc = self.MP.N / (self.FNi.Tt) ** 0.5
        self.Wc = self.FNi.W * (self.FNi.Tt) ** 0.5 / self.FNi.Pt
        self.Wc = self.FNi.W * (self.FNi.Tt) ** 0.5 / self.FNi.Pt

        # if we are in design mode set Nc scale factor, WcDes, and Rline
        if self.size == True:
            self.NcScale = self.NcMapDes / self.Nc
            self.WcDes = self.Wc
            self.Rline = self.RlineDes

        # scale the corrected speed to the value that will be read from the map
        self.NcMap = self.NcScale * self.Nc

        # read the maps to get efficiency, PR, and Wc at this operating point
        self.effMap = self.effTable.calc(self.NcMap, self.Rline)
        self.PRmap = self.PRtable.calc(self.NcMap, self.Rline)
        self.WcMap = self.WcTable.calc(self.NcMap, self.Rline)

        # if in design mode determine the scale factors
        if self.size == True:
            self.effScale = self.effDes / self.effMap
            self.PRscale = (self.PRdes-1. )/( self.PRmap-1. )
            self.WcScale = self.WcDes / self.WcMap

        # scale the map values
        self.eff = self.effMap * self.effScale
        self.PR = ( self.PRmap-1.) * self.PRscale + 1.0
        self.WcMap = self.WcScale * self.WcMap
        
        # this is not right
        self.SMN = ( self.PRtable.calc(self.NcMap, self.RlineStall) - self.PRmap ) / self.PRmap*100.
        if( self.SMN < 0 ):
        #    print( self.name1, self.RlineStall, self.Rline )
        #if self.Rline < self.RlineStall:
            self.session.errors += "\n" + self.name1 + " stall margin <0."

        # determine the ideal and actual exit conditions
        PtOut = self.FNi.Pt * self.PR
        sOutIdeal = self.FNi.s
        self.FNideal.set_sp( sOutIdeal, PtOut )
        htOutIdeal = self.FNideal.ht

        htOut = self.FNi.ht + (htOutIdeal - self.FNi.ht) / self.eff
        self.FNo.set_hp( htOut, PtOut )


        # set the bleed exit conditions
        self.FNoBld1.set_w(0.0)
        self.FNoBld2.set_w(0.0)

        if self.Wfrac1 > 0.0:
            self.FNoBld1.set_w(self.Wfrac1 * self.FNi.W)
            htBld1 = self.FNi.ht + self.hfract1 * (self.FNo.ht - self.FNi.ht)
            PtBld1 = self.FNi.Pt + self.hfract1 * (self.FNo.Pt - self.FNi.Pt)
            self.FNoBld1.set_hp( htBld1, PtBld1 )

        if self.Wfrac2 > 0.0:
            self.FNoBld2.set_w(self.Wfrac2 * self.FNi.W)
            htBld2 = self.FNi.ht + self.hfract2 * (self.FNo.ht - self.FNi.ht)
            PtBld2 = self.FNi.Pt + self.hfract2 * (self.FNo.Pt - self.FNi.Pt)
            self.FNoBld2.set_hp( htBld2, PtBld2 )

        # recalculate primary exit flow rate
        self.FNo.set_w(self.FNo.W - self.FNoBld1.W - self.FNoBld2.W)


        # calculate and set the mechanical work, negative by convention
        C_BTUperSECtoHP = 1.414284
        self.MP.set_hp(
            -1.0
            * (
                (self.FNo.ht - self.FNi.ht) * self.FNo.W * 3600./2545.
                + (self.FNoBld1.ht - self.FNi.ht) * self.FNoBld1.W * 3600./2545.
                + (self.FNoBld2.ht - self.FNi.ht) * self.FNoBld2.W * 3600./2545.
            )
        )


    def precheck(self):

        if self.Wfrac1 < 0.0000001:
            self.FNoBld1.isPort = False
            
        if self.Wfrac2 < 0.0000001:
            self.FNoBld2.isPort = False 
 
        # design: solver stuff inactive
        if self.size == True:
            self.ind_CR.active = False
            self.dep_CW.active = False
        # off design: solver stuff active
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

    def turbo_mode(self):
        """Change all RealT variables to be native floats"""
        for var in self.VIDL:
            if isinstance(var, RealT):
                print( var.desc )
                var = var.v
