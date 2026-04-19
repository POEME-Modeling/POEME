from ValueT import ValueT


class RealT(ValueT):

    def __init__(self, p, **kwargs):
        self.VIDL = 0
        self.v = 0.0
        self.name1 = ""
        self.units = ""
        self.desc = ""
        self.parent = p
        self.__dict__.update(kwargs)

        self.type = "RealT"
        if p == 0:
            pass
        else:
            p.addVID(self)

    def isa(s, type):
        if type == "RealT":
            return True
        else:
            return False

    def __truediv__(self, other):

        if isinstance(other, (int, float)):
            return self.v / other

        return self.v / other.v

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            return other / self.v

        return other.v / self.f

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.v * other
        return self.v * other.v

    def __rmul__(self, other):
        return self.v * other

    def __gt__(self, other):
        if isinstance(other, (int, float)):
            temp = self.v
            return temp > other
        else:
            return self.v > other.v

    def __rgt__(self, other):
        return other > self.v

    def __lt__(self, other):
        if isinstance(other, (int, float)):
            temp = self.v
            return temp < other
        else:
            return self.v < other.v

    def __rlt__(self, other):
        return other < self.v

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return self.v - other
        return self.v - other.v

    def __rsub__(self, other):
        temp = self.v
        return other - temp

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self.v + other
        return self.v + other.v

    def __radd__(self, other):
        temp = self.v
        return other + temp

    def __pow__(self, other):
        if isinstance(other, (int, float)):
            return self.v**other
        return self.v**other.v

    def __str__(self):
        length = 1
        return str(self.v)

    # def __iadd__(self, other):
    #     if isinstance(other, (int, float)):
    #         self.v = other
    #         return self
    #         print(self.v)
    #     self.v = other.v
    #     return self

    def set(self, v):
        if isinstance(v, (int, float)):
            self.v = v
        else:
            self.v = v.v

    def str(self):
        return str(self.v)

    def savePrint(self):
        return self.parent.name1 + "." + self.name1 + ".set(" + str(self.v) + ")"
