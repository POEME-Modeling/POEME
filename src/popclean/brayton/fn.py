import math

from popclean import Atom, BooleanT, RealT, StringT, ValueT, g
from popclean.working.newtherm import Newtherm

from .air2 import Air2
from .air4 import Air4
from .air6 import Air6
from .cantera_fn import CanteraFN
from .cpr134 import CPR134
from .h2o import H2O
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
                "name1": "",
                "VIDL": [],
                "type": "FN",
                "other": 0,
            }
        )
        self.__dict__.update(kwargs)
        if p != 0:
            p.add_vid(self)

        # All name1 tagging is handled automatically by __setattr__
        self.comp = StringT(self, v="none", desc="")
        self.FAR = RealT(self, v=0.0, units="", desc="")
        self.WAR = RealT(self, v=0.0, units="", desc="")
        self.W = RealT(self, v=0.0, units="", desc="")
        self.Tt = RealT(self, v=0.0, units="", desc="")
        self.Pt = RealT(self, v=0.0, units="", desc="")
        self.ht = RealT(self, v=0.0, units="", desc="")
        self.rhot = RealT(self, v=0.0, units="", desc="")
        self.mut = RealT(self, v=0.0, units="", desc="")
        self.kt = RealT(self, v=0.0, units="", desc="")
        self.Cpt = RealT(self, v=0.0, units="", desc="")
        self.gamt = RealT(self, v=0.0, units="", desc="")
        self.Rt = RealT(self, v=0.0, units="", desc="")
        self.Rs = RealT(self, v=0.0, units="", desc="")
        self.s = RealT(self, v=0.0, units="", desc="")
        self.MN = RealT(self, v=0.0, units="", desc="")
        self.A = RealT(self, v=0.0, units="", desc="")
        self.V = RealT(self, v=0.0, units="", desc="")
        self.Ts = RealT(self, v=0.0, units="", desc="")
        self.Ps = RealT(self, v=0.0, units="", desc="")
        self.hs = RealT(self, v=0.0, units="", desc="")
        self.rhos = RealT(self, v=0.0, units="", desc="")
        self.mus = RealT(self, v=0.0, units="", desc="")
        self.ks = RealT(self, v=0.0, units="", desc="")
        self.Cps = RealT(self, v=0.0, units="", desc="")
        self.gams = RealT(self, v=0.0, units="", desc="")
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

    def set_tp(self, tt, pt):
        if isinstance(tt, float):
            self.Tt.v = tt
        else:
            self.Tt.v = tt.v
        if isinstance(pt, float):
            self.Pt.v = pt
        else:
            self.Pt.v = pt.v
        if self.twoPhase == False:
            self.ht.v = GAS_MODELS[self.comp.v].h_tp(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.s.v = GAS_MODELS[self.comp.v].s_tp(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.rhot.v = GAS_MODELS[self.comp.v].rho(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.Rt.v = GAS_MODELS[self.comp.v].r(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.Cpt.v = GAS_MODELS[self.comp.v].cp(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.gamt.v = GAS_MODELS[self.comp.v].gam(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.mut.v = GAS_MODELS[self.comp.v].mu(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
        else:
            self.ht.v = GAS_MODELS[self.comp.v].h_tp(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.s.v = GAS_MODELS[self.comp.v].s_tp(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.rhot.v = GAS_MODELS[self.comp.v].rho(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.Rt.v = GAS_MODELS[self.comp.v].r(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.Cpt.v = GAS_MODELS[self.comp.v].cp(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.gamt.v = GAS_MODELS[self.comp.v].gam(
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

    def set_hp(self, ht, pt):
        if isinstance(ht, float):
            self.ht.v = ht
        else:
            self.ht.v = ht.v
        if isinstance(pt, float):
            self.Pt.v = pt
        else:
            self.Pt.v = pt.v
        if self.twoPhase == False:
            self.Tt.v = GAS_MODELS[self.comp.v].t_hp(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.s.v = GAS_MODELS[self.comp.v].s_tp(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.rhot.v = GAS_MODELS[self.comp.v].rho(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.Rt.v = GAS_MODELS[self.comp.v].r(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.gamt.v = GAS_MODELS[self.comp.v].gam(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.Cpt.v = GAS_MODELS[self.comp.v].cp(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.mut.v = GAS_MODELS[self.comp.v].mu(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
        else:
            self.Tt.v = GAS_MODELS[self.comp.v].t_hp(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.s.v = GAS_MODELS[self.comp.v].s_hp(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.rhot.v = GAS_MODELS[self.comp.v].rho(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.Rt.v = GAS_MODELS[self.comp.v].r(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.gamt.v = GAS_MODELS[self.comp.v].gam(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.Cpt.v = GAS_MODELS[self.comp.v].cp(
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

    def set_sp(self, s, pt):
        if isinstance(s, float):
            self.s.v = s
        else:
            self.s.v = s.v
        if isinstance(pt, float):
            self.Pt.v = pt
        else:
            self.Pt.v = pt.v
        if self.twoPhase == False:
            self.Tt.v = GAS_MODELS[self.comp.v].t_sp(
                self.s.v, self.Pt.v, self.FAR.v, self
            )
            self.ht.v = GAS_MODELS[self.comp.v].h_tp(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.rhot.v = GAS_MODELS[self.comp.v].rho(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.Rt.v = GAS_MODELS[self.comp.v].r(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.gamt.v = GAS_MODELS[self.comp.v].gam(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.Cpt.v = GAS_MODELS[self.comp.v].cp(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.mut.v = GAS_MODELS[self.comp.v].mu(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.Tt.v, self.Pt.v, self.FAR.v, self
            )
        else:
            self.Tt.v = GAS_MODELS[self.comp.v].t_sp(
                self.s.v, self.Pt.v, self.FAR.v, self
            )
            self.ht.v = GAS_MODELS[self.comp.v].h_sp(
                self.s.v, self.Pt.v, self.FAR.v, self
            )
            self.rhot.v = GAS_MODELS[self.comp.v].rho(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.Rt.v = GAS_MODELS[self.comp.v].r(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.gamt.v = GAS_MODELS[self.comp.v].gam(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.kt.v = GAS_MODELS[self.comp.v].k(
                self.ht.v, self.Pt.v, self.FAR.v, self
            )
            self.Cpt.v = GAS_MODELS[self.comp.v].cp(
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

    def set_ps(self, ps):
        self.ps.v = ps
        self.ps_calc()

    def statics(self):

        self.gams.v = self.gamt.v
        self.rhos.v = self.rhot.v

        if self.size.v == True:
            if self.MN.v == 0.0:
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
                g.errors = g.errors + "MN iteration failure\n"

            self.MN.v = mnor

        else:
            if self.A.v == 0:
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
                count = count + 1

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
                count = count + 1

            if count > 49:
                g.errors = (
                    self.parent.name1
                    + "."
                    + self.name1
                    + " "
                    + g.errors
                    + " failure during static area match\n"
                )

            self.A.v = aor

    def ps_calc(self):
        if self.twoPhase == False:
            self.Ts.v = GAS_MODELS[self.comp.v].t_sp(
                self.s.v, self.Ps.v, self.FAR.v, self
            )
            self.hs.v = GAS_MODELS[self.comp.v].h_tp(
                self.Ts.v, self.Ps.v, self.FAR.v, self
            )
            self.rhos.v = GAS_MODELS[self.comp.v].rho(
                self.Ts.v, self.Ps.v, self.FAR.v, self
            )
            self.Rs.v = GAS_MODELS[self.comp.v].r(
                self.Ts.v, self.Ps.v, self.FAR.v, self
            )
            self.Cps.v = GAS_MODELS[self.comp.v].cp(
                self.Ts.v, self.Ps.v, self.FAR.v, self
            )
            self.mus.v = GAS_MODELS[self.comp.v].mu(
                self.Ts.v, self.Ps.v, self.FAR.v, self
            )
            self.ks.v = GAS_MODELS[self.comp.v].k(
                self.Ts.v, self.Ps.v, self.FAR.v, self
            )
            self.gams.v = GAS_MODELS[self.comp.v].gam(
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
            self.Ts.v = GAS_MODELS[self.comp.v].t_sp(
                self.s.v, self.Ps.v, self.FAR.v, self
            )
            self.hs.v = GAS_MODELS[self.comp.v].h_sp(
                self.s.v, self.Ps.v, self.FAR.v, self
            )
            self.rhos.v = GAS_MODELS[self.comp.v].rho(
                self.hs.v, self.Ps.v, self.FAR.v, self
            )
            self.Rs.v = GAS_MODELS[self.comp.v].r(
                self.hs.v, self.Ps.v, self.FAR.v, self
            )
            self.Cps.v = GAS_MODELS[self.comp.v].cp(
                self.hs.v, self.Ps.v, self.FAR.v, self
            )
            self.mus.v = GAS_MODELS[self.comp.v].mu(
                self.hs.v, self.Ps.v, self.FAR.v, self
            )
            self.ks.v = GAS_MODELS[self.comp.v].k(
                self.hs.v, self.Ps.v, self.FAR.v, self
            )
            self.gams.v = GAS_MODELS[self.comp.v].gam(
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
        if e.MN.v != 0:
            self.MN.v = e.MN.v
        if e.A.v != 0:
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
            if e.MN.v != 0:
                self.MN.v = e.MN.v
            if e.A.v != 0:
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
            self.other.Rs.v = e.Rs.v
            self.other.s.v = e.s.v
            if e.MN.v != 0:
                self.other.MN.v = e.MN.v
            if e.A.v != 0:
                self.other.A.v = e.A.v
            self.other.V.v = e.V.v
            self.other.Ts.v = e.Ts.v
            self.other.Ps.v = e.Ps.v
            self.other.hs.v = e.hs.v
            self.other.rhos.v = e.rhos.v
            self.other.mus.v = e.mus.v
            self.other.ks.v = e.ks.v
            self.other.Cps.v = e.Cps.v
            self.other.gams.v = e.gams.v
            self.other.size.v = e.size.v

    def set_w(self, w):
        if isinstance(w, float):
            self.W.v = w
            if self.other != 0:
                self.other.W.v = w
        else:
            self.W.v = w.v
            if self.other != 0:
                self.other.W.v = w.v

    def set_ts_ps_mn(self, ts_i, ps_i, mach_i):
        ts = ts_i if isinstance(ts_i, float) else ts_i.v
        ps = ps_i if isinstance(ps_i, float) else ps_i.v
        mach = mach_i if isinstance(mach_i, float) else mach_i.v

        self.size.v = True
        self.MN.v = 0.0
        self.A.v = 0.0
        self.set_tp(ts, ps)

        s = self.s
        # TODO: do we need the Tt calculation here? It doesn't seem to be used
        # tt = ts * (1.0 + (self.gamt.v - 1.0) / 2.0 * mach**2.0)
        pt = ps * (1.0 + (self.gamt.v - 1.0) / 2.0 * mach**2.0) ** (
            (self.gamt.v - 1.0) / self.gamt.v
        )
        self.V.v = mach * math.sqrt(self.gamt.v * self.Rt.v * ts * 25037.0)
        ht = self.V.v**2.0 / 25037.0 / 2.0 + self.ht.v
        self.set_sp(s, pt)

        errorm1 = self.ht - ht

        xm1 = pt
        pt = self.Pt.v * 0.95
        self.set_sp(s, pt)
        error = self.ht - ht
        x = pt

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
            pt = x
            self.set_sp(s, pt)
            error = self.ht - ht
            i = i + 1

        self.size.v = True
        self.MN.v = mach
        self.statics()

    def dump(self):
        print(
            f"{self.parent.name1[:8]:10s} {self.name1[:8]:10s}  "
            f"W:{str(self.W.v)[:8]:10s}  Tt:{str(self.Tt.v)[:8]:10s}  "
            f"Pt:{str(self.Pt.v)[:8]:10s}  FAR:{str(self.FAR.v)[:8]:10s}  "
            f"MN:{str(self.MN.v)[:8]:10s}  Ts:{str(self.Ts.v)[:8]:10s}  "
            f"Ps:{str(self.Ps.v)[:8]:10s}",
            file=g.out,
        )

    def pretty(self):
        print(
            f"{self.parent.name1[:8]:10s} {self.name1[:8]:10s}  "
            f"W:{str(self.W.v)[:8]:10s}  Tt:{str(self.Tt.v)[:8]:10s}  "
            f"Pt:{str(self.Pt.v)[:8]:10s}  ht:{str(self.ht.v)[:8]:10s}  "
            f"FAR:{str(self.FAR.v)[:8]:10s}  MN:{str(self.MN.v)[:8]:10s}  "
            f"Ts:{str(self.Ts.v)[:8]:10s}  Ps:{str(self.Ps.v)[:8]:10s}",
            file=g.pretty,
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
