from Element import Element
from ComplexT import ComplexT
from RealT import RealT

class Enode( Element ):
	def __init__(self,name):
		super().__init__(name, "Enode" )
		self.name = name
		self.Vr = RealT( self, 0., "Vr", "Real component of voltage" )
		self.Vi = RealT( self, 0., "Vi", "Imaginary component of voltage" )
		self.V = ComplexT( self, complex(0,0), "V", "Voltage" )
		self.Inetr = RealT( self, 0., "Inetr", "Real component of Inet" )
		self.Ineti = RealT( self, 0., "Ineti", "Imaginary component of Inet" )
		self.InetDr = RealT( self, 0., "InetDr", "Real component of Inet demand" )
		self.InetDi = RealT( self, 0., "InetDi", "Imaginary component of Inet demand" )
		self.Inet = ComplexT( self, complex(0,0), "Inet", "Current" )
		self.I = ComplexT( self, complex(0,0), "I", "Current" )
		self.port_list = list()
		
	def LinkPort(self, port):
		self.port_list.append(port)
 			
	def preset(self):
		print( "enode preset" )
		for p in self.port_list:
			self.V.num = complex( self.Vr.v, self.Vi.v )
			p.setIV( complex( 0., 0.), self.V.num ) 
	
	def calc(self):
		self.Inet.num = complex( 0., 0. )
		for p in self.port_list:
			self.Inet.set( self.Inet + p.I )
			
		self.Inetr = self.Inet.num.real
		self.Ineti = self.Inet.num.imag
		