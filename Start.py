from Element import Element
from RealT import RealT
from StringT import StringT
from ComplexT import ComplexT
from FNC import FNC
import math

class Start( Element ):
    def __init__(s,name):
        super().__init__(name, "Start" )
        s.W = RealT( s, 0.,  "W", "lbm/s", "Flow" )  
        s.Tt = RealT( s, 0., "Tt", "R", "Total temperature" )
        s.Pt = RealT( s, 0., "Pt", "psia", "Total pressure" )
        s.comp = StringT( s, "comp", "none", "Composition of flow" )
        s.FPo = FNC( s, "FPo", "Output Port" )
      
    def calc(s):
        s.FPo.comp.v = s.comp.v
        s.FPo.W.v = s.W.v
        s.FPo.setTP( s.Tt.v, s.Pt.v )

    def dump( self ):
    	print( self.name, "Start" )
    	super().realPrint()
   