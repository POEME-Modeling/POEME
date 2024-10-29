
import numpy as np
from scipy import interpolate
from scipy.interpolate import RegularGridInterpolator

class Table2d ( ):

	def __init__(self, p, name, units, desc ):
		self.name = name
		p.addVID( self )
		self.x = [ 0. ]
		self.y = [ 0. ]
		self.data = [0.]
		self.desc = desc
		self.units = units
		self.parent = p
	
	def full( s ):
		if len( s.x ) > 1:
			return True
		return False
		 
	def calc(s,x,y):

		xi,yi = None,None
		for i,(x1,x2) in enumerate(zip(s.x[:-1],s.x[1:])):
			if x1 <= x <= x2:
				xi,w_x2,w_x1 = i,(x-x1)/(x2-x1),(x2-x)/(x2-x1)
				break
		for i,(y1,y2) in enumerate(zip(s.y[:-1],s.y[1:])):
			if y1 <= y <= y2:
				yi,w_y2,w_y1 = i,(y-y1)/(y2-y1),(y2-y)/(y2-y1)
				break
		if xi is None or yi is None:
			return False
		ave  = s.data[yi][xi]    *w_y1*w_x1
		ave += s.data[yi][xi+1]  *w_y1*w_x2
		ave += s.data[yi+1][xi]  *w_y2*w_x1
		ave += s.data[yi+1][xi+1]*w_y2*w_x2

		return ave

	def isa( self, type ):
		if type == "Table2d":
			return True
		else:
			return False
	

 