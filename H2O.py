
class H2O:
	def __init__(self):
		pass

	def h_TP( T, P, fract ):
		return T;
		
	def s_TP( T, P, fract ):
		T = T - 460
		return T / 200. * .28
		
	def T_hP( h, P, fract ):
		return h
		
	def T_sP( s, P, fract ):
		return s * 200./.28 + 460
		
		
		
