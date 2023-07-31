#!python3

verbose = 80


# lib_check_install v2 by Josef La Masek ----------------------------
import importlib.util
import pip
def lib_check_install(*packages):
	for p in packages:
		spec = importlib.util.find_spec(p)
		if spec is None:
			print(p +" is not installed, trying to install...")
			pip.main(['install', p])
#--------------------------------------------------------------------

lib_check_install('pyvisa', 'pyvisa-py')
import pyvisa #pip install pyvisa pyvisa-py

import time

import sys

import math

lib_check_install('pyqtgraph')
import pyqtgraph #as pg #pip install pyqtgraph
#from pyqtgraph import mkPen #nefunguje protoze kolize s importem z GUI

lib_check_install('matplotlib')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import (NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

lib_check_install('mplcursors')
import mplcursors

lib_check_install('PyQt6')
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtCore import QCoreApplication, Qt

lib_check_install('pyqtdarktheme')
import qdarktheme ### FIX it by: pip install pyqtdarktheme

#lib_check_install('pprint')
#import pprint

lib_check_install('pyqtconfig')
from pyqtconfig import QSettingsManager


# MS windows only
# 'FIX' the apllication logo in the taskbar 
# sets grouping this script as unique app - not Pythonw.exe with python logo
# see https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
lib_check_install('ctypes')
try:
    import ctypes
    myappid = u'LaMasek.tester_adapteru' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except all:
    pass




from MainWindow import Ui_MainWindow



###### GLOBAL variables - config ####################################################

#config_OLD = {
#			'GUI': {
#				'theme': 'auto', #light, dark, auto, none
#			},
#			'plots': {
#				'theme': 'auto', #light, dark, auto, none


CONFIG_DEFAULT = {
					'GUI/theme': 'auto', #auto, dark, light
					'plots/theme': 'auto',
					'load/VISAresource': 'TCPIP0::10.10.134.5::INSTR',
					'load/demo': False, #if True, demo values are served instead of connecting real Load
					'load/measure_interval': 1000, # ms
					'load/measure_A': True,
					'load/measure_V': True,
					'load/measure_W': True,
					'load/measure_Wh': False,
					'load/measure_X': False,
					'test_adapteru/reqmAstart':  500, # mA
					'test_adapteru/reqmAstep': 100, # mA
					'test_adapteru/reqmAstop': 1000, # mA
					'test_adapteru/stop_mV': 1000, # mV
					'test_adapteru/stop_mVAttempts': 5,
					'test_adapteru/time_step_delay': 1000, #ms, musi byt o trochu vetsi nez time_measure_delay
					'test_adapteru/time_measure_delay': 800,
					'export/CSVDELIM': ', ', #delimiter for export window
				}

# GLOBAL VARIABLES ##################################################################

data = { # all measured data
	#item_name : { #item is added when new
	#   data: (value1, value2, ...)
	#   time:   (time1, time2, ...)
	#   graphID: graphID
}
#configCurrent = config['cfgs'][config['curID']]

data_loadReqA = []
#data_loadReqAtime = []

data_loadA = []
data_loadAtime = []
data_loadV = []
data_loadVtime = []
data_loadW = []
data_loadWtime = []
data_loadAh = []
data_loadAhtime = []
data_loadWh = []
data_loadWhtime = []
data_loadTime = []


###############################

class load():
	def __init__(self, VISAresource):
		self.VISAresource = VISAresource

	demo = False	#f True, it does not connect to real device, it provide fake demo values
	VISAresource = ''
	connected = False

	def setDemo(self, d): #pokud demo, tak dela sinusovku co 10s a jen kladnou
		self.demo = d
	
	def is_connected(self):
		return(self.connected)

	def connect(self):
		if  self.demo == True:
			self.connected = True
			return(True)
		else:
			self.rm = pyvisa.ResourceManager()
			print('Connecting to ' + self.VISAresource)
			try:
				self.PVload = self.rm.open_resource(self.VISAresource)
			except Exception as e:
				print('  Connection failed: ' + str(e))
				self.connected = False
				return(False)

			# Query if instrument is present
			# Prints e.g. "RIGOL TECHNOLOGIES,DL3021,DL3A204800938,00.01.05.00.01"
			IDNreply = self.PVload.query("*IDN?")
			if verbose>50:
				print(IDNreply)
			self.connected = True
			#TODO check
			return(True)

	def disconnect(self):
		print('Load disconnecting...')
		if  self.demo == True:
			self.connected = False
			return(True)
		else:
			self.rm.close() 
			#TODO check
			self.connected = False
			return(True)

	def measure(self, varName):
		if  self.demo == True:
			i = math.sin( # sinus, period 5s in time
					(time.time()%5) / 5 * 2*3.1415
				)
			if i < 0: #only positive part
				i = 0
			return( i )
		else:
			if varName == 'A':
				return(float(self.PVload.query(":MEASURE:CURRENT?").strip()))
			elif varName == 'V':
				return(float(self.PVload.query(":MEASURE:VOLTAGE?").strip()))
			elif varName == 'W':
				return(float(self.PVload.query(":MEASURE:POWER?").strip()))
			elif varName == 'Wh':
				return(float(self.PVload.query(":MEASURE:WATThours?").strip()))
			else:
				return(False)
			

	def setFunctionCurrent(self):
		if  self.demo == True:
			return()

		self.PVload.write(":SOURCE:FUNCTION CURRent")    # Set to  mode CURRent

	def setStateOn(self, state = False): #True = ON, False=OFF
		if self.demo:
			None
			return()
		
		if state:
			self.PVload.write(":SOURCE:INPUT:STATE On")    # Enable electronic load
		else:
			self.PVload.write(":SOURCE:INPUT:STATE Off")

	def setCurrent(self, current):
		if  self.demo == True:
			return()
		else:
			PVcommand = ':SOURCE:CURRent:LEVEL:IMMEDIATE ' + str(current)
			if verbose > 100:
				print('PVcommand = '+PVcommand)
			self.PVload.write(PVcommand)



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

# development environment install
# pip install pyqt6-tools
# pyuic6 -o MainWindow.py mainwindow.ui
# or if something went wrong with PATH, .... you can use:
# python -m PyQt6.uic.pyuic -o output.py -x input.ui



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, *args, obj=None, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setupUi(self)


		QCoreApplication.setOrganizationName("LaMasek")
		QCoreApplication.setOrganizationDomain('lamasek.com')
		QCoreApplication.setApplicationName("tester_adapteru")

		# APP ICONS
		self.setWindowIcon(QtGui.QIcon('images\logo_charger_white.png'))



		# CONFIG ----------------------------
		self.config_plainTextEdit.setPlaceholderText('Config not read yet...')
		self.cfg = QSettingsManager()
		self.cfg.updated.connect(self.config_show)
		self.cfg.set_defaults(CONFIG_DEFAULT)
		self.config_show()
		self.config_pushButton_ClearToDefault.clicked.connect(self.config_set_to_default)

		self.config_comboBox_GUItheme.addItems(('auto', 'dark', 'light'))
		self.cfg.add_handler('GUI/theme', self.config_comboBox_GUItheme)
		self.config_GUItheme_change()
		self.config_comboBox_GUItheme.currentTextChanged.connect(self.config_GUItheme_change)

		#self.config_init()
		self.cfg.add_handler('test_adapteru/reqmAstart', self.spinBox_reqmAstart)
		self.cfg.add_handler('test_adapteru/reqmAstop', self.spinBox_reqmAstop)
		self.cfg.add_handler('test_adapteru/reqmAstep', self.spinBox_reqmAstep)
		self.cfg.add_handler('test_adapteru/time_step_delay', self.spinBox_time_step_delay)
		self.cfg.add_handler('test_adapteru/time_measure_delay', self.spinBox_time_measure_delay)
		self.cfg.add_handler('test_adapteru/stop_mV', self.spinBox_stop_mV)
		self.cfg.add_handler('test_adapteru/stop_mVAttempts', self.spinBox_stop_mVAttempts)
		
		self.loadstop_mVAttempts = self.cfg.get('test_adapteru/stop_mVAttempts')


		# LOAD --------------------
		self.cfg.add_handler('load/VISAresource', self.load_lineEdit_VISAresource)
		self.load = load(self.cfg.get('load/VISAresource'))

		self.load_pushButton_StateON.pressed.connect(self.load_pushButton_StateON_pressed)
		self.load_pushButton_StateOFF.pressed.connect(self.load_pushButton_StateOFF_pressed)
		
		self.load.setDemo(self.cfg.get('load/demo'))
		self.load_pushButton_mereni_start.pressed.connect(self.load_mereni_start)
		self.load_pushButton_mereni_stop.pressed.connect(self.load_mereni_stop)
		self.cfg.add_handler('load/demo', self.load_checkBox_demo)
		self.load_checkBox_demo.stateChanged.connect(self.load_checkBox_demo_changed)
		self.cfg.add_handler('load/measure_interval', self.load_spinBox_measure_interval)
		self.load_pushButton_clearGraphs.pressed.connect(self.load_mereni_clearGraphs)
		self.cfg.add_handler('load/measure_A', self.load_checkBox_measure_A)
		self.load_checkBox_measure_A.stateChanged.connect(self.load_checkBox_measure_A_changed)
		self.load_checkBox_measure_A_changed() # set initial state from config
		self.cfg.add_handler('load/measure_V', self.load_checkBox_measure_V)
		self.load_checkBox_measure_V.stateChanged.connect(self.load_checkBox_measure_V_changed)
		self.load_checkBox_measure_V_changed() # set initial state from config
		self.cfg.add_handler('load/measure_W', self.load_checkBox_measure_W)
		self.load_checkBox_measure_W.stateChanged.connect(self.load_checkBox_measure_W_changed)
		self.load_checkBox_measure_W_changed() # set initial state from config
		self.cfg.add_handler('load/measure_Wh', self.load_checkBox_measure_Wh)
		self.load_checkBox_measure_Wh.stateChanged.connect(self.load_checkBox_measure_Wh_changed)
		self.load_checkBox_measure_Wh_changed() # set initial state from config
		self.cfg.add_handler('load/measure_X', self.load_checkBox_measure_X)
		self.load_checkBox_measure_X.stateChanged.connect(self.load_checkBox_measure_X_changed)
		self.load_checkBox_measure_X_changed() # set initial state from config

		self.load_measuring_finished = True # semaphor for measuring method


		# setup graphs
		self.penColor = color=(205, 205, 205)
		self.pen = pyqtgraph.mkPen(self.penColor, width=1)
		self.cursor = Qt.CursorShape.CrossCursor
      # https://www.geeksforgeeks.org/pyqtgraph-symbols/
		#graphvars = [symbol ='o', symbolSize = 5, symbolBrush =(0, 114, 189)]
		
		self.load_plotWidget1.setMinimumSize(300, 200)
		self.load_plotWidget1.showGrid(x=True, y=True)
		#self.load_plotWidget1.setLimits(yMin=-0.1)
		#self.load_plotWidget2.setRange(yRange=(0,1), disableAutoRange=False)
		#self.load_plotWidget2.setAutoPan(y=True)
		daxis1 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
		self.load_plotWidget1.setAxisItems({"bottom": daxis1})
		self.load_plotWidget1.setLabel('left', 'Current/I [A]')
		self.load_plotWidget1.setCursor(self.cursor)
		self.load_plotWidget1_dataLine =  self.load_plotWidget1.plot([], [],
			'Current [A]', symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=self.pen)

		self.load_plotWidget2.setMinimumSize(300, 200)
		self.load_plotWidget2.showGrid(x=True, y=True)
		daxis2 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
		self.load_plotWidget2.setAxisItems({"bottom": daxis2})
		self.load_plotWidget2_dataLine =  self.load_plotWidget2.plot([], [],
			symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=self.pen)
		self.load_plotWidget2.setLabel('left', 'Voltage/U [V]')

		self.load_plotWidget3.setMinimumSize(300, 200)
		self.load_plotWidget3.showGrid(x=True, y=True)
		daxis3 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
		self.load_plotWidget3.setAxisItems({"bottom": daxis3})
		self.load_plotWidget3_dataLine =  self.load_plotWidget3.plot([], [],
			symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189))
		self.load_plotWidget3.setLabel('left', 'Power/P [W]')

		self.load_plotWidget4.setMinimumSize(300, 200)
		self.load_plotWidget4.showGrid(x=True, y=True)
		daxis4 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
		self.load_plotWidget4.setAxisItems({"bottom": daxis4})
		self.load_plotWidget4_dataLine =  self.load_plotWidget4.plot([], [],
			symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=self.pen)
		self.load_plotWidget4.setLabel('left', 'Capacity [Wh]')

		self.load_plotWidget5.setMinimumSize(300, 200)
		self.load_plotWidget5.showGrid(x=True, y=True)
		daxis5 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
		self.load_plotWidget5.setAxisItems({"bottom": daxis5})
		self.load_plotWidget5_dataLine =  self.load_plotWidget5.plot([], [],
			symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=self.pen)
		self.load_plotWidget5.setLabel('left', '?? [X]')




		# TEST ZATIZENI -----------------------------------
		self.mplWidget1.myinit()
		#self.mplWidget1.myinit(theme=configCurrent['plots']['theme'])
		self.mplWidget1.plot_init()


		self.test_zatizeni_running = False
		self.pushButton_test_zatizeni_start.pressed.connect(self.test_zatizeni_start)
		self.pushButton_test_zatizeni_stop.pressed.connect(self.test_zatizeni_stop)


		#self.penColor = color=(205, 205, 205)
		#self.pen = pg.mkPen(self.penColor, width=1)
		#self.cursor = Qt.CursorShape.CrossCursor
		#print(qwidget_as_canvas1)

		# EXPORTS -----------------------
		self.export_plainTextEdit1.setPlaceholderText('nothing measured yet...')
		self.export_plainTextEdit1.clear()


	def config_show(self):
		self.config_plainTextEdit.clear()
		d = self.cfg.as_dict()
		for key in d:
			self.config_plainTextEdit.appendPlainText(str(key)+': \t'+ str(d[key]))

		self.config_plainTextEdit.appendPlainText('')
		self.config_plainTextEdit.appendPlainText('DEFAULT config: -----------------------')
		d = CONFIG_DEFAULT
		for key in d:
			self.config_plainTextEdit.appendPlainText(str(key)+': \t'+ str(d[key]))

	def config_set_to_default(self):
		for key in CONFIG_DEFAULT:
			self.cfg.set(key, CONFIG_DEFAULT[key])

	def config_GUItheme_change(self):
		try:
			qdarktheme.setup_theme(self.cfg.get('GUI/theme'))
		except:
			None

	# LOAD ------------------------------

	def load_pushButton_StateON_pressed(self):
		if self.load.is_connected() != True:
			return()
		if verbose > 120:
			print('Load State set to ON')
		ret = self.load.setStateOn(True)

	def load_pushButton_StateOFF_pressed(self):
		if self.load.is_connected() != True:
			return()
		if verbose > 120:
			print('Load State set to OFF')
		ret = self.load.setStateOn(False)

	def load_checkBox_demo_changed(self):
		self.load.setDemo(self.cfg.get('load/demo'))

	def load_checkBox_measure_A_changed(self):
		if self.cfg.get('load/measure_A'):
			self.load_plotWidget1.show()
		else:
			self.load_plotWidget1.hide()

	def load_checkBox_measure_V_changed(self):
		if self.cfg.get('load/measure_V'):
			self.load_plotWidget2.show()
		else:
			self.load_plotWidget2.hide()

	def load_checkBox_measure_W_changed(self):
		if self.cfg.get('load/measure_W'):
			self.load_plotWidget3.show()
		else:
			self.load_plotWidget3.hide()

	def load_checkBox_measure_Wh_changed(self):
		if self.cfg.get('load/measure_Wh'):
			self.load_plotWidget4.show()
		else:
			self.load_plotWidget4.hide()

	def load_checkBox_measure_X_changed(self):
		if self.cfg.get('load/measure_X'):
			self.load_plotWidget5.show()
		else:
			self.load_plotWidget5.hide()


	def load_mereni_start(self):
		#self.load.setDemo(self.cfg.get('load/demo'))
		if  self.load.is_connected() == False:
			self.load_label_status.setText('Trying to connect...')
			self.label_test_zatizeni.setStyleSheet('')
			ret = self.load.connect()
			if ret == False:
				self.load_label_status.setText('FAILED to connect Load')
				self.load_label_status.setStyleSheet('color:red')
				return(False)
			else:
				self.load_label_status.setText('Load connected')
				self.load_label_status.setStyleSheet('color:green')
		

		self.label_test_zatizeni.setText('Measuring')
		self.label_test_zatizeni.setStyleSheet('color:green')

		# schedule Measuring
		self.timer_load_mereni = QtCore.QTimer()
		self.timer_load_mereni.setInterval(self.cfg.get('load/measure_interval')) # ms
		self.timer_load_mereni.timeout.connect(self.load_mereni_mereni)
		self.timer_load_mereni.start()


	def load_mereni_stop(self):
		if  self.load.is_connected() == True:
			self.load_label_status.setText('Disconnecting...')
			self.label_test_zatizeni.setStyleSheet(None)
			ret = self.load.disconnect()
			if ret == False:
				self.load_label_status.setText('Disconnected, FAILED to nice disconnect')
				self.load_label_status.setStyleSheet('color:red')
			else:
				self.load_label_status.setText('Disconnected ')
				self.load_label_status.setStyleSheet(None)

		self.load_label_status.setText('Stopped')
		self.load_label_status.setStyleSheet(None)
		self.load.disconnect()

		self.timer_load_mereni.stop()


	def load_mereni_mereni(self):
		if self.load_measuring_finished == False:
			print('load_mereni_mereni-nestiha')
			#return()
		self.load_measuring_finished = False

		global data_loadTime
		tt = time.time()
		data_loadTime.append(tt)


		if self.cfg.get('load/measure_A'):
			global data_loadA
			loadA = self.load.measure('A')
			data_loadA.append(loadA)
			data_loadAtime.append(time.time())
			self.load_plotWidget1_dataLine.setData(data_loadAtime, data_loadA)

		if self.cfg.get('load/measure_V'):
			global data_loadV
			loadV = self.load.measure('V')
			data_loadV.append(loadV)
			data_loadVtime.append(time.time())
			self.load_plotWidget2_dataLine.setData(data_loadVtime, data_loadV)

		if self.cfg.get('load/measure_W'):
			global data_loadW
			loadW = self.load.measure('W')
			data_loadW.append(loadW)
			data_loadWtime.append(time.time())
			self.load_plotWidget3_dataLine.setData(data_loadWtime, data_loadW)

		if self.cfg.get('load/measure_Wh'):
			global data_loadWh
			loadWh = self.load.measure('Wh')
			data_loadWh.append(loadWh)
			data_loadWhtime.append(time.time())
			self.load_plotWidget4_dataLine.setData(data_loadWhtime, data_loadWh)


		#Update exports
		#self.export_plainTextEdit1.appendPlainText(
		#	str(tt)+CSVDELIM+
		#	str(loadA)+CSVDELIM+
		#	str(loadV)+CSVDELIM+
		#	str(loadW)
		#	)
		self.load_measuring_finished = True


	def load_mereni_clearGraphs(self):
		global data_loadA, data_loadAtime
		data_loadA = []
		data_loadAtime = []
		global data_loadV, data_loadVtime
		data_loadV = []
		data_loadVtime = []
		global data_loadW, data_loadWtime
		data_loadW = []
		data_loadWtime = []
		global data_loadWh, data_loadWhtime
		data_loadWh = []
		data_loadWhtime = []

		self.load_plotWidget1_dataLine.setData([], [])
		self.load_plotWidget2_dataLine.setData([], [])
		self.load_plotWidget3_dataLine.setData([], [])
		self.load_plotWidget4_dataLine.setData([], [])
		self.load_plotWidget5_dataLine.setData([], [])


	# TEST_ZATIZENI -----------------------------------------
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
			self.loadstop_mVAttempts = self.cfg.get('test_adapteru/stop_mVAttempts')

			self.mplWidget1.plot_clear()

			if verbose > 100:
				print('Connecting to Load')
			ret = self.load.connect() #connected
			if ret == True:
				self.test_zatizeni_running = True
				self.label_test_zatizeni.setText('Load connected')
				self.label_test_zatizeni.setStyleSheet('color:green')
				self.loadReqmA = 0
				self.load.setFunctionCurrent()
				self.load.setCurrent(0)
				self.load.setStateOn(True)


				self.label_test_zatizeni.setText('Measuring')
				self.label_test_zatizeni.setStyleSheet('color:green')


				#EXPORTS
				self.export_plainTextEdit1.appendPlainText(
					'Requested Current [A]'+self.cfg.get('export/CSVDELIM')+
					'Measured Current [A]'+self.cfg.get('export/CSVDELIM')+
					'Measured Voltage [V]'+self.cfg.get('export/CSVDELIM')+
					'Measured Power [W]'
					)

				# schedule Measuring
				self.timer_test_zatizeni = QtCore.QTimer()
				self.timer_test_zatizeni.setInterval(self.cfg.get('test_adapteru/time_step_delay')) # ms
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
			ret = self.load.setStateOn(False)
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
		if self.loadReqmA < self.cfg.get('test_adapteru/reqmAstop'):
			self.loadReqA = float(self.loadReqmA/1000)
			if verbose>100:
				print('loadReqA=', self.loadReqA, ', ', end='')
			self.load.setCurrent(self.loadReqA)	
			if verbose>150:
				print('Wait ' + str(self.cfg.get('test_adapteru/time_measure_delay')/1000) +'s: ', end='', flush=True)
			time.sleep(self.cfg.get('test_adapteru/time_measure_delay')/1000)
			if verbose>150:
				print(' done.')

			loadA = self.load.measure('A')
			loadV = self.load.measure('V')
			loadW = self.load.measure('W')

			data_loadReqA.append(self.loadReqA) 
			data_loadA.append(loadA)
			data_loadV.append(loadV)
			data_loadW.append(loadW)

			if self.loadReqmA > 0 or self.cfg.get('test_adapteru/reqmAstart') == 0: # next step
				self.loadReqmA += self.cfg.get('test_adapteru/reqmAstep')
			else: # we are at zero and we need to skip to reqmAstart
				self.loadReqmA = self.cfg.get('test_adapteru/reqmAstart')

			self.mplWidget1.plot_update(data_loadReqA, data_loadA, data_loadV, data_loadW)

			#Update exports
			self.export_plainTextEdit1.appendPlainText(
				str(self.loadReqA)+self.cfg.get('export/CSVDELIM')+
				str(loadA)+self.cfg.get('export/CSVDELIM')+
				str(loadV)+self.cfg.get('export/CSVDELIM')+
				str(loadW)
				)

			# END of measuring by V?
			if loadV*1000 < self.cfg.get('test_adapteru/stop_mV'):
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
			self.load.setStateOn(False)
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
	#qdarktheme.setup_theme(configCurrent['GUI']['theme'])

	
	window = MainWindow()

	window.show()
	retcode = app.exec()
	print("Main done, exit...")
	sys.exit(retcode)


if __name__ == "__main__":
	main()