import os

import numpy as np

from poeme import interp_3d


class Air2:
    """Air property lookup table using 3D interpolation.

    Provides thermodynamic properties of air as a function of temperature (T),
    pressure (P), and fuel-air ratio (FAR). Properties are interpolated from
    precomputed data stored in ``air2_data.npz``.

    Parameters
    ----------
    T : float
        Temperature (K).
    P : float
        Pressure (Pa).
    FAR : float
        Fuel-air ratio (kg fuel / kg air).

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
    _data_file = os.path.join(os.path.dirname(__file__), "air2_data.npz")
    _data = np.load(_data_file)

    T_TP = _data["T_TP"].tolist()
    P_TP = _data["P_TP"].tolist()
    FAR_TP = _data["FAR_TP"].tolist()
    h_TPt = _data["h_TPt"].tolist()
    Cp_TPt = _data["Cp_TPt"].tolist()
    gam_TPt = _data["gam_TPt"].tolist()
    rho_TPt = _data["rho_TPt"].tolist()
    r_TPt = _data["R_TPt"].tolist()
    s_TPt = _data["s_TPt"].tolist()

    @staticmethod
    def gamma(T, P, FAR):
        """Heat capacity ratio (gamma = Cp/Cv).

        Parameters
        ----------
        T : float
            Temperature (K).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).

        Returns
        -------
        float
            Heat capacity ratio.
        """
        return interp_3d(
            FAR,
            P,
            T,
            Air2.FAR_TP,
            Air2.P_TP,
            Air2.T_TP,
            Air2.gam_TPt,
        )

    @staticmethod
    def rho(T, P, FAR):
        """Air density.

        Parameters
        ----------
        T : float
            Temperature (K).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).

        Returns
        -------
        float
            Density (kg/m³).
        """
        return interp_3d(
            FAR,
            P,
            T,
            Air2.FAR_TP,
            Air2.P_TP,
            Air2.T_TP,
            Air2.rho_TPt,
        )

    @staticmethod
    def Cp(T, P, FAR):
        """Specific heat at constant pressure.

        Parameters
        ----------
        T : float
            Temperature (K).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).

        Returns
        -------
        float
            Specific heat at constant pressure (J/(kg·K)).
        """
        return interp_3d(
            FAR,
            P,
            T,
            Air2.FAR_TP,
            Air2.P_TP,
            Air2.T_TP,
            Air2.Cp_TPt,
        )

    @staticmethod
    def h_TP(T, P, FAR):
        """Enthalpy.

        Parameters
        ----------
        T : float
            Temperature (K).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).

        Returns
        -------
        float
            Enthalpy (J/kg).
        """
        return interp_3d(
            FAR,
            P,
            T,
            Air2.FAR_TP,
            Air2.P_TP,
            Air2.T_TP,
            Air2.h_TPt,
        )

    @staticmethod
    def s_TP(T, P, FAR):
        """Entropy.

        Parameters
        ----------
        T : float
            Temperature (K).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).

        Returns
        -------
        float
            Entropy (J/(kg·K)).
        """
        return interp_3d(
            FAR,
            P,
            T,
            Air2.FAR_TP,
            Air2.P_TP,
            Air2.T_TP,
            Air2.s_TPt,
        )

    @staticmethod
    def R(T, P, FAR):
        """Specific gas constant.

        Parameters
        ----------
        T : float
            Temperature (K).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).

        Returns
        -------
        float
            Specific gas constant (J/(kg·K)).
        """
        return interp_3d(
            FAR,
            P,
            T,
            Air2.FAR_TP,
            Air2.P_TP,
            Air2.T_TP,
            Air2.r_TPt,
        )

    @staticmethod
    def mu(T, P, FAR):
        """Dynamic viscosity.

        Parameters
        ----------
        T : float
            Temperature (K).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).

        Returns
        -------
        float
            Dynamic viscosity (Pa·s). Currently returns 0.
        """
        return 0

    @staticmethod
    def k(T, P, FAR):
        """Thermal conductivity.

        Parameters
        ----------
        T : float
            Temperature (K).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).

        Returns
        -------
        float
            Thermal conductivity (W/(m·K)). Currently returns 0.
        """
        return 0

    @staticmethod
    def T_sP(s, P, FAR):
        """Temperature from entropy and pressure via Newton iteration.

        Parameters
        ----------
        s : float
            Target entropy (J/(kg·K)).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).

        Returns
        -------
        float
            Temperature (K) that satisfies the given entropy at pressure P.
        """
        T = 1500
        scalc = Air2.s_TP(T, P, FAR)

        errorm1 = (scalc - s) / s
        xm1 = T
        T = T * 0.95
        scalc = Air2.s_TP(T, P, FAR)
        error = (scalc - s) / s
        x = T
        while abs(error) > 0.0000001:
            xp1 = x - error * (x - xm1) / (error - errorm1)
            if xp1 - x > 0.3 * T:
                xp1 = x + 0.3 * T
            if xp1 - x < -0.3 * T:
                xp1 = x - 0.3 * T
            xm1 = x
            errorm1 = error
            x = xp1
            T = x
            scalc = Air2.s_TP(T, P, FAR)
            error = (scalc - s) / s

        return T

    @staticmethod
    def T_hp(h, P, FAR):
        """Temperature from enthalpy and pressure via Newton iteration.

        Parameters
        ----------
        h : float
            Target enthalpy (J/kg).
        P : float
            Pressure (Pa).
        FAR : float
            Fuel-air ratio (kg fuel / kg air).

        Returns
        -------
        float
            Temperature (K) that satisfies the given enthalpy at pressure P.
        """
        T = 1500
        hcalc = Air2.h_TP(T, P, FAR)
        errorm1 = (hcalc - h) / h
        xm1 = T
        T = T * 0.95
        hcalc = Air2.h_TP(T, P, FAR)
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
            hcalc = Air2.h_TP(T, P, FAR)
            error = (hcalc - h) / h

        return T
