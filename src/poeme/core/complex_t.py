class ComplexT:
    # real = 0
    # imag = 0

    def __init__(self, p, **kwargs):
        self.v = complex(0, 0)
        self.VIDL = 0
        self.name1 = ""
        self.units = ""
        self.desc = ""
        self.parent = p
        self.__dict__.update(kwargs)

        self.type = "ComplexT"

        if p == 0:
            pass
        else:
            p.add_vid(self)

    def add_vid(self, self1):
        pass

    def isa(self, type):
        return type == "ComplexT"

    def set(self, val):
        if isinstance(val, complex):
            self.v = val
        else:
            self.v = val.v

    def set_p(self, r, i):
        rval = r if isinstance(r, float) else r.v
        ival = i if isinstance(i, float) else i.v
        self.v = complex(rval, ival)

    def real(self):
        return self.v.real

    def __add__(self, other):
        v = self.v + other.v
        return ComplexT(self, v=v)

    def __sub__(self, other):
        val = self.v - other.v
        return ComplexT(self, v=val)

    def __rsub__(self, other):
        print(other.desc)
        val = self.v - other.v
        return ComplexT(self, v=val)

    def __mul__(self, other):
        if isinstance(other, float):
            other = complex(other, 0.0)
        v = self.v * other
        return v

    def __rmul__(self, other):
        if isinstance(other, float):
            other = complex(other, 0.0)
        v = self.v * other
        return v

    def __truediv__(self, other):
        v = self.v / other.v
        return ComplexT(self, v=v)

    def __str__(self):
        return str(self.v)

    # def __iadd__(self, other):
    #     if isinstance(other, complex):
    #         self.v = other
    #         return self
    #         print(self.v)
    #     self.v = other.v
    #     return self
