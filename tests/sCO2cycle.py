# ------------------------------------------------------
#       TRANSIENT BRAYTON CYCLE RUNNING CANTERA
#
# this model is transient model of ground based turbo
# power generator
# it includes an example of a PIV controller
# thermo properties are generated using the cantera package
# the cantera setup can be found in the brayton sub-directory
#
# run the model by giving the command:
#
# python brayton_cantera.py
#
# the fuel enthalpies are defined using the CEA methodology
# see:
# https://ntrs.nasa.gov/api/citations/20020085330/downloads/20020085330.pdf
# the ouptut file is
#
# estuff.out (trace.out)
# pop.out (detailed point data)
# ------------------------------------------------------

# load in the required POEME objects
from poeme import ModelSession, Newton, Output, RealT, Independent
from poeme.brayton import (
    MP,
    PIV,
    Burner,
    Compressor,
    Duct,
    FlowStart,
    FlowStartEnd,
    Nozzle,
    Perf,
    Shaft,
    Turbine,
    Heatx
)
from poeme.core.print import print_stdout

with ModelSession() as session:
    # create the components and set their values and link them up
    FS = FlowStartEnd("FS")

    FS.Pt = 511.
    FS.Tt = 1135.
    FS.W = 1000.0

    # start the model off with CanteraFN
    # this package is an interface between poeme
    # and cantera
    # the thermo properties are function of FAR
    # the the interface can be seen in the file
    # canter_fn.py in the brayton subdirectory
    FS.comp = "CPPROPS"
    FS.fname = "CO2"

    D1 = Duct("D1")
    D1.dPqP = 0.05
    D1.FNi.link_fn(FS.FNo)  

    C1 = Compressor("C1")
    C1.PRdes = 2.7
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
    C1.effTable.data = [[0.90, 0.93, 0.90], [0.92, 0.95, 0.92], [0.89, 0.92, 0.88]]
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
    
    FShx = FlowStartEnd("FShx")
    FShx.Pt = 511.
    FShx.Tt = 1135.
    FShx.W = 1000.0
    FShx.comp = "CPPROPS"
    FShx.fname = "CO2"
 
    FShx.ind_Pt.active = True
    FShx.ind_Tt.active = True
    
    H1 = Heatx( "H1" )
    H1.eff = .95
    H1.FNi1.link_fn(C1.FNo) 
    H1.FNi2.link_fn(FShx.FNo) 
    H1.FNo2.link_fn(FS.FNi)
    
    B1 = Duct("B1")
    B1.Q = 40000.
    B1.FNi.link_fn(H1.FNo1) 

    T1 = Turbine("T1")
    T1.effDes = 0.95
    T1.FNi.link_fn(B1.FNo)
    T1.FNiBld1.link_fn(C1.FNoBld2)
    T1.FNiBld2.link_fn(C1.FNoBld1)
    T1.effTable.x = [0.8, 0.9, 1.1]
    T1.effTable.y = [2.0, 3.0, 6.0]
    T1.effTable.data = [[0.90, 0.91, 0.87], [0.92, 0.95, 0.90], [0.89, 0.92, 0.88]]
    T1.WcTable.x = [0.8, 0.9, 1.1]
    T1.WcTable.y = [1.0, 3.0, 6.0]
    T1.WcTable.data = [[21.6, 21.6, 21.6], [19.4, 19.4, 19.4], [17.3, 17.3, 17.3]]
    T1.NcMapDes = 0.9
    T1.PRmapDes = 3.0
    T1.PR = 1.5
    # T1.FNo.MN.set( .3 )
    
    D1 = Duct("D1")
    D1.Q = -40000.
    D1.FNi.link_fn(T1.FNo) 
    
    FShx.FNi.link_fn(D1.FNo)

    S1 = Shaft("S1")
    S1.MPC = MP(S1, io="in")
    S1.MPT = MP(S1, io="in")
    S1.N = 10000.0
    S1.MPC.link_mp(C1.MP)
    S1.MPT.link_mp(T1.MP)
    S1.HPX=1000.
    S1.I = 6.0

    #P1 = Perf("P1")

    # create a solver
    solver = Newton("solver")

    # create a trace file
    estuff = Output("estuff")
    estuff.filename = "estuff.out"
    estuff.vars = [session.solver.time ]

    D1.ind_Q = Independent(
        D1,
        indname="Q",
        perturb=0.05,
        scale=100,
        perturb_type="Relative",
        active=True,
        session=session,
    )
    
    B1.ind_Q = Independent(
        B1,
        indname="Q",
        perturb=0.05,
        scale=100,
        perturb_type="Relative",
        active=True,
        session=session,
    )
    
# check the system including setting up the solver
session.check()
    
# solver the sizing point
solver.solve()
output_file = open( "pop.out" )
