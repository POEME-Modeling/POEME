"""Output formatting utilities for POEME simulation framework.

Provides functions for generating standard, pretty, and turbofan-formatted
output from simulation sessions, including port data, element data,
and solver state.
"""


def _print_ports(output_file, session, method_name="dump", port_types=None):
    """Write ports of specified types by calling the given method.

    Parameters
    ----------
    output_file : file-like
        File object to write to.
    session : ModelSession
        ModelSession instance.
    method_name : str
        Name of method to call on ports ('dump' or 'pretty').
    port_types : list
        List of port type strings to filter (e.g., ['EP', 'FN', 'MP']).
    """
    if port_types is None:
        port_types = ["EP", "FN", "MP"]

    port_labels = {"EP": "Electric Ports", "FN": "Fluid Ports", "MP": "Mech Ports"}

    for port_type in port_types:
        output_file.write("\n")
        output_file.write(f"{port_labels[port_type]}\n")
        for e in session.elements:
            for p in e.VIDL:
                if p.isa(port_type):
                    getattr(p, method_name)(output_file)


def _print_elements(output_file, session, method_name="dump"):
    """Write all elements by calling the given method.

    Parameters
    ----------
    output_file : file-like
        File object to write to.
    session : ModelSession
        ModelSession instance.
    method_name : str
        Name of method to call on elements ('dump' or 'pretty').
    """
    for e in session.elements:
        getattr(e, method_name)(output_file)


def _print_section_header(output_file, title, style="simple"):
    """Write a formatted section header.

    Parameters
    ----------
    output_file : file-like
        File object to write to.
    title : str
        Title text.
    style : str
        'simple', 'decorative', or 'turbofan'.
    """
    if style == "decorative":
        output_file.write("*" * 18 + "\n")
        output_file.write(f"{title}\n")
        output_file.write("*" * 18 + "\n")
    elif style == "turbofan":
        output_file.write("*" * 56 + "\n")
    else:  # simple
        output_file.write(f"{title}\n")


def _print_turbofan_port_data(output_file, element, port_name):
    """Write formatted turbofan port data for a specific port.

    Parameters
    ----------
    output_file : file-like
        File object to write to.
    element : Element
        The element containing the port.
    port_name : str
        Name of the port attribute on the element.
    """
    port = getattr(element, port_name)
    output_file.write(
        f"{element.name:12s} "
        f"{port.W.v:10.3f} "
        f"{port.Pt.v:10.3f} "
        f"{port.Tt.v:10.2f} "
        f"{port.ht.v:10.3f} "
        f"{port.s.v:10.5f} "
        f"{port.FAR.v:10.6f} "
        f"{port.rhos.v:10.6f} "
        f"{port.MN.v if hasattr(port, 'MN') else port.Ps.v:10.4f} "
        f"{port.Ps.v:10.3f} "
        f"{port.Ts.v:10.2f} "
        f"{port.A.v:10.3f}\n"
    )


def print_stdout(output_file, session):
    """Write standard output format.

    Parameters
    ----------
    output_file : file-like
        File object to write to.
    session : ModelSession
        ModelSession instance.
    """
    if session.solver:
        output_file.write(f"time = {session.solver.time}\n")
    output_file.write("Ports*************\n")
    _print_ports(output_file, session, method_name="dump")
    output_file.write("\n")
    output_file.write("Elements**********\n")
    output_file.write("\n")
    _print_elements(output_file, session, method_name="dump")


def print_pretty(output_file, session):
    """Write pretty-formatted output with detailed sections.

    Parameters
    ----------
    output_file : file-like
        File object to write to.
    session : ModelSession
        ModelSession instance.
    """
    output_file.write("*" * 96 + "\n")
    _print_section_header(output_file, "Errors************", style="decorative")  
    output_file.write(f"{session.errors}\n")
    if session.solver:
        output_file.write(f"time = {session.solver.time}\n")
    output_file.write("\n")
    _print_section_header(output_file, "Ports*************", style="decorative")
    output_file.write("\n")
    _print_ports(output_file, session, method_name="pretty")
    output_file.write("\n")
    _print_section_header(output_file, "Elements**********", style="decorative")
    output_file.write("\n")
    _print_elements(output_file, session, method_name="pretty")
    output_file.write("\n")
    _print_section_header(output_file, "Solver************", style="decorative")
    output_file.write("\n")
    if session.solver:
        session.solver.pretty(output_file)
    output_file.write("\n")
    #output_file.write( self.session.errors )


def print_scott(output_file, session):
    """Write turbofan-formatted output.

    Parameters
    ----------
    output_file : file-like
        File object to write to.
    session : ModelSession
        ModelSession instance.
    """

    output_file.write("** TURBOFAN OUTPUT **".center(56, "*") + "\n")
    _print_section_header(output_file, "Errors************", style="turbofan")   
    output_file.write(f"{session.errors}\n")
    output_file.write(f"time = {session.solver.time}\n")
    output_file.write("\n")
    _print_section_header(output_file, "Ports*************", style="turbofan")
    output_file.write("*" * 56 + "\n")

    for e in session.elements:
        for p in e.VIDL:
            if p.isa("FN"):
                # TODO: validate that this always works. If not, put in better logic
                for p.name1 in ("FNo", "FNo1", "FNo2"):
                    _print_turbofan_port_data(output_file, e, p.name1)
