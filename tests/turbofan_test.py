# ------------------------------------------------------
#        SIMPLE TURBOFAN CYCLE PERFORMANCE MODEL
# run the model by giving the command:
#
# python turbofan_test.py
#
# the ouptut file is
#
# turbofan.out
#
# this model load in two local elements from the subdirecoty
# tomstuff, compressortom and ducttom.  The elements show
# the minimum amount of data required for a functional element
#
# this file has four different thermo options to
# choose the appropiate thermo set the composition
# in the start element to want you want and then go
# down to the burner element and sent the appropiate
# value for the fuel enthalpy.
# start.comp = "jetatherm"  <---------new table create by user
# use tables for fluid properties
# start.comp = "jetatherm" <---------jeta and air
# start.comp = "ch4therm"  <---------liquid methane and air
#  start.comp = "h2therm"  <---------hydogen and air
#
# the fuel enthalpies are defined using the CEA methodology
# see:
# https://ntrs.nasa.gov/api/citations/20020085330/downloads/20020085330.pdf
# ------------------------------------------------------
import time

# Get the custom modules
# this is an exmaple of including your own elements
# look in the directory tomstuff to see these components
# this components are simplified to show thebare minum
# required to create a element
from tomstuff.compressortom import CompressorTom
from tomstuff.ducttom import DuctTom

# load in the required POEME objects
from poeme import (
    Constraint,
    Dependent,
    Independent,
    ModelSession,
    Newton,
    Output,
    RealT,
)
from poeme.brayton import (
    MP,
    Burner,
    Compressor,
    Duct,
    FlightConditionsSMJ,
    Inlet,
    Nozzle,
    Perf,
    Shaft,
    Splitter,
    Turbine,
)
from poeme.core.print import print_pretty

# start time for timing check
start_time = time.time()

# create a session for the model
session = ModelSession()


with session:
    # ---------------------------------------------------------------------------
    # create all of the component objects, including the shaft connection ports
    # --------------------------------------------------------------------------
    start = FlightConditionsSMJ("start")
    inlet = Inlet("inlet")
    fan = Compressor("fan")
    splitter = Splitter("splitter")
    duct2 = DuctTom("duct2")
    LPC = Compressor("LPC")
    duct25 = Duct("duct25")
    HPC = CompressorTom("HPC")
    duct3 = Duct("duct3")
    burner = Burner("burner")
    HPT = Turbine("HPT")
    duct45 = Duct("duct45")
    LPT = Turbine("LPT")
    duct5 = Duct("duct5")
    pri_nozzle = Nozzle("pri_nozzle")

    duct17 = Duct("duct17")
    fan_nozzle = Nozzle("fan_nozzle")
    hp_shaft = Shaft("HPshaft")
    lp_shaft = Shaft("LPshaft")

    lp_shaft.MPfan = MP(lp_shaft, io="in")
    lp_shaft.MPlpc = MP(lp_shaft, io="in")
    lp_shaft.MPlpt = MP(lp_shaft, io="in")

    hp_shaft.MPC = MP(hp_shaft, io="in")
    hp_shaft.MPT = MP(hp_shaft, io="in")

    perf = Perf("Perf")

# --------------------------------------
# link the objects together
# -------------------------------------
inlet.FNi.link_fn(start.FNo)
fan.FNi.link_fn(inlet.FNo)
splitter.FNi.link_fn(fan.FNo)
duct17.FNi.link_fn(splitter.FNo2)
fan_nozzle.FNi.link_fn(duct17.FNo)
duct2.FNi.link_fn(splitter.FNo1)
LPC.FNi.link_fn(duct2.FNo)
duct25.FNi.link_fn(LPC.FNo)
HPC.FNi.link_fn(duct25.FNo)
duct3.FNi.link_fn(HPC.FNo)
burner.FNi.link_fn(duct3.FNo)
HPT.FNi.link_fn(burner.FNo)
duct45.FNi.link_fn(HPT.FNo)
LPT.FNi.link_fn(duct45.FNo)
duct5.FNi.link_fn(LPT.FNo)
pri_nozzle.FNi.link_fn(duct5.FNo)

