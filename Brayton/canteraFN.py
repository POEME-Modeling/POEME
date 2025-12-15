
from interp3D import interp3D
import numpy as np
import cantera as ct

fuel_comp = {'C': 1.0, 'H':.16667}
oxidizer_comp = {'O2': 0.233, 'N2': 0.767} # Mass fractions for dry air

gas = ct.Solution('gri30.yaml')
gasair = ct.Solution('air.yaml' )

HC = .1667;

class canteraFN:
    gFAR = -1.

    def gam( T, P, FAR, p ):        	
        if FAR < .00001:
            if ( abs( gasair.T - T*5./9 ) > .0001 or abs( gasair.P - P*6894.76) > .0001 or abs( canteraFN.gFAR - FAR ) > .00001 ):
        	    gasair.TP=T*5./9.,P*6894.76
        	    gasair.equilibrate( 'TP' )
            return( gasair.cp/gasair.cv )
        else:
            if ( abs( gas.T - T*5./9 ) > .0001 or abs( gas.P - P*6894.76) > .0001 or abs( canteraFN.gFAR - FAR ) > .00001 ):
        	    gas.set_mixture_fraction(FAR/( 1 - FAR ), fuel=fuel_comp, oxidizer=oxidizer_comp, basis='mass')
        	    gas.TP=T*5./9.,P*6894.76
        	    canteraFN.gFAR = FAR
        	    gas.equilibrate( 'TP' )
            return( gas.cp/gas.cv )
        	
    def rho( T, P, FAR, p ):
        if FAR < .00001:    
            if ( abs( gasair.T - T*5./9 ) > .0001 or abs( gasair.P - P*6894.76) > .0001 or abs( canteraFN.gFAR - FAR ) > .00001 ):
	            gasair.TP=T*5./9.,P*6894.76
	            canteraFN.gFAR = FAR
	            gasair.equilibrate( 'TP' )
            return( gasair.density*0.062428 )                
        else:    
            if ( abs( gas.T - T*5./9 ) > .0001 or abs( gas.P - P*6894.76) > .0001 or abs( canteraFN.gFAR - FAR ) > .00001 ):
	            gas.set_mixture_fraction(FAR/( 1 - FAR ), fuel=fuel_comp, oxidizer=oxidizer_comp, basis='mass')
	            gas.TP=T*5./9.,P*6894.76
	            canteraFN.gFAR = FAR
	            gas.equilibrate( 'TP' )
            return( gas.density*0.062428 )   
                
    def Cp( T, P, FAR, p ):
        if FAR < .00001:    
            if ( abs( gasair.T - T*5./9 ) > .0001 or abs( gasair.P - P*6894.76) > .0001 or abs( canteraFN.gFAR - FAR ) > .00001 ):
	            gasair.TP=T*5./9.,P*6894.76
	            canteraFN.gFAR = FAR
	            gasair.equilibrate( 'TP' )  	
            return( gasair.cp*0.0002390057 )
         	
        else:
            if ( abs( gas.T - T*5./9 ) > .0001 or abs( gas.P - P*6894.76) > .0001 or abs( canteraFN.gFAR - FAR ) > .00001 ):
	            gas.set_mixture_fraction(FAR/( 1 - FAR ), fuel=fuel_comp, oxidizer=oxidizer_comp, basis='mass')
	            gas.TP=T*5./9.,P*6894.76
	            canteraFN.gFAR = FAR
	            gas.equilibrate( 'TP' )
            return( gas.cp*0.0002390057 )
			
    def h_TP( T, P, FAR, p ):
        if FAR < .00001:     
            if ( abs( gasair.T - T*5./9 ) > .0000001 or abs( gasair.P - P*6894.76) > .0001 or abs( canteraFN.gFAR - FAR ) > .00001 ):
	            gasair.TP=T*5./9.,P*6894.76
	            canteraFN.gFAR = FAR
	            gasair.equilibrate( 'TP' ) 
            return( gasair.h*0.0004299226 )
        else:
            if ( abs( gas.T - T*5./9 ) > .0000001 or abs( gas.P - P*6894.76) > .0001 or abs( canteraFN.gFAR - FAR ) > .00001 ):
	            gas.set_mixture_fraction(FAR/( 1 - FAR ), fuel=fuel_comp, oxidizer=oxidizer_comp, basis='mass')
	            gas.TP=T*5./9.,P*6894.76
	            canteraFN.gFAR = FAR
	            gas.equilibrate( 'TP' ) 
            return( gas.h*0.0004299226 )
        
    def s_TP( T, P, FAR, p ):
        if FAR < .00001:
            if ( abs( gasair.T - T*5./9 ) > .0001 or abs( gasair.P - P*6894.76) > .0001 or abs( canteraFN.gFAR - FAR ) > .00001 ):
	            gasair.TP=T*5./9.,P*6894.76
	            canteraFN.gFAR = FAR
	            gasair.equilibrate( 'TP' )

            return( gasair.s*0.0002390057 )
        else:
            if ( abs( gas.T - T*5./9 ) > .0001 or abs( gas.P - P*6894.76) > .0001 or abs( canteraFN.gFAR - FAR ) > .00001 ):
                gas.set_mixture_fraction(FAR/( 1 - FAR ), fuel=fuel_comp, oxidizer=oxidizer_comp, basis='mass')
                gas.TP=T*5./9.,P*6894.76
                canteraFN.gFAR = FAR
                gas.equilibrate( 'TP' ) 
            return( gas.s*0.0002390057 )
        
    def R( T, P, FAR, p ): 
        if FAR < .00001:
            if ( abs( gasair.T - T*5./9 ) > .0001 or abs( gasair.P - P*6894.76) > .0001 or abs( canteraFN.gFAR - FAR ) > .00001 ):
	            gasair.TP=T*5./9.,P*6894.76
	            canteraFN.gFAR = FAR
	            gasair.equilibrate( 'TP' )
            return( 8.314/gasair.mean_molecular_weight*0.0002390057*1000. )
        else:
            if ( abs( gas.T - T*5./9 ) > .0001 or abs( gas.P - P*6894.76) > .0001 or abs( canteraFN.gFAR - FAR ) > .00001 ):
	            gas.set_mixture_fraction(FAR/( 1 - FAR ), fuel=fuel_comp, oxidizer=oxidizer_comp, basis='mass')
	            gas.TP=T*5./9.,P*6894.76
	            canteraFN.gFAR = FAR
	            gas.equilibrate( 'TP' )
            return( 8.314/gas.mean_molecular_weight*0.0002390057*1000. )

    def mu( T, P, FAR, p ):
        return 0
        
    def k( T, P, FAR, p ):
    	return 0
    	
    def T_sP( s, P, FAR, p ):
        if FAR < .00001:
            if (abs( gasair.s - s/0.0002390057 ) > .0001 or abs( gasair.P - P*6894.76) > .0001 or abs( canteraFN.gFAR - FAR ) > .00001 ):
	            gasair.SP=s/0.0002390057,P*6894.76
	            canteraFN.gFAR = FAR
	            gasair.equilibrate( 'SP' )
            return( gasair.T*9./5. )
        else:
            if (abs( gas.s - s/0.0002390057 ) > .0001 or abs( gas.P - P*6894.76) > .0001 or abs( canteraFN.gFAR - FAR ) > .00001 ):
               gas.set_mixture_fraction(FAR/( 1 - FAR ), fuel=fuel_comp, oxidizer=oxidizer_comp, basis='mass')
               gas.SP=s/0.0002390057,P*6894.76
               canteraFN.gFAR = FAR
               gas.equilibrate( 'SP' )    
            return( gas.T*9./5. )
            
    def T_hP( h, P, FAR, p ):
    	T = 1500
    	hcalc = canteraFN.h_TP( T, P, FAR, p )
    	errorm1 = ( hcalc - h )/h
    	xm1 =  T
    	T = T*.95
    	hcalc = canteraFN.h_TP( T, P, FAR, p )    
    	error = ( hcalc - h )/ h
    	x = T
    	
    	while abs( error ) > .000001:
    		xp1 = x - error * (x - xm1 ) / ( error - errorm1 )
    		if xp1 - x > .3*T:
    			xp1 = x + .3*T    			
    		if xp1 - x < -.3*T:
    			xp1 = x - .3*T
    		xm1 = x
    		errorm1 = error
    		x = xp1
    		T = x
    		hcalc = canteraFN.h_TP( T, P, FAR, p )
    		error = ( hcalc - h )/ h
    
    		
    	return T 
 	        
        
    def P_hs( h, S, FAR, P ):
    	T = canteraFN.T_sP( S, P, FAR )

    	hcalc =  canteraFN.h_TP( T, P, FAR, p )
    	errorm1 = ( hcalc - h )/h
    	xm1 =  P
    	P = P*.95
    	T = canteraFN.T_sP( S, P, FAR ) 
    	hcalc =  canteraFN.h_TP( T, P, FAR, p )    	
    	error = ( hcalc - h )/ h
    	x = P
    	
    	while abs( error ) > .000001:
    		xp1 = x - error * (x - xm1 ) / ( error - errorm1 )
    		if xp1 - x > .1*P:
    			xp1 = x + .1*P    			
    		if xp1 - x < -.1*P:
    			xp1 = x - .1*P
    		xm1 = x
    		errorm1 = error
    		x = xp1
    		P = x
    		T = canteraFN.T_sP( S, P, FAR )
    		hcalc =  canteraFN.h_TP( T, P, FAR )
    		error = ( hcalc - h )/ h

    	return P 
 	