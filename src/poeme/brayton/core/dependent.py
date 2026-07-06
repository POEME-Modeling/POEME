from .atom import Atom
from .real_t import RealT
from .string_t import StringT


class Dependent(Atom):
    # def __init__( self, p, d1name, d2name, val_scale, active, desc ):
    def __init__(self, p, **kwargs):
        self.session = p.session
        self.parent = p
        self.name1 = ""
        self.type = "Dependent"
        self.VIDL = list()

        self.val_scale = 0.0
        self.__dict__.update(kwargs)

        self.desc = "The dependent object is defines the conditions that need to be\n"
        self.desc += "met for the model to be considered valid.  It described by two\n"
        self.desc += (
            "references to variables that have to be equal for the solution to\n"
        )
        self.desc += (
            "be valid.  And example would be the flow leaving a nozzle element\n"
        )
        self.desc += (
            "where the flow going out of the nozzle must equal the flow coming in."
        )

        # Variables
        self.d1name = StringT(self, v=self.d1name, desc="")
        self.d1name.name1 = "d1name"
        self.d2name = StringT(self, v=self.d2name, desc="")
        self.d2name.name1 = "d2name"
        self.err = RealT(self, units="", desc="Current error term")
        self.err.name1 = "err"
        self.errLast = RealT(self, units="", desc="Last error term")
        self.errLast.name1 = "errLast"
        self.val_scale = RealT(self, v=self.val_scale, units="", desc="Erro scalar")
        self.val_scale.name1 = "val_scale"
        if p == 0:
            pass
        else:
            p.add_vid(self)
        # gui location
        self.x = 0
        self.y = 0

        # add the dependent to the session
        self.session.dependents.append(self)

    def isa(self, type):
        return type == "Dependent"

    def add_vid(self, v):
        self.VIDL.append(v)

    def dep_error(self):

        # determine the dependent error
        # first see if the user has input a scalar
        denom = max(abs(self.d1.v), abs(self.d2.v))

        if self.val_scale.v != 0.0:
            denom = self.val_scale.v

        # determine the normalized error
        self.err.v = ((self.d1.v) - (self.d2.v)) / denom
        return self.err.v

    def precheck(self):

        # the dependent d1 value might not be in this element
        # if that is the case, look through all of the elements
        # first block happens if the variable is local

        try:
            float(self.d1name.v)
            self.d1 = RealT(self, float(self.d1name.v), "", "")
        except ValueError:
            tempname = self.d1name.v
            restofname = self.d1name.v
            top = self.parent

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
                    self.d1 = v

        # the dependent d2 value might not be in this element
        # if that is the case, look through all of the elements
        # first block happens if the variable is local
        try:
            float(self.d2name.v)
            self.d2 = RealT(self, float(self.d2name.v), "", "")
        except ValueError:
            tempname = self.d2name.v
            restofname = self.d2name.v
            top = self.parent

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
                    self.d2 = v