lp_shaft.MPfan.link_mp(fan.MP)
lp_shaft.MPlpc.link_mp(LPC.MP)
lp_shaft.MPlpt.link_mp(LPT.MP)

hp_shaft.MPC.link_mp(HPC.MP)
hp_shaft.MPT.link_mp(HPT.MP)

HPT.FNiBld2.link_fn(HPC.FNoBld1)
HPT.FNiBld1.link_fn(duct3.FNobld)
LPT.FNiBld1.link_fn(HPC.FNoBld2)

# ------------------------------------------------------------------------
# set component variable values to match N+3 reference cycle at SLS
# Mach numbers that are only used for sizing are commented out
# they have no effect on the cycle convergence
# ------------------------------------------------------------------------
start.alt = 35000.0
start.MN = 0.80
start.W = 813.51

# use tables for fluid properties
# the thermo is tabular function of thermo properties as a function of FAR
# (see the Brayton directory)
# start.comp = "jetatherm"
# use tables for fluid properties
start.comp = "jetatherm"
# start.comp = "ch4therm"
# start.comp = "h2therm"

inlet.rec = 0.99570  # inlet recovery 0.998; SMJ: lower to match N+3 fan entrance
# inlet.FNo.MN = 0.625

fan.PRdes = 1.300
fan.effDes = 0.9689
fan.NcMapDes = 1.000
fan.RlineDes = 2.000
# fan.NcMapDes = 1.00
# fan.RlineDes = 2.00
# fan.FNo.MN = 0.45

splitter.BPR = 23.9878
# splitter.FNo1.MN = 0.45
# splitter.FNo2.MN = 0.45

# duct2.FNo.MN = 0.45
duct2.dPswitch = "varies"
duct2.dPqPdes = 0.0100

LPC.PRdes = 3.000
LPC.effDes = 0.8894
LPC.NcMapDes = 1.10
LPC.RlineDes = 2.00
# LPC.FNo.MN = 0.45

duct25.dPswitch = "varies"
duct25.dPqPdes = 0.015
# duct25.FNo.MN = 0.45

HPC.PRdes = 14.1030
HPC.effDes = 0.8469
HPC.NcMapDes = 1.00
HPC.RlineDes = 2.00
HPC.Wfrac1 = 0.0693
HPC.hfract1 = 1.00
HPC.Wfrac2 = 0.02
HPC.hfract2 = 0.5
# HPC.FNo.MN = 0.30


duct3.Wbldfrac = 2.0354 / (31.91 - 2.2566)

# https://ntrs.nasa.gov/api/citations/20020085330/downloads/20020085330.pdf
burner.FAR = 0.02833
# Jet A fuel enthalpy (L) @ 298.15I
burner.hFuel = -303.403 / 167.311 * 429.9226
# CH4 fuel enthalpy (L) @ 111.64 K
# burner.hFuel = -89.233/16.04*429.9226
# H2 liquid fuel enthalpy (L) @ 20.27 K
# burner.hFuel=-9.012/2.01588*429.9226
burner.FAR = 0.01

burner.FAR = 0.02833
burner.dP = 0.0400
# burner.FNo.MN = 0.10
# print( burner.desc )

HPT.PRmapDes = 3.0
HPT.PR = 4.0
HPT.effDes = 0.9313
HPT.NcMapDes = 1.00
# HPT.FNo.MN = 0.30

duct45.dPswitch = "varies"
duct45.dPqPdes = 0.005
# duct45.FNo.MN = 0.45

LPT.PRmapDes = 6.0
LPT.PR = 10.0
LPT.effDes = 0.9410
LPT.NcMapDes = 0.9
# LPT.FNo.MN = 0.35

duct5.dPswitch = "varies"
duct5.dPqPdes = 0.010
# duct5.FNo.MN = 0.25

pri_nozzle.PsExh = "start.Pamb"
pri_nozzle.Cfg = 0.999

duct17.dPswitch = "varies"
duct17.dPqPdes = 0.015
# duct17.FNo.MN = 0.45

fan_nozzle.PsExh = "start.Pamb"
fan_nozzle.Cfg = 0.9975

hp_shaft.N = 20871.0
hp_shaft.I = 6.0
hp_shaft.HPX = 350.0

lp_shaft.N = 6772.0
lp_shaft.I = 6.0


