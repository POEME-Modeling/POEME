
import numpy as np
from scipy import interpolate


class Table ( ):
	
	def __init__(self, p, name ):
		self.name = name
		p.addVID( self )
		self.x = [ 0. ]
		self.y = [ 0. ]
	
	def full( s ):
		if len( s.x ) > 1:
			return True
		return False
		
	def calc(s, xinp ):
		tmp = interpolate.interp1d(s.x, s.y) 
		xnew = xinp
		ynew = tmp( xnew )
		return ( ynew )
	
	def isa( self, type ):
		if type == "Table":
			return True
		else:
			return False
	

 