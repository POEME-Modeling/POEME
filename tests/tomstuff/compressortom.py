from poeme import (
    BooleanT,
    Dependent,
    Element,
    Independent,
    ModelSession,
    RealT,
    Table2d,
)

from poeme.brayton import FN, MP


class CompressorTom(Element):
    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "CompressorTom", session=session)
        self.type = "Compressor"

        # tables
        self.effTable = Table2d( self )
        self.PRtable = Table2d( self )
        self.WcTable = Table2d( self )

        # fluid locations/ports
        self.FNi = FN(self)
        self.FNideal = FN(self, isPort=False)
        self.FNo = FN(self)
        self.FNoBld1 = FN(self)
        self.FNoBld2 = FN(self)

        # mechanical connections
        self.MP = MP(self)

        # solver stuff
        self.ind_CR = Independent(
            self,
            indname="Rline",
            perturb=0.05,
            scale=100,
            perturb_type="Relative",
            active=False,
        )
        self.dep_CW = Dependent(
            self,
            d1name="Wc",
            d2name="WcMap",
            active=False,
        )

        # variables
        self.eff = RealT(self)
        self.effDes = RealT(self)
        self.effMap = RealT(self)
        self.effScale = RealT(self)
        self.hfract1 = RealT(self)
        self.hfract2 = RealT(self)
        self.Nc = RealT(self)
        self.NcMap = RealT(self)
        self.NcMapDes = RealT(self)
        self.NcScale = RealT(self)
        self.PR = RealT(self)
        self.PRdes = RealT(self)
        self.PRmap = RealT(self)
        self.PRscale = RealT(self)
        self.Rline = RealT(self)
        self.RlineDes = RealT(self)
        self.RlineStall= RealT(self)
        self.SMN = RealT(self)
        self.Wc = RealT(self)
        self.WcDes = RealT(self)
        self.WcMap = RealT(self)
        self.WcScale = RealT(self)
        self.Wfrac1 = RealT(self)
        self.Wfrac2 = RealT(self)

        self.size = BooleanT(self, v=True)
         
        self.initial_list()
        

    def calc(self):

        # copy incoming flow to other ports to set their initial composition and state
        self.FNo.copy(self.FNi)
        self.FNideal.copy(self.FNi)
        self.FNoBld1.copy(self.FNi)
        self.FNoBld2.copy(self.FNi)


        # calculate corrected speed amd corrected flow
        self.Nc = self.MP.N / (self.FNi.Tt/518.67)**0.5
        self.Wc = self.FNi.W * (self.FNi.Tt/518.67)**0.5 / (self.FNi.Pt/14.696 )

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

