#global lists the entire model needs

from RealT import RealT
from Newton import Newton

element_list = list()
obs_list = list()
ind_list = list()
dep_list = list()
con_list = list()
state_list = list()
view_list = list()

solver = 0
import os

VIDL = list()
x = 0.
y = 0.
name1 = "varsg"

def __setattr__(self, name, value):
    super().__setattr__(name, value)

    if (eval( "hasattr(self."+name+" ,\"name1\")" )):
        temp = eval( "self."+name )
        temp.name1 = name


solveState = "SS"



out = 0
win=0
w=0
NS = Newton( "varsg.NS" )

errors = "test"

def check():

    
    for e in element_list:
        e.precheck()    
        
    for i in ind_list:
        i.precheck()    
        
    for d in dep_list:
        d.precheck()  
        
    for s in state_list:
        s.precheck()  

    for c in con_list:
        c.precheck()          
            
def set( var, value ):
    
    stuff = element_list.copy()
    stuff.append( NS )
    
    for e in stuff:
        for v in e.VIDL:
            if v.name1 == var:
                v.v =value
            if v.VIDL != 0:
                for v1 in v.VIDL:
                    if v1.name1 == var:
                        v1.v = value
                    try:
                        for v2 in v1.VIDL():
                            if v2.name1 == var:
                                v2.v = value

                    except:
                        pass
                    
               

                    

class stdOut( ):
    
    def print():
        
        print( "time = ", NS.time, file=out )
        print( "Ports*************", file=out )
        print ( "", file=out )
        print( "Electric Ports", file=out )
        for e in element_list:

            for p in e.VIDL:
                if p.isa( "EP" ):
                    p.dump()
                    
        print( "", file=out )
        print( "Fluid Ports", file=out )                    
        for e in element_list:
            for p in e.VIDL:
                if p.isa( "FN" ):
                    p.dump()
                    
        print( "", file=out )                   
        print( "Mech Ports", file=out )
        for e in element_list:
            for p in e.VIDL:
                if p.isa( "MP" ):
                    p.dump()
                    
        print( "", file = out )                 
        print( "Elements***********", file = out )
        print( "", file = out )
                    
        for e in element_list:
            e.dump()
            
class prettyPrint( ):
    
    def print():
        
        print( "******************************************************************************************", file=pretty)
        print( errors, file=pretty )
        print( "time = ", NS.time, file=pretty )
        print( "", file=pretty )
        print( "******************", file=pretty )
        print( "Ports*************", file=pretty )
        print( "******************", file=pretty )
        print( "", file=pretty )
        print( "Electric Ports", file=pretty )
        print( "", file=pretty )
        for e in element_list:
            for p in e.VIDL:
                if p.isa( "EP" ):
                    p.pretty()
                    
        print( "", file=pretty )
        print( "Fluid Ports", file=pretty )
        print( "", file=pretty )
        
        for e in element_list:
            for p in e.VIDL:
                if p.isa( "FN" ):
                    p.pretty()
                    
        print( "", file=pretty )                   
        print( "Mech Ports", file=pretty )
        print( "", file=pretty )
        for e in element_list:
            for p in e.VIDL:
                if p.isa( "MP" ):
                    p.pretty()
             
        print( "", file = pretty )
        print( "*******************", file=pretty )
        print( "Elements***********", file=pretty )
        print( "*******************", file=pretty )
        print( "", file = pretty )
                    
        for e in element_list:
            e.pretty()  
            
        print( "", file=pretty )
        print( "****************", file=pretty )
        print( "Solver**********", file=pretty )
        print( "****************", file=pretty )
        print( "", file=pretty )
        NS.pretty()
        print( "", file=pretty )

class scottPrint( ):
   def print():
      print( "******************** TURBOFAN OUTPUT ********************", file=scottfile)
      print( errors, file=scottfile)
      print( "time = ", NS.time, file=scottfile)
      print( "", file=scottfile)
      print( "******************", file=scottfile)
      print( "Ports*************", file=scottfile)
      print( "******************", file=scottfile)

      for e in element_list:
         for p in e.VIDL:
            if p.isa( "FN" ):
               if p.name1 == 'FNo':
                  print( f"{e.name:12s}", f"{e.FNo.W.v:10.3f}", f"{e.FNo.Pt.v:10.3f}", f"{e.FNo.Tt.v:10.2f}", 
                    f"{e.FNo.ht.v:10.3f}", f"{e.FNo.s.v:10.5f}", f"{e.FNo.FAR.v:10.6f}", f"{e.FNo.rhos.v:10.6f}",
                    f"{e.FNo.MN.v:10.4f}", 
                    f"{e.FNo.Ps.v:10.3f}", f"{e.FNo.Ts.v:10.2f}", f"{e.FNo.A.v:10.3f}", file=scottfile ) 

               if p.name1 == 'FNo1':
                  print( f"{e.name:12s}", f"{e.FNo1.W.v:10.3f}", f"{e.FNo1.Pt.v:10.3f}", f"{e.FNo1.Tt.v:10.2f}", 
                    f"{e.FNo1.ht.v:10.3f}", f"{e.FNo1.s.v:10.5f}", f"{e.FNo1.FAR.v:10.6f}", f"{e.FNo1.rhos.v:10.6f}",
                    f"{e.FNo1.Ps.v:10.3f}", f"{e.FNo1.Ts.v:10.2f}", f"{e.FNo1.A.v:10.3f}", file=scottfile ) 

               if p.name1 == 'FNo2':
                  print( f"{e.name:12s}", f"{e.FNo2.W.v:10.3f}", f"{e.FNo2.Pt.v:10.3f}", f"{e.FNo2.Tt.v:10.2f}", 
                    f"{e.FNo2.ht.v:10.3f}", f"{e.FNo2.s.v:10.5f}", f"{e.FNo2.FAR.v:10.6f}", f"{e.FNo2.rhos.v:10.6f}",
                    f"{e.FNo2.Ps.v:10.3f}", f"{e.FNo2.Ts.v:10.2f}", f"{e.FNo2.A.v:10.3f}", file=scottfile ) 

      
        
os.system( "del pop.out" )
out = open( "pop.out", "a")
os.system( "del pretty.out" )
pretty = open( "pretty.out", "a")