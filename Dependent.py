from Atom import Atom
from RealT import RealT
from ComplexT import ComplexT


import varsg

class Dependent( Atom ):
    val_1 = 0
    val_2 = 0
    active = False
    
    def __init__(self, name, val_1, val_2, val_scale ):
        self.name = name
        self.val_1 = val_1
        self.val_2 = val_2
        self.val_scale = val_scale
        self.baseError = 0.
        varsg.dep_list.append( self )
        
    def depError(d):
    	denom = max( abs( (d.val_1).getVal() ), abs( (d.val_2).getVal() ))
    	if d.val_scale !=0.:
    		denom = d.val_scale
    	return (((d.val_1).getVal()) - ( d.val_2 ).getVal())/ denom
            

