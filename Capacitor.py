from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from EP import EP
import math
from Table2d import Table2d
import varsg

class Capacitor( Element ):

    def __init__(s,name):
        super().__init__(name, "Capacitor" )
        s.C = RealT( s, 0., "C", "farad", "Capacitance" )  	  
        s.dV = ComplexT( s, complex(0,0), "dV", "volts", "Voltage" )
        s.Z = ComplexT( s, complex(0,0), "Z", "ohms", "Impedance" )
        s.I = ComplexT( s, complex(0,0),"I", "amps", "Current" )
        s.EPi = EP( s, "EPi", "in", "Inlet Electric Port" )
        s.EPo = EP( s, "EPo", "out", "Exit Electric Port" )
        s.CVc = Table2d( s, "CTable" )
      
    def calc(e):
        e.dV.set( e.EPi.V - e.EPo.V )
        if e.CVc.full() == True:
        	e.C.v = e.CVc.calc( e.dV.num.real, e.dV.num.imag )
        e.Z.num = complex( 0., -1 / (e.C.v * 2. * math.pi * e.EPi.freq))
        e.I.set( e.dV/e.Z )
        e.EPi.setIV ( -e.I.num, e.EPi.V.num)
        e.EPo.setIV ( e.I.num, e.EPo.V.num)
        
    def dump( self ):
    	print( self.name, "Capacitor", file = varsg.out )
    	super().realPrint()
       