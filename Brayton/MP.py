
from Atom import Atom
from ComplexT import ComplexT
from RealT import RealT
import g

class MP( Atom ):
    def __init__( m, p, **kwargs ):
        
        m.VIDL = list()
        m.name1 = ""
        m.parent = p
        m.__dict__.update( kwargs )  
        m.N = RealT( m, units="RPM", desc="Rotational speed" ) 
        m.N.name1 = "N"
        m.hp = RealT( m, units="hp", desc="Horse power passed through port" )               
        m.hp.name1 = "hp"
        m.I = RealT( m, units="lbm*ft**2", desc="Rotational Inertia" )      
        m.I.name1 = "I"
        m.other = 0
        p.addVID( m )
        m.type = "MP"
        
    def isa( m, type ):
        if type == "MP":
            return True
        else:
            return False
    
    def addVID(m,v):
        m.VIDL.append(v)
        
        
    def linkMP( m, MP ):
        m.other = MP
        MP.other = m
        
    def setN( m, N ):
        m.N.v = N
        if m.other != 0:
            m.other.N.v = N
  
    def setHP( m, HP ):
        m.hp.v = HP
        if m.other != 0:
            m.other.hp.v = HP
            
    def dump( self ):
        print( f"{self.parent.name1[:8]:10} {self.name1[:8]:10}  N:{str(self.N.v)[:8]:10s}  hp:{str(self.hp.v)[:8]:10s}  I:{str(self.I.v)[:8]:10s}", file=g.out)
        #print( self.parent.name1, self.name1, self.N.v, self.hp.v, self.I.v, file = g.out )

    def pretty ( self ):
        print( f"{self.parent.name1[:8]:10} {self.name1[:8]:10}  N:{str(self.N.v)[:8]:10s}  hp:{str(self.hp.v)[:8]:10s}  I:{str(self.I.v)[:8]:10s}", file=g.pretty)

    def hover( self ):
        return( self.parent.name1 + "." + self.name1 + "." + str( self.N.v ) + " " + str( self.hp.v ) + " " + str( self.I.v ))

    def savePrint( self ):
        temp = (self.parent.name1 +"."+ self.name1+".N.set( "+ str( self.N.v )) + ")\n"
        temp = temp + (self.parent.name1 +"."+ self.name1+".hp.set( "+ str( self.hp.v )) + ")\n"
        temp = temp + (self.parent.name1 +"."+ self.name1+".I.set( "+ str( self.I.v )) + ")\n"
        return( temp )      
        