# fmt: off
# =======================================================================
#                           Fan Map
# =======================================================================
fan.WcTable.x = [0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1., 1.05]
fan.WcTable.y = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5]
fan.WcTable.data = [
    [386.838,552.308,670.769,762.906,830.598,898.29,965.982],
    [544.786,659.487,766.667,855.043,918.974,982.905,1046.84],
    [693.333,781.709,881.368,956.581,1018.63,1080.68,1142.73],
    [830.598,911.453,996.068,1060,1114.53,1152.14,1182.22],
    [965.983,1037.44,1116.41,1165.3,1221.71,1249.91,1263.08],
    [1037.44,1108.89,1184.1,1227.35,1280,1304.44,1313.85],
    [1120.17,1191.62,1259.32,1300.68,1343.93,1364.61,1370.26],
    [1214.19,1280,1332.65,1368.38,1394.7,1402.22,1403.34],
    [1327.01,1374.02,1404.1,1428.55,1441.71,1449.23,1451.11],
    [1358.97,1405.98,1436.07,1460.51,1468.03,1469.91,1471.8],
]


fan.effTable.x = [0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1., 1.05]
fan.effTable.y = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5]
fan.effTable.data =[
    [0.6982,0.8757,0.8322,0.4826,0.1873,-0.108,-0.4033],
    [0.7344,0.8522,0.8902,0.7906,0.6583,0.526,0.3937],
    [0.7743,0.8467,0.8975,0.8703,0.7562,0.6421,0.528],
    [0.7797,0.8449,0.8848,0.8938,0.8377,0.6837,0.4609],
    [0.7797,0.8304,0.8739,0.8902,0.8848,0.7417,0.6402],
    [0.7797,0.8322,0.8721,0.8884,0.8902,0.787,0.6638],
    [0.787,0.8322,0.8721,0.8902,0.8975,0.8377,0.6647],
    [0.7924,0.8377,0.8685,0.8884,0.892,0.8848,0.8812],
    [0.8268,0.8576,0.8721,0.8775,0.8703,0.8649,0.863],
    [0.8069,0.8286,0.8413,0.8377,0.8268,0.825,0.8214,]
]
fan.PRtable.x = [0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1., 1.05]
fan.PRtable.y = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5]
fan.PRtable.data =[
    [1.091,1.084,1.06,1.005,0.9419,0.8788,0.8157],
    [1.147,1.142,1.121,1.079,1.019,0.959,0.899],
    [1.212,1.212,1.193,1.16,1.114,1.068,1.022],
    [1.302,1.298,1.284,1.267,1.221,1.153,1.065],
    [1.402,1.414,1.405,1.388,1.351,1.288,1.177],
    [1.467,1.486,1.481,1.465,1.428,1.377,1.263],
    [1.553,1.567,1.565,1.551,1.521,1.465,1.34],
    [1.647,1.663,1.658,1.64,1.602,1.519,1.388],
    [1.765,1.763,1.747,1.716,1.677,1.593,1.467],
    [1.8,1.795,1.781,1.753,1.702,1.626,1.498],
]

# =======================================================================
#                           LPC map
# =======================================================================

