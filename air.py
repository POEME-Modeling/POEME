from interp3D import interp3D
import numpy as np

class air:
	def __init__(self):
		pass

	def h_TP( T, P, fract ):
		return .24 *( T -518 );

		#return interp3D( fract, P, T, fracti, Pi, Ti, hi ) 

	def s_TP( T, P, fract ):
		s = .24*np.log( T/518. ) -  .06885*np.log( P/ 14.696 )
		return s;
		#return interp3D( fract, P, T, fracti, Pi, Ti, si ) 

	def T_hP( h, P, fract ):
		return h/.24 +518
		#return interp3D( fract, P, h, fracti, Pi, hi, T

	def T_sP( s, P, fract ):
		T  = np.exp( (s + .06885*np.log( P /14.696 )) /.24 )*518.
		return T
        
		#return interp3D( fract, P, s, fracti, Pi, si, Ti )  
		
	def rho( T, P, fract ):
		rho =  P /( .06885 * T )*.000053888*32.*144
		return rho
		#return interp3D( fract, P, T, fracti, Pi, Ti, rhoi )  
		 
	def gam( T, P, fract ):
		gam  = 1.4
		return gam


		#return interp3D( fract, P, T, fracti, Pi, Ti, rhoi )  
		 		

		
	def Cp( T, P, fract ):
		return 1.;
		
	def mu( T, P, fract ):
		T = T - 460.
		return ( 0.000006342 -0.000037418  )*( T - 32. )/( 200. - 32. ) + 0.000037418
		
	def k( T, P, fract ):
		T = T - 460.
		return (( .3987 - .3211  )*( T - 32. )/( 200. - 32. ) + .3211 )/ 3600.

	def R( T, P, fract ):
		return .0685559