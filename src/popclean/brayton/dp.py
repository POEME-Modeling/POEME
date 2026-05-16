from popclean import Atom, RealT


class DP(Atom):
    def __init__(self, p, name, io, desc):

        self.VIDL = list()
        self.name = name
        self.desc = desc
        self.parent = p
        self.io = io
        self.D = RealT(self, 0.0, "D", "", "Data Value")
        p.add_vid(self)
        self.type = "DP"

    def isa(self, type):
        return type == "DP"

    def set(self, v):
        self.D.v = v
        self.other.D.v = v

    def add_vid(self, v):
        self.VIDL.append(v)

    def link_dp(self, dp):
        self.other = dp
        dp.other = self

    def dump(self, output_file):
        output_file.write(f"{self.parent.name} {self.name} {self.D.v}\n")
