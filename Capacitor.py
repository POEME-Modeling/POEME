from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from EP import EP
import math

class Capacitor( Element ):

    def __init__(s,name):
        super().__init__(name, "Capacitor" )
        s.C = RealT( s, 0., "C", "farad", "Capacitance" )  	  
        s.dV = ComplexT( s, complex(0,0), "dV", "volts", "Voltage" )
        s.Z = ComplexT( s, complex(0,0), "Z", "ohms", "Impedance" )
        s.I = ComplexT( s, complex(0,0),"I", "amps", "Current" )
        s.EPi = EP( s, "EPi", "Inlet Electric Port" )
        s.EPo = EP( s, "EPo", "Exit Electric Port" )
      
    def calc(e):
        e.dV.set( e.EPi.V - e.EPo.V )
        e.Z.num = complex( 0., -1 / (e.C.v * 2 * math.pi * e.EPi.freq))
        e.I.set( e.dV/e.Z )
        e.EPi.setIV ( -e.I.num, complex( 0., 0.) )
        e.EPo.setIV ( e.I.num, complex( 0., 0. ) )
  	  
    def dump( self ):
    	print( self.name, "Capacitor" )
    	super().realPrint()
       