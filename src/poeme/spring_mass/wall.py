from poeme import Element, ModelSession, RealT


class Wall(Element):
    """Wall (fixed boundary) element for spring-mass systems.

    A fixed wall that provides a reaction point for spring-damper-mass
    connections. It has an x-location but does not move. Forces from
    connected ports are accumulated into positive and negative totals.

    Parameters
    ----------
    name : str
        Name of the wall element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    xloc : RealT
        X location of the wall (ft).
    Fp : RealT
        Total force in the positive direction (lbf).
    Fn : RealT
        Total force in the negative direction (lbf).
    port_list : list
        List of connected Fp force ports.
    """

    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Wall", session=session)
        self.name = name

        self.desc = (
            "This element is wall for the spring system.  It has \n "
            + "x location but does not move."
        )

        # force connections
        self.port_list = list()

        # Variables
        self.xloc = RealT(self, units="ft", desc="X location of the node")
        self.Fp = RealT(self, units="lbf", desc="Force in the positive direction")
        self.Fn = RealT(self, units="lbf", desc="Force in the negative direction")

        self.initial_list()

    def preset(self):
        """Fix all connected ports to zero velocity (wall is immovable).

        Iterates through all connected force ports and sets their
        position to this wall's x-location and velocity to 0.0.
        """
        for p in self.port_list:
            p.set_xv(self.xloc, 0.0)

    def precheck(self):
        """Collect all connected force ports before simulation begins.

        Iterates through all variable IDs and builds the port_list
        by filtering for Fp-type ports.
        """
        self.port_list = list()
        for p in self.VIDL:
            if p.isa("Fp"):
                self.port_list.append(p)

    def calc(self):
        """Calculate net reaction forces from connected ports.

        Sums forces from all connected ports into positive (Fp) and
        negative (Fn) totals based on port direction (in/out) and
        force sign.
        """

        # zero out the running current totals
        self.Fp.set(0.0)
        self.Fn.set(0.0)

        # loops through the ports
        # if current coming in, add it to in total
        # if current going out, add it to the out total
        for p in self.port_list:
            if p.F > 0.0:
                if p.io == "in":
                    self.Fp = self.Fp + p.F
                else:
                    self.Fn = self.Fp - p.F
            if p.F < 0.0:
                if p.io == "out":
                    self.Fp = self.Fp - p.F
                else:
                    self.Fn = self.Fp + p.F

    def dump(self, output_file):
        """Write wall state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(f"{self.name} Node\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Write a formatted table row of wall state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(
            f"{'Fp'[:10]:12s}{self.name1[:10]:12s}"
            f"{('xloc:' + str(self.xloc))[:10]:12s}\n"
        )
