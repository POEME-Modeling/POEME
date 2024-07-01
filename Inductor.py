from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from EP import EP
import math

class Inductor( Element ):
    def __init__(s,name):
        super().__init__(name, "Inductor" )
        s.L = RealT( s, 0.,  "L", "Inductance" )  	  
        s.dV = ComplexT( s, complex( 0, 0 ), "dV", "Voltage" )
        s.Z = ComplexT( s, "Z", complex(0,0),"Impedance" )
        s.I = ComplexT( s, "I", complex(0,0 ),"Current" )
        s.EPi = EP( s, "EPi", "Inlet Electric Port" )
        s.EPo = EP( s, "EPo", "Exit Electric Port" )
      
    def calc(e):
        e.dV.set( e.EPi.V - e.EPo.V )
        e.Z.num = complex( 0., 2 * math.pi * e.EPi.freq * e.L.v )
        e.I.set( e.dV/e.Z )
        e.EPi.setIV ( -e.I.num, 0. )
        e.EPo.setIV ( e.I.num, 0. )
