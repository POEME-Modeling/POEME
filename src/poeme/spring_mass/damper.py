from poeme import Element, ModelSession, RealT

from .fp import Fp


class Damper(Element):
    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Damper", session=session)

        self.desc = "Simple spring element"

        # electrical locations/ports
        self.Fp1 = Fp(self, "out", "Force port")
        self.Fp2 = Fp(self, "out", "Force Port")

        # Variables
        self.c = RealT(self, units="lbf/(ftsec)", desc="Spring damping constant")
        self.F = RealT(self, units="lbf/ft", desc="Spring constant")
        self.V = RealT(self, units="ft/sec", desc="Net velocity of the spring")
        self.length = RealT(self, units="ft", desc="Actual length of the spring")

        self.initial_list()

    def calc(self):

        # calculate the length of the spring from the port
        self.V = self.Fp2.V - self.Fp1.V

        # determin the force
        self.F = -1.0 * self.c * (self.V)
        self.Fp1.set_f(self.F)
        self.Fp2.set_f(self.F)

    def dump(self, output_file):
        output_file.write(f"{self.name1} Spring\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        output_file.write(
            f"{'Damper'[:10]:12s}{self.name1[:10]:12s}{('c:' + str(self.c))[:10]:12s}"
            f"{('F:' + str(self.F))[:10]:12s}{('V:' + str(self.V))[:10]:12s}"
            f"{('length:' + str(self.length))[:10]:12s}\n"
        )
