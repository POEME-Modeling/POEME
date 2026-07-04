from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .constraint import Constraint
    from .dependent import Dependent
    from .element import Element
    from .independent import Independent
    from .newton import Newton
    from .state import State

_active_session: ContextVar[ModelSession | None] = ContextVar(
    "active_session", default=None
)


class ModelSession:
    """Owns all state for one simulation/model instance.

    Each independent model should create its own session.
    Sessions are fully isolated — no cross-contamination between models.

    Attributes
    ----------
    elements : list[Element]
        All elements registered in this session.
    independents : list[Independent]
        Independent variables for the solver.
    dependents : list[Dependent]
        Dependent variables for the solver.
    states : list[State]
        State variables for transient simulation.
    constraints : list[Constraint]
        Active constraints for the solver.
    solver : Newton | None
        The Newton-Raphson solver instance.
    errors : str
        Accumulated error messages.
    """

    def __init__(self) -> None:
        """Initialize an empty model session."""
        self.elements: list[Element] = []
        self.independents: list[Independent] = []
        self.dependents: list[Dependent] = []
        self.states: list[State] = []
        self.constraints: list[Constraint] = []
        self.solver: Newton | None = None
        self.errors: str = ""

    def reset(self) -> None:
        """Clear all registered objects (for multi-model runs)."""
        self.elements.clear()
        self.independents.clear()
        self.dependents.clear()
        self.states.clear()
        self.constraints.clear()
        self.errors = ""
        self.solver = None

    def __enter__(self) -> ModelSession:
        """Enter the session context and set as active.

        Returns
        -------
        ModelSession
            This session instance.
        """
        self._token = _active_session.set(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # type: ignore[return]
        """Exit the session context and reset the active session."""
        _active_session.reset(self._token)

    def check(self) -> None:
        """Call precheck() on all registered objects."""
        for e in self.elements:
            e.precheck()
            for v in e.VIDL:
                if v.isa( "FN" ) or v.isa( "MP" ):
                    if (v.isPort==True) and (v.other == 0):
                        print( "port "+ e.name1+ "." +v.name1+ " is not linked" )
        
        for i in self.independents:
            i.precheck()

        for d in self.dependents:
            d.precheck()

        for s in self.states:
            s.precheck()

        for c in self.constraints:
            c.precheck()

    def set(self, var: str, value: float) -> None:
        """Set a variable by name across all registered objects.

        Parameters
        ----------
        var : str
            The name of the variable to set.
        value : float
            The value to assign.
        """
        stuff = self.elements.copy()
        if self.solver:
            stuff.append(self.solver)

        for e in stuff:
            for v in e.VIDL:
                if v.name1 == var:
                    v.v = value
                if v.VIDL != 0:
                    for v1 in v.VIDL:
                        if v1.name1 == var:
                            v1.v = value
                        try:
                            for v2 in v1.VIDL():
                                if v2.name1 == var:
                                    v2.v = value

                        except:  # noqa: E722, S110
                            pass
