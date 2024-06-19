from Element import Element
from circuit import ComplexT

class Enode( Element ):
	def __init__(s,name):
		super().__init__(name, "Enode" )
		s.name = name
		s.V = ComplexT( s, "V", "Voltage" )
		s.Inet = ComplexT( s, "Inet", "Current" )
		s.I = ComplexT( s, "I", "Current" )
		
	def precheck(s):
		s.EPL = []
		for a in s.VIDL:
			if a.isa( "EP" ):
				s.EPL.append(a)
    			
	def preset(s):
		for p in s.EPL:
			print( s.V.c  )
			p.setIV( complex( 0., 0.), s.V.c ) 
			print( s.V.c )
	
	def calc(s):
		s.Inet.c = complex( 0., 0. )
		for p in s.EPL:
			s.Inet.c = s.Inet.c + p.I.c
		