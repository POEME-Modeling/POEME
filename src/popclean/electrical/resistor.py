from popclean import ComplexT, Element, RealT, Table1d

from .ep import EP


class Resistor(Element):
    def __init__(self, name):
        super().__init__(name, "Resistor")
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
        output_file.write(f"{self.name1} Resistor\n")
        super().real_print(output_file)

    def hover(self):
        temp1 = self.name1 + " Resistor\n" + super().hover()
        return temp1

    def pretty(self, output_file):
        output_file.write(
            f"{'Resistor'[:10]:12s}"
            f"{self.name1[:10]:12s}"
            f"{('self:' + str(self.R))[:10]:12s}"
            f"{('dVr:' + str(self.EPi.Vr - self.EPo.Vr))[:10]:12s}"
            f"{('dVi:' + str(self.EPi.Vi - self.EPo.Vi))[:10]:12s}"
            f"{('Ir:' + str(self.EPi.Ir))[:10]:12s}"
            f"{('Ii:' + str(self.EPi.Ii))[:10]:12s}\n"
        )
