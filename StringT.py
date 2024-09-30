from ValueT import ValueT

class StringT ( ValueT ):
 
    
    def __init__(self, p, var, name, desc):
        self.v = var
        self.name = name
        self.desc = desc
        p.addVID( self )
        
    def isa( s, type ):
        if type == "StringT":
            return True
        else:
            return False
            
    def set( self, val ):
    	self.v = val.v

