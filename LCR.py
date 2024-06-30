

from Independent import Independent


exec( open( "./solver.py" ).read())

exec( open( "./circuit.py" ).read())


exec( open( "./Independent.py" ).read())

exec( open( "./Dependent.py" ).read())

R1 = Resistor( "R1" )
R1.R.v=  220.

C = Capacitor( "C" )
C.C.v = 3.3 * (10 ** -6)

I = Inductor( "I" )
I.L.v = 75. * (10 ** -3)

S1 = Enode( "S1" )
S1.Vr.v = 17.

E1 = Enode( "E1" )
E1.Vr.v =  9.

S2 = Enode( "S2" )

setFreq( 200. )
S1.LinkPort(C.EPi)
E1.LinkPort(C.EPo)
E1.LinkPort(R1.EPi)
E1.LinkPort(I.EPi)

S2.LinkPort(R1.EPo)
S2.LinkPort(I.EPo)

#mike vary these

#Independents
print( E1.V )
ind_1 = Independent("ind_E1.Vr", E1.Vr )
ind_2 = Independent("ind_E1.Vi", E1.Vi )


#Independents
ind_1 = Dependent("ind_E1.Inetr", E1.Inetr, E1.InetDr )
ind_2 = Dependent("ind_E1.Ineti", E1.Ineti, E1.InetDi )

solve =solver()
solve.calc()

print( E1.Vr.v )


#def objective():
#    print(abs(E1.Inet.c.real) + abs(E1.Inet.c.imag))

#    return - (abs(E1.Inet.c.real) + abs(E1.Inet.c.imag))

#hj = HookeJeeves(element_list, 0.1, objective)

#hj.Solve()

print( R1.EPo.I)
print( E1.Inet )
