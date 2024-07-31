from ValueT import ValueT

class BooleanT( ValueT ):
 
    
    def __init__(self, p, var, name, desc):
        self.v = var
        self.name = name
        self.desc = desc
        p.addVID( self )
        
    def isa( s, type ):
        if type == "BooleanT":
            return True
        else:
            return False
   