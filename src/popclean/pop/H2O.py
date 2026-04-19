class H2O:
    def __init__(self):
        pass

    def h_TP(T, P, fract):
        return T

    def s_TP(T, P, fract):
        T = T - 460.0
        return T / 200.0 * 0.28

    def T_hP(h, P, fract):
        return h

    def T_sP(s, P, fract):
        return s * 200.0 / 0.28 + 460

    def rho(T, P, fract):
        return 62.424 / 12.0**3.0

    def Cp(T, P, fract):
        return 1.0

    def mu(T, P, fract):
        T = T - 460.0
        return (0.000006342 - 0.000037418) * (T - 32.0) / (200.0 - 32.0) + 0.000037418

    def k(T, P, fract):
        T = T - 460.0
        return ((0.3987 - 0.3211) * (T - 32.0) / (200.0 - 32.0) + 0.3211) / 3600.0
