from Atom import Atom
from Element import Element
from RealT import RealT
from ComplexT import ComplexT

import varsg

class Independent( Element ):
    val = 0
    perturb = 0
    perturb_type = False # True is fractional
    active = False
    
    def __init__(self, name, val, perturb, scale, perturb_type):
        self.name = name
        self.val  = val
        self.VIDL =  list()
        self.scale = RealT( self, 0., "scale", "", "" )  
        self.perturb = RealT( self, .001, "perturb", "", "" )  
        
        self.perturb_type = perturb_type
        varsg.ind_list.append( self )
        self.type = "Independent"
        
    def addVID(self,v):
        self.VIDL.append(v)
        
    def perturbV(self):
    	
        if type(self.val) != RealT and type(self.val) != ComplexT:
            raise Exception("Not a perturbable type (RealT or ComplexT)")
		
        perturb_val = 0
        
        if self.perturb_type:
            perturb_val = self.val.getVal() * self.perturb.v 
        else:
            perturb_val = self.perturb.v
            
        return perturb_val
         
        
    def getVal(self):
        return self.val.GetVal()

    def setVal(self, value):
        self.val.SetVal(value)
            

