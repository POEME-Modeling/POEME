from Atom import Atom

class solver(Atom):
	
  
    def calc(self):
		
		#MIKE SET INDS HERE
        for i in ind_list:
        	print ( i.name )
		
        for e in element_list:
            e.preset
			
        for e in element_list:
            e.calc
            
        #MIKE CHEK DEPS HERE    
        for d in dep_list:
        	print ( d.name )
		