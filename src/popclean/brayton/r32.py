from CoolProp import CoolProp


class R32:
    @staticmethod
    def rho(temperature, pressure, fuel_air_ratio, p):
        return (
            CoolProp.PropsSI(
                "D", "T", temperature * 5.0 / 9.0, "P", pressure * 6894.76, "R32"
            )
            * 0.062428
        )

    @staticmethod
    def cp(temperature, pressure, fuel_air_ratio, p):
        # return CoolProp.PropsSI("D", "T", T, "P", P, "R32")
        return 0.0

    @staticmethod
    def k(temperature, pressure, fuel_air_ratio, p):
        # return CoolProp.PropsSI("D", "T", T, "P", P, "R32")
        return 0.0

    @staticmethod
    def mu(temperature, pressure, fuel_air_ratio, p):
        # return CoolProp.PropsSI("D", "T", T, "P", P, "R32")
        return 0.0

    @staticmethod
    def gamma(temperature, pressure, fuel_air_ratio, p):
        # return CoolProp.PropsSI("D", "T", T, "P", P, "R32")
        return 0.0

    @staticmethod
    def h_tp(temperature, pressure, fuel_air_ratio, p):
        return (
            CoolProp.PropsSI(
                "H", "T", temperature * 5.0 / 9.0, "P", pressure * 6894.76, "R32"
            )
            * 0.4299226
        )

    @staticmethod
    def t_hp(h, pressure, fuel_air_ratio, p):
        return (
            CoolProp.PropsSI("T", "H", h / 0.4299226, "P", pressure * 6894.76, "R32")
            * 9.0
            / 5.0
        )

    @staticmethod
    def t_sp(s, pressure, fuel_air_ratio, p):
        return (
            CoolProp.PropsSI("T", "S", s / 0.2388459, "P", pressure * 6894.76, "R32")
            * 9.0
            / 5.0
        )

    @staticmethod
    def s_tp(temperature, pressure, fuel_air_ratio, p):
        return (
            CoolProp.PropsSI(
                "S", "T", temperature * 5.0 / 9.0, "P", pressure * 6894.76, "R32"
            )
            * 0.2388459
        )

    @staticmethod
    def r(temperature, pressure, fuel_air_ratio, p):
        # return CoolProp.PropsSI("D", "T", T, "P", P*, "R32")
        return 0.0
