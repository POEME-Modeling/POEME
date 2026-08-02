import os

import numpy as np

from poeme import interp_3d


class JETATherm:
    # Load data from file
    _data_file = os.path.join(os.path.dirname(__file__), "jeta_air.npz")
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
        return interp_3d(
            FAR,
            P,
            T,
            JETATherm.FAR_TP,
            JETATherm.P_TP,
            JETATherm.T_TP,
            JETATherm.gam_TPt,
            p,
        )

    @staticmethod
    def rho(T, P, FAR, p):
        return interp_3d(
            FAR,
            P,
            T,
            JETATherm.FAR_TP,
            JETATherm.P_TP,
            JETATherm.T_TP,
            JETATherm.rho_TPt,
            p,
        )

    @staticmethod
    def Cp(T, P, FAR, p):
        return interp_3d(
            FAR,
            P,
            T,
            JETATherm.FAR_TP,
            JETATherm.P_TP,
            JETATherm.T_TP,
            JETATherm.Cp_TPt,
            p,
        )

    @staticmethod
    def h_TP(T, P, FAR, p):
        return interp_3d(
            FAR,
            P,
            T,
            JETATherm.FAR_TP,
            JETATherm.P_TP,
            JETATherm.T_TP,
            JETATherm.h_TPt,
            p,
        )

    @staticmethod
    def s_TP(T, P, FAR, p):
        return interp_3d(
            FAR,
            P,
            T,
            JETATherm.FAR_TP,
            JETATherm.P_TP,
            JETATherm.T_TP,
            JETATherm.s_TPt,
            p,
        )

    @staticmethod
    def R(T, P, FAR, p):
        return interp_3d(
            FAR,
            P,
            T,
            JETATherm.FAR_TP,
            JETATherm.P_TP,
            JETATherm.T_TP,
            JETATherm.r_TPt,
            p,
        )

    @staticmethod
    def mu(T, P, FAR, p):
        return 0

    @staticmethod
    def k(T, P, FAR, p):
        return 0

    @staticmethod
    def T_sP(s, P, FAR, p):
        T = 1500
        scalc = JETATherm.s_TP(T, P, FAR, p)

        errorm1 = (scalc - s) / s
        xm1 = T
        T = T * 0.95
        scalc = JETATherm.s_TP(T, P, FAR, p)
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
            scalc = JETATherm.s_TP(T, P, FAR, p)
            error = (scalc - s) / s

        if count > 49:
            error = "T_sP did not converge"
            raise ValueError(error)
            # TODO: fix this
            # p.session.errors += "Error in T_sp"

        return T

    @staticmethod
    def T_hp(h, P, FAR, p):
        T = 1500
        hcalc = JETATherm.h_TP(T, P, FAR, p)
        errorm1 = (hcalc - h) / h
        xm1 = T
        T = T * 0.95
        hcalc = JETATherm.h_TP(T, P, FAR, p)
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
            hcalc = JETATherm.h_TP(T, P, FAR, p)
            error = (hcalc - h) / h
        if count > 49:
            error = "T_hp did not converge"
            raise ValueError(error)
            # TODO: fix this
            # p.session.errors += "Error in T_hp"

        return T
