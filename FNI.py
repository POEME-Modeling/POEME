from RealT import RealT
import math
from Atom import Atom

from H2O import H2O

from RealT import RealT
from BooleanT import BooleanT

class FNI( Atom ):
	
	
	def __init__( f, name, desc ):
		f.VIDL =  list()
		f.name = name
		f.desc = desc
		f.comp = ""
		f.fract2 = RealT( f, 0., "", "", "" )
		f.W = RealT( f, 0., "", "", "" )
		f.Tt = RealT( f, 0., "", "", "" )
		f.Pt = RealT( f, 0., "", "", "" )
		f.ht = RealT( f, 0., "", "", "" )
		f.rhot = RealT( f, 0., "", "", "" )
		f.mut = RealT( f, 0., "", "", "" )
		f.kt = RealT( f, 0., "", "", "" )
		f.Cpt = RealT( f, 0., "", "", "" )
		f.gamt = RealT( f, 0., "", "", "" )
		f.s = RealT( f, 0., "", "", "" )
		f.A = RealT( f, 0., "", "", "" )
		f.V = RealT( f, 0., "", "", "" )
		f.Ts = RealT( f, 0., "", "", "" )
		f.Ps = RealT( f, 0., "", "", "" )
		f.hs = RealT( f, 0., "", "", "" )
		f.rhos = RealT( f, 0., "", "", "" )
		f.mus = RealT( f, 0., "", "", "" )
		f.ks = RealT( f, 0., "", "", "" )	
		f.Cps = RealT( f, 0., "", "", "" )
		f.gams = RealT( f, 0., "", "", "" )
		f.size = BooleanT( f, True, "", "" )
		
          
	def addVID(f,v):
		f.VIDL.append(v)

	def isa( f, type ):
		if type == "FluidNode":
			return True
		else:
			return False
			
	def setTP( f, Tt, Pt ):
		f.Tt.v = Tt
		f.Pt.v = Pt
		f.ht.v = eval(f.comp).h_TP( f.Tt.v, f.Pt.v, f.fract2.v )
		f.s.v = eval(f.comp).s_TP( f.Tt.v, f.Pt.v, f.fract2.v )
		f.rhot.v = eval(f.comp).rho( f.ht.v, f.Pt.v, f.fract2.v )
		f.Cpt.v = eval(f.comp).Cp( f.ht.v, f.Pt.v, f.fract2.v )
		f.mut.v = eval(f.comp).mu( f.ht.v, f.Pt.v, f.fract2.v )
		f.kt.v = eval(f.comp).k( f.ht.v, f.Pt.v, f.fract2.v )
		f.statics()
		
	def set_hP( f, ht, Pt ):
		f.ht.v = ht
		f.Pt.v = Pt
		f.Tt.v = eval(f.comp).T_hP( f.Tt.v, f.Pt.v, f.fract2.v )
		f.s.v = eval(f.comp).s_TP( f.Tt.v, f.Pt.v, f.fract2.v )	
		f.rhot.v = eval(f.comp).rho( f.ht.v, f.Pt.v, f.fract2.v )
		f.Cpt.v = eval(f.comp).Cp( f.ht.v, f.Pt.v, f.fract2.v )
		f.mut.v = eval(f.comp).mu( f.ht.v, f.Pt.v, f.fract2.v )
		f.kt.v = eval(f.comp).k( f.ht.v, f.Pt.v, f.fract2.v )
			
	def set_sP( f, s, Pt ):
		f.s.v = s
		f.Pt.v = Pt
		f.Tt.v = eval(f.comp).T_sP( f.s.v, f.Pt.v, f.fract2.v )
		f.ht.v = eval(f.comp).h_TP( f.ht.v, f.Pt.v, f.fract2.v )
		f.rhot.v = eval(f.comp).rho( f.ht.v, f.Pt.v, f.fract2.v )
		f.Cpt.v = eval(f.comp).Cp( f.ht.v, f.Pt.v, f.fract2.v )
		f.mut.v = eval(f.comp).mu( f.ht.v, f.Pt.v, f.fract2.v )
		f.kt.v = eval(f.comp).k( f.ht.v, f.Pt.v, f.fract2.v )
		
	def statics( f ):
		f.rhos.v = f.rhot.v
		if f.size.v == True:
			f.A.v = f.W.v /( f.V.v * f.rhos.v )/12.
		else:
			f.V.v = f.W.v /( f.A.v * f.rhos.v )/12.
			
		f.Ps.v  = f.Pt.v - 1./2.*(f.rhos.v*12.**3)*f.V.v**2. / 32.174;
		f.Ts.v = f.Tt.v
		f.Cps.v = f.Cpt.v
		f.mus.v = f.mut.v
		f.ks.v = f.kt.v
					
	
test = FNI( "H2O", "test" );
test.comp = "H2O"
H2O = H2O
test.W.v = 10.
test.V.v = 10.
test.setTP( 500 , 1000 ) 
print( test.Tt.v, test.Pt.v, test.ht.v, test.s.v )
test.set_hP( test.ht.v, test.Pt.v )
print( test.Tt.v, test.Pt.v, test.ht.v, test.s.v )
test.set_sP( test.s.v, test.Pt.v )
print( test.Tt.v, test.Pt.v, test.ht.v, test.s.v )
print( test.rhot.v )
print( test.Cpt.v )
print( test.mut.v )
print( test.kt.v )
print ( test.Pt.v, test.Ps.v )




	 