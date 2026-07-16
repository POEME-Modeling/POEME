import os

import numpy as np

from poeme import interp_3d


class Newtherm:
    """Thermodynamic property lookup table using 3D interpolation with session object.

    Provides thermodynamic properties of air as a function of temperature (T),
    pressure (P), and fuel-air ratio (FAR). Properties are interpolated from
    precomputed data stored in ``newtherm_data.npz``. This class includes convergence
    checking for iterative solvers.

    Parameters
    ----------
    T : float
        Temperature (K).
    P : float
        Pressure (Pa).
    FAR : float
        Fuel-air ratio (kg fuel / kg air).
    p : object
        Session or context object passed to methods.

    Attributes
    ----------
    T_TP : list
        Temperature grid points for interpolation.
    P_TP : list
        Pressure grid points for interpolation.
    FAR_TP : list
        Fuel-air ratio grid points for interpolation.
    h_TPt : list
        Enthalpy lookup table (J/kg).
    Cp_TPt : list
        Specific heat at constant pressure lookup table (J/(kg·K)).
    gam_TPt : list
        Heat capacity ratio (gamma) lookup table.
    rho_TPt : list
        Density lookup table (kg/m³).
    r_TPt : list
        Gas constant lookup table (J/(kg·K)).
    s_TPt : list
        Entropy lookup table (J/(kg·K)).
    """

    # Load data from file
    _data_file = os.path.join(os.path.dirname(__file__), "newtherm_data.npz")
    _data = np.load(_data_file)

    T_TP = _data["T_TP"].tolist()
    P_TP = _data["P_TP"].tolist()
    FAR_TP = _data["FAR_TP"].tolist()
    h_TPt = _data["h_TPt"].tolist()
    Cp_TPt = _data["Cp_TPt"].tolist()
    gam_TPt = _data["gam_TPt"].tolist()
    rho_TPt = _data["rho_TPt"].tolist()
    r_TPt = _data["r_TPt"].tolist()
    s_TPt = _data["s_TPt"].tolist()

    @staticmethod
    def gamma(T, P, FAR, p):
        """Heat capacity ratio (gamma = Cp/Cv).

        Parameters
        ----------
        T : float
            Temperature (K).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Heat capacity ratio.
        """
        return interp_3d(
            FAR,
            P,
            T,
            Newtherm.FAR_TP,
            Newtherm.P_TP,
            Newtherm.T_TP,
            Newtherm.gam_TPt,
            p,
        )

    @staticmethod
    def rho(T, P, FAR, p):
        """Air density.

        Parameters
        ----------
        T : float
            Temperature (K).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Density (kg/m³).
        """
        return interp_3d(
            FAR,
            P,
            T,
            Newtherm.FAR_TP,
            Newtherm.P_TP,
            Newtherm.T_TP,
            Newtherm.rho_TPt,
            p,
        )

    @staticmethod
    def Cp(T, P, FAR, p):
        """Specific heat at constant pressure.

        Parameters
        ----------
        T : float
            Temperature (K).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Specific heat at constant pressure (J/(kg·K)).
        """
        return interp_3d(
            FAR,
            P,
            T,
            Newtherm.FAR_TP,
            Newtherm.P_TP,
            Newtherm.T_TP,
            Newtherm.Cp_TPt,
            p,
        )

    @staticmethod
    def h_TP(T, P, FAR, p):
        """Enthalpy.

        Parameters
        ----------
        T : float
            Temperature (K).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Enthalpy (J/kg).
        """
        return interp_3d(
            FAR,
            P,
            T,
            Newtherm.FAR_TP,
            Newtherm.P_TP,
            Newtherm.T_TP,
            Newtherm.h_TPt,
            p,
        )

    @staticmethod
    def s_TP(T, P, FAR, p):
        """Entropy.

        Parameters
        ----------
        T : float
            Temperature (K).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Entropy (J/(kg·K)).
        """
        return interp_3d(
            FAR,
            P,
            T,
            Newtherm.FAR_TP,
            Newtherm.P_TP,
            Newtherm.T_TP,
            Newtherm.s_TPt,
            p,
        )

    @staticmethod
    def R(T, P, FAR, p):
        """Specific gas constant.

        Parameters
        ----------
        T : float
            Temperature (K).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Specific gas constant (J/(kg·K)).
        """
        return interp_3d(
            FAR,
            P,
            T,
            Newtherm.FAR_TP,
            Newtherm.P_TP,
            Newtherm.T_TP,
            Newtherm.r_TPt,
            p,
        )

    @staticmethod
    def mu(T, P, FAR, p):
        """Dynamic viscosity.

        Parameters
        ----------
        T : float
            Temperature (K).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Dynamic viscosity (Pa·s). Currently returns 0.
        """
        return 0

    @staticmethod
    def k(T, P, FAR, p):
        """Thermal conductivity.

        Parameters
        ----------
        T : float
            Temperature (K).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Thermal conductivity (W/(m·K)). Currently returns 0.
        """
        return 0

    @staticmethod
    def T_sP(s, P, FAR, p):
        """Temperature from entropy and pressure via Newton iteration.

        Parameters
        ----------
        s : float
            Target entropy (J/(kg·K)).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Temperature (K) that satisfies the given entropy at pressure P.

        Raises
        ------
        ValueError
            If the solver does not converge within 50 iterations.
        """
        T = 1500
        scalc = Newtherm.s_TP(T, P, FAR, p)

        errorm1 = (scalc - s) / s
        xm1 = T
        T = T * 0.95
        scalc = Newtherm.s_TP(T, P, FAR, p)
        error = (scalc - s) / s
        x = T
        count = 0
        while abs(error) > 0.0000001 and count < 50:
            count = count + 1
            xp1 = x - error * (x - xm1) / (error - errorm1)
            if xp1 - x > 0.3 * T:
                xp1 = x + 0.3 * T
            if xp1 - x < -0.3 * T:
                xp1 = x - 0.3 * T
            xm1 = x
            errorm1 = error
            x = xp1
            T = x
            scalc = Newtherm.s_TP(T, P, FAR, p)
            error = (scalc - s) / s

        if count > 49:
            error = "T_sP did not converge"
            raise ValueError(error)
            # TODO: fix this
            # p.session.errors += "Error in T_sp"

        return T

    @staticmethod
    def T_hp(h, P, FAR, p):
        """Temperature from enthalpy and pressure via Newton iteration.

        Parameters
        ----------
        h : float
            Target enthalpy (J/kg).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Temperature (K) that satisfies the given enthalpy at pressure P.

        Raises
        ------
        ValueError
            If the solver does not converge within 50 iterations.
        """
        T = 1500
        hcalc = Newtherm.h_TP(T, P, FAR, p)
        errorm1 = (hcalc - h) / h
        xm1 = T
        T = T * 0.95
        hcalc = Newtherm.h_TP(T, P, FAR, p)
        error = (hcalc - h) / h
        x = T
        count = 0
        while abs(error) > 0.000001 and count < 50:
            count = count + 1
            xp1 = x - error * (x - xm1) / (error - errorm1)
            if xp1 - x > 0.3 * T:
                xp1 = x + 0.3 * T
            if xp1 - x < -0.3 * T:
                xp1 = x - 0.3 * T
            xm1 = x
            errorm1 = error
            x = xp1
            T = x
            hcalc = Newtherm.h_TP(T, P, FAR, p)
            error = (hcalc - h) / h
        if count > 49:
            error = "T_hp did not converge"
            raise ValueError(error)
            # TODO: fix this
            # p.session.errors += "Error in T_hp"

        return T
