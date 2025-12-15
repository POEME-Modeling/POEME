#global lists the entire model needs

from RealT import RealT
from Newton import Newton

element_list = list()
obs_list = list()
ind_list = list()
dep_list = list()
con_list = list()
state_list = list()
view_list = list()

solver = 0
import os

VIDL = list()
x = 0.
y = 0.
name1 = "varsg"

def __setattr__(self, name, value):
    super().__setattr__(name, value)

    if (eval( "hasattr(self."+name+" ,\"name1\")" )):
        temp = eval( "self."+name )
        temp.name1 = name


solveState = "SS"



out = 0
win=0
w=0
NS = Newton( "varsg.NS" )



def check(): 
	for e in element_list:
		e.precheck()   	
		
	for i in ind_list:
		i.precheck()   	
		
	for d in dep_list:
		d.precheck()  
		
	for s in state_list:
		s.precheck()  
			
def set( var, value ):
	
	stuff = element_list.copy()
	stuff.append( NS )
	
	for e in stuff:
		for v in e.VIDL:
			if v.name1 == var:
				v.v =value
			if v.VIDL != 0:
				for v1 in v.VIDL:
					if v1.name1 == var:
						v1.v = value
					try:
						for v2 in v1.VIDL():
							if v2.name1 == var:
								v2.v = value

					except:
						pass
					



class stdOut( ):
	
	def print():
		print( "in print 1" )
		print( "time = ", NS.time, file=out )
		print( "Ports*************", file=out )
		print ( "", file=out )
		print( "Electric Ports", file=out )
		for e in element_list:

			for p in e.VIDL:
				if p.isa( "EP" ):
					p.dump()
					
		print( "", file=out )
		print( "Fluid Ports", file=out )					
		for e in element_list:
			for p in e.VIDL:
				if p.isa( "FN" ):
					p.dump()
					
		print( "", file=out )					
		print( "Mech Ports", file=out )
		for e in element_list:
			for p in e.VIDL:
				if p.isa( "MP" ):
					p.dump()
					
		print( "", file = out )					
		print( "Elements***********", file = out )
		print( "", file = out )
					
		for e in element_list:
			e.dump()

