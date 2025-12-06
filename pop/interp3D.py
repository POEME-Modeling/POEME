
import varsg

def interp3D( x1, x2, x3, x1i, x2i, x3i, yi, p ):
    ix1 = index( x1, x1i, p )
    ix2 = index( x2, x2i, p ) 
    ix3 = index( x3, x3i, p )
    
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


def index( x, temp, p ):

    if x < temp[0]:
        if p.parent != 0:
            varsg.errors = varsg.errors + p.parent.name1+"."       
        varsg.errors = varsg.errors + p.name1 + " interp 3d input to low " + str( x )+ " < " + str( temp[0] )+"\n"
    if x > temp[ len( temp ) - 1 ]:
        if p.parent != 0:
            varsg.errors = varsg.errors + p.parent.name1+"."          
        varsg.errors = varsg.errors + p.name1 + "interp 3d input to high " + str( x )+ " > " + str( temp[ len( temp )- 1 ] )+"\n"   
    location = 0
    min = 0 
    max = len( temp )
    while max - min > 2:
        lentemp = len( temp )
        i = int( ( max + min ) /2. + 1. ) - 1
        if x > temp[i]:
            min = i
            #location = location + int( lentemp/2. + 1. ) - 1
        else:
            max = i+1
    
    return min
