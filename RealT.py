from ValueT import ValueT

class RealT ( ValueT ):
    def __init__(self, p, var, name, desc):
        self.v = var
        self.name = name
        self.desc = desc
        p.addVID( self )
        
    def isa( s, type ):
        if type == "RealT":
            return True
        else:
            return False
     
    # Returns a list of perturbation possibilities (3 possible for RealT)
    # perturb_type = True means Fractional    
    def Perturb(self, step, perturb_type, perturb):
        perturb_val = 0

        if perturb_type:
            perturb_val = self.v * perturb
        else:
            perturb_val = perturb
            
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
       