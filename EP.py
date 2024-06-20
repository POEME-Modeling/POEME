from Atom import Atom
from ComplexT import ComplexT

class EP( Atom ):
	def __init__( self, p, name, desc ):
		self.name = name
		self.desc = desc
		self.parent = p
		self.freq = -1
		self.V = ComplexT( p, "V", "Voltage" )
		self.I = ComplexT( p, "I", "Amperage" )
		p.addVID( self )
		
	def isa( self, type ):
		if type == "EP":
			return True
		else:
			return False
		
	def setIV( self, I , V ):
		self.I.c = I
		self.V.c = V