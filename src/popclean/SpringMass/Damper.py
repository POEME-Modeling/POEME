from Element import Element
from RealT import RealT
from Fp import Fp
from Mass import Mass
import math
from Table2d import Table2d
import g


class Damper(Element):

    def __init__(d, name):
        super().__init__(name, "Damper")

        d.desc = "Simple spring element"

        # electrical locations/ports
        d.Fp1 = Fp(d, "out", "Force port")
        d.Fp2 = Fp(d, "out", "Force Port")

        # Variables
        d.c = RealT(d, units="lbf/(ftsec)", desc="Spring damping constant")
        d.F = RealT(d, units="lbf/ft", desc="Spring constant")
        d.V = RealT(d, units="ft/sec", desc="Net velocity of the spring")
        d.length = RealT(d, units="ft", desc="Actual length of the spring")

        d.initialList()

    def calc(d):

        # calculate the length of the spring from the port
        d.V += d.Fp2.V - d.Fp1.V

        # determin the force
        d.F += -1.0 * d.c * (d.V)
        d.Fp1.setF(d.F)
        d.Fp2.setF(d.F)

    def dump(d):
        print(d.name1, "Spring", file=g.out)
        super().realPrint()

    def pretty(d):
        print(
            f"{"Damper"[:10]:12s}{d.name1[:10]:12s}{("c:"+str(d.c))[:10]:12s}{("F:"+str(d.F))[:10]:12s}{("V:"+str(d.V))[:10]:12s}{("length:"+str(d.length))[:10]:12s}",
            file=g.pretty,
        )
