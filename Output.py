from Element import Element
from RealT import RealT
from ComplexT import ComplexT
from EP import EP
from Table1d import Table1d
import varsg

class Output(Element):
    
    def __init__(s,name,filename):
        super().__init__(name,"Output")
        s.name = name
        s.vars = ()
        s.filename = filename
        s.row = 0
        
    def calc(e):
    	pass

    def dump( s ):  
        temp = ""
        if s.row == 0:
        	s.out = open( s.filename, "a")
        	for e in s.vars:
        		temp = temp + " " + e.parent.name + "." + e.name
        	print( temp , file =  s.out )
        temp = ""	
        for e in s.vars:
            temp =  temp + " " + str( e.getVal()) 
        print( temp, file=s.out )
        super().realPrint()
        s.row += 1
  
       
       