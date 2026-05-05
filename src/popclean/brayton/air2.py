import os

import numpy as np

from popclean import interp_3d


class Air2:
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
        return 0

    @staticmethod
    def k(T, P, FAR):
        return 0

    @staticmethod
    def T_sP(s, P, FAR):
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
