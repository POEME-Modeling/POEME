from Element import Element
from RealT import RealT
from Fp import Fp
from Mass import Mass
import math
from Table2d import Table2d
import g
import time

class Spring( Element ):

    def __init__( s, name ):
        super().__init__( name, "Capacitor" )
        s.type = "Spring"
        
        s.desc = "Simple spring element"
       
      
        # Variables  
        s.k = RealT( s, units = "lbf/ft", desc = "Spring constant" ) 
        s.F = RealT( s, units = "lbf/ft", desc = "Spring constant" ) 
        s.LN = RealT( s, units = "ft", desc = "Nuetral length of the spring" ) 
        s.L = RealT( s, units = "ft", desc = "actual length of the spring" )  	  

        # electrical locations/ports
        s.Fp1 = Fp( s, "out", "Force port" )
        s.Fp2 = Fp( s, "out", "Force Port" )
  
        s.type = "Spring"
        
        s.initialList()
      
    def calc( s ):
    
    	# calculate the length of the spring from the port
        s.L += s.Fp2.x - s.Fp1.x 

        # determin the force 
        s.F += -1.*s.k *( s.L - s.LN )
        s.Fp1.setF( s.F )
        s.Fp2.setF( s.F )     
        
    def dump( s ):
    	print( s.name1, "Spring", file = g.out )
    	super().realPrint()
        
    def pretty( s ):
        print( f"{"Fp"[:10]:12s}{s.name1[:10]:12s}{("L:"+str(s.L))[:10]:12s}{("F:"+str(s.F))[:10]:12s}{("k:"+str(s.k))[:10]:12s}" , file=g.pretty )
            