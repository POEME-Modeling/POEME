import CoolProp.CoolProp

fluid = "R134a"


class CPR134:
    @staticmethod
    def t_hp(ht, pt, fuel_air_ratio, p):
        return (
            CoolProp.PropsSI("T", "H", ht * 2326.0, "P", pt * 6894.76, fluid)
            * 9.0
            / 5.0
        )

    @staticmethod
    def t_sp(s, pt, fuel_air_ratio, p):
        return (
            CoolProp.PropsSI("T", "S", s / 0.0002388, "P", pt * 6894.76, fluid)
            * 9.0
            / 5.0
        )

    @staticmethod
    def h_tp(tt, pt, fuel_air_ratio, p):
        return (
            CoolProp.PropsSI("H", "T", tt * 5.0 / 9.0, "P", pt * 6894.76, fluid)
            / 2326.0
        )

    @staticmethod
    def h_sp(s, pt, fuel_air_ratio, p):
        return (
            CoolProp.PropsSI("H", "S", s / 0.0002388, "P", pt * 6894.76, fluid) / 2326.0
        )

    @staticmethod
    def h_qp(q, pt, fuel_air_ratio, p):
        return CoolProp.PropsSI("H", "Q", q, "P", pt * 6894.76, fluid) / 2326.0

    @staticmethod
    def tsat(pt, fuel_air_ratio, p):
        return CoolProp.PropsSI("T", "P", pt * 6894.76, "Q", 0.5, fluid) * 9.0 / 5.0

    @staticmethod
    def s_hp(ht, pt, fuel_air_ratio, p):
        return (
            CoolProp.PropsSI("S", "H", ht * 2326.0, "P", pt * 6894.76, fluid)
            * 0.0002388
        )

    @staticmethod
    def s_tp(tt, pt, fuel_air_ratio, p):
        return (
            CoolProp.PropsSI("S", "T", tt * 5.0 / 9.0, "P", pt * 6894.76, fluid)
            * 0.0002388
        )

    @staticmethod
    def rho(ht, pt, fuel_air_ratio, p):
        return (
            CoolProp.PropsSI("D", "H", ht * 2326.0, "P", pt * 6894.76, fluid)
            * 0.0624279606
        )

    @staticmethod
    def r(ht, pt, fuel_air_ratio, p):
        return 0.0

    @staticmethod
    def cp(ht, pt, fuel_air_ratio, p):
        return 0.0

    @staticmethod
    def gam(ht, pt, fuel_air_ratio, p):
        return 0.0

    @staticmethod
    def k(ht, pt, fuel_air_ratio, p):
        return 0.0

    @staticmethod
    def mu(ht, pt, fuel_air_ratio, p):
        return 0.0

    @staticmethod
    def q(ht, pt, fuel_air_ratio, p):
        return CoolProp.PropsSI("Q", "H", ht * 2326.0, "P", pt * 6894.76, fluid)
