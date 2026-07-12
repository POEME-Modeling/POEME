from poeme import Atom, BooleanT, RealT


class Fp(Atom):
    """Force port for spring-mass systems.

    A bond-graph force port that connects elements together. Each Fp has
    through-variable (force) and across-variable (velocity) quantities,
    plus an x-location. Ports are linked in pairs so that force and
    position/velocity are synchronized across connections.

    Parameters
    ----------
    p : Element
        Parent element that owns this port.
    io : str
        Port direction: "in" or "out".
    desc : str
        Description of the port.

    Attributes
    ----------
    F : RealT
        Force (lbf).
    x : RealT
        x location (ft).
    V : RealT
        Velocity (ft/sec).
    parent : Element
            Parent element containing this port.
    io : str
        Port direction ("in" or "out").
    other : Fp
        The paired port this port is linked to.
    name1 : str
        Name of this port.
    desc : str
        Description of this port.
    VIDL : list
        List of variable IDs associated with this port.
    """

    def __init__(self, p, io, desc, **kwargs):

        # variables
        self.VIDL = list()
        self.name1 = ""
        self.desc = desc
        self.parent = p
        self.isPort = True
        self.io = io
        self.__dict__.update(kwargs)

        # engineering variables
        self.F = RealT(self, units="lbf", desc="Force")
        self.x = RealT(self, units="ft", desc="x location")
        self.V = RealT(self, units="ft/sec", desc="velocity")
        self.isPort = BooleanT(
            self,
            v=self.isPort,
            desc="Determines if we are running to fixed Mach or Area",
        )
        p.add_vid(self)
        self.type = "Fp"
        self.other = 0

    def isa(self, type):
        """Check if this port is of a given type.

        Parameters
        ----------
        type : str
            The type string to check against.

        Returns
        -------
        bool
            True if the port type matches the given type.
        """
        return type == "Fp"

    def set_xv(self, x, v):
        """Set position and velocity on this port and the linked port.

        Parameters
        ----------
        x : RealT or float
            Position value to set.
        v : RealT or float
            Velocity value to set.
        """
        self.x.v = x.v
        if isinstance(v, float):
            self.V.v = v
        else:
            self.V.v = v.v
        self.other.x.v = self.x.v
        self.other.V.v = self.V.v

    def set_f(self, f):
        """Set force on this port and the linked port.

        Parameters
        ----------
        f : RealT or float
            Force value to set.
        """
        self.F.v = f.v
        self.other.F.v = f.v

    def add_vid(self, v):
        """Add a variable ID to this port's list.

        Parameters
        ----------
        v : object
            The variable ID to append.
        """
        self.VIDL.append(v)

    def link_fp(self, fp):
        """Link this port to another force port.

        Creates a bidirectional link so that both ports reference each other.

        Parameters
        ----------
        fp : Fp
            The other force port to link to.
        """
        self.other = fp
        fp.other = self

    def dump(self, output_file):
        """Write port state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(f"{self.parent.name1} {self.name1} {self.x} {self.V}\n")

    def hover(self):
        """Get a hover string for this port.

        Returns
        -------
        str
            A string containing the parent name, port name, position, and velocity.
        """
        return (
            self.parent.name1 + " " + self.name1 + str(self.x.v) + " " + str(self.V.v)
        )

    def pretty(self, output_file):
        """Write a formatted table row of port state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(
            f"{'Fp'[:10]:12s}{self.name1[:10]:12s}{('F:' + str(self.F))[:10]:12s}"
            f"{('F:' + str(self.F))[:10]:12s}{('x:' + str(self.x))[:10]:12s}"
            f"{('V:' + str(self.V))[:10]:12s}\n"
        )
