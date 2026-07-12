# TODO: Fix this file to use new error handling system
# Porentially combine the interp files and/or use an off-the-shelf interpolation


def _add_error(msg: str, p) -> None:
    """Add error message to session errors.

    Parameters
    ----------
    msg : str
        The error message to add.
    p : object
        Parent object with a session attribute.
    """
    p.session.errors += msg


def interp_3d(x1, x2, x3, x1i, x2i, x3i, yi, p):
    """Perform trilinear interpolation on a 3D table.

    Locates the interpolation cell using binary search, then computes
    the interpolated value using trilinear weighting of the eight
    corner values.

    Parameters
    ----------
    x1 : float
        First interpolation coordinate.
    x2 : float
        Second interpolation coordinate.
    x3 : float
        Third interpolation coordinate.
    x1i : list
        Sorted array of x1 grid points.
    x2i : list
        Sorted array of x2 grid points.
    x3i : list
        Sorted array of x3 grid points.
    yi : list
        3D lookup table of y values.
    p : object
        Parent object for error reporting.

    Returns
    -------
    float
        The interpolated y value at (x1, x2, x3).
    """

    ix1 = index(x1, x1i, p)
    ix2 = index(x2, x2i, p)
    ix3 = index(x3, x3i, p)

    y0 = yi[ix1][ix2][ix3]
    y1 = yi[ix1][ix2][ix3 + 1]

    yx20 = (x3 - x3i[ix3]) / (x3i[ix3 + 1] - x3i[ix3]) * (y1 - y0) + y0

    y0 = yi[ix1][ix2 + 1][ix3]
    y1 = yi[ix1][ix2 + 1][ix3 + 1]

    yx21 = (x3 - x3i[ix3]) / (x3i[ix3 + 1] - x3i[ix3]) * (y1 - y0) + y0

    yx10 = (x2 - x2i[ix2]) / (x2i[ix2 + 1] - x2i[ix2]) * (yx21 - yx20) + yx20

    y0 = yi[ix1 + 1][ix2][ix3]
    y1 = yi[ix1 + 1][ix2][ix3 + 1]

    yx20 = (x3 - x3i[ix3]) / (x3i[ix3 + 1] - x3i[ix3]) * (y1 - y0) + y0

    y0 = yi[ix1 + 1][ix2 + 1][ix3]
    y1 = yi[ix1 + 1][ix2 + 1][ix3 + 1]

    yx21 = (x3 - x3i[ix3]) / (x3i[ix3 + 1] - x3i[ix3]) * (y1 - y0) + y0
    yx11 = (x2 - x2i[ix2]) / (x2i[ix2 + 1] - x2i[ix2]) * (yx21 - yx20) + yx20

    val = (x1 - x1i[ix1]) / (x1i[ix1 + 1] - x1i[ix1]) * (yx11 - yx10) + yx10

    return val


# TODO: which def index to use?????
# def index(x, temp):
#     location = 0
#     while len(temp) > 2:
#         lentemp = len(temp)
#         i = int(lentemp / 2.0 + 1.0) - 1
#         if x > temp[i]:
#             temp = temp[i:]
#             location = location + int(lentemp / 2.0 + 1.0) - 1
#         else:
#             temp = temp[: i + 1]
#     return location


def index(x, temp, p):
    """Binary search to find the index of x in a sorted array.

    Locates the position where x falls between two consecutive
    elements in the sorted array temp. Reports errors for
    out-of-bounds inputs.

    Parameters
    ----------
    x : float
        The value to search for.
    temp : list
        Sorted array to search in.
    p : object
        Parent object for error reporting.

    Returns
    -------
    int
        The index of the lower bound of x in temp.
    """

    if x < temp[0]:
        msg = ""
        if p and hasattr(p, "parent") and p.parent != 0:
            msg += p.parent.name1 + "."
        if p and hasattr(p, "name1"):
            msg += p.name1
        msg += " interp 3d input too low " + str(x) + " < " + str(temp[0]) + "\n"

        _add_error(msg, p)
    if x > temp[len(temp) - 1]:
        if p.parent != 0:
            p.session.errors = p.session.errors + p.parent.name1 + "."
        p.session.errors = (
            p.session.errors
            + p.name1
            + "interp 3d input too high "
            + str(x)
            + " > "
            + str(temp[len(temp) - 1])
            + "\n"
        )

    # location = 0
    min = 0
    max = len(temp)
    while max - min > 2:
        # lentemp = len(temp)
        i = int((max + min) / 2.0 + 1.0) - 1
        if x > temp[i]:
            min = i
            # location = location + int( lentemp/2. + 1. ) - 1
        else:
            max = i + 1

    return min
