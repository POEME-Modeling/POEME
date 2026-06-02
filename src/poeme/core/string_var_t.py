from .real_t import RealT
from .value_t import ValueT


class StringVarT(ValueT):
    """String variable type for POEME.

    A string variable type that wraps a text value and supports
    resolution of cross-element references. Used for dynamic variable
    lookup by name string.

    Parameters
    ----------
    p : Element
        Parent element that owns this value.
    **kwargs : dict
        Additional keyword arguments including v, desc, etc.

    Attributes
    ----------
    session : ModelSession
        Model session this value belongs to.
    v : str
        String value.
    ptr : int
        Pointer to resolved variable.
    desc : str
        Description of this value.
    name1 : str
        Name of this value.
    VIDL : int
        Variable ID list (initialized to 0).
    parent : Element
        Parent element containing this value.
    valve : str
        Valve identifier.
    type : str
        Type identifier ("StringVarT").
    value : str
        Stored value for save_print.
    """

    def __init__(self, p, **kwargs):
        self.session = p.session
        self.v = ""
        self.ptr = 0
        self.desc = ""
        self.__dict__.update(kwargs)
        self.name1 = ""
        self.VIDL = 0
        self.parent = p
        self.valve = ""
        self.type = "StringVarT"
        if p == 0:
            pass
        else:
            p.add_vid(self)

    def isa(self, type):
        """Check if this value is a StringVarT.

        Parameters
        ----------
        type : str
            The type string to check against.

        Returns
        -------
        bool
            True if the type matches "StringVarT".
        """
        return type == "StringVarT"

    def get(self):
        """Get the resolved pointer value.

        Resolves the string reference to find the target variable
        and returns its value.

        Returns
        -------
        float
            The resolved variable value.
        """
        if self.ptr == 0:
            tempname = self.v
            restofname = self.v
            for e in self.session.elements:
                top = e
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
                        self.ptr = v

        return self.ptr.v

    # def __iadd__(self, other):
    #     self.set(other)
    #     return self

    def set(self, val):
        """Set the string value and resolve the pointer.

        Parameters
        ----------
        val : str
            The string value to set. If it contains a dot notation
            reference, the pointer is resolved to the target variable.
        """

        self.value = val

        if self.ptr == 0:
            tempname = val
            restofname = val
            top = self.parent

            for e in self.session.elements:
                top = e
                if tempname[0 : tempname.find(".")] == e.name1:
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

                for v in e.VIDL:
                    if restofname == v.name1:
                        self.ptr = v

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
        """Concatenate this string with another.

        Parameters
        ----------
        other : StringVarT
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
        other : StringVarT
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
        other : StringVarT
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
        other : StringVarT
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

    def get_val(self):
        """Get the current string value.

        Returns
        -------
        str
            The current string value.
        """
        return self.v

    def set_val(self, val):
        """Set the pointer value.

        Parameters
        ----------
        val : float
            The value to set on the pointer.
        """
        self.ptr.v = val

    def save_print(self):
        """Generate Python statements to restore this string variable.

        Returns
        -------
        str
            A string containing the Python assignment statements.
        """
        temp = self.parent.name1 + "." + self.name1 + ".ptr=0\n"
        temp = (
            temp
            + self.parent.name1
            + "."
            + self.name1
            + '.set("'
            + str(self.value)
            + '")\n'
        )
        return temp
