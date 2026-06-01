import math

from poeme import ComplexT, Element, ModelSession, RealT

from .ep import EP


class Inductor(Element):
    """Inductor element for electrical systems.

    A linear inductor that relates voltage and current via inductive reactance.
    The inductor has two electrical ports (EPi and EPo) and computes its
    voltage drop, impedance, and current based on the port conditions.

    Parameters
    ----------
    name : str
        Name of the inductor element.
    inductance : float
        Inductance value (henries).
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    L : RealT
        Inductance (henries).
    dV : ComplexT
        Voltage drop across the inductor (volts).
    I : ComplexT
        Current through the inductor (amps).
    Z : ComplexT
        Impedance of the inductor (ohms).
    EPi : EP
        Inlet electrical port.
    EPo : EP
        Exit electrical port.
    """

    def __init__(self, name, inductance=0, session: ModelSession | None = None):
        # TODO: inductance not used
        super().__init__(name, "Inductor", session=session)
        self.type = "Inductor"
        self.desc = "Simple inductor element"

        # electrical locations/ports
        self.EPi = EP(self, io="in", desc="Inlet Electric Port")
        self.EPo = EP(self, io="out", desc="Exit Electric Port")

        # variables
        self.dV = ComplexT(self, units="volts", desc="Voltage drop")
        self.I = ComplexT(self, units="amps", desc="Current")
        self.L = RealT(self, units="henries", desc="Inductance")
        self.Z = ComplexT(self, units="ohms", desc="Impedance")
        self.initial_list()

    def calc(self):
        """Calculate inductor impedance and current.

        Computes the voltage drop from port voltages, then applies
        inductive reactance: Z = j * 2 * pi * f * L. Current is
        computed via Ohm's law: I = dV / Z. Sets the current on
        both ports.
        """

        # determine the voltage drop
        self.dV = self.EPi.V - self.EPo.V

        # deterine the impedance
        self.Z.set_p(0.0, 2 * math.pi * self.EPi.freq * self.L)

        # calculate the current
        self.I = self.dV / self.Z

        # set the ports
        # voltage does not chage
        self.EPi.set_iv(-1.0 * self.I, self.EPi.V)
        self.EPo.set_iv(self.I, self.EPo.V)

    def dump(self, output_file):
        """Write inductor state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(f"{self.name1} Inductor\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Write a formatted table row of inductor state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(
            f"{'Inductor'[:10]:12s}{self.name1[:10]:12s}"
            f"{('L:' + str(self.L))[:10]:12s}"
            f"{('dVr:' + str(self.EPi.Vr - self.EPo.Vr))[:10]:12s}"
            f"{('dVi:' + str(self.EPi.Vi - self.EPo.Vi))[:10]:12s}"
            f"{('Ir:' + str(self.EPi.Ir))[:10]:12s}"
            f"{('Ii:' + str(self.EPi.Ii))[:10]:12s}\n"
        )
