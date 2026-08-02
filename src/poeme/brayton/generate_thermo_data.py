"""Generate thermo data.npz file for generic fuel/oxidizer property lookups.

This module computes equilibrium thermodynamic properties (specific enthalpy,
specific heat at constant pressure, specific heat ratio, density, gas constant,
and specific entropy) on a 3D parameter grid of temperature, pressure, and
fuel-air-ratio (FAR). The equilibrium state is obtained via Cantera's
``equilibrate('TP')`` method, which finds the composition that minimizes Gibbs
free energy at fixed temperature and pressure.

Computations are performed over a dense low-pressure grid (1-10 psi) for
accuracy in subsonic / low-supersonic combustor regimes, with sparse sampling
above 10 psi to capture high-pressure turbine conditions without an excessive
number of evaluation points. A pre-generated ``.npz`` file is consumed by
``poeme.brayton`` components (e.g., ``burner``, ``turbine``) through bidirectional
linear / bilinear interpolation.

Grid specifications
-------------------
T (temperature):
    300-3950 °R in steps of 50 °R → 74 points.
    Covers cold-air startup (300 °R ≈ 167 K) through typical flame temperatures
    (~3950 °R ≈ 2194 K).
P (pressure):
    1-10.1 psi in steps of 0.1 → 91 points.
    Then sparse sampling at 20.1, 30.1, …, 950.1 psi in steps of 50 → 7 points.
    Total: 98 points. Dense at low pressure, sparse at high.
FAR (fuel-air ratio by mass):
    0.0-0.065 in steps of 0.0025 → 27 points.
    Covers stoichiometric ~0.06 for JP-7 / air mixtures.

Output arrays are stored in ``(FAR, pressure, temperature)`` indexing order to
match the iteration loop and the expected axis ordering downstream.

Compositional fuels & oxidizers
-------------------------------
Each composition is expressed as **mass fractions**. Known compositions:
    h2: pure hydrogen (100% H)
    ch4: methane (C 12.01, H 4.04 — approximate elemental mass ratios)
    jp7 / jeta: Jet-A / JP-7 surrogate (C 0.845, H 0.145; remainder trace)
    jp: JP-4 surrogate (C 1.0, H 0.16667)
    air: dry air (O₂ 21.53%, N₂ 75.2%, Ar 1.28%, CO₂ 0.06%)

Custom compositions may be supplied as JSON objects at runtime.

CLI usage
---------
The script is executable directly. The default invocation generates data for
an input + air using the GRI-Mech 3.0 reaction mechanism:

    python generate_thermo_data.py ch4         # ch4 + air, gri30.yaml

Custom fuel / oxidizer / output:

    python generate_thermo_data.py h2 air mechanism.yaml -o h2_air.npz
"""

import json
import os

import cantera as ct
import numpy as np

