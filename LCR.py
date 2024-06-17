
exec( open("./circuit.py" ).read())

R1 = Resistor( "R1" )
R1.R.v = 100.

C = Capacitor( "C" )
C.C.v = 5

I = Inductor( "I" )
I.L.v = 5.2

S1 = Enode( "S1" )
S1.V.c = complex( 120., 0. )

E1 = Enode( "E1" )
E1.V.c = complex( 60., 0. )

S2 = Enode( "S2" )
S2.V.c = complex( 0., 0. )

setFreq( 60. )
linkEV( R1.EPi, S1 )
linkEV( R1.EPo, E1 )
linkEV( C.EPi, E1 )
linkEV( I.EPi, E1 )

link( C.EPo, S2 )
link( I.EPo, S2 )


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
