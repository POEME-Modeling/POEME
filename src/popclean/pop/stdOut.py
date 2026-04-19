import g

class stdOut( ):
	
	def print():
		
		print( "Electric Ports*************" )
		print ( "" )
		for e in varsg.element_list:
			for p in e.VIDL:
				if p.isa( "EP" ):
					p.dump()

		print( "Data Ports*************" )
		print ( "" )
		for e in varsg.element_list:
			for p in e.VIDL:
				if p.isa( "DP" ):
					p.dump()
					
		print( "Fluid Ports*************" )					
		for e in varsg.element_list:
			for p in e.VIDL:
				if p.isa( "FN" ):
					p.dump()

		print( "Mech Ports*************" )					
		for e in varsg.element_list:
			for p in e.VIDL:
				if p.isa( "MP" ):
					p.dump()
					
		print( "" )					
		print( "Elements***********" )
		print( "" )
					
		for e in g.element_list:
			e.dump()
			
		for d in g.view_list:
			d.dump()
			