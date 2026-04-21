from popclean import Atom, ComplexT, RealT, g


class EP(Atom):
    def __init__(self, parent, **kwargs):

        self.parent = parent
        self.name1 = ""
        # variables
        self.VIDL = list()
        self.__dict__.update(kwargs)

        # engineering variables
        self.freq = RealT(self, units="hz", desc="frequency")
        self.freq.name1 = "freq"
        self.I = ComplexT(self, units="amps", desc="Amperage")
        self.I.name1 = "I"
        self.Ii = RealT(self, units="amps", desc="Imaginary amperage")
        self.Ii.name1 = "Ii"
        self.Ir = RealT(self, units="amps", desc="Real amperage")
        self.Ir.name1 = "Ir"
        self.V = ComplexT(self, units="volts", desc="Voltage")
        self.V.name1 = "V"
        self.Vr = RealT(self, units="volts", desc="Real voltage")
        self.Vr.name1 = "Vr"
        self.Vi = RealT(self, units="volts", desc="Imaginary voltage")
        self.Vi.name1 = "Vi"

        parent.add_vid(self)
        self.type = "EP"

    def isa(self, type):
        return type == "EP"

    # set the conditions in this port and connected port
    def set_iv(self, current, voltage):
        self.I.set(current)
        self.V.set(voltage)
        self.other.I.set(current)
        self.other.V.set(voltage)
        self.Vr.set(self.V.v.real)
        self.Vi.set(self.V.v.imag)
        self.Ir.set(self.I.v.real)
        self.Ii.set(self.I.v.imag)
        self.other.Vr.set(self.V.v.real)
        self.other.Vi.set(self.V.v.imag)
        self.other.Ir.set(self.I.v.real)
        self.other.Ii.set(self.I.v.imag)

    def add_vid(self, v):
        self.VIDL.append(v)

    # link this port to another port
    def link_ep(self, ep):
        self.other = ep
        ep.other = self

    def link_e(self, other):
        other.link_e(self)

    def dump(self):
        print(self.parent.name1, self.name1, self.V.v, self.I.v, file=g.out)

    def hover(self):
        return (
            self.parent.name1
            + " "
            + self.name1
            + " "
            + str(self.V.v)
            + " "
            + str(self.I.v)
        )

    def save_print(self):
        return ""

    def pretty(self):
        print(
            f"{self.parent.name1[:8]:12s}{self.name1[:8]:12s}"
            f"Vr:{str(self.Vr.v)[:8]:12s}Vi:{str(self.Vi.v)[:8]:12s}"
            f"Ir:{str(self.Ir.v)[:8]:12s}Ii:{str(self.Ii.v)[:8]:12s}",
            file=g.pretty,
        )
