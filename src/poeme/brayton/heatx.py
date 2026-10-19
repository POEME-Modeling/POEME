from poeme import Element, ModelSession, RealT

from .fn import FN


class Heatx(Element):
    """Heat exchanger element.  Applies pressure loss to both streams as
    well as heat transfer based on input effectiveness.

    """

    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "Duct", session=session)
        self.type = "Heatx"

        self.desc = "The heat exchanger element calculates the energy transfer"
        "between to streams based on the input effectiveness.  It also applies"
        "a pressure drop to each stream based on a input normalized pressure drop."

        # Variables
        self.eff = RealT(self, v=0.0, units="none", desc="Heat exchange effectiveness")
        self.dPqP1 = RealT(
            self, v=0.0, units="none", desc="Stream 1 relative pressure drop"
        )
        self.dPqP2 = RealT(
            self, v=0.0, units="none", desc="Stream 2 relative pressure drop"
        )

        # Fluid locations
        self.FNi1 = FN(self, io="in", desc="Incoming flow")
        self.FNo1 = FN(self, io="out", desc="Outgoing flow")
        self.FNi2 = FN(self, io="in", desc="Incoming flow")
        self.FNo2 = FN(self, io="out", desc="Outgoing flow")

        self.initial_list()

    def calc(self):

        # pass the flow along
        self.FNo1.copy(self.FNi1)
        self.FNo2.copy(self.FNi2)

        # determine capacitance of each stream
        cap1 = self.FNi1.W * self.FNi1.Cpt
        cap2 = self.FNo2.W * self.FNo2.Cpt

        # Determine which side has the minimum and maximum capacity
        capMin = cap1 if cap2 >= cap1 else cap2

        # If T2 > T1 then stream 2 is the hot side
        if self.FNi2.Tt > self.FNi1.Tt:
            # Determine cold side temp (TO1) from effectiveness equation
            ToutCold = self.FNi1.Tt + self.eff * (self.FNi2.Tt - self.FNi1.Tt) * (
                capMin / cap1
            )

            # Set the cold side conditions based on the temp and pressure loss
            self.FNo1.setTotalTP(ToutCold, self.FNo1.Pt * (1.0 - self.dPqP1))

            # Set the hot side conditions based on an energy balance and
            # pressure loss
            self.FNo2.set_hP(
                self.FNi2.ht
                + (self.FNi1.ht - self.FNi2.ht) * self.FNi1.W / self.FNo2.W,
                self.FNi2.Pt * (1 - self.dPqP2),
            )

        else:
            # Determine cold side temp (TO2) from effectiveness equation
            ToutCold = self.FNi2.Tt + self.eff * (self.FNi1.Tt - self.FNi2.Tt) * (
                capMin / cap2
            )

            # Set the cold side conditions based on the temp and pressure loss
            self.FNo2.set_tp(ToutCold, self.FNo2.Pt * (1 - self.dPqP2))

            # Set the hot side conditions based on an energy balance and
            # pressure loss
            self.FNo1.set_hp(
                self.FNi1.ht
                + (self.FNi2.ht - self.FNo2.ht) * self.FNi2.W / self.FNi1.W,
                self.FNi1.Pt * (1 - self.dPqP1),
            )

    def precheck(self):
        """Check bleed flow fraction and deactivate port if negligible.

        If the bleed flow fraction is near zero, sets the bleed out
        port's ``isPort`` attribute to False so it is ignored by the solver.
        """

    def dump(self, output_file):
        """Dump duct state to an output file.

        Parameters
        ----------
        output_file : file-like
            File object to write the duct state to.
        """
        output_file.write(f"{self.name1} Duct\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Print a formatted summary of the duct state.

        Parameters
        ----------
        output_file : file-like
            File object to write the pretty-printed output to.
        """
        output_file.write(
            f"{'Heatx':12s}{self.name1[:10]:12s}{('dPqP1:' + str(self.dPqP1))[:10]:12s}"
            f"{('dPqP2:' + str(self.dPqP1))[:10]:12s}"
            f"{('eff:' + str(self.eff))[:10]:12s}\n"
        )
