from .value_t import ValueT


class RealT(ValueT):
    """Real value type for POEME.

    A real number value type that wraps a numeric value and integrates with
    the POEME variable identification (VID) system. Supports arithmetic
    operations (addition, subtraction, multiplication, division, power),
    comparison operations, and serialization for saving/printing.

    Parameters
    ----------
    p : Element
        Parent element that owns this value.
    **kwargs : dict
        Additional keyword arguments including v, units, desc, etc.

    Attributes
    ----------
    v : float
        Real number value.
    VIDL : int
        Variable ID list (initialized to 0).
    name1 : str
        Name of this value.
    units : str
        Units of measurement.
    desc : str
        Description of this value.
    parent : Element
        Parent element containing this value.
    type : str
        Type identifier ("RealT").
    """

    def __init__(self, p, **kwargs):
        self.VIDL = 0
        self.v = 0.0
        self.name1 = ""
        self.units = ""
        self.desc = ""
        self.parent = p
        self.__dict__.update(kwargs)

        self.type = "RealT"
        if p == 0:
            pass
        else:
            p.add_vid(self)

    def isa(self, type):
        """Check if this value is a RealT.

        Parameters
        ----------
        type : str
            The type string to check against.

        Returns
        -------
        bool
            True if the type matches "RealT".
        """
        return type == "RealT"

    def __truediv__(self, other):
        """Divide this value by another.

        Parameters
        ----------
        other : float, int, or RealT
            The divisor.

        Returns
        -------
        float
            The quotient.
        """

        if isinstance(other, (int, float)):
            return self.v / other

        return self.v / other.v

    def __rtruediv__(self, other):
        """Divide another value by this value.

        Parameters
        ----------
        other : float, int, or RealT
            The dividend.

        Returns
        -------
        float
            The quotient.
        """
        if isinstance(other, (int, float)):
            return other / self.v

        return other.v / self.v

    def __mul__(self, other):
        """Multiply this value by another.

        Parameters
        ----------
        other : float, int, or RealT
            The multiplier.

        Returns
        -------
        float
            The product.
        """
        if isinstance(other, (int, float)):
            return self.v * other
        return self.v * other.v

    def __rmul__(self, other):
        """Multiply another value by this value.

        Parameters
        ----------
        other : float or int
            The multiplier.

        Returns
        -------
        float
            The product.
        """
        return self.v * other

    def __gt__(self, other):
        """Check if this value is greater than another.

        Parameters
        ----------
        other : float, int, or RealT
            The value to compare against.

        Returns
        -------
        bool
            True if this value is greater.
        """
        if isinstance(other, (int, float)):
            temp = self.v
            return temp > other
        else:
            return self.v > other.v

    def __ge__(self, other):
        if isinstance(other, (int, float)):
            temp = self.v
            return temp >= other
        else:
            return self.v >= other.v

    def __rgt__(self, other):
        """Check if another value is greater than this value.

        Parameters
        ----------
        other : float or int
            The value to compare against.

        Returns
        -------
        bool
            True if the other value is greater.
        """
        return other > self.v

    def __lt__(self, other):
        """Check if this value is less than another.

        Parameters
        ----------
        other : float, int, or RealT
            The value to compare against.

        Returns
        -------
        bool
            True if this value is less.
        """
        if isinstance(other, (int, float)):
            temp = self.v
            return temp < other
        else:
            return self.v < other.v

    def __le__(self, other):
        if isinstance(other, (int, float)):
            temp = self.v
            return temp <= other
        else:
            return self.v <= other.v

    def __rlt__(self, other):
        """Check if another value is less than this value.

        Parameters
        ----------
        other : float or int
            The value to compare against.

        Returns
        -------
        bool
            True if the other value is less.
        """
        return other < self.v

    def __sub__(self, other):
        """Subtract another value from this value.

        Parameters
        ----------
        other : float, int, or RealT
            The value to subtract.

        Returns
        -------
        float
            The difference.
        """
        if isinstance(other, (int, float)):
            return self.v - other
        return self.v - other.v

    def __rsub__(self, other):
        """Subtract this value from another value.

        Parameters
        ----------
        other : float or int
            The value to subtract from.

        Returns
        -------
        float
            The difference.
        """
        temp = self.v
        return other - temp

    def __add__(self, other):
        """Add another value to this value.

        Parameters
        ----------
        other : float, int, or RealT
            The value to add.

        Returns
        -------
        float
            The sum.
        """
        if isinstance(other, (int, float)):
            return self.v + other
        return self.v + other.v

    def __radd__(self, other):
        """Add this value to another value.

        Parameters
        ----------
        other : float or int
            The value to add to.

        Returns
        -------
        float
            The sum.
        """
        temp = self.v
        return other + temp

    def __pow__(self, other):
        """Raise this value to a power.

        Parameters
        ----------
        other : float, int, or RealT
            The exponent.

        Returns
        -------
        float
            The result of raising this value to the power.
        """
        if isinstance(other, (int, float)):
            return self.v**other
        return self.v**other.v

    def __str__(self):
        """Convert the value to a string.

        Returns
        -------
        str
            String representation of the value.
        """
        # length = 1
        return str(self.v)

    def set(self, v):
        """Set the real value.

        Parameters
        ----------
        v : float, int, or RealT
            The value to set. If a RealT is passed, its internal value
            is extracted.
        """
        if isinstance(v, (int, float)):
            self.v = v
        else:
            self.v = v.v

    def str(self):
        """Convert the value to a string.

        Returns
        -------
        str
            String representation of the value.
        """
        return str(self.v)

    def save_print(self):
        """Get string representation of this data.

        Returns
        -------
        str
            A string containing the the data.
        """
        return self.parent.name1 + "." + self.name1 + ".set(" + str(self.v) + ")"
