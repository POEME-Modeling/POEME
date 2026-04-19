from Element import Element

import numpy as np
import g
from scipy import linalg
import time
from numpy import dot, outer
from RealT import RealT
from BooleanT import BooleanT
import math
import time

def magnitude(vector): 
    return math.sqrt(sum(pow(element, 2) for element in vector))
 

# No dependents or constraints yet
# Still need to generate independent list from elements
class Newton(Element):
   
    def __init__ (s, name):
        
        # variables
        s.name1 = name
        s.VIDL = list()
        s.ind_list = g.ind_list
        s.dep_list = g.dep_list
        s.maxJacobians =  RealT( s, v=50., units="Integer", desc="Maxium number of Jacobians" )  
        s.numpasses =  RealT( s, v=0., units="Integer", desc="Number of passes" )  
        s.tolerance = RealT( s, v=.0001, units="real", desc="tolernace" )  
        s.constraints = False
        g.solver = s
        s.type = "NewtonSolver"
        s.time = RealT( s, v=0.,  units="seconds", dessc="Simulation time" )
        s.dtime = RealT( s, v=0.05,  units="seconds", desc="Simulation time step" ) 
        s.timeLast = RealT( s, v=0.05,  units="seconds", desc="Simulation stop time" ) 
        s.trans = BooleanT( s, v=False,  desc="True for transient, false for SS" )
        s.converged = BooleanT( s, v=False,  desc="converged flag" ) 
        
        # gui location
        s.x = 0
        s.y = 0
        
        
    # define one analysis pass
    def onepass( s ):
    
        g.errors = ""
        s.numpasses = s.numpasses + 1
        # run the prepass on all the elements
        for e in g.element_list:
            e.preset()
            
        # run the calculate section for one element
        for e in g.element_list:    
            e.before()
            e.calc()
            e.after()
            
    # run
    def run(s):
        if s.trans == False:
            s.solve()
        else:
            s.transrun()
        
    # solve the system
    def solve(s):
       
        s.numpasses = 0.
        # get the list of all the solver objects
        s.ind_list = list()
        s.dep_list = list()
        s.state_list = list()
        s.con_list = list()
        
        for d in g.dep_list:
            if d.active == True:
                s.dep_list.append( d )

        for i in g.ind_list:
            if i.active == True:
                s.ind_list.append( i )
                  
        for st in g.state_list:
            if st.active == True:
                s.state_list.append( st )
   
        for c in g.con_list:
            if c.on == True:
                s.con_list.append( c )
                c.active = False
                c.dep.active = True

        # create an empty matrix
        matrix = np.zeros( (len( s.ind_list ), len( s.dep_list )+len( s.state_list )))
        delx = np.zeros( len( s.ind_list ))
        delxs = np.zeros( len( s.ind_list ))
        dely = np.zeros( len( s.ind_list ))

        s.constraints = True
        # start working
        while ( s.constraints == True ):
            s.converged.set( False )
            iter = 0
            g.errors = ""
            errSumLast = 9e9
            errSum = 8e9
            while ( iter < s.maxJacobians.v and s.converged == False  ):
                iter = iter + 1
                if ( iter > 1 and len( s.ind_list ) > 1 and errSum < errSumLast ):
                
                    id = 0
                    for d in s.dep_list:
                        if d.active == True:
                            dely[id] =  d.depError() - d.errLast
                            d.errLast.v = d.depError()
                            id = id + 1
                                    
                    for st in s.state_list:
                        if st.active == True:
                            dely[id] =  st.depError() - st.errLast
                            st.errLast.v = st.depError()
                            id = id + 1
                        
                    for c in s.con_list:
                        if c.active == True:
                            dely[id] =  c.depError() - c.errLast                                    
                            c.errLast.v = c.depError()
                            id = id + 1
                            
                    a1 = np.dot(matrix, delxs)
                    a2 = dely
                    a3 = a2 - a1
                    a4 = np.outer(a3, delxs)
                    a5 = np.dot(delxs, delxs)
                    a6 = a4/a5
                    
                    a7 = outer( dely - dot( matrix, delxs ), delxs )/ dot( delxs, delxs )
                    matrix = matrix + a7
                
                    #matrix = matrix + outer( dely - dot( matrix, delxs ), delxs )/ dot( delxs, delxs )
            
                else:       

                    scale = 0
                    # run base point
                    try:
                        s.onepass()
                    except:
                        iter = s.maxJacobians.v

                    errSum = 0
                
                    # check the active dep, states, and cons
                    for d in s.dep_list:
                        if d.active == True:
                            d.baseError = ( d.depError() )
                            errSum = errSum + d.baseError**2.

                    for st in s.state_list:
                        if st.active == True:
                            st.baseError = ( st.depError() )
                            errSum = errSum + st.baseError**2.
                        
                    for c in s.con_list:
                        if c.active == True:
                            c.baseError = ( c.depError() )
                            errSum = errSum + c.baseError**2.
                    
                    icount = 0
                    matrixold = matrix
                
                    # perturb independents and determine response
                    for i in s.ind_list:
                        dx = i.perturbV()
                        # perturb ind
                        i.ind.v = i.ind.v + dx
                        dcount = 0
                        #try:
                        s.onepass()

                        for d in s.dep_list:
                            if d.active == True:
                                matrix[dcount][icount] =( d.depError() - d.baseError )/dx
                                dcount = dcount+1
                            
                        for st in s.state_list:
                            if st.active == True:
                                matrix[dcount][icount] =( st.depError() - st.baseError )/dx
                                dcount = dcount+1
                                    
                        for c in s.con_list:
                            if c.active == True:
                                matrix[ dcount][icount] =( c.depError() - c.baseError )/dx 
                                dcount = dcount+1
                                
                        #except:
                            #iter = s.maxJacobians.v
                            
                        # move independent back
                        i.ind.v = ( i.ind.v - dx )
                        icount = icount + 1

                # invert the matrix
                try:
                    imatrix = linalg.inv( matrix )
                except:
                    iter = s.maxJacobians.v
                    g.errors = g.errors + "Could not invert solver matrix\n"
                bc = 0

                # if the error keeps improving, keep using jacobian
                #while errSum <= errSumLast and s.converged == False:
                check = 0
                while check == 0:
                    #try:

                        check = 1
                    
                        bc =  bc + 1
                        # broyden update
                        
                        
                        ic = 0
                   
                        s.onepass()

 
                 
                        # determine how much to change an independent by
                        # how it affects the deps, etc
                        for i in s.ind_list:
                            id = 0
                            delx[ic]=0
                            for d in s.dep_list:
                                if d.active == True:
                                    d.errLast.v = d.depError()
                                    delx[ic] = delx[ic]-imatrix[ic][id]*d.depError()
                                    id = id + 1
                                
                            for st in s.state_list:
                                if st.active == True:
                                    st.errLast.v = st.depError()
                                    delx[ic] = delx[ic]-imatrix[ic][id]*st.depError()
                                    id = id + 1                     
                        
                            for c in s.con_list:
                                if c.active == True:
                                    c.errLast.v = c.depError()
                                    delx[ic] = delx[ic]-imatrix[ic][id]*c.depError()
                                    id = id + 1
                            ic = ic + 1     
                        
                        # determine a maximum the inds are allowed to step
                        # based on the max value for any ind
                        # all other inds are scaled to this vale
                        ic = 0
                        scale = 1.
                        maxdx = 1.
                        iscale = 1.
                        for i in s.ind_list:
                            if i.ind.v!= 0:
                                scale = i.ind.v
                            if i.scale.v != 0:
                                scale = i.scale.v
                            if abs( delx[ic]/scale ) > .1:
                                if abs( delx[ic] )> abs( .1*scale ):
                                    if iscale > abs( .1*scale/delx[ic] ):
                                        iscale = abs( .1*scale/delx[ic] )
                              
                            ic = ic + 1
                        if iscale == 0:
                            iscale = 1.
                        #iscale = 1.
                        
                        # update the inds
                        # and rerun
                        ic = 0
                        for i in s.ind_list:
                            delxs[ic] = delx[ic]*iscale
                            i.ind.v = ( i.ind.v + delxs[ic] )
                            ic = ic + 1

                        #try:
                        s.onepass()
                        #except:
                            #iter = s.maxJacobians.v
                       
                    

                        errSumLast = errSum
                        errSum = 0.

                        for d in s.dep_list:
                            if d.active == True:
                                errSum = errSum + d.depError()**2.
                                    
                        for st in s.state_list:
                            if st.active == True:
                                errSum = errSum + st.depError()**2.
                        
                        for c in s.con_list:
                            if c.active == True:
                                errSum =  errSum + c.depError()**2
                
                        # if error is worse, we stepped to far
                        # step back
                        ic = 0

                        s.converged.set( True )
                        for d in s.dep_list:
                            if d.active == True:
                                if abs( d.depError() ) > s.tolerance.v:
                                    s.converged.set( False )
                                
                                
                        for st in s.state_list:
                            if st.active == True:
                                if abs( st.depError() ) > s.tolerance.v:
                                    s.converged.set( False )

                                
                        for c in s.con_list:
                            if c.active == True:
                                if abs( c.depError() ) > s.tolerance.v:
                                    s.converged.set( False )

                
                    #except Exception as err:
                        #print( f"exception: {err}" )
                        #iter = s.maxJacobians
                        #g.errors = g.errors + " error during jacbian step\n"
                        
            # check status of the constraints   
            s.constraints = False                           
            for c in s.con_list:
                if c.errorCheck() and c.active == False:
                    c.dep.active = False
                    c.active = True
                    s.constraints =  True  
 
                    
        # if we are here, model is done
        #try:
        g.errors = ""
        s.onepass()
        #except:
            #g.errors = g.errors + " error during final model pass\n"
            #pass
 
        for c in g.con_list:
            if c.on == True:
                s.con_list.append( c )
                c.active = False
                c.dep.active = True        
        
        if iter > s.maxJacobians.v - 1:
            s.converged.set( False )
            g.errors = g.errors + " solver exceeded maximu number of iterations\n"
        else:
            s.converged.set( True )
           
          
    def trim( s ):
        # trim up model
        for st in g.state_list:
            st.trim()   
            
            
    def saveInds( s ):
        for i in g.ind_list:
            i.ind.save = ( i.ind.v )
         
    def restoreInds( s ):
        for i in g.ind_list:
            i.ind.v = ( i.ind.save )

    def pretty( s ):
        print( "Converged:" + str( s.converged.v ), file=g.pretty )
            
    # user wants transient data                         
    def transrun( s ):
            
        while s.time.v < s.timeLast.v:

            s.time.v = s.time.v + s.dtime.v
            # solve time step
            s.solve()
            g.stdOut.print()

            # step the elements and states
            for st in g.state_list:
                st.step()
            for e in g.element_list:
                e.step()
                 
            # print data for this time step
            
            #g.stdOut = open( "pop.out", "a" )
            #g.stdOut.print()
            
        

            
            
