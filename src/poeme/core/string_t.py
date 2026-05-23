from .real_t import RealT
from .value_t import ValueT


class StringT(ValueT):
    # def __init__(self, p, var,  desc):
    def __init__(self, p, **kwargs):
        self.v = ""
        self.desc = ""
        self.__dict__.update(kwargs)
        self.name1 = ""
        self.VIDL = 0
        self.parent = p
        self.type = "StringT"
        if p == 0:
            pass
        else:
            p.add_vid(self)

    def isa(self, type):
        return type == "StringT"

    # DOES NOTHING
    def add_vid(self, dummy):
        pass

    def __eq__(self, other):
        if isinstance(other, str):
            return self.v == other
        else:
            return self.v == other.v

    __hash__ = None

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
        v = self.num / other.v
        return RealT(self, v, "", "")

    def __str__(self):
        return str(self.v)

    # Returns a list of perturbation possibilities (3 possible for RealT)
    # perturb_type = True means Fractional
    def perturb(self, step, perturb_type, perturb):
        perturb_val = self.v * perturb * step if perturb_type else perturb * step
        perturb_list = [self.v - perturb_val, self.v, self.v + perturb_val]
        return perturb_list

    def get(self):
        return self.v

    def set(self, val):
        if isinstance(val, StringT):
            self.v = val.v
        else:
            self.v = val

    # def __iadd__(self, other):
    #     if isinstance(other, str):
    #         self.v = other
    #         return self
    #         print(self.v)
    #     self.v = other.v
    #     return self

    def save_print(self):
        return self.parent.name1 + "." + self.name1 + '.set("' + str(self.v) + '")'

    # def Add(self, other):
    # return RealT(self.v + other.v, self.desc)

    # def IAdd( self, other ):
    # self.var = other.var
    # return RealT(other.var, self.desc)

    # def  Multipy(self, other):
    # return RealT(self.var * other.var, self.desc)
