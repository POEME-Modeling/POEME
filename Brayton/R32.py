import CoolProp.CoolProp as CP
from CoolProp.State import State

class R32:              
	
    def rho( T, P, FAR ):
        return CP.PropsSI("D", "T", T*5./9., "P", P*6894.76, "R32")*0.062428
		 
    def Cp( T, P, FAR ):
        #return CP.PropsSI("D", "T", T, "P", P, "R32")
        return 0.

    def k( T, P, FAR ):
        #return CP.PropsSI("D", "T", T, "P", P, "R32")
        return 0.
        
    def mu( T, P, FAR ):
        #return CP.PropsSI("D", "T", T, "P", P, "R32")
        return 0.
        
    def gam( T, P, FAR ):
        #return CP.PropsSI("D", "T", T, "P", P, "R32")
        return 0.
        
    def h_TP( T, P, FAR ):
        return CP.PropsSI("H", "T", T*5./9., "P", P*6894.76, "R32" )*0.4299226  
        
    def T_hP( h, P, FAR ):
        return CP.PropsSI("T", "H", h/0.4299226 , "P", P*6894.76, "R32" )*9./5. 

    def T_sP( s, P, FAR ):
        return CP.PropsSI("T", "S", s/0.2388459, "P", P*6894.76, "R32")*9./5. 
        
    def s_TP( T, P, FAR ):
        return CP.PropsSI("S", "T", T*5./9., "P", P*6894.76, "R32")*0.2388459
        
    def R( T, P, FAR ):
        #return CP.PropsSI("D", "T", T, "P", P*, "R32") 
        return 0.




