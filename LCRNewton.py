from Independent import Independent
from Dependent import Dependent
from solver import solver
from circuit import *
from HookeJeeves import HookeJeeves
from Newton import Newton
from stdOut import stdOut

import varsg

R1 = Resistor( "R1" )
R1.R.v =  470.
R1.RV.y = [ 470, 470. ]
R1.RV.x = [-100, 100. ]

C = Capacitor( "C" )
C.C.v = 4.7 * (10 ** -6)
C.CVc.x = [-1000., 0., 1000. ]
C.CVc.y = [-1000., 0., 1000. ]
C.CVc.data = [ [4.7 * (10 ** -6),4.7 * (10 ** -6),4.7 * (10 ** -6)], \
               [4.7 * (10 ** -6),4.7 * (10 ** -6),4.7 * (10 ** -6)],\
               	   [4.7 * (10 ** -6),4.7 * (10 ** -6),4.7 * (10 ** -6) ]]
              
I = Inductor( "I" )
I.L.v = 65. * (10 ** -2)

S1 = Enode( "S1" )
S1.Vr.v = 120.

E1 = Enode( "E1" )
E1.Vr.v =  -50
E1.Vi.v = 10

S2 = Enode( "S2" )

setFreq( 60. )
S1.LinkPort(C.EPi)
E1.LinkPort(C.EPo)
E1.LinkPort(R1.EPi)
E1.LinkPort(I.EPi)

S2.LinkPort(R1.EPo)
S2.LinkPort(I.EPo)

#mike vary these

#Independents
ind_1 = Independent("ind_E1.Vr", E1.Vr, .05, 100, True)
ind_2 = Independent("ind_E1.Vi", E1.Vi, .05, 100, True)

#Dependents
dep_1 = Dependent("dep_E1.Inetr", E1.IinR, E1.IoutR, 0. )
dep_2 = Dependent("dep_E1.Ineti", E1.IinI, E1.IoutI, 0. )


###
element_list = varsg.element_list
ind_list = varsg.ind_list
dep_list = varsg.dep_list
###

NS = Newton("solve")

NS.solve()

stdOut.print()

