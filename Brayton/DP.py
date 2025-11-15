
from Atom import Atom
from RealT import RealT
import varsg

class DP( Atom ):
	def __init__( self, p, name, io, desc ):

		self.VIDL = list()
		self.name = name
		self.desc = desc
		self.parent = p
		self.io = io
		self.D = RealT( self, 0., "D", "", "Data Value" )  	    
		p.addVID( self )
		self.type = "DP"
		
	def isa( self, type ):
		if type == "DP":
			return True
		else:
			return False
		
	def set( self, v ):
		self.D.v = v
		self.other.D.v = v

	def addVID(self,v):
		self.VIDL.append(v)
		
		
	def linkDP( d, DP ):
		d.other = DP
		DP.other = d

  

	def dump( self ):
		
		print( self.parent.name, self.name, self.D.v, file = varsg.out )
		