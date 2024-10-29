import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel,QVBoxLayout, QWidget
import varsg
from PyQt6 import QtWidgets


class MainWindow1(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("My App")
        
        label = QLabel("Hello, World!")
        self.setCentralWidget(label)
        self.awins = list()

        
    def show_new_window(self,temp,title):
   	   self.awins.append( AnotherWindow(temp,title))
   	   self.awins[len(self.awins)-1].show()
   	   
    def table2d(self,v):
    	
        ix = 0
        iy = 0
        temp = "        "
        for x in v.x:
            temp = temp + str(x) + "  "
            
        temp = temp +"\n"
        
        for x in v.x:
            iy = 0
            temp = temp + str(v.y[ix]) + "  " 
            for y in v.y:
                temp = temp + str( v.data[ix][iy] ) + "  "
                iy = iy + 1
                
            temp = temp + "\n"
            ix = ix + 1
        title =  v.parent.name+"."+v.name             
        self.show_new_window(temp, title)
        
    def table1d(self,v):
		
        temp = ""
        for x in v.x:
            temp = temp + str(x) + "  "
			
        temp = temp +"\n"
		
        for y in v.y:
            temp = temp + str(y) + "  " 
            
        temp =  temp + "\n"
        title =  v.parent.name+"."+v.name  
        self.show_new_window(temp,title)
        
    def deeperWindow( self, v ):
        widget = QtWidgets.QWidget()
        l = QtWidgets.QGridLayout()
        l.setSpacing(0)
        widget.setLayout(l)
        ctrls = {}
        row = 0

        for x in v.VIDL:    
            if x.isa( "RealT" ):
               w = QtWidgets.QDoubleSpinBox()
               w.setMaximum( 1e+99 )
               w.setMinimum( -1e+99 )
               w.setValue( x.v )
               k = x.name
               l.addWidget( w, row, 1 )
               label = QLabel()
               label.setText( k + "  " )
               l.addWidget( label, row, 0 )
               label = QLabel()
               label.setText( "  " + x.units+"  " )
               l.addWidget( label, row, 2 ) 
               label = QLabel()
               label.setText( x.desc )
               l.addWidget( label, row, 3 ) 
          
               ctrls[k] = w
               w.rowNum = row
               row += 1
        title =  v.parent.name+"."+v.name   
        self.awins.append( AnotherWindowDeeper(widget,title,ctrls))
        self.awins[len(self.awins)-1].show()

class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self,temp,title):
        super().__init__()
        layout = QVBoxLayout()
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(200)
        label = QLabel(temp)
        scroll.setWidget( label )
        layout.addWidget(scroll)
        self.setLayout(layout)
        self.setWindowTitle( title )

			
			
class AnotherWindowDeeper(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self,temp,title,ctrls):
        super().__init__()
        layout = QVBoxLayout()
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(200)
        scroll.setWidget( temp )
        layout.addWidget(scroll)
        self.setLayout(layout)
        self.setWindowTitle( title )
        self.ctrls = ctrls
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        