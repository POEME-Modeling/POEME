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
		
	def onepass( s ):
		for e in varsg.element_list:
			e.preset()
		for e in varsg.element_list:
			e.calc()         
			
	def solve(s):
		s.ind_list = varsg.ind_list
		s.dep_list = varsg.dep_list

		matrix = np.zeros( (len( varsg.ind_list), len( varsg.dep_list )))

		iter = 0
		while ( iter < 50 ):
			print()
			print()
			iter =  iter+1
			s.onepass()
			for d in varsg.dep_list:
				d.baseError = d.depError() 



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
			ic = 0
			for i in varsg.ind_list:
				id = 0
				for d in varsg.dep_list:
					delx[ic] = delx[ic]-imatrix[id][ic]*d.baseError
					id = id + 1
				ic = ic + 1
			
			ic = 0
			scale = 1
			maxdx = 0
			for i in varsg.ind_list:
				scale = max( abs( 100 ), abs( i.val.getVal() ))
				if abs( delx[ic]/ scale ) > maxdx:
					maxdx = abs( delx[ic]/ scale )
					ic = ic + 1
				
			
			scale = .1 / maxdx
			print( scale, maxdx )
		    
        
			ic = 0
			for i in varsg.ind_list:
				i.val.setVal( i.val.getVal() + scale* delx[ic] )
				ic = ic + 1
				print( i.val.getVal())
  
			for i in varsg.ind_list:
				print( i.val.getVal() )
				
			print( "ddddddddddddddddd" )
			for d in varsg.dep_list:
				print( d.baseError )
			print( "dddddddddddddddddd" )
			

		s.onepass()			
		for i in varsg.ind_list:
			print( i.val.getVal() )
		print( "ddddddddddddddddd" )
		for d in varsg.dep_list:
			print( d.baseError )
		print( "dddddddddddddddddd" )
	
		quit()
