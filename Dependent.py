from Atom import Atom
from RealT import RealT
from ComplexT import ComplexT


import varsg

class Dependent( Atom ):
    val_1 = 0
    val_2 = 0
    active = False
    
    def __init__(self, name, val_1, val_2 ):
        self.name = name
        self.val_1 = val_1
        self.val_2 = val_2
        varsg.dep_list.append( self )
        
    def DepError(self):
        return abs(float(self.val_1.GetVal()) - float(self.val_2.GetVal()))
            