LPC.WcTable.x = [0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1., 1.05]
LPC.WcTable.y = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5]
LPC.WcTable.data = [
    [35.0194,37.8114,40.0302,40.0522,44.9029,82.9728,104.814],
    [45.147,48.5087,53.1232,55.4665,61.3755,99.8114,123.605],
    [63.5718,67.5315,72.9752,76.1212,82.2407,118.968,141.298],
    [79.9223,86.1794,93.0473,98.2561,106.034,136.661,156.184],
    [104.692,113.502,120.215,125.872,134.221,155.696,170.704],
    [114.82,125.038,132.534,139.093,147.765,164.725,177.171],
    [128.608,138.357,147.328,155.561,164.115,176.561,186.689],
    [143.86,151.547,158.715,165.822,174.121,186.811,197.793],
    [162.529,168.256,174.959,181.288,187.665,198.891,208.286],
    [179.002,184.074,189.678,194.982,200.355,209.14,217.316],
]
LPC.effTable.x = [0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1., 1.05]
LPC.effTable.y = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5]
LPC.effTable.data =[
    [0.816,0.826951,0.833772,0.837974,0.8503,0.9043,0.6074],
    [0.7939,0.815116,0.83194,0.845061,0.8589,0.8871,0.6221],
    [0.8503,0.859344,0.869592,0.879282,0.8847,0.8773,0.6933],
    [0.8393,0.856467,0.871084,0.884611,0.8945,0.8883,0.7178],
    [0.8552,0.873068,0.88469,0.895957,0.9031,0.8785,0.7632],
    [0.8601,0.876483,0.889037,0.8969,0.8957,0.8724,0.7681],
    [0.8736,0.886619,0.894547,0.900156,0.9043,0.9031,0.8994],
    [0.8699,0.880708,0.888177,0.893678,0.8982,0.9018,0.8969],
    [0.8859,0.891232,0.892813,0.89508,0.8969,0.8834,0.8638],
    [0.8871,0.890711,0.894132,0.893397,0.8859,0.8724,0.8564],
]
LPC.PRtable.x = [0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1., 1.05]
LPC.PRtable.y = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5]
LPC.PRtable.data =[
    [1.0997,1.10062,1.10071,1.10196,1.1016,1.085,1.0489],
    [1.1446,1.15038,1.1566,1.16341,1.1642,1.1358,1.0762],
    [1.2336,1.23876,1.24343,1.24763,1.2433,1.2023,1.127],
    [1.3205,1.32826,1.33383,1.34026,1.3371,1.2805,1.1925],
    [1.4534,1.46113,1.46247,1.4624,1.4505,1.3782,1.2824],
    [1.5121,1.5223,1.52421,1.52141,1.5042,1.43,1.3342],
    [1.5902,1.59707,1.60117,1.59749,1.5746,1.5052,1.4163],
    [1.6743,1.67051,1.66207,1.64817,1.6244,1.5775,1.5257],
    [1.7642,1.75774,1.74561,1.73028,1.7104,1.6752,1.6362],
    [1.8404,1.82915,1.81821,1.80632,1.7906,1.7642,1.7349],
]

# =======================================================================
#                           HPC map
# =======================================================================

HPC.WcTable.x = [0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1., 1.05]
HPC.WcTable.y = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5]
HPC.WcTable.data = [
    [8.9682,9.15046,9.63145,10.1389,10.4763,10.635,10.9524],
    [14.0476,14.4643,14.8908,15.2659,15.5556,15.7937,15.9524],
    [19.127,19.7781,20.1502,20.3929,20.6349,20.9524,20.9524],
    [27.1429,28.1108,28.3904,28.4577,28.6508,28.9683,29.127],
    [42.4603,42.9373,44.0477,45.0683,45.6349,46.2698,46.5873],
    [52.3016,53.3801,54.134,54.6985,55.1587,55.4762,55.7143],
    [68.8889,70.0952,70.9301,71.5376,71.9841,72.1429,72.381],
    [92.4603,94.2695,95.6782,96.7567,97.4603,97.4603,97.4603],
    [122.143,122.573,122.947,123.283,123.571,123.73,123.968],
    [137.223,137.59,137.619,137.675,138.017,138.65,138.412],
]
HPC.effTable.x = [0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1., 1.05]
HPC.effTable.y = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5]
HPC.effTable.data =[
    [0.6313,0.634372,0.632666,0.628111,0.6104,0.539,0.5506],
    [0.6453,0.647829,0.648466,0.645385,0.6306,0.5809,0.5615],
    [0.6593,0.661287,0.664265,0.662659,0.6508,0.6228,0.5724],
    [0.688,0.700359,0.702816,0.701376,0.6966,0.6756,0.6492],
    [0.754,0.758199,0.767657,0.774187,0.7734,0.7703,0.7517],
    [0.7641,0.783882,0.791627,0.794062,0.7936,0.782,0.7587],
    [0.7734,0.795649,0.805223,0.808814,0.8107,0.8092,0.7828],
    [0.7882,0.807149,0.818516,0.824836,0.8278,0.827,0.8022],
    [0.7835,0.80112,0.812218,0.818687,0.8216,0.82,0.8022],
    [0.7571,0.749135,0.746801,0.747612,0.7486,0.7456,0.7246],
]
HPC.PRtable.x = [0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1., 1.05]
HPC.PRtable.y = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5]
HPC.PRtable.data =[
    [1.3345,1.30298,1.30995,1.27272,1.1825,1.2129,1.1215],
    [2.2769,2.2271,2.1916,2.12143,2.0033,1.9121,1.6688],
    [3.2193,3.15121,3.07326,2.97015,2.8241,2.6113,2.2161],
    [4.861,4.65701,4.44265,4.289,4.1618,3.7666,3.1889],
    [7.6884,7.61302,7.44917,7.30059,7.1412,6.6243,5.6515],
    [10.2117,9.8417,9.48737,9.211,8.9349,8.2356,7.202],
    [13.6775,13.2689,12.8283,12.3962,11.9446,11.2757,9.9989],
    [19.4235,19.1148,18.7104,18.1704,17.4473,16.4745,14.9544],
    [27.0239,26.4773,25.872,25.1264,24.1357,22.7372,21.5212],
    [31.0369,30.4771,29.7238,29.1328,28.5135,26.3246,25.1694],
]



