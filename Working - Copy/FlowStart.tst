#
# ====================================================
#        SIMPLE TURBOFAN CYCLE PERFORMANCE MODEL
# ====================================================

# BUGS and ERRORS
# static pressure is incorrect for start fluid node, possibly all flow stations
# can't have zero cooling flow taken from a compressor
# python's formatted output doesn't work with RealT
# maps have to be placed in the model and can't be reused or imported in scope



exec( open( "pop.std").read())

loadDirectory( "../pop" ) 
loadDirectory( "../Brayton" ) 

exec( open( "temp.include").read())


# create all of the component objects, including the shaft connection ports
# ------------------------------------- 
start = FlightConditions( "start" )
FS = FlowStart( "FS" )
start.alt.set( 0. )
start.MN.set( 0.25 )
start.W.set( 1726.57 )
start.comp.set( "canteraFN" )
start.calc()

FS.Pt.set( start.FNo.Pt )
FS.Tt.set( start.FNo.Tt )
FS.FNo.MN.set( start.FNo.MN )
FS.comp.set( "canteraFN" )


FS.calc()
print( start.Pamb, start.FNo.Ps, start.Tamb, start.FNo.Ts, start.FNo.Pt, start.FNo.Tt )
print( FS.FNo.Ps, FS.FNo.Pt, FS.FNo.Ts, FS.FNo.Tt )


start.alt.set( 35000. )
start.MN.set( 0.85 )
start.W.set( 1726.57 )
start.comp.set( "canteraFN" )
start.calc()

FS.Pt.set( start.FNo.Pt )
FS.Tt.set( start.FNo.Tt )
FS.FNo.MN.set( start.FNo.MN )
FS.comp.set( "canteraFN" )


FS.calc()
print( start.Pamb, start.FNo.Ps, start.Tamb, start.FNo.Ts, start.FNo.Pt, start.FNo.Tt )
print( FS.FNo.Ps, FS.FNo.Pt, FS.FNo.Ts, FS.FNo.Tt )

quit()
