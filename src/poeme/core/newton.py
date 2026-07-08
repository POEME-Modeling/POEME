import math
import sys

import numpy as np
from numpy import dot, outer
from scipy import linalg

from .boolean_t import BooleanT
from .element import Element
from .print import print_stdout
from .real_t import RealT
from .session import ModelSession, _active_session


def magnitude(vector):
    """Compute the Euclidean magnitude of a vector.

    Parameters
    ----------
    vector : iterable
        The vector to compute the magnitude of.

    Returns
    -------
    float
        The Euclidean norm of the vector.
    """
    return math.sqrt(sum(pow(element, 2) for element in vector))


# No dependents or constraints yet
# Still need to generate independent list from elements
class Newton(Element):
    """Newton-Raphson solver for POEME simulation framework.

    Implements a Newton-Raphson solver with Broyden update for solving
    nonlinear systems of equations. Supports both steady-state and
    transient analysis with independent variable perturbations and
    dependent equation convergence checking.

    Parameters
    ----------
    name : str
        Name of the solver.
    output_file : file-like | None
        File to write output to. If None, defaults to "newton.out".
    session : ModelSession | None
        Model session to associate with this solver.

    Attributes
    ----------
    session : ModelSession
        Model session this solver belongs to.
    name1 : str
        Name of the solver.
    output_file : file-like
        Output file handle.
    VIDL : list
        List of variable IDs.
    ind_list : list
        List of active independent variables.
    dep_list : list
        List of active dependent variables.
    maxJacobians : RealT
        Maximum number of Jacobian evaluations.
    numpasses : RealT
        Number of solver passes completed.
    tolerance : RealT
        Convergence tolerance.
    constraints : bool
        Whether constraints are active.
    type : str
        Type identifier ("NewtonSolver").
    time : RealT
        Simulation time.
    dtime : RealT
        Simulation time step.
    timeLast : RealT
        Simulation stop time.
    trans : BooleanT
        True for transient, False for steady-state.
    converged : BooleanT
        Convergence flag.
    x : int
        GUI x location.
    y : int
        GUI y location.
    """

    def __init__(self, name, output_file=None, session: ModelSession | None = None):
        if session is None:
            session = _active_session.get()
        if session is None:
            error_msg = f"Newton {name} requires a session parameter or active "
            "ModelSession context"
            raise ValueError(error_msg)
        self.session = session

        self.desc = "Newton is a Newton Rhapson solver. It is used to balance the "
        "models by varying the independents in the models such that the dependents and "
        "states are satisfied. The number of independents and dependents/states need "
        "to be equal to ensure a square Jacobian matrix. The solver allows for "
        "constraints to be specified. The contraints need to be tied to dependent and "
        "they replace the dependent when they are not satisfied.\nIn steady-state mode "
        "the states act just line dependents. The requirement is that their "
        "steady-state condition is met. In transient mode, the state requirement is "
        "that the value of the state matches the value predictied by integrating the "
        "derivative.\nFor transient runs, the solver will step through time based on "
        "the user input time step. It will solve each time step as a case and advance "
        "in time until the stop time is reached."

        # variables
        self.name1 = name
        # TODO: fix this to use a better default
        self.output_file = (
            output_file if output_file is not None else open("newton.out", "w")
        )
        self.VIDL = list()
        self.ind_list = self.session.independents
        self.iterCount = RealT(
            self, v=0.0, units="Integer", desc="Maxium number of Jacobians"
        )
        self.dep_list = self.session.dependents
        self.maxJacobians = RealT(
            self, v=50.0, units="Integer", desc="Maxium number of Jacobians"
        )
        self.maxIterations = RealT(
            self, v=100.0, units="Integer", desc="Maxium number of iterataions"
        )
        self.numpasses = RealT(self, v=0.0, units="Integer", desc="Number of passes")
        self.tolerance = RealT(self, v=0.0001, units="real", desc="tolernace")
        self.constraints = False
        self.session.solver = self
        self.type = "NewtonSolver"
        self.time = RealT(self, v=0.0, units="seconds", dessc="Simulation time")
        self.dtime = RealT(self, v=0.05, units="seconds", desc="Simulation time step")
        self.timeLast = RealT(
            self, v=0.05, units="seconds", desc="Simulation stop time"
        )
        self.trans = BooleanT(self, v=False, desc="Truer for transient, false for SS")
        self.converged = BooleanT(self, v=False, desc="converged flag")

        self.debugfile = open("solver.debug", "w")
        self.debug = BooleanT(
            self, v=False, desc="Determine is solver debug information is printed"
        )
        self.transView = 0

        # gui location
        self.x = 0
        self.y = 0

    # define one analysis pass
    def onepass(self):
        """Execute one analysis pass over all elements.

        Runs preset(), before(), calc(), and after() on all elements
        in the session. Increments the pass counter.
        """

        self.session.errors = ""
        self.numpasses = self.numpasses + 1
        # run the prepass on all the elements
        for e in self.session.elements:
            e.preset()

        # run the calculate section for one element
        for e in self.session.elements:
            e.before()
            e.calc()
            e.after()

    # run
    def run(self):
        """Run the solver in either steady-state or transient mode.

        If transient mode is enabled, calls transrun(). Otherwise,
        calls solve() for steady-state analysis.
        """
        if self.trans == False:
            self.solve()
        else:
            self.transrun()

    # solve the system
    def solve(self):
        """Solve the system of equations using Newton-Raphson with Broyden update.

        Collects active dependents, independents, states, and constraints.
        Builds and inverts the Jacobian matrix, then iteratively updates
        independent variables until convergence or max iterations.
        """

        self.iterCount = 0
        if self.debug == True:
            print("\n\n", file=self.debugfile)
            print("SOLVER DEBUG", file=self.debugfile)
        self.numpasses = 0.0
        # get the list of all the solver objects
        self.ind_list = list()
        self.dep_list = list()
        self.state_list = list()
        self.con_list = list()

        if self.debug == True:
            print("INDEPENDENTS", file=self.debugfile)
        for i in self.session.independents:
            if i.active == True:
                self.ind_list.append(i)
                if self.debug == True:
                    print(i.name1, i.ind.parent.name, i.ind.name1, file=self.debugfile)

        if self.debug == True:
            print("DEPENDENTS", file=self.debugfile)
        for d in self.session.dependents:
            if d.active == True:
                self.dep_list.append(d)
                if self.debug == True:
                    print(
                        d.name1,
                        d.d1.parent.name1,
                        d.d1.name1,
                        d.d2.parent.name1,
                        d.d2.name1,
                        file=self.debugfile,
                    )

        if self.debug == True:
            print("STATES", file=self.debugfile)
        for st in self.session.states:
            if st.active == True:
                self.state_list.append(st)
                if self.debug == True:
                    print(
                        st.name1,
                        st.d1.parent.name1,
                        st.d1.name1,
                        st.d2.parent.name1,
                        d.d2.name1,
                        file=self.debugfile,
                    )

        if self.debug == True:
            print("CONSTRAINTS", file=self.debugfile)
        for c in self.session.constraints:
            if c.on == True:
                self.con_list.append(c)
                c.active = False
                c.dep.active = True
                if self.debug == True:
                    print(
                        c.name1,
                        c.d1.parent.name1,
                        c.d1.name1,
                        c.d2.parent.name1,
                        c.d2.name1,
                        file=self.debugfile,
                    )

        # create an empty matrix
        matrix = np.zeros(
            (len(self.ind_list), len(self.dep_list) + len(self.state_list))
        )

        if len(self.ind_list) != len(self.dep_list) + len(self.state_list):
            print(
                "the number of independents "
                + str(len(self.ind_list))
                + " does not match the number of dependents and states "
                + str(len(self.dep_list) + len(self.state_list))
            )
            sys.exit()
        delx = np.zeros(len(self.ind_list))
        delxs = np.zeros(len(self.ind_list))
        dely = np.zeros(len(self.ind_list))

        self.constraints = True
        # start working
        while self.constraints == True:
            self.converged.set(False)
            iter = 0
            self.session.errors = ""
            err_sum_last = 9e9
            err_sum = 8e9
            while iter < self.maxJacobians.v and self.converged == False:
                iter = iter + 1
                if self.debug == True:
                    print(
                        "Error summation update",
                        err_sum,
                        err_sum_last,
                        file=self.debugfile,
                    )
                if iter > 1 and len(self.ind_list) > 1 and err_sum < err_sum_last:
                    id = 0
                    for d in self.dep_list:
                        if d.active == True:
                            dely[id] = d.dep_error() - d.errLast
                            d.errLast.v = d.dep_error()
                            id = id + 1

                    for st in self.state_list:
                        if st.active == True:
                            dely[id] = st.dep_error() - st.errLast
                            st.errLast.v = st.dep_error()
                            id = id + 1

                    for c in self.con_list:
                        if c.active == True:
                            dely[id] = c.dep_error() - c.errLast
                            c.errLast.v = c.dep_error()
                            id = id + 1

                    # a1 = np.dot(matrix, delxs)
                    # a2 = dely
                    # a3 = a2 - a1
                    # a4 = np.outer(a3, delxs)
                    # a5 = np.dot(delxs, delxs)
                    # a6 = a4 / a5

                    a7 = outer(dely - dot(matrix, delxs), delxs) / dot(delxs, delxs)
                    matrix = matrix + a7

                    if self.debug == True:
                        print("BROYDEN MATRIX UPDATE", file=self.debugfile)
                        print(matrix, file=self.debugfile)

                    # matrix = matrix + outer( dely - dot( matrix, delxs ), delxs )
                    # / dot( delxs, delxs )

                else:
                    scale = 0
                    # run base point
                    try:
                        self.onepass()
                    except:  # noqa: E722
                        iter = self.maxJacobians.v

                    err_sum = 0

                    # check the active dep, states, and cons
                    for d in self.dep_list:
                        if d.active == True:
                            d.baseError = d.dep_error()
                            err_sum = err_sum + d.baseError**2.0

                    for st in self.state_list:
                        if st.active == True:
                            st.baseError = st.dep_error()
                            err_sum = err_sum + st.baseError**2.0

                    for c in self.con_list:
                        if c.active == True:
                            c.baseError = c.dep_error()
                            err_sum = err_sum + c.baseError**2.0

                    icount = 0
                    # matrixold = matrix

                    # perturb independents and determine response
                    for i in self.ind_list:
                        dx = i.perturb_v()
                        # perturb ind
                        i.ind.v = i.ind.v + dx
                        dcount = 0
                        # try:
                        self.onepass()

                        for d in self.dep_list:
                            if d.active == True:
                                matrix[dcount][icount] = (
                                    d.dep_error() - d.baseError
                                ) / dx
                                dcount = dcount + 1

                        for st in self.state_list:
                            if st.active == True:
                                matrix[dcount][icount] = (
                                    st.dep_error() - st.baseError
                                ) / dx
                                dcount = dcount + 1

                        for c in self.con_list:
                            if c.active == True:
                                matrix[dcount][icount] = (
                                    c.dep_error() - c.baseError
                                ) / dx
                                dcount = dcount + 1

                        # except:
                        # iter = self.maxJacobians.v

                        # move independent back
                        i.ind.v = i.ind.v - dx
                        icount = icount + 1
                    if self.debug == True:
                        print("JACOBIAN MATRIX", file=self.debugfile)
                        print(matrix, file=self.debugfile)

                # invert the matrix
                try:
                    imatrix = linalg.inv(matrix)
                except:  # noqa: E722
                    iter = self.maxJacobians.v
                    self.session.errors += "Could not invert solver matrix\n"

                    zero_row_indices = []
                    for i, row in enumerate(matrix):
                        # all() checks if the condition (x == 0) is true
                        # for every element in the row
                        if all(x == 0 for x in row):
                            zero_row_indices.append(i)

                    if len(zero_row_indices) > 0:
                        depnumber = zero_row_indices[0]
                        dcount = 0
                        for d in self.dep_list:
                            if d.active == True:
                                if dcount == depnumber:
                                    dep = d
                                dcount = dcount + 1

                        for st in self.state_list:
                            if st.active == True:
                                if dcount == depnumber:
                                    dep = st
                                dcount = dcount + 1

                        for c in self.con_list:
                            if c.active == True:
                                if dcount == depnumber:
                                    dep = c
                                dcount = dcount + 1

                        print(
                            "Dependent "
                            + dep.parent.name1
                            + "."
                            + dep.name1
                            + " is not effected by any of the independents"
                        )
                        sys.exit()

                    matrix_T = [list(row) for row in zip(*matrix, strict=True)]
                    matrix = matrix_T
                    zero_row_indices = []
                    for i, row in enumerate(matrix):
                        # all() checks if the condition (x == 0) is true
                        # for every element in the row
                        if all(x == 0 for x in row):
                            zero_row_indices.append(i)

                    if len(zero_row_indices) > 0:
                        ind = self.ind_list[zero_row_indices[0]]
                        print(
                            "Varying independent "
                            + ind.parent.name1
                            + "."
                            + ind.name1
                            + " has no effect on the model"
                        )
                        sys.exit()

                    n_rows = len(matrix)
                    print(n_rows)
                    for i in range(n_rows):
                        for j in range(i + 1, n_rows):
                            row_i, row_j = matrix[i], matrix[j]

                            same = True
                            ratioBase = 0.0
                            ratio = 0.0
                            for column in range(len(row_i)):
                                if abs(row_j[column]) < 0.00000000001:
                                    if abs(row_i[column]) > 0.00000000001:
                                        same = False
                                else:
                                    ratio = row_i[column] / row_j[column]
                                if abs(ratioBase) <= 0.00000000001:
                                    ratioBase = ratio
                                if abs(ratio - ratioBase) > 0.00000000001:
                                    same = False

                            # Check if all ratios are equal (within tolerance)
                            if same:
                                # pairs.append((i, j, ratios[0]))
                                ind = self.ind_list[i]
                                print(
                                    "Varying independent "
                                    + ind.parent.name1
                                    + "."
                                    + ind.name1
                                )
                                ind = self.ind_list[j]
                                print(
                                    "Is multiplicative of varying independent "
                                    + ind.parent.name1
                                    + "."
                                    + ind.name1
                                )
                                sys.exit()

                bc = 0

                # if the error keeps improving, keep using jacobian
                # while err_sum <= err_sum_last and self.converged == False:
                check = 0
                while check == 0:
                    # try:

                    check = 1

                    bc = bc + 1
                    # broyden update

                    ic = 0

                    self.onepass()

                    # determine how much to change an independent by
                    # how it affects the deps, etc
                    for _i in self.ind_list:
                        id = 0
                        delx[ic] = 0
                        for d in self.dep_list:
                            if d.active == True:
                                d.errLast.v = d.dep_error()
                                delx[ic] = delx[ic] - imatrix[ic][id] * d.dep_error()
                                id = id + 1

                        for st in self.state_list:
                            if st.active == True:
                                st.errLast.v = st.dep_error()
                                delx[ic] = delx[ic] - imatrix[ic][id] * st.dep_error()
                                id = id + 1

                        for c in self.con_list:
                            if c.active == True:
                                c.errLast.v = c.dep_error()
                                delx[ic] = delx[ic] - imatrix[ic][id] * c.dep_error()
                                id = id + 1
                        ic = ic + 1

                    # determine a maximum the inds are allowed to step
                    # based on the max value for any ind
                    # all other inds are scaled to this vale
                    ic = 0
                    scale = 1.0
                    # maxdx = 1.0
                    iscale = 1.0
                    for i in self.ind_list:
                        if i.ind.v != 0:
                            scale = i.ind.v
                        if i.scale.v != 0:
                            scale = i.scale.v
                        if abs(delx[ic] / scale) > 0.1 and abs(delx[ic]) > abs(
                            0.1 * scale
                        ):
                            iscale = min(iscale, abs(0.1 * scale / delx[ic]))

                        ic = ic + 1
                    if iscale == 0:
                        iscale = 1.0
                    # iscale = 1.

                    # update the inds
                    # and rerun
                    ic = 0
                    if self.debug == True:
                        print("Independents", file=self.debugfile)

                    for i in self.ind_list:
                        delxs[ic] = delx[ic] * iscale
                        i.ind.v = i.ind.v + delxs[ic]
                        ic = ic + 1
                        if self.debug == True:
                            print(
                                i.name1,
                                i.ind.parent.name,
                                i.ind.name1,
                                i.ind.v,
                                file=self.debugfile,
                            )

                    # try:
                    self.onepass()
                    self.iterCount = self.iterCount + 1
                    # except:
                    # iter = self.maxJacobians.v

                    err_sum_last = err_sum
                    err_sum = 0.0

                    if self.debug == True:
                        print("Dependents", file=self.debugfile)
                    for d in self.dep_list:
                        if d.active == True:
                            err_sum = err_sum + d.dep_error() ** 2.0
                            if self.debug == True:
                                print(
                                    d.name1,
                                    d.d1.parent.name1,
                                    d.d1.name1,
                                    d.d1.v,
                                    d.d2.parent.name1,
                                    d.d2.name1,
                                    d.d2.v,
                                    d.dep_error(),
                                    file=self.debugfile,
                                )

                    if self.debug == True:
                        print("States", file=self.debugfile)
                    for st in self.state_list:
                        if st.active == True:
                            err_sum = err_sum + st.dep_error() ** 2.0
                            if self.debug == True:
                                print(
                                    st.name1,
                                    st.d1.parent.name1,
                                    st.d1.name1,
                                    st.d1.v,
                                    st.d2.parent.name1,
                                    st.d2.name1,
                                    st.d2.v,
                                    st.dep_error(),
                                    file=self.debugfile,
                                )

                    if self.debug == True:
                        print("Constraints", file=self.debugfile)
                    for c in self.con_list:
                        if c.active == True:
                            err_sum = err_sum + c.dep_error() ** 2
                            if self.debug == True:
                                print(
                                    c.name1,
                                    c.d1.parent.name1,
                                    c.d1.name1,
                                    c.d1.v,
                                    c.d2.parent.name1,
                                    c.d2.name1,
                                    c.d2.v,
                                    c.dep_error(),
                                    file=self.debugfile,
                                )

                    # if error is worse, we stepped to far
                    # step back
                    ic = 0

                    self.converged.set(True)
                    for d in self.dep_list:
                        if d.active == True and abs(d.dep_error()) > self.tolerance.v:
                            self.converged.set(False)

                    for st in self.state_list:
                        if st.active == True and abs(st.dep_error()) > self.tolerance.v:
                            self.converged.set(False)

                    for c in self.con_list:
                        if c.active == True and abs(c.dep_error()) > self.tolerance.v:
                            self.converged.set(False)

                # except Exception as err:
                # print( f"exception: {err}" )
                # iter = self.maxJacobians
                # g.errors = g.errors + " error during jacbian step\n"

            # check status of the constraints
            self.constraints = False
            for c in self.con_list:
                if c.error_check() and c.active == False:
                    c.dep.active = False
                    c.active = True
                    self.constraints = True

        # if we are here, model is done
        # try:
        self.session.errors = ""
        self.onepass()

        # except:
        # g.errors = g.errors + " error during final model pass\n"
        # pass

        for c in self.session.constraints:
            if c.on == True:
                self.con_list.append(c)
                c.active = False
                c.dep.active = True

        if self.iterCount > self.maxIterations.v - 1:
            self.converged.set(False)
            self.session.errors += " solver exceeded maximu number of iterations\n"
        else:
            self.converged.set(True)

    def trim(self):
        """Trim all states for transient initialization.

        Sets the last state and derivative values to current values
        to prepare for transient simulation start.
        """
        # trim up model
        for st in self.session.states:
            st.trim()

    def save_independents(self):
        """Save current independent variable values for later restoration."""
        for i in self.session.independents:
            i.ind.save = i.ind.v

    def restore_independents(self):
        """Restore independent variable values to their saved state."""
        for i in self.session.independents:
            i.ind.v = i.ind.save

    def pretty(self, output_file):
        """Write solver convergence state to a file.

        Parameters
        ----------
        output_file : file-like
            File-like object to write to.
        """
        output_file.write("Converged:" + str(self.converged.v) + "\n")

    # user wants transient data
    def transrun(self):
        """Run transient simulation by stepping through time.

        Advances simulation time in increments of dtime, solving
        at each step and writing output until timeLast is reached.
        """

        while self.time.v < self.timeLast.v:
            self.time.v = self.time.v + self.dtime.v
            # solve time step
            self.solve()
            # if self.transView != 0:
            print_stdout(self.output_file, self.session)

            # step the elements and states
            for st in self.session.states:
                st.step()
            for e in self.session.elements:
                e.step()

            # print data for this time step

            # print_stdout(self.output_file, self.session)

    def listBalances(self):

        self.numpasses = 0.0
        # get the list of all the solver objects
        self.ind_list = list()
        self.dep_list = list()
        self.state_list = list()
        self.con_list = list()

        print("Independents")
        for i in self.session.independents:
            if i.active == True:
                print(i.name1, i.ind.parent.name, i.ind.name1)

        print("Dependents")
        for d in self.session.dependents:
            if d.active == True:
                print(
                    d.name1,
                    d.d1.parent.name1,
                    d.d1.name1,
                    d.d2.parent.name1,
                    d.d2.name1,
                    d.dep_error(),
                )

        print("States")
        for st in self.session.states:
            if st.active == True:
                print(
                    st.name1,
                    st.d1.parent.name1,
                    st.d1.name1,
                    st.d2.parent.name1,
                    st.d2.name1,
                    st.dep_error(),
                )
        print("Constraints")
        for c in self.session.constraints:
            if c.on == True:
                print(
                    c.name1,
                    c.d1.parent.name1,
                    c.d1.name1,
                    c.d2.parent.name1,
                    c.d2.name1,
                    c.dep_error(),
                )

    def empty(self):

        # get the list of all the solver objects
        self.ind_list = list()
        self.dep_list = list()
        self.state_list = list()
        self.con_list = list()

        for i in self.session.independents:
            i.active = False

        for d in self.session.dependents:
            d.active = False

        for st in self.session.states:
            st.active = False

        for c in self.session.constraints:
            c.on = False
            c.active = False
