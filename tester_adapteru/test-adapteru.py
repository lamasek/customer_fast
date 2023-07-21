#!python3

verbose = 180


# lib_check_install v2
import importlib.util
import pip
def lib_check_install(*packages):
	for p in packages:
		spec = importlib.util.find_spec(p)
		if spec is None:
			print(p +" is not installed, trying to install...")
			pip.main(['install', p])


lib_check_install('pyvisa', 'pyvisa-py')
import pyvisa #pip install pyvisa pyvisa-py

import time

import sys

lib_check_install('pyqtgraph')
#import pyqtgraph as pg #pip install pyqtgraph

lib_check_install('matplotlib')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import (NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

lib_check_install('mplcursors')
import mplcursors

lib_check_install('PyQt6')
from PyQt6 import QtWidgets, uic, QtCore

lib_check_install('pyqtdarktheme')
import qdarktheme ### FIX it by: pip install pyqtdarktheme


from MainWindow import Ui_MainWindow



###### GLOBAL variables - config ####################################################


config = {
	'GUItheme': 'auto', #light, dark, auto
	"curID": '2',
	'cfgs': {
		'1': {
			"load": {
				'type': 'VISA',
				'VISAresource': 'TCPIP0::10.10.134.5::INSTR',
			},
			"wattmeter": {
				'VISAresource': '',
			},
			'test_adapteru': {
				'reqmAstart': 500,#mA
				'reqmAstep': 100,#mA
				'reqmAmax' : 10000,#mA
				'Vmin': 1,#V
				'VminAttempts': 3,#attempts
				'time_step_delay': 1000, #ms, musi byt o trochu vetsi nez time_measure_delay
				'time_measure_delay': 800, #ms , jak dlouho ceka mereni po nastaveni proudu - nemelo by byt vetsi nez time_step_delay - cca 100ms
			},
		},
		'2': {
			"load": {
				'type': 'demo1',
				'VISAresource': '',
			},
			"wattmeter": {
				'VISAresource': '',
			},
			'test_adapteru': {
				'reqmAstart': 500,#mA
				'reqmAstep': 100,#mA
				'reqmAmax' : 10000,#mA
				'Vmin': 1,#V
				'VminAttempts': 3,#attempts
				'time_step_delay': 80, #ms
				'time_measure_delay': 2, #ms , jak dlouho ceka mereni po nastaveni proudu - nemelo by byt vetsi nez time_step_delay - cca 100ms
			},
		},
	},
}

data = { # all measured data
	#item_name : { #item is added when new
	#   data: (value1, value2, ...)
	#   time:   (time1, time2, ...)
	#   graphID: graphID
}
configCurrent = config['cfgs'][config['curID']]

# GLOBAL VARIABLES ##################################################################

# DATA 
data_loadReqA = []
data_loadA = []
data_loadV = []
data_loadW = []

###############################

class load():

	demo_loadReqA = [0.0, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4]
	demo_loadA =  [0.0, 0.500547, 0.600448, 0.699854, 0.799964, 0.899635, 0.99913, 1.099376, 0.0, 1.300171, 1.399442, 1.494956, 1.59529, 1.69556, 1.799899, 1.900312, 2.000822, 2.100236, 2.200443, 2.294846, 2.39518, 2.500621, 2.600104, 2.700486, 2.799766, 2.89998, 3.000602, 3.099993, 3.200127, 0.154693, 0.155484, 0, 0]
	demo_loadV =  [20.110512, 19.90115, 19.857828, 19.818253, 19.779373, 19.736511, 19.692806, 19.652285, 0.000429, 4.552769, 4.509553, 4.466291, 4.425251, 4.38199, 4.337087, 4.293545, 4.250551, 4.207586, 4.164163, 4.123359, 4.079357, 4.033477, 3.990113, 3.945801, 3.902156, 3.857874, 3.815471, 3.769044, 3.724066, 0.186585, 0.000444, 0 , 0]
	demo_loadW =  [0.0, 9.961804, 11.923586, 13.869891, 15.822795, 17.755629, 19.675667, 21.605242, 0.0, 5.919187, 6.310858, 6.676911, 7.059631, 7.429928, 7.806316, 8.159076, 8.504566, 8.836926, 9.163002, 9.462538, 9.770794, 10.086198, 10.374709, 10.655582, 10.925121, 11.187757, 11.448711, 11.683687, 11.917484, 0.028863, 6.9e-05, 0, 0]

	demo_idx = 0

	connected = False

	def connect(self):
		if  configCurrent['load']['type'] == 'demo1':
			self.connected = True
			return(True)
		elif configCurrent['load']['type'] == 'VISA':
			self.rm = pyvisa.ResourceManager()
			print('Connecting to ' + configCurrent['load']['VISAresource'])
			try:
				self.PVload = self.rm.open_resource(configCurrent['load']['VISAresource'])
			except Exception as e:
				print('  Connection failed: ' + str(e))
				self.connected = False
				return(False)

			# Query if instrument is present
			# Prints e.g. "RIGOL TECHNOLOGIES,DL3021,DL3A204800938,00.01.05.00.01"
			print(self.PVload.query("*IDN?"))
			self.connected = True
			#TODO check
			return(True)
		else:
			return(False)

	def disconnect(self):
		print('Load disconnecting...')
		if  configCurrent['load']['type'] == 'demo1':
			self.connected = False
			return(True)
		elif configCurrent['load']['type'] == 'VISA':
			self.rm.close() 
			#TODO check
			self.connected = False
			return(True)
		else:
			return(False)

	def measure_init(self):
		if  configCurrent['load']['type'] == 'demo1':
			self.demo_idx = 0
			return(True)
		elif configCurrent['load']['type'] == 'VISA':
			self.PVload.write(":SOURCE:FUNCTION CURRent")    # Set to  mode CURRent
			self.PVload.write(':SOURCE:CURRent:LEVEL:IMMEDIATE 0') #set load to 0 Amps
			self.PVload.write(":SOURCE:INPUT:STATE On")    # Enable electronic load
			#TODO check
			return(True)
		else:
			return(False)

	def measure(self):
		if  configCurrent['load']['type'] == 'demo1':
			if self.demo_idx < len (self.demo_loadA):
				loadA = self.demo_loadA[self.demo_idx]
				loadV = self.demo_loadV[self.demo_idx]
				loadW = self.demo_loadW[self.demo_idx]
			else:
				loadA = 0
				loadV = 0
				loadW = 0
			self.demo_idx += 1
		elif configCurrent['load']['type'] == 'VISA':
			loadA = float(self.PVload.query(":MEASURE:CURRENT?").strip())
			loadV = float(self.PVload.query(":MEASURE:VOLTAGE?").strip())
			loadW = float(self.PVload.query(":MEASURE:POWER?").strip())
			#TODO check
		else:
			return(False)
		
		if verbose>120:
			print("Current: ", loadA, ', ', end='')
			print("Voltage: ", loadV, ', ', end='')
			print("Power: ", loadW)
		return(loadA, loadV, loadW)


	def measure_finish(self):
		if  configCurrent['load']['type'] == 'demo1':
			None
		elif configCurrent['load']['type'] == 'VISA':
			self.PVload.write(":SOURCE:INPUT:STATE Off")
		else:
			None

	def setCurrent(self, current):
		if  configCurrent['load']['type'] == 'demo1':
			None
		elif configCurrent['load']['type'] == 'VISA':
			PVcommand = ':SOURCE:CURRent:LEVEL:IMMEDIATE ' + str(current)
			if verbose > 100:
				print('PVcommand = '+PVcommand)
			self.PVload.write(PVcommand)
		else:
			None



#pyuic6 mainwindow.ui -o MainWindow.py
#https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_qt_sgskip.html
#https://www.pythonguis.com/tutorials/pyqt6-first-steps-qt-designer/
# https://www.pythonguis.com/tutorials/pyqt6-plotting-matplotlib/
#to delam widget
# FigureCanvasQTAgg
# matplotlib.backends.backend_qtagg

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, *args, obj=None, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setupUi(self)

#verze s .ui
#class MainWindow(QtWidgets.QMainWindow):
#	def __init__(self, *args, **kwargs):
#		super().__init__(*args, **kwargs)
#		uic.loadUi("mainwindow.ui", self)

		#graph
		#self.widget_test_zatizeni_graph
		#self.graphWidget1 = PlotWidget(parent=self.verticalLayoutWidget)

		self.loadReqmAstart = configCurrent['test_adapteru']['reqmAstart']
		self.loadReqmAstep = configCurrent['test_adapteru']['reqmAstep']
		self.loadReqmAmax = configCurrent['test_adapteru']['reqmAmax']
		self.loadVmin = configCurrent['test_adapteru']['Vmin']
		self.loadVminAttempts = configCurrent['test_adapteru']['VminAttempts']
		self.time_step_delay = configCurrent['test_adapteru']['time_step_delay']

		self.load = load()

		self.mplWidget1.plot_init()

		self.test_zatizeni_running = False
		self.pushButton_test_zatizeni.pressed.connect(self.test_zatizeni_start_stop)

		#self.penColor = color=(205, 205, 205)
		#self.pen = pg.mkPen(self.penColor, width=1)
		#self.cursor = Qt.CursorShape.CrossCursor
		#print(qwidget_as_canvas1)


	def test_zatizeni_start_stop(self):
		if self.test_zatizeni_running == False: # START
			self.loadReqmAstart = configCurrent['test_adapteru']['reqmAstart']
			print('Connecting to Load')
			ret = self.load.connect()
			if ret == True:
				self.label_test_zatizeni.setText('Load connected')
				self.label_test_zatizeni.setStyleSheet('color:green')
				self.test_zatizeni_running = True
				self.loadReqmA = 0
				self.load.measure_init()

				global data_loadReqA
				data_loadReqA = []
				global data_loadA
				data_loadA = []
				global data_loadV
				data_loadV = []
				global data_loadW
				data_loadW = []
				self.loadVminAttempts = configCurrent['test_adapteru']['VminAttempts']

				self.mplWidget1.plot_init()
				#self.addToolBar(NavigationToolbar(self.mplWidget1.canvas, self))
				#self.mplWidget1.canvas.axes.clear()
				#self.mplWidget1.canvas.axes.plot([1,2,3,4,5],  [1,2,3,3,2])
				#self.mplWidget1.canvas.draw()


				self.label_test_zatizeni.setText('Measuring')
				self.label_test_zatizeni.setStyleSheet('color:green')

				# schedule Measure!
				self.timer_test_zatizeni = QtCore.QTimer()
				self.timer_test_zatizeni.setInterval(self.time_step_delay) # ms
				self.timer_test_zatizeni.timeout.connect(self.test_zatizeni_mereni)
				self.timer_test_zatizeni.start()
			else:
				self.label_test_zatizeni.setText('FAIL to connect Load')
				self.label_test_zatizeni.setStyleSheet('color:red')
		else: #STOP
			self.test_zatizeni_running = False
			self.timer_test_zatizeni.stop()
			ret = self.load.measure_finish()
			ret = self.load.disconnect()
			if ret:
				self.label_test_zatizeni.setText('User aborted')
				self.label_test_zatizeni.setStyleSheet(None)

			else:
				self.label_test_zatizeni.setText('User aborted, FAIL to disconnect')
				self.label_test_zatizeni.setStyleSheet('color:red')


	def test_zatizeni_mereni(self):
		if verbose >200:
			print('test_zatizeni_mereni()')
		if self.loadReqmA < self.loadReqmAmax:
			self.loadReqA = float(self.loadReqmA/1000)
			if verbose>100:
				print('loadReqA=', self.loadReqA, ', ', end='')
			self.load.setCurrent(self.loadReqA)	
			if verbose>150:
				print('Wait ' + str(configCurrent['test_adapteru']['time_measure_delay']/1000) +'s: ', end='', flush=True)
			time.sleep(configCurrent['test_adapteru']['time_measure_delay']/1000)
			if verbose>150:
				print(' done.')

			loadA, loadV, loadW = self.load.measure()

			data_loadReqA.append(self.loadReqA) 
			data_loadA.append(loadA)
			data_loadV.append(loadV)
			data_loadW.append(loadW)

			self.loadReqmA += self.loadReqmAstep

			self.mplWidget1.plot_update(data_loadReqA, data_loadA, data_loadV, data_loadW)

			if loadV < self.loadVmin:
				self.loadVminAttempts -= 1
			if self.loadVminAttempts < 0:
				self.test_zatizeni_finish()

		else: #finished
			self.test_zatizeni_finish()

	def test_zatizeni_finish(self):
			print('Measurement done...')
			self.label_test_zatizeni.setText('Finished')
			self.label_test_zatizeni.setStyleSheet(None)
			self.test_zatizeni_running = False
			self.load.measure_finish()
			self.load.disconnect()
			self.timer_test_zatizeni.stop()
			# TODO update grafu
			# self.mplWidget1.plotItem.plot(data_loadV)


def main():
	global data
	print("Main running...")


	app = QtWidgets.QApplication(sys.argv)

	## Apply dark theme to Qt application
	qdarktheme.setup_theme(config['GUItheme'])

	
	window = MainWindow()

	window.show()
	retcode = app.exec()
	print("Main done, exit...")
	sys.exit(retcode)


if __name__ == "__main__":
	main()