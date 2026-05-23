from scipy import interpolate


class Table1d:
    def __init__(self, p, **kwargs):
        self.name1 = ""
        self.VIDL = 0
        p.add_vid(self)
        self.x = [0.0]
        self.y = [0.0]
        self.desc = ""
        self.units = ""
        self.__dict__.update(kwargs)
        self.parent = p
        self.type = "Table1d"

    def full(self):
        return len(self.x) > 1

    def calc(self, xin):
        # find the location in the table and interpolate
        xinp = xin if isinstance(xin, float) else xin.v
        tmp = interpolate.interp1d(self.x, self.y)
        xnew = xinp
        ynew = tmp(xnew)
        return float(ynew)

    def isa(self, type):
        return type == "Table1d"

    def save_print(self):
        temp = (self.parent.name1 + "." + self.name1 + ".x = " + str(self.x)) + "\n"
        temp = temp + (self.parent.name1 + "." + self.name1 + ".y = " + str(self.y))
        return temp
