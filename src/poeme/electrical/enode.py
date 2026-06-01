from poeme import (
    ComplexT,
    Dependent,
    Element,
    Independent,
    ModelSession,
    RealT,
)

from .ep import EP


class Enode(Element):
    """Electrical node for circuit analysis.

    An electrical node (Enode) that accumulates currents from connected
    electrical ports and balances real and imaginary current components.
    Supports both independent variable perturbations and dependent
    current-balance equations for Newton-based solving.

    Parameters
    ----------
    name : str
        Name of the electrical node.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    V : ComplexT
        Voltage at the node (volts).
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
        Net current at the node (amps).
    ind_1 : Independent
        Independent variable for real voltage perturbation.
    ind_2 : Independent
        Independent variable for imaginary voltage perturbation.
    dep_1 : Dependent
        Dependent equation for real current balance.
    dep_2 : Dependent
        Dependent equation for imaginary current balance.
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

        # solver stuff
        self.ind_1 = Independent(
            self,
            indname="Vr",
            perturb=0.05,
            scale=100,
            perturb_type="Relative",
            active=True,
            desc="Varies real component of Voltage",
        )
        self.ind_2 = Independent(
            self,
            indname="Vi",
            perturb=0.05,
            scale=100,
            perturb_type="Relative",
            active=True,
            desc="Varies imaginary component of Voltage",
        )
        self.dep_1 = Dependent(
            self,
            d1name="IinR",
            d2name="IoutR",
            val_scale=1.0,
            active=True,
            desc="Balances real component of current",
        )
        self.dep_2 = Dependent(
            self,
            d1name="IinI",
            d2name="IoutI",
            val_scale=1.0,
            active=True,
            desc="Balances imaginary component of current",
        )

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

    # def LinkPort( self, port ):
    # self.port_list.append( port )

    def preset(self):
        """Set voltage on all connected ports before solver pass.

        Iterates through all connected electrical ports and sets their
        voltage to match this node's current complex voltage state.
        """
        for port in self.port_list:
            self.V.v = complex(self.Vr.v, self.Vi.v)
            port.set_iv(port.I.v, self.V.v)

    def precheck(self):
        """Collect all connected electrical ports before simulation begins.

        Iterates through all variable IDs and builds the port_list
        by filtering for EP-type ports.
        """
        self.port_list = list()
        for v in self.VIDL:
            if v.isa("EP"):
                self.port_list.append(v)

    def link_e(self, ep):
        """Link this node to an electrical port.

        Parameters
        ----------
        ep : EP
            The electrical port to link to this node.
        """
        temp = EP(self, io="in")
        temp.other = ep
        ep.other = temp
        if ep.io == "in":
            temp.io = "out"
        else:
            temp.io = "in"
        temp.name1 = ep.parent.name1 + "_" + ep.name1

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
        """Write node state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(f"{self.name} Node\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Write a formatted table row of node state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(
            f"{'Node'[:10]:12s}{self.name1[:10]:12s}"
            f"{('Vr:' + str(self.Vr))[:10]:12s}"
            f"{('Vi:' + str(self.Vi))[:10]:12s}\n"
        )
