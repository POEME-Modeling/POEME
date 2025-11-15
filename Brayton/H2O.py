
class H2O:
	def __init__(self):
		pass

	def h_TP( T, P, fract ):
		return T;
		
	def s_TP( T, P, fract ):
		T = T - 460.
		return T / 200. * .28
		
	def T_hP( h, P, fract ):
		return h
		
	def T_sP( s, P, fract ):
		return s * 200./.28 + 460
		
	def rho( T, P, fract ):
		return 62.424/12.**3.
		
	def Cp( T, P, fract ):
		return 1.;
		
	def mu( T, P, fract ):
		T = T - 460.
		return ( 0.000006342 -0.000037418  )*( T - 32. )/( 200. - 32. ) + 0.000037418
		
	def k( T, P, fract ):
		T = T - 460.
		return (( .3987 - .3211  )*( T - 32. )/( 200. - 32. ) + .3211 )/ 3600.
		