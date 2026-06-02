from .real_t import RealT
from .value_t import ValueT


class StringT(ValueT):
    """String value type for POEME.

    A string value type that wraps a text value and integrates with
    the POEME variable identification (VID) system. Supports comparison
    operations, perturbation, and serialization for saving/printing.

    Parameters
    ----------
    p : Element
        Parent element that owns this value.
    **kwargs : dict
        Additional keyword arguments including v, desc, etc.

    Attributes
    ----------
    v : str
        String value.
    desc : str
        Description of this value.
    name1 : str
        Name of this value.
    VIDL : int
        Variable ID list (initialized to 0).
    parent : Element
        Parent element containing this value.
    type : str
        Type identifier ("StringT").
    """

    # def __init__(self, p, var,  desc):
    def __init__(self, p, **kwargs):
        self.v = ""
        self.desc = ""
        self.__dict__.update(kwargs)
        self.name1 = ""
        self.VIDL = 0
        self.parent = p
        self.type = "StringT"
        if p == 0:
            pass
        else:
            p.add_vid(self)

    def isa(self, type):
        """Check if this value is a StringT.

        Parameters
        ----------
        type : str
            The type string to check against.

        Returns
        -------
        bool
            True if the type matches "StringT".
        """
        return type == "StringT"

    # DOES NOTHING
    def add_vid(self, dummy):
        """No-op placeholder for variable ID registration.

        Parameters
        ----------
        dummy : object
            The variable ID to register (ignored).
        """
        pass

    def __eq__(self, other):
        """Check equality between this string and another value.

        Parameters
        ----------
        other : str or StringT
            The value to compare against.

        Returns
        -------
        bool
            True if the values are equal.
        """
        if isinstance(other, str):
            return self.v == other
        else:
            return self.v == other.v

    __hash__ = None

    def __add__(self, other):
        """Concatenate this string with another.

        Parameters
        ----------
        other : StringT
            The string to concatenate.

        Returns
        -------
        RealT
            A new RealT containing the concatenated result.
        """
        v = self.v + other.v
        return RealT(self, v, "", "")

    def __sub__(self, other):
        """Subtract another string from this one.

        Parameters
        ----------
        other : StringT
            The string to subtract.

        Returns
        -------
        RealT
            A new RealT containing the result.
        """
        v = self.v - other.v
        return RealT(self, v, "", "")

    def __mul__(self, other):
        """Multiply this string by another.

        Parameters
        ----------
        other : StringT
            The multiplier.

        Returns
        -------
        RealT
            A new RealT containing the result.
        """
        v = self.v * other.v
        return RealT(self, v, "", "")

    def __truediv__(self, other):
        """Divide this string by another.

        Parameters
        ----------
        other : StringT
            The divisor.

        Returns
        -------
        RealT
            A new RealT containing the result.
        """
        v = self.num / other.v
        return RealT(self, v, "", "")

    def __str__(self):
        """Convert the string value to a string.

        Returns
        -------
        str
            String representation of the value.
        """
        return str(self.v)

    # Returns a list of perturbation possibilities (3 possible for RealT)
    # perturb_type = True means Fractional
    def perturb(self, step, perturb_type, perturb):
        """Generate a list of perturbation possibilities.

        Parameters
        ----------
        step : float
            Step multiplier.
        perturb_type : bool
            True for fractional perturbation, False for absolute.
        perturb : float
            Perturbation magnitude.

        Returns
        -------
        list
            A list of three values: [v - perturb_val, v, v + perturb_val].
        """
        perturb_val = self.v * perturb * step if perturb_type else perturb * step
        perturb_list = [self.v - perturb_val, self.v, self.v + perturb_val]
        return perturb_list

    def get(self):
        """Get the current string value.

        Returns
        -------
        str
            The current string value.
        """
        return self.v

    def set(self, val):
        """Set the string value.

        Parameters
        ----------
        val : str or StringT
            The string value to set. If a StringT is passed, its
            internal value is extracted.
        """
        if isinstance(val, StringT):
            self.v = val.v
        else:
            self.v = val

    def save_print(self):
        """Generate a Python statement to restore this string value.

        Returns
        -------
        str
            A string containing the Python assignment statement.
        """
        return self.parent.name1 + "." + self.name1 + '.set("' + str(self.v) + '")'
