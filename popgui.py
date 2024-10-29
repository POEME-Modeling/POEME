import numpy as np
import pyqtgraph as pg
from pyqtgraph.flowchart import Flowchart
from pyqtgraph.Qt import QtWidgets
import os
from MainWindow1 import MainWindow1
import varsg



app = pg.mkQApp("Flowchart Example")

## Create main window with grid layout
varsg.win = QtWidgets.QMainWindow()

varsg.win = MainWindow1()

varsg.win.setWindowTitle('pop')


cw = QtWidgets.QWidget()
varsg.win.setCentralWidget(cw)
layout = QtWidgets.QGridLayout()
cw.setLayout(layout)

 
varsg.win.show()



## Create flowchart, define input/output terminals

fc = Flowchart()
w = fc.widget()



## Add flowchart control panel to the main window
layout.addWidget(fc.widget(), 0, 0, 2, 1)

exec( open("./LCRNewton.py" ).read())




fc.nodeList =[]
x=0
y=0

listStuff = element_list.copy()
listStuff.append( varsg.NS )

for i in varsg.ind_list:
	listStuff.append( i )

for d in varsg.dep_list:
	listStuff.append( d )

for c in varsg.con_list:
	listStuff.append( c )

for e in listStuff:

	realList = list()
	vars = e.VIDL
	for v in vars:
		realList.append( v )
	fNode = fc.createNode('Pop', e.name, pos=(x, y))
	x=x+50
	y=y+10

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
		
#btn = QtWidgets.QPushButton('Paste')


varsg.nodeList =  fc.nodeList
	

varsg.out.close()
os.system( "jedit pop.out" )

pg.exec()
