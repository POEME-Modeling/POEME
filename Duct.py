from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from FNC import FNC
import math

class Duct( Element ):
    def __init__(s,name):
        super().__init__(name, "Duct" )
        s.dPn = RealT( s, 0.,  "dPn", "none","Normalized pressure drop" )  	  
        s.FPi = FNC( s, "FPi", "Input Port" )
        s.FPo = FNC( s, "FPo", "Output Port" )
      
    def calc(s):
        s.FPo.copy( s.FPi )
        s.FPo.set_hP( s.FPo.ht.v, s.FPo.Pt.v*( 1 - s.dPn.v ) )

    def dump( self ):
    	print( self.name, "Duct" )
    	super().realPrint()
   