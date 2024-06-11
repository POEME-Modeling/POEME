from Atom import Atom
from VID import VID
from RealT import RealT

class Element(Atom):
    VIDL = list()

    def __init__(self, ElementList):
        ElementList.append(self)
        self.VIDL = list()
   
    def List(self, type, VIDL):
        if type == RealT:
            for v in VIDL:
                print(v.name)
           
    def Real(value, name, descript):
        variableID = VID(name, descript, "real")
        Element.VIDL.append(variableID)
        return value
   
    def isA(type):
        if (type == "Element"):
            return True
        else:
            return Atom.isa(type)



