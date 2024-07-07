from Element import Element
from ComplexT import ComplexT
from RealT import RealT

class Enode( Element ):
	def __init__(self,name):
		super().__init__(name, "Enode" )
		self.name = name
		self.Vr = RealT( self, 0., "Vr", "volts", "Real component of voltage" )
		self.Vi = RealT( self, 0., "Vi", "volts", "Imaginary component of voltage" )
		self.V = ComplexT( self, complex(0,0), "V", "volts", "Voltage" )
		self.Inetr = RealT( self, 0., "Inetr", "amps", "Real component of Inet" )
		self.Ineti = RealT( self, 0., "Ineti", "amps", "Imaginary component of Inet" )
		self.InetDr = RealT( self, 0., "InetDr", "amps", "Real component of Inet demand" )
		self.InetDi = RealT( self, 0., "InetDi", "amps", "Imaginary component of Inet demand" )
		self.Inet = ComplexT( self, complex(0,0), "Inet", "amps", "Current" )
		self.I = ComplexT( self, complex(0,0), "I", "amps", "Current" )
		self.port_list = list()
		
	def LinkPort(self, port):
		self.port_list.append(port)
 			
	def preset(self):
		for p in self.port_list:
			self.V.num = complex( self.Vr.v, self.Vi.v )
			p.setIV( complex( 0., 0.), self.V.num ) 
	
	def calc(self):
		self.Inet.num = complex( 0., 0. )
		for p in self.port_list:
			self.Inet.set( self.Inet + p.I )
			
		self.Inetr.v = self.Inet.num.real
		self.Ineti.v = self.Inet.num.imag
		
	    
	def dump( self ):
		print( self.name, "Node" )
		super().realPrint()
  
		