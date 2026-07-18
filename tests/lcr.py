# ------------------------------------------------------
#       SIMPLE CIRCUIT MODEL
#
# this is a model of a simple inductor capacitor resistor
# circuit
# run the model by giving the command:
#
# python lcr.py
#
# the ouptut file is
#
# pretty.out
# ------------------------------------------------------
from poeme import Constraint, ModelSession, Newton, Output
from poeme.core.print import print_pretty, print_stdout
from poeme.electrical import Capacitor, Enode, Esource, Inductor, Resistor

session = ModelSession()

with session:
    
    # create the elements
    R = Resistor("R")
    R.R = 470.0

    C1 = Capacitor("C1")
    C1.C = 4.7 * 10**-6

    I1 = Inductor("I1")
    I1.L = 65.0 * 10.0**-2

    C2 = Capacitor("C2")
    C2.C = 1.5 * 10**-6

    S1 = Esource("S1")
    S1.Vr = 120.0

    E1 = Enode("E1")
    E1.Vr = -50.0
    E1.Vi = 10.0

    E2 = Enode("E2")
    E2.Vr = -50.0
    E2.Vi = 10.0

    S2 = Esource("S2")

    # set the AC frequency for the system
    session.set("freq", 60.0)

    # link the model
    C1.EPi.link_e(S1)
    C1.EPo.link_e(E1)
    I1.EPi.link_e(E1)
    I1.EPo.link_e(E2)
    C2.EPi.link_e(E2)
    C2.EPo.link_e(S2)
    R.EPi.link_e(E1)
    R.EPo.link_e(S2)
    
    # create an output file
    estuff = Output("estuff")
    estuff.filename = "estuff.out"
    estuff.vars = []

    E1.con_1 = Constraint(
        E1, d1name="E1.IinIp1", d2name="E1.IoutI", depname="E1.dep_2", active=False
    )
    E1.con_2 = Constraint(
        E1, d1name="E1.IinIp2", d2name="E1.IoutI", depname="E1.dep_2", active=False
    )

    # set the model to run
    session.check()

    # create a Newton Rhapson solver
    solver = Newton("session.solver")

# run the model
solver.run()

print("converged", solver.converged)

# dump some output
output_file = open("pop.out", "w")
print_stdout(output_file, session)
pretty_file = open("pretty.out", "w")
print_pretty(pretty_file, session)
