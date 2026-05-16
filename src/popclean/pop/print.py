# TODO: fix this and get rid of noqa after g is fully refactored
def _get_g():
    """Lazily import g to avoid circular imports."""
    from . import g  # noqa PLC0415

    return g


def _print_ports(output_file, method_name="dump", port_types=None):
    """
    Write ports of specified types by calling the given method.

    Args:
        output_file: File object to write to
        method_name: Name of method to call on ports ('dump' or 'pretty')
        port_types: List of port type strings to filter (e.g., ['EP', 'FN', 'MP'])
    """
    if port_types is None:
        port_types = ["EP", "FN", "MP"]

    port_labels = {"EP": "Electric Ports", "FN": "Fluid Ports", "MP": "Mech Ports"}
    g_module = _get_g()

    for port_type in port_types:
        output_file.write("\n")
        output_file.write(f"{port_labels[port_type]}\n")
        for e in g_module.element_list:
            for p in e.VIDL:
                if p.isa(port_type):
                    getattr(p, method_name)(output_file)


def _print_elements(output_file, method_name="dump"):
    """
    Write all elements by calling the given method.

    Args:
        output_file: File object to write to
        method_name: Name of method to call on elements ('dump' or 'pretty')
    """
    g_module = _get_g()
    for e in g_module.element_list:
        getattr(e, method_name)(output_file)


def _print_section_header(output_file, title, style="simple"):
    """
    Write a formatted section header.

    Args:
        output_file: File object to write to
        title: Title text
        style: 'simple', 'decorative', or 'turbofan'
    """
    if style == "decorative":
        output_file.write("*" * 50 + "\n")
        output_file.write(f"{title}\n")
        output_file.write("*" * 50 + "\n")
    elif style == "turbofan":
        output_file.write("*" * 56 + "\n")
    else:  # simple
        output_file.write(f"{title}\n")


def _print_turbofan_port_data(output_file, element, port_name):
    """Write formatted turbofan port data for a specific port."""
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


def print_stdout(output_file):
    g_module = _get_g()
    """Write standard output format."""
    output_file.write(f"time = {g_module.NS.time}\n")
    output_file.write("Ports*************\n")
    _print_ports(output_file, method_name="dump")
    output_file.write("\n")
    output_file.write("Elements***********\n")
    output_file.write("\n")
    _print_elements(output_file, method_name="dump")


def print_pretty(output_file, errors):
    g_module = _get_g()
    """Write pretty-formatted output with detailed sections."""
    output_file.write("*" * 96 + "\n")
    output_file.write(f"{errors}\n")
    output_file.write(f"time = {g_module.NS.time}\n")
    output_file.write("\n")
    _print_section_header(output_file, "Ports*************", style="decorative")
    output_file.write("\n")
    _print_ports(output_file, method_name="pretty")
    output_file.write("\n")
    _print_section_header(output_file, "Elements***********", style="decorative")
    output_file.write("\n")
    _print_elements(output_file, method_name="pretty")
    output_file.write("\n")
    _print_section_header(output_file, "Solver**********", style="decorative")
    output_file.write("\n")
    g_module.NS.pretty(output_file)
    output_file.write("\n")


def print_scott(output_file, errors):
    """Write turbofan-formatted output."""
    g_module = _get_g()
    output_file.write("** TURBOFAN OUTPUT **".center(56, "*") + "\n")
    output_file.write(f"{errors}\n")
    output_file.write(f"time = {g_module.NS.time}\n")
    output_file.write("\n")
    _print_section_header(output_file, "Ports*************", style="turbofan")
    output_file.write("*" * 56 + "\n")

    for e in g_module.element_list:
        for p in e.VIDL:
            if p.isa("FN"):
                # TODO: validate that this always works. If not, put in better logic
                for p.name1 in ("FNo", "FNo1", "FNo2"):
                    _print_turbofan_port_data(output_file, e, p.name1)
