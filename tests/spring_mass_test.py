# ------------------------------------------------------
#       SIMPLE SPRING MASS SYSTEM
#
# this is a model of a mass attached to a spring
# and a damper
#
# run the model by giving the command:
#
# python sprint_mass_test.py
#
# the ouptut file is
#
# 1mass.out
# ------------------------------------------------------
from poeme import ModelSession, Newton, Output
from poeme.spring_mass import Damper, Fp, Mass, Spring, Wall

with ModelSession() as session:
    # declare the elements
    W1 = Wall("W1")
    W1.xloc = 0.0
    # create ports for the spring and damper
    W1.Fp1 = Fp(W1, "in", "")
    W1.Fp2 = Fp(W1, "in", "")

    S1 = Spring("S1")
    S1.k = 0.1
    S1.LN = 3.0

    D1 = Damper("Damper")
    D1.c = 0.01

    M1 = Mass("Mass")
    M1.mass = 1.0
    M1.xloc = 3.0

    # create ports for the spring and damper
    M1.Fp1 = Fp(M1, "in", "")
    M1.Fp2 = Fp(M1, "in", "")

    # link the spring
    S1.Fp1.link_fp(W1.Fp1)
    S1.Fp2.link_fp(M1.Fp1)

    # link the damper
    D1.Fp1.link_fp(W1.Fp2)
    D1.Fp2.link_fp(M1.Fp2)

    # set the model up
    session.check()

    # declare some output files
    output_file = open("pop.out", "w")

    # create a sovler
    solver = Newton("solver", output_file)
    session.solver = solver

    estuff = Output("estuff")
    estuff.filename = "1mass.out"
    estuff.vars = [solver.time, S1.L, M1.xloc]

    # run the steady state initial point
    solver.solve()

    # configure the model for transient operatio
    session.set("trans", True)
    solver.timeLast = 100.0
    solver.dtime = 0.01

    # perturb the mass so it oscillates
    M1.xloc = M1.xloc + 1.0

    solver.trim()

    # run the transient
    solver.run()
