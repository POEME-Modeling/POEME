from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from Table1d import Table1d
from DP import DP

import varsg
from StringVarT import StringVarT

class PIV( Element ):
    
    def __init__( p, name ):
        super().__init__( name,"PIV" )
        p.type = "PIV"
        
        # variables
        p.P = RealT( p, units="none", desc="P" )  	  
        p.I = RealT( p, units="none", desc="I" )
        p.D = RealT( p, units="none", desc="D" )
        p.G = RealT( p, units="none", desc="G" )        
        p.elast = RealT( p, units="none", desc="Error term from last time step" )
        p.e = RealT( p, units="none", desc="Error term" )
        p.Inte = RealT( p, units="none", desc="Inte" )
        p.DPi = StringVarT( p, "Sensed value" )
        p.DPo = StringVarT( p, "Set value" )
        p.timeLast= RealT( p, units="time", desc="Last time this element ran" )
        p.type = "PIV"
     
    def calc( p ):
    	# if stepping in time them caclulate new conditions
        if ( varsg.NS.time.v > p.timeLast.v ):     
        	p.e.set( p.G - p.DPi.get() )
        	p.DPo.setVal( p.DPo.get() + ( p.P * p.e + p.D*( p.e - p.elast )/varsg.NS.dtime + p.I*( p.Inte + p.e*varsg.NS.dtime )))       
        	p.timeLast.set( varsg.NS.time )

    
    def step( p ):
    	# step in time
        p.elast.set( p.e )
        p.Inte.set( p.Inte + p.e.v*varsg.NS.dtime )
      
		
    def dump( p ): 
        print( p.name1, "PIV", file=varsg.out )
        super().realPrint()       
  
  
       
       