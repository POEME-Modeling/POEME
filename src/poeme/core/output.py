import os

from .element import Element
from .string_t import StringT

# Afrom EP import EP
# TODO: This should be re-written to take advantage of passing around output files
# instead of using global outputs. May be able to be deleted entirely


class Output(Element):
    """Output management for POEME simulation framework.

    Manages output file generation for simulation results, writing
    variable values and element state to external files.

    Parameters
    ----------
    name : str
        Name of the output element.
    **kwargs : dict
        Additional keyword arguments including filename and vars.

    Attributes
    ----------
    session : ModelSession
        Model session this output belongs to.
    name : str
        Name of the output element.
    name1 : str
        Name alias.
    vars : tuple
        List of variables to output.
    filename : StringT
        Output file path.
    row : int
        Output row counter (0 = header, 1 = data).
    out : file-like
        Open output file handle.
    """

    def __init__(self, name, **kwargs):
        super().__init__(name, "Output")
        self.name = name
        self.vars = ()
        self.filename = StringT(self, v="", desc="Output file")
        self.__dict__.update(kwargs)
        self.row = 0
        self.initial_list()

    def isa(self, type):
        """Check if this element is an Output.

        Parameters
        ----------
        type : str
            The type string to check against.

        Returns
        -------
        bool
            True if the type matches "Output".
        """
        return type == "Output"

    def calc(self):
        """Calculate output values.

        Default implementation does nothing.
        """
        pass

    def dump(self, output_file):
        """Write output data to the configured output file.

        On the first call (row == 0), writes the header with variable
        names. On subsequent calls, writes the current values.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to (unused, writes to self.out).
        """
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
        if len( self.session.errors ) > 0:
            print( self.session.errors, file=self.out )
        self.out.close()
        

        # self.out.write(
        #     f"{"Fp"[:10]:12s}{w.name1[:10]:12s}{("xloc:"+str(w.xloc))[:10]:12s}",
        # )
