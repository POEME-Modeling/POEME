f = "Turbofantest.pop"



out = open( f[:f.index('.')+1]+"py", 'w' )
file = open(f, "r")
start = True
for line in file: 
   
    line = line[:len(line)]
    templine = line.lstrip()
    if ( "RealT" in line ):
        out.write( line )      
    elif ( "=" in line and "(" in line and "\"" in line ) or ( "=" in line and "[" in line ):
        out.write( line )
    else:
        if '=' in templine and not "==" in templine:
            templine = templine[ :templine.index('=')+1] 
        if "." in templine and "=" in templine and start == True and not "==" in templine and not "(" in templine:
            if templine.count('.') == 1 or ".MN" in templine:
                print( "do it" )
                out.write( line[:line.index('=')]+"+"+line[line.index('='):] )
            else:
                out.write( line )
        else:
            out.write( line )