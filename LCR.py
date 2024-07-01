from Independent import Independent
from Dependent import Dependent
from solver import solver
from circuit import *
from HookeJeeves import HookeJeeves

import varsg

R1 = Resistor( "R1" )
R1.R.v=  470.

C = Capacitor( "C" )
C.C.v = 4.7 * (10 ** -6)

I = Inductor( "I" )
I.L.v = 65. * (10 ** -2)

S1 = Enode( "S1" )
S1.Vr.v = 120.

E1 = Enode( "E1" )
E1.Vr.v =  -30
E1.Vi.v = 16

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
print( E1.V )
ind_1 = Independent("ind_E1.Vr", E1.Vr, 1, False)
ind_2 = Independent("ind_E1.Vi", E1.Vi, 1, False)

#Dependents
dep_1 = Dependent("dep_E1.Inetr", E1.Inetr, E1.InetDr)
dep_2 = Dependent("dep_E1.Ineti", E1.Ineti, E1.InetDi)


###
element_list = varsg.element_list
ind_list = varsg.ind_list
dep_list = varsg.dep_list
###

hj = HookeJeeves(element_list, ind_list, dep_list, 1)

hj.Solve()

print("Resulting")
print( E1.Inet )
print( E1.Vr )
print( E1.Vi )

print("Done")
