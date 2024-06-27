from Element import Element
from ComplexT import ComplexT
from RealT import RealT

class Enode( Element ):
	def __init__(self,name):
		super().__init__(name, "Enode" )
		self.name = name
		self.Vr = RealT( self, 0., "Vr", "Real component of voltage" )
		self.Vi = RealT( self, 0., "Vi", "Imaginary component of voltage" )
		self.V = ComplexT( self, "V", "Voltage" )
		self.Inetr = RealT( self, 0., "Inetr", "Real component of Inet" )
		self.Ineti = RealT( self, 0., "Ineti", "Imaginary component of Inet" )
		self.InetDr = RealT( self, 0., "InetDr", "Real component of Inet demand" )
		self.InetDi = RealT( self, 0., "InetDi", "Imaginary component of Inet demand" )
		self.Inet = ComplexT( self, "Inet", "Current" )
		self.I = ComplexT( self, "I", "Current" )
		self.port_list = list()
		
	def LinkPort(self, port):
		self.port_list.append(port)

	def precheck(self):
		pass
    			
	def preset(self):
		for p in self.port_list:
			V.c = complex( Vr, Vi )
			p.setIV( complex( 0., 0.), self.V.c ) 
	
	def calc(self):
		self.Inet.c = complex( 0., 0. )
		for p in self.port_list:
			self.Inet.c = self.Inet.c + p.I.c
		self.Inetr = self.Inet.c.real
		