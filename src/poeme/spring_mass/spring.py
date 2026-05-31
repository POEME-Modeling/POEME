from poeme import Element, ModelSession, RealT

from .fp import Fp


class Spring(Element):
    """Simple spring element for spring-mass systems.

    A linear spring that relates force and displacement via Hooke's law.
    The spring has two force ports (Fp1 and Fp2) and computes its
    current length and internal force based on the port positions.

    Parameters
    ----------
    name : str
        Name of the spring element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    k : float
        Spring constant (lbf/ft).
    F : float
        Spring force (lbf/ft).
    LN : float
        Neutral length of the spring (ft).
    L : float
        Actual length of the spring (ft).
    Fp1 : Fp
        Force port 1 (output).
    Fp2 : Fp
        Force port 2 (output).
    """

    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Capacitor", session=session)
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
        """Calculate spring length and force.

        Computes the current length from port positions, then applies
        Hooke's law: F = -k * (L - LN). Sets the force on both ports.
        """

        # calculate the length of the spring from the port
        self.L = self.Fp2.x - self.Fp1.x

        # determin the force
        self.F = -1.0 * self.k * (self.L - self.LN)
        self.Fp1.set_f(self.F)
        self.Fp2.set_f(self.F)

    def dump(self, output_file):
        """Write spring state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(f"{self.name1} Spring\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Write a formatted table row of spring state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(
            f"{'Fp'[:10]:12s}{self.name1[:10]:12s}{('L:' + str(self.L))[:10]:12s}"
            f"{('F:' + str(self.F))[:10]:12s}{('k:' + str(self.k))[:10]:12s}\n"
        )
