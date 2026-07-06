import os

from .element import Element
from .string_t import StringT

# Afrom EP import EP
# TODO: This should be re-written to take advantage of passing around output files
# instead of using global outputs. May be able to be deleted entirely


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

    def dump(self, output_file):
        # print( "in dump" )
        temp = ""
        self.out = open(self.filename.v, "a")
        if self.row == 0:
            os.system("del /f /q " + self.filename.v)
            self.out = open(self.filename.v, "w")
            for e in self.vars:
                if hasattr(e, "parent"):
                    temp = temp + f"{e.name1[:10]:12s}"
                else:
                    temp = temp + f"{(e.parent.name1 + '.' + e.name1)[:10]:12s}"
            print(temp, file=self.out)

        temp = ""
        if self.session and len(self.session.errors) > 0:
            print(self.session.errors, file=self.out)
        for e in self.vars:
            temp = temp + f"{str(e)[:10]:12s}"
        print(temp, file=self.out)
        super().real_print(self.out)
        self.row = 1
        if len(self.session.errors) > 0:
            print(self.session.errors, file=self.out)
        self.out.close()

        # self.out.write(
        #     f"{"Fp"[:10]:12s}{w.name1[:10]:12s}{("xloc:"+str(w.xloc))[:10]:12s}",
        # )
