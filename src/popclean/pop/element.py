from . import g
from .atom import Atom
from .real_t import RealT
from .value_t import ValueT
from .vid import VID


class Element(Atom):
    def __init__(self, name, type):
        # Bypass custom __setattr__ for internal attributes during init
        super().__setattr__("VIDL", [])
        super().__setattr__("type", type)
        super().__setattr__("name", name)
        super().__setattr__("name1", name)
        super().__setattr__("x", -1.0)
        super().__setattr__("y", 0.0)
        g.element_list.append(self)

    def __setattr__(self, name, value):
        existing = self.__dict__.get(name)  # direct dict lookup, no descriptor overhead
        if isinstance(existing, ValueT):
            # Update the ValueT in-place, don't replace the object
            existing.set(value)
        else:
            super().__setattr__(name, value)

        # Assign name1 if the value has that attribute
        if hasattr(getattr(self, name), "name1"):
            getattr(self, name).name1 = name

    def initial_list(self):
        self.VIDLi = list()
        for v in self.VIDL:
            self.VIDLi.append(v)

    def add_independent(self, ind):
        self.ind_list.append(ind)

    def list(self, type, vidl):
        if type == RealT:
            for v in vidl:
                print(v.name)

    def real(self, value, name, descript):
        variable_id = VID(name, descript, "real")
        self.VIDL.append(variable_id)
        return value

    def isa(self, type):
        return type == "Element"

    def add_vid(self, v):
        self.VIDL.append(v)

    def preset(self):
        pass

    def precheck(self):
        pass

    def dump(self):
        pass

    def step(self):
        pass

    def before(self):
        pass

    def after(self):
        pass

    def real_print(self):
        for v in self.VIDL:
            if v.isa("RealT"):
                print(
                    f"  {v.name1[:8]:10s} {str(v.v)[:8]:8} {v.units:8} {v.desc}",
                    file=g.out,
                )
            if v.isa("ComplexT"):
                print("    ", v.name1, v.v, v.units, v.desc, file=g.out)

    def pretty(self):
        for v in self.VIDL:
            if v.isa("RealT"):
                print(
                    f"  {v.name1[:8]:10s} {str(v.v)[:8]:8} {v.units:8} {v.desc}",
                    file=g.pretty,
                )
            if v.isa("ComplexT"):
                print("    ", v.name1, v.v, v.units, v.desc, file=g.out)

    def hover(self):
        temp1 = ""
        temp1 = self.type + " " + self.name1 + "\n"
        for v in self.VIDL:
            if v.isa("RealT"):
                temp1 = (
                    temp1
                    + " "
                    + v.name1
                    + " "
                    + str(v.v)
                    + " "
                    + v.units
                    + " "
                    + v.desc
                    + "\n"
                )
            if v.isa("ComplexT"):
                temp1 = (
                    temp1
                    + " "
                    + v.name1
                    + " "
                    + str(v.v)
                    + " "
                    + v.units
                    + " "
                    + v.desc
                    + "\n"
                )
        return temp1
