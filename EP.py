
from Atom import Atom
from ComplexT import ComplexT
from RealT import RealT
import varsg

class EP( Atom ):
	def __init__( self, p, name, io, desc ):
		
		self.VIDL = list()
		self.name = name
		self.desc = desc
		self.parent = p
		self.io = io
		self.freq = -1
		self.V = ComplexT( self, complex(0,0), "V", "volts", "Voltage" )
		self.I = ComplexT( self, complex(0,0), "I", "amps", "Amperage" )
		self.Vr = RealT( self, 0., "Vr", "volts", "Real voltage" )  	    
		self.Vi = RealT( self, 0., "Vi", "volts", "Imaginary voltage" )  	    
		self.Ir = RealT( self, 0., "Ir", "amps", "Real amperage" )  	    
		self.Ii = RealT( self, 0., "Ii", "amps", "Imaginary amperage" )  	    

		p.addVID( self )
		
	def isa( self, type ):
		if type == "EP":
			return True
		else:
			return False
		
	def setIV( self, I , V ):
		self.I.num = I
		self.V.num = V
		self.other.I.num = I
		self.other.V.num = V
		self.Vr.v = V.real
		self.Vi.v = V.imag
		self.Ir.v = I.real
		self.Ii.v = I.imag
		self.other.Vr.v = V.real
		self.other.Vi.v = V.imag
		self.other.Ir.v = I.real
		self.other.Ii.v = I.imag		
		
		
	def addVID(self,v):
		self.VIDL.append(v)
		
		
	def linkEP( e, EP ):
		e.other = EP
		EP.other = e
  

	def dump( self ):
		
		print( self.parent.name, self.name, self.V.num, self.I.num, file = varsg.out )
		