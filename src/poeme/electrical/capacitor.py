import math

from poeme import ComplexT, Element, ModelSession, RealT, Table2d

from .ep import EP


class Capacitor(Element):
    """Capacitor element for electrical systems.

    A linear capacitor that relates voltage and current via capacitive reactance.
    The capacitor has two electrical ports (input EPi and output EPo) and computes its
    voltage drop, impedance, and current based on the port conditions.

    Parameters
    ----------
    name : str
        Name of the capacitor element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    C : RealT
        Capacitance (farad).
    dV : ComplexT
        Voltage drop across the capacitor (volts).
    I : ComplexT
        Current through the capacitor (amps).
    Z : ComplexT
        Impedance of the capacitor (ohms).
    CVc : Table2d
        Capacitance versus voltage lookup table.
    EPi : EP
        Inlet electrical port.
    EPo : EP
        Exit electrical port.
    """

    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Capacitor", session=session)
        self.type = "Capacitor"

        self.desc = "Simple capacitor element"

        # tables
        self.CVc = Table2d(self, units="farad", desc="Capacitance versus dV")

        # electrical locations/ports
        self.EPi = EP(self, io="in", desc="Inlet Electric Port")
        self.EPo = EP(self, io="out", desc="Exit Electric Port")

        # Variables
        self.C = RealT(self, units="farad", desc="Capacitance")
        self.dV = ComplexT(self, units="volts", desc="Voltage")
        self.I = ComplexT(self, units="amps", desc="Current")
        self.Z = ComplexT(self, units="ohms", desc="Impedance")

        self.type = "Capacitor"
        self.initial_list()

    def calc(self):
        """Calculate capacitor impedance and current.

        Computes the voltage drop from port voltages, reads capacitance
        from a lookup table if available, then applies capacitive reactance:
        Z = -j / (2 * pi * f * C). Current is computed via Ohm's law:
        I = dV / Z. Sets the current on both ports.
        """

        # calculate pressure drop
        self.dV = self.EPi.V - self.EPo.V

        # if there is a table, read it to determine self
        if self.CVc.full():
            self.C.v = self.CVc.calc(self.dV.num.real, self.dV.num.imag)

        # calculate impendance
        self.Z.set_p(0.0, -1.0 / (self.C * 2.0 * math.pi * self.EPi.freq))

        # determine current
        self.I = self.dV / self.Z

        # set the current in the ports
        # voltage does not change
        self.EPi.set_iv(-1.0 * self.I, self.EPi.V)
        self.EPo.set_iv(self.I, self.EPo.V)

    def dump(self, output_file):
        """Write capacitor state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(f"{self.name1} Capacitor\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Write a formatted table row of capacitor state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(
            f"{'Capacitor'[:10]:12s}{self.name1[:10]:12s}"
            f"{('self:' + str(self.C))[:10]:12s}"
            f"{('dVr:' + str(self.EPi.Vr - self.EPo.Vr))[:10]:12s}"
            f"{('dVi:' + str(self.EPi.Vi - self.EPo.Vi))[:10]:12s}"
            f"{('Ir:' + str(self.EPi.Ir))[:10]:12s}"
            f"{('Ii:' + str(self.EPi.Ii))[:10]:12s}\n"
        )
