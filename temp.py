fracti = [ 0, .03, .06 ]
Pi = [ 10., 500., 1000. ]
Ti = [ 10., 500., 1000. ]
hi = [ 
	[ 
		[ 2.25727, 119.585, 241.139 ], 
		[ 3.25727, 120.585, 243.139 ], 
		[ 4.25727, 121.585, 244.139 ], 
	], 
	[ 
		[ 12.25727, 129.585, 251.139 ], 
		[ 13.25727, 130.585, 253.139 ], 
		[ 14.25727, 131.585, 254.139 ], 
    ], 
    [ 
		[ 22.25727, 139.585, 261.139 ], 
		[ 23.25727, 140.585, 263.139 ], 
		[ 24.25727, 141.585, 264.139 ], 
    ] 
]

fract = .037
P = 700.
T =  800.



def interp3D( x1, x2, x3, x1i, x2i, x3i, yi ):
	ix1 = index( x1, x1i )
	ix2 = index( x2, x2i ) 
	ix3 = index( x3, x3i )
	
	y0 = yi[ ix1][ix2][ix3]
	y1 = yi[ ix1][ix2][ix3+1]
	
	yx20 = (x3 - x3i[ix3])/(x3i[ix3+1] -x3i[ix3])*(y1 - y0)+y0
	
	y0 = yi[ ix1][ix2+1][ix3]
	y1 = yi[ ix1][ix2+1][ix3+1]
	
	yx21 = (x3 - x3i[ix3])/(x3i[ix3+1] -x3i[ix3])*(y1 - y0)+y0 
	
	yx10 = (x2 - x2i[ix2])/(x2i[ix2+1] -x2i[ix2])*(yx21 - yx20)+yx20 

	y0 = yi[ ix1+1][ix2][ix3]
	y1 = yi[ ix1+1][ix2][ix3+1]
	
	yx20 = (x3 - x3i[ix3])/(x3i[ix3+1] -x3i[ix3])*(y1 - y0)+y0 

	
	y0 = yi[ ix1+1][ix2+1][ix3]
	y1 = yi[ ix1+1][ix2+1][ix3+1]
	
	yx21 = (x3 - x3i[ix3])/(x3i[ix3+1] -x3i[ix3])*(y1 - y0)+y0 
	yx11 = (x2 - x2i[ix2])/(x2i[ix2+1] -x2i[ix2])*(yx21 - yx20)+yx20
	
	val = (x1 - x1i[ix1])/(x1i[ix1+1] - x1i[ix1])*(yx11 - yx10)+yx10

	return val

def index( x, temp ):
	location = 0
	while len( temp ) > 2:
		lentemp = len( temp )
		i = int( lentemp/2. + 1. ) - 1
		if x > temp[i]:
			temp = temp[i:]
			location = location + int( lentemp/2. + 1. ) - 1
		else:
			temp = temp[:i+1]
	return location


print( interp3D( .037, 700., 800., fracti, Pi, Ti, hi ) )
