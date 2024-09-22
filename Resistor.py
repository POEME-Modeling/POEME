from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from EP import EP
from Table import Table
import varsg

class Resistor( Element ):
    
    def __init__(s,name):
        super().__init__(name,"Resistor")
        s.R = RealT( s, 0., "R", "Ohms", "Resistance" )  	  
        s.dV = ComplexT( s, complex(0,0),"dV", "volts", "Voltage drop" )
        s.Z = ComplexT( s, complex(0,0), "Z", "ohms","Impedance" )
        s.I = ComplexT( s, complex(0,0), "I", "amps", "Current" )
        s.EPi = EP( s, "EPi", "in", "Inlet Electric Port" )
        s.EPo = EP( s, "EPo", "out", "Exit Electric Port" )
        s.RV = Table( s, "RTable" )
      
    def calc(e):
        e.dV.set( e.EPi.V - e.EPo.V )
        if e.RV.full() == True:
        	e.R.v = e.RV.calc( e.dV.num.real)
        e.Z.num = complex( e.R.v, 0 )
        e.I.set ( e.dV/ e.Z )
        e.EPi.setIV ( -e.I.num, e.EPi.V.num)
        e.EPo.setIV ( e.I.num, e.EPo.V.num)
        
    def dump( self ): 
        print( self.name, "Resistor", file=varsg.out )
        super().realPrint()       
  
       
       