
import numpy as np
from scipy import interpolate
from scipy.interpolate import RegularGridInterpolator
import g

class Table2d ( ):

    def __init__( t, p, **kwargs ):
        t.name1 = ""
        t.VIDL = 0
        p.addVID( t )
        t.x = [ 0. ]
        t.y = [ 0. ]
        t.data = [0.]
        t.units = ""
        t.desc =""
        t.__dict__.update(kwargs)

        t.parent = p
        t.type = "Table2d"

    def full( t ):
        # determine if the table has data or not
        if len( t.x ) > 1:
            return True
        return False
         
    def calc( s, xin, yin ):
        
        # find the location in the table and interpolate
        if isinstance( xin, float ):
            x = xin
        else:
            x = xin.v

        if isinstance( yin, float ):
            y = yin
        else:
            y = yin.v
             
        xi,yi = None,None
        for i,(x1,x2) in enumerate(zip(s.x[:-1],s.x[1:])):
            if x1 <= x <= x2:
                xi,w_x2,w_x1 = i,(x-x1)/(x2-x1),(x2-x)/(x2-x1)
                break
        for i,(y1,y2) in enumerate(zip(s.y[:-1],s.y[1:])):
            if y1 <= y <= y2:
                yi,w_y2,w_y1 = i,(y-y1)/(y2-y1),(y2-y)/(y2-y1)
                break
        if x < s.x[0]:
            x1 = s.x[0]
            x2 = s.x[1]
            xi,w_x2,w_x1 = 0,(x-x1)/(x2-x1),(x2-x)/(x2-x1)
            if s.parent != 0:
                g.errors = g.errors + s.parent.name1+"."
            g.errors = g.errors + s.name1
            g.errors = g.errors + " Table 2d input to low " + str( x ) + " < " + str( s.x[0] )+"\n"            
        
        if x > s.x[len(s.x)-1]:
            x1 = s.x[len(s.x)-2]
            x2 = s.x[len(s.x)-1]
            xi,w_x2,w_x1 = len(s.x)-2,(x-x1)/(x2-x1),(x2-x)/(x2-x1)
            if s.parent != 0:
                g.errors = g.errors + s.parent.name1+"."
            g.errors = g.errors + s.name1
            g.errors = g.errors +  " Table 2d input to high " + str( x ) + " > " + str( s.x[len(s.x)-1] )+"\n"               
            
    
        if y < s.y[0]:
            y1 = s.y[0]
            y2 = s.y[1]
            yi,w_y2,w_y1 = 0,(y-y1)/(y2-y1),(y2-y)/(y2-y1)
            if s.parent != 0:
                g.errors = g.errors + s.parent.name1+"."
            g.errors = g.errors + s.name1
            g.errors = g.errors + " Table 2d input to low " + str( y ) + " < " + str( s.y[0] ) + "\n"            

            
        if y > s.y[len(s.y)-1]:
            y1 = s.y[len(s.y)-2]
            y2 = s.y[len(s.y)-1]
            yi,w_y2,w_y1 = len(s.y)-2,(y-y1)/(y2-y1),(y2-y)/(y2-y1)         
            if s.parent != 0:
                g.errors = g.errors + s.parent.name1+"."
            g.errors = g.errors + s.name1
            g.errors = g.errors + " Table 2d input to high " + str( y ) + " > " + str( s.y[len(s.y)-1] )+"\n"               

        
        #if xi is None or yi is None:
            #return False

        ave  = s.data[xi][yi]    *w_x1*w_y1
        ave += s.data[xi][yi+1]  *w_x1*w_y2
        
        ave += s.data[xi+1][yi]  *w_x2*w_y1
        ave += s.data[xi+1][yi+1]*w_x2*w_y2 
        
        return ave

    def isa( self, type ):
        if type == "Table2d":
            return True
        else:
            return False
    

    def savePrint( self ):
        temp = (self.parent.name1 +"."+ self.name1+".x = "+ str( self.x )) + "\n"
        temp = temp + (self.parent.name1 +"."+ self.name1+".y = "+ str( self.y ))+ "\n"
        temp = temp +(self.parent.name1 +"."+ self.name1+".data = "+ str( self.data ))
        return( temp )
     