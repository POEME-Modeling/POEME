from Element import Element
from Dependent import Dependent
from Independent import Independent
from State import State
from ComplexT import ComplexT
from RealT import RealT
from BooleanT import BooleanT
import g

class Perf( Element ):
    
    def __init__( p,name ):
        super().__init__( name, "Shaft" )
        p.type = "Perf"
        
        p.desc = "Simple overall performance calculation"
        
        # variables
        p.alt = RealT( p, units="ft", desc="Altitude" )       
        p.Fg = RealT( p, units="lbf", desc="Gross thrust" )
        p.Fn = RealT( p, units="lbf", desc="Net thrust" )
        p.MN = RealT( p, desc="Mach number" )             
        p.SFC = RealT( p, units="??", desc="Specifc fuel consumption" )
        p.Wfuel = RealT( p, units="lbm/s", desc="Fuel flow" )
        p.Fram = RealT( p, units="lbf", desc="Ram drag" )
        
        p.initialList()


            

    def calc(p):
    
        p.Fg.set( 0. )
        p.Wfuel.set( 0. )
        p.Fram.set( 0. )
        
        # loop through elements to find the nozzles and burners 
        for e in g.element_list:
            if e.type == "Nozzle":
                p.Fg.set(  p.Fg + e.Fg )
            if e.type == "Burner":
                p.Wfuel.set( p.Wfuel + e.Wfuel )
            if e.type == "FlightConditionsSMJ":
                p.Fram.set( p.Fram + e.Fram )
                p.alt.set( e.alt )
                p.MN.set( e.MN )
                 
        # calculate SFC
        p.Fn.set( p.Fg - p.Fram )
        p.SFC.set( p.Wfuel/ p.Fn*3600. ) 

        

    def dump( self ):
        print( self.name, "Shaft", file = g.out )
        super().realPrint()
        
    def pretty( p ):
        print( f"{"Performance"[:10]:12s}{p.name1[:10]:12s}{("alt:"+str(p.alt))[:10]:12s}{("MN:"+str(p.MN))[:10]:12s}{("Fn:"+str(p.Fn))[:10]:12s}{("SFC:"+str(p.SFC))[:10]:12s}{("Fg:"+str(p.Fg))[:10]:12s}{("Fram:"+str(p.Fram))[:10]:12s}{("Wfuel:"+str(p.Wfuel))[:10]:12s} " , file=g.pretty )
         