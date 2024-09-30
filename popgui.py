import numpy as np
import pyqtgraph as pg
from pyqtgraph.flowchart import Flowchart
from pyqtgraph.Qt import QtWidgets
import os




app = pg.mkQApp("Flowchart Example")

## Create main window with grid layout
win = QtWidgets.QMainWindow()
win.setWindowTitle('pyqtgraph example: Flowchart')
cw = QtWidgets.QWidget()
win.setCentralWidget(cw)
layout = QtWidgets.QGridLayout()
cw.setLayout(layout)

 
win.show()



## Create flowchart, define input/output terminals
fc = Flowchart(terminals={
    'dataIn': {'io': 'in'},
    'dataOut': {'io': 'out'}    
})


w = fc.widget()



## Add flowchart control panel to the main window
layout.addWidget(fc.widget(), 0, 0, 2, 1)

exec( open("./LCRNewton.py" ).read())



fc.nodeList =[]
for e in element_list:

	realList = list()
	vars = e.VIDL
	for v in vars:
		realList.append( v )
	fNode = fc.createNode('Pop', e.name, pos=(0, 0))

	fc.nodeList.append( fNode )
	for r in realList:
		if r.isa( "RealT"):
			fNode.ctrls[ r.name ].setValue( eval( e.name+"."+r.name+".v" ))

for n in fc.nodeList:
   
	for t in n.terminals:

		port = eval( n._name+"."+t )
		t = fc.getTerminal(  port.parent.name, port.name )

		o = fc.getTerminal(  port.other.parent.name, port.other.name )

		if t.connectedTo ( o ):
			pass
		else:
			fc.connectTerminals( t, o )
		
btn = QtWidgets.QPushButton('Paste')


varsg.nodeList =  fc.nodeList

w1 = pg.LayoutWidget()


#n.ctrls['R'].setValue(4)		

varsg.out.close()
os.system( "jedit pop.out" )

pg.exec()
