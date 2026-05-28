import os

import numpy as np

from poeme import interp_2d


class R134:
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
        return interp_2d(Pt, ht, R134.p_hp, R134.h_hp, R134.t_hpt)

    @staticmethod
    def s_hP(ht, Pt):
        return interp_2d(Pt, ht, R134.p_hp, R134.h_hp, R134.s_hpt)

    @staticmethod
    def rho(ht, Pt):
        return interp_2d(Pt, ht, R134.p_hp, R134.h_hp, R134.rho_hp)