from poeme.core import (
    C_JOULES_PER_KG_KELVIN_TO_BTU_PER_LB_RANKINE,
    C_JOULES_PER_KG_TO_BTU_PER_LB,
    C_KG_PER_METER_CUBED_TO_LB_PER_FEET_CUBED,
    C_RtoK,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# TODO: VALIDATE THESE AS MASS VS MOLE FRACTIONS (can do either, which is preferred?)
CH4 = {"C": 12.01, "H": 4.04}
H2 = {"H": 1.0}
JET_A = JP_7 = {"C": 0.845, "H": 0.145}
JP = {"C": 1.0, "H": 0.16667}

AIR = {
    "O2": 0.2153,
    "N2": 0.752,
    "AR": 0.0128,
    "CO2": 0.0006,
}  # Mass fractions for dry air

COMPOSITIONS = {
    "h2": H2,
    "ch4": CH4,
    "jp7": JP_7,
    "jeta": JET_A,
    "jp": JP,
    "air": AIR,
}
"""Known fuel and oxidizer compositions keyed by short name.

Each value is a ``dict[str, float]`` mapping element (or species) symbol
to its **mass fraction**.  Valid keys: ``h2``, ``ch4``, ``jp7``, ``jeta``,
``jp``, ``air``.  Additional entries may be added at runtime.
"""


# ---------------------------------------------------------------------------
# Grid definitions
# ---------------------------------------------------------------------------

# fmt: off
# Temperature: Rankine; Pressure: psi
T_grid = np.array([300.0, 350.0, 400.0, 450.0, 500.0, 550.0, 600.0, 650.0, 700.0, 750.0, 800.0, 850.0, 900.0, 950.0, 1000.0, 1050.0, 1100.0, 1150.0, 1200.0, 1250.0, 1300.0, 1350.0, 1400.0, 1450.0, 1500.0, 1550.0, 1600.0, 1650.0, 1700.0, 1750.0, 1800.0, 1850.0, 1900.0, 1950.0, 2000.0, 2050.0, 2100.0, 2150.0, 2200.0, 2250.0, 2300.0, 2350.0, 2400.0, 2450.0, 2500.0, 2550.0, 2600.0, 2650.0, 2700.0, 2750.0, 2800.0, 2850.0, 2900.0, 2950.0, 3000.0, 3050.0, 3100.0, 3150.0, 3200.0, 3250.0, 3300.0, 3350.0, 3400.0, 3450.0, 3500.0, 3550.0, 3600.0, 3650.0, 3700.0, 3750.0, 3800.0, 3850.0, 3900.0, 3950.0]) # noqa: E501
"""Temperature grid in Rankine (°R)."""

P_grid = np.array([1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 10.0, 10.1, 20.1, 30.1, 40.1, 50.1, 60.1, 70.1, 80.1, 90.1, 100.1, 150.1, 200.1, 250.1, 300.1, 350.1, 400.1, 450.1, 500.1, 550.1, 600.1, 650.1, 700.1, 750.1, 800.1, 850.1, 900.1, 950.1]) # noqa: E501
"""Pressure grid in pounds per square inch (psi).

Dense sampling from 1 to 10 psi (step 0.1) for combustor-regime accuracy,
followed by sparse sampling every 50 psi up to 950 psi.
"""

FAR_grid = np.array([0.0, 0.0025, 0.005, 0.0075, 0.01, 0.0125, 0.015, 0.0175, 0.02, 0.0225, 0.025, 0.0275, 0.03, 0.0325, 0.035, 0.0375, 0.04, 0.0425, 0.045, 0.0475, 0.05, 0.0525, 0.055, 0.0575, 0.06, 0.0625, 0.065]) # noqa: E501
# fmt: on
"""Fuel-air ratio grid (mass basis)."""

FAR_n = len(FAR_grid)
"""Number of FAR grid points."""

T_n = len(T_grid)
"""Number of temperature grid points."""

P_n = len(P_grid)
"""Number of pressure grid points."""


def _validate_thermo_inputs(input_data):
    """Resolve a fuel or oxidizer specification to its composition dictionary.

    Accepts either a known short-name string, a raw JSON string (which is
    parsed into a dictionary), or an already-constructed ``dict``.  This
    indirection allows CLI users to type ``h2`` while also supporting arbitrary
    custom compositions without modifying the code.

    Parameters
    ----------
    input_data : str | dict[str, float]
        A known composition key (e.g., ``"h2"``, ``"air"``), a JSON-encoded
        dictionary string, or a ``dict`` mapping element/species symbols to
        mass fractions.

    Returns
    -------
    dict[str, float]
        A composition dictionary suitable for passing to
        ``Cantera.Solution.set_mixture_fraction``.

    Raises
    ------
    ValueError
        If *input_data* is a string that does not match a known key and
        fails JSON parsing.
    TypeError
        If *input_data* is neither a string nor a dict.
    """
    if isinstance(input_data, str):
        if input_data in COMPOSITIONS:
            return COMPOSITIONS[input_data]
        try:
            return json.loads(input_data)
        except (json.JSONDecodeError, TypeError):
            error_str = f"{input_data!r} is not a known fuel/oxidizer or valid JSON."
            raise ValueError(error_str) from None
    if isinstance(input_data, dict):
        return input_data
    error_str = f"Expected str or dict, got {type(input_data).__name__}"
    raise TypeError()


def _name_from_composition(input):
    """Derive a filesystem-safe filename stem from a composition dictionary.

    Converts each key-value pair into ``keyvalue`` tokens joined by underscores,
    producing names like ``O20.2153N20.752`` for dry air.  This is used as a
    fallback when the user does not supply an explicit ``--output`` name.

    Parameters
    ----------
    input : dict | str | object
        A dictionary mapping element/species symbols to values.
        Also accepts a non-dict object whose string representation is
        formatted in the same way (for backward compatibility).

    Returns
    -------
    str
        A filename-safe stem such as ``O20.2153N20.752AR0.0128CO20.0006``.
    """
    if isinstance(input, dict):
        return "_".join(f"{k}{v}" for k, v in input.items())
    return (
        str(input)
        .replace("{", "")
        .replace("}", "")
        .replace(":", "")
        .replace(" ", "")
        .replace(",", "_")
    )


def generate_thermo_data(fuel, oxidizer, model, output=None):
    """Compute equilibrium thermodynamic properties and save results as an NPZ file.

    Iterates over the full 3D grid (FAR, P, T), invoking Cantera's Gibbs-free-
    energy minimization at each point via ``equilibrate('TP')``.  The following
    six properties are recorded:

    +-------------+--------------------------+-----------------------------------+
    | Key         | Unit (output)            | Description                       |
    +-------------+--------------------------+-----------------------------------+
    | h_TPt       | BTU / lb                 | Specific enthalpy                 |
    +-------------+--------------------------+-----------------------------------+
    | Cp_TPt      | BTU / (lb·°R)           | Specific heat at constant pressure|
    +-------------+--------------------------+-----------------------------------+
    | gam_TPt     | dimensionless            | Specific heat ratio              |
    |             | (γ = Cp / Cv)           |                                   |
    +-------------+--------------------------+-----------------------------------+
    | rho_TPt     | lb / ft³                 | Mass density                      |
    +-------------+--------------------------+-----------------------------------+
    | r_TPt       | BTU / (lb·°R) × 1000    | Specific gas constant (×1000)     |
    +-------------+--------------------------+-----------------------------------+
    | s_TPt       | BTU / (lb·°R)           | Specific entropy                  |
    +-------------+--------------------------+-----------------------------------+

    Grid array order is ``(FAR_index, pressure_index, temperature_index)`` to
    match the nested iteration loop.

    Parameters
    ----------
    fuel : str | dict[str, float]
        Fuel specification. Accepts a known short name (``"h2"``,
        ``"ch4"``, ``"jp7"``, ``"jeta"``, ``"jp"``), a JSON string, or a
        ``dict`` of elemental mass fractions.
    oxidizer : str | dict[str, float]
        Oxidizer specification. Accepts ``"air"`` (default), a JSON
        string, or a ``dict``.
    model : cantera.Solution
        A Cantera ``Solution`` object representing the reaction mechanism
        (e.g., ``ct.Solution('gri30.yaml')``).  The same object is mutated
        in-place via ``set_mixture_fraction`` and ``equilibrate`` at each
        grid point; no deep copy is made.
    output : str | None, optional
        Optional output filename. If ``None``, the file is named as
        ``{fuel_stem}_{oxidizer_stem}.npz`` where stems are derived from the
        composition dictionaries (see :func:`_name_from_composition`).
        The default is ``None``.

    Returns
    -------
    None
        Results are printed to stdout and written to disk.

    Raises
    ------
    ValueError
        If *fuel* or *oxidizer* cannot be resolved to a valid composition.
    TypeError
        If either argument has an unsupported type.

    Notes
    -----
    Unit conversions applied after each Cantera evaluation (SI → Imperial):

    - Enthalpy :math:`[J/kg] \\rightarrow [BTU/lb]`
    - Specific heat :math:`[J/(kg\\cdot K)] \\rightarrow [BTU/(lb\\cdot ^\\circ R)]`
    - Density :math:`[kg/m^3] \\rightarrow [lb/ft^3]`
    - Gas constant is computed from the mean molecular weight and scaled by
      1000 for numerical stability during interpolation.

    Total grid evaluations:

    .. math::
       N_{{\\text{FAR}}} \\times N_P \\times N_T = 27 \\times 98 \\times 74 
       = 195,756

    On a typical laptop with GRI-Mech 3.0 (325 species, 1836 reactions),
    the full grid takes approximately 2-4 hours.

    Examples
    --------
    >>> model = ct.Solution('gri30.yaml')  # doctest: +SKIP
    >>> generate_thermo_data('ch4', 'air', model)  # doctest: +SKIP
    All properties computed.
    Saved ch4_air.npz to /path/to/generate_ch4_air.npz
    >>> generate_thermo_data('ch4', 'air', model)  # doctest: +SKIP
    All properties computed.
    Saved ch4_air.npz to /path/to/generate_ch4_air.npz
    """
    # Validate inputs
    fuel_comp = _validate_thermo_inputs(fuel)
    oxidizer_comp = _validate_thermo_inputs(oxidizer)

    # Set up empty results arrays
    h_TPt = np.empty((FAR_n, P_n, T_n))  # noqa: N816
    Cp_TPt = np.empty((FAR_n, P_n, T_n))
    gam_TPt = np.empty((FAR_n, P_n, T_n))  # noqa: N816
    rho_TPt = np.empty((FAR_n, P_n, T_n))  # noqa: N816
    r_TPt = np.empty((FAR_n, P_n, T_n))  # noqa: N816
    s_TPt = np.empty((FAR_n, P_n, T_n))  # noqa: N816

    # Iterate through and run calculations
    for i, far in enumerate(FAR_grid):
        for j, p in enumerate(P_grid):
            for k, t in enumerate(T_grid):
                model.set_mixture_fraction(
                    far / (1 - far),
                    fuel=fuel_comp,
                    oxidizer=oxidizer_comp,
                    basis="mass",
                )
                model.TP = (
                    t * C_RtoK,
                    p * 6894.76,
                )  # Convert Rankine to Kelvin; psi to pascal
                model.equilibrate("TP")
                h_TPt[i, j, k] = model.h * C_JOULES_PER_KG_TO_BTU_PER_LB
                Cp_TPt[i, j, k] = (
                    model.cp * C_JOULES_PER_KG_KELVIN_TO_BTU_PER_LB_RANKINE
                )
                gam_TPt[i, j, k] = model.cp / model.cv  # unitless
                rho_TPt[i, j, k] = (
                    model.density * C_KG_PER_METER_CUBED_TO_LB_PER_FEET_CUBED
                )
                r_TPt[i, j, k] = (
                    8.314
                    / model.mean_molecular_weight
                    * C_JOULES_PER_KG_KELVIN_TO_BTU_PER_LB_RANKINE
                    * 1000.0
                )  # BTU/lb*degF
                s_TPt[i, j, k] = model.s * C_JOULES_PER_KG_KELVIN_TO_BTU_PER_LB_RANKINE

    print("All properties computed.")

    # ---------------------------------------------------------------------------
    # Save to NPZ
    # ---------------------------------------------------------------------------

    if output is None:
        fuel_name = _name_from_composition(fuel)
        oxidizer_name = _name_from_composition(oxidizer)
        filename = f"{fuel_name}_{oxidizer_name}.npz"
    else:
        filename = output
    save_path = os.path.join(os.path.dirname(__file__), filename)

    np.savez(
        save_path,
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

    print(f"Saved {os.path.basename(save_path)} to {save_path}")
    print(f"Grid shapes: T={T_grid.shape}, P={P_grid.shape}, FAR={FAR_grid.shape}")

    props = {
        "h_TPt": h_TPt,
        "Cp_TPt": Cp_TPt,
        "gam_TPt": gam_TPt,
        "rho_TPt": rho_TPt,
        "r_TPt": r_TPt,
        "s_TPt": s_TPt,
    }

    for name, arr in props.items():
        print(f"  {name}: shape={arr.shape}, min={arr.min():.4e}, max={arr.max():.4e}")


if __name__ == "__main__":
    """CLI entry point for generating thermodynamic equilibrium data.

    This script computes equilibrium properties over a 3D grid of
    temperature, pressure, and fuel-air-ratio using Cantera's Gibbs
    free energy minimization, then saves the results as an NPZ file
    for downstream interpolation by ``poeme.brayton`` components.

    Usage::

        python generate_thermo_data.py <fuel> [oxidizer] [-o OUTPUT.npz] [-m mechanism.yaml]

    Parameters
    ----------
    fuel : str
        Fuel name or JSON composition. Known values: h2, ch4, jp7, jeta, jp.
    oxidizer : str, optional
        Oxidizer name or JSON composition. Known values: air.
        The default is "air".
    -o OUTPUT : str, optional
        Output NPZ filename. The default is ``<fuel>_<oxidizer>.npz``.
    -m MODEL : str, optional
        Cantera YAML mechanism file. The default is gri30.yaml.

    Examples
    --------
    Generate CH\\u2084/air data using GRI-Mech 3.0::

        python generate_thermo_data.py ch4 air -o ch4_air.npz

    Generate H\\u2082/air data with a custom mechanism::

        python generate_thermo_data.py h2 "O2:1.0,N2:3.76" -m my_mech.yaml

    Generate JP-7/argon mixture::

        python generate_thermo_data.py jp "Ar:1.0" -o jp_ar.npz
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate thermodynamic data for a fuel/oxidizer pair."
    )
    parser.add_argument(
        "fuel",
        help="Fuel name or JSON composition (known: h2, ch4, jp7, jeta, jp)",
    )
    parser.add_argument(
        "oxidizer",
        default="air",
        nargs="?",
        help="Oxidizer name or JSON composition (known: air; default: air)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output NPZ name (default: <fuel>_<oxidizer>.npz)",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="gri30.yaml",
        help="Cantera YAML model file (default: gri30.yaml)",
    )
    args = parser.parse_args()

    model = ct.Solution(args.model)
    generate_thermo_data(args.fuel, args.oxidizer, model=model, output=args.output)
