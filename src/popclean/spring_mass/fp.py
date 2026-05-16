from popclean import Atom, RealT


class Fp(Atom):
    def __init__(self, p, io, desc):

        # variables
        self.VIDL = list()
        self.name1 = ""
        self.desc = desc
        self.parent = p
        self.io = io

        # engineering variables
        self.F = RealT(self, units="lbf", desc="Force")
        self.x = RealT(self, units="ft", desc="x location")
        self.V = RealT(self, units="ft/sec", desc="velocity")

        p.add_vid(self)
        self.type = "Fp"
        self.other = 0

    def isa(self, type):
        return type == "Fp"

    # set the conditions in this port and connected port
    def set_xv(self, x, v):
        self.x.v = x.v
        if isinstance(v, float):
            self.V.v = v
        else:
            self.V.v = v.v
        self.other.x.v = self.x.v
        self.other.V.v = self.V.v

    # set the conditions in this port and connected port
    def set_f(self, f):
        self.F.v = f.v
        self.other.F.v = f.v

    def add_vid(self, v):
        self.VIDL.append(v)

    # link this port to another port
    def link_fp(self, fp):
        self.other = fp
        fp.other = self

    def dump(self, output_file):
        output_file.write(f"{self.parent.name1} {self.name1} {self.x} {self.V}\n")

    def hover(self):
        return (
            self.parent.name1 + " " + self.name1 + str(self.x.v) + " " + str(self.V.v)
        )

    def pretty(self, output_file):
        output_file.write(
            f"{'Fp'[:10]:12s}{self.name1[:10]:12s}{('F:' + str(self.F))[:10]:12s}"
            f"{('F:' + str(self.F))[:10]:12s}{('x:' + str(self.x))[:10]:12s}"
            f"{('V:' + str(self.V))[:10]:12s}\n"
        )
