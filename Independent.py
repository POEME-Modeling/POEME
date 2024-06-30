from Atom import Atom
from RealT import RealT
from ComplexT import ComplexT

import varsg

class Independent( Atom ):
    val = 0
    perturb = 0
    perturb_type = False # True is fractional
    active = False
    
    def __init__(self, name, variable):
        self.name = name
        self.variable = variable
        varsg.ind_list.append( self )
        
        
    def Perturb(self, step):
        if type(self.val) != RealT and type(self.val) != ComplexT:
            raise Exception("Not a perturbable type (RealT or ComplexT)")
        
        self.val.Perturb(step, self.perturb_type, self.perturb)
        
    def GetVal(self):
        self.val.GetVal()

    def SetVal(self):
        self.val.SetVal()
            

