from Atom import Atom
from RealT import RealT
from ComplexT import ComplexT
from StringT import StringT


import varsg

class Dependent( Atom ):

    #def __init__( d, p, d1name, d2name, val_scale, active, desc ):
    def __init__( d, p, **kwargs ):
        d.p = p
        d.name1 = ""
        d.type =  "Dependent"
        d.VIDL = list()

        d.val_scale = 0.
        d.__dict__.update(kwargs)  

		# Variables        
        d.d1name  = StringT( d, v=d.d1name, desc="" )
        d.d1name.name1 = "d1name"
        d.d2name  = StringT( d, v=d.d2name, desc="" )
        d.d2name.name1 = "d2name" 
        d.err = RealT( d, units="", desc="Current error term" )
        d.err.name1 = "err"
        d.errLast = RealT( d, units="", desc="Last error term" )
        d.errLast.name1 = "errLast"
        d.val_scale = RealT( d, v=d.val_scale, units="", desc="Erro scalar" ) 
        d.val_scale.name1 = "val_scale"
        if p == 0:
           pass  
        else:
           p.addVID( d )
        # gui location
        d.x = 0
        d.y = 0

		# add the dependent to the global space
        varsg.dep_list.append( d )

    def isa( s, type ):
        if type == "Dependent":
            return True
        else:
            return False
            
    def addVID( d, v ):
        d.VIDL.append( v )
       
    def depError( d ):
    	
    	# determine the dependent error
    	# first see if the user has input a scalar
    	denom = max( abs( d.d1.v ), abs(  d.d2.v ))

    	if d.val_scale.v !=0.:
    		denom = d.val_scale.v
    		
		# determine the normalized error
    	d.err.v =((d.d1.v) - ( d.d2.v))/denom
    	return d.err.v
    	
    def precheck(d):

		# the dependent d1 value might not be in this element
		# if that is the case, look through all of the elements
		# first block happens if the variable is local
    
    	try:
    		float(d.d1name.v)
    		d.d1 = RealT( d,float(d.d1name.v) , "", "" ) 
    	except ValueError:
  		   	
	    	tempname = d.d1name.v
	    	restofname= d.d1name.v
	    	top = d.p
    	
	    	while tempname.find( "." )>-1:
	    		restofname= tempname[tempname.find(".")+1:]
	    		restofname = tempname
	    		tempname = tempname[0:tempname.find(".") ] 
	    		for v in top.VIDL:
	    			temp =  v.name1

	    			if temp == tempname:
	    				if restofname.find(".")>-1:
	    					top = v
	    				tempname = restofname
    	
	    	restofname=restofname[restofname.find(".")+1:] 
	    	for v in top.VIDL:
	    		if restofname == v.name1:
	    			d.d1 = v

		# the dependent d2 value might not be in this element
		# if that is the case, look through all of the elements
		# first block happens if the variable is local
    	try:
    		float(d.d2name.v)
    		d.d2 = RealT( d,float(d.d2name.v) , "", "" ) 
    	except ValueError:
  		   	
	    	tempname = d.d2name.v
	    	restofname= d.d2name.v
	    	top = d.p
    	
	    	while tempname.find( "." )>-1:
	    		restofname= tempname[tempname.find(".")+1:]
	    		restofname = tempname
	    		tempname = tempname[0:tempname.find(".") ] 
	    		for v in top.VIDL:
	    			temp =  v.name1

	    			if temp == tempname:
	    				if restofname.find(".")>-1:
	    					top = v
	    				tempname = restofname
    	
	    	restofname=restofname[restofname.find(".")+1:] 
	    	for v in top.VIDL:
	    		if restofname == v.name1:
	    			d.d2 = v

				
    	


		
