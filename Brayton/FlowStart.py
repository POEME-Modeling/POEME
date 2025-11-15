from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from StringT import StringT
from FN import FN
from Table1d import Table1d
import varsg
from Independent import Independent
from BooleanT import BooleanT

class FlowStart( Element ):
    
    def __init__(f,name):
        super().__init__(name, "FlowStart" )
        f.type = "FlowStart"
        
        f.desc = "Start a Flow stream."
        
        # variables
        f.comp = StringT( f, desc="Composition of the stream." )
        
        f.Pt = RealT( f, units="lbm/in2", desc="Pressure" )
        f.Tt = RealT( f, units="R", desc="Temperature" )
        f.W = RealT( f, units="lbm/sec", descc="Weight" )
        f.size = BooleanT( f, v=True, desc="Determine if the element is in design mode or not" )        

		# fluid locations
        f.FNo = FN( f, io="out", desc="Outgoing flow" )

		# solver stuff	
        f.ind_1 = Independent( f, indname="W", perturb=.05, scale=100, perturb_type="Relative", active=False, desc="Vary mass flow" )   
            
    def calc(f):
    	
    	# set the flow conditions 
    	f.FNo.comp.set( f.comp );
    	f.FNo.setTP( f.Tt, f.Pt )
    	f.FNo.setW( f.W )
    	
    	
    def precheck( f ):

        # design point turn off solver stuff
        if f.size == True:
        	f.ind_1.active = False
		# off design turn on solver stuff        	
        else:
            f.ind_1.active = True
           
    def dump( f ): 
    	#dump output variables    	
        print( f.name1, "FlowStart", file=varsg.out )
        super().realPrint()       
  
       
       