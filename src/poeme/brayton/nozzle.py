# import g
from poeme import (
    BooleanT,
    Dependent,
    Element,
    ModelSession,
    RealT,
    StringVarT,
)

from .fn import FN


class Nozzle(Element):
    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Duct", session=session)
        self.type = "Nozzle"

        # variables
        self.Cfg = RealT(self, v=1.0, units="non", desc="Coefficient of gross thrust")
        self.desc = "Very basic nozzle.  Just expands flow to giving PsExh"
        self.PsExh = StringVarT(self, desc="Exhaust pressure")
        self.Anoz = RealT(self, units="in2", desc="Throat area")
        self.Fg = RealT(self, units="blf", desc="Gross thrust")

        # flow connections
        self.FNi = FN(self, io="in", desc="Incoming flow")
        self.FNo = FN(self, io="out", desc="Outgoing flow",isPort=False)

        # dependents
        self.dep_NA = Dependent(
            self, d1name="Anoz", d2name="FNo.A", active=False, desc="Nozzle area error"
        )
        self.size = BooleanT(
            self, v=True, desc="determines if nozzle is in sizing mode or not"
        )

        self.initial_list()

    def precheck(self):

        # if we are in sizing mode there is no dependent
        if self.size.v == True:
            self.dep_NA.active = False
        # if we are not is sizinig mode than there is a dependent
        else:
            self.dep_NA.active = True

    def calc(self):
        
        if self.FNo.Pt < self.PsExh.get():
            self.session.errors += "\n" + self.name1 + "nozzle pressure ratio < 1"
        # copy the inlet flow to the exit
        self.FNo.copy(self.FNi)

        # set the exit conditions to Mach 1.
        self.FNo.size = True
        self.FNo.MN = 1.0
        self.FNo.set_tp(self.FNo.Tt, self.FNo.Pt)
        if self.FNo.Ps > self.PsExh.get():
            # if we are in sizing mode then set the area
            if self.size == True:
                self.Anoz = self.FNo.A
        else:
            self.FNo.Ps = self.PsExh.get()
            self.FNo.ps_calc()
            if self.size == True:
                self.Anoz = self.FNo.A

        # calculate gross thrust
        self.Fg = self.Cfg * (
            self.FNo.W * self.FNo.V / 32.17
            + self.FNo.A * 144.0 * (self.FNo.Ps - self.PsExh.get())
        )

    def dump(self, output_file):
        output_file.write(f"{self.name1} Nozzle\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        output_file.write(
            f"{'Nozzle'[:10]:12s}{self.name1[:10]:12s}"
            f"{('Fg:' + str(self.Fg))[:10]:12s}\n"
        )
