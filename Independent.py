from Atom import Atom

class Independent(Atom):
    val = 0
    perturb = 0
    perturb_type = False # True is fractional
    active = False


    def __init__(self, val, perturb, perturb_type, active):
        self.val = val
        self.perturb = perturb
        self.perturb_type = perturb_type
        self.active = active
        
    def GetPerturbVal(self, step):
        if(self.perturb_type):
            return self.val * self.perturb * step
        else:
            return self.perturb
            

