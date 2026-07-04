from poeme import Atom, RealT


class DP(Atom):
    """Double-precision variable for Brayton cycle solver coupling.

    A double-precision (DP) variable that links two values together so that
    setting one automatically updates the other. Used for solver coupling
    between elements in the Brayton cycle model.

    Parameters
    ----------
    p : Element
        Parent element that owns this DP variable.
    name : str
        Name of the DP variable.
    io : str
        Direction: "in" or "out".
    desc : str
        Description of the DP variable.

    Attributes
    ----------
    D : RealT
        The double-precision data value.
    other : DP
        The paired DP variable that is linked to this one.
    VIDL : list
        List of variable IDs associated with this DP.
    """

    def __init__(self, p, name, io, desc):

        self.VIDL = list()
        self.name = name
        self.desc = desc
        self.parent = p
        self.io = io
        self.D = RealT(self, 0.0, "D", "", "Data Value")
        p.add_vid(self)
        self.type = "DP"

    def isa(self, type):
        """Check if this DP matches a given type string.

        Parameters
        ----------
        type : str
            Type string to compare against.

        Returns
        -------
        bool
            True if the type is "DP", False otherwise.
        """
        return type == "DP"

    def set(self, v):
        """Set the data value on this DP and its linked partner.

        Parameters
        ----------
        v : float
            Value to set on both D fields.
        """
        self.D.v = v
        self.other.D.v = v

    def add_vid(self, v):
        """Add a variable ID to this DP's VIDL list.

        Parameters
        ----------
        v : object
            Variable ID to append.
        """
        self.VIDL.append(v)

    def link_dp(self, dp):
        """Link this DP to another DP so they share values.

        Parameters
        ----------
        dp : DP
            The other DP variable to link with.
        """
        self.other = dp
        dp.other = self

    def dump(self, output_file):
        """Dump this DP's state to an output file.

        Parameters
        ----------
        output_file : file-like
            File object to write the DP state to.
        """
        output_file.write(f"{self.parent.name} {self.name} {self.D.v}\n")
