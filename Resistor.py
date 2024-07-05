from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from EP import EP

class Resistor( Element ):
    
    def __init__(s,name):
        super().__init__(name,"Resistor")
        s.R = RealT( s, 0., "R", "Resistance" )  	  
        s.dV = ComplexT( s, complex(0,0),"dV", "Voltage" )
        s.Z = ComplexT( s, complex(0,0), "Z", "Impedance" )
        s.I = ComplexT( s, complex(0,0), "I", "Current" )
        s.EPi = EP( s, "EPi", "Inlet Electric Port" )
        s.EPo = EP( s, "EPo", "Exit Electric Port" )
      
    def calc(e):
        e.dV.set( e.EPi.V - e.EPo.V )
        e.Z.num = complex( e.R.v, 0 )
        e.I.set ( e.dV/ e.Z )
        e.EPi.setIV ( -e.I.num, complex( 0., 0. ))
        e.EPo.setIV ( e.I.num, complex( 0., 0. ))
        
    def dump( self ):
        print( self.name, "Resistor" )
        super().realPrint()       
  
       
       