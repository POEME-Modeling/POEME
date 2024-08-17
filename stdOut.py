import varsg

class stdOut( ):
	
	def print():
		
		print( "Ports*************" )
		print ( "" )
		for e in varsg.element_list:
			for p in e.VIDL:
				if p.isa( "EP" ):
					p.dump()
					
		for e in varsg.element_list:
			for p in e.VIDL:
				if p.isa( "FNC" ):
					p.dump()

					
		print( "" )					
		print( "Elements***********" )
		print( "" )
					
		for e in varsg.element_list:
			e.dump()