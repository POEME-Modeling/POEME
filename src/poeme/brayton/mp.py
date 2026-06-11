from poeme import Atom, RealT, BooleanT


class MP(Atom):
    def __init__(self, p, io, **kwargs):

        self.VIDL = list()
        self.name1 = ""
        self.parent = p
        self.__dict__.update(kwargs)
        self.N = RealT(self, units="RPM", desc="Rotational speed")
        self.N.name1 = "N"
        self.hp = RealT(self, units="hp", desc="Horse power passed through port")
        self.hp.name1 = "hp"
        self.I = RealT(self, units="lbm*ft**2", desc="Rotational Inertia")
        self.I.name1 = "I"
        self.other = 0
        self.io = io
        p.add_vid(self)
        self.isPort=True
        self.isPort = BooleanT(
            self, v=self.isPort, desc="Determines if we are running to fixed Mach or Area"
        )        
        self.type = "MP"

    def isa(self, type):
        return type == "MP"

    def add_vid(self, v):
        self.VIDL.append(v)

    def link_mp(self, mp):
        if self.other != 0:
            print( self.parent.name1 + "." + self.name1 + " is already linked " )
            quit()
        if mp.other != 0:
            print( mp.parent.name1 + "." + mp.name1 + " is already linked " )
            quit() 
        if ( mp.isa( "MP")==False):
            print( mp.parent.name1 + "." + mp.name1 + " is not a mechanical node " )
            quit()                
        self.other = mp
        mp.other = self

    def set_n(self, n):
        self.N.v = n
        if self.other != 0:
            self.other.N.v = n

    def set_hp(self, hp):
        self.hp.v = hp
        if self.other != 0:
            self.other.hp.v = hp

    def dump(self, output_file):
        output_file.write(
            f"{self.parent.name1[:8]:10} {self.name1[:8]:10}  "
            f"N:{str(self.N.v)[:8]:10s}  hp:{str(self.hp.v)[:8]:10s}  "
            f"I:{str(self.I.v)[:8]:10s}\n"
        )
        # print( self.parent.name1, self.name1, self.N.v, self.hp.v, self.I.v)

    def pretty(self, output_file):
        output_file.write(
            f"{self.parent.name1[:8]:10} {self.name1[:8]:10}  "
            f"N:{str(self.N.v)[:8]:10s}  hp:{str(self.hp.v)[:8]:10s}  "
            f"I:{str(self.I.v)[:8]:10s}\n"
        )

    def hover(self):
        return (
            self.parent.name1
            + "."
            + self.name1
            + "."
            + str(self.N.v)
            + " "
            + str(self.hp.v)
            + " "
            + str(self.I.v)
        )

    def save_print(self):
        temp = (
            self.parent.name1 + "." + self.name1 + ".N.set( " + str(self.N.v)
        ) + ")\n"
        temp = (
            temp
            + (self.parent.name1 + "." + self.name1 + ".hp.set( " + str(self.hp.v))
            + ")\n"
        )
        temp = (
            temp
            + (self.parent.name1 + "." + self.name1 + ".I.set( " + str(self.I.v))
            + ")\n"
        )
        return temp
