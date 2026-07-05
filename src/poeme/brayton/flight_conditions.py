from poeme import (
    BooleanT,
    Element,
    Independent,
    ModelSession,
    RealT,
    StringT,
    Table1d,
)

from .fn import FN


class FlightConditions(Element):
    """Flight conditions element for Brayton cycle atmospheric state.

    Starts a flow stream using atmospheric tables to determine static
    temperature and pressure from altitude, then computes total conditions
    from Mach number.

    Parameters
    ----------
    name : str
        Name of the flight conditions element.
    session : ModelSession | None
        Model session to associate with this element.

    Attributes
    ----------
    comp : StringT
        Composition of the stream.
    alt : RealT
        Altitude (ft).
    MN : RealT
        Mach number.
    Pamb : RealT
        Ambient pressure (lbm/in²).
    Pt : RealT
        Total pressure (lbm/in²).
    Qdyn : RealT
        Dynamic pressure (lbf/ft²).
    Tamb : RealT
        Ambient temperature (R).
    Tt : RealT
        Total temperature (R).
    VTAS : RealT
        True air speed (ft/s).
    W : RealT
        Mass flow (lbm/sec).
    size : BooleanT
        Determines if the element is in design mode or not.
    Ptable : Table1d
        Table of pressure versus altitude.
    Ttable : Table1d
        Table of temperature versus altitude.
    """

    def __init__(self, name, session: ModelSession | None = None):
        super().__init__(name, "FlowStart", session=session)
        self.type = "FlightConditionsSMJ"

        self.desc = "Start a Flow stream."

        # variables
        self.comp = StringT(self, desc="Composition of the stream.")
        self.alt = RealT(self, units="ft", desc="Altitude")
        self.MN = RealT(self, desc="MN")
        self.Pamb = RealT(self, units="lbm/in2", desc="Ambient pressure")
        self.Pt = RealT(self, units="lbm/in2", desc="Total pressure")
        self.Qdyn = RealT(self, units="lbf/ft2", desc="Dynamic pressure")
        self.Tamb = RealT(self, units="R", desc="Ambient temperature")
        self.Tt = RealT(self, units="R", desc="Total temperature")
        self.VTAS = RealT(self, units="ft/s", desc="True air speed")
        self.W = RealT(self, units="lbm/sec", desc="Massflow")
        # self.gams = RealT(self, units="ft", desc="gamma")
        self.size = BooleanT(
            self, v=True, desc="Determine if the element is in design mode or not"
        )

        # altitude pressure temperature tables
        # data from https://www.digitaldutch.com/atmoscalc
        self.Ptable = Table1d( self, desc="Table of pressure versus altitude" )
        self.Ptable.x = [                                -5000,    -4000,    -3000,    -2000,    -1000,        0,
                  1000,     2000,     3000,     4000,     5000,     6000,     7000,     8000,     9000,    10000,
                 11000,    12000,    13000,    14000,    15000,    16000,    17000,    18000,    19000,    20000,
                 21000,    22000,    23000,    24000,    25000,    26000,    27000,    28000,    29000,    30000,
                 31000,    32000,    33000,    34000,    35000,    36000,    37000,    38000,    39000,    40000,
                 41000,    42000,    43000,    44000,    45000,    46000,    47000,    48000,    49000,    50000,
                 51000,    52000,    53000,    54000,    55000,    56000,    57000,    58000,    59000,    60000,
                 61000,    62000,    63000,    64000,    65000,    66000,    67000,    68000,    69000,    70000,
                 71000,    72000,    73000,    74000,    75000,    76000,    77000,    78000,    79000,    80000,
                 81000,    82000,    83000,    84000,    85000,    86000,    87000,    88000,    89000,    90000,
                 91000,    92000,    93000,    94000,    95000,    96000,    97000,    98000,    99000,   100000 ] # altitude, 'ft'
        self.Ptable.y = [                              17.5529,  16.9483,  16.3607,  15.7896,  15.2348,  14.6959,
               14.1726,  13.6644,  13.1711,  12.6923,  12.2277,  11.7770,  11.3398,  10.9159,  10.5049,  10.1065,
               9.72040,  9.34636,  8.98405,  8.63321,  8.29354,  7.96478,  7.64665,  7.33889,  7.04123,  6.75343,
               6.47523,  6.20638,  5.94664,  5.69578,  5.45355,  5.21974,  4.99410,  4.77644,  4.56651,  4.36413,
               4.16906,  3.98112,  3.80010,  3.62580,  3.45803,  3.29661,  3.14191,  2.99447,  2.85395,  2.72003,
               2.59239,  2.47073,  2.35479,  2.24429,  2.13897,  2.03860,  1.94293,  1.85176,  1.76486,  1.68204,
               1.60311,  1.52788,  1.45618,  1.38785,  1.32272,  1.26065,  1.20149,  1.14511,  1.09137,  1.04016,
              0.991347, 0.944827, 0.900489, 0.858232, 0.817958, 0.779578, 0.743039, 0.708261, 0.675156, 0.643641,
              0.613638, 0.585073, 0.557875, 0.531976, 0.507313, 0.483825, 0.461455, 0.440148, 0.419853, 0.400519,
              0.382101, 0.364553, 0.347833, 0.331902, 0.316720, 0.302253, 0.288464, 0.275323, 0.262796, 0.250856,
              0.239473, 0.228621, 0.218275, 0.208410, 0.199003, 0.190032, 0.181478, 0.173319, 0.165537, 0.158114 ] # pressure, 'psi'


        self.Ttable = Table1d( self, desc="Table of temperature versus altitude" )
        self.Ttable.x = [                                -5000,    -4000,    -3000,    -2000,    -1000,        0,
                  1000,     2000,     3000,     4000,     5000,     6000,     7000,     8000,     9000,    10000,
                 11000,    12000,    13000,    14000,    15000,    16000,    17000,    18000,    19000,    20000,
                 21000,    22000,    23000,    24000,    25000,    26000,    27000,    28000,    29000,    30000,
                 31000,    32000,    33000,    34000,    35000,    36000,    37000,    38000,    39000,    40000,
                 41000,    42000,    43000,    44000,    45000,    46000,    47000,    48000,    49000,    50000,
                 51000,    52000,    53000,    54000,    55000,    56000,    57000,    58000,    59000,    60000,
                 61000,    62000,    63000,    64000,    65000,    66000,    67000,    68000,    69000,    70000,
                 71000,    72000,    73000,    74000,    75000,    76000,    77000,    78000,    79000,    80000,
                 81000,    82000,    83000,    84000,    85000,    86000,    87000,    88000,    89000,    90000,
                 91000,    92000,    93000,    94000,    95000,    96000,    97000,    98000,    99000,   100000 ] # altitude, 'ft'
        self.Ttable.y = [                              536.501,  532.935,  529.368,  525.802,  522.236,  518.670,
               515.104,  511.538,  507.972,  504.405,  500.839,  497.273,  493.707,  490.141,  486.575,  483.008,
               479.442,  475.876,  472.310,  468.744,  465.178,  461.611,  458.045,  454.479,  450.913,  447.347,
               443.781,  440.214,  436.648,  433.082,  429.516,  425.950,  422.384,  418.818,  415.251,  411.685,
               408.119,  404.553,  400.987,  397.421,  393.854,  390.288,  389.970,  389.970,  389.970,  389.970,
               389.970,  389.970,  389.970,  389.970,  389.970,  389.970,  389.970,  389.970,  389.970,  389.970,
               389.970,  389.970,  389.970,  389.970,  389.970,  389.970,  389.970,  389.970,  389.970,  389.970,
               389.970,  389.970,  389.970,  389.970,  389.970,  390.180,  390.729,  391.278,  391.826,  392.375,
               392.923,  393.472,  394.021,  394.569,  395.118,  395.667,  396.215,  396.764,  397.313,  397.861,
               398.410,  398.958,  399.507,  400.056,  400.604,  401.153,  401.702,  402.250,  402.799,  403.348,
               403.896,  404.445,  404.994,  405.542,  406.091,  406.639,  407.188,  407.737,  408.285,  408.834 ] #temperature, 'Rankine'

   

        # fluid locations
        self.FNo = FN(self, io="out", desc="Outgoing flow")

        # solver stuff
        self.ind_1 = Independent(
            self,
            indname="W",
            perturb=0.05,
            scale=100,
            perturb_type="Relative",
            active=False,
            desc="Vary mass flow",
        )

    def calc(self):
        """Calculate flight conditions from altitude and Mach number.

        Sets composition, reads atmospheric temperature and pressure
        from tables based on altitude, sets mass flow, and computes
        total conditions from static conditions and Mach number. Also
        computes flight speed and dynamic pressure.

        Dynamic pressure is computed as::

            Qdyn = 0.5 * gamma * Pamb * MN^2 * 144.0
        """

        # set the comp
        self.FNo.comp = self.comp

        # read atmospheric conditions
        self.Tamb = self.Ttable.calc(self.alt)
        self.Pamb = self.Ptable.calc(self.alt)

        self.FNo.set_w(self.W)
        if self.MN > 0.0:
            self.FNo.set_ts_ps_mn(self.Tamb, self.Pamb, self.MN)
        else:
            self.FNo.MN = 0.0
            self.FNo.set_tp(self.Tamb, self.Pamb)

        self.Tt = self.FNo.Tt
        self.Pt = self.FNo.Pt

        # flight speed
        self.VTAS = self.FNo.V

        # dynamic pressure, 1/2 rho (V**2)
        self.Qdyn = 0.5 * self.FNo.gams * self.Pamb * (self.MN**2.0) * 144.0

    def precheck(self):
        """Activate or deactivate mass flow independent based on sizing mode.

        In sizing mode, the W independent is deactivated because the
        mass flow is fixed by user input. In fixed mode, it is activated
        so the solver can adjust the mass flow.
        """

        # design point turn off solver stuff
        if self.size == True:
            self.ind_1.active = False
        # off design turn on solver stuff
        else:
            self.ind_1.active = True

    def dump(self, output_file):
        """Dump flight conditions state to an output file.

        Parameters
        ----------
        output_file : file-like
            File object to write the flight conditions state to.
        """
        # dump output variables
        output_file.write(f"{self.name1} FlowStart\n")
        super().real_print(output_file)

    def pretty(self, output_file):
        """Print a formatted summary of the flight conditions state.

        Parameters
        ----------
        output_file : file-like
            File object to write the pretty-printed output to.
        """
        output_file.write(
            f"{'FlightConditions'[:10]:12s}{self.name1[:10]:12s}"
            f"{('W:' + str(self.W))[:10]:12s}{('Tt:' + str(self.FNo.Tt))[:10]:12s}"
            f"{('Pt:' + str(self.FNo.Pt))[:10]:12s}"
            f"{('Tamb:' + str(self.Tamb))[:10]:12s}"
            f"{('Pamb:' + str(self.Pamb))[:10]:12s}\n"
        )
