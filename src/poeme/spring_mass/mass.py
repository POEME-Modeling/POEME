from poeme import (
    BooleanT,
    Element,
    Independent,
    ModelSession,
    RealT,
    State,
)


class Mass(Element):
    """Mass element for spring-mass systems.

    A nodal mass element that accumulates forces from connected force ports
    and computes acceleration via Newton's second law. Supports both static
    and dynamic (stateful) analysis through independent variables and states.

    Parameters
    ----------
    name : str
        Name of the mass element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    xloc : RealT
        X location of the mass (ft).
    Fp : RealT
        Total force in the positive direction (lbf).
    Fn : RealT
        Total force in the negative direction (lbf).
    mass : RealT
        Mass of the element (lbm).
    V : RealT
        Velocity of the mass (ft/sec).
    dVdt : RealT
        Derivative of the velocity (ft/sec^2).
    dxdt : RealT
        Derivative of the x-position (ft/sec).
    vert : BooleanT
        Whether gravity is acting on the mass.
    ind_x : Independent
        Independent variable for x location perturbation.
    ind_V : Independent
        Independent variable for velocity perturbation.
    state_1 : State
        State for x integration (position -> velocity).
    state_2 : State
        State for V integration (velocity -> acceleration).
    port_list : list
        List of connected Fp force ports.
    """

    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Mass", session=session)
        self.name = name

        self.desc = "This element is nodal x location for a mass spring system."

        # force connections
        self.port_list = list()

        # solver stuff
        self.ind_x = Independent(
            self,
            indname="xloc",
            perturb=0.05,
            scale=1.0,
            perturb_type="Absolute",
            active=True,
            desc="Varies the x location of the mass",
        )
        self.ind_V = Independent(
            self,
            indname="V",
            perturb=0.05,
            scale=100.0,
            perturb_type="Absolute",
            active=True,
            desc="Varies the x location of the mass",
        )

        self.state_1 = State(
            self,
            d1name="Fp",
            d2name="Fn",
            sname="xloc",
            dsname="V",
            val_scale=100.0,
            active=True,
            desc="X integration",
        )
        self.state_2 = State(
            self,
            d1name="V",
            d2name="0.",
            sname="V",
            dsname="dVdt",
            val_scale=100.0,
            active=True,
            desc="V integration",
        )

        # Variables
        self.xloc = RealT(self, units="ft", desc="X location of the node")
        self.Fp = RealT(self, units="lbf", desc="Force in the positive direction")
        self.Fn = RealT(self, units="lbf", desc="Force in the negative direction")
        self.mass = RealT(self, units="lbm", desc="Mass")
        self.V = RealT(self, units="ft/sec", desc="Velocity of the mass")
        self.dVdt = RealT(self, units="ft/secw", desc="Derivative of the velocity")
        self.dxdt = RealT(self, units="ft/sec", desc="Derivative of the x-position")
        self.vert = BooleanT(
            self, v=True, desc="deterimes in gravity is acting on spring"
        )

        self.initial_list()

    def preset(self):
        """Set position and velocity on all connected ports before solver pass.

        Iterates through all connected force ports and sets their position
        and velocity to match this mass's current state.
        """
        for p in self.port_list:
            p.set_xv(self.xloc, self.V)

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
        """Calculate net forces and acceleration.

        Sums forces from all connected ports into positive (Fp) and
        negative (Fn) totals, applies gravity if vertical mode is enabled,
        then computes acceleration via Newton's second law:
        dVdt = (Fp - Fn) / mass * 32.2.
        """

        # zero out the running current totals
        self.Fp.set(0.0)
        if self.vert == True:
            self.Fp.set(self.mass)
        self.Fn.set(0.0)

        # loops through the ports
        # if current coming in, add it to in total
        # if current going out, add it to the out total
        for p in self.port_list:
            if p.io == "in":
                if p.F > 0.0:
                    self.Fp = self.Fp + p.F
                else:
                    self.Fn = self.Fn - p.F
            elif p.F > 0.0:
                self.Fn = self.Fn + p.F
            else:
                self.Fp = self.Fp - p.F

        # calculate the derivative
        self.dVdt = (self.Fp - self.Fn) / (self.mass) * 32.2

    def dump(self, output_file):
        """Write mass state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(f"{self.name} Node\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Write a formatted table row of mass state to a text output file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write(
            f"{'Fp'[:10]:12s}{self.name1[:10]:12s}"
            f"{('xloc:' + str(self.xloc))[:10]:12s}{('V:' + str(self.V))[:10]:12s}"
            f"{('mass:' + str(self.mass))[:10]:12s}\n"
        )
