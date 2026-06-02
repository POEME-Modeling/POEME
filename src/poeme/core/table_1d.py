from scipy import interpolate


class Table1d:
    """1D lookup table for POEME.

    Provides 1D interpolation using scipy's interp1d for looking up
    values from a table of x-y pairs.

    Parameters
    ----------
    p : Element
        Parent element that owns this table.
    **kwargs : dict
        Additional keyword arguments including x, y, units, desc, etc.

    Attributes
    ----------
    name1 : str
        Name of this table.
    VIDL : int
        Variable ID list (initialized to 0).
    x : list
        X-axis data points.
    y : list
        Y-axis data points.
    desc : str
        Description of this table.
    units : str
        Units of measurement.
    parent : Element
        Parent element containing this table.
    type : str
        Type identifier ("Table1d").
    """

    def __init__(self, p, **kwargs):
        self.name1 = ""
        self.VIDL = 0
        p.add_vid(self)
        self.x = [0.0]
        self.y = [0.0]
        self.desc = ""
        self.units = ""
        self.__dict__.update(kwargs)
        self.parent = p
        self.type = "Table1d"

    def full(self):
        """Check if the table has more than one data point.

        Returns
        -------
        bool
            True if the table has data (more than one x point).
        """
        return len(self.x) > 1

    def calc(self, xin):
        """Interpolate a value from the table.

        Parameters
        ----------
        xin : float or RealT
            The x value to interpolate.

        Returns
        -------
        float
            The interpolated y value.
        """
        # find the location in the table and interpolate
        xinp = xin if isinstance(xin, float) else xin.v
        tmp = interpolate.interp1d(self.x, self.y)
        xnew = xinp
        ynew = tmp(xnew)
        return float(ynew)

    def isa(self, type):
        """Check if this object is a Table1d.

        Parameters
        ----------
        type : str
            The type string to check against.

        Returns
        -------
        bool
            True if the type matches "Table1d".
        """
        return type == "Table1d"

    def save_print(self):
        """Get string representation of this table.

        Returns
        -------
        str
            A string containing the the full table data.
        """
        temp = (self.parent.name1 + "." + self.name1 + ".x = " + str(self.x)) + "\n"
        temp = temp + (self.parent.name1 + "." + self.name1 + ".y = " + str(self.y))
        return temp
