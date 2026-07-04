from .atom import Atom
from .real_t import RealT
from .string_t import StringT


class Dependent(Atom):
    """Dependent equation element for POEME solver.

    A dependent equation that compares two values (d1 and d2) and computes
    a normalized error. Dependents are registered with the model session and
    participate in the Newton solver's convergence checking. Supports
    string-based resolution of dependent variable references across elements.

    Parameters
    ----------
    p : Element
        Parent element that owns this dependent.
    **kwargs : dict
        Additional keyword arguments for d1name, d2name, val_scale,
        active, and other attributes.

    Attributes
    ----------
    session : ModelSession
        Model session this dependent belongs to.
    d1name : StringT
        Name of the first dependent variable.
    d2name : StringT
        Name of the second dependent variable.
    err : RealT
        Current error term.
    errLast : RealT
        Last error term.
    val_scale : RealT
        Error scalar for normalization.
    parent : Element
        Parent element containing this dependent.
    type : str
        Type identifier ("Dependent").
    name1 : str
        Name of this dependent.
    VIDL : list
        List of variable IDs associated with this dependent.
    x : int
        GUI x location.
    y : int
        GUI y location.
    d1 : RealT
        Resolved first dependent variable.
    d2 : RealT
        Resolved second dependent variable.
    """

    def __init__(self, p, **kwargs):
        self.session = p.session
        self.parent = p
        self.name1 = ""
        self.type = "Dependent"
        self.VIDL = list()

        self.val_scale = 0.0
        self.__dict__.update(kwargs)

        self.desc  = "The dependent object is defines the conditions that need to be\n"
        self.desc += "met for the model to be considered valid.  It described by two\n"
        self.desc += "references to variables that have to be equal for the solution to\n"
        self.desc += "be valid.  And example would be the flow leaving a nozzle element\n"
        self.desc += "where the flow going out of the nozzle must equal the flow coming in."
 
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
        """Check if this atom is a Dependent.

        Parameters
        ----------
        type : str
            The type string to check against.

        Returns
        -------
        bool
            True if the type matches "Dependent".
        """
        return type == "Dependent"

    def add_vid(self, v):
        """Add a variable ID to this dependent's variable list.

        Parameters
        ----------
        v : object
            The variable ID to add.
        """
        self.VIDL.append(v)

    def dep_error(self):
        """Calculate the normalized error between d1 and d2.

        Computes the normalized error as (d1 - d2) / denom, where denom
        is the maximum of the absolute values of d1 and d2, or val_scale
        if it is non-zero.

        Returns
        -------
        float
            The normalized error value.
        """

        # determine the dependent error
        # first see if the user has input a scalar
        denom = max(abs(self.d1.v), abs(self.d2.v))

        if self.val_scale.v != 0.0:
            denom = self.val_scale.v

        # determine the normalized error
        self.err.v = ((self.d1.v) - (self.d2.v)) / denom
        return self.err.v

    def precheck(self):
        """Resolve string-based variable references to actual variables.

        Looks through the parent's variable IDs to find and resolve the
        d1 and d2 dependent variable references by name. Handles both
        local variables and cross-element references using dot notation.
        """

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
