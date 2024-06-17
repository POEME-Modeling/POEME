

exec(open("./Poop.py").read())
exec(open("./circuit.py").read())

class H2O( Element ):
	

  Element.setTy( "H2O" ) 
  
  def __init__(s,name):
  	  super().__init__(name)
  	  s.x = RealT( s, 3., "x", "x variable" )
  	  s.y = RealT( s, 4., "y", "y variable" )
  	  s.a = RealT( s, 4., "a", "a variable" )
  	  s.b = RealT( s, 4., "b", "b variable" )
  	

  def calc(e):
  	  e.a.v = e.x.v + e.y.v
  	  e.b.v = 3*e.x.v - e.y.v



class H2O2( Element ):
	
  Element.setTy( "H2O2" ) 
  
  def __init__(s,name ):
  	  super().__init__(name)
  	  s.x = RealT( s, 3., "x", "x variable" )
  	  s.z = RealT( s, 4., "z", "z variable" )
  	  s.a = RealT( s, 4., "a", "a variable" )
  	  s.b = RealT( s, 4., "b", "b variable" )
  	  s.B = EP( s, "EP", "" )

  	  
  	  
  def calc(e):
  	  e.b.v = 4.*e.x.v + e.z.v

H2 = H2O( "H2" )

O2 = H2O2("H2O2")

Independent( "H2.x", "H2.x.v" )
Dependent( "H2.a", "H2.a.v", 5. )

Independent( "O2.x", "O2.x.v" )
Dependent( "O2.b", "O2.b.v", "4." )

solv = solver()

solv.solve()



