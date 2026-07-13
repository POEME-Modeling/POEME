"""Generate air2_data.npz for Air2 property lookups.

Computes thermodynamic properties of air on a 3D grid (T, P, FAR) using
Cantera's `Air` equation of state, then saves the results as an NPZ file
compatible with ``poeme.brayton.air2.Air2``.

Run this script to regenerate ``src/poeme/brayton/air2_data.npz``:

    python generate_air2_data.py
"""

import os

import cantera as ct
import numpy as np



fuel_comp = {"C": 1.0, "H": 0.16667}
oxidizer_comp = {"O2": 0.2153, "N2": 0.752, "AR":.0128, "CO2":.0006}  # Mass fractions for dry air

# ---------------------------------------------------------------------------
# Grid definitions
# ---------------------------------------------------------------------------

T_min, T_max, T_n = 200, 3000, 61          # Temperature (K)
P_min, P_max, P_n = 1e4, 1e8, 61           # Pressure (Pa)
FAR_min, FAR_max, FAR_n = 0.0, 0.25, 31    # Fuel-air ratio (kg fuel / kg air)

#T_grid = np.linspace(T_min, T_max, T_n)
#P_grid = np.linspace(P_min, P_max, P_n)
#FAR_grid = np.linspace(FAR_min, FAR_max, FAR_n)


T_grid = np.array( [ 300., 350., 400., 450., 500., 550., 600., 650., 700., 750., 800., 850., 900., 950., 1000., 1050., 1100., 1150., 1200., 1250., 1300., 1350., 1400., 1450., 1500., 1550., 1600., 1650., 1700., 1750., 1800., 1850., 1900., 1950., 2000., 2050., 2100., 2150., 2200., 2250., 2300., 2350., 2400., 2450., 2500., 2550., 2600., 2650., 2700., 2750., 2800., 2850., 2900., 2950., 3000., 3050., 3100., 3150., 3200., 3250., 3300., 3350., 3400., 3450., 3500., 3550., 3600., 3650., 3700., 3750., 3800., 3850., 3900., 3950.] )
P_grid = np.array ([1., 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 10., 10.1, 20.1, 30.1, 40.1, 50.1, 60.1, 70.1, 80.1, 90.1, 100.1, 150.1, 200.1, 250.1, 300.1, 350.1, 400.1, 450.1, 500.1, 550.1, 600.1, 650.1, 700.1, 750.1, 800.1, 850.1, 900.1, 950.1])
FAR_grid = np.array( [0., 0.0025, 0.005, 0.0075, 0.01, 0.0125, 0.015, 0.0175, 0.02, 0.0225, 0.025, 0.0275, 0.03, 0.0325, 0.035, 0.0375, 0.04, 0.0425, 0.045, 0.0475, 0.05, .0525, .055, .0575, .06, .0625, .065 ])



FAR_n = len( FAR_grid )
T_n = len( T_grid )
P_n = len( P_grid )

# ---------------------------------------------------------------------------
# Cantera setup
# ---------------------------------------------------------------------------

air = ct.Solution("air.yaml")  # ideal-gas air mixture

gas = ct.Solution("gri30.yaml")
gasair = ct.Solution("air.yaml")

# ---------------------------------------------------------------------------
# Compute all properties on the grid in a single pass
# ---------------------------------------------------------------------------

h_TPt = np.empty((FAR_n, P_n, T_n))
Cp_TPt = np.empty((FAR_n, P_n, T_n))
gam_TPt = np.empty((FAR_n, P_n, T_n))
rho_TPt = np.empty((FAR_n, P_n, T_n))
r_TPt = np.empty((FAR_n, P_n, T_n))
s_TPt = np.empty((FAR_n, P_n, T_n))

for i, far in enumerate(FAR_grid):
    for j, p in enumerate(P_grid):
        for k, t in enumerate(T_grid):
            gas.set_mixture_fraction(
                far / (1 - far),
                fuel=fuel_comp,
                oxidizer=oxidizer_comp,
                basis="mass",
            )
            print( far,p,t )
            gas.TP = t * 5.0 / 9.0, p * 6894.76
            gas.equilibrate("TP")            
            mw = gas.molecular_weights  # kg/kmol
            h_TPt[i, j, k] = gas.h*0.0004299226
            Cp_TPt[i, j, k] = gas.cp*0.0002390057
            gam_TPt[i, j, k] = gas.cp / gas.cv
            rho_TPt[i, j, k] = gas.density*0.062428
            r_TPt[i, j, k] = 8.314 / gas.mean_molecular_weight * 0.0002390057 * 1000.0
            s_TPt[i, j, k] = gas.s*0.0002390057

print("All properties computed.")

# ---------------------------------------------------------------------------
# Save to NPZ
# ---------------------------------------------------------------------------

output_dir = os.path.dirname(__file__)
output_path = os.path.join(output_dir, "newtherm_data.npz")

np.savez(
    output_path,
    T_TP=T_grid,
    P_TP=P_grid,
    FAR_TP=FAR_grid,
    h_TPt=h_TPt,
    Cp_TPt=Cp_TPt,
    gam_TPt=gam_TPt,
    rho_TPt=rho_TPt,
    r_TPt=r_TPt,
    s_TPt=s_TPt,
)

print(f"Saved air2_data.npz to {output_path}")
print(f"Grid shapes: T={T_grid.shape}, P={P_grid.shape}, FAR={FAR_grid.shape}")
for name in ["h_TPt", "Cp_TPt", "gam_TPt", "rho_TPt", "r_TPt", "s_TPt"]:
    arr = eval(name)
    print(f"  {name}: shape={arr.shape}, min={arr.min():.4e}, max={arr.max():.4e}")
