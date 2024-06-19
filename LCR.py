
exec( open("./circuit.py" ).read())

R1 = Resistor( "R1" )
R1.R.v = 220.

C = Capacitor( "C" )
C.C.v = 3.3*(10**-6)

I = Inductor( "I" )
I.L.v = 75*(10**-3)

S1 = Enode( "S1" )
S1.V.c = complex( 17., 0. )

E1 = Enode( "E1" )
E1.V.c = complex( 9., 0. )

S2 = Enode( "S2" )
S2.V.c = complex( 0., 0. )

setFreq( 200. )
linkEV( C.EPi, S1 )
linkEV( C.EPo, E1 )
linkEV( R1.EPi, E1 )
linkEV( I.EPi, E1 )

link( R1.EPo, S2 )
link( I.EPo, S2 )

#mike vary these

#Independents
#E1.V.c.real
#E1.V.c.imag

#Mike make the some of these absolute values to be zero
#abs(E1.Inet.c.real)
#abs(E1.Inet.c.imag)


class solver:
	
	def run():
		for e in element_list:
			e.precheck()
		
		for e in element_list:
			e.preset()
			
		for e in element_list:
			e.calc()

solve = solver()

solver.run()

print( R1.EPo.I.c )
print( E1.Inet.c )
