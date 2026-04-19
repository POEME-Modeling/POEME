from RealT import RealT
from ValueT import ValueT
import math
from Atom import Atom
import g

from H2O import H2O
from R32 import R32
from CPR134 import CPR134
from R134 import R134
from air4 import air4
from air6 import air6
from canteraFN import canteraFN
from RealT import RealT
from StringT import StringT
from BooleanT import BooleanT
from newtherm import newtherm


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
            p.addVID(self)

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

    def addVID(f, v):
        f.VIDL.append(v)

    def isa(f, type):
        if type == "FN":
            return True
        else:
            return False

    def setW(f, W):
        if isinstance(W, float):
            f.W.v = W
        else:
            f.W.v = W.v
        if f.other != 0:
            f.other.W.v = f.W.v

    def add(f, o):
        f.ht.v = (f.ht.v * f.W.v + o.ht.v * o.W.v) / (f.W.v + o.W.v)
        FARt = f.FAR.v
        f.FAR.v = (
            f.W.v * f.FAR.v / (1.0 + f.FAR.v + f.WAR.v)
            + o.W.v * o.FAR.v / (1.0 + o.FAR.v + o.WAR.v)
        ) / (f.W.v / (1.0 + f.FAR.v + f.WAR.v) + o.W.v / (1.0 + o.FAR.v + o.WAR.v))
        f.WAR.v = (
            f.W.v * f.WAR.v / (1.0 + FARt + f.WAR.v)
            + o.W.v * o.WAR.v / (1.0 + o.FAR.v + o.WAR.v)
        ) / (f.W.v / (1.0 + FARt + f.WAR.v) + o.W.v / (1.0 + o.FAR.v + o.WAR.v))
        f.W.v = f.W.v + o.W.v
        f.set_hP(f.ht.v, f.Pt.v)

    def setTP(f, Tt, Pt):
        if isinstance(Tt, float):
            f.Tt.v = Tt
        else:
            f.Tt.v = Tt.v
        if isinstance(Pt, float):
            f.Pt.v = Pt
        else:
            f.Pt.v = Pt.v
        if f.twoPhase == False:
            f.ht.v = eval(f.comp.v).h_TP(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.s.v = eval(f.comp.v).s_TP(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.rhot.v = eval(f.comp.v).rho(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.Rt.v = eval(f.comp.v).R(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.Cpt.v = eval(f.comp.v).Cp(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.gamt.v = eval(f.comp.v).gam(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.kt.v = eval(f.comp.v).k(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.mut.v = eval(f.comp.v).mu(f.Tt.v, f.Pt.v, f.FAR.v, f)
        else:
            f.ht.v = eval(f.comp.v).h_TP(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.s.v = eval(f.comp.v).s_TP(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.rhot.v = eval(f.comp.v).rho(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.Rt.v = eval(f.comp.v).R(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.Cpt.v = eval(f.comp.v).Cp(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.gamt.v = eval(f.comp.v).gam(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.kt.v = eval(f.comp.v).k(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.mut.v = eval(f.comp.v).mu(f.ht.v, f.Pt.v, f.FAR.v, f)
        f.statics()
        if f.other != 0:
            f.other.copyDeep(f)

    def set_hP(f, ht, Pt):
        if isinstance(ht, float):
            f.ht.v = ht
        else:
            f.ht.v = ht.v
        if isinstance(Pt, float):
            f.Pt.v = Pt
        else:
            f.Pt.v = Pt.v
        if f.twoPhase == False:
            f.Tt.v = eval(f.comp.v).T_hP(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.s.v = eval(f.comp.v).s_TP(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.rhot.v = eval(f.comp.v).rho(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.Rt.v = eval(f.comp.v).R(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.gamt.v = eval(f.comp.v).gam(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.kt.v = eval(f.comp.v).k(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.Cpt.v = eval(f.comp.v).Cp(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.mut.v = eval(f.comp.v).mu(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.kt.v = eval(f.comp.v).k(f.Tt.v, f.Pt.v, f.FAR.v, f)
        else:
            f.Tt.v = eval(f.comp.v).T_hP(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.s.v = eval(f.comp.v).s_hP(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.rhot.v = eval(f.comp.v).rho(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.Rt.v = eval(f.comp.v).R(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.gamt.v = eval(f.comp.v).gam(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.kt.v = eval(f.comp.v).k(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.Cpt.v = eval(f.comp.v).Cp(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.mut.v = eval(f.comp.v).mu(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.kt.v = eval(f.comp.v).k(f.ht.v, f.Pt.v, f.FAR.v, f)

        f.statics()
        if f.other != 0:
            f.other.copyDeep(f)

    def set_sP(f, s, Pt):
        if isinstance(s, float):
            f.s.v = s
        else:
            f.s.v = s.v
        if isinstance(Pt, float):
            f.Pt.v = Pt
        else:
            f.Pt.v = Pt.v
        if f.twoPhase == False:
            f.Tt.v = eval(f.comp.v).T_sP(f.s.v, f.Pt.v, f.FAR.v, f)
            f.ht.v = eval(f.comp.v).h_TP(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.rhot.v = eval(f.comp.v).rho(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.Rt.v = eval(f.comp.v).R(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.gamt.v = eval(f.comp.v).gam(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.kt.v = eval(f.comp.v).k(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.Cpt.v = eval(f.comp.v).Cp(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.mut.v = eval(f.comp.v).mu(f.Tt.v, f.Pt.v, f.FAR.v, f)
            f.kt.v = eval(f.comp.v).k(f.Tt.v, f.Pt.v, f.FAR.v, f)
        else:
            f.Tt.v = eval(f.comp.v).T_sP(f.s.v, f.Pt.v, f.FAR.v, f)
            f.ht.v = eval(f.comp.v).h_SP(f.s.v, f.Pt.v, f.FAR.v, f)
            f.rhot.v = eval(f.comp.v).rho(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.Rt.v = eval(f.comp.v).R(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.gamt.v = eval(f.comp.v).gam(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.kt.v = eval(f.comp.v).k(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.Cpt.v = eval(f.comp.v).Cp(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.mut.v = eval(f.comp.v).mu(f.ht.v, f.Pt.v, f.FAR.v, f)
            f.kt.v = eval(f.comp.v).k(f.ht.v, f.Pt.v, f.FAR.v, f)
        f.statics()
        if f.other != 0:
            f.other.copyDeep(f)

    def set_hs(f, h, s):
        if isinstance(h, float):
            f.ht.v = h
        else:
            f.ht.v = j.v
        if isinstance(s, float):
            f.s.v = s
        else:
            f.s.v = s.v

        f.Pt.v = eval(f.comp.v).P_hs(f.ht.v, f.s.v, f.FAR.v, f)
        f.set_sP(f.s.v, f.Pt.v)

    def setPs(f, Ps):
        f.Ps.v = Ps
        f.PsCalc()

    def statics(f):

        f.gams.v = f.gamt.v
        f.rhos.v = f.rhot.v

        if f.size.v == True:

            if f.MN.v == 0.0:
                return
            MNor = f.MN.v
            f.Ps.v = f.Pt.v * 0.9
            f.PsCalc()
            errorm1 = 0
            xm1 = 0
            f.Ps.v = f.Ps.v * 0.95
            f.PsCalc()

            error = (f.MN.v - MNor) / MNor
            x = f.Ps.v
            count = 0
            while abs(error) > 0.00001 and count < 50:
                count = count + 1
                xp1 = x - error * (x - xm1) / (error - errorm1)
                if xp1 - x > 0.1 * f.Pt.v:
                    xp1 = x + 0.1 * f.Pt.v
                if xp1 - x < -0.1 * f.Pt.v:
                    xp1 = x - 0.1 * f.Pt.v
                xm1 = x
                errorm1 = error
                x = xp1
                f.Ps.v = x

                f.PsCalc()

                error = (f.MN.v - MNor) / MNor

            if count > 49:
                g.errors = g.errors + "MN iteration failure\n"

            f.MN.v = MNor

        else:

            if f.A.v == 0:
                return
            Aor = f.A.v
            f.Ps.v = f.Pt.v * 0.99
            f.PsCalc()
            errorm1 = (f.A.v - Aor) / Aor
            xm1 = f.MN.v
            f.Ps.v = f.Ps.v * 0.95
            f.PsCalc()
            error = (f.A.v - Aor) / Aor
            x = f.Ps.v

            count = 0
            while abs(error) > 0.00001 and count < 50:
                count = count + 1

                xp1 = x - error * (x - xm1) / (error - errorm1)

                if xp1 - x > 0.1 * x:
                    xp1 = x + 0.1 * x
                if xp1 - x < -0.1 * x:
                    xp1 = x - 0.1 * x
                xm1 = x
                if xp1 > f.Pt.v * 0.99:
                    xp1 = f.Pt.v * 0.99

                errorm1 = error
                x = xp1
                f.Ps.v = x
                f.PsCalc()
                # print( f.Ps.v, f.A.v, Aor, f.MN.v )
                error = (f.A.v - Aor) / Aor
                count = count + 1

            if count > 49:
                g.errors = (
                    f.parent.name1
                    + "."
                    + f.name1
                    + " "
                    + g.errors
                    + " failure during static area match\n"
                )

            f.A.v = Aor

    def PsCalc(f):
        if f.twoPhase == False:
            f.Ts.v = eval(f.comp.v).T_sP(f.s.v, f.Ps.v, f.FAR.v, f)
            f.hs.v = eval(f.comp.v).h_TP(f.Ts.v, f.Ps.v, f.FAR.v, f)
            f.rhos.v = eval(f.comp.v).rho(f.Ts.v, f.Ps.v, f.FAR.v, f)
            f.Rs.v = eval(f.comp.v).R(f.Ts.v, f.Ps.v, f.FAR.v, f)
            f.Cps.v = eval(f.comp.v).Cp(f.Ts.v, f.Ps.v, f.FAR.v, f)
            f.mus.v = eval(f.comp.v).mu(f.Ts.v, f.Ps.v, f.FAR.v, f)
            f.ks.v = eval(f.comp.v).k(f.Ts.v, f.Ps.v, f.FAR.v, f)
            f.gams.v = eval(f.comp.v).gam(f.Ts.v, f.Ps.v, f.FAR.v, f)
            f.V.v = (
                math.sqrt(2 * abs(f.ht.v - f.hs.v) * 25037.0)
                * abs(f.ht.v - f.hs.v)
                / (f.ht.v - f.hs.v)
            )
            f.MN.v = (
                f.V.v
                / math.sqrt(f.gams.v * f.Rs.v * f.Ts.v * 25037.0)
                * abs(f.ht.v - f.hs.v)
                / (f.ht.v - f.hs.v)
            )
            f.A.v = f.W.v / (f.rhos.v * abs(f.V.v))
        else:
            f.Ts.v = eval(f.comp.v).T_sP(f.s.v, f.Ps.v, f.FAR.v, f)
            f.hs.v = eval(f.comp.v).h_SP(f.s.v, f.Ps.v, f.FAR.v, f)
            f.rhos.v = eval(f.comp.v).rho(f.hs.v, f.Ps.v, f.FAR.v, f)
            f.Rs.v = eval(f.comp.v).R(f.hs.v, f.Ps.v, f.FAR.v, f)
            f.Cps.v = eval(f.comp.v).Cp(f.hs.v, f.Ps.v, f.FAR.v, f)
            f.mus.v = eval(f.comp.v).mu(f.hs.v, f.Ps.v, f.FAR.v, f)
            f.ks.v = eval(f.comp.v).k(f.hs.v, f.Ps.v, f.FAR.v, f)
            f.gams.v = eval(f.comp.v).gam(f.hs.v, f.Ps.v, f.FAR.v, f)
            f.V.v = (
                math.sqrt(2 * abs(f.ht.v - f.hs.v) * 25037.0)
                * abs(f.ht.v - f.hs.v)
                / (f.ht.v - f.hs.v)
            )
            f.MN.v = (
                f.V.v
                / math.sqrt(f.gams.v * f.Rs.v * f.Ts.v * 25037.0)
                * abs(f.ht.v - f.hs.v)
                / (f.ht.v - f.hs.v)
            )
            f.A.v = f.W.v / (f.rhos.v * abs(f.V.v))

    def isa(m, type):
        if type == "FN":
            return True
        else:
            return False

    def linkFN(self, FN):
        self.__dict__.update({"other": FN})
        FN.__dict__.update({"other": self})

    def copy(f, e):
        f.comp.v = e.comp.v
        f.twoPhase.v = e.twoPhase.v
        f.FAR.v = e.FAR.v
        f.W.v = e.W.v
        f.Tt.v = e.Tt.v
        f.Pt.v = e.Pt.v
        f.ht.v = e.ht.v
        f.rhot.v = e.rhot.v
        f.mut.v = e.mut.v
        f.kt.v = e.kt.v
        f.Cpt.v = e.Cpt.v
        f.gamt.v = e.gamt.v
        f.Rt.v = e.Rt.v
        f.s.v = e.s.v
        if f.other != 0:
            f.other.comp.v = e.comp.v
            f.other.FAR.v = e.FAR.v
            f.other.W.v = e.W.v
            f.other.Tt.v = e.Tt.v
            f.other.Pt.v = e.Pt.v
            f.other.ht.v = e.ht.v
            f.other.rhot.v = e.rhot.v
            f.other.mut.v = e.mut.v
            f.other.kt.v = e.kt.v
            f.other.Cpt.v = e.Cpt.v
            f.other.gamt.v = e.gamt.v
            f.other.Rt.v = e.Rt.v
            f.other.s.v = e.s.v

    def copyDeep(f, e):
        f.twoPhase.v = e.twoPhase.v
        f.comp.v = e.comp.v
        f.FAR.v = e.FAR.v
        f.W.v = e.W.v
        f.Tt.v = e.Tt.v
        f.Pt.v = e.Pt.v
        f.ht.v = e.ht.v
        f.rhot.v = e.rhot.v
        f.mut.v = e.mut.v
        f.kt.v = e.kt.v
        f.Cpt.v = e.Cpt.v
        f.gamt.v = e.gamt.v
        f.Rt.v = e.Rt.v
        f.Rs.v = e.Rs.v
        f.s.v = e.s.v
        if e.MN.v != 0:
            f.MN.v = e.MN.v
        if e.A.v != 0:
            f.A.v = e.A.v
        f.V.v = e.V.v
        f.Ts.v = e.Ts.v
        f.Ps.v = e.Ps.v
        f.hs.v = e.hs.v
        f.rhos.v = e.rhos.v
        f.mus.v = e.mus.v
        f.ks.v = e.ks.v
        f.Cps.v = e.Cps.v
        f.gams.v = e.gams.v
        f.size.v = e.size.v
        if f.other != 0:
            f.comp.v = e.comp.v
            f.FAR.v = e.FAR.v
            f.W.v = e.W.v
            f.Tt.v = e.Tt.v
            f.Pt.v = e.Pt.v
            f.ht.v = e.ht.v
            f.rhot.v = e.rhot.v
            f.mut.v = e.mut.v
            f.kt.v = e.kt.v
            f.Cpt.v = e.Cpt.v
            f.gamt.v = e.gamt.v
            f.Rt.v = e.Rt.v
            f.Rs.v = e.Rs.v
            f.s.v = e.s.v
            if e.MN.v != 0:
                f.MN.v = e.MN.v
            if e.A.v != 0:
                f.A.v = e.A.v
            f.V.v = e.V.v
            f.Ts.v = e.Ts.v
            f.Ps.v = e.Ps.v
            f.hs.v = e.hs.v
            f.rhos.v = e.rhos.v
            f.mus.v = e.mus.v
            f.ks.v = e.ks.v
            f.Cps.v = e.Cps.v
            f.gams.v = e.gams.v
            f.size.v = e.size.v

        if f.other != 0:
            f.other.comp.v = e.comp.v
            f.other.FAR.v = e.FAR.v
            f.other.W.v = e.W.v
            f.other.Tt.v = e.Tt.v
            f.other.Pt.v = e.Pt.v
            f.other.ht.v = e.ht.v
            f.other.rhot.v = e.rhot.v
            f.other.mut.v = e.mut.v
            f.other.kt.v = e.kt.v
            f.other.Cpt.v = e.Cpt.v
            f.other.gamt.v = e.gamt.v
            f.other.Rt.v = e.Rt.v
            f.other.Rs.v = e.Rs.v
            f.other.s.v = e.s.v
            if e.MN.v != 0:
                f.other.MN.v = e.MN.v
            if e.A.v != 0:
                f.other.A.v = e.A.v
            f.other.V.v = e.V.v
            f.other.Ts.v = e.Ts.v
            f.other.Ps.v = e.Ps.v
            f.other.hs.v = e.hs.v
            f.other.rhos.v = e.rhos.v
            f.other.mus.v = e.mus.v
            f.other.ks.v = e.ks.v
            f.other.Cps.v = e.Cps.v
            f.other.gams.v = e.gams.v
            f.other.size.v = e.size.v

    def setW(f, W):
        if isinstance(W, float):
            f.W.v = W
            if f.other != 0:
                f.other.W.v = W
        else:
            f.W.v = W.v
            if f.other != 0:
                f.other.W.v = W.v

    def setTsPsMN(f, Tsi, Psi, MNi):
        if isinstance(Tsi, float):
            Ts = Tsi
        else:
            Ts = Tsi.v
        if isinstance(Psi, float):
            Ps = Psi
        else:
            Ps = Psi.v
        if isinstance(MNi, float):
            MN = MNi
        else:
            MN = MNi.v

        f.size.v = True
        f.MN.v = 0.0
        f.A.v = 0.0
        f.setTP(Ts, Ps)

        s = f.s
        Tt = Ts * (1.0 + (f.gamt.v - 1.0) / 2.0 * MN**2.0)
        Pt = Ps * (1.0 + (f.gamt.v - 1.0) / 2.0 * MN**2.0) ** (
            (f.gamt.v - 1.0) / f.gamt.v
        )
        f.V.v = MN * math.sqrt(f.gamt.v * f.Rt.v * Ts * 25037.0)
        ht = f.V.v**2.0 / 25037.0 / 2.0 + f.ht.v
        f.set_sP(s, Pt)

        errorm1 = f.ht - ht

        xm1 = Pt
        Pt = f.Pt.v * 0.95
        f.set_sP(s, Pt)
        error = f.ht - ht
        x = Pt

        i = 0
        count = 0
        while abs(error) > 0.00001 and count < 50:
            count = count + 1
            xp1 = x - error * (x - xm1) / (error - errorm1)
            if xp1 - x > 0.05 * f.Pt.v:
                xp1 = x + 0.05 * f.Pt.v
            if xp1 - x < -0.05 * f.Pt.v:
                xp1 = x - 0.05 * f.Pt.v
            xm1 = x
            errorm1 = error
            x = xp1
            Pt = x
            f.set_sP(s, Pt)
            error = f.ht - ht
            i = i + 1

        f.size.v = True
        f.MN.v = MN
        f.statics()

    def dump(f):
        print(
            f"{f.parent.name1[:8]:10s} {f.name1[:8]:10s}  W:{str(f.W.v)[:8]:10s}  Tt:{str(f.Tt.v)[:8]:10s}  Pt:{str(f.Pt.v)[:8]:10s}  FAR:{str(f.FAR.v)[:8]:10s}  MN:{str(f.MN.v)[:8]:10s}  Ts:{str(f.Ts.v)[:8]:10s}  Ps:{str(f.Ps.v)[:8]:10s}",
            file=g.out,
        )

    def pretty(f):
        print(
            f"{f.parent.name1[:8]:10s} {f.name1[:8]:10s}  W:{str(f.W.v)[:8]:10s}  Tt:{str(f.Tt.v)[:8]:10s}  Pt:{str(f.Pt.v)[:8]:10s}  ht:{str(f.ht.v)[:8]:10s}  FAR:{str(f.FAR.v)[:8]:10s}  MN:{str(f.MN.v)[:8]:10s}  Ts:{str(f.Ts.v)[:8]:10s}  Ps:{str(f.Ps.v)[:8]:10s}",
            file=g.pretty,
        )

    def hover(f):
        return (
            f.parent.name1
            + " "
            + f.name1
            + " "
            + str(f.W.v)
            + " "
            + str(f.Tt.v)
            + " "
            + str(f.Pt.v)
            + " "
            + str(f.FAR.v)
        )

    def savePrint(self):
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
