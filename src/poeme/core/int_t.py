from .real_t import RealT
from .value_t import ValueT


class IntT(ValueT):
    def __init__(self, p, var, name, units, desc):
        self.v = var
        self.name = name
        self.units = units
        self.desc = desc
        self.parent = p
        if p == 0:
            pass
        else:
            p.add_vid(self)

    def isa(self, type):
        return type == "RealT"

    def set(self, val):
        self.v = val.v

    # DOES NOTHING
    def add_vid(self, dummy):
        pass

    def __add__(self, other):
        v = self.v + other.v
        return RealT(self, v, "", "")

    def __sub__(self, other):
        v = self.v - other.v
        return RealT(self, v, "", "")

    def __mul__(self, other):
        v = self.v * other.v
        return RealT(self, v, "", "")

    def __truediv__(self, other):
        v = self.v / other.v
        return RealT(self, v, "", "")

    def __str__(self):
        return str(self.v)

    # Returns a list of perturbation possibilities (3 possible for RealT)
    # perturb_type = True means Fractional
    def perturb(self, step, perturb_type, perturb):
        perturb_val = self.v * perturb * step if perturb_type else perturb * step
        perturb_list = [self.v - perturb_val, self.v, self.v + perturb_val]
        return perturb_list

    def get_val(self):
        return self.v

    def set_val(self, val):
        self.v = val

    # def Add(self, other):
    # return RealT(self.v + other.v, self.desc)

    # def IAdd( self, other ):
    # self.var = other.var
    # return RealT(other.var, self.desc)

    # def  Multipy(self, other):
    # return RealT(self.var * other.var, self.desc)
