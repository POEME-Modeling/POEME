import sys

from poeme import Atom, BooleanT, RealT


class MP(Atom):
    """Mechanical port for Brayton cycle shaft power transfer.

    A mechanical port (MP) that connects rotating elements together in a
    Brayton cycle model. Each MP has through-variable (horsepower) and
    across-variable (rotational speed) quantities. Ports are linked in
    pairs so that speed and horsepower are synchronized across connections.

    Parameters
    ----------
    p : Element
        Parent element that owns this mechanical port.

    Attributes
    ----------
    N : RealT
        Rotational speed (RPM).
    hp : RealT
        Horsepower passed through the port.
    I : RealT
        Rotational inertia (lbm·ft²).
    other : MP
        The paired mechanical port this port is linked to.
    VIDL : list
        List of variable IDs associated with this port.
    """

    def __init__(self, p, **kwargs):

        self.VIDL = list()
        self.name1 = ""
        self.parent = p
        self.__dict__.update(kwargs)
        self.N = RealT(self, units="RPM", desc="Rotational speed")
        self.N.name1 = "N"
        self.hp = RealT(self, units="hp", desc="Horse power passed through port")
        self.hp.name1 = "hp"
        self.I = RealT(self, units="lbm*ft**2", desc="Rotational Inertia")
        self.I.name1 = "I"
        self.other = 0
        p.add_vid(self)
        self.isPort = True
        self.isPort = BooleanT(
            self,
            v=self.isPort,
            desc="Determines if we are running to fixed Mach or Area",
        )
        self.type = "MP"

    def isa(self, type):
        """Check if this MP matches a given type string.

        Parameters
        ----------
        type : str
            Type string to compare against.

        Returns
        -------
        bool
            True if the type is "MP", False otherwise.
        """
        return type == "MP"

    def add_vid(self, v):
        """Add a variable ID to this MP's VIDL list.

        Parameters
        ----------
        v : object
            Variable ID to append.
        """
        self.VIDL.append(v)

    def link_mp(self, mp):
        """Link this MP to another MP so they share speed and horsepower.

        Validates that neither port is already linked and that the other
        object is an MP type before establishing the bidirectional link.

        Parameters
        ----------
        mp : MP
            The other mechanical port to link with.

        Raises
        ------
        SystemExit
            If either port is already linked or the other object is not an MP.
        """
        if self.other != 0:
            print(self.parent.name1 + "." + self.name1 + " is already linked ")
            sys.exit()
        if mp.other != 0:
            print(mp.parent.name1 + "." + mp.name1 + " is already linked ")
            sys.exit()
        if mp.isa("MP") == False:
            print(mp.parent.name1 + "." + mp.name1 + " is not a mechanical node ")
            sys.exit()
        self.other = mp
        mp.other = self

    def set_n(self, n):
        """Set the rotational speed on this MP and its linked partner.

        Parameters
        ----------
        n : float
            Rotational speed (RPM) to set.
        """
        self.N.v = n
        if self.other != 0:
            self.other.N.v = n

    def set_hp(self, hp):
        """Set the horsepower on this MP and its linked partner.

        Parameters
        ----------
        hp : float
            Horsepower to set.
        """
        self.hp.v = hp
        if self.other != 0:
            self.other.hp.v = hp

    def dump(self, output_file):
        """Dump this MP's state to an output file.

        Parameters
        ----------
        output_file : file-like
            File object to write the MP state to.
        """
        output_file.write(
            f"{self.parent.name1[:8]:10} {self.name1[:8]:10}  "
            f"N:{str(self.N.v)[:8]:10s}  hp:{str(self.hp.v)[:8]:10s}  "
            f"I:{str(self.I.v)[:8]:10s}\n"
        )
        # print( self.parent.name1, self.name1, self.N.v, self.hp.v, self.I.v)

    def pretty(self, output_file):
        """Print a formatted summary of this MP's state.

        Parameters
        ----------
        output_file : file-like
            File object to write the pretty-printed output to.
        """
        output_file.write(
            f"{self.parent.name1[:8]:10} {self.name1[:8]:10}  "
            f"N:{str(self.N.v)[:8]:10s}  hp:{str(self.hp.v)[:8]:10s}  "
            f"I:{str(self.I.v)[:8]:10s}\n"
        )

    def hover(self):
        """Return a hover string for this MP's current state.

        Returns
        -------
        str
            Formatted string with parent name, port name, speed, horsepower, and
            inertia.
        """
        return (
            self.parent.name1
            + "."
            + self.name1
            + "."
            + str(self.N.v)
            + " "
            + str(self.hp.v)
            + " "
            + str(self.I.v)
        )

    def save_print(self):
        """Generate Python code to restore this MP's state.

        Returns
        -------
        str
            Multi-line string containing set() calls for N, hp, and I.
        """
        temp = (
            self.parent.name1 + "." + self.name1 + ".N.set( " + str(self.N.v)
        ) + ")\n"
        temp = (
            temp
            + (self.parent.name1 + "." + self.name1 + ".hp.set( " + str(self.hp.v))
            + ")\n"
        )
        temp = (
            temp
            + (self.parent.name1 + "." + self.name1 + ".I.set( " + str(self.I.v))
            + ")\n"
        )
        return temp
