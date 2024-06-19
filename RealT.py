class RealT:
    def __init__(self, p,var, name, desc):
        self.v = var
        self.name = name
        self.desc = desc
        p.addVID( self )
        
    def isa( s, type ):
        if type == "RealT":
            return True
        else:
            return False
    		
    #def Add(self, other):
        #return RealT(self.v + other.v, self.desc)

    #def IAdd( self, other ):
        #self.var = other.var
        #return RealT(other.var, self.desc)
        
    #def  Multipy(self, other):
        #return RealT(self.var * other.var, self.desc)
       