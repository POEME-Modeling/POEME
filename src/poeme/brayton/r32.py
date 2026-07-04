from CoolProp import CoolProp


class R32:
    """R32 refrigerant property lookup table using CoolProp.

    Provides thermodynamic properties of R32 refrigerant as a function
    of temperature (T), pressure (P), and fuel-air ratio (FAR). Properties
    are computed on-the-fly using the CoolProp library.

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

    Notes
    -----
    Internal unit conversions: R to K via T * 5/9, Pa to psi via P * 6894.76.
    Output conversions: density to lbm/ft³ via * 0.062428, enthalpy to BTU/lbm
    via * 0.4299226, entropy to BTU/(lbm·R) via * 0.2388459.
    """

    @staticmethod
    def rho(T, P, FAR, p):
        """R32 density.

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
        return (
            CoolProp.PropsSI("D", "T", T * 5.0 / 9.0, "P", P * 6894.76, "R32")
            * 0.062428
        )

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
            Specific heat at constant pressure. Currently returns 0.
        """
        # return CoolProp.PropsSI("D", "T", T, "P", P, "R32")
        return 0.0

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
        # return CoolProp.PropsSI("D", "T", T, "P", P, "R32")
        return 0.0

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
        # return CoolProp.PropsSI("D", "T", T, "P", P, "R32")
        return 0.0

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
            Heat capacity ratio. Currently returns 0.
        """
        # return CoolProp.PropsSI("D", "T", T, "P", P, "R32")
        return 0.0

    @staticmethod
    def h_TP(T, P, FAR, p):
        """Enthalpy as a function of temperature and pressure.

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
        return (
            CoolProp.PropsSI("H", "T", T * 5.0 / 9.0, "P", P * 6894.76, "R32")
            * 0.4299226
        )

    @staticmethod
    def T_hp(h, P, FAR, p):
        """Temperature from enthalpy and pressure via CoolProp.

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
        return (
            CoolProp.PropsSI("T", "H", h / 0.4299226, "P", P * 6894.76, "R32")
            * 9.0
            / 5.0
        )

    @staticmethod
    def T_sP(s, P, FAR, p):
        """Temperature from entropy and pressure via CoolProp.

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
        return (
            CoolProp.PropsSI("T", "S", s / 0.2388459, "P", P * 6894.76, "R32")
            * 9.0
            / 5.0
        )

    @staticmethod
    def s_TP(T, P, FAR, p):
        """Entropy as a function of temperature and pressure.

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
        return (
            CoolProp.PropsSI("S", "T", T * 5.0 / 9.0, "P", P * 6894.76, "R32")
            * 0.2388459
        )

    @staticmethod
    def R(T, P, FAR, p):
        """Specific gas constant.

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
            Specific gas constant. Currently returns 0.
        """
        # return CoolProp.PropsSI("D", "T", T, "P", P*, "R32")
        return 0.0
