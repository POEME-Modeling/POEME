from CoolProp import CoolProp

fluid = "R134a"


class CPR134:
    """R134 refrigerant property evaluation using CoolProp.

    Provides thermodynamic properties of R134 refrigerant as a function
    of temperature (T), pressure (P), enthalpy (h), entropy (s), and
    quality (x). Properties are computed on-the-fly using the CoolProp
    library.

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
    """

    @staticmethod
    def T_hp(ht, Pt, FAR, p):
        """Temperature from enthalpy and pressure.

        Parameters
        ----------
        ht : float
            Enthalpy (BTU/lbm).
        Pt : float
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
            CoolProp.PropsSI("T", "H", ht * 2326.0, "P", Pt * 6894.76, fluid)
            * 9.0
            / 5.0
        )

    @staticmethod
    def T_sP(s, Pt, FAR, p):
        """Temperature from entropy and pressure.

        Parameters
        ----------
        s : float
            Entropy (BTU/(lbm·R)).
        Pt : float
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
            CoolProp.PropsSI("T", "S", s / 0.0002388, "P", Pt * 6894.76, fluid)
            * 9.0
            / 5.0
        )

    @staticmethod
    def h_TP(Tt, Pt, FAR, p):
        """Enthalpy from temperature and pressure.

        Parameters
        ----------
        Tt : float
            Temperature (R).
        Pt : float
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
            CoolProp.PropsSI("H", "T", Tt * 5.0 / 9.0, "P", Pt * 6894.76, fluid)
            / 2326.0
        )

    @staticmethod
    def h_sp(s, Pt, FAR, p):
        """Enthalpy from entropy and pressure.

        Parameters
        ----------
        s : float
            Entropy (BTU/(lbm·R)).
        Pt : float
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
            CoolProp.PropsSI("H", "S", s / 0.0002388, "P", Pt * 6894.76, fluid) / 2326.0
        )

    @staticmethod
    def h_qp(q, Pt, FAR, p):
        """Enthalpy from quality and pressure.

        Parameters
        ----------
        q : float
            Quality (mass fraction of vapor).
        Pt : float
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
        return CoolProp.PropsSI("H", "Q", q, "P", Pt * 6894.76, fluid) / 2326.0

    @staticmethod
    def tsat(Pt, FAR, p):
        """Saturation temperature at pressure.

        Parameters
        ----------
        Pt : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (dimensionless).
        p : object
            Session or context object.

        Returns
        -------
        float
            Saturation temperature (R).
        """
        return CoolProp.PropsSI("T", "P", Pt * 6894.76, "Q", 0.5, fluid) * 9.0 / 5.0

    @staticmethod
    def s_hP(ht, Pt, FAR, p):
        """Entropy from enthalpy and pressure.

        Parameters
        ----------
        ht : float
            Enthalpy (BTU/lbm).
        Pt : float
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
            CoolProp.PropsSI("S", "H", ht * 2326.0, "P", Pt * 6894.76, fluid)
            * 0.0002388
        )

    @staticmethod
    def s_TP(Tt, Pt, FAR, p):
        """Entropy from temperature and pressure.

        Parameters
        ----------
        Tt : float
            Temperature (R).
        Pt : float
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
            CoolProp.PropsSI("S", "T", Tt * 5.0 / 9.0, "P", Pt * 6894.76, fluid)
            * 0.0002388
        )

    @staticmethod
    def rho(ht, Pt, FAR, p):
        """Density from enthalpy and pressure.

        Parameters
        ----------
        ht : float
            Enthalpy (BTU/lbm).
        Pt : float
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
            CoolProp.PropsSI("D", "H", ht * 2326.0, "P", Pt * 6894.76, fluid)
            * 0.0624279606
        )

    @staticmethod
    def R(ht, Pt, FAR, p):
        """Gas constant.

        Parameters
        ----------
        ht : float
            Enthalpy (BTU/lbm).
        Pt : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (dimensionless).
        p : object
            Session or context object.

        Returns
        -------
        float
            Gas constant. Currently returns 0.
        """
        return 0.0

    @staticmethod
    def Cp(ht, Pt, FAR, p):
        """Specific heat at constant pressure.

        Parameters
        ----------
        ht : float
            Enthalpy (BTU/lbm).
        Pt : float
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
        return 0.0

    @staticmethod
    def gamma(ht, Pt, FAR, p):
        """Heat capacity ratio (gamma = Cp/Cv).

        Parameters
        ----------
        ht : float
            Enthalpy (BTU/lbm).
        Pt : float
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
        return 0.0

    @staticmethod
    def k(ht, Pt, FAR, p):
        """Thermal conductivity.

        Parameters
        ----------
        ht : float
            Enthalpy (BTU/lbm).
        Pt : float
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
        return 0.0

    @staticmethod
    def mu(ht, Pt, FAR, p):
        """Dynamic viscosity.

        Parameters
        ----------
        ht : float
            Enthalpy (BTU/lbm).
        Pt : float
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
        return 0.0

    @staticmethod
    def q(ht, Pt, FAR, p):
        """Vapor quality from enthalpy and pressure.

        Parameters
        ----------
        ht : float
            Enthalpy (BTU/lbm).
        Pt : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (dimensionless).
        p : object
            Session or context object.

        Returns
        -------
        float
            Vapor quality (mass fraction of vapor, 0-1).
        """
        return CoolProp.PropsSI("Q", "H", ht * 2326.0, "P", Pt * 6894.76, fluid)
