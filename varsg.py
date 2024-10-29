#global lists the entire model needs

element_list = list()
obs_list = list()
ind_list = list()
dep_list = list()
con_list = list()
solver = 0
import os

NS = 0
out = 0
win=0
w=0

class stdOut( ):
	
	def print():
		
	
		
		print( "Ports*************", file=out )
		print ( "", file=out )
		for e in element_list:
			for p in e.VIDL:
				if p.isa( "EP" ):
					p.dump()
					
		for e in element_list:
			for p in e.VIDL:
				if p.isa( "FNC" ):
					p.dump()

					
		print( "", file = out )					
		print( "Elements***********", file = out )
		print( "", file = out )
					
		for e in element_list:
			e.dump()
			
	
os.system( "del pop.out" )
out = open( "pop.out", "a")