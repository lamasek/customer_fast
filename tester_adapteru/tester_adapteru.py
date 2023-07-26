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
	"curID": '1',
	'cfgs': {
		'1': {
			'GUI': {
				'theme': 'auto', #light, dark, auto, none
			},
			'plots': {
				'theme': 'auto', #light, dark, auto, none
			},
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
				'reqmAstop' : 10000,#mA
				'stop_mV': 1,#V
				'stop_mVAttempts': 3,#attempts
				'time_step_delay': 1000, #ms, musi byt o trochu vetsi nez time_measure_delay
				'time_measure_delay': 800, #ms , jak dlouho ceka mereni po nastaveni proudu - nemelo by byt vetsi nez time_step_delay - cca 100ms
			},
		},
		'2': {
			'GUI': {
				'theme': 'light', #light, dark, auto
			},
			'plots': {
				'theme': 'light', #light, dark, auto
			},
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
				'reqmAstop' : 10000,#mA
				'stop_mV': 1,#V
				'stop_mVAttempts': 3,#attempts
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


CSVDELIM = ', '

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

#verze s .ui
#class MainWindow(QtWidgets.QMainWindow):
#	def __init__(self, *args, **kwargs):
#		super().__init__(*args, **kwargs)
#		uic.loadUi("mainwindow.ui", self)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, *args, obj=None, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setupUi(self)


		#graph
		#self.widget_test_zatizeni_graph
		#self.graphWidget1 = PlotWidget(parent=self.verticalLayoutWidget)

		self.load = load()

		self.mplWidget1.myinit(theme=configCurrent['plots']['theme'])
		self.mplWidget1.plot_init()

		self.test_zatizeni_running = False
		self.pushButton_test_zatizeni_start.pressed.connect(self.test_zatizeni_start)
		self.pushButton_test_zatizeni_stop.pressed.connect(self.test_zatizeni_stop)


		#self.loadReqmAstart = configCurrent['test_adapteru']['reqmAstart']
		#self.loadReqmAstep = configCurrent['test_adapteru']['reqmAstep']
		#self.loadreqmAstop = configCurrent['test_adapteru']['reqmAstop']
		#self.loadstop_mV = configCurrent['test_adapteru']['stop_mV']
		self.loadstop_mVAttempts = configCurrent['test_adapteru']['stop_mVAttempts']
		#self.time_step_delay = configCurrent['test_adapteru']['time_step_delay']
		#self.time_measure_delay = configCurrent['test_adapteru']['time_measure_delay']

		self.spinBox_reqmAstart.setValue(configCurrent['test_adapteru']['reqmAstart'])
		self.spinBox_reqmAstart.valueChanged.connect(self.spinBox_reqmAstart_changed)
		
		self.spinBox_reqmAstop.setValue(configCurrent['test_adapteru']['reqmAstop'])
		self.spinBox_reqmAstop.valueChanged.connect(self.spinBox_reqmAstop_changed)
		
		self.spinBox_reqmAstep.setValue(configCurrent['test_adapteru']['reqmAstep'])
		self.spinBox_reqmAstep.valueChanged.connect(self.spinBox_reqmAstep_changed)
		
		self.spinBox_time_step_delay.setValue(configCurrent['test_adapteru']['time_step_delay'])
		self.spinBox_time_step_delay.valueChanged.connect(self.spinBox_time_step_delay_changed)
		
		self.spinBox_time_measure_delay.setValue(configCurrent['test_adapteru']['time_measure_delay'])
		self.spinBox_time_measure_delay.valueChanged.connect(self.spinBox_time_measure_delay_changed)
		
		self.spinBox_stop_mV.setValue(configCurrent['test_adapteru']['stop_mV'])
		self.spinBox_stop_mV.valueChanged.connect(self.spinBox_stop_mV_changed)
		
		self.spinBox_stop_mVAttempts.setValue(configCurrent['test_adapteru']['stop_mVAttempts'])
		self.spinBox_stop_mVAttempts.valueChanged.connect(self.spinBox_stop_mVAttempts_changed)
		

		#self.penColor = color=(205, 205, 205)
		#self.pen = pg.mkPen(self.penColor, width=1)
		#self.cursor = Qt.CursorShape.CrossCursor
		#print(qwidget_as_canvas1)

		#EXPORTS
		self.export_plainTextEdit1.setPlaceholderText('nothing measured yet...')
		self.export_plainTextEdit1.clear()

	def spinBox_reqmAstart_changed(self, i):
		configCurrent['test_adapteru']['reqmAstart'] = i

	def spinBox_reqmAstop_changed(self, i):
		configCurrent['test_adapteru']['reqmAstop'] = i

	def spinBox_reqmAstep_changed(self, i):
		configCurrent['test_adapteru']['reqmAstep'] = i

	def spinBox_time_step_delay_changed(self, i):
		configCurrent['test_adapteru']['time_step_delay'] = i

	def spinBox_time_measure_delay_changed(self, i):
		configCurrent['test_adapteru']['time_measure_delay'] = i

	def spinBox_stop_mV_changed(self, i):
		configCurrent['test_adapteru']['stop_mV'] = i

	def spinBox_stop_mVAttempts_changed(self, i):
		configCurrent['test_adapteru']['stop_mVAttempts'] = i


	def test_zatizeni_start(self):
		if self.test_zatizeni_running == False:
			self.label_test_zatizeni.setText('init')
			self.label_test_zatizeni.setStyleSheet('')

			global data_loadReqA
			data_loadReqA = []
			global data_loadA
			data_loadA = []
			global data_loadV
			data_loadV = []
			global data_loadW
			data_loadW = []
			self.loadstop_mVAttempts = configCurrent['test_adapteru']['stop_mVAttempts']

			self.mplWidget1.plot_clear()

			if verbose > 100:
				print('Connecting to Load')
			ret = self.load.connect()
			if ret == True:
				self.test_zatizeni_running = True
				self.label_test_zatizeni.setText('Load connected')
				self.label_test_zatizeni.setStyleSheet('color:green')
				self.loadReqmA = 0
				self.load.measure_init()


				self.label_test_zatizeni.setText('Measuring')
				self.label_test_zatizeni.setStyleSheet('color:green')


				#EXPORTS
				self.export_plainTextEdit1.appendPlainText(
					'Requested Current [A]'+CSVDELIM+
					'Measured Current [A]'+CSVDELIM+
					'Measured Voltage [V]'+CSVDELIM+
					'Measured Power [W]'
					)

				# schedule Measuring
				self.timer_test_zatizeni = QtCore.QTimer()
				self.timer_test_zatizeni.setInterval(configCurrent['test_adapteru']['time_step_delay']) # ms
				self.timer_test_zatizeni.timeout.connect(self.test_zatizeni_mereni)
				self.timer_test_zatizeni.start()
			else:
				self.label_test_zatizeni.setText('FAIL to connect Load')
				self.label_test_zatizeni.setStyleSheet('color:red')
		else:
			None

	def test_zatizeni_stop(self):
		if self.test_zatizeni_running == True:
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
		if self.loadReqmA < configCurrent['test_adapteru']['reqmAstop']:
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

			if self.loadReqmA > 0 or configCurrent['test_adapteru']['reqmAstart'] == 0: # next step
				self.loadReqmA += configCurrent['test_adapteru']['reqmAstep']
			else: # we are at zero and we need to skip to reqmAstart
				self.loadReqmA = configCurrent['test_adapteru']['reqmAstart']

			self.mplWidget1.plot_update(data_loadReqA, data_loadA, data_loadV, data_loadW)

			#Update exports
			self.export_plainTextEdit1.appendPlainText(
				str(self.loadReqA)+CSVDELIM+
				str(loadA)+CSVDELIM+
				str(loadV)+CSVDELIM+
				str(loadW)
				)

			# END of measuring?
			if loadV < configCurrent['test_adapteru']['stop_mV']:
				self.loadstop_mVAttempts -= 1
				if verbose > 100:
					print('Measuring - test_zatizeni_mereni - attempts is now:' + str(self.loadstop_mVAttempts))
			if self.loadstop_mVAttempts <= 0:
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
			self.export_plainTextEdit1.appendPlainText('#--------------------------------------')
			self.export_plainTextEdit1.appendPlainText('')



def main():
	global data
	print("Main running...")


	app = QtWidgets.QApplication(sys.argv)

	## Apply dark theme to Qt application
	qdarktheme.setup_theme(configCurrent['GUI']['theme'])

	
	window = MainWindow()

	window.show()
	retcode = app.exec()
	print("Main done, exit...")
	sys.exit(retcode)


if __name__ == "__main__":
	main()