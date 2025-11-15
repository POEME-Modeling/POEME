from Atom import Atom
from VID import VID
from RealT import RealT
from RealT import RealT
from ComplexT import ComplexT
import varsg
import __main__

class Element(Atom):
		
    def __init__(self, name, type):
        varsg.element_list.append(self)
        self.VIDL = list() 
        self.type = type
        self.name = name
        self.name1 = name
        self.x = -1.
        self.y = 0.

    def initialList( self ):
    	self.VIDLi = list()
    	for v in self.VIDL:
    		self.VIDLi.append( v )

    def AddIndependent(self, ind):
        self.ind_list.append(ind)
        
    def List(self, type, VIDL):
        if type == RealT:
            for v in VIDL:
                print(v.name)
                
    def Real(value, name, descript):
        variable_id = VID(name, descript, "real")
        self.VIDL.append(variable_id)
        return value
  	    
    def isA(s, type):
        if (type == "Element"):
            return True

            
    def addVID(self,v):
        self.VIDL.append(v)
        
    def preset(s):
        pass
    
    def precheck(s):
    	pass

    def dump(s):
    	pass
    
    def step(s):
    	pass
           
    def before(e):
    	pass
    
    def after(e):
    	pass
    
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if (eval( "hasattr(self."+name+" ,\"name1\")" )):
        	temp = eval( "self."+name )
        	temp.name1 = name

  
    
    def realPrint( self ):
    	for v in self.VIDL:
    		if v.isa( "RealT" ):
    			print( "    ", v.name1, v.v, v.units, v.desc, file=varsg.out )
    		if v.isa( "ComplexT" ):
    			print( "    ", v.name1, v.v, v.units, v.desc, file=varsg.out )
    			
    def hover( self ):
    	temp1 = ""
    	temp1 = self.type + " " + self.name1 + "\n"
    	for v in self.VIDL:
    		if v.isa( "RealT" ):
    			temp1 = temp1 + " " + v.name1+ " " + str( v.v ) +" " + v.units + " "+ v.desc + "\n"
    		if v.isa( "ComplexT" ):
    			temp1 = temp1 +" " + v.name1 + " " + str( v.v ) + " " + v.units + " " + v.desc + "\n"
    	return temp1