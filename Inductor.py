class Inductor( Element ):

  def __init__(s,name):
  	  super().__init__(name, "Inductor" )
  	  s.L = RealT( s, 0., "L", "Inductance" )  	  
  	  s.dV = ComplexT( s, "dV", "Voltage" )
  	  s.Z = ComplexT( s, "Z", "Impedance" )
  	  s.I = ComplexT( s, "I", "Current" )
  	  s.EPi = EP( s, "EPi", "Inlet Electric Port" )
  	  s.EPo = EP( s, "EPo", "Exit Electric Port" )
      
  def calc(e):
  	  
  	  e.dV.c = e.EPi.V.c - e.EPo.V.c
  	  print( e.EPi.freq )
  	  e.Z.c = complex( 0., 2.*3.14*e.EPi.freq*e.L.v )
  	  e.I.c =  e.dV.c/e.Z.c
  	  e.EPi.setIV ( -e.I.c, 0. )
  	  e.EPo.setIV ( e.I.c, 0. )  	  