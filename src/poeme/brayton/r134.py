import os

import numpy as np

from poeme import interp_2d


class R134:
    """R134a refrigerant property lookup table using 2D interpolation.

    Provides thermodynamic properties of R134a refrigerant as a function
    of enthalpy (ht) and pressure (P). Properties are interpolated from
    precomputed data stored in ``r134_data.npz``.

    Attributes
    ----------
    h_hp : list
        Enthalpy grid for hp lookup.
    p_hp : list
        Pressure grid for hp lookup.
    t_hpt : list
        Temperature lookup table (K).
    s_hpt : list
        Entropy lookup table (J/(kg·K)).
    rho_hp : list
        Density lookup table (kg/m³).
    """

    # Load data from file
    _data_file = os.path.join(os.path.dirname(__file__), "r134_data.npz")
    _data = np.load(_data_file)

    h_hp = _data["h_hp"].tolist()
    p_hp = _data["P_hp"].tolist()
    t_hpt = _data["T_hPt"].tolist()
    s_hpt = _data["s_hPt"].tolist()
    rho_hp = _data["rho_hp"].tolist()

    @staticmethod
    def T_hp(ht, Pt):
        """Temperature from enthalpy and pressure.

        Parameters
        ----------
        ht : float
            Enthalpy (BTU/lbm).
        Pt : float
            Pressure (Pa).

        Returns
        -------
        float
            Temperature (K).
        """
        return interp_2d(Pt, ht, R134.p_hp, R134.h_hp, R134.t_hpt)

    @staticmethod
    def s_hP(ht, Pt):
        """Entropy from enthalpy and pressure.

        Parameters
        ----------
        ht : float
            Enthalpy (BTU/lbm).
        Pt : float
            Pressure (Pa).

        Returns
        -------
        float
            Entropy (J/(kg·K)).
        """
        return interp_2d(Pt, ht, R134.p_hp, R134.h_hp, R134.s_hpt)

    @staticmethod
    def rho(ht, Pt):
        """Density from enthalpy and pressure.

        Parameters
        ----------
        ht : float
            Enthalpy (BTU/lbm).
        Pt : float
            Pressure (Pa).

        Returns
        -------
        float
            Density (kg/m³).
        """
        return interp_2d(Pt, ht, R134.p_hp, R134.h_hp, R134.rho_hp)
