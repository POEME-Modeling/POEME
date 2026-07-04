from .atom import Atom
from .real_t import RealT
from .string_t import StringT
from .boolean_t import BooleanT


class Independent(Atom):
    """Independent variable element for POEME Newton solver.

    An independent variable that the Newton solver perturbs to solve
    the system of equations. Supports both absolute and relative
    perturbation types and resolves its target variable by name.

    Parameters
    ----------
    p : Element
        Parent element that owns this independent variable.
    **kwargs : dict
        Additional keyword arguments for indname, perturb, perturb_type,
        scale, active, and other attributes.

    Attributes
    ----------
    session : ModelSession
        Model session this independent belongs to.
    indname : StringT
        Name of the target independent variable.
    perturb : RealT
        Perturbation magnitude.
    perturb_type : str
        Perturbation type ("Relative" or "Absolute").
    scale : RealT
        Scaling factor for the independent.
    saved : RealT
        Saved value of the independent.
    parent : Element
        Parent element containing this independent.
    type : str
        Type identifier ("Independent").
    name1 : str
        Name of this independent.
    VIDL : list
        List of variable IDs associated with this independent.
    x : int
        GUI x location.
    y : int
        GUI y location.
    ind : RealT
        Resolved target variable.
    """

    def __init__(self, p, **kwargs):
        self.session = p.session
        self.parent = p
        self.type = "Independent"
        self.name1 = ""
        self.VIDL = list()
        self.scale = 0.0

        self.__dict__.update(kwargs)

        self.desc  = "The independent object is the link between the solver object\n"
        self.desc += "and the model.  The independent object knows the name of the\n"
        self.desc += "variable it controls and the information about how it is to be\n"
        self.desc += "varied."  

        # Variables
        self.active  = BooleanT( self, v=self.active )
        self.indname = StringT(self, v=self.indname, desc="")
        self.indname.name1 = "indname"
        self.perturb = RealT(self, v=self.perturb, units="", desc="")
        self.perturb.name1 = "perturb"
        self.perturb_type = self.perturb_type
        self.scale = RealT(self, v=self.scale, units="", desc="")
        self.scale.name1 = "scale"
        self.saved = RealT(self, units="", desc="")

        if p == 0:
            pass
        else:
            p.add_vid(self)
        # add the independent to the session
        self.session.independents.append(self)

        # gui location
        self.x = 0
        self.y = 0

    def isa(self, type):
        """Check if this atom is an Independent.

        Parameters
        ----------
        type : str
            The type string to check against.

        Returns
        -------
        bool
            True if the type matches "Independent".
        """
        return type == "Independent"

    def add_vid(self, v):
        """Add a variable ID to this independent's variable list.

        Parameters
        ----------
        v : object
            The variable ID to add.
        """
        self.VIDL.append(v)

    def perturb_v(self):
        """Calculate the perturbation value for this independent.

        Computes the perturbation based on the perturbation type:
        - "Relative": perturb_val = ind * perturb
        - "Absolute": perturb_val = perturb

        Returns
        -------
        float
            The computed perturbation value.
        """

        # perturb the independent

        # either absolute or relative
        perturb_val = 0
        if self.perturb_type == "Relative":
            perturb_val = self.ind.v * self.perturb.v
        else:
            perturb_val = self.perturb.v
        return perturb_val

    # def get_val(self):
    # sys.exit()
    # return self.ind.v
    # def set_val(self, value):
    # self.ind.v = value

    # before running, find the memory location of the independent
    def precheck(self):
        """Resolve the target variable by name from the parent's VIDL.

        Searches the parent element's variable ID list for a variable
        whose name matches this independent's indname.
        """
        for var in self.parent.VIDL:
            if var.name1 == self.indname.v:
                self.ind = var
                return

    def __setattr__(self, name, value):
        """Set an attribute and propagate name1 to ValueT objects.

        Parameters
        ----------
        name : str
            The attribute name to set.
        value : any
            The value to assign.
        """

        super().__setattr__(name, value)
        if hasattr(getattr(self, name, None), "name1"):
            temp = getattr(self, name)
            if temp.name1 == "":
                temp.name1 = name
