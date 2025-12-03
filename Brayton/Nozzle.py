from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from StringT import StringT
from FN import FN
from Table1d import Table1d
import varsg
from Dependent import Dependent
from BooleanT import BooleanT
from IntT import IntT
from StringVarT import StringVarT
import varsg

class Nozzle( Element ):
    
    def __init__( n,name ):
        super().__init__(name,"Duct")
        n.type = "Nozzle"
        
        # variables
        n.desc = "Very basic nozzle.  Just expands flow to giving PsExh"
        n.PsExh = StringVarT( n, desc="Exhaust pressure" )
        n.Anoz = RealT( n, units="in2", desc="Throat area" )
        n.Fg = RealT( n, units="blf", desc="Gross thrust" )
        
        # flow connections
        n.FNi = FN( n, io="in", desc="Incoming flow" )
        n.FNo = FN( n, io="out", desc="Outgoing flow" )

        # dependents
        n.dep_NA = Dependent( n, d1name="Anoz", d2name="FNo.A", active=False, desc="Nozzle area error" )
        n.size = BooleanT( n, v=True, desc="determines if nozzle is in sizing mode or not" )
        
        n.initialList()
        
    def precheck( n ):
        
        # if we are in sizing mode there is no dependent
        if n.size.v == True:
            n.dep_NA.active = False
        # if we are not is sizinig mode than there is a dependent
        else:
            n.dep_NA.active = True                   


    def calc( n ):
        
        if ( n.FNo.Pt < n.PsExh.get() ):
            varsg.errors = varsg.errors + n.name1 + " nozzle pressure ratio < 1 "
        # copy the inlet flow to the exit
        n.FNo.copy( n.FNi )
        
        # set the exit conditions to Mach 1.
        n.FNo.size.set( True )
        n.FNo.MN.set( 1. )  
        n.FNo.setTP( n.FNo.Tt, n.FNo.Pt )
        if ( n.FNo.Ps > n.PsExh.get() ):
            # if we are in sizing mode then set the area
            if n.size == True:
                n.Anoz.set( n.FNo.A )
        else:
            n.FNo.Ps.set( n.PsExh.get() )
            n.FNo.PsCalc()
            if n.size == True:
                n.Anoz.set( n.FNo.A )           
            
        # calculate gross thrust
        n.Fg.set( n.FNo.W*n.FNo.V/32.17 + n.FNo.A*144.*( n.FNo.Ps - n.PsExh.get() ))
    
    
  
    def dump( self ): 
        print( self.name1, "Nozzle", file=varsg.out )
        super().realPrint()       
  
    def pretty( n ):
        print( f"{"Nozzle"[:10]:12s}{n.name1[:10]:12s}{("Fg:"+str(n.Fg))[:10]:12s}", file = varsg.pretty )
       