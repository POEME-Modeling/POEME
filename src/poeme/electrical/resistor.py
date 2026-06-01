from poeme import ComplexT, Element, ModelSession, RealT, Table1d

from .ep import EP


class Resistor(Element):
    """Resistor element for electrical systems.

    A linear resistor that relates voltage and current via Ohm's law.
    The resistor has two electrical ports (EPi and EPo) and computes its
    voltage drop, impedance, and current based on the port conditions.
    Supports optional resistance lookup tables for temperature-dependent
    resistance values.

    Parameters
    ----------
    name : str
        Name of the resistor element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    R : RealT
        Resistance (ohms).
    dV : ComplexT
        Voltage drop across the resistor (volts).
    I : ComplexT
        Current through the resistor (amps).
    Z : ComplexT
        Impedance of the resistor (ohms).
    RV : Table1d
        Resistance as a function of temperature lookup table.
    EPi : EP
        Inlet electrical port.
    EPo : EP
        Exit electrical port.
    """

    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Resistor", session=session)
        self.type = "Resistor"
        self.desc = "Simple reistor element"

        # electrical location/ports
        self.EPi = EP(self, io="in", desc="Inlet ElectricPort")
        self.EPo = EP(self, io="out", desc="Exit Electric Port")

        # tables
        self.RV = Table1d(
            self, units="ohms", desc="Resistance as a function of temeperature"
        )

        # variables
        self.dV = ComplexT(self, units="volts", desc="Voltage drop")
        self.I = ComplexT(self, units="amps", desc="Current")
        self.R = RealT(self, units="ohms", desc="Resistance")
        self.Z = ComplexT(self, units="ohms", desc="Impedance")
        self.initial_list()

    def calc(self):
        """Calculate resistor impedance and current.

        Computes the voltage drop from port voltages, reads resistance
        from a lookup table if available, then sets impedance to the
        resistance value. Current is computed via Ohm's law:
        I = dV / R. Sets the current on both ports.
        """

        # determine the voltage drop
        self.dV = self.EPi.V - self.EPo.V

        # if the table is there, determine resistane from it
        if self.RV.full():
            self.R = self.RV.calc(self.dV.real())

        # calculate impedence
        self.Z.set_p(self.R, 0.0)

        # calculate the current
        self.I = self.dV / self.Z

        # set the ports
        # voltage does not chage
        self.EPi.set_iv(-1.0 * self.I, self.EPi.V)
        self.EPo.set_iv(self.I, self.EPo.V)

    def dump(self, output_file):
        """Write resistor state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(f"{self.name1} Resistor\n")
        super().real_print(output_file)

    def hover(self):
        """Get a hover summary string for this resistor.

        Returns
        -------
        str
            Summary string with resistor name and parent hover info.
        """
        temp1 = self.name1 + " Resistor\n" + super().hover()
        return temp1

    def pretty(self, output_file):
        """Write a formatted table row of resistor state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(
            f"{'Resistor'[:10]:12s}"
            f"{self.name1[:10]:12s}"
            f"{('self:' + str(self.R))[:10]:12s}"
            f"{('dVr:' + str(self.EPi.Vr - self.EPo.Vr))[:10]:12s}"
            f"{('dVi:' + str(self.EPi.Vi - self.EPo.Vi))[:10]:12s}"
            f"{('Ir:' + str(self.EPi.Ir))[:10]:12s}"
            f"{('Ii:' + str(self.EPi.Ii))[:10]:12s}\n"
        )
