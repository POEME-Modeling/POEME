from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from EP import EP
import math
from Table2d import Table2d
import varsg

class Capacitor( Element ):

    def __init__( c, name ):
        super().__init__( name, "Capacitor" )
        c.type = "Capacitor"
        
        c.desc = "Simple capacitor element"
        
        # tables
        c.CVc = Table2d( c, units="farad", desc="Capacitance versus dV" )
        
        # electrical locations/ports
        c.EPi = EP( c, io="in", desc="Inlet Electric Port" )
        c.EPo = EP( c, io="out", desc="Exit Electric Port" )
        
        # Variables
        c.C = RealT( c, units="farad", desc="Capacitance" )  	  
        c.dV = ComplexT( c, units="volts", desc="Voltage" )
        c.I = ComplexT( c, units="amps", desc="Current" )
        c.Z = ComplexT( c, units="ohms", desc="Impedance" )

        c.type = "Capacitor"
        c.initialList()
      
    def calc( c ):
    
    	# calculate pressure drop
        c.dV.set( c.EPi.V - c.EPo.V )
        
        # if there is a table, read it to determine C
        if c.CVc.full() == True:
        	c.C.v = c.CVc.calc( c.dV.num.real, c.dV.num.imag )
        	
		# calculate impendance
        c.Z.v = complex( 0., -1. /( c.C.v * 2. * math.pi * c.EPi.freq))
        
        # determine current
        c.I.set( c.dV/c.Z )
        
        # set the current in the ports
        # voltage does not change
        c.EPi.setIV ( -1.*c.I, c.EPi.V )
        c.EPo.setIV ( c.I, c.EPo.V )


        
    def dump( c ):
    	print( c.name1, "Capacitor", file = varsg.out )
    	super().realPrint()
       