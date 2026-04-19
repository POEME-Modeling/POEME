import CoolProp.CoolProp as CP

fluid = "R134a"


class CPR134:

    def T_hP(ht, Pt, FAR, p):
        return CP.PropsSI("T", "H", ht * 2326.0, "P", Pt * 6894.76, fluid) * 9.0 / 5.0

    def T_sP(s, Pt, FAR, p):
        return CP.PropsSI("T", "S", s / 0.0002388, "P", Pt * 6894.76, fluid) * 9.0 / 5.0

    def h_TP(Tt, Pt, FAR, p):
        return CP.PropsSI("H", "T", Tt * 5.0 / 9.0, "P", Pt * 6894.76, fluid) / 2326.0

    def h_SP(S, Pt, FAR, p):
        return CP.PropsSI("H", "S", S / 0.0002388, "P", Pt * 6894.76, fluid) / 2326.0

    def h_QP(Q, Pt, FAR, p):
        return CP.PropsSI("H", "Q", Q, "P", Pt * 6894.76, fluid) / 2326.0

    def Tsat(Pt, FAR, p):
        return CP.PropsSI("T", "P", Pt * 6894.76, "Q", 0.5, fluid) * 9.0 / 5.0

    def s_hP(ht, Pt, FAR, p):
        return CP.PropsSI("S", "H", ht * 2326.0, "P", Pt * 6894.76, fluid) * 0.0002388

    def s_TP(Tt, Pt, FAR, p):
        return (
            CP.PropsSI("S", "T", Tt * 5.0 / 9.0, "P", Pt * 6894.76, fluid) * 0.0002388
        )

    def rho(ht, Pt, FAR, p):
        return (
            CP.PropsSI("D", "H", ht * 2326.0, "P", Pt * 6894.76, fluid) * 0.0624279606
        )

    def R(ht, Pt, FAR, p):
        return 0.0

    def Cp(ht, Pt, FAR, p):
        return 0.0

    def gam(ht, Pt, FAR, p):
        return 0.0

    def k(ht, Pt, FAR, p):
        return 0.0

    def mu(ht, Pt, FAR, p):
        return 0.0

    def Q(ht, Pt, FAR, p):
        return CP.PropsSI("Q", "H", ht * 2326.0, "P", Pt * 6894.76, fluid)
