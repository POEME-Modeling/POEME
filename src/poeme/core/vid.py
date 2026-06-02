from .atom import Atom


class VID(Atom):
    """Variable identification for POEME.

    The VID class provides a lightweight wrapper for variable identification
    within the POEME simulation framework, storing name, description, and
    type information for each variable.

    Parameters
    ----------
    name : str
        Name of the variable.
    descript : str
        Description of the variable.
    type : str
        Type identifier for the variable.

    Attributes
    ----------
    name : str
        Name of the variable.
    descript : str
        Description of the variable.
    type : str
        Type identifier for the variable.
    """

    def __init__(self, name, descript, type):
        self.name = name
        self.descript = descript
        self.type = type
