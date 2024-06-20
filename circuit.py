from Atom import Atom
from Element import Element
from Inductor import Inductor
from Capacitor import Capacitor
from Resistor import Resistor
from Enode import Enode
from Esource import Esource
from ComplexT import ComplexT
from EP import EP
	
def setFreq( freq, element_list ):
	for e in element_list:
		for v in e.VIDL:
			if v.isa( "EP" ):
				v.freq = freq
		
# port ISTYPE EP
# V ISTYPE Enode				
def linkEV( port, V ):
	V.AddPort(port)
	
	

	
	
	
	