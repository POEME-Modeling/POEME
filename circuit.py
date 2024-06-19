
class ComplexT:
	def __init__( self, p, name, desc ):
		self.c = complex( 0., 0. )
		self.name = name
		self.desc = desc
		
	def isa( self, type ):
		if type == "ComplexT":
			return True
		else:
			return False
			
			
exec( open( "./Element.py" ).read())
exec( open( "./Inductor.py" ).read())
exec( open( "./Capacitor.py" ).read())
exec( open( "./Resistor.py" ).read())
exec( open( "./Enode.py").read())
exec( open("./Esource.py").read())
	
def setFreq( freq ):
	for e in element_list:
		for v in e.VIDL:
			if v.isa( "EP" ):
				v.freq = freq
		

def linkEV( R, V ):
    setattr ( V, R.parent.name,EP(  V, R.parent.name, "" ) )
    temp =  V.name + "."+R.parent.name
    print( temp )
    Port = eval( temp )
    print( Port.name )
    R.other = Port
    Port.other = R
   
    
class EP( Atom ):
	def __init__( self, p, name, desc ):
		self.name = name
		self.desc = desc
		self.parent = p
		self.freq = -1
		self.V = ComplexT( p, "V", "Voltage" )
		self.I = ComplexT( p, "I", "Amperage" )
		p.addVID( self )
	def isa( self, type ):
		if type == "EP":
			return True
		else:
			return False
	def setIV( s, I , V ):
		s.I.c = I
		print( s.I.c )
		s.V.c = V
		s.other.I.c = I
		s.other.V.c = V
		print( "hi" )
		
				
				
		
def link( L1, L2 ):
	L1.other = L2
	L2.other = L1

def Port( P1, name ):
	setattr( P1, name,EP(  P1, "", "" ) )
	

	
	
	
	