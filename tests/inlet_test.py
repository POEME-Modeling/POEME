# ------------------------------------------------------
#                    INLET COMPONENT TEST
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
    start = FlightConditions("start")
    inlet = Inlet("inlet")

    # add the solver
    solver = Newton("solver")

    # set up an output object and a file to write that output
    estuff = Output("estuff")
    estuff.filename = "inlet_test.out"



# --------------------------------------
# link the objects together
# --------------------------------------
inlet.FNi.link_fn(start.FNo)



# --------------------------------------
# set component variable values
# --------------------------------------
# use cantera or NewTherm tables for fluid properties
#start.comp = "CanteraFN"
start.comp = "Newtherm"
start.alt = 35000.0
start.MN = 0.80
start.W = 100.



# --------------------------------------
# method to print the test results
# --------------------------------------
def print_testResults():
    print(
        "----- CASE", case_counter["count"],
        "     MN", f"{start.MN.v:4.2f}", "     altitude", f"{start.alt.v:6.0f}", "ft ", "-----",
        "     Q =", f"{start.Qdyn.v:5.1f}", "psf      speed =", f"{start.VTAS.v:7.2f}", 
        "     Pt recovery =", f"{inlet.rec.v:6.4f}",
    )



# --------------------------------------
# vary altitude to a target flight dynamic pressure
# --------------------------------------
start.ind_ALT = Independent( start, indname="alt", perturb=0.05, perturb_type="Relative",
    active=False, desc="Varies altitude", session=session,
)
start.dep_Q = Dependent( start, d1name="start.Qdyn", d2name="start.Qdemand", active=False,
    desc="Target dynamic pressure",
)

start.Qdemand = RealT(start)
start.Qdemand = 1000.0



# --------------------------------------
# check that everything's ready to run
# --------------------------------------
session.check()
output_file = open("inlet_test.out", "w")



# --------------------------------------
# run the tests
# --------------------------------------

# --------------------------------------
# TEST 1: recovery input
# --------------------------------------
inlet.recoverySwitch = "Input"

print( 'RUNNING TEST 1' )
case_counter = {"count": 1}

for MNset in numpy.arange( 0.0, 1.70, 0.2 ):
    start.MN = MNset
    inlet.rec = 1.0 - MNset/10.

    solver.solve()
    print_pretty( output_file, session)
    print_testResults()
    case_counter["count"] += 1

start.ind_ALT.active = True
start.dep_Q.active = True

for MNset in numpy.arange( 1.80, 3.01, 0.2 ):
    start.MN = MNset
    inlet.rec = 1.0 - MNset/10.

    solver.solve()
    print_pretty( output_file, session)
    print_testResults()
    case_counter["count"] += 1


# reset
start.ind_ALT.active = False
start.dep_Q.active = False
start.alt = 35000.
print( ' ' )


# --------------------------------------
# TEST 2: recovery from table
# --------------------------------------
inlet.recoverySwitch = "Table"
inlet.RECtable.x = [  0.00,  0.10,  0.20,  0.30,  0.40,  0.50,  0.60,  0.70,  0.80,  0.90, 3.50 ]
inlet.RECtable.y = [ 0.995, 0.996, 0.997, 0.997, 0.998, 0.998, 0.998, 0.998, 0.998, 0.998, 0.80 ]
inlet.s_rec = 1.000  # scale factor

print( 'RUNNING TEST 2' )
case_counter = {"count": 1}

for MNset in numpy.arange( 0., 1.70, 0.2 ):
    start.MN = MNset

    solver.solve()
    print_pretty( output_file, session)
    print_testResults()
    case_counter["count"] += 1

start.ind_ALT.active = True
start.dep_Q.active = True

for MNset in numpy.arange( 1.80, 3.01, 0.2 ):
    start.MN = MNset

    solver.solve()
    print_pretty( output_file, session)
    print_testResults()
    case_counter["count"] += 1


# reset
start.ind_ALT.active = False
start.dep_Q.active = False
start.alt = 55000.
print( ' ' )


# --------------------------------------
# TEST 3: Mil-Spec recovery
# --------------------------------------
inlet.recoverySwitch = "Mil-Spec"
inlet.s_rec = 1.000  # scale factor

print( 'RUNNING TEST 3' )
case_counter = {"count": 1}

for MNset in numpy.arange( 0., 1.70, 0.2 ):
    start.MN = MNset

    solver.solve()
    print_pretty( output_file, session)
    print_testResults()
    case_counter["count"] += 1

#start.ind_ALT.active = True
#start.dep_Q.active = True

for MNset in numpy.arange( 1.80, 3.01, 0.2 ):
    start.MN = MNset

    solver.solve()
    print_pretty( output_file, session)
    print_testResults()
    case_counter["count"] += 1
