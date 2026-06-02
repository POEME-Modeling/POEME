from .value_t import ValueT

# TODO: remove iadd, check all T types and operators


class BooleanT(ValueT):
    """Boolean value type for POEME.

    A boolean value type that wraps a boolean value and integrates with
    the POEME variable identification (VID) system. Supports comparison
    operations and serialization for saving/printing.

    Parameters
    ----------
    p : Element
        Parent element that owns this value.
    **kwargs : dict
        Additional keyword arguments passed to the parent class.

    Attributes
    ----------
    v : bool
        Boolean value.
    VIDL : int
        Variable ID list (initialized to 0).
    name1 : str
        Name of this value (initialized to empty string).
    parent : Element
        Parent element containing this value.
    """

    def __init__(self, p, **kwargs):
        self.parent = p
        self.__dict__.update(kwargs)
        self.VIDL = 0
        self.name1 = ""
        p.add_vid(self)

    def __eq__(self, other):
        """Check equality between this boolean and another value.

        Parameters
        ----------
        other : bool or BooleanT
            The value to compare against.

        Returns
        -------
        bool
            True if the values are equal.
        """
        return self.v == other

    __hash__ = None

    def set(self, val):
        """Set the boolean value.

        Parameters
        ----------
        val : bool
            The boolean value to set.
        """
        self.v = val

    def __str__(self):
        """Convert the boolean value to a string.

        Returns
        -------
        str
            String representation of the boolean value.
        """
        return str(self.v)

    def isa(self, type):
        """Check if this value is a BooleanT.

        Parameters
        ----------
        type : str
            The type string to check against.

        Returns
        -------
        bool
            True if the type matches "BooleanT".
        """
        return type == "BooleanT"

    # def __iadd__(self, other):
    #     if isinstance(other, bool):
    #         self.v = other
    #         return self
    #         print(self.v)
    #     self.v = other.v
    #     return self

    def save_print(self):
        """Generate a Python statement to restore this boolean value.

        Returns
        -------
        str
            A string containing the Python assignment statement.
        """
        return self.parent.name1 + "." + self.name1 + ".set(" + str(self.v) + ")"
