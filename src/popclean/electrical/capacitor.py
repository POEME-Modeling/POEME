import math

from popclean import ComplexT, Element, RealT, Table2d, g

from .ep import EP


class Capacitor(Element):
    def __init__(self, name):
        super().__init__(name, "Capacitor")
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

    def dump(self):
        print(self.name1, "Capacitor", file=g.out)
        super().real_print()

    def pretty(self):
        print(
            f"{'Capacitor'[:10]:12s}{self.name1[:10]:12s}"
            f"{('self:' + str(self.C))[:10]:12s}"
            f"{('dVr:' + str(self.EPi.Vr - self.EPo.Vr))[:10]:12s}"
            f"{('dVi:' + str(self.EPi.Vi - self.EPo.Vi))[:10]:12s}"
            f"{('Ir:' + str(self.EPi.Ir))[:10]:12s}"
            f"{('Ii:' + str(self.EPi.Ii))[:10]:12s}",
            file=g.pretty,
        )
