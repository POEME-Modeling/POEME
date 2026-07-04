# ------------------------------------------------------
#                    DUCT COMPONENT TEST
# ------------------------------------------------------
import time
start_time = time.time()

import numpy

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
    FlightConditions,
    FlowStart,
    Inlet,
    Nozzle,
    Perf,
    Shaft,
    Splitter,
    Turbine,
)

from poeme.core.print import print_pretty


session = ModelSession()

with session:
    # ---------------------------------------------------------------------------
    # create instances all of the component objects in this model
    # --------------------------------------------------------------------------
    start = FlowStart("start")
    #start = FlightConditions("start")
    duct = Duct("duct")

    # add the solver
    solver = Newton("solver")

    # set up an output object and a file to write that output
    estuff = Output("estuff")
    estuff.filename = "duct_test.out"



# --------------------------------------
# link the objects together
# --------------------------------------
duct.FNi.link_fn(start.FNo)



# --------------------------------------
# set component variable values
# --------------------------------------
# use cantera or NewTherm tables for fluid properties
#start.comp = "CanteraFN"
start.comp = "Newtherm"
start.W = 100.0
start.Pt = 40.0
start.Tt = 650.0
start.FNo.MN = 0.40

#start.W = 100.0
#start.MN = 0.40
#start.alt = 0.0

duct.FNo.MN = 0.40
duct.dPqPdes = 0.10
duct.Q = 100.0
duct.dPswitch = 'varies'


# --------------------------------------
# method to print the test results
# --------------------------------------
def print_testResults():
    #print(
    #    "----- CASE", case_counter["count"],
    #    "     MN", f"{start.MN.v:4.2f}",  "-----",
    #    "     Q =", f"{start.Qdyn.v:5.1f}", "psf      velocity =", f"{start.VTAS.v:7.2f}", 
    #    "     area =", f"{duct.FNo.A.v:5.3f}", "     MN =", f"{duct.FNo.MN.v:6.4f}",
    #    "     Pt loss =", f"{duct.dPqP.v:6.4f}",
    #)
    print(
        "----- CASE", case_counter["count"],
        "     MN", f"{start.FNo.MN.v:4.2f}",  "-----",
        "     area =", f"{duct.FNo.A.v:5.3f}", "     MN =", f"{duct.FNo.MN.v:6.4f}",
        "     Pt loss =", f"{duct.dPqP.v:6.4f}",
    )


# --------------------------------------
# check that everything's ready to run
# --------------------------------------
session.check()
output_file = open("duct_test.out", "w")



# --------------------------------------
# run the tests
# --------------------------------------
case_counter = {"count": 1}

solver.solve()
#print_pretty( output_file, session)
#print_testResults()


session.set("size", False) # this is setting the code from DESIGN (sizing) mode to OFF-DESIGN mode


# --------------------------------------
# TEST 1: dP/P constant, heat added
# --------------------------------------
print( 'RUNNING TEST 1' )
case_counter = {"count": 1}

duct.dPswitch = "constant"

for Wset in numpy.arange( 100., 39., -20. ):
    start.W = Wset
    duct.Q = 100.0

    solver.solve()
    print_pretty( output_file, session )
    print_testResults()
    case_counter["count"] += 1


# reset
duct.Q = 0.;
print( ' ' )


# --------------------------------------
# TEST 2: dP/P varies with Wc
# --------------------------------------
print( 'RUNNING TEST 2' )
case_counter = {"count": 1}

duct.dPswitch = "varies"

for Wset in numpy.arange( 100., 39., -20. ):
    start.W = Wset
    #duct.Q = 100.0

    solver.solve()
    print_pretty( output_file, session )
    print_testResults()
    case_counter["count"] += 1

