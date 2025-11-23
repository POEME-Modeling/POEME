from Element import Element
from RealT import RealT
from BooleanT import BooleanT
from ComplexT import ComplexT
from StringT import StringT
from FN import FN
from Table1d import Table1d
import varsg

class Burner( Element ):
    
    def __init__( b, name ):
        super().__init__( name, "Burner" )
        b.type = "Burner"        
        
        b.desc = "Adds fuel to fuel and burns it."


        # fluid locations/ports
        b.FNi = FN( b, io="in", desc="Incoming flow" )
        b.FNo = FN( b, io="out", desc="Outgoing flow" )        

        # Variables       
        b.dP = RealT( b, units="none", desc="Pressure loss (fractional)" )
        b.eff = RealT( b, v=1., units="none", desc="Burner efficiency" )        
        b.FAR = RealT( b, units="none", desc="Fuel to air ratio" )
        b.LHV = RealT( b, units="BTU/lbm", desc="Fuel enthalpy" )  
        b.WFset = BooleanT( b, v=False, desc="If true the user is setting fuel flow" )
        b.Tout = RealT( b, units="R", desc="Exit temperature" )         
        b.Wfuel = RealT( b, units="lbm/s", desc="Fuel flow" ) 
        
        b.initialList()

    def calc( b ):
        
        # pass incoming flow information along
        b.FNo.copy( b.FNi )

        # determine if we are running to input fuel flow or FAR
        if b.WFset == False:
            b.Wfuel.set( b.FNi.W * b.FAR )
        else:
            b.FAR.set( b.Wfuel / b.FNi.W )

        #`set the exit conditions
        b.FNo.setW( b.FNi.W + b.Wfuel )
        b.FNo.FAR.set( b.FAR )
        htout = ( b.FNi.ht*b.FNi.W + b.Wfuel*b.LHV )/b.FNo.W
        b.FNo.set_hP( htout, b.FNo.Pt*( 1- b.dP ) )

    def dump( self ): 
        print( self.name1, "Burner", file=varsg.out )
        super().realPrint()       
 

       

       
       