from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from StringT import StringT
from FN import FN
from Table1d import Table1d
from MP import MP
import g
from Table2d import Table2d
from BooleanT import BooleanT
from Dependent import Dependent
from Independent import Independent


class Turbine( Element ):
    
    def __init__(t,name):
        super().__init__(name,"Turbine")
        t.type = "Turbine"
        
        t.desc = "Basic turbine.  This turbine read in maps of efficiency " \
        + "and corrected weight flow as a function of corrected speed and " \
        + "pressure ratio.  The element also has two bleed input ports."

        # tables
        t.effTable = Table2d( t, desc="Table of efficiency versus corrected speed and pressure ratio" )
        t.WcTable = Table2d( t, units="lbm/sec", desc="Table of corrected weight flow versus corrected speed and pressure ratio" )
        
        # fluid locations
        t.FN41 = FN( t, desc="Station 41 after bleed 1" )
        t.FN42 = FN( t, desc="Station 42 before bleed 2" )
        t.FNi = FN( t, io="in", desc="Primary input flow" )
        t.FNiBld1 = FN( t, io="in", desc="First bleed flow (before turbine)" )
        t.FNiBld2 = FN( t, io="in", desc="Second bleed flow (after turbine)" )
        t.FNideal = FN( t, desc="Ideal flow conditions" )
        t.FNo = FN( t, io="out", desc="Primary outlet floe" )
        
        # mechanical connections
        t.MP = MP( t, io="out", desc="Connection to shaft" )

        # solver stuff
        t.ind_TPR = Independent( t, indname="PR", perturb=.05, perturb_type="Relative", active=True, desc="Varies pressure ratio" )        
        t.dep_TW = Dependent( t, d1name="Wc", d2name="WcMap", active=False, desc="Handles flow error" )

        # variables
        t.eff = RealT( t, units="none", desc="Efficiency" )
        t.effDes = RealT( t, units="none", desc="Desired deisgn efficiency" )
        t.effMap = RealT( t, units="none", desc="Efficiency read from map" ) 
        t.effScale = RealT( t, units="none", desc="Scale factor on efficiency" )
        t.Nc = RealT( t, units="RPM", desc="Corrected speed" )   
        t.NcMap = RealT( t, units="RPM", desc="Speed used to read map" ) 
        t.NcMapDes = RealT( t, units="RPM", desc="Design speed map location" ) 
        t.NcScale = RealT( t, units="none", desc="Scale factor on corrected speed" ) 
        t.PR = RealT( t, units="none", desc="Pressure ratio" )
        t.PRmap = RealT( t, units="none", desc="Pressure ratio read from map" ) 
        t.PRmapDes = RealT( t, units="none", desc="Design pressure ratio on map" )
        t.PRmapScale = RealT( t, units="none", desc="Scale on map pressure ratio" )
        t.Wc = RealT( t, units="lbm/sec", desc="Correctef flow" ) 
        t.WcDes = RealT( t, units="lbm/sec", desc="Design corrected flow" )        
        t.WcMap = RealT( t, units="lbm/sec", desc="Corrected flow read from map" )     
        t.WcScale = RealT( t, units="none", desc="scale factor of corrected flow" )                          
        
        t.size = BooleanT( t, v=True, desc="determines if the turbine is in sizing mode or not" )
        t.initialList()
        
    def calc(t):
        
        # add in the first bleed flow

        t.FN41.copy ( t.FNi )
        t.FN41.add( t.FNiBld1 )
       
        # calculate corrected conditions
        t.Nc.set( t.MP.N/( t.FNi.Tt )**.5 )
        t.Wc.set( t.FNi.W*( t.FNi.Tt )**.5/ t.FNi.Pt )  
    
        # if we are in sizing mode calculate scalars
        if t.size == True:
            t.NcScale.set( t.NcMapDes/ t.Nc )
            t.PRmapScale.set( ( t.PRmapDes.v - 1. )/( t.PR.v - 1. ))
            t.WcDes.set( t.Wc ) 
            
        # set the map independents  
        t.NcMap.set( t.NcScale*t.Nc )
        t.PRmap.set( t.PRmapScale*( t.PR - 1. ) + 1. )
    
        # read the tables
        t.effMap.set( t.effTable.calc( t.NcMap, t.PRmap  ))
        t.WcMap.set( t.WcTable.calc( t.NcMap, t.PRmap ))
    
        # if in sizing mode calculate scalars
        if t.size == True:
            t.effScale.set( t.effDes / t.effMap )
            t.WcScale.set( t.WcDes / t.WcMap )
            
        # scale the map results
        t.eff.set( t.effMap*t.effScale )
        t.WcMap.set( t.WcMap*t.WcScale )

        # calculate the expansions conditions
        t.FNideal.copy( t.FN41 )    
        t.FNideal.set_sP( t.FN41.s, t.FN41.Pt/t.PR )
        htOut = t.FNi.ht + ( t.FNideal.ht - t.FNi.ht )*t.eff
        t.FN42.copy(  t.FN41 )
        t.FN42.set_hP( htOut, t.FNideal.Pt )
        
        # add in the second bleed flow
        t.FNo.copy( t.FN42 )
        t.FNo.add( t.FNiBld2 )

        
        # set the horse power on the mechanical port
        t.MP.setHP(-1*( t.FN42.ht - t.FN41.ht )*t.FN41.W*3600./2545.)

        
  
    def precheck( t ):
        
        # if we are sizing mode dont add in the weight flow error
        if t.size.v == True:
            t.ind_TPR.active = True
            t.dep_TW.active = False
            
        # if we are not in sizing mode then add in weight flow error    
        else:
            t.ind_TPR.active = True
            t.dep_TW.active = True                   

            
    def dump( self ): 
        print( self.name1, "Turbine", file=g.out )
        super().realPrint()       
 
    def pretty( t ):
        print( f"{"Turbine"[:10]:12s}{t.name1[:10]:12s}{("PR:"+str(t.PR))[:10]:12s}{("eff:"+str(t.eff))[:10]:12s}{("PRmap:"+str(t.PRmap))[:10]:12s}{("NcMap:"+str(t.NcMap))[:10]:12s}" , file=g.pretty )
  