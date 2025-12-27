from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from StringT import StringT
from FN import FN
from Table1d import Table1d
import g
from Independent import Independent
from Dependent import Dependent 
from BooleanT import BooleanT

class FlowStartEnd2D( Element ):
    
    def __init__(f,name):
        super().__init__(name, "FlowStart" )
        f.type = "FlowStart"
        
        f.desc = "Start a Flow stream."
        
        # variables
        f.comp = StringT( f, desc="Composition of the stream." )
        f.Pt = RealT( f, units="lbm/in2", desc="Pressure" )
        f.ht = RealT( f, units="Btu/lbm", desc="Specfic enthalpy" )
        f.W = RealT( f, units="lbm/sec", desc="Weight flow" )
        f.size = BooleanT( f, desc="Determine if the element is in design mode or not" )        

		# fluid locations
        f.FNi = FN( f, io="out", desc="Incoming flow" )
        f.FNo = FN( f, io="out", desc="Outgoing flow" )
        
		# solver stuff	
        f.dep_ht = Dependent( f, d1name="ht", d2name="FNi.ht", active=True, desc="Insure the enthalpy loop closes" )
        f.depPt = Dependent( f, d1name="Pt", d2name="FNi.Pt", active=True, desc="Insure the pressue loop closes" )
        f.depW = Dependent( f, d1name="W", d2name="FNi.W", active=False, desc="Insure the pressue loop closes" )
 
     
    def calc(f):
    	
    	# set the flow conditions 
    	f.FNo.comp += f.comp
    	f.FNo.set_hP( f.ht, f.Pt )
    	f.FNo.setW( f.W )
    	 
    def dump( f ): 
    	#dump output variables    	
        print( f.name1, "FlowStart", file=g.out )
        super().realPrint()       
  
    def pretty( f ):
        print( f"{"FSE2D"[:10]:12s}{f.name1[:10]:12s}{("W:"+str(f.W))[:10]:12s}{("Pt:"+str(f.FNo.Pt))[:10]:12s}{("Tt:"+str(f.FNo.Tt))[:10]:12s}" , file=g.pretty )
            
       