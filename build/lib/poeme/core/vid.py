from .atom import Atom


class VID(Atom):
    def __init__(self, name, descript, type):
        self.name = name
        self.descript = descript
        self.type = type
