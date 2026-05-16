from popclean import Element, RealT

from .fp import Fp


class Spring(Element):
    def __init__(self, name):
        super().__init__(name, "Capacitor")
        self.type = "Spring"

        self.desc = "Simple spring element"

        # Variables
        self.k = RealT(self, units="lbf/ft", desc="Spring constant")
        self.F = RealT(self, units="lbf/ft", desc="Spring constant")
        self.LN = RealT(self, units="ft", desc="Nuetral length of the spring")
        self.L = RealT(self, units="ft", desc="actual length of the spring")

        # electrical locations/ports
        self.Fp1 = Fp(self, "out", "Force port")
        self.Fp2 = Fp(self, "out", "Force Port")

        self.type = "Spring"

        self.initial_list()

    def calc(self):

        # calculate the length of the spring from the port
        self.L = self.Fp2.x - self.Fp1.x

        # determin the force
        self.F = -1.0 * self.k * (self.L - self.LN)
        self.Fp1.set_f(self.F)
        self.Fp2.set_f(self.F)

    def dump(self, output_file):
        output_file.write(f"{self.name1} Spring\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        output_file.write(
            f"{'Fp'[:10]:12s}{self.name1[:10]:12s}{('L:' + str(self.L))[:10]:12s}"
            f"{('F:' + str(self.F))[:10]:12s}{('k:' + str(self.k))[:10]:12s}\n"
        )
