from poeme import Element, ModelSession, RealT

from .fp import Fp


class Damper(Element):
    """Simple damper element for spring-mass systems.

    A linear damper that relates force and velocity via viscous damping.
    The damper has two force ports (Fp1 and Fp2) and computes its
    net velocity and internal force based on the port velocities.

    Parameters
    ----------
    name : str
        Name of the damper element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    c : float
        Damping constant (lbf/(ft*sec)).
    F : float
        Damping force (lbf).
    V : float
        Net velocity of the damper (ft/sec).
    length : float
        Actual length of the damper (ft).
    Fp1 : Fp
        Force port 1 (output).
    Fp2 : Fp
        Force port 2 (output).
    """

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
        """Calculate damper velocity and force.

        Computes the net velocity from port velocities, then applies
        viscous damping: F = -c * V. Sets the force on both ports.
        """

        # calculate the length of the spring from the port
        self.V = self.Fp2.V - self.Fp1.V

        # determin the force
        self.F = -1.0 * self.c * (self.V)
        self.Fp1.set_f(self.F)
        self.Fp2.set_f(self.F)

    def dump(self, output_file):
        """Write damper state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(f"{self.name1} Spring\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Write a formatted table row of damper state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(
            f"{'Damper'[:10]:12s}{self.name1[:10]:12s}{('c:' + str(self.c))[:10]:12s}"
            f"{('F:' + str(self.F))[:10]:12s}{('V:' + str(self.V))[:10]:12s}"
            f"{('length:' + str(self.length))[:10]:12s}\n"
        )
