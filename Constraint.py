from Atom import Atom
from RealT import RealT
from ComplexT import ComplexT
from Element import Element

import varsg

class Constraint( Element ):
    val_1 = 0
    val_2 = 0
    active = True
    
    def __init__(self, name, val_1, val_2, val_scale, dep ):
        self.name = name
        self.VIDL = list()
        self.val_1 = val_1
        self.val_2 = val_2
        self.val_scale = RealT( self, val_scale, "val_scale", "", "" )     
        self.err = RealT( self, 0., "err", "", "" )        
        self.baseError = 0.
        self.active = False
        varsg.con_list.append( self )
        self.dep = dep
     
    def addVID(self,v):
        self.VIDL.append(v)
    
    def depError(d):
    	denom = max( abs( (d.val_1).getVal() ), abs( (d.val_2).getVal() ))
    	if d.val_scale.v !=0.:
    		denom = d.val_scale.v
    		
    	d.err.v = (((d.val_1).getVal()) - ( d.val_2 ).getVal())/ denom
    		
    	return d.err.v
            
    def errorCheck(d):
    	denom = max( abs( (d.val_1).getVal() ), abs( (d.val_2).getVal() ))
    	if (d.val_1).getVal()  > (d.val_2).getVal():
    	    return True
    	else:
    		return False 
		
