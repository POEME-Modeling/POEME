from .boolean_t import BooleanT
from .real_t import RealT
from .string_t import StringT


class State:
    val_1 = 0
    val_2 = 0
    active = True

    def __init__(self, p, **kwargs):
        self.session = p.session
        self.parent = p
        self.type = "State"
        self.name1 = ""
        self.VIDL = list()
        self.val_scale = 0.0
        self.__dict__.update(kwargs)

        self.desc  = "The state object is and extension of the dependent object.  In"
        self.desc += "steady state mode it defines the conditions that need to be\n"
        self.desc += "met for the model to be considered valid.  It described by two\n"
        self.desc += "references to variables that have to be equal for the solution to\n"
        self.desc += "be valid.  And example would be the flow leaving a nozzle element\n"
        self.desc += "where the flow going out of the nozzle must equal the flow coming in.\n\n"
        self.desc += "In transient mode it will define a variable that is to be integrated\n"
        self.desc += "as well as the calculated value of the deriavative.  And example would\n"
        self.desc += "be integrating the shaft speed per the shaft speed derivative calculated.\n\n"

        # Variables
        self.d1name = StringT(self, v=self.d1name, desc="")
        self.d1name.name1 = "d1name"
        self.d2name = StringT(self, v=self.d2name, desc="")
        self.d2name.name1 = "d2name"
        self.dsname = StringT(self, v=self.dsname, desc="")
        self.dsname.name1 = "dsname"
        self.err = RealT(self, desc="Current value of error term")
        self.errLast = RealT(self, desc="Previous value of error term")
        self.sname = StringT(self, v=self.sname, desc="")
        self.sname.name1 = "sname"
        self.stateL = RealT(self, desc="Previous value of state value")
        self.val_scale = RealT(self, v=self.val_scale, desc="scalar")

        self.dsL = RealT(self, desc="")

        self.solve_state = ""
        self.trans = BooleanT(
            self, v=False, desc="determines if the state is in transient or SS mode"
        )
        if p == 0:
            pass
        else:
            p.add_vid(self)

        # add state to the session
        self.session.states.append(self)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if hasattr(getattr(self, name, None), "name1"):
            temp = getattr(self, name)
            if temp.name1 == "":
                temp.name1 = name

    def isa(self, type):
        return type == "State"

    def add_vid(self, v):
        self.VIDL.append(v)

    def dep_error(self):

        # if we are in steady state mode, just return dep error
        if self.trans.v == False:
            # deterime the appropriate denominator
            denom = max(abs(self.d1.v), abs(self.d2.v))
            if self.val_scale.v != 0.0:
                denom = self.val_scale.v

            if denom == 0.0:
                denom = 1.0

            # calculate and return the error
            self.err.v = ((self.d1.v) - (self.d2.v)) / denom

            return self.err.v

        # if we are in transient mode the error is the difference
        # between the current value of the state
        # and the integrated value of the state using the last time info
        if self.trans.v == True:
            denom = 1.0 if self.self.v == 0.0 else self.self.v

            if self.val_scale.v != 0.0:
                denom = self.val_scale.v

            # return ( self.self.v - ( self.stateL.v + ( self.ds.v  )/
            # 2.*self.session.solver.dtime.v ))
            # / denom
            return (
                self.self.v
                - (
                    self.stateL.v
                    + (self.ds.v + self.dsL.v) / 2.0 * self.session.solver.dtime.v
                )
            ) / denom

    def trim(self):
        # trim it up by setting last value to current value to start transient
        # done to start transient
        self.stateL.v = self.self.v
        self.dsL.v = 0.0

    def step(self):
        # step in time by making current value last value
        self.stateL.v = self.self.v
        self.dsL.v = self.ds.v

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
            self.d2 = RealT(self, v=float(self.d2name.v))

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

        # the state value might not be in this element
        # if that is the case, look through all of the elements
        # first block happens if the variable is local
        try:
            float(self.sname.v)
            self.self = RealT(self, float(self.sname.v), "", "")
        except ValueError:
            tempname = self.sname.v
            restofname = self.sname.v
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
                    self.self = v

        # the state value might not be in this element
        # if that is the case, look through all of the elements
        # first block happens if the variable is local
        try:
            float(self.dsname.v)
            self.ds = RealT(self, float(self.dsname.v), "", "")

        except ValueError:
            tempname = self.dsname.v
            restofname = self.dsname.v
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
                    self.ds = v
