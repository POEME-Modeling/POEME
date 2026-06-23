from .atom import Atom
from .real_t import RealT
from .string_t import StringT
from .boolean_t import BooleanT


class Independent(Atom):
    def __init__(self, p, **kwargs):
        self.session = p.session
        self.parent = p
        self.type = "Independent"
        self.name1 = ""
        self.VIDL = list()
        self.scale = 0.0

        self.__dict__.update(kwargs)

        self.desc  = "The independent object is the link between the solver object\n"
        self.desc += "and the model.  The independent object knows the name of the\n"
        self.desc += "variable it controls and the information about how it is to be\n"
        self.desc += "varied."  

        # Variables
        self.active  = BooleanT( self, v=self.active )
        self.indname = StringT(self, v=self.indname, desc="")
        self.indname.name1 = "indname"
        self.perturb = RealT(self, v=self.perturb, units="", desc="")
        self.perturb.name1 = "perturb"
        self.perturb_type = self.perturb_type
        self.scale = RealT(self, v=self.scale, units="", desc="")
        self.scale.name1 = "scale"
        self.saved = RealT(self, units="", desc="")

        if p == 0:
            pass
        else:
            p.add_vid(self)
        # add the independent to the session
        self.session.independents.append(self)

        # gui location
        self.x = 0
        self.y = 0

    def isa(self, type):
        return type == "Independent"

    def add_vid(self, v):
        self.VIDL.append(v)

    def perturb_v(self):

        # perturb the independent

        # either absolute or relative
        perturb_val = 0
        if self.perturb_type == "Relative":
            perturb_val = self.ind.v * self.perturb.v
        else:
            perturb_val = self.perturb.v
        return perturb_val

    # def get_val(self):
    # sys.exit()
    # return self.ind.v
    # def set_val(self, value):
    # self.ind.v = value

    # before running, find the memory location of the independent
    def precheck(self):
        for var in self.parent.VIDL:
            if var.name1 == self.indname.v:
                self.ind = var
                return

    def __setattr__(self, name, value):

        super().__setattr__(name, value)
        if hasattr(getattr(self, name, None), "name1"):
            temp = getattr(self, name)
            if temp.name1 == "":
                temp.name1 = name
