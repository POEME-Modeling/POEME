import sys

from popclean import Independent, ModelSession, Newton
from popclean.brayton import Compressor, Duct, FlowStartEnd2D
from popclean.pop.print import print_pretty, print_stdout

session = ModelSession()
with session:
    FSE = FlowStartEnd2D("FSE")
FSE.Pt = 29.00
FSE.comp = "CPR134"
FSE.FNo.twoPhase = True
FSE.FNo.comp = "CPR134"

FSE.FNo.set_tp(600.0, 29.0)
print(FSE.FNo.ht)
FSE.FNo.set_hp(FSE.FNo.ht, 29.0)
print(FSE.FNo.ht)
FSE.FNo.set_hp(FSE.FNo.ht - 1.0, 145.0)
print(FSE.FNo.Tt)
FSE.FNo.set_hp(FSE.FNo.ht - 1.0, 145.0)
print(FSE.FNo.Tt)
while True:
    FSE.FNo.set_hp(FSE.FNo.ht - 1.0, 145.0)
    print(FSE.FNo.Tt)

sys.exit()

sys.exit()

FSE.FNo.set_tp(473.0, 20.30)
FSE.ht = FSE.FNo.ht
FSE.W = 40.0

Comp = Compressor("Comp")

Condensor = Duct("Condesor")
Condensor.dP = 0.0
Condensor.Q = -100.0

Valve = Duct("Valve")
Valve.dP = 1.0 - 1.4 / 9.0

Evap = Duct("Evap")
Evap.dP = 0.00
Evap.Q = +50.0

Comp.PRdes = 9.0 / 1.4
Comp.effDes = 0.89
Comp.MP.set_n(6000.0)
Comp.NcMapDes = 0.9
Comp.RlineDes = 2.0
Comp.effTable.x = [0.8, 0.95, 1.1]
Comp.effTable.y = [1.0, 2.0, 3.0]
Comp.effTable.data = [[0.90, 0.93, 0.90], [0.92, 0.95, 0.92], [0.89, 0.92, 0.88]]
Comp.PRtable.x = [0.8, 0.95, 1.1]
Comp.PRtable.y = [1.0, 2.0, 3.0]
Comp.PRtable.data = [
    [6.183, 4.572, 2.455],
    [16.044, 17.705, 7.148],
    [37.995, 27.657, 14.535],
]

Comp.WcTable.x = [0.8, 0.95, 1.1]
Comp.WcTable.y = [1.0, 2.0, 3.0]
Comp.WcTable.data = [
    [32.496, 34.173, 35.169],
    [68.234, 72.934, 74.243],
    [118.945, 126.124, 126.182],
]

FSE.FNo.link_fn(Comp.FNi)
Comp.FNo.link_fn(Condensor.FNi)
Condensor.FNo.link_fn(Valve.FNi)
Valve.FNo.link_fn(Evap.FNi)
Evap.FNo.link_fn(FSE.FNi)

Comp.ind_PRdes = Independent(
    Comp,
    indname="PRdes",
    perturb=0.05,
    scale=100,
    perturb_type="Relative",
    active=True,
    desc="Varies R-line",
    session=session,
)

Evap.ind_Q = Independent(
    Evap,
    indname="Q",
    perturb=0.05,
    scale=100,
    perturb_type="Relative",
    active=True,
    desc="Varies R-line",
    session=session,
)

solver = Newton("solver")
session.solver = solver
session.check()

solver.solve()
solver.solve()
solver.solve()
solver.solve()
solver.solve()
solver.solve()

print_stdout("pop.out")
print_pretty("pretty.out")
