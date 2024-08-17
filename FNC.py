from RealT import RealT
import math
from Atom import Atom

from H2O import H2O
from air import air

from RealT import RealT
from StringT import StringT
from BooleanT import BooleanT


Mach = 1
Area = 2

class FNC( Atom ):
	
	
	def __init__( f, p, name, desc ):
		f.parent = p
		f.VIDL =  list()
		f.name = name
		f.desc = desc
		f.comp = StringT( f, "none", "comp", "Composition of flow" )
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
		f.Rs = RealT( f, 0., "", "", "" )
		f.size = BooleanT( f, False, "", "" )
		f.sizer =RealT( f, 0, "", "", "" )
		Mach = 0
		Area = 1
		f.other = ""
		p.addVID( f )
	
 			
	def addVID(f,v):
		f.VIDL.append(v)

	def isa( f, type ):
		if type == "FNC":
			return True
		else:
			return False
			
	def setTP( f, Ttin, Ptin ):
		f.Tt.v = Ttin
		f.Pt.v = Ptin
		f.ht.v = eval(f.comp.v).h_TP( f.Tt.v, f.Pt.v, f.fract2.v )
		f.s.v = eval(f.comp.v).s_TP( f.Tt.v, f.Pt.v, f.fract2.v )
		f.rhot.v = eval(f.comp.v).rho( f.Tt.v, f.Pt.v, f.fract2.v )
		f.Rt.v =  eval(f.comp.v).R( f.Tt.v, f.Pt.v, f.fract2.v )
		f.gamt.v =  eval(f.comp.v).gam( f.Tt.v, f.Pt.v, f.fract2.v )
		f.Cpt.v = eval(f.comp.v).Cp( f.Tt.v, f.Pt.v, f.fract2.v )
		f.mut.v = eval(f.comp.v).mu( f.Tt.v, f.Pt.v, f.fract2.v )
		f.kt.v = eval(f.comp.v).k( f.Tt.v, f.Pt.v, f.fract2.v )
		f.statics()
		f.setPort()
		
	def set_hP( f, htin, Ptin ):
		f.ht.v = htin
		f.Pt.v = Ptin
		f.Tt.v = eval(f.comp.v).T_hP( f.ht.v, f.Pt.v, f.fract2.v )
		f.s.v = eval(f.comp.v).s_TP( f.Tt.v, f.Pt.v, f.fract2.v )	
		f.rhot.v = eval(f.comp.v).rho( f.Tt.v, f.Pt.v, f.fract2.v )
		f.Rt.v =  eval(f.comp.v).R( f.Tt.v, f.Pt.v, f.fract2.v )
		f.Cpt.v = eval(f.comp.v).Cp( f.Tt.v, f.Pt.v, f.fract2.v )
		f.mut.v = eval(f.comp.v).mu( f.Tt.v, f.Pt.v, f.fract2.v )
		f.kt.v = eval(f.comp.v).k( f.Tt.v, f.Pt.v, f.fract2.v )
		f.statics()
		f.setPort()
			
	def set_sP( f, sin, Ptin ):
		f.s.v = sin
		f.Pt.v = Ptin
		f.Tt.v = eval(f.comp.v).T_sP( f.s.v, f.Pt.v, f.fract2.v )
		f.ht.v = eval(f.comp.v).h_TP( f.Tt.v, f.Pt.v, f.fract2.v )
		f.rhot.v = eval(f.comp.v).rho( f.Tt.v, f.Pt.v, f.fract2.v )
		f.Rt.v =  eval(f.comp.v).R( f.Tt.v, f.Pt.v, f.fract2.v )
		f.Cpt.v = eval(f.comp.v).Cp( f.Tt.v, f.Pt.v, f.fract2.v )
		f.mut.v = eval(f.comp.v).mu( f.Tt.v, f.Pt.v, f.fract2.v )
		f.kt.v = eval(f.comp.v).k( f.Tt.v, f.Pt.v, f.fract2.v )
		f.statics()
		f.setPort()
		
	def PsCalc( f ):
		f.Ts.v = eval(f.comp.v).T_sP( f.s.v, f.Ps.v, f.fract2.v )
		f.hs.v = eval(f.comp.v).h_TP( f.Ts.v, f.Ps.v, f.fract2.v )
		f.rhos.v = eval(f.comp.v).rho( f.Ts.v, f.Ps.v, f.fract2.v )
		f.Rs.v =  eval(f.comp.v).R( f.Ts.v, f.Ps.v, f.fract2.v )
		f.gams.v =  eval(f.comp.v).gam( f.Ts.v, f.Ps.v, f.fract2.v )
		f.Cps.v = eval(f.comp.v).Cp( f.Ts.v, f.Ps.v, f.fract2.v )
		f.mus.v = eval(f.comp.v).mu( f.Ts.v, f.Ps.v, f.fract2.v )
		f.ks.v = eval(f.comp.v).k( f.Ts.v, f.Ps.v, f.fract2.v )
		f.V.v = math.sqrt(2*( f.ht.v - f.hs.v)*25037)
		f.MN.v =f.V.v / math.sqrt( f.gams.v * f.Rs.v * f.Ts.v*25037 )
		f.A.v = f.W.v /( f.rhos.v *f.V.v )
					

	def setPort( f ):
		if f.other != "":
			f.other.comp.v = f.comp.v
			f.other.fract2.v = f.fract2.v
			f.other.W.v = f.W.v
			f.other.Tt.v = f.Tt.v
			f.other.Pt.v = f.Pt.v
			f.other.ht.v = f.ht.v
			f.other.rhot.v = f.rhot.v
			f.other.mut.v = f.mut.v
			f.other.kt.v = f.kt.v
			f.other.Cpt.v = f.Cpt.v
			f.other.gamt.v = f.gamt.v
			f.other.Rt.v = f.Rt.v
			f.other.s.v = f.s.v		
			f.other.MN.v = f.MN.v
			f.other.A.v = f.A.v
			f.other.V.v = f.V.v
			f.other.Ts.v = f.Ts.v
			f.other.Ps.v = f.Ps.v
			f.other.hs.v = f.hs.v
			f.other.rhos.v = f.rhos.v
			f.other.mus.v = f.mus.v
			f.other.ks.v = f.ks.v
			f.other.Cps.v = f.Cps.v
			f.other.gams.v = f.gams.v
			f.other.Rs.v = f.Rs.v
			f.other.size.v = f.size.v
			f.other.sizer.v = f.sizer.v			


	def statics( f ):
		f.gams = f.gamt;
		f.rhos.v = f.rhot.v

		if f.size.v == True:
			if f.sizer.v == Mach:
				MNor = f.MN.v
				f.Ps.v = f.Pt.v*.8
				f.PsCalc()
				errorm1 = ( f.MN.v - MNor )/ MNor
				xm1 =  f.Ps.v
				f.Ps.v = f.Ps.v*.95
				f.PsCalc()
				error = ( f.MN.v - MNor )/ MNor
				x = f.Ps.v 
				while abs( error ) > .001:
					xp1 = x - error * (x - xm1 ) / ( error - errorm1 )
					if xp1 - x > .1:
						xp1 = x + .1
					if xp1 - x < -.1:
						xp1 = x - .1
					xm1 = x
					errorm1 = error
					x = xp1
					f.Ps.v = x
					f.PsCalc()
					error = ( f.MN.v - MNor )/ MNor
	
				f.MN.v = MNor			

			
			else:
				Aor = f.A.v
				f.Ps.v = f.Pt.v*.9
				f.PsCalc()
				errorm1 = ( f.A.v - Aor )/ Aor
				xm1 =  f.MN.v
				f.Ps.v = f.Ps.v*.95
				f.PsCalc()
				error = ( f.A.v - Aor )/ Aor
				x = f.Ps.v 
				while abs( error ) > .001:
					xp1 = x - error * (x - xm1 ) / ( error - errorm1 )
					if xp1 - x > .1:
						xp1 = x + .1
					if xp1 - x < -.1:
						xp1 = x - .1
					xm1 = x
					errorm1 = error
					x = xp1
					f.Ps.v = x
					f.PsCalc()
					error = ( f.A.v - Aor )/ Aor
			    
				f.A.v = Aor
				
	def copy( f, FP ):
		f.fract2 = FP.fract2
		f.comp.v = FP.comp.v
		f.W.v = FP.W.v
		f.set_hP( FP.ht.v, FP.Pt.v )
		
	def dump( self ):
		print( self.parent.name, self.name, self.comp.v, self.W.v, self.Pt.v, self.Tt.v )
			
	def linkFP( f, FP ):
		f.other = FP
		FP.other = f
