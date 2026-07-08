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
    """Compressor element for Brayton cycle compression calculations.

    A conventional map-based adiabatic compressor that reads maps of efficiency,
    corrected flow, and pressure ratio as a function of R-line (index) and
    corrected speed. This element allows two bleed flows.

    The compressor has two possible bleeds. The ports are described by the weight
    fraction and power fraction of the bleed. The power fraction describes how
    much of the compressor's overall compression is applied to the bleed. A value
    of 0 indicates the bleed comes off at the front of the compressor. A value of
    1.0 indicates the bleed is taken off at the compressor exit.

    The compressor has two modes of operation: sizing and fixed. In sizing mode
    the user inputs a design efficiency and pressure ratio with a design corrected
    flow and a design R-line. These values anchor the map at the sizing point and
    scalars are calculated on all the map parameters to tie the map to the cycle
    sizing point. Away from the sizing point, the scalars are used to determine
    the machine.

    When not in sizing mode, the compressor has a default independent and dependent
    that get added to the solver. The independent controls the R-line and the
    dependent is the flow error between what the system is providing in terms of
    weight flow and what the machine can take in terms of weight flow calculated
    from the scaled map.

    Parameters
    ----------
    name : str
        Name of the compressor element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    eff : RealT
        Adiabatic efficiency.
    effDes : RealT
        Design adiabatic efficiency.
    effMap : RealT
        Efficiency read from the map table.
    effScale : RealT
        Scalar on the efficiency map.
    hfract1 : RealT
        Enthalpy fraction (0=entrance, 1=exit) for bleed flow 1.
    hfract2 : RealT
        Enthalpy fraction (0=entrance, 1=exit) for bleed flow 2.
    Nc : RealT
        Corrected speed (RPM).
    NcMap : RealT
        Corrected speed used to read the map (RPM).
    NcMapDes : RealT
        Design point map corrected speed (RPM).
    NcScale : RealT
        Scalar on corrected speed.
    PR : RealT
        Pressure ratio.
    PRdes : RealT
        Design pressure ratio.
    PRmap : RealT
        Pressure ratio read from the map table.
    PRscale : RealT
        Scalar on the pressure ratio map.
    Rline : RealT
        R-line index value.
    RlineDes : RealT
        Design point R-line value.
    RlineStall : RealT
        The R-line value that represents the stall line.
    SMN : RealT
        Stall margin based on corrected speed.
    Wc : RealT
        Corrected flow (lbm/sec).
    WcDes : RealT
        Design corrected flow (lbm/sec).
    WcMap : RealT
        Corrected flow read from the map table (lbm/sec).
    WcScale : RealT
        Scalar on corrected flow map.
    Wfrac1 : RealT
        Weight flow fraction for bleed flow 1.
    Wfrac2 : RealT
        Weight flow fraction for bleed flow 2.
    effTable : Table2d
        Table of efficiency versus corrected speed and R-line.
    PRtable : Table2d
        Table of pressure ratio versus corrected speed and R-line.
    WcTable : Table2d
        Table of corrected flow versus corrected speed and R-line.
    FNi : FN
        Incoming fluid flow port.
    FNideal : FN
        Ideal exit conditions.
    FNo : FN
        Outgoing fluid flow port.
    FNoBld1 : FN
        Bleed flow 1 port.
    FNoBld2 : FN
        Bleed flow 2 port.
    MP : MP
        Mechanical port connection.
    """

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
        self.FNi = FN(self, io="in", desc="Incoming fluid flow")
        self.FNideal = FN(self, desc="Ideal exit conditions", isPort=False)
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
        self.effMap = RealT(
            self, units="none", desc="Efficiency read from the map table"
        )
        self.effScale = RealT(self, units="none", desc="Scalar on the efficiency map")
        self.hfract1 = RealT(
            self,
            units="BTU/lbm",
            desc="Enthalpy fraction (0=entrance, 1=exit) for bleed flow 1",
        )
        self.hfract2 = RealT(
            self,
            units="BTU/lbm",
            desc="Enthalpy fraction (0=entrance, 1=exit) for bleed flow 2",
        )
        self.Nc = RealT(self, units="RPM", desc="Corrected speed")
        self.NcMap = RealT(
            self, units="RPM", desc="Corrected speed used to read the map"
        )
        self.NcMapDes = RealT(
            self, units="RPM", desc="Design point map corrected speed"
        )
        self.NcScale = RealT(self, units="none", desc="Scalar on corrected speed")
        self.PR = RealT(self, units="none", desc="Pressure ratio")
        self.PRdes = RealT(self, units="none", desc="Design pressure ratio")
        self.PRmap = RealT(
            self, units="none", desc="Pressure ratio read from the map table"
        )
        self.PRscale = RealT(
            self, units="none", desc="Scalar on the pressure ratio map"
        )
        self.Rline = RealT(self, units="none", desc="R-line index value")
        self.RlineDes = RealT(self, units="none", desc="Design point R-line value")
        self.RlineStall = RealT(
            self,
            v=1.0,
            units="none",
            desc="The Rline value that representns the stall line",
        )
        self.SMN = RealT(
            self, units="none", desc="Stall margin based on corrected speed"
        )
        self.Wc = RealT(self, units="lbm/sec", desc="Corrected flow")
        self.WcDes = RealT(self, units="lbm/sec", desc="Design corrected flow")
        self.WcMap = RealT(
            self, units="lbm/sec", desc="Corrected flow read from the map table"
        )
        self.WcScale = RealT(self, units="none", desc="Scalar on corrected flow map")
        self.Wfrac1 = RealT(
            self, units="none", desc="Weight flow fraction for bleed flow 1"
        )
        self.Wfrac2 = RealT(
            self, units="none", desc="Weight flow fraction for bleed flow 2"
        )

        self.size = BooleanT(
            self, v=True, desc="Determine if the element is in design mode or not"
        )

        self.desc = "Compressor - This element is a conventional map based adiabatic "
        "compressor. The user inputs a design point efficiency and pressure raio. The "
        "user also supplies a compressor map. This map is three 2-D tables that "
        "describe the machines weight flow, efficiency, and pressure ratio as a "
        "function of corrected speed and Rline. The Riline is a mathmatical construct "
        "that moves the compressore operating point away from the stall line.\nThe "
        "compressor has two possible bleed power. The ports are described the weight "
        "fraction and power fraction of the bleed. The power fraction describes how "
        "much of the compressor's overall compressor is applied to the bleed. A value "
        "of 0 indicates the bleed comes off at the from of the compressor. A value of "
        "1.0 indicates the bleed is take off at the compressor exit.\nThe compressor "
        "has two modes of operation, sizing and fixed. In sizing mode The user inputs "
        "a design efficiency and pressure ratio with a design corrected and a design "
        "Rline. This values anchor the map at the sizing point and scalars are "
        "calculated on all the map parameters to tie the map to cycle sizing point. "
        "Away from the sizing point, the scalars are used to determine the machine.\n"
        "When not in sizing mode, the compressor has a default independent and "
        "dependent that get added to the solver. The independent controls the Rline "
        "and the dependent is the flow error between what the system is providing in "
        "terms of weight flow and what the machine can take in terms of weight flow "
        "calculated from the scaled map."

        self.initial_list()

    def calc(self):
        """Calculate compressor exit conditions and performance.

        Copies incoming flow to all ports, calculates corrected speed and
        corrected flow, reads efficiency/PR/Wc from map tables (with scaling
        if in sizing mode), computes ideal and actual exit enthalpies, sets
        bleed flow conditions, and calculates mechanical work.

        The corrected speed is computed as::

            Nc = N / (Tt_in / 518.67)^0.5

        The corrected flow is computed as::

            Wc = W_in * (Tt_in / 518.67)^0.5 / (Pt_in / 14.696)

        In sizing mode, scalars are calculated to anchor the map at the design
        point. The ideal exit enthalpy is computed from isentropic relations,
        and the actual exit enthalpy uses the efficiency::

            ht_out = ht_in + (ht_out_ideal - ht_in) / eff

        Mechanical work is computed as::

            HP = -(ht_out - ht_in) * W_out * 3600/2545
               - (ht_bld1 - ht_in) * W_bld1 * 3600/2545
               - (ht_bld2 - ht_in) * W_bld2 * 3600/2545
        """
       
        # copy incoming flow to other ports to set their initial composition and state
        self.FNo.copy(self.FNi)
        self.FNideal.copy(self.FNi)
        self.FNoBld1.copy(self.FNi)
        self.FNoBld2.copy(self.FNi)

        # calculate corrected speed amd corrected flow
        self.Nc = self.MP.N / (self.FNi.Tt / 518.67) ** 0.5
        self.Wc = self.FNi.W * (self.FNi.Tt / 518.67) ** 0.5 / (self.FNi.Pt / 14.696)

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
            self.PRscale = (self.PRdes - 1.0) / (self.PRmap - 1.0)
            self.WcScale = self.WcDes / self.WcMap

        # scale the map values
        self.eff = self.effMap * self.effScale
        self.PR = (self.PRmap - 1.0) * self.PRscale + 1.0
        self.WcMap = self.WcScale * self.WcMap

        # this is not right
        self.SMN = (
            (self.PRtable.calc(self.NcMap, self.RlineStall) - self.PRmap)
            / self.PRmap
            * 100.0
        )
        if self.SMN < 0:
            # if self.Rline < self.RlineStall:
            self.session.errors += "\n" + self.name1 + " stall margin <0."

        # determine the ideal and actual exit conditions
        PtOut = self.FNi.Pt * self.PR
        sOutIdeal = self.FNi.s
        self.FNideal.set_sp(sOutIdeal, PtOut)
        htOutIdeal = self.FNideal.ht

        htOut = self.FNi.ht + (htOutIdeal - self.FNi.ht) / self.eff
        self.FNo.set_hp(htOut, PtOut)

        # set the bleed exit conditions
        self.FNoBld1.set_w(0.0)
        self.FNoBld2.set_w(0.0)

        if self.Wfrac1 > 0.0:
            self.FNoBld1.set_w(self.Wfrac1 * self.FNi.W)
            htBld1 = self.FNi.ht + self.hfract1 * (self.FNo.ht - self.FNi.ht)
            PtBld1 = self.FNi.Pt + self.hfract1 * (self.FNo.Pt - self.FNi.Pt)
            self.FNoBld1.set_hp(htBld1, PtBld1)

        if self.Wfrac2 > 0.0:
            self.FNoBld2.set_w(self.Wfrac2 * self.FNi.W)
            htBld2 = self.FNi.ht + self.hfract2 * (self.FNo.ht - self.FNi.ht)
            PtBld2 = self.FNi.Pt + self.hfract2 * (self.FNo.Pt - self.FNi.Pt)
            self.FNoBld2.set_hp(htBld2, PtBld2)

        # recalculate primary exit flow rate
        self.FNo.set_w(self.FNo.W - self.FNoBld1.W - self.FNoBld2.W)

        # calculate and set the mechanical work, negative by convention
        self.MP.set_hp(
            -1.0
            * (
                (self.FNo.ht - self.FNi.ht) * self.FNo.W * 3600.0 / 2545.0
                + (self.FNoBld1.ht - self.FNi.ht) * self.FNoBld1.W * 3600.0 / 2545.0
                + (self.FNoBld2.ht - self.FNi.ht) * self.FNoBld2.W * 3600.0 / 2545.0
            )
        )

    def precheck(self):
        """Check bleed flows and solver state based on sizing mode.

        If bleed flow fractions are near zero, sets the corresponding port
        inactive. In sizing mode, solver independent and dependent are
        deactivated. In off-design mode, they are activated.
        """

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
        """Dump compressor state to an output file.

        Parameters
        ----------
        output_file : file-like
            File object to write the compressor state to.
        """
        # dump output variables
        output_file.write(f"{self.name1} Compressor\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Print a formatted summary of the compressor state.

        Parameters
        ----------
        output_file : file-like
            File object to write the pretty-printed output to.
        """
        output_file.write(
            f"{'Compressor'[:10]:12s}{self.name1[:10]:12s}"
            f"{('PR:' + str(self.PR))[:10]:12s}"
            f"{('eff:' + str(self.eff))[:10]:12s}"
            f"{('Rline:' + str(self.Rline))[:10]:12s}"
            f"{('NcMap:' + str(self.NcMap))[:10]:12s}\n"
        )
