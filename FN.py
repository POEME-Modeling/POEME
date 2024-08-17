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
		f.Rt = RealT( f, 0., "", "", "" )
		f.s = RealT( f, 0., "", "", "" )		
		f.MN = RealT( f, 0., "", "", "" )
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
		if type == "FN ":
			return True
		else:
			return False
			
	def setTP( f, Tt, Pt ):
		f.Tt.v = Tt
		f.Pt.v = Pt
		f.ht.v = eval(f.comp).h_TP( f.Tt.v, f.Pt.v, f.fract2.v )
		f.s.v = eval(f.comp).s_TP( f.Tt.v, f.Pt.v, f.fract2.v )
		f.rhot.v = eval(f.comp).rho( f.Tt.v, f.Pt.v, f.fract2.v )
		f.R.v =  eval(f.comp).R( f.Tt.v, f.Pt.v, f.fract2.v )
		f.Cpt.v = eval(f.comp).Cp( f.Tt.v, f.Pt.v, f.fract2.v )
		f.mut.v = eval(f.comp).mu( f.Tt.v, f.Pt.v, f.fract2.v )
		f.kt.v = eval(f.comp).k( f.Tt.v, f.Pt.v, f.fract2.v )
		f.statics()
		
	def set_hP( f, ht, Pt ):
		f.ht.v = ht
		f.Pt.v = Pt
		f.Tt.v = eval(f.comp).T_hP( f.ht.v, f.Pt.v, f.fract2.v )
		f.s.v = eval(f.comp).s_TP( f.Tt.v, f.Pt.v, f.fract2.v )	
		f.rhot.v = eval(f.comp).rho( f.Tt.v, f.Pt.v, f.fract2.v )
		f.R.v =  eval(f.comp).R( f.Tt.v, f.Pt.v, f.fract2.v )
		f.Cpt.v = eval(f.comp).Cp( f.Tt.v, f.Pt.v, f.fract2.v )
		f.mut.v = eval(f.comp).mu( f.Tt.v, f.Pt.v, f.fract2.v )
		f.kt.v = eval(f.comp).k( f.Tt.v, f.Pt.v, f.fract2.v )
			
	def set_sP( f, s, Pt ):
		f.s.v = s
		f.Pt.v = Pt
		f.Tt.v = eval(f.comp).T_sP( f.s.v, f.Pt.v, f.fract2.v )
		f.ht.v = eval(f.comp).h_TP( f.Tt.v, f.Pt.v, f.fract2.v )
		f.rhot.v = eval(f.comp).rho( f.Tt.v, f.Pt.v, f.fract2.v )
		f.R.v =  eval(f.comp).R( f.Tt.v, f.Pt.v, f.fract2.v )
		f.Cpt.v = eval(f.comp).Cp( f.Tt.v, f.Pt.v, f.fract2.v )
		f.mut.v = eval(f.comp).mu( f.Tt.v, f.Pt.v, f.fract2.v )
		f.kt.v = eval(f.comp).k( f.Tt.v, f.Pt.v, f.fract2.v )
		
	def statics( f ):
		f.gams = f.gamt;
		f.rhos.v = f.rhot.v
		
		if f.size.v == True:
			MNor = f.MN.v
			f.Ps.v = f.Pt.v*.9
			PsCalc()
			errorm1 = ( f.MN.v - MNor )/ MNor
			xm1 =  f.Ps.v
			f.Ps.v = f.Ps.v*.95
			PsCalc()
			error = ( f.MN.v - MNor )/ MMor
			x = f.Ps.v 
			while abs( error ) > .00001:
				xp1 = x - error * (x - xm1 ) / ( error - errorm1 )
				if xp1 - x > .1:
					xp1 = x + .1
				if xp1 - x < .1:
					xp1 = x - .1
					xm1 = x
				errorm1 = error
				x = xp1
				f.Ps.v = x
				PsCalc()
				error = ( f.MN.v - MNor )/ MNor
			    		
			f.MN.v = MNor			

			
		else:
			Aor = f.A.v
			f.Ps.v = f.Pt.v*.9
			PsCalc()
			errorm1 = ( f.A.v - Aor )/ Aor
			xm1 =  f.MN.v
			f.Ps.v = f.Ps.v*.95
			PsCalc()
			error = ( f.A.v - Aor )/ Aor
			x = f.Ps.v 
			while abs( error ) > .00001:
				xp1 = x - error * (x - xm1 ) / ( error - errorm1 )
				if xp1 - x > .1:
					xp1 = x + .1
				if xp1 - x < .1:
					xp1 = x - .1
				xm1 = x
				errorm1 = error
				x = xp1
				f.Ps.v = x
				PsCal()
				error = ( f.A.v - Aor )/ Aor
			    
			f.A.v = Aor
 			    
		def PsCalc( f ):
			f.Ts.v = eval(f.comp).T_sP( f.s.v, f.Ps.v, f.fract2.v )
			f.hs.v = eval(f.comp).h_TP( f.Ts.v, f.Ps.v, f.fract2.v )
			f.rhos.v = eval(f.comp).rho( f.Ts.v, f.Ps.v, f.fract2.v )
			f.Rt.v =  eval(f.comp).R( f.Ts.v, f.Ps.v, f.fract2.v )
			f.Cps.v = eval(f.comp).Cp( f.Ts.v, f.Ps.v, f.fract2.v )
			f.mus.v = eval(f.comp).mu( f.Ts.v, f.Ps.v, f.fract2.v )
			f.ks.v = eval(f.comp).k( f.Ts.v, f.Ps.v, f.fract2.v )
			f.V.v = 2.*sqrt(( f.ht.v - f.hs.v)/25037. )
			f.MN.v = sqrt( f.gams.v * f.Rs.v * f.Ts.v )
			f.A.v = f.W.v /( f.rhos.v *f.V.v )
			
			

			
	
					
	
test = FN( "air", "test" );
test.comp = "air"

test.W.v = 10.
test.MN.v = .5
test.setTP( 500 , 1000 ) 
quit();
