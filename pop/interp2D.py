


def interp2D( x1, x2, x1i, x2i, yi ):
	ix1 = index( x1, x1i )
	ix2 = index( x2, x2i ) 
	
	y00 = yi[ix1][ix2]
	y10 = yi[ix1+1][ix2]
	y01 = yi[ix1][ix2+1]
	y11 = yi[ix1+1][ix2+1]
	yx21 = (x1i[ix1+1]-x1)/(x1i[ix1+1]-x1i[ix1])*y00 + (x1-x1i[ix1])/(x1i[ix1+1]-x1i[ix1])*y10
	yx22 = (x1i[ix1+1]-x1)/(x1i[ix1+1]-x1i[ix1])*y01 + (x1-x1i[ix1])/(x1i[ix1+1]-x1i[ix1])*y11 
	
	return (x2i[ix2+1]-x2)/(x2i[ix2+1]-x2i[ix2])*yx21 + (x2-x2i[ix2])/(x2i[ix2+1]-x2i[ix2])*yx22
	

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



