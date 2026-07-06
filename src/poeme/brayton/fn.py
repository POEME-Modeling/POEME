import math

from poeme import Atom, BooleanT, RealT, StringT, ValueT

from .air2 import Air2
from .air4 import Air4
from .air6 import Air6
from .cantera_fn import CanteraFN
from .cpr134 import CPR134
from .h2o import H2O
from .newtherm import Newtherm
from .r32 import R32
from .r134 import R134

GAS_MODELS = {
    "H2O": H2O,
    "R32": R32,
    "CPR134": CPR134,
    "R134": R134,
    "air2": Air2,
    "air4": Air4,
    "air6": Air6,
    "CanteraFN": CanteraFN,
    "Newtherm": Newtherm,
}


class FN(Atom):
    def __init__(self, p, **kwargs):
        # Bypass __setattr__ during init — ValueT objects don't exist yet
        self.__dict__.update(
            {
                "parent": p,
                "session": p.session,
                "name1": "",
                "VIDL": [],
                "type": "FN",
                "other": 0,
                "isPort": True,
            }
        )
        self.__dict__.update(kwargs)
        if p != 0:
            p.add_vid(self)

        # All name1 tagging is handled automatically by __setattr__
        self.comp = StringT(self, v="none", desc="composition string")
        self.FAR = RealT(self, v=0.0, units="none", desc="Fuel to air ratio")
        self.WAR = RealT(self, v=0.0, units="none", desc="Water to air ratio")
        self.W = RealT(self, v=0.0, units="lbm/sec", desc="Weight flow")
        self.Tt = RealT(self, v=0.0, units="Rankine", desc="Total temperature")
        self.Pt = RealT(self, v=0.0, units="lbf/in2", desc="Total pressure")
        self.ht = RealT(self, v=0.0, units="BTU/lbm", desc="Specific total enthalpy")
        self.rhot = RealT(self, v=0.0, units="lbm/ft3", desc="Total density")
        self.mut = RealT(
            self, v=0.0, units="lbm/(ft*sec)", desc="Total dynmanic viscosity"
        )
        self.kt = RealT(
            self, v=0.0, units="BTU/(ft*sec*R)", desc="Total thermal conductivity"
        )
        self.Cpt = RealT(
            self,
            v=0.0,
            units="BTU/(lbm*R)",
            desc="Total specific heat at constant pressure",
        )
        self.gamt = RealT(
            self, v=0.0, units="none", desc="Total ratio of specific heats"
        )
        self.Rt = RealT(self, v=0.0, units="BTU/(lbm*R)", desc="Total gas constant")
        self.Rs = RealT(self, v=0.0, units="BTU/(lbm*R)", desc="Static constant")
        self.s = RealT(self, v=0.0, units="BTU/(lbm*R)", desc="Entropy")
        self.MN = RealT(self, v=-9999.0, units="Mach number", desc="Mach number")
        self.A = RealT(self, v=-9999.0, units="in2", desc="Flow area")
        self.V = RealT(self, v=0.0, units="ft/sec", desc="Velocity")
        self.Ts = RealT(self, v=0.0, units="Rankine", desc="Static temperature")
        self.Ps = RealT(self, v=0.0, units="lbf/in2", desc="Static pressure")
        self.hs = RealT(self, v=0.0, units="BTU/lbm", desc="Static specific enthalkpy")
        self.rhos = RealT(self, v=0.0, units="lbm/ft3", desc="Static density")
        self.mus = RealT(self, v=0.0, units="lbm/(ft*sec)", desc="Static viscosity")
        self.ks = RealT(
            self, v=0.0, units="BTU/(ft*sec*R)", desc="Static thermal conductivity"
        )
        self.Cps = RealT(
            self,
            v=0.0,
            units="BTU/(lbm*R)",
            desc="Static specific heat at constant pressure",
        )
        self.gams = RealT(
            self, v=0.0, units="none", desc="Static specific heat at constant pressure"
        )
        self.size = BooleanT(
            self, v=True, desc="Determines if we are running to fixed Mach or Area"
        )
        self.isPort = BooleanT(
            self,
            v=self.isPort,
            desc="Determines if we are running to fixed Mach or Area",
        )
        self.size = BooleanT(
            self, v=True, desc="Determines if we are running to fixed Mach or Area"
        )
        self.twoPhase = BooleanT(
            self,
            v=False,
            desc="Determines if we need to use enthalpy for all properties",
        )

    def __setattr__(self, name, value):
        existing = self.__dict__.get(name)
        if isinstance(existing, ValueT):
            existing.set(value)
        else:
            super().__setattr__(name, value)
        if hasattr(value, "name1"):
            value.name1 = name

    def add_vid(self, v):
        self.VIDL.append(v)

    def isa(self, type):
        return type == "FN"

    def add(self, o):
        self.ht.v = (self.ht.v * self.W.v + o.ht.v * o.W.v) / (self.W.v + o.W.v)
        fuel_air_ratio_t = self.FAR.v
        self.FAR.v = (
            self.W.v * self.FAR.v / (1.0 + self.FAR.v + self.WAR.v)
            + o.W.v * o.FAR.v / (1.0 + o.FAR.v + o.WAR.v)
        ) / (
            self.W.v / (1.0 + self.FAR.v + self.WAR.v)
            + o.W.v / (1.0 + o.FAR.v + o.WAR.v)
        )
        self.WAR.v = (
            self.W.v * self.WAR.v / (1.0 + fuel_air_ratio_t + self.WAR.v)
            + o.W.v * o.WAR.v / (1.0 + o.FAR.v + o.WAR.v)
        ) / (
            self.W.v / (1.0 + fuel_air_ratio_t + self.WAR.v)
            + o.W.v / (1.0 + o.FAR.v + o.WAR.v)
        )
        self.W.v = self.W.v + o.W.v
        self.set_hp(self.ht.v, self.Pt.v)

    def set_tp(self, Tt, Pt):
        if isinstance(Tt, float):
            self.Tt.v = Tt
        else:
            self.Tt.v = Tt.v
        if isinstance(Pt, float):
            self.Pt.v = Pt
        else:
            self.Pt.v = Pt.v
        if self.twoPhase == False:
            self.ht.v = GAS_MODELS[self.comp.v].h_TP(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.s.v = GAS_MODELS[self.comp.v].s_TP(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.rhot.v = GAS_MODELS[self.comp.v].rho(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.Rt.v = GAS_MODELS[self.comp.v].R(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.Cpt.v = GAS_MODELS[self.comp.v].Cp(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.gamt.v = GAS_MODELS[self.comp.v].gamma(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.mut.v = GAS_MODELS[self.comp.v].mu(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
        else:
            self.ht.v = GAS_MODELS[self.comp.v].h_TP(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.s.v = GAS_MODELS[self.comp.v].s_TP(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.rhot.v = GAS_MODELS[self.comp.v].rho(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.Rt.v = GAS_MODELS[self.comp.v].R(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.Cpt.v = GAS_MODELS[self.comp.v].Cp(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.gamt.v = GAS_MODELS[self.comp.v].gamma(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.mut.v = GAS_MODELS[self.comp.v].mu(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
        self.statics()
        if self.other != 0:
            self.other.copy_deep(self)

    def set_hp(self, ht, Pt):
        if isinstance(ht, float):
            self.ht.v = ht
        else:
            self.ht.v = ht.v
        if isinstance(Pt, float):
            self.Pt.v = Pt
        else:
            self.Pt.v = Pt.v
        if self.twoPhase == False:
            self.Tt.v = GAS_MODELS[self.comp.v].T_hp(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.s.v = GAS_MODELS[self.comp.v].s_TP(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.rhot.v = GAS_MODELS[self.comp.v].rho(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.Rt.v = GAS_MODELS[self.comp.v].R(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.gamt.v = GAS_MODELS[self.comp.v].gamma(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.Cpt.v = GAS_MODELS[self.comp.v].Cp(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.mut.v = GAS_MODELS[self.comp.v].mu(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
        else:
            self.Tt.v = GAS_MODELS[self.comp.v].T_hp(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.s.v = GAS_MODELS[self.comp.v].s_hP(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.rhot.v = GAS_MODELS[self.comp.v].rho(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.Rt.v = GAS_MODELS[self.comp.v].R(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.gamt.v = GAS_MODELS[self.comp.v].gamma(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.Cpt.v = GAS_MODELS[self.comp.v].Cp(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.mut.v = GAS_MODELS[self.comp.v].mu(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )

        self.statics()
        if self.other != 0:
            self.other.copy_deep(self)

    def set_sp(self, s, Pt):
        if isinstance(s, float):
            self.s.v = s
        else:
            self.s.v = s.v
        if isinstance(Pt, float):
            self.Pt.v = Pt
        else:
            self.Pt.v = Pt.v
        if self.twoPhase == False:
            self.Tt.v = GAS_MODELS[self.comp.v].T_sP(
                self.s.v, self.Pt.v, self.FAR.v, self
            )
            self.ht.v = GAS_MODELS[self.comp.v].h_TP(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.rhot.v = GAS_MODELS[self.comp.v].rho(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.Rt.v = GAS_MODELS[self.comp.v].R(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.gamt.v = GAS_MODELS[self.comp.v].gamma(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.Cpt.v = GAS_MODELS[self.comp.v].Cp(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.mut.v = GAS_MODELS[self.comp.v].mu(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
        else:
            self.Tt.v = GAS_MODELS[self.comp.v].T_sP(
                self.s.v, self.Pt.v, self.FAR.v, self
            )
            self.ht.v = GAS_MODELS[self.comp.v].h_sp(
                self.s.v, self.Pt.v, self.FAR.v, self
            )
            self.rhot.v = GAS_MODELS[self.comp.v].rho(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.Rt.v = GAS_MODELS[self.comp.v].R(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.gamt.v = GAS_MODELS[self.comp.v].gamma(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.Cpt.v = GAS_MODELS[self.comp.v].Cp(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.mut.v = GAS_MODELS[self.comp.v].mu(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
        self.statics()
        if self.other != 0:
            self.other.copy_deep(self)

    def set_hs(self, h, s):
        if isinstance(h, float):
            self.ht.v = h
        else:
            self.ht.v = h.v
        if isinstance(s, float):
            self.s.v = s
        else:
            self.s.v = s.v

        self.Pt.v = GAS_MODELS[self.comp.v].P_hs(self.ht.v, self.s.v, self.FAR.v, self)
        self.set_sp(self.s.v, self.Pt.v)

    def set_ps(self, Ps):
        self.Ps.v = Ps
        self.ps_calc()

    def statics(self):

        self.gams.v = self.gamt.v
        self.rhos.v = self.rhot.v
        if self.size.v == True:
            if self.MN.v < 0.0:
                return
            if self.MN.v < 0.00001:
                self.A = -9999.0
                self.V.v = 0.0
                self.Ts.v = self.Tt
                self.Ps.v = self.Pt
                self.hs.v = self.ht
                self.rhos.v = self.rhos
                self.mus.v = self.mut
                self.ks.v = self.kt
                self.Cps.v = self.Cpt
                self.gams.v = self.gamt
                return

            mnor = self.MN.v
            self.Ps.v = self.Pt.v * 0.9
            self.ps_calc()
            errorm1 = 0
            xm1 = 0
            self.Ps.v = self.Ps.v * 0.95
            self.ps_calc()

            error = (self.MN.v - mnor) / mnor
            x = self.Ps.v
            count = 0
            while abs(error) > 0.00001 and count < 50:
                count = count + 1
                xp1 = x - error * (x - xm1) / (error - errorm1)
                if xp1 - x > 0.1 * self.Pt.v:
                    xp1 = x + 0.1 * self.Pt.v
                if xp1 - x < -0.1 * self.Pt.v:
                    xp1 = x - 0.1 * self.Pt.v
                xm1 = x
                errorm1 = error
                x = xp1
                self.Ps.v = x

                self.ps_calc()

                error = (self.MN.v - mnor) / mnor

            if count > 49:
                self.session.errors += "MN iteration failure\n"

            self.MN.v = mnor

        else:
            if self.A.v < 0.0:
                self.MN.v = 0.0
                self.V.v = 0.0
                self.Ts.v = self.Tt.v
                self.Ps.v = self.Pt.v
                self.hs.v = self.ht.v
                self.rhos.v = self.rhos.v
                self.mus.v = self.mut.v
                self.ks.v = self.kt.v
                self.Cps.v = self.Cpt.v
                self.gams.v = self.gamt.v
                return

            aor = self.A.v
            self.Ps.v = self.Pt.v * 0.99
            self.ps_calc()
            errorm1 = (self.A.v - aor) / aor
            xm1 = self.MN.v
            self.Ps.v = self.Ps.v * 0.95
            self.ps_calc()
            error = (self.A.v - aor) / aor
            x = self.Ps.v

            count = 0
            while abs(error) > 0.00001 and count < 50:
                count += 1

                xp1 = x - error * (x - xm1) / (error - errorm1)

                if xp1 - x > 0.1 * x:
                    xp1 = x + 0.1 * x
                if xp1 - x < -0.1 * x:
                    xp1 = x - 0.1 * x
                xm1 = x
                xp1 = min(xp1, self.Pt.v * 0.99)

                errorm1 = error
                x = xp1
                self.Ps.v = x
                self.ps_calc()
                # print( self.Ps.v, self.A.v, aor, self.MN.v )
                error = (self.A.v - aor) / aor

            if count >= 49:
                new_error = f"{self.parent.name1}.{self.name1} failure "
                "during static area match\n"
                self.session.errors += new_error

            self.A.v = aor

    def ps_calc(self):
        if self.twoPhase == False:
            self.Ts.v = GAS_MODELS[self.comp.v].T_sP(
                self.s.v, self.Ps.v, self.FAR.v, self
            )
            self.hs.v = GAS_MODELS[self.comp.v].h_TP(
                self.Ts.v, self.Ps.v, self.FAR.v, self
            )
            self.rhos.v = GAS_MODELS[self.comp.v].rho(
                self.Ts.v, self.Ps.v, self.FAR.v, self
            )
            self.Rs.v = GAS_MODELS[self.comp.v].R(
                self.Ts.v, self.Ps.v, self.FAR.v, self
            )
            self.Cps.v = GAS_MODELS[self.comp.v].Cp(
                self.Ts.v, self.Ps.v, self.FAR.v, self
            )
            self.mus.v = GAS_MODELS[self.comp.v].mu(
                self.Ts.v, self.Ps.v, self.FAR.v, self
            )
            self.ks.v = GAS_MODELS[self.comp.v].k(
                self.Ts.v, self.Ps.v, self.FAR.v, self
            )
            self.gams.v = GAS_MODELS[self.comp.v].gamma(
                self.Ts.v, self.Ps.v, self.FAR.v, self
            )
            self.V.v = (
                math.sqrt(2 * abs(self.ht.v - self.hs.v) * 25037.0)
                * abs(self.ht.v - self.hs.v)
                / (self.ht.v - self.hs.v)
            )
            self.MN.v = (
                self.V.v
                / math.sqrt(self.gams.v * self.Rs.v * self.Ts.v * 25037.0)
                * abs(self.ht.v - self.hs.v)
                / (self.ht.v - self.hs.v)
            )
            self.A.v = self.W.v / (self.rhos.v * abs(self.V.v))
        else:
            self.Ts.v = GAS_MODELS[self.comp.v].T_sP(
                self.s.v, self.Ps.v, self.FAR.v, self
            )
            self.hs.v = GAS_MODELS[self.comp.v].h_sp(
                self.s.v, self.Ps.v, self.FAR.v, self
            )
            self.rhos.v = GAS_MODELS[self.comp.v].rho(
                self.hs.v, self.Ps.v, self.FAR.v, self
            )
            self.Rs.v = GAS_MODELS[self.comp.v].R(
                self.hs.v, self.Ps.v, self.FAR.v, self
            )
            self.Cps.v = GAS_MODELS[self.comp.v].Cp(
                self.hs.v, self.Ps.v, self.FAR.v, self
            )
            self.mus.v = GAS_MODELS[self.comp.v].mu(
                self.hs.v, self.Ps.v, self.FAR.v, self
            )
            self.ks.v = GAS_MODELS[self.comp.v].k(
                self.hs.v, self.Ps.v, self.FAR.v, self
            )
            self.gams.v = GAS_MODELS[self.comp.v].gamma(
                self.hs.v, self.Ps.v, self.FAR.v, self
            )
            self.V.v = (
                math.sqrt(2 * abs(self.ht.v - self.hs.v) * 25037.0)
                * abs(self.ht.v - self.hs.v)
                / (self.ht.v - self.hs.v)
            )
            self.MN.v = (
                self.V.v
                / math.sqrt(self.gams.v * self.Rs.v * self.Ts.v * 25037.0)
                * abs(self.ht.v - self.hs.v)
                / (self.ht.v - self.hs.v)
            )
            self.A.v = self.W.v / (self.rhos.v * abs(self.V.v))

    def link_fn(self, fn):
        if self.other != 0:
            print(self.parent.name1 + "." + self.name1 + " is already linked ")
            quit()
        if fn.other != 0:
            print(fn.parent.name1 + "." + fn.name1 + " is already linked ")
            quit()
        if fn.isa("FN") == False:
            print(fn.parent.name1 + "." + fn.name1 + " is not a fluid node ")
            quit()

        self.__dict__.update({"other": fn})
        fn.__dict__.update({"other": self})

    def copy(self, e):
        self.comp.v = e.comp.v
        self.twoPhase.v = e.twoPhase.v
        self.FAR.v = e.FAR.v
        self.W.v = e.W.v
        self.Tt.v = e.Tt.v
        self.Pt.v = e.Pt.v
        self.ht.v = e.ht.v
        self.rhot.v = e.rhot.v
        self.mut.v = e.mut.v
        self.kt.v = e.kt.v
        self.Cpt.v = e.Cpt.v
        self.gamt.v = e.gamt.v
        self.Rt.v = e.Rt.v
        self.s.v = e.s.v
        if self.other != 0:
            self.other.comp.v = e.comp.v
            self.other.FAR.v = e.FAR.v
            self.other.W.v = e.W.v
            self.other.Tt.v = e.Tt.v
            self.other.Pt.v = e.Pt.v
            self.other.ht.v = e.ht.v
            self.other.rhot.v = e.rhot.v
            self.other.mut.v = e.mut.v
            self.other.kt.v = e.kt.v
            self.other.Cpt.v = e.Cpt.v
            self.other.gamt.v = e.gamt.v
            self.other.Rt.v = e.Rt.v
            self.other.s.v = e.s.v

    def copy_deep(self, e):
        self.twoPhase.v = e.twoPhase.v
        self.comp.v = e.comp.v
        self.FAR.v = e.FAR.v
        self.W.v = e.W.v
        self.Tt.v = e.Tt.v
        self.Pt.v = e.Pt.v
        self.ht.v = e.ht.v
        self.rhot.v = e.rhot.v
        self.mut.v = e.mut.v
        self.kt.v = e.kt.v
        self.Cpt.v = e.Cpt.v
        self.gamt.v = e.gamt.v
        self.Rt.v = e.Rt.v
        self.Rs.v = e.Rs.v
        self.s.v = e.s.v
        self.MN.v = e.MN.v
        self.A.v = e.A.v
        self.V.v = e.V.v
        self.Ts.v = e.Ts.v
        self.Ps.v = e.Ps.v
        self.hs.v = e.hs.v
        self.rhos.v = e.rhos.v
        self.mus.v = e.mus.v
        self.ks.v = e.ks.v
        self.Cps.v = e.Cps.v
        self.gams.v = e.gams.v
        self.size.v = e.size.v
        if self.other != 0:
            self.comp.v = e.comp.v
            self.FAR.v = e.FAR.v
            self.W.v = e.W.v
            self.Tt.v = e.Tt.v
            self.Pt.v = e.Pt.v
            self.ht.v = e.ht.v
            self.rhot.v = e.rhot.v
            self.mut.v = e.mut.v
            self.kt.v = e.kt.v
            self.Cpt.v = e.Cpt.v
            self.gamt.v = e.gamt.v
            self.Rt.v = e.Rt.v
            self.Rs.v = e.Rs.v
            self.s.v = e.s.v
            self.MN.v = e.MN.v
            self.A.v = e.A.v
            self.V.v = e.V.v
            self.Ts.v = e.Ts.v
            self.Ps.v = e.Ps.v
            self.hs.v = e.hs.v
            self.rhos.v = e.rhos.v
            self.mus.v = e.mus.v
            self.ks.v = e.ks.v
            self.Cps.v = e.Cps.v
            self.gams.v = e.gams.v
            self.size.v = e.size.v

    def set_w(self, w):
        if isinstance(w, float):
            self.W.v = w
            if self.other != 0:
                self.other.W.v = w
        else:
            self.W.v = w.v
            if self.other != 0:
                self.other.W.v = w.v

    def set_ts_ps_mn(self, Ts_i, Ps_i, MN_i):
        Ts = Ts_i if isinstance(Ts_i, float) else Ts_i.v
        Ps = Ps_i if isinstance(Ps_i, float) else Ps_i.v
        MN = MN_i if isinstance(MN_i, float) else MN_i.v

        self.size.v = True
        self.MN.v = 0.0
        self.A.v = 0.0
        self.set_tp(Ts, Ps)

        s = self.s
        # TODO: do we need the Tt calculation here? It doesn't seem to be used
        # Tt = Ts * (1.0 + (self.gamt.v - 1.0) / 2.0 * MN**2.0)
        Pt = Ps * (1.0 + (self.gamt.v - 1.0) / 2.0 * MN**2.0) ** (
            (self.gamt.v - 1.0) / self.gamt.v
        )
        self.V.v = MN * math.sqrt(self.gamt.v * self.Rt.v * Ts * 25037.0)
        ht = self.V.v**2.0 / 25037.0 / 2.0 + self.ht.v
        self.set_sp(s, Pt)

        errorm1 = self.ht - ht

        xm1 = Pt
        Pt = self.Pt.v * 0.95
        self.set_sp(s, Pt)
        error = self.ht - ht
        x = Pt

        i = 0
        count = 0
        while abs(error) > 0.00001 and count < 50:
            count = count + 1
            xp1 = x - error * (x - xm1) / (error - errorm1)
            if xp1 - x > 0.05 * self.Pt.v:
                xp1 = x + 0.05 * self.Pt.v
            if xp1 - x < -0.05 * self.Pt.v:
                xp1 = x - 0.05 * self.Pt.v
            xm1 = x
            errorm1 = error
            x = xp1
            Pt = x
            self.set_sp(s, Pt)
            error = self.ht - ht
            i = i + 1

        self.size.v = True
        self.MN.v = MN
        self.statics()
        if self.other != 0:
            self.other.copy_deep(self)

    def dump(self, output_file):
        output_file.write(
            f"{self.parent.name1[:8]:10s} {self.name1[:8]:10s}  "
            f"W:{str(self.W.v)[:8]:10s}  Tt:{str(self.Tt.v)[:8]:10s}  "
            f"Pt:{str(self.Pt.v)[:8]:10s}  FAR:{str(self.FAR.v)[:8]:10s}  "
            f"MN:{str(self.MN.v)[:8]:10s}  Ts:{str(self.Ts.v)[:8]:10s}  "
            f"Ps:{str(self.Ps.v)[:8]:10s}\n"
        )

    def pretty(self, output_file):
        output_file.write(
            f"{self.parent.name1[:8]:10s} {self.name1[:8]:10s}  "
            f"W:{str(self.W.v)[:8]:10s}  Tt:{str(self.Tt.v)[:8]:10s}  "
            f"Pt:{str(self.Pt.v)[:8]:10s}  ht:{str(self.ht.v)[:8]:10s}  "
            f"FAR:{str(self.FAR.v)[:8]:10s}  MN:{str(self.MN.v)[:8]:10s}  "
            f"Ts:{str(self.Ts.v)[:8]:10s}  Ps:{str(self.Ps.v)[:8]:10s}\n"
        )

    def hover(self):
        return (
            self.parent.name1
            + " "
            + self.name1
            + " "
            + str(self.W.v)
            + " "
            + str(self.Tt.v)
            + " "
            + str(self.Pt.v)
            + " "
            + str(self.FAR.v)
        )

    def save_print(self):
        temp = (
            self.parent.name1 + "." + self.name1 + ".MN.set( " + str(self.MN.v)
        ) + ")\n"
        temp = (
            temp
            + (self.parent.name1 + "." + self.name1 + '.comp.set( "' + str(self.comp.v))
            + '")\n'
        )
        temp = (
            temp
            + (self.parent.name1 + "." + self.name1 + ".A.set( " + str(self.A.v))
            + ")\n"
        )
        temp = (
            temp
            + (self.parent.name1 + "." + self.name1 + ".size.set( " + str(self.size.v))
            + ")"
        )
        return temp
