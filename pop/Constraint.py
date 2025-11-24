from Atom import Atom
from RealT import RealT
from ComplexT import ComplexT
from StringT import StringT

import varsg

class Constraint( Atom ):

    
    def __init__( c, p, **kwargs):
        c.d1name = ""
        c.d2name = ""
        c.depname = ""
        c.val_scale = 0.
        c.p = p
        c.on = False
        
        c.type = "Constraint"
        c.name1 = ""
        c.VIDL = list()
        c.active = False
        c.on = False

        c.__dict__.update(kwargs)
           
        # variables
        c.baseError = 0.

        
        c.d1name  = StringT( c, v=c.d1name )
        c.d2name  = StringT( c, v=c.d2name )    
        c.depname  = StringT( c, v=c.depname )
        c.val_scale =  RealT( c, v=c.val_scale )
        c.err =  RealT( c, v=0. )       
        c.errLast =  RealT( c, v=0. )  
        
        # gui location
        c.x = 0
        c.y = 0
        # add constraint to the global list
        varsg.con_list.append( c )
        if p == 0:
           pass  
        else:
           p.addVID( c ) 
           
    def isa( s, type ):
        if type == "Constraint":
            return True
        else:
            return False
            
    def isa( s, type ):
        if type == "Independent":
            return True
        else:
            return False        
    def addVID( c,v ):
        c.VIDL.append( v )
    
    def depError( c ):
        
        # determine the dependent error
        # first see if the user has input a scalar
        denom = max( abs( c.d1.v ), abs(  c.d2.v ))

        if c.val_scale.v !=0.:
            denom = c.val_scale.v
            
        # determine the normalized error
        c.err.v =((c.d1.v) - ( c.d2.v))/denom
        return c.err.v
            
    def errorCheck( c ):
        # check to see if the constraint is active
        denom = max( abs(c.d1.v ), abs( c.d2.v ))
        if ( c.d2.v  > c.d1.v ):
            return True
        else:
            return False 
        
    def precheck( c ):

        # the dependent d1 value might not be in this element
        # if that is the case, look through all of the elements
        # first block happens if the variable is local
        
        for d in varsg.dep_list:
            if( (d.p.name1+"."+d.name1))==c.depname.v:
                c.dep = d
        if c.on == True:
            c.dep.active = True
        c.active = False
        try:
            float(c.d1name.v)
            c.d1 = RealT( d,float(c.d1name.v) , "", "" ) 
        except ValueError:
            
            tempname = c.d1name.v
            restofname= c.d1name.v
            top=c.p
            
            if tempname.find( "." )>-1:
                first = tempname[0:tempname.find(".") ]
                top = 0
                for e in varsg.element_list:
                    if e.name1 == first:
                        top = e 
                       
                if top!=0:
                   second=tempname[tempname.find(".")+1:]
                   if second.find( "." )>-1:
                       third = second[second.find(".")+1:]
                       second = second[0:second.find(".") ]
                      
                       top = c.p
                       for v in top.VIDL:
                           if ( second == v.name1 ):
                               for v2 in v.VIDL: 
                                   if( v2.name1 == third ): 
                                       c.d1=v2
                   else:
                       top=c.p
                       for v in top.VIDL:
                           if ( v.name1==second ):
                               c.d1=v
                else:
                   first=tempname[0:tempname.find(".")]
                   second=tempname[tempname.find(".")+1:]
                   top=c.p
                   for o in top.VIDL:
                       if ( o.name1==first ):
                           for v in o.VIDL:
                               if (v.name1==second):
                                   c.d1 = v
                                   
       
                   if second.find( "." )>-1:
                       third = second[second.find(".")+1:]
                       second = second[0:second.find(".") ]
                       quit()
                       top = c.p
                       for v in top.VIDL:
                           if ( second == v.name1 ):
                               for v2 in v.VIDL:
                                   if( v2.name1 == third ): 
                                      c.d1=v2
                       for v in top.VIDL:
                           if ( second == v.name1 ):
                               c.d1 = v  
               
            else:
                for v in top.VIDL:
                    if tempname == v.name1:
                        c.d1 = v
           
        # the dependent d2 value might not be in this element
        # if that is the case, look through all of the elements
        # first block happens if the variable is local
        
        try:
            float(c.d2name.v)
            c.d2 = RealT( d,float(c.d2name.v) , "", "" ) 
        except ValueError:
            
            tempname = c.d2name.v
            restofname= c.d2name.v
            top=c.p
            
            if tempname.find( "." )>-1:
                first = tempname[0:tempname.find(".") ]
                top = 0
                for e in varsg.element_list:
                    if e.name1 == first:
                        top = e 
                       
                if top!=0:
                   second=tempname[tempname.find(".")+1:]
                   if second.find( "." )>-1:
                       third = second[second.find(".")+1:]
                       second = second[0:second.find(".") ]
                      
                       top = c.p
                       for v in top.VIDL:
                           if ( second == v.name1 ):
                               for v2 in v.VIDL: 
                                   if( v2.name1 == third ): 
                                       c.d2=v2
                   else:
                       top=c.p
                       for v in top.VIDL:
                           if ( v.name1==second ):
                               c.d2=v
                else:
                   first=tempname[0:tempname.find(".")]
                   second=tempname[tempname.find(".")+1:]
                   top=c.p
                   for o in top.VIDL:
                       if ( o.name1==first ):
                           for v in o.VIDL:
                               if (v.name1==second):
                                   c.d2 = v
                                   
       
                   if second.find( "." )>-1:
                       third = second[second.find(".")+1:]
                       second = second[0:second.find(".") ]
                 
                       top = c.p
                       for v in top.VIDL:
                           if ( second == v.name1 ):
                               for v2 in v.VIDL:
                                   if( v2.name1 == third ): 
                                      c.d2=v2
                       for v in top.VIDL:
                           if ( second == v.name1 ):
                               c.d2 = v  
               
            else:
                for v in top.VIDL:
                    if tempname == v.name1:
                        c.d2 = v       
            
            
      

