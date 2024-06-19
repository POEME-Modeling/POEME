from Element import Element
from circuit import ComplexT
from circuit import EP

class Esource( Element ):
	def __init__(s,name):
		super().__init__(name, "Enode" )
		s.name = name
		s.V = ComplexT( s, "V", "Voltage" )
		s.EP = EP( s, "EPo", "Exit Electric Port" )
  		
    			
	def preset(s):
		s.EP.setIV( complex(0,0), s.V.c )
			
	def calc(s):
		pass