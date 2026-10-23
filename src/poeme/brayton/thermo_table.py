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

    _tables = {}

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
    def _iterate_calc(func, var, P, FAR, name, p):
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
        calc = func(T, P, FAR, name, p)
        errorm1 = (calc - var) / var
        xm1 = T
        T = T * 0.95
        calc = func(T, P, FAR, name, p)
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
            calc = func(T, P, FAR, name, p)
            error = (calc - var) / var
        if count > 49:
            p.session.errors += f"{func.__name__} did not converge"

        return T

    @classmethod
    def gamma(cls, T, P, FAR, name, p):
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
        table = cls._table(name)
        return interp_3d(FAR, P, T, table.FAR_TP, table.P_TP, table.T_TP, table.gam_TPt, p)

    @classmethod
    def rho(cls, T, P, FAR, name, p):
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
        table = cls._table(name)
        return interp_3d(FAR, P, T, table.FAR_TP, table.P_TP, table.T_TP, table.rho_TPt, p)

    @classmethod
    def Cp(cls, T, P, FAR, name, p):
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
        table = cls._table(name)
        return interp_3d(FAR, P, T, table.FAR_TP, table.P_TP, table.T_TP, table.Cp_TPt, p)

    @classmethod
    def h_TP(cls, T, P, FAR, name, p):
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
        table = cls._table(name)
        return interp_3d(FAR, P, T, table.FAR_TP, table.P_TP, table.T_TP, table.h_TPt, p)

    @classmethod
    def s_TP(cls, T, P, FAR, name, p):
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
        table = cls._table(name)
        return interp_3d(FAR, P, T, table.FAR_TP, table.P_TP, table.T_TP, table.s_TPt, p)

    @classmethod
    def R(cls, T, P, FAR, name, p):
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
        table = cls._table(name)
        return interp_3d(FAR, P, T, table.FAR_TP, table.P_TP, table.T_TP, table.r_TPt, p)

    @classmethod
    def mu(cls, T, P, FAR, name, p):
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

    @classmethod
    def k(cls, T, P, FAR, name, p):
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

    @classmethod
    def T_sP(cls, s, P, FAR, name, p):
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
        return cls._iterate_calc(cls.s_TP, s, P, FAR, name, p)

    @classmethod
    def T_hp(cls, h, P, FAR, name, p):
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
        return cls._iterate_calc(cls.h_TP, h, P, FAR, name, p)

    @classmethod
    def h_sp(cls, s, P, FAR, name, p):
        """Enthalpy from entropy and pressure via Newton iteration."""
        T = cls.T_sP(s, P, FAR, name, p)
        return cls.h_TP(T, P, FAR, name, p)

    @classmethod
    def s_hP(cls, h, P, FAR, name, p):
        """Entropy from enthalpy and pressure via Newton iteration."""
        T = cls.T_hp(h, P, FAR, name, p)
        return cls.s_TP(T, P, FAR, name, p)
    @classmethod
    def _table(cls, name):
        if name == "none":
            raise ValueError("ThermoTable requires fname to name a thermo table")
        if name not in cls._tables:
            filename = name if name.endswith(".npz") else name + ".npz"
            cls._tables[name] = ThermoTable(os.path.join("thermo_tables", filename))
        return cls._tables[name]

