from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from EP import EP
import math
import varsg

class Inductor( Element ):
    def __init__(s,name):
        super().__init__(name, "Inductor" )
        s.L = RealT( s, 0.,  "L", "ohms","Inductance" )  	  
        s.dV = ComplexT( s, complex( 0, 0 ), "dV", "volts", "Voltage drop" )
        s.Z = ComplexT( s, complex(0,0), "Z", "Ohms", "Impedance" )
        s.I = ComplexT( s, complex(0,0 ), "I", "amps", "Current" )
        s.EPi = EP( s, "EPi", "in", "Inlet Electric Port" )
        s.EPo = EP( s, "EPo", "out", "Exit Electric Port" )
      
    def calc(e):
        e.dV.set( e.EPi.V - e.EPo.V )
        e.Z.num = complex( 0., 2 * math.pi * e.EPi.freq * e.L.v )
        e.I.set( e.dV/e.Z )
        e.EPi.setIV ( -e.I.num, e.EPi.V.num)
        e.EPo.setIV ( e.I.num, e.EPo.V.num)
        
    def dump( self ):
    	print( self.name, "Inductor", file = varsg.out )
    	super().realPrint()
   