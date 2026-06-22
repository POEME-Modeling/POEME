import sys

from .atom import Atom
from .real_t import RealT
from .string_t import StringT


class Constraint(Atom):
    def __init__(self, p, **kwargs):
        self.session = p.session
        self.d1name = ""
        self.d2name = ""
        self.depname = ""
        self.val_scale = 0.0
        self.parent = p
        self.on = False

        self.type = "Constraint"
        self.name1 = ""
        self.VIDL = list()
        self.active = False
        self.on = False

        self.__dict__.update(kwargs)
        
        self.desc  = "The constraint obejct applies limits to values in a model.\n"
        self.desc += "It works by being tied to a particular dependent.  If the\n"
        self.desc += "constraint is going to be violated, the constraint will replace\n"
        self.desc += "the dependent in the solver matrix.\n\n"

        # variables
        self.baseError = 0.0

        self.d1name = StringT(self, v=self.d1name)
        self.d2name = StringT(self, v=self.d2name)
        self.depname = StringT(self, v=self.depname)
        self.val_scale = RealT(self, v=self.val_scale)
        self.err = RealT(self, v=0.0)
        self.errLast = RealT(self, v=0.0)

        # gui location
        self.x = 0
        self.y = 0
        # add constraint to the session
        self.session.constraints.append(self)
        if p == 0:
            pass
        else:
            p.add_vid(self)

    def isa(self, type):
        return type == "Constraint"

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

    def error_check(self):
        # check to see if the constraint is active
        # denom = max(abs(self.d1.v), abs(self.d2.v))
        max(abs(self.d1.v), abs(self.d2.v))
        return self.d2.v > self.d1.v

    def precheck(self):

        # the dependent d1 value might not be in this element
        # if that is the case, look through all of the elements
        # first block happens if the variable is local

        for d in self.session.dependents:
            if (d.parent.name1 + "." + d.name1) == self.depname.v:
                self.dep = d
        if self.on == True:
            self.dep.active = True
        self.active = False
        try:
            float(self.d1name.v)
            self.d1 = RealT(d, float(self.d1name.v), "", "")
        except ValueError:
            tempname = self.d1name.v
            # restofname = self.d1name.v
            top = self.parent

            if tempname.find(".") > -1:
                first = tempname[0 : tempname.find(".")]
                top = 0
                for e in self.session.elements:
                    if e.name1 == first:
                        top = e

                if top != 0:
                    second = tempname[tempname.find(".") + 1 :]
                    if second.find(".") > -1:
                        third = second[second.find(".") + 1 :]
                        second = second[0 : second.find(".")]

                        top = self.parent
                        for v in top.VIDL:
                            if second == v.name1:
                                for v2 in v.VIDL:
                                    if v2.name1 == third:
                                        self.d1 = v2
                    else:
                        top = self.parent
                        for v in top.VIDL:
                            if v.name1 == second:
                                self.d1 = v
                else:
                    first = tempname[0 : tempname.find(".")]
                    second = tempname[tempname.find(".") + 1 :]
                    top = self.parent
                    for o in top.VIDL:
                        if o.name1 == first:
                            for v in o.VIDL:
                                if v.name1 == second:
                                    self.d1 = v

                    if second.find(".") > -1:
                        third = second[second.find(".") + 1 :]
                        second = second[0 : second.find(".")]
                        sys.exit()
                        top = self.parent
                        for v in top.VIDL:
                            if second == v.name1:
                                for v2 in v.VIDL:
                                    if v2.name1 == third:
                                        self.d1 = v2
                        for v in top.VIDL:
                            if second == v.name1:
                                self.d1 = v

            else:
                for v in top.VIDL:
                    if tempname == v.name1:
                        self.d1 = v

        # the dependent d2 value might not be in this element
        # if that is the case, look through all of the elements
        # first block happens if the variable is local

        try:
            float(self.d2name.v)
            self.d2 = RealT(d, float(self.d2name.v), "", "")
        except ValueError:
            tempname = self.d2name.v
            # restofname = self.d2name.v
            top = self.parent

            if tempname.find(".") > -1:
                first = tempname[0 : tempname.find(".")]
                top = 0
                for e in self.session.elements:
                    if e.name1 == first:
                        top = e

                if top != 0:
                    second = tempname[tempname.find(".") + 1 :]
                    if second.find(".") > -1:
                        third = second[second.find(".") + 1 :]
                        second = second[0 : second.find(".")]

                        top = self.parent
                        for v in top.VIDL:
                            if second == v.name1:
                                for v2 in v.VIDL:
                                    if v2.name1 == third:
                                        self.d2 = v2
                    else:
                        top = self.parent
                        for v in top.VIDL:
                            if v.name1 == second:
                                self.d2 = v
                else:
                    first = tempname[0 : tempname.find(".")]
                    second = tempname[tempname.find(".") + 1 :]
                    top = self.parent
                    for o in top.VIDL:
                        if o.name1 == first:
                            for v in o.VIDL:
                                if v.name1 == second:
                                    self.d2 = v

                    if second.find(".") > -1:
                        third = second[second.find(".") + 1 :]
                        second = second[0 : second.find(".")]

                        top = self.parent
                        for v in top.VIDL:
                            if second == v.name1:
                                for v2 in v.VIDL:
                                    if v2.name1 == third:
                                        self.d2 = v2
                        for v in top.VIDL:
                            if second == v.name1:
                                self.d2 = v

            else:
                for v in top.VIDL:
                    if tempname == v.name1:
                        self.d2 = v
