import numpy as np
from scipy import interpolate


class Table1d:

    def __init__(self, p, **kwargs):
        self.name1 = ""
        self.VIDL = 0
        p.addVID(self)
        self.x = [0.0]
        self.y = [0.0]
        self.desc = ""
        self.units = ""
        self.__dict__.update(kwargs)
        self.parent = p
        self.type = "Table1d"

    def full(s):
        if len(s.x) > 1:
            return True
        return False

    def calc(s, xin):
        # find the location in the table and interpolate
        if isinstance(xin, float):
            xinp = xin
        else:
            xinp = xin.v

        tmp = interpolate.interp1d(s.x, s.y)
        xnew = xinp
        ynew = tmp(xnew)
        return float(ynew)

    def isa(self, type):
        if type == "Table1d":
            return True
        else:
            return False

    def savePrint(self):
        temp = (self.parent.name1 + "." + self.name1 + ".x = " + str(self.x)) + "\n"
        temp = temp + (self.parent.name1 + "." + self.name1 + ".y = " + str(self.y))
        return temp
