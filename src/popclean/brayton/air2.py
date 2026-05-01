import os

import numpy as np

from popclean import interp3D


class Air2:
    # Load data from file
    _data_file = os.path.join(os.path.dirname(__file__), "air2_data.npz")
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
    def gamma(temperature, pressure, fuel_air_ratio):
        return interp3D(
            fuel_air_ratio,
            pressure,
            temperature,
            Air2.far_tp,
            Air2.p_tp,
            Air2.t_tp,
            Air2.gam_tpt,
        )

    @staticmethod
    def rho(temperature, pressure, fuel_air_ratio):
        return interp3D(
            fuel_air_ratio,
            pressure,
            temperature,
            Air2.far_tp,
            Air2.p_tp,
            Air2.t_tp,
            Air2.rho_tpt,
        )

    @staticmethod
    def cp(temperature, pressure, fuel_air_ratio):
        return interp3D(
            fuel_air_ratio,
            pressure,
            temperature,
            Air2.far_tp,
            Air2.p_tp,
            Air2.t_tp,
            Air2.cp_tpt,
        )

    @staticmethod
    def h_tp(temperature, pressure, fuel_air_ratio):
        return interp3D(
            fuel_air_ratio,
            pressure,
            temperature,
            Air2.far_tp,
            Air2.p_tp,
            Air2.t_tp,
            Air2.h_tpt,
        )

    @staticmethod
    def s_tp(temperature, pressure, fuel_air_ratio):
        return interp3D(
            fuel_air_ratio,
            pressure,
            temperature,
            Air2.far_tp,
            Air2.p_tp,
            Air2.t_tp,
            Air2.s_tpt,
        )

    @staticmethod
    def r(temperature, pressure, fuel_air_ratio):
        return interp3D(
            fuel_air_ratio,
            pressure,
            temperature,
            Air2.far_tp,
            Air2.p_tp,
            Air2.t_tp,
            Air2.r_tpt,
        )

    @staticmethod
    def mu(temperature, pressure, fuel_air_ratio):
        return 0

    @staticmethod
    def k(temperature, pressure, fuel_air_ratio):
        return 0

    @staticmethod
    def t_sp(s, pressure, fuel_air_ratio):
        temperature = 1500
        scalc = Air2.s_tp(temperature, pressure, fuel_air_ratio)

        errorm1 = (scalc - s) / s
        xm1 = temperature
        temperature = temperature * 0.95
        scalc = Air2.s_tp(temperature, pressure, fuel_air_ratio)
        error = (scalc - s) / s
        x = temperature
        while abs(error) > 0.0000001:
            xp1 = x - error * (x - xm1) / (error - errorm1)
            if xp1 - x > 0.3 * temperature:
                xp1 = x + 0.3 * temperature
            if xp1 - x < -0.3 * temperature:
                xp1 = x - 0.3 * temperature
            xm1 = x
            errorm1 = error
            x = xp1
            temperature = x
            scalc = Air2.s_tp(temperature, pressure, fuel_air_ratio)
            error = (scalc - s) / s

        return temperature

    @staticmethod
    def t_hp(h, pressure, fuel_air_ratio):
        temperature = 1500
        hcalc = Air2.h_tp(temperature, pressure, fuel_air_ratio)
        errorm1 = (hcalc - h) / h
        xm1 = temperature
        temperature = temperature * 0.95
        hcalc = Air2.h_tp(temperature, pressure, fuel_air_ratio)
        error = (hcalc - h) / h
        x = temperature
        while abs(error) > 0.000001:
            xp1 = x - error * (x - xm1) / (error - errorm1)
            if xp1 - x > 0.3 * temperature:
                xp1 = x + 0.3 * temperature
            if xp1 - x < -0.3 * temperature:
                xp1 = x - 0.3 * temperature
            xm1 = x
            errorm1 = error
            x = xp1
            temperature = x
            hcalc = Air2.h_tp(temperature, pressure, fuel_air_ratio)
            error = (hcalc - h) / h

        return temperature
