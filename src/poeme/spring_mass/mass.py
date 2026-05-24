from poeme import (
    BooleanT,
    Element,
    Independent,
    ModelSession,
    RealT,
    State,
)


class Mass(Element):
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

    # first step in solver pass is to set the voltage in all of the ports
    def preset(self):
        for p in self.port_list:
            p.set_xv(self.xloc, self.V)

    # before anything is run at all, loop through all substructures to find the
    # ports
    def precheck(self):
        self.port_list = list()
        for p in self.VIDL:
            if p.isa("Fp"):
                self.port_list.append(p)

    def calc(self):

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
        output_file.write(f"{self.name} Node\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        output_file.write(
            f"{'Fp'[:10]:12s}{self.name1[:10]:12s}"
            f"{('xloc:' + str(self.xloc))[:10]:12s}{('V:' + str(self.V))[:10]:12s}"
            f"{('mass:' + str(self.mass))[:10]:12s}\n"
        )
