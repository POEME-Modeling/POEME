from popclean import Element, RealT, g

from .fp import Fp


class Damper(Element):
    def __init__(self, name):
        super().__init__(name, "Damper")

        self.desc = "Simple spring element"

        # electrical locations/ports
        self.Fp1 = Fp(self, "out", "Force port")
        self.Fp2 = Fp(self, "out", "Force Port")

        # Variables
        self.c = RealT(self, units="lbf/(ftsec)", desc="Spring damping constant")
        self.F = RealT(self, units="lbf/ft", desc="Spring constant")
        self.V = RealT(self, units="ft/sec", desc="Net velocity of the spring")
        self.length = RealT(self, units="ft", desc="Actual length of the spring")

        self.initialList()

    def calc(self):

        # calculate the length of the spring from the port
        self.V = self.Fp2.V - self.Fp1.V

        # determin the force
        self.F = -1.0 * self.c * (self.V)
        self.Fp1.set_f(self.F)
        self.Fp2.set_f(self.F)

    def dump(self):
        print(self.name1, "Spring", file=g.out)
        super().realPrint()

    def pretty(self):
        print(
            f"{'Damper'[:10]:12s}{self.name1[:10]:12s}{('c:' + str(self.c))[:10]:12s}"
            f"{('F:' + str(self.F))[:10]:12s}{('V:' + str(self.V))[:10]:12s}"
            f"{('length:' + str(self.length))[:10]:12s}",
            file=g.pretty,
        )
