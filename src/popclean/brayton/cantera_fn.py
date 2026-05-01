import cantera as ct

fuel_comp = {"C": 1.0, "H": 0.16667}
oxidizer_comp = {"O2": 0.233, "N2": 0.767}  # Mass fractions for dry air

gas = ct.Solution("gri30.yaml")
gasair = ct.Solution("air.yaml")

HC = 0.16087


class CanteraFN:
    g_fuel_air_ratio = -1.0

    @staticmethod
    def gam(temperature, pressure, fuel_air_ratio, p):
        if fuel_air_ratio < 0.00001:
            if (
                abs(gasair.T - temperature * 5.0 / 9) > 0.0001
                or abs(gasair.P - pressure * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - fuel_air_ratio) > 0.00001
            ):
                gasair.TP = temperature * 5.0 / 9.0, pressure * 6894.76
                gasair.equilibrate("TP")
            return gasair.cp / gasair.cv
        else:
            if (
                abs(gas.T - temperature * 5.0 / 9) > 0.0001
                or abs(gas.P - pressure * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - fuel_air_ratio) > 0.00001
            ):
                gas.set_mixture_fraction(
                    fuel_air_ratio / (1 - fuel_air_ratio),
                    fuel=fuel_comp,
                    oxidizer=oxidizer_comp,
                    basis="mass",
                )
                gas.TP = temperature * 5.0 / 9.0, pressure * 6894.76
                CanteraFN.g_fuel_air_ratio = fuel_air_ratio
                gas.equilibrate("TP")
            return gas.cp / gas.cv

    @staticmethod
    def rho(temperature, pressure, fuel_air_ratio, p):
        if fuel_air_ratio < 0.00001:
            if (
                abs(gasair.T - temperature * 5.0 / 9) > 0.0001
                or abs(gasair.P - pressure * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - fuel_air_ratio) > 0.00001
            ):
                gasair.TP = temperature * 5.0 / 9.0, pressure * 6894.76
                CanteraFN.g_fuel_air_ratio = fuel_air_ratio
                gasair.equilibrate("TP")
            return gasair.density * 0.062428
        else:
            if (
                abs(gas.T - temperature * 5.0 / 9) > 0.0001
                or abs(gas.P - pressure * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - fuel_air_ratio) > 0.00001
            ):
                gas.set_mixture_fraction(
                    fuel_air_ratio / (1 - fuel_air_ratio),
                    fuel=fuel_comp,
                    oxidizer=oxidizer_comp,
                    basis="mass",
                )
                gas.TP = temperature * 5.0 / 9.0, pressure * 6894.76
                CanteraFN.g_fuel_air_ratio = fuel_air_ratio
                gas.equilibrate("TP")
            return gas.density * 0.062428

    @staticmethod
    def cp(temperature, pressure, fuel_air_ratio, p):
        if fuel_air_ratio < 0.00001:
            if (
                abs(gasair.T - temperature * 5.0 / 9) > 0.0001
                or abs(gasair.P - pressure * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - fuel_air_ratio) > 0.00001
            ):
                gasair.TP = temperature * 5.0 / 9.0, pressure * 6894.76
                CanteraFN.g_fuel_air_ratio = fuel_air_ratio
                gasair.equilibrate("TP")
            return gasair.cp * 0.0002390057

        else:
            if (
                abs(gas.T - temperature * 5.0 / 9) > 0.0001
                or abs(gas.P - pressure * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - fuel_air_ratio) > 0.00001
            ):
                gas.set_mixture_fraction(
                    fuel_air_ratio / (1 - fuel_air_ratio),
                    fuel=fuel_comp,
                    oxidizer=oxidizer_comp,
                    basis="mass",
                )
                gas.TP = temperature * 5.0 / 9.0, pressure * 6894.76
                CanteraFN.g_fuel_air_ratio = fuel_air_ratio
                gas.equilibrate("TP")
            return gas.cp * 0.0002390057

    @staticmethod
    def h_tp(temperature, pressure, fuel_air_ratio, p):
        if fuel_air_ratio < 0.00001:
            if (
                abs(gasair.T - temperature * 5.0 / 9) > 0.0000001
                or abs(gasair.P - pressure * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - fuel_air_ratio) > 0.00001
            ):
                gasair.TP = temperature * 5.0 / 9.0, pressure * 6894.76
                CanteraFN.g_fuel_air_ratio = fuel_air_ratio
                gasair.equilibrate("TP")
            return gasair.h * 0.0004299226
        else:
            if (
                abs(gas.T - temperature * 5.0 / 9) > 0.0000001
                or abs(gas.P - pressure * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - fuel_air_ratio) > 0.00001
            ):
                gas.set_mixture_fraction(
                    fuel_air_ratio / (1 - fuel_air_ratio),
                    fuel=fuel_comp,
                    oxidizer=oxidizer_comp,
                    basis="mass",
                )
                gas.TP = temperature * 5.0 / 9.0, pressure * 6894.76
                CanteraFN.g_fuel_air_ratio = fuel_air_ratio
                gas.equilibrate("TP")
            return gas.h * 0.0004299226

    @staticmethod
    def s_tp(temperature, pressure, fuel_air_ratio, p):
        if fuel_air_ratio < 0.00001:
            if (
                abs(gasair.T - temperature * 5.0 / 9) > 0.0001
                or abs(gasair.P - pressure * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - fuel_air_ratio) > 0.00001
            ):
                gasair.TP = temperature * 5.0 / 9.0, pressure * 6894.76
                CanteraFN.g_fuel_air_ratio = fuel_air_ratio
                gasair.equilibrate("TP")

            return gasair.s * 0.0002390057
        else:
            if (
                abs(gas.T - temperature * 5.0 / 9) > 0.0001
                or abs(gas.P - pressure * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - fuel_air_ratio) > 0.00001
            ):
                gas.set_mixture_fraction(
                    fuel_air_ratio / (1 - fuel_air_ratio),
                    fuel=fuel_comp,
                    oxidizer=oxidizer_comp,
                    basis="mass",
                )
                gas.TP = temperature * 5.0 / 9.0, pressure * 6894.76
                CanteraFN.g_fuel_air_ratio = fuel_air_ratio
                gas.equilibrate("TP")
            return gas.s * 0.0002390057

    @staticmethod
    def r(temperature, pressure, fuel_air_ratio, p):
        if fuel_air_ratio < 0.00001:
            if (
                abs(gasair.T - temperature * 5.0 / 9) > 0.0001
                or abs(gasair.P - pressure * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - fuel_air_ratio) > 0.00001
            ):
                gasair.TP = temperature * 5.0 / 9.0, pressure * 6894.76
                CanteraFN.g_fuel_air_ratio = fuel_air_ratio
                gasair.equilibrate("TP")
            return 8.314 / gasair.mean_molecular_weight * 0.0002390057 * 1000.0
        else:
            if (
                abs(gas.T - temperature * 5.0 / 9) > 0.0001
                or abs(gas.P - pressure * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - fuel_air_ratio) > 0.00001
            ):
                gas.set_mixture_fraction(
                    fuel_air_ratio / (1 - fuel_air_ratio),
                    fuel=fuel_comp,
                    oxidizer=oxidizer_comp,
                    basis="mass",
                )
                gas.TP = temperature * 5.0 / 9.0, pressure * 6894.76
                CanteraFN.g_fuel_air_ratio = fuel_air_ratio
                gas.equilibrate("TP")
            return 8.314 / gas.mean_molecular_weight * 0.0002390057 * 1000.0

    @staticmethod
    def mu(temperature, pressure, fuel_air_ratio, p):
        return 0

    @staticmethod
    def k(temperature, pressure, fuel_air_ratio, p):
        return 0

    @staticmethod
    def t_sp(s, pressure, fuel_air_ratio, p):
        if fuel_air_ratio < 0.00001:
            if (
                abs(gasair.s - s / 0.0002390057) > 0.0001
                or abs(gasair.P - pressure * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - fuel_air_ratio) > 0.00001
            ):
                gasair.SP = s / 0.0002390057, pressure * 6894.76
                CanteraFN.g_fuel_air_ratio = fuel_air_ratio
                gasair.equilibrate("SP")
            return gasair.T * 9.0 / 5.0
        else:
            if (
                abs(gas.s - s / 0.0002390057) > 0.0001
                or abs(gas.P - pressure * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - fuel_air_ratio) > 0.00001
            ):
                gas.set_mixture_fraction(
                    fuel_air_ratio / (1 - fuel_air_ratio),
                    fuel=fuel_comp,
                    oxidizer=oxidizer_comp,
                    basis="mass",
                )
                gas.SP = s / 0.0002390057, pressure * 6894.76
                CanteraFN.g_fuel_air_ratio = fuel_air_ratio
                gas.equilibrate("SP")
            return gas.T * 9.0 / 5.0

    @staticmethod
    def t_hp(h, pressure, fuel_air_ratio, p):
        temperature = 1500
        hcalc = CanteraFN.h_TP(temperature, pressure, fuel_air_ratio, p)
        errorm1 = (hcalc - h) / h
        xm1 = temperature
        temperature = temperature * 0.95
        hcalc = CanteraFN.h_TP(temperature, pressure, fuel_air_ratio, p)
        error = (hcalc - h) / h
        x = temperature

        while abs(error) > 0.000001:
            xp1 = x - error * (x - xm1) / (error - errorm1)
            if xp1 - x > 0.3 * temperature:
                xp1 = x + 0.3 * temperature
            if xp1 - x < -0.3 * temperature:
                xp1 = x - 0.3 * temperature
            xm1 = x
            errorm1 = error
            x = xp1
            temperature = x
            hcalc = CanteraFN.h_TP(temperature, pressure, fuel_air_ratio, p)
            error = (hcalc - h) / h

        return temperature

    @staticmethod
    def p_hs(h, s, fuel_air_ratio, pressure):
        temperature = CanteraFN.T_sP(s, pressure, fuel_air_ratio)

        hcalc = CanteraFN.h_TP(temperature, pressure, fuel_air_ratio, p)
        errorm1 = (hcalc - h) / h
        xm1 = pressure
        pressure = pressure * 0.95
        temperature = CanteraFN.T_sP(s, pressure, fuel_air_ratio)
        hcalc = CanteraFN.h_TP(temperature, pressure, fuel_air_ratio, p)
        error = (hcalc - h) / h
        x = pressure

        while abs(error) > 0.000001:
            xp1 = x - error * (x - xm1) / (error - errorm1)
            if xp1 - x > 0.1 * pressure:
                xp1 = x + 0.1 * pressure
            if xp1 - x < -0.1 * pressure:
                xp1 = x - 0.1 * pressure
            xm1 = x
            errorm1 = error
            x = xp1
            pressure = x
            temperature = CanteraFN.T_sP(s, pressure, fuel_air_ratio)
            hcalc = CanteraFN.h_TP(temperature, pressure, fuel_air_ratio)
            error = (hcalc - h) / h

        return pressure
