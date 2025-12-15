from Atom import Atom
from RealT import RealT
from ComplexT import ComplexT
from StringT import StringT
#from Element import Element

import varsg

class Independent( Atom ):
 
    
    def __init__( i, p, **kwargs):
        i.p = p
        i.type = "Independent"
        i.name1 = ""
        i.VIDL = list()
        i.scale = 0.
        
        i.__dict__.update(kwargs)  
        
        # Variables
        i.indname  = StringT( i, v=i.indname, desc="" )
        i.indname.name1 = "indname"
        i.perturb = RealT( i, v=i.perturb, units="", desc="" )
        i.perturb.name1 = "perturb"
        i.perturb_type = i.perturb_type
        i.scale = RealT( i, v=i.scale,  units="", desc="" )
        i.scale.name1 = "scale"
        i.saved = RealT( i, units="", desc="" )

        if p == 0:
           pass  
        else:
           p.addVID( i )       
        # add the independent to the global space
        varsg.ind_list.append( i )

        # gui location
        i.x = 0
        i.y = 0

    def isa( s, type ):
        if type == "Independent":
            return True
        else:
            return False
            
    def addVID(self,v):
        self.VIDL.append(v)
        
    def perturbV(self):
       
        # perturb the independent
        # either absolute or relative
        perturb_val = 0 
        if self.perturb_type == "Relative":
        	perturb_val = self.ind.v * self.perturb.v 
        else:
        	perturb_val = self.perturb.v
        return perturb_val
                
    #def getVal(self):
        #quit()
        #return self.ind.v

    #def setVal(self, value):
    	#self.ind.v = value

	# before running, find the memory location of the independent        
    def precheck(self):
    	for var in self.p.VIDL:
    		if var.name1 == self.indname.v:
    			self.ind = var
    			return
    
   
    def __setattr__(self, name, value):

        super().__setattr__(name, value)
        if (eval( "hasattr(self."+name+" ,\"name1\")" )):
        	temp = eval( "self."+name )
        	if ( temp.name1 == "" ):
        		temp.name1 = name    
        
            
 
    		 	
	
		

