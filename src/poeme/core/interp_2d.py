# TODO: Fix this file to use new error handling system
# Porentially combine the interp files and/or use an off-the-shelf interpolation


def _add_error(msg: str, p) -> None:
    """Add error message to session errors."""
    p.session.errors += msg


def interp_2d(x1, x2, x1i, x2i, yi, p):
    ix1 = index(x1, x1i, p)
    ix2 = index(x2, x2i, p)
    y00 = yi[ix1][ix2]
    y10 = yi[ix1 + 1][ix2]
    y01 = yi[ix1][ix2 + 1]
    y11 = yi[ix1 + 1][ix2 + 1]
    yx21 = (x1i[ix1 + 1] - x1) / (x1i[ix1 + 1] - x1i[ix1]) * y00 + (x1 - x1i[ix1]) / (
        x1i[ix1 + 1] - x1i[ix1]
    ) * y10
    yx22 = (x1i[ix1 + 1] - x1) / (x1i[ix1 + 1] - x1i[ix1]) * y01 + (x1 - x1i[ix1]) / (
        x1i[ix1 + 1] - x1i[ix1]
    ) * y11

    return (x2i[ix2 + 1] - x2) / (x2i[ix2 + 1] - x2i[ix2]) * yx21 + (x2 - x2i[ix2]) / (
        x2i[ix2 + 1] - x2i[ix2]
    ) * yx22


def index(x, temp, p):

    if x < temp[0]:
        msg = ""
        if p and hasattr(p, "parent") and p.parent != 0:
            msg += p.parent.name1 + "."
        if p and hasattr(p, "name1"):
            msg += p.name1 + "."
        msg += "interp 2d input too low " + str(x) + " < " + str(temp[0]) + "\n"
        _add_error(msg, p)
    if x > temp[len(temp) - 1]:
        msg = (
            "interp 2d input too high "
            + str(x)
            + " > "
            + str(temp[len(temp) - 1])
            + "\n"
        )
        _add_error(msg, p)

    location = 0
    while len(temp) > 2:
        lentemp = len(temp)
        i = int(lentemp / 2.0 + 1.0) - 1
        if x > temp[i]:
            temp = temp[i:]
            location = location + int(lentemp / 2.0 + 1.0) - 1
        else:
            temp = temp[: i + 1]
    return location