# =======================================================================
#                                 HPT map
# =======================================================================
#  6 speeds
# 20 index (pressure ratio)

HPT.WcTable.x = [0.40, 0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.95, 1.00, 1.05]
HPT.WcTable.y = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 4.75, 4.96, 5.25, 5.5, 5.75, 6.0]
HPT.WcTable.data = [
    [16.007,16.041,16.041,16.041,16.041,16.041,16.041,16.041,16.041,16.041,16.041,16.041],
    [15.781,16.025,16.025,16.025,16.025,16.025,16.025,16.025,16.025,16.025,16.025,16.025],
    [15.523,15.966,15.986,15.986,15.986,15.986,15.986,15.986,15.986,15.986,15.986,15.986],
    [15.358,15.87,15.964,15.964,15.964,15.964,15.964,15.964,15.964,15.964,15.964,15.964],
    [15.249,15.749,15.894,15.907,15.907,15.907,15.907,15.907,15.907,15.907,15.907,15.907],
    [15.2318,15.7098,15.8634,15.8872,15.8876,15.8876,15.8876,15.8876,15.8876,15.8876,15.8876,15.8876],
    [15.226,15.674,15.828,15.862,15.863,15.863,15.863,15.863,15.863,15.863,15.863,15.863],
    [15.2126,15.6247,15.7735,15.8127,15.8152,15.8152,15.8152,15.8152,15.8152,15.8152,15.8152,15.8152],
    [15.208,15.581,15.72,15.761,15.765,15.765,15.765,15.765,15.765,15.765,15.765,15.765],
    [15.2265,15.5612,15.6873,15.7265,15.7313,15.7313,15.7313,15.7313,15.7313,15.7313,15.7313,15.7313],
]
HPT.effTable.x = [0.40, 0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.95, 1.00, 1.05]
HPT.effTable.y = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 4.75, 4.96, 5.25, 5.5, 5.75, 6.0]
HPT.effTable.data = [
    [0.806,0.79,0.776,0.765,0.755,0.746,0.742,0.739,0.736,0.732,0.729,0.726],
    [0.847,0.843,0.837,0.83,0.822,0.816,0.813,0.81,0.807,0.804,0.802,0.799],
    [0.865,0.873,0.874,0.871,0.867,0.862,0.86,0.858,0.856,0.854,0.851,0.849],
    [0.868,0.887,0.895,0.895,0.894,0.892,0.891,0.89,0.888,0.886,0.885,0.883],
    [0.86,0.889,0.903,0.908,0.91,0.91,0.909,0.909,0.908,0.907,0.906,0.905],
    [0.85225,0.887,0.903875,0.911,0.91375,0.9155,0.915,0.914875,0.91375,0.91325,0.912875,0.912375],
    [0.843,0.883,0.903,0.912,0.916,0.919,0.919,0.919,0.918,0.918,0.918,0.918],
    [0.83225,0.876625,0.90025,0.910625,0.91675,0.920125,0.920625,0.92125,0.920625,0.92125,0.921125,0.92175],
    [0.82,0.869,0.896,0.908,0.916,0.92,0.921,0.922,0.922,0.923,0.923,0.924],
    [0.806125,0.860125,0.89025,0.904,0.913625,0.9185,0.920125,0.921,0.92225,0.923125,0.923625,0.924625,]
]
# =======================================================================
#                                 LPT map
# =======================================================================

