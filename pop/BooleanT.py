from ValueT import ValueT

class BooleanT( ValueT ):
 
    
    def __init__( self, p, **kwargs ):
        self.parent = p
        self.__dict__.update(kwargs)    
        self.VIDL = 0
        self.name1 = ""
        p.addVID( self )
        
        
    def __eq__( self, other ):
    	
	    return self.v == other
	
    def set(s, val ):
        s.v = val
        
    def __str__(self):
        return str( self.v )
        
    def isa( s, type ):
        if type == "BooleanT":
            return True
        else:
            return False
            
    def savePrint( self ):
    	return( self.parent.name1+"."+self.name1+".set("+ str(self.v) + ")" )
		   