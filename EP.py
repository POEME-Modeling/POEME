from Atom import Atom
from ComplexT import ComplexT

class EP( Atom ):
	def __init__( self, p, name, desc ):
		
		self.VIDL = list()
		self.name = name
		self.desc = desc
		self.parent = p
		self.freq = -1
		self.V = ComplexT( self, complex(0,0), "V", "volts", "Voltage" )
		self.I = ComplexT( self, complex(0,0), "I", "amps", "Amperage" )
		p.addVID( self )
		
	def isa( self, type ):
		if type == "EP":
			return True
		else:
			return False
		
	def setIV( self, I , V ):
		self.I.num = I
		self.V.num = V
		
	def addVID(self,v):
		self.VIDL.append(v)

	def dump( self ):
		print( self.parent.name, self.name, self.V.num, self.I.num )
		