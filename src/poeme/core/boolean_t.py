from .value_t import ValueT

# TODO: remove iadd, check all T types and operators


class BooleanT(ValueT):
    def __init__(self, p, **kwargs):
        self.parent = p
        self.__dict__.update(kwargs)
        self.VIDL = 0
        self.name1 = ""
        p.add_vid(self)

    def __eq__(self, other):

        return self.v == other

    __hash__ = None

    def set(self, val):
        self.v = val

    def __str__(self):
        return str(self.v)

    def isa(self, type):
        return type == "BooleanT"

    # def __iadd__(self, other):
    #     if isinstance(other, bool):
    #         self.v = other
    #         return self
    #         print(self.v)
    #     self.v = other.v
    #     return self

    def save_print(self):
        return self.parent.name1 + "." + self.name1 + ".set(" + str(self.v) + ")"
