import CoolProp.CoolProp as CP

fluid = 'R134a'

class CPR134:

    def T_hP( ht, Pt ):
    	return( CP.PropsSI( 'T', 'H', ht*2326., 'P', Pt*6894.76, fluid )*9./5. )

    def h_TP( Tt, Pt ):
    	return( CP.PropsSI( 'H', 'T', Tt*5./9., 'P', Pt*6894.76, fluid )/2326. )

    def h_SP( Tt, Pt ):
    	return( CP.PropsSI( 'H', 'S', S/.0002388 , 'P', Pt*6894.76, fluid )/2326. )

    def h_QP( Q, Pt ):
    	return( CP.PropsSI( 'H', 'Q', Q , 'P', Pt*6894.76, fluid )/2326. )
  
    def Tsat( Pt ):
    	return( CP.PropsSI( "T", "P", Pt*6894.76, "Q", .5, fluid )*9./5. )

    def s_hP( ht, Pt ):
    	return( CP.PropsSI( 'S', 'H', ht*2326., 'P', Pt*6894.76, fluid )*.0002388 )

    def rho( ht, Pt ):
    	return( CP.PropsSI( 'D', 'H', ht*2326., 'P', Pt*6894.76, fluid )*0.0624279606 )   

    def Q( ht, Pt ):
    	return( CP.PropsSI( 'Q', 'H', ht*2326., 'P', Pt*6894.76, fluid ))
