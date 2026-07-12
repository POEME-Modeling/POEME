from .value_t import ValueT


class ComplexT(ValueT):
    """Complex value type for POEME.

    A complex number value type that wraps Python complex numbers and
    integrates with the POEME variable identification (VID) system.
    Supports arithmetic operations (addition, subtraction, multiplication,
    division) and real-part extraction for AC circuit analysis.

    Parameters
    ----------
    p : Element
        Parent element that owns this value.
    **kwargs : dict
        Additional keyword arguments passed to the parent class.

    Attributes
    ----------
    v : complex
        Complex number value.
    VIDL : int
        Variable ID list (initialized to 0).
    name1 : str
        Name of this value (initialized to empty string).
    units : str
        Units of measurement.
    desc : str
        Description of this value.
    parent : Element
        Parent element containing this value.
    type : str
        Type identifier ("ComplexT").
    """

    def __init__(self, p, **kwargs):
        self.v = complex(0, 0)
        self.VIDL = 0
        self.name1 = ""
        self.units = ""
        self.desc = ""
        self.parent = p
        self.__dict__.update(kwargs)

        self.type = "ComplexT"

        if p == 0:
            pass
        else:
            p.add_vid(self)

    def add_vid(self, self1):
        """No-op placeholder for variable ID registration.

        Parameters
        ----------
        self1 : object
            The variable ID to register (ignored).
        """
        pass

    def isa(self, type):
        """Check if this value is a ComplexT.

        Parameters
        ----------
        type : str
            The type string to check against.

        Returns
        -------
        bool
            True if the type matches "ComplexT".
        """
        return type == "ComplexT"

    def set(self, val):
        """Set the complex value.

        Parameters
        ----------
        val : complex or ComplexT
            The complex value to set. If a ComplexT is passed, its
            internal value is extracted.
        """
        if isinstance(val, complex):
            self.v = val
        else:
            self.v = val.v

    def set_p(self, r, i):
        """Set the complex value from real and imaginary parts.

        Parameters
        ----------
        r : float or RealT
            Real part of the complex number.
        i : float or RealT
            Imaginary part of the complex number.
        """
        rval = r if isinstance(r, float) else r.v
        ival = i if isinstance(i, float) else i.v
        self.v = complex(rval, ival)

    def real(self):
        """Extract the real part of the complex value.

        Returns
        -------
        float
            The real part of the complex number.
        """
        return self.v.real

    def __add__(self, other):
        """Add two complex values.

        Parameters
        ----------
        other : ComplexT
            The complex value to add.

        Returns
        -------
        ComplexT
            A new ComplexT containing the sum.
        """
        v = self.v + other.v
        return ComplexT(self, v=v)

    def __sub__(self, other):
        """Subtract two complex values.

        Parameters
        ----------
        other : ComplexT
            The complex value to subtract.

        Returns
        -------
        ComplexT
            A new ComplexT containing the difference.
        """
        val = self.v - other.v
        return ComplexT(self, v=val)

    def __rsub__(self, other):
        """Subtract this complex value from another.

        Parameters
        ----------
        other : complex
            The value to subtract this from.

        Returns
        -------
        ComplexT
            A new ComplexT containing the difference.
        """
        print(other.desc)
        val = self.v - other.v
        return ComplexT(self, v=val)

    def __mul__(self, other):
        """Multiply this complex value by another.

        Parameters
        ----------
        other : float or complex or ComplexT
            The multiplier. If a float, it is converted to a complex number.

        Returns
        -------
        complex or ComplexT
            The product.
        """
        if isinstance(other, float):
            other = complex(other, 0.0)
        v = self.v * other
        return v

    def __rmul__(self, other):
        """Multiply another value by this complex value.

        Parameters
        ----------
        other : float or complex
            The multiplier. If a float, it is converted to a complex number.

        Returns
        -------
        complex
            The product.
        """
        if isinstance(other, float):
            other = complex(other, 0.0)
        v = self.v * other
        return v

    def __truediv__(self, other):
        """Divide this complex value by another.

        Parameters
        ----------
        other : ComplexT
            The divisor.

        Returns
        -------
        ComplexT
            A new ComplexT containing the quotient.
        """
        v = self.v / other.v
        return ComplexT(self, v=v)

    def __str__(self):
        """Convert the complex value to a string.

        Returns
        -------
        str
            String representation of the complex number.
        """
        return str(self.v)

    # def __iadd__(self, other):
    #     if isinstance(other, complex):
    #         self.v = other
    #         return self
    #         print(self.v)
    #     self.v = other.v
    #     return self
