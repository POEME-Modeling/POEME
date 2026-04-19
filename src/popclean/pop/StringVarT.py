from ValueT import ValueT
import g
import time


class StringVarT(ValueT):

    def __init__(self, p, **kwargs):
        self.v = ""
        self.ptr = 0
        self.desc = ""
        self.__dict__.update(kwargs)
        self.name1 = ""
        self.VIDL = 0
        self.parent = p
        self.valve = ""
        self.type = "StringVarT"
        if p == 0:
            pass
        else:
            p.addVID(self)

    def isa(s, type):
        if type == "StringVarT":
            return True
        else:
            return False

    def get(self):
        if self.ptr == 0:
            tempname = self.v
            restofname = self.v
            for e in g.element_list:
                top = e
                while tempname.find(".") > -1:
                    restofname = tempname[tempname.find(".") + 1 :]
                    restofname = tempname
                    tempname = tempname[0 : tempname.find(".")]
                    for v in top.VIDL:
                        temp = v.name1

                        if temp == tempname:
                            if restofname.find(".") > -1:
                                top = v
                            tempname = restofname

                restofname = restofname[restofname.find(".") + 1 :]
                for v in top.VIDL:
                    if restofname == v.name1:
                        self.ptr = v

        return self.ptr.v

    def __iadd__(self, other):
        self.set(other)
        return self

    def set(self, val):

        self.value = val

        if self.ptr == 0:
            tempname = val
            restofname = val
            top = self.parent

            for e in g.element_list:
                top = e
                if tempname[0 : tempname.find(".")] == e.name1:
                    while tempname.find(".") > -1:
                        restofname = tempname[tempname.find(".") + 1 :]
                        restofname = tempname
                        tempname = tempname[0 : tempname.find(".")]
                        for v in top.VIDL:
                            temp = v.name1
                            if temp == tempname:
                                if restofname.find(".") > -1:
                                    top = v
                                tempname = restofname

                restofname = restofname[restofname.find(".") + 1 :]

                for v in e.VIDL:
                    if restofname == v.name1:
                        self.ptr = v

    # DOES NOTHING
    def addVID(self, dummy):
        pass

    def __add__(self, other):
        v = self.v + other.v
        return RealT(self, v, "", "")

    def __sub__(self, other):
        v = self.v - other.v
        return RealT(self, v, "", "")

    def __mul__(self, other):
        num = self.v * other.v
        return RealT(self, v, "", "")

    def __truediv__(self, other):
        v = self.num / other.v
        return RealT(self, v, "", "")

    def __str__(self):
        return str(self.v)

    # Returns a list of perturbation possibilities (3 possible for RealT)
    # perturb_type = True means Fractional
    def Perturb(self, step, perturb_type, perturb):
        perturb_val = 0

        if perturb_type:
            perturb_val = self.v * perturb * step
        else:
            perturb_val = perturb * step

        perturb_list = [self.v - perturb_val, self.v, self.v + perturb_val]

        return perturb_list

    def getVal(self):
        return self.v

    def setVal(self, val):
        self.ptr.v = val

    def savePrint(self):
        temp = self.parent.name1 + "." + self.name1 + ".ptr=0\n"
        temp = (
            temp
            + self.parent.name1
            + "."
            + self.name1
            + '.set("'
            + str(self.value)
            + '")\n'
        )
        return temp

    # def Add(self, other):
    # return RealT(self.v + other.v, self.desc)

    # def IAdd( self, other ):
    # self.var = other.var
    # return RealT(other.var, self.desc)

    # def  Multipy(self, other):
    # return RealT(self.var * other.var, self.desc)
