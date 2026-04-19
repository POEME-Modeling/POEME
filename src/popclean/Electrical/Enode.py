from Element import Element
from Dependent import Dependent
from Independent import Independent
from ComplexT import ComplexT
from RealT import RealT
from EP import EP

import g


class Enode(Element):

    def __init__(e, name):
        super().__init__(name, "Enode")
        e.name = name

        e.desc = (
            "This element is an electrical node location.  It has a voltage "
            + " that is represented by a complex number.  Any number of impedance "
            + " elements can be hooked into this element.  It will determine the net"
            + " current it is seeing based on the system conditions. "
        )

        # eletrical connections
        e.port_list = list()

        # solver stuff
        e.ind_1 = Independent(
            e,
            indname="Vr",
            perturb=0.05,
            scale=100,
            perturb_type="Relative",
            active=True,
            desc="Varies real component of Voltage",
        )
        e.ind_2 = Independent(
            e,
            indname="Vi",
            perturb=0.05,
            scale=100,
            perturb_type="Relative",
            active=True,
            desc="Varies imaginary component of Voltage",
        )
        e.dep_1 = Dependent(
            e,
            d1name="IinR",
            d2name="IoutR",
            val_scale=1.0,
            active=True,
            desc="Balances real component of current",
        )
        e.dep_2 = Dependent(
            e,
            d1name="IinI",
            d2name="IoutI",
            val_scale=1.0,
            active=True,
            desc="Balances imaginary component of current",
        )

        # Variables
        e.V = ComplexT(e, units="volts", desc="Voltage")
        e.Vi = RealT(e, units="volts", desc="Imaginary component of voltage")
        e.Vr = RealT(e, units="volts", desc="Real component of voltage")
        e.IinI = RealT(e, units="amps", desc="Imaginery component of I coming in")
        e.IinR = RealT(e, units="amps", desc="Real component of I comping in")
        e.IoutI = RealT(e, units="amps", desc="Imaginary component of I going out")
        e.IoutR = RealT(e, units="amps", desc="Real component I going out")
        e.Inet = ComplexT(e, units="amps", desc="Current")
        e.initialList()

    # def LinkPort( e, port ):
    # e.port_list.append( port )

    # first step in solver pass is to set the voltage in all of the ports
    def preset(e):
        for p in e.port_list:
            e.V = complex(e.Vr.v, e.Vi.v)
            p.setIV(p.I.v, e.V.v)

    # before anything is run at all, loop through all substructures to find the
    # ports
    def precheck(e):
        e.port_list = list()
        for v in e.VIDL:
            if v.isa("EP"):
                e.port_list.append(v)

    def linkE(e, ep):
        temp = EP(e, io="in")
        temp.other = ep
        ep.other = temp
        if ep.io == "in":
            temp.io = "out"
        else:
            temp.io = "in"
        temp.name1 = ep.parent.name1 + "_" + ep.name1

    def calc(e):

        # zero out the running current totals
        e.IinR = 0.0
        e.IoutR = 0.0
        e.IinI = 0.0
        e.IoutI = 0.0

        # loops through the ports
        # if current coming in, add it to in total
        # if current going out, add it to the out total
        for p in e.port_list:
            if p.I.v.real > 0:
                e.IinR = e.IinR + p.I.v.real
            else:
                e.IoutR = e.IoutR - p.I.v.real
            if p.I.v.imag > 0:
                e.IinI = e.IinI + p.I.v.imag
            else:
                e.IoutI = e.IoutI - p.I.v.imag

    def dump(self):
        print(self.name, "Node", file=g.out)
        super().realPrint()

    def pretty(self):
        print(
            f"{"Node"[:10]:12s}{self.name1[:10]:12s}{("Vr:"+str(self.Vr))[:10]:12s}{("Vi:"+str(self.Vi ))[:10]:12s}",
            file=g.pretty,
        )
