from poeme import (
    BooleanT,
    Element,
    Independent,
    ModelSession,
    RealT,
    State,
)


class Shaft(Element):
    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Shaft", session=session)
        self.type = "Shaft"
        
        #desciption
        self.desc  = "Shaft - this element determines the net power balance on a spool.\n"
        self.desc += "It is has mechanical ports on it that are designed to connect to\n"
        self.desc += "compressors in turbines.  In sizing mode, this element has a solver\n"
        self.desc += "state that will provide an error to the solver that is net power on\n"
        self.desc += "the shaft. If non sizing mode, in a solver independent is added that\n"
        self.desc += "varies the speed of the shaft.  In transient mode the shaft will use\n"
        self.desc += "the power inbalance on the shaft to determine the derivative of the\n"
        self.desc += "the shaft that will be integrated by the solver.  The inertia is\n"
        self.desc += "determined from all of the elements attached to the shaft\n\n"
        

        # dynamic mechanical port list
        self.port_list = list()

        # solver stuff
        self.ind_1 = Independent(
            self,
            indname="N",
            perturb=0.05,
            perturb_type="Relative",
            active=False,
            desc="Vary shaft speed",
        )
        self.state_1 = State(
            self,
            d1name="HPpos",
            d2name="HPneg",
            sname="N",
            dsname="dNdt",
            active=True,
            desc="Shaft speed power error/state",
        )

        # variables
        self.dNdt = RealT(self, units="RPM/sec", desc="Speed derivative")
        self.eff = RealT(self, v=1.0, units="none", desc="Shaft eff applied to incoming power")
        self.effLoss = RealT(self, units="HP", desc="Shaft eff total loss")
        self.HPneg = RealT(self, units="HP", desc="Total negative power on the shaft")
        self.HPpos = RealT(self, units="HP", desc="Total positive power on the shaft")
        self.HPX = RealT(self, units="HP", desc="Power extraction")
        self.I = RealT(self, units="lbm*ft**2", desc="inertia of the shaft itself ")
        self.Ispool = RealT(self, units="lbm*ft**2", desc="total spool intertia")
        self.N = RealT(self, units="RPM", desc="Shaft speed")

        self.size = BooleanT(self, v=True, desc="determines if the mode is sizing mode")
        self.initial_list()

    def preset(self):

        # before each solver pass set the speed in all connected elements
        for p in self.port_list:
            p.set_n(self.N.v)

    def precheck(self):
        # determine the current port list
        self.port_list = list()
        for v in self.VIDL:
            if v.isa("MP"):
                self.port_list.append(v)

        # if in sizing mode than speed is not an independent
        if self.size.v == True:
            self.ind_1.active = False
            self.state_1.active = True

        # if not in sizing mode than we need to vary speed
        else:
            self.ind_1.active = True
            self.state_1.active = True

    def calc(self):

        # loop through the ports and determine the horsepower and inertia
        self.HPpos = 0.0
        self.HPneg = 0.0
        self.Ispool = self.I

        for p in self.port_list:
            self.Ispool = self.Ispool + p.I
            if p.hp < 0.0:
                self.HPpos = self.HPpos + p.hp
            else:
                self.HPneg = self.HPneg - p.hp

        if self.HPX > 0.0:
            self.HPneg = self.HPneg + self.HPX
        else:
            self.HPpos = self.HPpos - self.HPX

        # determine the speed derivative
        self.HPneg = self.HPneg*self.eff
        self.effLoss = self.HPneg*(1. - self.eff )      
        self.dNdt = (self.HPpos - self.HPneg) / (self.N / 5252.0) / self.Ispool

    def dump(self, output_file):
        output_file.write(f"{self.name1} Shaft\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        output_file.write(
            f"{'Shaft'[:10]:12s}{self.name1[:10]:12s}{('N:' + str(self.N))[:10]:12s}"
            f"{('HPX:' + str(self.HPX))[:10]:12s}\n"
        )
