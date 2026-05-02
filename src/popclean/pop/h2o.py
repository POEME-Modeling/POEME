class H2O:
    def __init__(self):
        pass

    @staticmethod
    def h_tp(temperature, pressure, fract):
        return temperature

    @staticmethod
    def s_tp(temperature, pressure, fract):
        temperature = temperature - 460.0
        return temperature / 200.0 * 0.28

    @staticmethod
    def t_hp(h, pressure, fract):
        return h

    @staticmethod
    def t_sp(s, pressure, fract):
        return s * 200.0 / 0.28 + 460

    @staticmethod
    def rho(temperature, pressure, fract):
        return 62.424 / 12.0**3.0

    @staticmethod
    def cp(temperature, pressure, fract):
        return 1.0

    @staticmethod
    def mu(temperature, pressure, fract):
        temperature = temperature - 460.0
        return (0.000006342 - 0.000037418) * (temperature - 32.0) / (
            200.0 - 32.0
        ) + 0.000037418

    @staticmethod
    def k(temperature, pressure, fract):
        temperature = temperature - 460.0
        return (
            (0.3987 - 0.3211) * (temperature - 32.0) / (200.0 - 32.0) + 0.3211
        ) / 3600.0
