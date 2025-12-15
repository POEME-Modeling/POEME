

class ComplexT (  ):
    real = 0
    imag = 0

    def __init__( self, p,  **kwargs ):
        self.v =  complex( 0, 0 )
        self.VIDL = 0
        self.name1 =  ""
        self.units = ""
        self.desc = ""
        self.parent = p
        self.__dict__.update(kwargs) 

        self.type = "ComplexT"

        if p == 0:
            pass
        else:
            p.addVID( self )
           
    def addVID(self,self1 ):
        pass
    
    def isa( self, type ):
        if type == "ComplexT":
            return True
        else:
            return False
            
    def set( self, val ):
        if isinstance( val, complex ):
            self.v = val
        else:
            self.v = val.v      

    def setP( self, r, i ):
        if isinstance( r, float ):
            rval = r
        else:
            rval = r.v
        if isinstance( i, float ):
            ival = i
        else:
            ival = i.v
        self.v = complex( rval, ival )
        
    def real( self ):
        return self.v.real
        
    def __add__( self, other ):
        v = self.v+other.v
        return( ComplexT( self, v=v ))
        
    def __sub__( self, other ):
        val = self.v - other.v
        return( ComplexT( self, v=val  ))
        
    def __rsub__( self, other ):
        print( other.desc )
        val = self.v - other.v
        return( ComplexT( self, v=val  ))

    def __mul__( self, other ):
        if ( isinstance( other, float )):
            other = complex( other, 0. )
        v = self.v * other
        return( v )
        
    def __rmul__( self, other ):
        if ( isinstance( other, float )):
            other = complex( other, 0. )
        v = self.v * other
        return( v ) 

    def __truediv__( self, other ):
        v = self.v / other.v
        return( ComplexT( self, v=v ))      
        
    def __str__( self ):
        return str( self.v )

