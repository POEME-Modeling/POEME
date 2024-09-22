from Element import Element
from ComplexT import ComplexT
from RealT import RealT
import varsg

class Enode( Element ):
	def __init__(self,name):
		super().__init__(name, "Enode" )
		self.name = name
		self.Vr = RealT( self, 0., "Vr", "volts", "Real component of voltage" )
		self.Vi = RealT( self, 0., "Vi", "volts", "Imaginary component of voltage" )
		self.V = ComplexT( self, complex(0,0), "V", "volts", "Voltage" )
		self.IinR = RealT( self, 0., "IinR", "amps", "Real component of I comping in" )
		self.IoutR = RealT( self, 0., "IoutR", "amps", "Real component I going out" )
		self.IinI = RealT( self, 0., "IinI", "amps", "Imaginery component of I coming in" )
		self.IoutI = RealT( self, 0., "IoutI", "amps", "Imaginary component of I going out" )
		self.Inet = ComplexT( self, complex(0,0), "Inet", "amps", "Current" )
		self.I = ComplexT( self, complex(0,0), "I", "amps", "Current" )
		self.port_list = list()
		
	def LinkPort(self, port):
		self.port_list.append(port)
 			
	def preset(self):
		for p in self.port_list:
			self.V.num = complex( self.Vr.v, self.Vi.v )
			p.setIV( complex( 0., 0.), self.V.num ) 
			
	def precheck( self ):
	
		for v in self.VIDL:
			if v.isa( "EP" ):
				self.port_list.append( v )
	
	
	def calc(s):
		
		s.IinR.v = 0.
		s.IoutR.v = 0.
		s.IinI.v = 0.
		s.IoutI.v = 0.

		for p in s.port_list:


			if p.I.num.real > 0:
				s.IinR.v = s.IinR.v + p.I.num.real
			else:
				s.IoutR.v = s.IoutR.v - p.I.num.real
			if p.I.num.imag > 0:
				s.IinI.v = s.IinI.v + p.I.num.imag
			else:
				s.IoutI.v = s.IoutI.v - p.I.num.imag


	    
	def dump( self ):
		print( self.name, "Node", file = varsg.out )
		super().realPrint()
	
		