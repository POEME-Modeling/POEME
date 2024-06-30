from Atom import Atom

import Element

import varsg

class solver(Atom):
	
  
    def calc(self):
		
        print("sovler.stuff")
		#MIKE SET INDS HERE
        for i in varsg.ind_list:
            print ( i.name )
            print ( i.variable.v )
     	
        for e in varsg.element_list: 
             e.preset()
		
        for e in varsg.element_list:
             print( e.name )
             e.calc()
            
        #MIKE CHEK DEPS HERE    
        for d in varsg.dep_list:
        	print ( d.name )
		