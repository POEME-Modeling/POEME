from CoolProp import CoolProp


class R32:
    @staticmethod
    def rho(T, P, FAR, p):
        return (
            CoolProp.PropsSI("D", "T", T * 5.0 / 9.0, "P", P * 6894.76, "R32")
            * 0.062428
        )

    @staticmethod
    def Cp(T, P, FAR, p):
        # return CoolProp.PropsSI("D", "T", T, "P", P, "R32")
        return 0.0

    @staticmethod
    def k(T, P, FAR, p):
        # return CoolProp.PropsSI("D", "T", T, "P", P, "R32")
        return 0.0

    @staticmethod
    def mu(T, P, FAR, p):
        # return CoolProp.PropsSI("D", "T", T, "P", P, "R32")
        return 0.0

    @staticmethod
    def gamma(T, P, FAR, p):
        # return CoolProp.PropsSI("D", "T", T, "P", P, "R32")
        return 0.0

    @staticmethod
    def h_TP(T, P, FAR, p):
        return (
            CoolProp.PropsSI("H", "T", T * 5.0 / 9.0, "P", P * 6894.76, "R32")
            * 0.4299226
        )

    @staticmethod
    def T_hp(h, P, FAR, p):
        return (
            CoolProp.PropsSI("T", "H", h / 0.4299226, "P", P * 6894.76, "R32")
            * 9.0
            / 5.0
        )

    @staticmethod
    def T_sP(s, P, FAR, p):
        return (
            CoolProp.PropsSI("T", "S", s / 0.2388459, "P", P * 6894.76, "R32")
            * 9.0
            / 5.0
        )

    @staticmethod
    def s_TP(T, P, FAR, p):
        return (
            CoolProp.PropsSI("S", "T", T * 5.0 / 9.0, "P", P * 6894.76, "R32")
            * 0.2388459
        )

    @staticmethod
    def R(T, P, FAR, p):
        # return CoolProp.PropsSI("D", "T", T, "P", P*, "R32")
        return 0.0
