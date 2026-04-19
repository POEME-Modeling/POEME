from Atom import Atom
from RealT import RealT
from StringT import StringT
from ComplexT import ComplexT
from BooleanT import BooleanT


import g

class State:

    val_1 = 0
    val_2 = 0
    active = True
     
    def __init__( s, p, **kwargs ):
        s.parent = p
        s.type = "State"
        s.name1 = ""
        s.VIDL = list()
        s.val_scale = 0.
        s.__dict__.update(kwargs)        
        
        # Variables
        s.d1name  = StringT( s, v=s.d1name, desc="" )
        s.d1name.name1 = "d1name"
        s.d2name  = StringT( s, v=s.d2name, desc="" )
        s.d2name.name1 = "d2name"
        s.dsname  = StringT( s, v=s.dsname, desc="" )
        s.dsname.name1 = "dsname"
        s.err = RealT( s, desc="Current value of error term" )
        s.errLast = RealT( s, desc="Previous value of error term" )
        s.sname  = StringT( s, v=s.sname, desc="" )
        s.sname.name1 = "sname"     
        s.stateL = RealT( s, desc="Previous value of state value" )        
        s.val_scale = RealT( s, v=s.val_scale, desc="scalar" )

        s.dsL = RealT( s, desc= "" ) 
        
        s.solveState = "";
        s.trans = BooleanT( s, v=False,  desc="determines if the state is in transient or SS mode" )
        if p == 0:
           pass  
        else:
           p.addVID( s )

 
        # add state to the global space
        g.state_list.append( s )
 
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if (eval( "hasattr(self."+name+" ,\"name1\")" )):
            temp = eval( "self."+name )
            if ( temp.name1 == "" ):
                temp.name1 = name
            
    def isa( s, type ):
        if type == "State":
            return True
        else:
            return False
            

    def addVID( s,v ):
        s.VIDL.append(v)
        
    def depError( s ):

        # if we are in steady state mode, just return dep error
        if s.trans.v == False:
            # deterime the appropriate denominator
            denom = max( abs( s.d1.v ), abs( s.d2.v ))
            if s.val_scale.v !=0.:
                denom = s.val_scale.v
            
            if ( denom == 0. ):
                denom = 1.
            
            # calculate and return the error
            s.err.v =(( s.d1.v ) - ( s.d2.v ))/ denom 

            return s.err.v
            
        # if we are in transient mode the error is the difference
        # between the current value of the state
        # and the integrated value of the state using the last time info
        if s.trans.v == True:
            if s.s.v == 0.:
                denom = 1.
            else:
                denom = s.s.v
                
            if s.val_scale.v !=0.:
                denom = s.val_scale.v
                
            #return ( s.s.v - ( s.stateL.v + ( s.ds.v  )/2.*g.NS.dtime.v ))/ denom
            return ( s.s.v - ( s.stateL.v + ( s.ds.v + s.dsL.v )/2.*g.NS.dtime.v ))/ denom
            
    def trim( s ):
        # trim it up by setting last value to current value to start transient
        # done to start transient
        s.stateL.v = s.s.v
        s.dsL.v = 0.
        
    def step( s ):
        # step in time by making current value last value
        s.stateL.v = s.s.v
        s.dsL.v = s.ds.v
    
        
    def precheck( s ):
        
        
        # the dependent d1 value might not be in this element
        # if that is the case, look through all of the elements
        # first block happens if the variable is local      
        try:
            float( s.d1name.v )
            s.d1 = RealT( s,float(d.d1name.v) , "", "" ) 
            
        except ValueError:
            
            tempname = s.d1name.v
            restofname= s.d1name.v
            top = s.parent
        
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
                    s.d1 = v

        # the dependent d2 value might not be in this element
        # if that is the case, look through all of the elements
        # first block happens if the variable is local 
        try:
            float( s.d2name.v )
            s.d2 = RealT( s,v=float( s.d2name.v ) ) 
            
        except ValueError:
            
            tempname = s.d2name.v
            restofname= s.d2name.v
            top = s.parent
        
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
                    s.d2 = v

        # the state value might not be in this element
        # if that is the case, look through all of the elements
        # first block happens if the variable is local 
        try:
            float( s.sname.v )
            s.s = RealT( s, float( s.sname.v ) , "", "" ) 
        except ValueError:
            
            tempname = s.sname.v
            restofname= s.sname.v
            top = s.parent
        
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
                    s.s = v

        # the state value might not be in this element
        # if that is the case, look through all of the elements
        # first block happens if the variable is local 
        try:
            float( s.dsname.v )
            s.ds = RealT( s, float( s.dsname.v ) , "", "" ) 

        except ValueError:
            
            tempname = s.dsname.v
            restofname= s.dsname.v
            top = s.parent
        
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
                    s.ds = v
