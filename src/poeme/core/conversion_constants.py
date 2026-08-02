import math

# CONSTANTS and CONVERSIONS

# constants
C_GRAVITY = 32.1740486
C_c = 299792458 * 3.2808084
C_Pstd = 14.696
C_Tstd = 518.67


# standard to standard conversions
C_DEGtoRAD = math.pi / 180.0
C_FTtoIN = 12.0
C_FT2toIN2 = 144.0
C_RPMtoRADperSEC = math.pi / 30.0
C_BTUperSECtoHP = 1.414284
C_BTUtoFT_LBF = 778.16926
C_HPtoFT_LBFperSEC = 550.0
C_KNOTtoFTperSEC = 1.68780986
C_SLUGtoLBM = 32.1740486
C_LBFtoLBM_FTperSEC2 = 32.1740486


# standard to SI conversions
C_FTtoM = 0.3048
C_LBFtoN = 4.44822162
C_PSItoPa = 6894.75729
C_RtoK = 5.0 / 9.0
C_LBMtoKG = 0.45359237
C_FT_LBFtoJ = 1.35581795
C_BTUtoJ = C_BTUtoFT_LBF * C_FT_LBFtoJ
C_BTUperSECtoKW = C_BTUtoFT_LBF * C_FT_LBFtoJ / 1000.0
C_FTperSECtoKMperHR = 1.09728

C_JOULES_PER_KG_TO_BTU_PER_LB = 0.0004299226 # J/kg -> BTU/lb
C_JOULES_PER_KG_KELVIN_TO_BTU_PER_LB_RANKINE = 0.0002390057  # J/kg*K -> BTU/lb*degR
C_KG_PER_METER_CUBED_TO_LB_PER_FEET_CUBED = 0.062428  # kg/m^3 -> lb/ft^3

# Auto-generated list of public constants for __all__
__all__ = [name for name in dir() if name.startswith("C_")]
