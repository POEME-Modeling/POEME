from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from EP import EP
from Table1d import Table1d
import g


class Resistor(Element):

    def __init__(r, name):
        super().__init__(name, "Resistor")
        r.type = "Resistor"
        r.desc = "Simple reistor element"

        # electrical location/ports
        r.EPi = EP(r, io="in", desc="Inlet ElectricPort")
        r.EPo = EP(r, io="out", desc="Exit Electric Port")

        # tables
        r.RV = Table1d(r, units="ohms", desc="Resistance as a function of temeperature")

        # variables
        r.dV = ComplexT(r, units="volts", desc="Voltage drop")
        r.I = ComplexT(r, units="amps", desc="Current")
        r.R = RealT(r, units="ohms", desc="Resistance")
        r.Z = ComplexT(r, units="ohms", desc="Impedance")
        r.initialList()

    def calc(r):

        # determine the voltage drop
        r.dV = r.EPi.V - r.EPo.V

        # if the table is there, determine resistane from it
        if r.RV.full() == True:
            r.R = r.RV.calc(r.dV.real())

        # calculate impedence
        r.Z.setP(r.R, 0.0)

        # calculate the current
        r.I = r.dV / r.Z

        # set the ports
        # voltage does not chage
        r.EPi.setIV(-1.0 * r.I, r.EPi.V)
        r.EPo.setIV(r.I, r.EPo.V)

    def dump(self):
        print(self.name1, "Resistor", file=g.out)
        super().realPrint()

    def hover(self):
        temp1 = self.name1 + " Resistor\n" + super().hover()
        return temp1

    def pretty(r):
        print(
            f"{"Resistor"[:10]:12s}{r.name1[:10]:12s}{("R:"+str(r.R))[:10]:12s}{("dVr:"+str(r.EPi.Vr - r.EPo.Vr))[:10]:12s}{("dVi:"+str(r.EPi.Vi - r.EPo.Vi))[:10]:12s}{("Ir:"+str(r.EPi.Ir))[:10]:12s}{("Ii:"+str(r.EPi.Ii))[:10]:12s}",
            file=g.pretty,
        )
