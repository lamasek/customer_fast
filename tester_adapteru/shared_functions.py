#!python3

import pyqtgraph
from pyqtgraph import mkPen

from PyQt6.QtWidgets import*
from PyQt6 import QtCore
from PyQt6.QtGui import QImage, QTextCursor, QPageSize, QPixmap, QPainter, QCloseEvent
from PyQt6.QtCore import QCoreApplication, Qt, QFile, QTextStream, QIODevice, QSemaphore, QByteArray

from pyqtconfig import QSettingsManager


def plot_prepare(cfg: QSettingsManager, plot: pyqtgraph.PlotWidget, labelY: str, addLine2Zero = False, *kwargs):
	'''
	clear and prepare pyqtgraph for plotting data - set ups colors, styles, labels, ....
	
	parameters:
       addLine2Zero        if True it will add data line for invisible data at 0 - to force Auto show 0 at X
    
	config is read from cfg, used items:
       'plots/minWidth'
       'plots/minHeight'
    
	returns:
     line
     or (line0, line)       if addLine2Zero == True
    '''
	
	penColor = color=(205, 205, 205)
	pen = pyqtgraph.mkPen(penColor, width=1)
	cursor = Qt.CursorShape.CrossCursor
	# https://www.geeksforgeeks.org/pyqtgraph-symbols/

	#plot.show()
	plot.clear()
	plot.setMinimumSize(cfg.get('plots/minWidth'), cfg.get('plots/minHeight'))
	#plot1.showGrid(x=True, y=True)
	daxis = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
	plot.setAxisItems({"bottom": daxis})
	plot.setLabel('left', labelY)
	#plot.setCursor(self.cursor)
	plot_dataLine =  plot.plot([], [],
		labelY, symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=pen)
	
    #self.load_plotWidget2.autoRange(item)
    #self.load_plotWidget2.enableAutoRange(x=True, y=True)
    #self.load_plotWidget2.setAutoVisible(x=True, y=True) # Set whether automatic range uses only visible data when determining the range to show.
    #self.load_plotWidget1.setLimits(yMin=-0.1)
    #self.load_plotWidget2.setRange(yRange=(0,1), disableAutoRange=False)
    #self.load_plotWidget2.setAutoPan(y=True)

	if addLine2Zero:
		plot_dataLine0 = plot.plot([], [], symbol='+', symbolSize = 0)
		#plot_dataLine0.setData([time.time()], [0]) #better during 1st measure
		return(plot_dataLine0, plot_dataLine)
	else:
		return(plot_dataLine)
	