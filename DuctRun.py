from Independent import Independent
from Dependent import Dependent
from solver import solver
from Start import Start
from Duct import Duct
from HookeJeeves import HookeJeeves
from stdOut import stdOut

import varsg

S1 = Start( "S1" )
S1.Tt.v = 600
S1.Pt.v = 100
S1.W.v = 500
S1.comp.v = "air"

D1 = Duct( "D1" )
D1.dPn.v = .05
S1.FPo.linkFP( D1.FPi )

#mike vary these

#Independents
#ind_1 = Independent("ind_E1.Vr", E1.Vr, 1, False)
#ind_2 = Independent("ind_E1.Vi", E1.Vi, 1, False)

#Dependents
#dep_1 = Dependent("dep_E1.Inetr", E1.Inetr, E1.InetDr)
#dep_2 = Dependent("dep_E1.Ineti", E1.Ineti, E1.InetDi)


###
#element_list = varsg.element_list
#ind_list = varsg.ind_list
#dep_list = varsg.dep_list
###

for e in varsg.element_list:
	e.calc()
	

stdOut.print()

