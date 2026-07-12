class ValueT:
    """Base value type for POEME.

    The ValueT class serves as the base class for all value types in the
    POEME simulation framework, including RealT, ComplexT, BooleanT, IntT,
    StringT, and StringVarT. Provides the common interface for value
    manipulation and perturbation.
    """

    def __init__(self):
        """Initialize the base value type."""
        pass

    def perturb(self):
        """Generate perturbation values for this value.

        Default implementation does nothing. Override in subclasses.
        """
        pass
