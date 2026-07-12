class Atom:
    """Base atom class for POEME element hierarchy.

    The Atom class serves as the root of the element inheritance hierarchy.
    All value types and elements derive from Atom and implement an isa()
    method to identify their type.
    """

    def isa(self, type):
        """Check if this atom is of a given type.

        Parameters
        ----------
        type : str
            The type string to check against.

        Returns
        -------
        bool
            True if the atom type matches the given type.
        """
        return type == "Atom"
