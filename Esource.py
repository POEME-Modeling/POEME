class Esource( Element ):
	def __init__(s,name):
		super().__init__(name, "Enode" )
		s.name = name
		s.V = Complex( s, "V", "Voltage" )
		s.EP = EP( s, "EPo", "Exit Electric Port" )
  		
    			
	def preset(s):
		s.EP.setIV( complex(0,0), s.V.c )
			
	def calc(s):
		pass