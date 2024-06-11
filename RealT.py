class RealT:
    def __init__(self, var, desc):
        self.var = var
        self.desc = desc
 
    def Add(self, other):
        return RealT(self.var + other.var, self.desc)

    def IAdd( self, other ):
        self.var = other.var
        return RealT(other.var, self.desc)
       
    def  Multipy(self, other):
        return RealT(self.var * other.var, self.desc)
       