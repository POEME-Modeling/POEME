from RealT import RealT
import math
from Atom import Atom

from H2O import H2O

class FluidNode( Atom ):

	def __init__( f, name, desc ):
		f.name = name
		f.desc = desc
		f.comp = ""
		f.fract2 = 0
		f.Tt = 0
		f.Pt = 0
		f.ht = 0
		f.rhot = 0
		f.Cpt = 0
		f.gamt = 0
		f.s = 0
		f.MN = 0
		f.V = 0
		f.Ts = 0
		f.Ps = 0
		f.hs = 0
		f.rhos = 0
		f.Cps = 0
		f.gams = 0

#p.addVID( self )
		
	def isa( f, type ):
		if type == "FluidNode":
			return True
		else:
			return False
			
	def setTP( f, Tt, Pt ):
		f.Tt = Tt
		f.Pt = Pt
		f.ht = eval(f.comp).h_TP( f.Tt, f.Pt, f.fract2 )
		f.s = eval(f.comp).s_TP( f.Tt, f.Pt, f.fract2 )
		
	def set_hP( f, ht, Pt ):
		f.ht = ht
		f.Pt = Pt
		print( f.comp )
		f.T = eval(f.comp).T_hP( f.Tt, f.Pt, f.fract2 )
		f.s = eval(f.comp).s_TP( f.Tt, f.Pt, f.fract2 )		
	
	def set_sP( f, s, Pt ):
		f.s = s
		f.Pt = Pt
		print( f.comp )
		f.Tt = eval(f.comp).T_sP( f.s, f.Pt, f.fract2 )
		f.ht = eval(f.comp).h_TP( f.ht, f.Pt, f.fract2 )
			
		
test = FluidNode( "H2O", "test" );
test.comp = "H2O"
H2O = H2O
test.setTP( 500 , 1000 ) 
print( test.Tt, test.Pt, test.ht, test.s )
test.set_hP( test.ht, test.Pt )
print( test.Tt, test.Pt, test.ht, test.s )
test.set_sP( test.s, test.Pt )
print( test.Tt, test.Pt, test.ht, test.s )
		
	 