LPT.WcTable.x = [0.40, 0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.95, 1.00, 1.05]
LPT.WcTable.y = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 4.75, 4.96, 5.25, 5.5, 5.75, 6.0]
LPT.WcTable.data = [
    [81.16,81.16,81.16,81.16,81.16,81.16,81.16,81.16,81.16,81.16,81.16,81.16],
    [80.944,81.14,81.14,81.14,81.14,81.14,81.14,81.14,81.14,81.14,81.14,81.14],
    [79.536,81.031,81.031,81.031,81.031,81.031,81.031,81.031,81.031,81.031,81.031,81.031],
    [77.681,80.45,80.884,80.884,80.884,80.884,80.884,80.884,80.884,80.884,80.884,80.884],
    [75.817,79.203,80.278,80.588,80.635,80.635,80.635,80.635,80.635,80.635,80.635,80.635],
    [74.8914,78.4206,79.6869,80.1487,80.3067,80.3694,80.3863,80.396,80.4057,80.4116,80.4156,80.4184],
    [73.988,77.577,78.968,79.558,79.834,79.9695,80.007,80.0294,80.052,80.066,80.076,80.083],
    [73.1408,76.7307,78.1969,78.8637,79.2046,79.3877,79.4426,79.4778,79.5148,79.5387,79.5571,79.5702],
    [72.301,75.84,77.339,78.05,78.43,78.6459,78.714,78.7594,78.808,78.84,78.865,78.883],
    [71.4307,74.8806,76.3808,77.1115,77.5111,77.7417,77.8145,77.8628,77.9144,77.9472,77.9725,77.99,]
]
LPT.effTable.x = [0.40, 0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.95, 1.00, 1.05]
LPT.effTable.y = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 4.75, 4.96, 5.25, 5.5, 5.75, 6.0]
LPT.effTable.data = [
    [0.767,0.739,0.718,0.702,0.688,0.676965,0.672,0.668666,0.663,0.659,0.656,0.652],
    [0.827,0.81,0.794,0.779,0.767,0.756334,0.752,0.748632,0.744,0.74,0.737,0.733],
    [0.863,0.857,0.845,0.834,0.824,0.814768,0.811,0.807597,0.804,0.8,0.797,0.795],
    [0.88,0.886,0.88,0.872,0.864,0.857158,0.854,0.851476,0.848,0.845,0.842,0.839],
    [0.885,0.901,0.901,0.896,0.891,0.886547,0.884,0.882356,0.879,0.877,0.874,0.872],
    [0.883125,0.903875,0.907625,0.903875,0.9005,0.896876,0.895,0.893237,0.890375,0.888375,0.886625,0.8845],
    [0.879,0.905,0.912,0.91,0.908,0.905351,0.904,0.902332,0.9,0.898,0.897,0.895],
    [0.87225,0.904375,0.91375,0.9145,0.91325,0.911928,0.910875,0.909619,0.908,0.90575,0.90475,0.90325],
    [0.864,0.902,0.914,0.917,0.917,0.91674,0.916,0.915166,0.914,0.912,0.911,0.91],
    [0.85425,0.897875,0.91275,0.917,0.91925,0.91946,0.919,0.918719,0.9175,0.91675,0.915625,0.91525,]
]
# fmt: on

# --------------------------------------
# declare some output
# -------------------------------------
with session:
    estuff = Output("estuff")

estuff.filename = "turbofan.out"
estuff.vars = [start.alt, start.MN, start.W, perf.Fn, perf.Wfuel]


burner.ind_FAR = Independent(
    burner,
    indname="FAR",
    perturb=0.05,
    perturb_type="Relative",
    active=True,
    desc="Varies FAR",
)


# create an burner exit temperature variable for the engine to balance to
burner.Tset = RealT(burner, v=3200.0)

# create a dependent that will match the burner exit temp to desired value
burner.dep_Tset = Dependent(burner, d2name="Tset", d1name="FNo.Tt", active=True)

