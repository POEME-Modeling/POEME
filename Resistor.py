from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from EP import EP

class Resistor( Element ):
    
    def __init__(s,name):
        super().__init__(name, "Resistor")
        s.R = RealT( s, 0., "R", "Resistance" )  	  
        s.dV = ComplexT( s, "dV", "Voltage" )
        s.Z = ComplexT( s, "Z", "Impedance" )
        s.I = ComplexT( s, "I", "Current" )
        s.EPi = EP( s, "EPi", "Inlet Electric Port" )
        s.EPo = EP( s, "EPo", "Exit Electric Port" )
      
    def calc(e):
        e.dV.c = e.EPi.V.c - e.EPo.V.c
        e.Z.c = complex( e.R.v, 0. )
        e.I.c =  e.dV.c/e.Z.c
        e.EPi.setIV ( -e.I.c, complex( 0., 0.) )
        e.EPo.setIV ( e.I.c, complex( 0. , 0.) )