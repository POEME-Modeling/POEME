from poeme import Element, ModelSession, RealT, StringVarT


class PIV(Element):
    """PIV controller element for Brayton cycle transient control.

    A PIV (Proportional-Integral-Derivative) controller that senses a value
    from the system (represented by DPi) and adjusts the controlled value in
    the system (represented by DPo). This element is meant to run in transient
    mode only.

    Parameters
    ----------
    name : str
        Name of the PIV controller element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    P : RealT
        P - scalar applied to current error.
    I : RealT
        I - scalar applied to current integral of the error.
    D : RealT
        D - scalar applied to the derivative of the term.
    G : RealT
        G - desired value of the controlled value.
    elast : RealT
        Error term from last time step.
    e : RealT
        Current error term.
    Inte : RealT
        Integral of error.
    DPi : StringVarT
        Sensed value (setpoint input).
    DPo : StringVarT
        Set value (controller output).
    timeLast : RealT
        Last time this controller ran.
    """

    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "PIV", session=session)
        self.type = "PIV"

        self.desc = "PIV - This element is a PIV controller. It senses a value from "
        "the system, which is represented by the string value DPi, and adjustes the "
        "contolled value in the system, represented by the string value DPo. This "
        "element is meant to run is a transient mode only. It does this by checking "
        "the model to find all the inlets, nozzles and burners in the model. From "
        "these elements it will calculcale the overall values of total gross thrust, "
        "ram drag, net thrust, SFC and fuel flow."

        # variables
        self.P = RealT(self, units="none", desc="P - scalar applied to current error")
        self.I = RealT(
            self,
            units="none",
            desc="I - scalar applied to curreny integral of the error",
        )
        self.D = RealT(
            self, units="none", desc="D - scalare applied to the derivative of the term"
        )
        self.G = RealT(
            self, units="none", desc="G - desired value of the controlled value"
        )
        self.elast = RealT(self, units="none", desc="Error term from last time step")
        self.e = RealT(self, units="none", desc="Error term")
        self.Inte = RealT(self, units="none", desc="Inte")
        self.DPi = StringVarT(self, desc="Sensed value")
        self.DPo = StringVarT(self, desc="Set value")
        self.timeLast = RealT(self, units="time", desc="Last time this g ran")
        self.type = "PIV"

    def calc(self):
        """Calculate PIV controller output if time has advanced.

        If the solver time has advanced since the last call, computes the
        error between the desired value (G) and sensed value (DPi), then
        updates the controlled value (DPo) using proportional, integral,
        and derivative terms.

        The control law is::

            DPo += P*e + D*(e - elast)/dtime + I*(Inte + e*dtime)
        """
        # if stepping in time them caclulate new conditions
        if self.session.solver.time.v > self.timeLast.v:
            self.e = self.G - self.DPi.get()
            self.DPo.set_val(
                self.DPo.get()
                + (
                    self.P * self.e
                    + self.D * (self.e - self.elast) / self.session.solver.dtime
                    + self.I * (self.Inte + self.e * self.session.solver.dtime)
                )
            )
            self.timeLast = self.session.solver.time

    def step(self):
        """Step the integral term and error history for the next time step.

        Updates the error from the last time step (elast) and accumulates
        the current error into the integral term (Inte).
        """
        # step in time
        self.elast = self.e
        self.Inte = self.Inte + self.e.v * self.session.solver.dtime

    def dump(self, output_file):
        """Dump PIV controller state to an output file.

        Parameters
        ----------
        output_file : file-like
            File object to write the PIV state to.
        """
        output_file.write(f"{self.name1} PIV\n")
        super().real_print(output_file)
