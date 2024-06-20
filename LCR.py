from Independent import Independent
from circuit import *
from HookeJeeves import HookeJeeves

element_list = list()

R1 = Resistor( "R1" )
R1.R.v = 220
element_list.append(R1)

C = Capacitor( "C" )
C.C.v = 3.3 * (10 ** -6)
element_list.append(C)

I = Inductor( "I" )
I.L.v = 75 * (10 ** -3)
element_list.append(I)

S1 = Enode( "S1" )
S1.V.c = complex( 17., 0. )
element_list.append(S1)

E1 = Enode( "E1" )
E1.V.c = complex( 9., 0. )
element_list.append(E1)

S2 = Enode( "S2" )
S2.V.c = complex( 0., 0. )
element_list.append(S2)

setFreq( 200., element_list)
S1.LinkPort(C.EPi)
E1.LinkPort(C.EPo)
E1.LinkPort(R1.EPi)
E1.LinkPort(I.EPi)

S2.LinkPort(R1.EPo)
S2.LinkPort(I.EPo)

#mike vary these

#Independents
ind_1 = Independent(E1.V, 1, True, True)
ind_2 = Independent(E1.V, 1, True, True)

E1.AddIndependent(ind_1)
E1.AddIndependent(ind_2)

def objective():
    print(abs(E1.Inet.c.real) + abs(E1.Inet.c.imag))

    return - (abs(E1.Inet.c.real) + abs(E1.Inet.c.imag))

hj = HookeJeeves(element_list, 0.1, objective)

hj.Solve()

print( R1.EPo.I.c )
print( E1.Inet.c )
