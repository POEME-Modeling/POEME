import pyqtgraph as pg
from pyqtgraph.flowchart import Flowchart, Node
import numpy as np

app = pg.mkQApp("Flowchart Example")

## Create a flowchart with a basic set of terminals
fc = Flowchart(terminals={
    'dataIn': {'io': 'in'},
    'dataOut': {'io': 'out'}
})
w = fc.widget()

## Add a few nodes to the flowchart
plot_node = fc.createNode('PlotWidget', pos=(0, 0))
filter_node = fc.createNode('GaussianFilter', pos=(150, 0))

## Connect the nodes
fc.connectTerminals(fc['dataIn'], plot_node['In'])
fc.connectTerminals(plot_node['Out'], filter_node['In'])
fc.connectTerminals(filter_node['Out'], fc['dataOut'])

## Create some noisy data and set it as input
data = np.random.normal(size=1000)
fc.setInput(dataIn=data)

## Show the flowchart
w.show()

if __name__ == '__main__':
    pg.exec()