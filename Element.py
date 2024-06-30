from Atom import Atom
from VID import VID
from RealT import RealT

import varsg



class Element(Atom):
	
	
    VIDL = list()
    ind_list = list()
    
    def __init__(self, name, type):
        varsg.element_list.append(self)
        self.VIDL = list()
        self.type = type
        self.name = name

    def AddIndependent(self, ind):
        self.ind_list.append(ind)
        
    def List(self, type, VIDL):
        if type == RealT:
            for v in VIDL:
                print(v.name)
                
    def Real(value, name, descript):
        variable_id = VID(name, descript, "real")
        Element.VIDL.append(variable_id)
        return value
  	    
    def isA(type):
        if (type == "Element"):
            return True
        else:
            return Atom.isa(type)
            
    def addVID(self,v):
        self.VIDL.append(v)
        
    def preset(s):
        pass
    
    def precheck(s):
    	pass
 
            
            
