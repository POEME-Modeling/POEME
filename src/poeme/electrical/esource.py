from poeme import ComplexT, Element, ModelSession, RealT

from .ep import EP


class Esource(Element):
    """Electrical voltage source for circuit analysis.

    An electrical voltage source that provides a fixed complex voltage
    and accumulates currents from connected electrical ports. Supports
    both real and imaginary current components for AC steady-state analysis.

    Parameters
    ----------
    name : str
        Name of the voltage source element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    V : ComplexT
        Voltage of the source (volts).
    Vi : RealT
        Imaginary component of voltage (volts).
    Vr : RealT
        Real component of voltage (volts).
    IinI : RealT
        Imaginary component of incoming current (amps).
    IinR : RealT
        Real component of incoming current (amps).
    IoutI : RealT
        Imaginary component of outgoing current (amps).
    IoutR : RealT
        Real component of outgoing current (amps).
    Inet : ComplexT
        Net current at the source (amps).
    port_list : list
        List of connected EP electrical ports.
    """

    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Enode", session=session)
        self.name = name

        self.desc = (
            "This element is an electrical node location.  It has a voltage "
            + " that is represented by a complex number.  Any number of impedance "
            + " elements can be hooked into this element.  It will determine the net"
            + " current it is seeing based on the system conditions. "
        )

        # eletrical connections
        self.port_list = list()

        # Variables
        self.V = ComplexT(self, units="volts", desc="Voltage")
        self.Vi = RealT(self, units="volts", desc="Imaginary component of voltage")
        self.Vr = RealT(self, units="volts", desc="Real component of voltage")
        self.IinI = RealT(self, units="amps", desc="Imaginery component of I coming in")
        self.IinR = RealT(self, units="amps", desc="Real component of I comping in")
        self.IoutI = RealT(
            self, units="amps", desc="Imaginary component of I going out"
        )
        self.IoutR = RealT(self, units="amps", desc="Real component I going out")
        self.Inet = ComplexT(self, units="amps", desc="Current")
        self.initial_list()

    def preset(self):
        """Set voltage on all connected ports before solver pass.

        Iterates through all connected electrical ports and sets their
        voltage to match this source's current complex voltage state.
        """
        for port in self.port_list:
            self.V.v = complex(self.Vr.v, self.Vi.v)
            port.set_iv(port.I.v, self.V.v)

    def link_e(self, ep):
        """Link this source to an electrical port.

        Parameters
        ----------
        ep : EP
            The electrical port to link to this source.
        """
        temp = EP(self, io="in")
        temp.other = ep
        ep.other = temp
        if ep.io == "in":
            temp.io = "out"
        else:
            temp.io = "in"
        temp.name1 = ep.parent.name1 + "_" + ep.name1

    def precheck(self):
        """Collect all connected electrical ports before simulation begins.

        Iterates through all variable IDs and builds the port_list
        by filtering for EP-type ports.
        """
        self.port_list = list()
        for v in self.VIDL:
            if v.isa("EP"):
                self.port_list.append(v)

    def calc(self):
        """Calculate net currents from connected ports.

        Sums currents from all connected ports into positive (Iin) and
        negative (Iout) totals based on port direction (in/out) and
        current sign for both real and imaginary components.
        """

        # zero out the running current totals
        self.IinR = 0.0
        self.IoutR = 0.0
        self.IinI = 0.0
        self.IoutI = 0.0

        # loops through the ports
        # if current coming in, add it to in total
        # if current going out, add it to the out total
        for port in self.port_list:
            if port.I.v.real > 0:
                self.IinR = self.IinR + port.I.v.real
            else:
                self.IoutR = self.IoutR - port.I.v.real
            if port.I.v.imag > 0:
                self.IinI = self.IinI + port.I.v.imag
            else:
                self.IoutI = self.IoutI - port.I.v.imag

    def dump(self, output_file):
        """Write source state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(f"{self.name} Node\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Write a formatted table row of source state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(
            f"{'Source'[:8]:12s}{self.name1[:8]:12s}"
            f"{'Vr:' + str(self.Vr.v)[:8]:12s}"
            f"{'Vi:' + str(self.Vi.v)[:8]:12s}\n"
        )
