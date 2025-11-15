from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from EP import EP
import math
import varsg

class Inductor( Element ):
    def __init__( i ,name, L=0 ):
        super().__init__( name, "Inductor" )
        i.type = "Inductor"
        i.desc = "Simple inductor element"

		# electrical locations/ports
        i.EPi = EP( i, io="in", desc="Inlet Electric Port" )
        i.EPo = EP( i, io="out", desc="Exit Electric Port" )
      
        # variables
        i.dV = ComplexT( i, units="volts", desc="Voltage drop" )
        i.I = ComplexT( i, units="amps", desc="Current" )
        i.L = RealT( i, units="ohms", desc="Inductance" )  	  
        i.Z = ComplexT( i, units="ohms", desc="Impedance" )
        i.initialList()

      
    def calc( i ):
    	
    	# determine the voltage drop
        i.dV.set( i.EPi.V - i.EPo.V )
        
        # deterine the impedance 
        i.Z.v = complex( 0., 2 * math.pi * i.EPi.freq * i.L.v )
        
        # calculate the current
        i.I.set( i.dV/i.Z )
        
        # set the ports
        # voltage does not chage
        i.EPi.setIV ( -1.*i.I, i.EPi.V )
        i.EPo.setIV ( i.I, i.EPo.V )
        
    def dump( self ):
    	print( self.name1, "Inductor", file = varsg.out )
    	super().realPrint()
   