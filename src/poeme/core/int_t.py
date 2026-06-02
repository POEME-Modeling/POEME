from .real_t import RealT
from .value_t import ValueT


class IntT(ValueT):
    """Integer value type for POEME.

    An integer value type that wraps a numeric value and integrates with
    the POEME variable identification (VID) system. Supports arithmetic
    operations and perturbation for solver use.

    Parameters
    ----------
    p : Element
        Parent element that owns this value.
    var : float
        Initial value.
    name : str
        Name of this value.
    units : str
        Units of measurement.
    desc : str
        Description of this value.

    Attributes
    ----------
    v : float
        Numeric value.
    name : str
        Name of this value.
    units : str
        Units of measurement.
    desc : str
        Description of this value.
    parent : Element
        Parent element containing this value.
    """

    def __init__(self, p, var, name, units, desc):
        self.v = var
        self.name = name
        self.units = units
        self.desc = desc
        self.parent = p
        if p == 0:
            pass
        else:
            p.add_vid(self)

    def isa(self, type):
        """Check if this value is an IntT (returns "RealT" for compatibility).

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

    def set(self, val):
        """Set the value.

        Parameters
        ----------
        val : float or IntT
            The value to set. If an IntT is passed, its internal value
            is extracted.
        """
        self.v = val.v

    # DOES NOTHING
    def add_vid(self, dummy):
        """No-op placeholder for variable ID registration.

        Parameters
        ----------
        dummy : object
            The variable ID to register (ignored).
        """
        pass

    def __add__(self, other):
        """Add two values.

        Parameters
        ----------
        other : IntT
            The value to add.

        Returns
        -------
        RealT
            A new RealT containing the sum.
        """
        v = self.v + other.v
        return RealT(self, v, "", "")

    def __sub__(self, other):
        """Subtract two values.

        Parameters
        ----------
        other : IntT
            The value to subtract.

        Returns
        -------
        RealT
            A new RealT containing the difference.
        """
        v = self.v - other.v
        return RealT(self, v, "", "")

    def __mul__(self, other):
        """Multiply two values.

        Parameters
        ----------
        other : IntT
            The multiplier.

        Returns
        -------
        RealT
            A new RealT containing the product.
        """
        v = self.v * other.v
        return RealT(self, v, "", "")

    def __truediv__(self, other):
        """Divide this value by another.

        Parameters
        ----------
        other : IntT
            The divisor.

        Returns
        -------
        RealT
            A new RealT containing the quotient.
        """
        v = self.v / other.v
        return RealT(self, v, "", "")

    def __str__(self):
        """Convert the value to a string.

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

    def get_val(self):
        """Get the current value.

        Returns
        -------
        float
            The current value.
        """
        return self.v

    def set_val(self, val):
        """Set the current value.

        Parameters
        ----------
        val : float
            The value to set.
        """
        self.v = val

    # def Add(self, other):
    # return RealT(self.v + other.v, self.desc)

    # def IAdd( self, other ):
    # self.var = other.var
    # return RealT(other.var, self.desc)

    # def  Multipy(self, other):
    # return RealT(self.var * other.var, self.desc)
