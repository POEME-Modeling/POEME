from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from StringT import StringT
from FN import FN
from Table1d import Table1d
import varsg

class Duct( Element ):
    
    def __init__( d, name ):
        super().__init__( name, "Duct" )
        d.type = "Duct"
        
        d.desc = "Applies a constant enthalpy pressure drop"
        
        # Variables
        d.dP = RealT( d, v=0., units="none", desc="Pressure loss (fractional)" )
        d.Q = RealT( d, v=0., units="BTU", desc="Heat added to the duct" )
        d.Wbldfrac = RealT( d, io="out", desc="Bleed flow fraction" )  
        
        # Fluid locations
        d.FNi = FN( d, io="in", desc="Incoming flow" )
        d.FNo = FN( d, io="out", desc="Outgoing flow" )
        d.FNobld = FN( d, io="out", desc="Bleed flow" ) 
      
        d.initialList()
        
    def calc(d):
        # pass incoming flow information
        d.FNo.copy( d.FNi )
        # keep enthalpy constant and apply a pressure drop
        d.FNo.set_hP( d.FNo.ht + d.Q/d.FNi.W, d.FNo.Pt*( 1.- d.dP ) )
        d.FNobld.copy( d.FNi )
        d.FNo.setW( d.FNi.W*( 1. - d.Wbldfrac ))
        d.FNobld.setW( d.FNi.W*( d.Wbldfrac ))       
  
    def dump( d ): 
        print( d.name1, "Duct", file=varsg.out )
        super().realPrint()       

    def pretty( d ):
        print( f"{"Duct":12s}{d.name1[:10]:12s}{("dP:"+str(d.dP))[:10]:12s}{("Q:"+str(d.Q))[:10]:12s}" , file=varsg.pretty )            
      
       