# --------------------------------------
# run the DESIGN case
# -------------------------------------
# check the model
# this also will case the model to load in
# the default solver independents that are
# needed for the sizing mode
session.check()

# create a Newton solver for this model
with session:
    solver = Newton("solver")
session.solver = solver

# list the current balances to the screen
solver.listBalances()

# activate this line if you want to turn the solver
# debug on
# solver.debug = True

# tell model to solve itsellf
solver.solve()

# the burner temperature match is only for the sizing point
burner.ind_FAR.active = False
burner.dep_Tset.active = False


# open a file for the output
output_file = open("turbofan.out", "w")

# print the standard output for the model
print_pretty(output_file, session)

_case_counter = {"count": 0}


# create a function to run a throtte hook
def run_throttle_hook(mnset, altitude):

    _case_counter["count"] += 1
    # full power run to a corrrected fan speed of 1.0
    fan.NcDem = 1.0
    # set the conditions
    start.MN = mnset
    start.alt = altitude

    # run the model at full power
    solver.run()

    # save the solver values to reload later
    solver.save_independents()

    # print the output
    print_pretty(output_file, session)

    # update progress to screen
    print(
        start.MN, start.alt, burner.FAR, perf.Fn, "1.000", fan.NcMap, solver.converged
    )

    # save off the full power net thrust
    perf.FnetMax = RealT(perf)
    perf.FnetMax = perf.Fn

    _case_counter["count"] += 1

    # save off the full power solver state to restore later
    solver.save_independents()
    factor = 1.0

    # turn off the full power settings
    fan.dep_NmechC.active = False
    burner.con_1.on = False
    burner.con_1.active = False
    burner.ind_FAR.active = False
    # session.check()

    # loop through the part power cases as long as thrust is greater
    # that 20% thrust, the solver is converged and the primary
    # nozzle is producing positive thrust
    while factor > 0.2 and solver.converged == True and pri_nozzle.Fg > 0.0:
        # step the burner FAR down
        burner.FAR = burner.FAR - 0.0025
        # run the model
        solver.run()
        # print the otuput to a file
        print_pretty(output_file, session)
        # determine the thrust fractio
        factor = (perf.Fn) / perf.FnetMax
        # print info to the screen
        print(
            start.MN,
            start.alt,
            burner.FAR,
            perf.Fn,
            factor,
            fan.NcMap,
            solver.converged,
        )
        _case_counter["count"] += 1

    # return the solver to full power for the point so
    # the starting point is good for the next full power
    # call

    # drive the fan to 100% speed at full power
    fan.dep_NmechC.active = True
    # turn the burner temperature constraint on
    # if it looks like it will be violated the solver
    # run to the burner max temperature instead of getting
    # 100% fan speed
    burner.con_1.on = True
    burner.ind_FAR.active = True

    # session.check()
    fan.NcDem = 1.0

    # reload the full power converged independent values
    solver.restore_independents()
    solver.run()
    _case_counter["count"] += 1


# this is setting the code from DESIGN (sizing) mode to OFF-DESIGN mode
session.set("size", False)


# create and independent to vary the fan nozzle area
# this will be used to prevent the fan from stalling
fan_nozzle.ind_Area = Independent(
    fan_nozzle,
    indname="Anoz",
    perturb=0.05,
    scale=100,
    perturb_type="Relative",
    active=True,
)

# ------------------------------------------
# set the model up for off design mode
# ------------------------------------------

# create an Rline demand variable for the engine balance too
fan.RlineSet = RealT(fan, v=2.0)

# create a dependent that will match the current Rline to the demand
# value
fan.dep_Rline = Dependent(fan, d2name="RlineSet", d1name="Rline", active=True)

# configure the model including adding the appropiate auto-balances
session.check()
# display for the user
solver.listBalances()
# run the model with at the same point as the sizing case
# the model should not move
solver.run()
# print the output
print_pretty(output_file, session)

# create a new fan variable which is the speed the fans is driving too
fan.NcDem = RealT(fan)
fan.NcDem = 1.0

# create a new burner variable for the burner max temperatuyre
burner.Tmax = RealT(burner)
burner.Tmax = 3600.0

