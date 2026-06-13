# TODO: Fix this file to use new error handling system


class Table2d:
    def __init__(self, p, **kwargs):
        self.name1 = ""
        self.VIDL = 0
        p.add_vid(self)
        self.x = [0.0]
        self.y = [0.0]
        self.data = [0.0]
        self.units = ""
        self.desc = ""
        self.extrapError = False
        self.__dict__.update(kwargs)

        self.parent = p
        self.type = "Table2d"

    def _add_error(self, msg: str) -> None:
        """Add error message to session errors."""
        self.parent.session.errors += msg

    def full(self):
        # determine if the table has data or not
        return len(self.x) > 1

    def calc(self, xin, yin):

        # find the location in the table and interpolate
        x = xin if isinstance(xin, float) else xin.v
        y = yin if isinstance(yin, float) else yin.v

        xi, yi = None, None
        for i, (x1, x2) in enumerate(zip(self.x[:-1], self.x[1:], strict=True)):
            if x1 <= x <= x2:
                xi, w_x2, w_x1 = i, (x - x1) / (x2 - x1), (x2 - x) / (x2 - x1)
                break
        for i, (y1, y2) in enumerate(zip(self.y[:-1], self.y[1:], strict=True)):
            if y1 <= y <= y2:
                yi, w_y2, w_y1 = i, (y - y1) / (y2 - y1), (y2 - y) / (y2 - y1)
                break
        if x < self.x[0]:
            x1 = self.x[0]
            x2 = self.x[1]
            xi, w_x2, w_x1 = 0, (x - x1) / (x2 - x1), (x2 - x) / (x2 - x1)
            msg = ""
            if self.parent != 0:
                msg += self.parent.name1 + "."
            msg += self.name1
            msg += " Table 2d input to low " + str(x) + " < " + str(self.x[0]) + "\n"
            if ( self.extrapError ):
                self._add_error(msg)

        if x > self.x[len(self.x) - 1]:
            x1 = self.x[len(self.x) - 2]
            x2 = self.x[len(self.x) - 1]
            xi, w_x2, w_x1 = len(self.x) - 2, (x - x1) / (x2 - x1), (x2 - x) / (x2 - x1)
            msg = ""
            if self.parent != 0:
                msg += self.parent.name1 + "."
            msg += self.name1
            msg += (
                " Table 2d input to high "
                + str(x)
                + " > "
                + str(self.x[len(self.x) - 1])
                + "\n"
            )
            if ( self.extrapError ):
                self._add_error(msg)

        if y < self.y[0]:
            y1 = self.y[0]
            y2 = self.y[1]
            yi, w_y2, w_y1 = 0, (y - y1) / (y2 - y1), (y2 - y) / (y2 - y1)
            msg = ""
            if self.parent != 0:
                msg += self.parent.name1 + "."
            msg += self.name1
            msg += " Table 2d input to low " + str(y) + " < " + str(self.y[0]) + "\n"
            if ( self.extrapError ):
                self._add_error(msg)

        if y > self.y[len(self.y) - 1]:
            y1 = self.y[len(self.y) - 2]
            y2 = self.y[len(self.y) - 1]
            yi, w_y2, w_y1 = len(self.y) - 2, (y - y1) / (y2 - y1), (y2 - y) / (y2 - y1)
            msg = ""
            if self.parent != 0:
                msg += self.parent.name1 + "."
            msg += self.name1
            msg += (
                " Table 2d input to high "
                + str(y)
                + " > "
                + str(self.y[len(self.y) - 1])
                + "\n"
            )
            if ( self.extrapError ):
                self._add_error(msg)

        # if xi is None or yi is None:
        # return False

        ave = self.data[xi][yi] * w_x1 * w_y1
        ave += self.data[xi][yi + 1] * w_x1 * w_y2

        ave += self.data[xi + 1][yi] * w_x2 * w_y1
        ave += self.data[xi + 1][yi + 1] * w_x2 * w_y2

        return ave

    def isa(self, type):
        return type == "Table2d"

    def save_print(self):
        temp = (self.parent.name1 + "." + self.name1 + ".x = " + str(self.x)) + "\n"
        temp = (
            temp + (self.parent.name1 + "." + self.name1 + ".y = " + str(self.y)) + "\n"
        )
        temp = temp + (
            self.parent.name1 + "." + self.name1 + ".data = " + str(self.data)
        )
        return temp
