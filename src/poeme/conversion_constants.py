
# CONSTANTS and CONVERSIONS

'''
# constants
C_GRAVITY = 32.1740486
C_C = 299792458*3.2808084
C_Pstd = 14.696
C_Tstd = 518.67


# standard to standard conversions
C_DEGtoRAD = PI/180.0
C_FTtoIN = 12.0
C_FT2toIN2 = 144.0
C_RPMtoRADperSEC = PI/30.0
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
C_RtoK = 5./9.
C_LBMtoKG = 0.45359237
C_FT_LBFtoJ = 1.35581795
C_BTUtoJ = C_BTUtoFT_LBF*C_FT_LBFtoJ
C_BTUperSECtoKW = C_BTUtoFT_LBF*C_FT_LBFtoJ / 1000.0
C_FTperSECtoKMperHR = 1.09728
'''

all fluid nodes always calculate statics
if size = True
   if MN < 0.00001
      area = -999
      statics = totals
   else
      statics and area iterated using input MN
      areaDes = area
if size = False
   if MN < 0.00001
      area = -999
      statics = totals
   else
      statics and MN iterated using input areaDes