# start.Fdem = RealT(start)
# start.Fnet = RealT(start)

# create an independent that allows the solver to vary burner
# FAR
burner.ind_FAR = Independent(
    burner,
    indname="FAR",
    perturb=0.05,
    perturb_type="Relative",
    active=True,
    desc="Varies FAR",
)

# Create a dependent that matchest the current fan map corrected
# speed to the desired fan map speed
fan.dep_NmechC = Dependent(
    fan, d1name="NcMap", d2name="NcDem", active=True, desc="Handles weight flow error"
)

# create a constrating that sets a max temperature at Tmax
# if the the burner exceeds this value, the the depedent that
# makes the solver drive the corrected speed to 1.0 is dropped
# and replaced with a dependent that drive the burner to max
# temperature
burner.con_1 = Constraint(
    burner, d1name="burner.Tmax", d2name="FNo.Tt", depname="fan.dep_NmechC", on=True
)


session.check()

# run the flight envelope by performing different
# throttle hooks
run_throttle_hook(0.90, 45000.0)
run_throttle_hook(0.85, 45000.0)
run_throttle_hook(0.80, 45000.0)
run_throttle_hook(0.75, 45000.0)
run_throttle_hook(0.70, 45000.0)

run_throttle_hook(0.60, 40000.0)
run_throttle_hook(0.70, 40000.0)
run_throttle_hook(0.75, 40000.0)
run_throttle_hook(0.80, 40000.0)
run_throttle_hook(0.85, 40000.0)
run_throttle_hook(0.90, 40000.0)

run_throttle_hook(0.90, 36089.0)
run_throttle_hook(0.85, 36089.0)
run_throttle_hook(0.80, 36089.0)
run_throttle_hook(0.75, 36089.0)
run_throttle_hook(0.70, 36089.0)
run_throttle_hook(0.60, 36089.0)

run_throttle_hook(0.50, 30000.0)
run_throttle_hook(0.60, 30000.0)
run_throttle_hook(0.70, 30000.0)
run_throttle_hook(0.75, 30000.0)
run_throttle_hook(0.80, 30000.0)
run_throttle_hook(0.85, 30000.0)

run_throttle_hook(0.80, 25000.0)
run_throttle_hook(0.75, 25000.0)
run_throttle_hook(0.70, 25000.0)
run_throttle_hook(0.60, 25000.0)
run_throttle_hook(0.50, 25000.0)

run_throttle_hook(0.40, 20000.0)
run_throttle_hook(0.50, 20000.0)
run_throttle_hook(0.60, 20000.0)
run_throttle_hook(0.70, 20000.0)
run_throttle_hook(0.75, 20000.0)

run_throttle_hook(0.70, 15000.0)
run_throttle_hook(0.60, 15000.0)
run_throttle_hook(0.50, 15000.0)
run_throttle_hook(0.40, 15000.0)
run_throttle_hook(0.30, 15000.0)

run_throttle_hook(0.60, 10000.0)
run_throttle_hook(0.50, 10000.0)
run_throttle_hook(0.40, 10000.0)

run_throttle_hook(0.00, 5000.0)
run_throttle_hook(0.10, 5000.0)
run_throttle_hook(0.20, 5000.0)
run_throttle_hook(0.25, 5000.0)
run_throttle_hook(0.30, 5000.0)
run_throttle_hook(0.40, 5000.0)
run_throttle_hook(0.50, 5000.0)

run_throttle_hook(0.50, 2000.0)
run_throttle_hook(0.40, 2000.0)
run_throttle_hook(0.30, 2000.0)
run_throttle_hook(0.25, 2000.0)
run_throttle_hook(0.20, 2000.0)
run_throttle_hook(0.10, 2000.0)
run_throttle_hook(0.00, 2000.0)

run_throttle_hook(0.50, 0.0)
run_throttle_hook(0.40, 0.0)
run_throttle_hook(0.30, 0.0)
run_throttle_hook(0.25, 0.0)
run_throttle_hook(0.20, 0.0)
run_throttle_hook(0.10, 0.0)
run_throttle_hook(0.00, 0.0)

print(
    time.time() - start_time,
    _case_counter["count"],
    (time.time() - start_time) / _case_counter["count"],
)
