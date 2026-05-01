import os

import numpy as np

from popclean import g, interp3D


class Newtherm:
    # Load data from file
    _data_file = os.path.join(os.path.dirname(__file__), "newtherm_data.npz")
    _data = np.load(_data_file)

    t_tp = _data["T_TP"].tolist()
    p_tp = _data["P_TP"].tolist()
    far_tp = _data["FAR_TP"].tolist()
    h_tpt = _data["h_TPt"].tolist()
    cp_tpt = _data["Cp_TPt"].tolist()
    gam_tpt = _data["gam_TPt"].tolist()
    rho_tpt = _data["rho_TPt"].tolist()
    r_tpt = _data["R_TPt"].tolist()
    s_tpt = _data["s_TPt"].tolist()

    @staticmethod
    def gam(temperature, pressure, fuel_air_ratio, p):
        return interp3D(
            fuel_air_ratio,
            pressure,
            temperature,
            Newtherm.far_tp,
            Newtherm.p_tp,
            Newtherm.t_tp,
            Newtherm.gam_tpt,
            p,
        )

    @staticmethod
    def rho(temperature, pressure, fuel_air_ratio, p):
        return interp3D(
            fuel_air_ratio,
            pressure,
            temperature,
            Newtherm.far_tp,
            Newtherm.p_tp,
            Newtherm.t_tp,
            Newtherm.rho_tpt,
            p,
        )

    @staticmethod
    def cp(temperature, pressure, fuel_air_ratio, p):
        return interp3D(
            fuel_air_ratio,
            pressure,
            temperature,
            Newtherm.far_tp,
            Newtherm.p_tp,
            Newtherm.t_tp,
            Newtherm.cp_tpt,
            p,
        )

    @staticmethod
    def h_tp(temperature, pressure, fuel_air_ratio, p):
        return interp3D(
            fuel_air_ratio,
            pressure,
            temperature,
            Newtherm.far_tp,
            Newtherm.p_tp,
            Newtherm.t_tp,
            Newtherm.h_tpt,
            p,
        )

    @staticmethod
    def s_tp(temperature, pressure, fuel_air_ratio, p):
        return interp3D(
            fuel_air_ratio,
            pressure,
            temperature,
            Newtherm.far_tp,
            Newtherm.p_tp,
            Newtherm.t_tp,
            Newtherm.s_tpt,
            p,
        )

    @staticmethod
    def r(temperature, pressure, fuel_air_ratio, p):
        return interp3D(
            fuel_air_ratio,
            pressure,
            temperature,
            Newtherm.far_tp,
            Newtherm.p_tp,
            Newtherm.t_tp,
            Newtherm.r_tpt,
            p,
        )

    @staticmethod
    def mu(temperature, pressure, fuel_air_ratio, p):
        return 0

    @staticmethod
    def k(temperature, pressure, fuel_air_ratio, p):
        return 0

    @staticmethod
    def t_sp(s, pressure, fuel_air_ratio, p):
        temperature = 1500
        scalc = Newtherm.s_tp(temperature, pressure, fuel_air_ratio, p)

        errorm1 = (scalc - s) / s
        xm1 = temperature
        temperature = temperature * 0.95
        scalc = Newtherm.s_tp(temperature, pressure, fuel_air_ratio, p)
        error = (scalc - s) / s
        x = temperature
        count = 0
        while abs(error) > 0.0000001 and count < 50:
            count = count + 1
            xp1 = x - error * (x - xm1) / (error - errorm1)
            if xp1 - x > 0.3 * temperature:
                xp1 = x + 0.3 * temperature
            if xp1 - x < -0.3 * temperature:
                xp1 = x - 0.3 * temperature
            xm1 = x
            errorm1 = error
            x = xp1
            temperature = x
            scalc = Newtherm.s_tp(temperature, pressure, fuel_air_ratio, p)
            error = (scalc - s) / s

        if count > 49:
            g.errors = g.errors + "Error in T_sp"

        return temperature

    @staticmethod
    def t_hp(h, pressure, fuel_air_ratio, p):
        temperature = 1500
        hcalc = Newtherm.h_tp(temperature, pressure, fuel_air_ratio, p)
        errorm1 = (hcalc - h) / h
        xm1 = temperature
        temperature = temperature * 0.95
        hcalc = Newtherm.h_tp(temperature, pressure, fuel_air_ratio, p)
        error = (hcalc - h) / h
        x = temperature
        count = 0
        while abs(error) > 0.000001 and count < 50:
            count = count + 1
            xp1 = x - error * (x - xm1) / (error - errorm1)
            if xp1 - x > 0.3 * temperature:
                xp1 = x + 0.3 * temperature
            if xp1 - x < -0.3 * temperature:
                xp1 = x - 0.3 * temperature
            xm1 = x
            errorm1 = error
            x = xp1
            temperature = x
            hcalc = Newtherm.h_tp(temperature, pressure, fuel_air_ratio, p)
            error = (hcalc - h) / h
        if count > 49:
            g.errors = g.errors + "Error in T_hp"

        return temperature
