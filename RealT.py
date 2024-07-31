from ValueT import ValueT

class RealT ( ValueT ):
 
    
    def __init__(self, p, var, name, units, desc):
        self.v = var
        self.name = name
        self.units = units
        self.desc = desc
        p.addVID( self )
        
    def isa( s, type ):
        if type == "RealT":
            return True
        else:
            return False
            
    def set( self, val ):
    	self.v = val.v

    # DOES NOTHING
    def addVID(self, dummy):
        pass
        
    def __add__( self, other ):
        v = self.v+other.v
        return( RealT( self, v,"","" ))
		
    def __sub__( self, other ):
        v = self.v - other.v
        return( RealT( self, v,"","" ))
		
    def __mul__( self, other ):
        num = self.v * other.v
        return( RealT( self, v,"","" ))		
		
    def __truediv__( self, other ):
        v = self.num / other.v
        return( RealT( self, v,"","" ))		
	
    def __str__(self):
        return str( self.v )
		
    # Returns a list of perturbation possibilities (3 possible for RealT)
    # perturb_type = True means Fractional    
    def Perturb(self, step, perturb_type, perturb):
        perturb_val = 0
        
        if perturb_type:
            perturb_val = self.v * perturb * step
        else:
            perturb_val = perturb * step
            
        perturb_list = [self.v - perturb_val, self.v, self.v + perturb_val]

        return perturb_list
        
    def GetVal(self):
        return self.v
        
    def SetVal(self, val):
        self.v = val
        
    #def Add(self, other):
    #return RealT(self.v + other.v, self.desc)
    
    #def IAdd( self, other ):
    #self.var = other.var
    #return RealT(other.var, self.desc)
    
    #def  Multipy(self, other):
    #return RealT(self.var * other.var, self.desc)
    