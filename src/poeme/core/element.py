from .atom import Atom
from .real_t import RealT
from .session import ModelSession, _active_session
from .value_t import ValueT
from .vid import VID


class Element(Atom):
    """Base class for all simulation elements.

    The Element class serves as the base for all simulation elements.
    It manages variable identification (VID) lists, session association,
    attribute updates, and provides output methods for dumping and
    pretty-printing element state.

    Parameters
    ----------
    name : str
        Name of the element.
    type : str
        Type identifier for the element.
    session : ModelSession | None
        Model session to associate with this element. If None, uses
        the active session from the context variable.

    Attributes
    ----------
    session : ModelSession
        Model session this element belongs to.
    VIDL : list
        List of variable IDs associated with this element.
    type : str
        Type identifier for the element.
    name : str
        Name of the element.
    name1 : str
        Name alias for the element.
    x : float
        GUI x location.
    y : float
        GUI y location.
    ind_list : list
        List of independent variables.
    VIDLi : list
        Copy of VIDL for initial state.
    """

    def __init__(self, name, type, session: ModelSession | None = None):
        if session is None:
            session = _active_session.get()
        if session is None:
            error_msg = f"Newton {name} requires a session parameter or active "
            "ModelSession context"
            raise ValueError(error_msg)
        self.session = session
        # Bypass custom __setattr__ for internal attributes during init
        super().__setattr__("VIDL", [])
        super().__setattr__("type", type)
        super().__setattr__("name", name)
        super().__setattr__("name1", name)
        super().__setattr__("x", -1.0)
        super().__setattr__("y", 0.0)
        # object.__setattr__(self, "VIDL", [])
        # object.__setattr__(self, "type", type)
        # object.__setattr__(self, "name", name)
        # object.__setattr__(self, "name1", name)
        # object.__setattr__(self, "x", -1.0)
        # object.__setattr__(self, "y", 0.0)
        self.session.elements.append(self)

    def __setattr__(self, name, value):
        """Set an attribute, updating ValueT objects in-place.

        If the existing attribute is a ValueT, its value is updated
        in-place rather than replacing the object. Also sets name1
        on the value if it has that attribute.

        Parameters
        ----------
        name : str
            The attribute name to set.
        value : any
            The value to assign.
        """
        existing = self.__dict__.get(name)  # direct dict lookup, no descriptor overhead
        if isinstance(existing, ValueT):
            # Update the ValueT in-place, don't replace the object
            existing.set(value)
        else:
            super().__setattr__(name, value)

        # Assign name1 if the value has that attribute
        if hasattr(getattr(self, name), "name1"):
            getattr(self, name).name1 = name

    def initial_list(self):
        """Create a copy of VIDL for initial state tracking.

        Copies all variable IDs from VIDL into VIDLi for use during
        solver initialization.
        """
        self.VIDLi = list()
        for v in self.VIDL:
            self.VIDLi.append(v)

    def add_independent(self, ind):
        """Add an independent variable to this element's independent list.

        Parameters
        ----------
        ind : Independent
            The independent variable to add.
        """
        self.ind_list.append(ind)

    def list(self, type, vidl):
        """Print all RealT variables in the given VID list.

        Parameters
        ----------
        type : type
            The type to check (RealT).
        vidl : list
            The list of variable IDs to iterate.
        """
        if type == RealT:
            for v in vidl:
                print(v.name)

    def real(self, value, name, descript):
        """Create a new real variable and add it to this element.

        Parameters
        ----------
        value : float
            Initial value of the variable.
        name : str
            Name of the variable.
        descript : str
            Description of the variable.

        Returns
        -------
        VID
            The created variable identification object.
        """
        variable_id = VID(name, descript, "real")
        self.VIDL.append(variable_id)
        return value

    def isa(self, type):
        """Check if this element is of a given type.

        Parameters
        ----------
        type : str
            The type string to check against.

        Returns
        -------
        bool
            True if the element type matches the given type.
        """
        return type == "Element"

    def add_vid(self, v):
        """Add a variable ID to this element's variable list.

        Parameters
        ----------
        v : object
            The variable ID to add.
        """
        self.VIDL.append(v)

    def preset(self):
        """Set up the element before a solver pass.

        Default implementation does nothing. Override in subclasses.
        """
        pass

    def precheck(self):
        """Validate and resolve the element before simulation begins.

        Default implementation does nothing. Override in subclasses.
        """
        pass

    def dump(self, output_file):
        """Dump element state to a file.

        Default implementation does nothing. Override in subclasses.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        pass

    def step(self):
        """Advance the element by one time step.

        Default implementation does nothing. Override in subclasses.
        """
        pass

    def before(self):
        """Execute before the calculation pass.

        Default implementation does nothing. Override in subclasses.
        """
        pass

    def after(self):
        """Execute after the calculation pass.

        Default implementation does nothing. Override in subclasses.
        """
        pass

    def real_print(self, output_file):
        """Print all RealT and ComplexT variables to a file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        for v in self.VIDL:
            if v.isa("RealT"):
                output_file.write(
                    f"  {v.name1[:8]:10s} {str(v.v)[:8]:8} {v.units:8} {v.desc}\n",
                )
            if v.isa("ComplexT"):
                output_file.write(f"    {v.name1} {v.v} {v.units} {v.desc}\n")

    def pretty(self, output_file):
        """Pretty-print all RealT and ComplexT variables to a file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        for v in self.VIDL:
            if v.isa("RealT"):
                output_file.write(
                    f"  {v.name1[:8]:10s} {str(v.v)[:8]:8} {v.units:8} {v.desc}\n"
                )
            if v.isa("ComplexT"):
                output_file.write(f"    {v.name1} {v.v} {v.units} {v.desc}\n")

    def hover(self):
        """Get a hover summary string for this element.

        Returns
        -------
        str
            Summary string with element type, name, and all variable
            values, units, and descriptions.
        """
        temp1 = ""
        temp1 = self.type + " " + self.name1 + "\n"
        for v in self.VIDL:
            if v.isa("RealT"):
                temp1 = (
                    temp1
                    + " "
                    + v.name1
                    + " "
                    + str(v.v)
                    + " "
                    + v.units
                    + " "
                    + v.desc
                    + "\n"
                )
            if v.isa("ComplexT"):
                temp1 = (
                    temp1
                    + " "
                    + v.name1
                    + " "
                    + str(v.v)
                    + " "
                    + v.units
                    + " "
                    + v.desc
                    + "\n"
                )
        return temp1
