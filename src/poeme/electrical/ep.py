from poeme import Atom, BooleanT, ComplexT, RealT


class EP(Atom):
    """Electrical port for bond-graph circuit connections.

    A bond-graph electrical port that connects elements together. Each EP has
    through-variable (current) and across-variable (voltage) quantities,
    represented as complex numbers for AC steady-state analysis. Ports are
    linked in pairs so that voltage and current are synchronized across connections.

    Parameters
    ----------
    parent : Element
        Parent element that owns this port.
    io : str
        Port direction: "in" or "out".

    Attributes
    ----------
    freq : RealT
        System frequency (hz).
    I : ComplexT
        Current (amps).
    Ii : RealT
        Imaginary component of current (amps).
    Ir : RealT
        Real component of current (amps).
    V : ComplexT
        Voltage (volts).
    Vr : RealT
        Real component of voltage (volts).
    Vi : RealT
        Imaginary component of voltage (volts).
    parent : Element
        Parent element containing this port.
    io : str
        Port direction ("in" or "out").
    other : EP
        The paired port this port is linked to.
    name1 : str
        Name of this port.
    VIDL : list
        List of variable IDs associated with this port.
    """

    def __init__(self, parent, **kwargs):

        self.parent = parent
        self.name1 = ""
        # variables
        self.VIDL = list()
        self.isPort = True
        self.__dict__.update(kwargs)

        # engineering variables
        self.freq = RealT(self, units="hz", desc="frequency")
        self.freq.name1 = "freq"
        self.I = ComplexT(self, units="amps", desc="Amperage")
        self.I.name1 = "I"
        self.Ii = RealT(self, units="amps", desc="Imaginary amperage")
        self.Ii.name1 = "Ii"
        self.Ir = RealT(self, units="amps", desc="Real amperage")
        self.Ir.name1 = "Ir"
        self.V = ComplexT(self, units="volts", desc="Voltage")
        self.V.name1 = "V"
        self.Vr = RealT(self, units="volts", desc="Real voltage")
        self.Vr.name1 = "Vr"
        self.Vi = RealT(self, units="volts", desc="Imaginary voltage")
        self.Vi.name1 = "Vi"
        self.isPort = BooleanT(
            self,
            v=self.isPort,
            desc="Determines if we are running to fixed Mach or Area",
        )
        parent.add_vid(self)
        self.other = 0
        self.type = "EP"

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
        return type == "EP"

    def set_iv(self, current, voltage):
        """Set current and voltage on this port and the linked port.

        Parameters
        ----------
        current : ComplexT or complex
            Current value to set.
        voltage : ComplexT or complex
            Voltage value to set.
        """
        self.I.set(current)
        self.V.set(voltage)
        self.other.I.set(current)
        self.other.V.set(voltage)
        self.Vr.set(self.V.v.real)
        self.Vi.set(self.V.v.imag)
        self.Ir.set(self.I.v.real)
        self.Ii.set(self.I.v.imag)
        self.other.Vr.set(self.V.v.real)
        self.other.Vi.set(self.V.v.imag)
        self.other.Ir.set(self.I.v.real)
        self.other.Ii.set(self.I.v.imag)

    def add_vid(self, v):
        """Add a variable ID to this port's variable list.

        Parameters
        ----------
        v : object
            The variable ID to add.
        """
        self.VIDL.append(v)

    def link_ep(self, ep):
        """Link this port to another electrical port.

        Parameters
        ----------
        ep : EP
            The other electrical port to link to.
        """
        self.other = ep
        ep.other = self

    def link_e(self, other):
        """Link this port to another port via the other's link_e method.

        Parameters
        ----------
        other : EP
            The other electrical port to link to.
        """
        other.link_e(self)

    def dump(self, output_file):
        """Write port state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(f"{self.parent.name1} {self.name1} {self.V.v} {self.I.v}\n")

    def hover(self):
        """Get a hover summary string for this port.

        Returns
        -------
        str
            Summary string with parent name, port name, voltage, and current.
        """
        return (
            self.parent.name1
            + " "
            + self.name1
            + " "
            + str(self.V.v)
            + " "
            + str(self.I.v)
        )

    def save_print(self):
        """Get the save print string for this port.

        Returns
        -------
        str
            Empty string (no save print for EP ports).
        """
        return ""

    def pretty(self, output_file):
        """Write a formatted table row of port state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(
            f"{self.parent.name1[:8]:12s}{self.name1[:8]:12s}"
            f"Vr:{str(self.Vr.v)[:8]:12s}Vi:{str(self.Vi.v)[:8]:12s}"
            f"Ir:{str(self.Ir.v)[:8]:12s}Ii:{str(self.Ii.v)[:8]:12s}\n"
        )
