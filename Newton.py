from Element import Element

import numpy as np
import varsg
from scipy import linalg
import time

# No dependents or constraints yet
# Still need to generate independent list from elements
class Newton(Element):
   
	def __init__ (s, name):
		s.name = name
		s.ind_list = varsg.ind_list
		s.dep_list = varsg.dep_list
		s.maxJacobians = 10.
		s.tolerance = .0001
		
	def onepass( s ):

		for e in varsg.element_list:
			e.preset()
		for e in varsg.element_list:
			e.calc()         
			
	def solve(s):
		s.ind_list = varsg.ind_list
		s.dep_list = varsg.dep_list
		
		for e in varsg.element_list:
			e.precheck()   		

		matrix = np.zeros( (len( varsg.ind_list), len( varsg.dep_list )))

		iter = 0
		
		converged = False 
		while ( iter < s.maxJacobians and converged == False ):

			iter =  iter+1
			s.onepass()

			
			errSum = 0
			for d in varsg.dep_list:
				d.baseError = d.depError()
				errSum = errSum + d.baseError**2.

			
			icount = 0
			for i in varsg.ind_list:
				dx = i.perturbV()
				i.val.setVal( i.val.getVal() + dx )
				dcount = 0
				s.onepass()
				for d in varsg.dep_list:
					matrix[ icount][dcount ] =( d.depError() - d.baseError )/dx 
					dcount = dcount+1
				i.val.setVal( i.val.getVal() - dx )
			
				icount = icount + 1

			delx = np.zeros( len (varsg.ind_list ))
	
			imatrix = linalg.inv( matrix )
			
			
			
			errSumLast = 9e9
			errSum = 8e9

			while errSum < errSumLast and converged == False:

				ic = 0
				s.onepass()
				for i in varsg.ind_list:
					id = 0
					for d in varsg.dep_list:
						delx[ic] = delx[ic]-imatrix[id][ic]*d.depError()
						id = id + 1
					ic = ic + 1
		
				ic = 0
				scale = 1
				maxdx = 0
				for i in varsg.ind_list:
					scale =  i.val.getVal()
					if i.scale != 0:
						scale = i.scale
					if abs( delx[ic]/scale ) > .1:	
						if maxdx < abs( delx[ic]/ scale ):
							maxdx = abs( delx[ic]/ scale ) 
					ic = ic + 1
	
					
			
				if maxdx != 0:
					scale = .1/ maxdx
				else: 
					scale = 1

				ic = 0
				for i in varsg.ind_list:
					i.val.setVal( i.val.getVal() + scale* delx[ic] )
					ic = ic + 1

 
				s.onepass()

	   


				errSumLast = errSum
				errSum = 0

				for d in varsg.dep_list:

					d.baseError = d.depError()
					errSum = errSum + d.baseError**2.

				
				ic = 0

				if errSum > errSumLast:
					for i in varsg.ind_list:
						i.val.setVal( i.val.getVal() - scale* delx[ic] )
						ic = ic + 1
						

				#time.sleep(4)
				
				converged = True
				for d in varsg.dep_list:
					d.baseError = d.depError()
					if abs( d.depError() ) > s.tolerance:
						converged = False

				
			
  	

		s.onepass()			

	