# ------------------------------------------------------
#       TRANSIENT BRAYTON CYCLE RUNNING CANTERA
# run the model by giving the command:
#
# python brayton_cantera.py
#
# the ouptut file is 
#
# estuff.out (trace.out)
# pop.out (detailed point data)
# ------------------------------------------------------

# load in the required POEME objects
from poeme import ModelSession, Newton, Output, RealT
from poeme.brayton import (
    MP,
    PIV,
    Burner,
    Compressor,
    Duct,
    FlowStart,
    Nozzle,
    Perf,
    Shaft,
    Turbine,
)
from poeme.core.print import print_stdout


with ModelSession() as session:
    # create the components and set their values and link them up
    FS = FlowStart("FS")
    FS.Pamb = RealT(FS)
    FS.Pamb = 10.0 

    FS.Pt = 15.0
    FS.Tt = 500.0
    FS.W = 1000.0
    
    # start the model off with CanteraFN
    FS.comp = "CanteraFN"

    D1 = Duct("D1")
    D1.dPqP= 0.05
    D1.FNi.link_fn(FS.FNo)

    C1 = Compressor("C1")
    C1.PRdes = 20.0
    C1.effDes = 0.89
    C1.FNi.link_fn(D1.FNo)
    C1.hfract1 = 0.7
    C1.Wfrac1 = 0.02
    C1.hfract2 = 0.9
    C1.Wfrac2 = 0.03
    C1.NcMapDes = 1.0
    C1.RlineDes = 2.0
    C1.effTable.x = [0.8, 1.0, 1.2]
    C1.effTable.y = [1.0, 2.0, 3.0]
    C1.effTable.data = [[0.90, 0.93, 0.90], 
    [0.92, 0.95, 0.92], 
    [0.89, 0.92, 0.88]]
    C1.PRtable.x = [0.8, 1.0, 1.2]
    C1.PRtable.y = [1.0, 2.0, 3.0]
    C1.PRtable.data = [
        [6.183, 4.572, 2.455],
        [26.044, 17.705, 7.148],
        [37.995, 27.657, 14.535],
    ]

    C1.WcTable.x = [0.8, 1.0, 1.2]
    C1.WcTable.y = [1.0, 2.0, 3.0]
    C1.WcTable.data = [
        [32.496, 34.173, 35.169],
        [68.234, 72.934, 74.243],
        [118.945, 126.124, 126.182],
    ]

    B1 = Burner("B1")
    B1.FAR = 0.025
    B1.LHV = -500.
    B1.FNi.link_fn(C1.FNo)

    T1 = Turbine("T1")
    T1.effDes = 0.95
    T1.FNi.link_fn(B1.FNo)
    T1.FNiBld1.link_fn(C1.FNoBld2)
    T1.FNiBld2.link_fn(C1.FNoBld1)
    T1.effTable.x = [0.8, 0.9, 1.1]
    T1.effTable.y = [2.0, 3.0, 6.0]
    T1.effTable.data = [[0.90, 0.91, 0.87], 
    [0.92, 0.95, 0.90], 
    [0.89, 0.92, 0.88]]
    T1.WcTable.x = [0.8, 0.9, 1.1]
    T1.WcTable.y = [1.0, 3.0, 6.0]
    T1.WcTable.data = [[21.6, 21.6, 21.6], 
    [19.4, 19.4, 19.4], 
    [17.3, 17.3, 17.3]]
    T1.NcMapDes = 0.9
    T1.PRmapDes = 3.0
    T1.PR = 3.5
    # T1.FNo.MN.set( .3 )

    N1 = Nozzle("N1")
    N1.FNi.link_fn(T1.FNo)
    N1.PsExh = "FS.Pamb"

    S1 = Shaft("S1")
    S1.MPC = MP(S1, io="in")
    S1.MPT = MP(S1, io="in")
    S1.N = 10000.0
    S1.MPC.link_mp(C1.MP)
    S1.MPT.link_mp(T1.MP)
    S1.I = 6.0

    P1 = Perf("P1")
    
    # create a solver
    solver = Newton("solver")
    
    # create a trace file
    estuff = Output("estuff")
    estuff.filename = "estuff.out"
    estuff.vars = [session.solver.time, B1.FAR, S1.N, B1.Wfuel, B1.FNo.Tt]

    # check the system including setting up the solver
    session.check()

    # solver the sizing point
    solver.solve()
    
    # create an output file for the sizing point
    output_file = open("pop.out", "w")
    print_stdout(output_file, session)

    # set to offdesign mode
    session.set("size", False)
    
    # reconfigure the system
    session.check()
    # solve at the sizing point in off-design mode
    solver.solve()
    
    # print the output
    print_stdout(output_file, session)

    # increase the FAR incrementally and run some additional points
    B1.FAR = 0.025
    solver.solve()
    print_stdout(output_file, session)

    B1.FAR = 0.026
    solver.solve()
    print_stdout(output_file, session)
    
    B1.FAR = 0.027
    solver.run()
    print_stdout(output_file, session)
    
    B1.FAR = 0.028
    print_stdout(output_file, session)
    solver.run()

    B1.FAR = 0.030
    print_stdout(output_file, session)
    solver.run()

    # walk the model back down
    B1.FAR = 0.028
    solver.run()

    B1.FAR = 0.027
    solver.run()

    B1.FAR = 0.026
    solver.run()

    # add a PIV controller
    PIV1 = PIV("PIV1")
    PIV1.P = 0.00000005 
    # set FAR as what the controller is changing
    PIV1.DPo = "B1.FAR"
    # sense shaft speed
    PIV1.DPi = "S1.N"
    # set the goal for speed at 10500.   
    PIV1.G= 10500.0

    # set the solver up for a transient run
    solver.timeLast = 20.0
    solver.dtime = 0.01
    session.set("trans", True)
    solver.tolerance = 0.0002
    solver.trim()
    solver.run()
