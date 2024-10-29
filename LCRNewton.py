
from Independent import Independent
from Dependent import Dependent
from solver import solver
from Constraint import Constraint

from circuit import *
from HookeJeeves import HookeJeeves
from Newton import Newton
from stdOut import stdOut
from Output import Output

import varsg


R1 = Resistor( "R1" )
R1.R.v =  450.
#exec( open("./RV.tbl" ).read())
R1.RV.y = [ 470, 470. ]
R1.RV.x = [-1000, 1000. ]

C = Capacitor( "C" )
C.C.v = 4.7 * (10 ** -6)
C.CVc.x = [-1000., 0., 1000. ]
C.CVc.y = [-1000., 0., 1000. ]
C.CVc.data = [ [4.7 * (10 ** -6),4.8 * (10 ** -6),4.9 * (10 ** -6)], \
               [4.4 * (10 ** -6),4.5 * (10 ** -6),4.6 * (10 ** -6)],\
               	   [4.1 * (10 ** -6),4.2 * (10 ** -6),4.4 * (10 ** -6) ]]
              
I = Inductor( "I" )
I.L.v = 65. * (10 ** -2)


S1 = Enode( "S1" )
S1.Vr.v = 120.

E1 = Enode( "E1" )
E1.Vr.v =  -50
E1.Vi.v = 10

S2 = Enode( "S2" )

setFreq( 60. )
S1.EP1=EP( S1, "EP1", "out", "" )
S1.EP1.linkEP(C.EPi)
#S1.LinkPort(C.EPi)

E1.EP1=EP( E1, "EP1", "in", "" )
E1.EP1.linkEP(C.EPo)
E1.EP2=EP( E1, "EP2", "out", "" )
E1.EP2.linkEP(R1.EPi)
E1.EP3=EP( E1, "EP3", "out", "" )
E1.EP3.linkEP(I.EPi)

#E1.LinkPort(C.EPo)
#E1.LinkPort(R1.EPi)
#E1.LinkPort(I.EPi)

S2.EP1=EP( S2, "EP1", "in", "" )
S2.EP1.linkEP(I.EPo)
S2.EP2=EP( S2, "EP2", "in", "" )
S2.EP2.linkEP(R1.EPo)

Out=Output( "estuff", "estuff.out" )
Out.vars = [ R1.R, C.C ]
#S2.EP1.linkEP(R1.EPo)
#S2.EP2.linkEP(I.EPo)

#mike vary these

#Independents
ind_1 = Independent("ind_1", E1.Vr, .05, 100, True)
ind_2 = Independent("ind_2", E1.Vi, .05, 100, True)

#Dependents
dep_1 = Dependent("dep_1", E1.IinR, E1.IoutR, 0. )
dep_2 = Dependent("dep_2", E1.IinI, E1.IoutI, 0. )

con_1 = Constraint("con_1", E1.IinIp1, E1.IoutI, 0., dep_2 )
con_2 = Constraint("con_2", E1.IinIp2, E1.IoutI, 0., dep_2 )
	
element_list = varsg.element_list
ind_list = varsg.ind_list

dep_list = varsg.dep_list


varsg.NS = Newton( "varsg.NS" )

varsg.NS.solve()

varsg.stdOut.print()

print( "converged",  varsg.NS.converged )


#print( con_1.active )
#print( con_2.active )
