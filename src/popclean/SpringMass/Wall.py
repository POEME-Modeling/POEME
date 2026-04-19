from Element import Element
from Dependent import Dependent
from State import State
from Independent import Independent
from ComplexT import ComplexT
from RealT import RealT
import g

class Wall( Element ):
    
    def __init__( m, name ):
        super().__init__( name, "Wall" )
        m.name = name
        
        m.desc = "This element is wall for the spring system.  It has \n " \
        + "x location but does not move."
        
        # force connections
        m.port_list = list()
        

        # Variables
        m.xloc = RealT( m, units = "ft", desc = "X location of the node" )
        m.Fp = RealT( m, units = "lbf", desc = "Force in the positive direction" )
        m.Fn = RealT( m, units = "lbf", desc = "Force in the negative direction" )

        m.initialList()
        
    # first step in solver pass is to set the voltage in all of the ports
    def preset( m ):
        for p in m.port_list:
            p.setxV( m.xloc, 0.  ) 
            
    # before anything is run at all, loop through all substructures to find the 
    # ports
    def precheck( m ):
        m.port_list = list()
        for p in m.VIDL:
            if p.isa( "Fp" ):
                m.port_list.append( p )
    
    
    def calc( m ):
        
        # zero out the running current totals
        m.Fp.set( 0. )
        m.Fn.set( 0. )

        
        # loops through the ports
        # if current coming in, add it to in total
        # if current going out, add it to the out total
        for p in m.port_list:
            if p.F > 0.:
                if p.io == "in":
                    m.Fp+= m.Fp + p.F 
                else:
                    m.Fn+=  m.Fp - p.F 
            if p.F < 0.:
                if p.io == "out":
                    m.Fp+= m.Fp - p.F 
                else:
                    m.Fn+= m.Fp + p.F           
        
    
    def dump( self ):
        print( self.name, "Node", file = g.out )
        super().realPrint()
    
    def pretty( w ):
        print( f"{"Fp"[:10]:12s}{w.name1[:10]:12s}{("xloc:"+str(w.xloc))[:10]:12s}" , file=g.pretty )
            