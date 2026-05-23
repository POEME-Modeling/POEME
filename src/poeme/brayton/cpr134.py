from CoolProp import CoolProp

fluid = "R134a"


class CPR134:
    @staticmethod
    def T_hp(ht, Pt, FAR, p):
        return (
            CoolProp.PropsSI("T", "H", ht * 2326.0, "P", Pt * 6894.76, fluid)
            * 9.0
            / 5.0
        )

    @staticmethod
    def T_sP(s, Pt, FAR, p):
        return (
            CoolProp.PropsSI("T", "S", s / 0.0002388, "P", Pt * 6894.76, fluid)
            * 9.0
            / 5.0
        )

    @staticmethod
    def h_TP(Tt, Pt, FAR, p):
        return (
            CoolProp.PropsSI("H", "T", Tt * 5.0 / 9.0, "P", Pt * 6894.76, fluid)
            / 2326.0
        )

    @staticmethod
    def h_sp(s, Pt, FAR, p):
        return (
            CoolProp.PropsSI("H", "S", s / 0.0002388, "P", Pt * 6894.76, fluid) / 2326.0
        )

    @staticmethod
    def h_qp(q, Pt, FAR, p):
        return CoolProp.PropsSI("H", "Q", q, "P", Pt * 6894.76, fluid) / 2326.0

    @staticmethod
    def tsat(Pt, FAR, p):
        return CoolProp.PropsSI("T", "P", Pt * 6894.76, "Q", 0.5, fluid) * 9.0 / 5.0

    @staticmethod
    def s_hP(ht, Pt, FAR, p):
        return (
            CoolProp.PropsSI("S", "H", ht * 2326.0, "P", Pt * 6894.76, fluid)
            * 0.0002388
        )

    @staticmethod
    def s_TP(Tt, Pt, FAR, p):
        return (
            CoolProp.PropsSI("S", "T", Tt * 5.0 / 9.0, "P", Pt * 6894.76, fluid)
            * 0.0002388
        )

    @staticmethod
    def rho(ht, Pt, FAR, p):
        return (
            CoolProp.PropsSI("D", "H", ht * 2326.0, "P", Pt * 6894.76, fluid)
            * 0.0624279606
        )

    @staticmethod
    def R(ht, Pt, FAR, p):
        return 0.0

    @staticmethod
    def Cp(ht, Pt, FAR, p):
        return 0.0

    @staticmethod
    def gamma(ht, Pt, FAR, p):
        return 0.0

    @staticmethod
    def k(ht, Pt, FAR, p):
        return 0.0

    @staticmethod
    def mu(ht, Pt, FAR, p):
        return 0.0

    @staticmethod
    def q(ht, Pt, FAR, p):
        return CoolProp.PropsSI("Q", "H", ht * 2326.0, "P", Pt * 6894.76, fluid)
