from popclean import Element, RealT, g


class Wall(Element):
    def __init__(self, name):
        super().__init__(name, "Wall")
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

    # first step in solver pass is to set the voltage in all of the ports
    def preset(self):
        for p in self.port_list:
            p.set_xv(self.xloc, 0.0)

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

    def dump(self):
        print(self.name, "Node", file=g.out)
        super().real_print()

    def pretty(self):
        print(
            f"{'Fp'[:10]:12s}{self.name1[:10]:12s}"
            f"{('xloc:' + str(self.xloc))[:10]:12s}",
            file=g.pretty,
        )
