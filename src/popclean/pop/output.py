import os

from . import g
from .element import Element
from .string_t import StringT

# Afrom EP import EP


class Output(Element):
    def __init__(self, name, **kwargs):
        super().__init__(name, "Output")
        self.name = name
        self.vars = ()
        self.filename = StringT(self, v="", desc="Output file")
        self.__dict__.update(kwargs)
        self.row = 0
        self.initial_list()

    def isa(self, type):
        return type == "Output"

    def calc(self):
        pass

    def dump(self):
        # print( "in dump" )
        temp = ""
        self.out = open(self.filename.v, "a")
        if self.row == 0:
            os.remove(self.filename.v)
            self.out = open(self.filename.v, "a")
            for e in self.vars:
                if e.parent == 0:
                    temp = temp + f"{e.name1[:10]:12s}"
                else:
                    temp = temp + f"{(e.parent.name1 + '.' + e.name1)[:10]:12s}"
            print(temp, file=self.out)

        temp = ""
        if len(g.errors) > 0:
            print(g.errors, file=self.out)
        for e in self.vars:
            temp = temp + f"{str(e)[:10]:12s}"
        print(temp, file=self.out)
        super().real_print()
        self.row = 1
        self.out.close()

        # print( f"{"Fp"[:10]:12s}{w.name1[:10]:12s}{("xloc:"+str(w.xloc))[:10]:12s}" ,
        #  file=g.pretty )
