import math

import numpy as np
from numpy import dot, outer
from scipy import linalg

from .boolean_t import BooleanT
from .element import Element
from .print import print_stdout
from .real_t import RealT
from .session import ModelSession, _active_session


def magnitude(vector):
    return math.sqrt(sum(pow(element, 2) for element in vector))


# No dependents or constraints yet
# Still need to generate independent list from elements
class Newton(Element):
    def __init__(self, name, output_file=None, session: ModelSession | None = None):
        if session is None:
            session = _active_session.get()
        if session is None:
            error_msg = f"Newton {name} requires a session parameter or active "
            "ModelSession context"
            raise ValueError(error_msg)
        self.session = session
        # variables
        self.name1 = name
        # TODO: fix this to use a better default
        self.output_file = (
            output_file if output_file is not None else open("newton.out", "w")
        )
        self.VIDL = list()
        self.ind_list = self.session.independents
        self.dep_list = self.session.dependents
        self.maxJacobians = RealT(
            self, v=50.0, units="Integer", desc="Maxium number of Jacobians"
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
        self.trans = BooleanT(self, v=False, desc="True for transient, false for SS")
        self.converged = BooleanT(self, v=False, desc="converged flag")

        # gui location
        self.x = 0
        self.y = 0

    # define one analysis pass
    def onepass(self):

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
        if self.trans == False:
            self.solve()
        else:
            self.transrun()

    # solve the system
    def solve(self):

        self.numpasses = 0.0
        # get the list of all the solver objects
        self.ind_list = list()
        self.dep_list = list()
        self.state_list = list()
        self.con_list = list()

        for d in self.session.dependents:
            if d.active == True:
                self.dep_list.append(d)

        for i in self.session.independents:
            if i.active == True:
                self.ind_list.append(i)

        for st in self.session.states:
            if st.active == True:
                self.state_list.append(st)

        for c in self.session.constraints:
            if c.on == True:
                self.con_list.append(c)
                c.active = False
                c.dep.active = True

        # create an empty matrix
        matrix = np.zeros(
            (len(self.ind_list), len(self.dep_list) + len(self.state_list))
        )
        
        if( len(self.ind_list) != len(self.dep_list) + len(self.state_list)):
            print( "the number of independents " + str( len(self.ind_list)) + " does not match the number of dependents and states " + str( len(self.dep_list) + len(self.state_list) ) )
            quit()
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

                # invert the matrix
                try:
                    imatrix = linalg.inv(matrix)
                except:  # noqa: E722
                    iter = self.maxJacobians.v
                    self.session.errors += "Could not invert solver matrix\n"
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
                    for i in self.ind_list:
                        delxs[ic] = delx[ic] * iscale
                        i.ind.v = i.ind.v + delxs[ic]
                        ic = ic + 1

                    # try:
                    self.onepass()
                    # except:
                    # iter = self.maxJacobians.v

                    err_sum_last = err_sum
                    err_sum = 0.0

                    for d in self.dep_list:
                        if d.active == True:
                            err_sum = err_sum + d.dep_error() ** 2.0

                    for st in self.state_list:
                        if st.active == True:
                            err_sum = err_sum + st.dep_error() ** 2.0

                    for c in self.con_list:
                        if c.active == True:
                            err_sum = err_sum + c.dep_error() ** 2

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

        if iter > self.maxJacobians.v - 1:
            self.converged.set(False)
            self.session.errors += " solver exceeded maximu number of iterations\n"
        else:
            self.converged.set(True)

    def trim(self):
        # trim up model
        for st in self.session.states:
            st.trim()

    def save_independents(self):
        for i in self.session.independents:
            i.ind.save = i.ind.v

    def restore_independents(self):
        for i in self.session.independents:
            i.ind.v = i.ind.save

    def pretty(self, output_file):
        output_file.write("Converged:" + str(self.converged.v) + "\n")

    # user wants transient data
    def transrun(self):

        while self.time.v < self.timeLast.v:
            self.time.v = self.time.v + self.dtime.v
            # solve time step
            self.solve()
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

        print( "Independents" )
        for i in self.session.independents:
            if i.active == True:
                print( i.name1, i.ind.parent.name, i.ind.name1 )

        print( "Dependents" )
        for d in self.session.dependents:
            if d.active == True:
                print( d.name1, d.d1.parent.name1, d.d1.name1, d.d2.parent.name1, d.d2.name1 )

        print( "States" )                
        for st in self.session.states:
            if st.active == True:
                print( st.name1, st.d1.parent.name1, st.d1.name1, st.d2.parent.name1, d.d2.name1 )
        print( "Constraints" )   
        for c in self.session.constraints:
            if c.on == True:
                print( c.name1, c.d1.parent.name1, c.d1.name1, c.d2.parent.name1, c.d2.name1 )

               

