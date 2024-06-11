from Atom import Atom
from Element import Element
from RealT import RealT
#from Independent import Independent
#from Dependent import Dependent
#from VID import VID

ElementList = list()
    

class H2O(Element):
    a = ''
    b = ''
    x = ''
    y = ''

    def __init__(self, a, b, x, y):
        self.a = a
        self.b = b
        self.x = x
        self.y = y 

    def Calc(self):
        self.a = self.x + self.y
        self.b = 3*self.x - self.y
    
class H2O2(Element):
    a = ''
    b = ''
    x = ''
    y = ''
  
    def __init__(self, a, b, x, y):
        self.a = a
        self.b = b
        self.x = x
        self.y = y 

    def isA(self, type):
        if(type == "H2O2"):
            return True
        else:
            return Element.isa(type)	

    def Calc(self):
        self.a = 2 * self.x + self.y
        self.b = 4 * self.x + self.y
    
H2 = H2O(0, 0, Element.Real(3, "x", "x variable"), 4)
O2 = H2O2(0, 0, Element.Real(3, "x", "x variable"), Element.Real(4, "y", "y variable"))

x1 = RealT(5, "x1")
x2 = RealT(2, "x2")

x3 = RealT(2000, "x3")

print (x3.desc)

print(x3.desc)

print (x3.var)

print(eval("H2.x.decr"))
H2V = H2.VIDL

for v in H2V:
    print(v.name)


O2.y = 10

class solver(Atom):
    def solve(self):
        for e in ElementList:
            e.calc()

solv = solver()
	
solv.solve()
	
#eval( "H2.calc()" )
#eval( "O2.calc()" )


print(O2.isa("Ato"))