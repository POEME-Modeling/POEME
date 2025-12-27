from Element import Element
from RealT import RealT
from StringT import StringT
from IntT import IntT
from ComplexT import ComplexT
#Afrom EP import EP
from Table1d import Table1d
import g
import os

class Output(Element):
    
    def __init__( s, name, **kwargs ):
        super().__init__( name, "Output" )
        s.name = name
        s.vars = ()
        s.filename = StringT( s, v="", desc="Output file" )  
        s.__dict__.update(kwargs)
        s.row = 0 
        s.initialList()
      
    def isA(s, type ):
    	if ( type == "Output" ):
    		return True
    	else:
    		return False
			
    def calc(e):
    	pass

    def dump( s ): 
        #print( "in dump" )
        temp =  ""
        s.out = open( s.filename.v, "a")
        if s.row == 0:
        	os.system( "del " + s.filename.v )
        	s.out = open( s.filename.v, "a")
        	for e in s.vars:
        		if e.parent == 0:
        			temp = temp + f"{e.name1[:10]:12s}"
        		else:
        		   temp = temp + f"{(e.parent.name1 + "." + e.name1)[:10]:12s}"
        	print( temp, file=s.out )
		
        temp = ""	
        if( len( g.errors ) > 0 ): 
            print( g.errors, file=s.out )
        for e in s.vars:
            temp =  temp + f"{str(e)[:10]:12s}"
        print( temp, file=s.out )		
        super().realPrint()
        s.row += 1
        s.out.close()
  
               #print( f"{"Fp"[:10]:12s}{w.name1[:10]:12s}{("xloc:"+str(w.xloc))[:10]:12s}" , file=g.pretty )
 
       