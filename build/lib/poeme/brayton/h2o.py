class H2O:
    def __init__(self):
        pass

    @staticmethod
    def h_TP(T, P, fract):
        return T

    @staticmethod
    def s_TP(T, P, fract):
        T = T - 460.0
        return T / 200.0 * 0.28

    @staticmethod
    def T_hp(h, P, fract):
        return h

    @staticmethod
    def T_sP(s, P, fract):
        return s * 200.0 / 0.28 + 460

    @staticmethod
    def rho(T, P, fract):
        return 62.424 / 12.0**3.0

    @staticmethod
    def Cp(T, P, fract):
        return 1.0

    @staticmethod
    def mu(T, P, fract):
        T = T - 460.0
        return (0.000006342 - 0.000037418) * (T - 32.0) / (200.0 - 32.0) + 0.000037418

    @staticmethod
    def k(T, P, fract):
        T = T - 460.0
        return ((0.3987 - 0.3211) * (T - 32.0) / (200.0 - 32.0) + 0.3211) / 3600.0
