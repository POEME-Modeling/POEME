class H2O2( Element ):
	
  def __init__(s, name):
  	  super().__init__(name,"H2O2")
  	  s.x = RealT( s, 3., "x", "x variable" )
  	  s.y = RealT( s, 4., "y", "y variable" )
  	  s.a = RealT( s, 4., "a", "a variable" )
  	  s.b = RealT( s, 4., "b", "b variable" )
  	

  def calc(e):
  	  print( "bunghole" )
  	  e.a.v = 1./3.*e.x.v
  	  e.b.v = 3.*e.x.v + e.y.v

