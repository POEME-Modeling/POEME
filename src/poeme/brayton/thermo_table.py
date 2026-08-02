import os

import numpy as np

from poeme import interp_3d


class ThermoTable:
    """Thermodynamic property lookup table using 3D interpolation with session object.

    Provides thermodynamic properties of air as a function of temperature (T),
    pressure (P), and fuel-air ratio (FAR). Properties are interpolated from
    precomputed data stored in ``newtherm_data.npz``. This class includes convergence
    checking for iterative solvers.

    Attributes
    ----------
    T_TP : list
        Temperature grid points for interpolation (°R).
    P_TP : list
        Pressure grid points for interpolation (psi).
    FAR_TP : list
        Fuel-air ratio grid points for interpolation.
    h_TPt : list
        Enthalpy lookup table (BTU/lbm).
    Cp_TPt : list
        Specific heat at constant pressure lookup table (BTU/(lbm·°R)).
    gam_TPt : list
        Heat capacity ratio (gamma) lookup table.
    rho_TPt : list
        Density lookup table (lbm/ft^3).
    r_TPt : list
        Gas constant lookup table (ft·lbf/(lbm·°R)).
    s_TPt : list
        Entropy lookup table (BTU/(lbm·°R)).
    """

    def __init__(self, thermo_file):
        # Load data from file
        if os.path.isabs(thermo_file):
            _data_file = thermo_file
        else:
            if (
                os.path.sep in thermo_file
                or thermo_file.startswith(".")
                or thermo_file.endswith(".npz")
            ):
                filename = thermo_file
            else:
                filename = thermo_file + ".npz"
            _data_file = os.path.join(os.path.dirname(__file__), filename)

        _data = np.load(_data_file)

        self.T_TP = _data["T_TP"].tolist()
        self.P_TP = _data["P_TP"].tolist()
        self.FAR_TP = _data["FAR_TP"].tolist()
        self.h_TPt = _data["h_TPt"].tolist()
        self.Cp_TPt = _data["Cp_TPt"].tolist()
        self.gam_TPt = _data["gam_TPt"].tolist()
        self.rho_TPt = _data["rho_TPt"].tolist()
        self.r_TPt = _data["r_TPt"].tolist()
        self.s_TPt = _data["s_TPt"].tolist()

    @staticmethod
    def _iterate_calc(func, var, P, FAR, p):
        """Iterate to find T such that func(T, P, FAR, p) converges to var.

        Uses a secant-like method with damping to solve for temperature.

        Parameters
        ----------
        func : callable
            Function of the form func(T, P, FAR, p) returning a computed value.
        var : float
            Target value for convergence.
        P : float
            Pressure (psi).
        FAR : float
            Fuel-air ratio (lbm fuel / lbm air).
        p : object
            Session or context object with an ``errors`` attribute.

        Returns
        -------
        float
            Converged temperature (°R).
        """
        T = 1500
        calc = func(T, P, FAR, p)
        errorm1 = (calc - var) / var
        xm1 = T
        T = T * 0.95
        calc = func(T, P, FAR, p)
        error = (calc - var) / var
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
            calc = func(T, P, FAR, p)
            error = (calc - var) / var
        if count > 49:
            p.session.errors += f"{func.__name__} did not converge"

        return T

    def gamma(self, T, P, FAR, p):
        """Heat capacity ratio (gamma = Cp/Cv).

        Parameters
        ----------
        T : float
            Temperature (°R).
        P : float
            Pressure (psi).
        FAR : float
            Fuel-air ratio (lbm fuel / lbm air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Heat capacity ratio.
        """
        return interp_3d(FAR, P, T, self.FAR_TP, self.P_TP, self.T_TP, self.gam_TPt, p)

    def rho(self, T, P, FAR, p):
        """Air density.

        Parameters
        ----------
        T : float
            Temperature (°R).
        P : float
            Pressure (psi).
        FAR : float
            Fuel-air ratio (lbm fuel / lbm air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Density (lbm/ft^3).
        """
        return interp_3d(FAR, P, T, self.FAR_TP, self.P_TP, self.T_TP, self.rho_TPt, p)

    def Cp(self, T, P, FAR, p):
        """Specific heat at constant pressure.

        Parameters
        ----------
        T : float
            Temperature (°R).
        P : float
            Pressure (psi).
        FAR : float
            Fuel-air ratio (lbm fuel / lbm air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Specific heat at constant pressure (BTU/(lbm·°R)).
        """
        return interp_3d(FAR, P, T, self.FAR_TP, self.P_TP, self.T_TP, self.Cp_TPt, p)

    def h_TP(self, T, P, FAR, p):
        """Enthalpy.

        Parameters
        ----------
        T : float
            Temperature (°R).
        P : float
            Pressure (psi).
        FAR : float
            Fuel-air ratio (lbm fuel / lbm air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Enthalpy (BTU/lbm).
        """
        return interp_3d(FAR, P, T, self.FAR_TP, self.P_TP, self.T_TP, self.h_TPt, p)

    def s_TP(self, T, P, FAR, p):
        """Entropy.

        Parameters
        ----------
        T : float
            Temperature (°R).
        P : float
            Pressure (psi).
        FAR : float
            Fuel-air ratio (lbm fuel / lbm air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Entropy (BTU/(lbm·°R)).
        """
        return interp_3d(FAR, P, T, self.FAR_TP, self.P_TP, self.T_TP, self.s_TPt, p)

    def R(self, T, P, FAR, p):
        """Specific gas constant.

        Parameters
        ----------
        T : float
            Temperature (°R).
        P : float
            Pressure (psi).
        FAR : float
            Fuel-air ratio (lbm fuel / lbm air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Specific gas constant (ft·lbf/(lbm·°R)).
        """
        return interp_3d(FAR, P, T, self.FAR_TP, self.P_TP, self.T_TP, self.r_TPt, p)

    def mu(self, T, P, FAR, p):
        """Dynamic viscosity.

        Parameters
        ----------
        T : float
            Temperature (°R).
        P : float
            Pressure (psi).
        FAR : float
            Fuel-air ratio (lbm fuel / lbm air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Dynamic viscosity (lbm/(ft·s)). Currently returns 0.
        """
        return 0

    def k(self, T, P, FAR, p):
        """Thermal conductivity.

        Parameters
        ----------
        T : float
            Temperature (°R).
        P : float
            Pressure (psi).
        FAR : float
            Fuel-air ratio (lbm fuel / lbm air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Thermal conductivity (BTU/(h·ft·°R)). Currently returns 0.
        """
        return 0

    def T_sP(self, s, P, FAR, p):
        """Temperature from entropy and pressure via Newton iteration.

        Parameters
        ----------
        s : float
            Target entropy (BTU/(lbm·°R)).
        P : float
            Pressure (psi).
        FAR : float
            Fuel-air ratio (lbm fuel / lbm air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Temperature (°R) that satisfies the given entropy at pressure P.
        """
        return self._iterate_calc(self.s_TP, s, P, FAR, p)

    def T_hp(self, h, P, FAR, p):
        """Temperature from enthalpy and pressure via Newton iteration.

        Parameters
        ----------
        h : float
            Target enthalpy (BTU/lbm).
        P : float
            Pressure (psi).
        FAR : float
            Fuel-air ratio (lbm fuel / lbm air).
        p : object
            Session or context object.

        Returns
        -------
        float
            Temperature (°R) that satisfies the given enthalpy at pressure P.
        """
        return self._iterate_calc(self.h_TP, h, P, FAR, p)
