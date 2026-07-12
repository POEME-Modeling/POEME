import cantera as ct

fuel_comp = {"C": 1.0, "H": 0.16667}
oxidizer_comp = {"N2": 0.78, "O2": 0.21, "Ar": 0.01}  # Mass fractions for dry air

gas = ct.Solution("gri30.yaml")
gasair = ct.Solution("air.yaml")
# gasair = ct.Solution("custom_air.yaml", name="custom_air")

HC = 0.16087


class CanteraFN:
    """Cantera-based thermodynamic property evaluation.

    Provides thermodynamic properties of air and fuel-air mixtures as a
    function of temperature (T), pressure (P), and fuel-air ratio (FAR)
    using the Cantera library for equilibrium calculations. Internal unit
    conversions: R to K via T * 5/9, Pa to psi via P * 6894.76. Output
    conversions: density to lbm/ft³ via * 0.062428, enthalpy to BTU/lbm
    via * 0.4299226, entropy to BTU/(lbm·R) via * 0.2388459.

    Parameters
    ----------
    T : float
        Temperature (R).
    P : float
        Pressure (Pa).
    FAR : float
        Fuel-air ratio (dimensionless).
    p : object
        Session or context object passed to methods.

    Attributes
    ----------
    g_fuel_air_ratio : float
        Cached fuel-air ratio for Cantera solution state.
    """

    g_fuel_air_ratio = -1.0

    @staticmethod
    def gamma(T, P, FAR, p):
        """Heat capacity ratio (gamma = Cp/Cv).

        Parameters
        ----------
        T : float
            Temperature (R).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (dimensionless).
        p : object
            Session or context object.

        Returns
        -------
        float
            Heat capacity ratio.
        """
        if FAR < 0.00001:
            if (
                abs(gasair.T - T * 5.0 / 9) > 0.0001
                or abs(gasair.P - P * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - FAR) > 0.00001
            ):
                gasair.TP = T * 5.0 / 9.0, P * 6894.76
                gasair.equilibrate("TP")
            return gasair.cp / gasair.cv
        else:
            if (
                abs(gas.T - T * 5.0 / 9) > 0.0001
                or abs(gas.P - P * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - FAR) > 0.00001
            ):
                gas.set_mixture_fraction(
                    FAR / (1 - FAR),
                    fuel=fuel_comp,
                    oxidizer=oxidizer_comp,
                    basis="mass",
                )
                gas.TP = T * 5.0 / 9.0, P * 6894.76
                CanteraFN.g_fuel_air_ratio = FAR
                gas.equilibrate("TP")
            return gas.cp / gas.cv

    @staticmethod
    def rho(T, P, FAR, p):
        """Density.

        Parameters
        ----------
        T : float
            Temperature (R).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (dimensionless).
        p : object
            Session or context object.

        Returns
        -------
        float
            Density (lbm/ft³).
        """
        if FAR < 0.00001:
            if (
                abs(gasair.T - T * 5.0 / 9) > 0.0001
                or abs(gasair.P - P * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - FAR) > 0.00001
            ):
                gasair.TP = T * 5.0 / 9.0, P * 6894.76
                CanteraFN.g_fuel_air_ratio = FAR
                gasair.equilibrate("TP")
            return gasair.density * 0.062428
        else:
            if (
                abs(gas.T - T * 5.0 / 9) > 0.0001
                or abs(gas.P - P * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - FAR) > 0.00001
            ):
                gas.set_mixture_fraction(
                    FAR / (1 - FAR),
                    fuel=fuel_comp,
                    oxidizer=oxidizer_comp,
                    basis="mass",
                )
                gas.TP = T * 5.0 / 9.0, P * 6894.76
                CanteraFN.g_fuel_air_ratio = FAR
                gas.equilibrate("TP")
            return gas.density * 0.062428

    @staticmethod
    def Cp(T, P, FAR, p):
        """Specific heat at constant pressure.

        Parameters
        ----------
        T : float
            Temperature (R).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (dimensionless).
        p : object
            Session or context object.

        Returns
        -------
        float
            Specific heat at constant pressure (BTU/(lbm·R)).
        """
        if FAR < 0.00001:
            if (
                abs(gasair.T - T * 5.0 / 9) > 0.0001
                or abs(gasair.P - P * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - FAR) > 0.00001
            ):
                gasair.TP = T * 5.0 / 9.0, P * 6894.76
                CanteraFN.g_fuel_air_ratio = FAR
                gasair.equilibrate("TP")
            return gasair.cp * 0.0002390057

        else:
            if (
                abs(gas.T - T * 5.0 / 9) > 0.0001
                or abs(gas.P - P * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - FAR) > 0.00001
            ):
                gas.set_mixture_fraction(
                    FAR / (1 - FAR),
                    fuel=fuel_comp,
                    oxidizer=oxidizer_comp,
                    basis="mass",
                )
                gas.TP = T * 5.0 / 9.0, P * 6894.76
                CanteraFN.g_fuel_air_ratio = FAR
                gas.equilibrate("TP")
            return gas.cp * 0.0002390057

    @staticmethod
    def h_TP(T, P, FAR, p):
        """Enthalpy from temperature and pressure.

        Parameters
        ----------
        T : float
            Temperature (R).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (dimensionless).
        p : object
            Session or context object.

        Returns
        -------
        float
            Enthalpy (BTU/lbm).
        """
        if FAR < 0.00001:
            if (
                abs(gasair.T - T * 5.0 / 9) > 0.0000001
                or abs(gasair.P - P * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - FAR) > 0.00001
            ):
                gasair.TP = T * 5.0 / 9.0, P * 6894.76
                CanteraFN.g_fuel_air_ratio = FAR
                gasair.equilibrate("TP")
            return gasair.h * 0.0004299226
        else:
            if (
                abs(gas.T - T * 5.0 / 9) > 0.0000001
                or abs(gas.P - P * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - FAR) > 0.00001
            ):
                gas.set_mixture_fraction(
                    FAR / (1 - FAR),
                    fuel=fuel_comp,
                    oxidizer=oxidizer_comp,
                    basis="mass",
                )
                gas.TP = T * 5.0 / 9.0, P * 6894.76
                CanteraFN.g_fuel_air_ratio = FAR
                gas.equilibrate("TP")
            return gas.h * 0.0004299226

    @staticmethod
    def s_TP(T, P, FAR, p):
        """Entropy from temperature and pressure.

        Parameters
        ----------
        T : float
            Temperature (R).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (dimensionless).
        p : object
            Session or context object.

        Returns
        -------
        float
            Entropy (BTU/(lbm·R)).
        """
        if FAR < 0.00001:
            if (
                abs(gasair.T - T * 5.0 / 9) > 0.0001
                or abs(gasair.P - P * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - FAR) > 0.00001
            ):
                gasair.TP = T * 5.0 / 9.0, P * 6894.76
                CanteraFN.g_fuel_air_ratio = FAR
                gasair.equilibrate("TP")

            return gasair.s * 0.0002390057
        else:
            if (
                abs(gas.T - T * 5.0 / 9) > 0.0001
                or abs(gas.P - P * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - FAR) > 0.00001
            ):
                gas.set_mixture_fraction(
                    FAR / (1 - FAR),
                    fuel=fuel_comp,
                    oxidizer=oxidizer_comp,
                    basis="mass",
                )
                gas.TP = T * 5.0 / 9.0, P * 6894.76
                CanteraFN.g_fuel_air_ratio = FAR
                gas.equilibrate("TP")
            return gas.s * 0.0002390057

    @staticmethod
    def R(T, P, FAR, p):
        """Gas constant.

        Parameters
        ----------
        T : float
            Temperature (R).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (dimensionless).
        p : object
            Session or context object.

        Returns
        -------
        float
            Gas constant (BTU/(lbm·R)).
        """
        if FAR < 0.00001:
            if (
                abs(gasair.T - T * 5.0 / 9) > 0.0001
                or abs(gasair.P - P * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - FAR) > 0.00001
            ):
                gasair.TP = T * 5.0 / 9.0, P * 6894.76
                CanteraFN.g_fuel_air_ratio = FAR
                gasair.equilibrate("TP")
            return 8.314 / gasair.mean_molecular_weight * 0.0002390057 * 1000.0
        else:
            if (
                abs(gas.T - T * 5.0 / 9) > 0.0001
                or abs(gas.P - P * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - FAR) > 0.00001
            ):
                gas.set_mixture_fraction(
                    FAR / (1 - FAR),
                    fuel=fuel_comp,
                    oxidizer=oxidizer_comp,
                    basis="mass",
                )
                gas.TP = T * 5.0 / 9.0, P * 6894.76
                CanteraFN.g_fuel_air_ratio = FAR
                gas.equilibrate("TP")
            return 8.314 / gas.mean_molecular_weight * 0.0002390057 * 1000.0

    @staticmethod
    def mu(T, P, FAR, p):
        """Dynamic viscosity.

        Parameters
        ----------
        T : float
            Temperature (R).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (dimensionless).
        p : object
            Session or context object.

        Returns
        -------
        float
            Dynamic viscosity. Currently returns 0.
        """
        return 0

    @staticmethod
    def k(T, P, FAR, p):
        """Thermal conductivity.

        Parameters
        ----------
        T : float
            Temperature (R).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (dimensionless).
        p : object
            Session or context object.

        Returns
        -------
        float
            Thermal conductivity. Currently returns 0.
        """
        return 0

    @staticmethod
    def T_sP(s, P, FAR, p):
        """Temperature from entropy and pressure.

        Parameters
        ----------
        s : float
            Entropy (BTU/(lbm·R)).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (dimensionless).
        p : object
            Session or context object.

        Returns
        -------
        float
            Temperature (R).
        """
        if FAR < 0.00001:
            if (
                abs(gasair.s - s / 0.0002390057) > 0.0001
                or abs(gasair.P - P * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - FAR) > 0.00001
            ):
                gasair.SP = s / 0.0002390057, P * 6894.76
                CanteraFN.g_fuel_air_ratio = FAR
                gasair.equilibrate("SP")
            return gasair.T * 9.0 / 5.0
        else:
            if (
                abs(gas.s - s / 0.0002390057) > 0.0001
                or abs(gas.P - P * 6894.76) > 0.0001
                or abs(CanteraFN.g_fuel_air_ratio - FAR) > 0.00001
            ):
                gas.set_mixture_fraction(
                    FAR / (1 - FAR),
                    fuel=fuel_comp,
                    oxidizer=oxidizer_comp,
                    basis="mass",
                )
                gas.SP = s / 0.0002390057, P * 6894.76
                CanteraFN.g_fuel_air_ratio = FAR
                gas.equilibrate("SP")
            return gas.T * 9.0 / 5.0

    @staticmethod
    def T_hp(h, P, FAR, p):
        """Temperature from enthalpy and pressure.

        Parameters
        ----------
        h : float
            Enthalpy (BTU/lbm).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (dimensionless).
        p : object
            Session or context object.

        Returns
        -------
        float
            Temperature (R).
        """
        T = 1500
        hcalc = CanteraFN.h_TP(T, P, FAR, p)
        errorm1 = (hcalc - h) / h
        xm1 = T
        T = T * 0.95
        hcalc = CanteraFN.h_TP(T, P, FAR, p)
        error = (hcalc - h) / h
        x = T

        while abs(error) > 0.000001:
            xp1 = x - error * (x - xm1) / (error - errorm1)
            if xp1 - x > 0.3 * T:
                xp1 = x + 0.3 * T
            if xp1 - x < -0.3 * T:
                xp1 = x - 0.3 * T
            xm1 = x
            errorm1 = error
            x = xp1
            T = x
            hcalc = CanteraFN.h_TP(T, P, FAR, p)
            error = (hcalc - h) / h

        return T

    @staticmethod
    def p_hs(h, s, FAR, P, p):
        """Pressure from enthalpy and entropy.

        Parameters
        ----------
        h : float
            Enthalpy (BTU/lbm).
        s : float
            Entropy (BTU/(lbm·R)).
        FAR : float
            Fuel-air ratio (dimensionless).
        P : float
            Pressure (Pa).
        p : object
            Session or context object.

        Returns
        -------
        float
            Pressure (Pa).
        """
        T = CanteraFN.T_sP(s, P, FAR)

        hcalc = CanteraFN.h_TP(T, P, FAR, p)
        errorm1 = (hcalc - h) / h
        xm1 = P
        P = P * 0.95
        T = CanteraFN.T_sP(s, P, FAR)
        hcalc = CanteraFN.h_TP(T, P, FAR, p)
        error = (hcalc - h) / h
        x = P

        while abs(error) > 0.000001:
            xp1 = x - error * (x - xm1) / (error - errorm1)
            if xp1 - x > 0.1 * P:
                xp1 = x + 0.1 * P
            if xp1 - x < -0.1 * P:
                xp1 = x - 0.1 * P
            xm1 = x
            errorm1 = error
            x = xp1
            P = x
            T = CanteraFN.T_sP(s, P, FAR)
            hcalc = CanteraFN.h_TP(T, P, FAR)
            error = (hcalc - h) / h

        return P
