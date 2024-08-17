	
test = FNC( "air", "test" );
test.comp = "air"

test.W.v = 10.
test.MN.v = .8
test.size.v = True
test.sizer.v = Mach
test.setTP( 59+460 , 70 ) 
print( test.Tt, test.ht, test.s, test.rhot )

print( test.Ps, test.A.v, test.rhos )

test.sizer.v = Area
test.set_hP( test.ht.v, test.Pt.v )
print( test.Tt, test.ht, test.s )


test.set_sP( test.s.v, test.Pt.v )
print( test.Tt, test.ht, test.s )
print( test.Ps, test.A.v, test.rhos )
print( test.Ts 