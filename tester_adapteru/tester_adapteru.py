#!python3

verbose = 80


# lib_check_install v3 by Josef La Masek ----------------------------
import importlib.util
import subprocess
import sys
import pip
def lib_check_install(MODULEname, PACKAGEname=None): 
	#
	# check if module MODULEname is avalable for include, if not, it try to install it via pip
	# if MODname name is different than package name, you have to provide PACKAGEname too
	#
	#  if there is package which is not able to include, use (MODULEname=None, PACKAGENAME)
	#
	# useful especially when you dont have package for your soft, but need to install it on more computers
	#
	#
	# examples:
	#
	# lib_check_install('pyvisa')
	# import pyvisa
	#
	# lib_check_install(None, 'pyvisa-py')
	#
	# lib_check_install('qdarktheme', 'pyqtdarktheme')
	# import qdarktheme


	if PACKAGEname == None:
		PACKAGEname = MODULEname

	if MODULEname is not None:
		spec = importlib.util.find_spec(MODULEname)
		if spec is not None:
			return()
		print(MODULEname + ' is not import able, trying to install PKG ' + PACKAGEname)
	else: # non importable package is checked via pip
		reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
		installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
		if PACKAGEname.lower() in map(str.lower, installed_packages):
			return()
		print(PACKAGEname + ' is not installed, trying to install...')
		
	try:
		subprocess.check_call([sys.executable, '-m', 'pip', 'install', PACKAGEname])
	except:
		None
	#pip.main(['install', p]) # old deprecated way
#--------------------------------------------------------------------

lib_check_install('io')
import io

lib_check_install('pyvisa')
import pyvisa #pip install pyvisa pyvisa-py

lib_check_install(None, 'pyvisa-py')

import time

lib_check_install('datetime')
from datetime import datetime, timezone

import sys

import math

lib_check_install('matplotlib')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import (NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

lib_check_install('mplcursors')
import mplcursors

lib_check_install('PyQt6')
from PyQt6 import QtWidgets, uic, QtCore, QtGui, QtTest


from PyQt6.QtCore import QCoreApplication, Qt, QFile, QTextStream, QIODevice, QSemaphore

lib_check_install('qdarktheme', 'pyqtdarktheme')
import qdarktheme ### FIX it by: pip install pyqtdarktheme
#https://pyqtdarktheme.readthedocs.io/en/v1.0.2/how_to_use.html

lib_check_install('darkdetect')
import darkdetect ### FIX it by: pip install darkdetect

#lib_check_install('pprint')
#import pprint

lib_check_install('pyqtconfig')
from pyqtconfig import QSettingsManager

lib_check_install('pyqtgraph')
import pyqtgraph # pip install pyqtgraph
from pyqtgraph import mkPen


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

CONFIG_DEFAULT = {
					'GUI/theme': 'auto', #auto, dark, light
					'plots/theme': 'auto',
					'VISA/VISAresource': 'TCPIP0::10.10.134.5::INSTR',
					'VISA/demo': False,
					'VISA/SCPIcommand' : '*IDN?',
					'wattmeter/VISAresource' : 'TCPIP0::10.10.134.6::INSTR',
					'wattmeter/measure_interval' : 1000, #ms
					'wattmeter/demo' : False,
					'wattmeter/measure_W': True,
					'wattmeter/measure_A': True,
					'wattmeter/measure_V': True,
					'wattmeter/measure_MATH': True,
					'load/VISAresource': 'TCPIP0::10.10.134.5::INSTR',
					'load/demo': False, #if True, demo values are served instead of connecting real Load
					'load/measure_interval': 1000, # ms
					'load/measure_A': True,
					'load/measure_V': True,
					'load/measure_W': True,
					'load/measure_Wh': False,
					'load/measure_X': False,
					'testACDCadapteru/Po':  1, #W
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

data_wattmeter_W = []
data_wattmeter_Wtime = []
data_wattmeter_A = []
data_wattmeter_Atime = []
data_wattmeter_V = []
data_wattmeter_Vtime = []
data_wattmeter_MATH = []
data_wattmeter_MATHtime = []

data_test_zatizeni_ReqA = []
data_test_zatizeni_A = []
data_test_zatizeni_V = []
data_test_zatizeni_W = []


###############################
class VisaDevice():
	
	def __init__(self, VISAresource: str, demo: bool):
		self. VISAresource = VISAresource
		self.demo = demo

	demo = False	# if True, it does not connect to real device, it provide fake demo values
	#demo_connected = False
	
	def setDemo(self, d: bool): #pokud demo, tak dela sinusovku co 10s a jen kladnou
		self.demo = d
	

	VISAresource = ''
	connected = False

	def is_connected(self):
		return(self.connected)
	
	def setVISAresource(self, Vr: str):
		self.VISAresource = Vr

	def connect(self):
		# return retCode=True/False, retString=Error str/IDN of device
		if  self.demo == True:
			self.connected = True
			return(True, 'Demo connected')

		if self.connected:
			return(True, 'Already connected')
		self.rm = pyvisa.ResourceManager()
		if verbose > 70:
			print('Connecting to ' + self.VISAresource)
		try:
			self.PVdevice = self.rm.open_resource(self.VISAresource)
		except Exception as e:
			print('  Connection failed: ' + str(e))
			self.connected = False
			return(False, ' Connection failed'+str(e))

		# Query if instrument is present
		# Prints e.g. "RIGOL TECHNOLOGIES,DL3021,DL3A204800938,00.01.05.00.01"
		try:
			IDNreply = self.PVdevice.query("*IDN?")
		except Exception as e:
			print('SCPI *IDN? test after connection failed: ' + str(e))
			self.connected = False
			return(False, 'SCPI *IDN? test after connection failed: '+str(e))
		if verbose>50:
			print(IDNreply.strip())
		self.connected = True
		return(True, IDNreply)

	def disconnect(self):
		if  self.demo == True:
			self.connected = False
			return(True)

		if verbose > 70:
			print('Load disconnecting...')
		self.rm.close() 
		#TODO check
		self.connected = False
		return(True)

	def send(self, commandi):
		if  self.connected == True:
			command = commandi.strip()
			if command =='':
				return(False, 'Empty command, nothing to send...') # we have to handle itself, some devices (e.g. Rigol DL3031A) freezes permanently after emty command
			try:
				if verbose>70:
					print('Command:' + command)
				if '?' in command: # some devices (e.g. Yokogawa WT310E) have some IDs after ? (e.g. ":NUM:VAL? 1")
					reply = self.PVdevice.query(command)
				else:
					self.PVdevice.write(command)
					reply = ''
				if verbose>150:
					print(reply)
				return(True, reply)
			except Exception as e:
				if verbose > 50:
					print('  Comand "' + command + '" failed: ' + str(e))
				return(False, str(e))
		else:
			return(False, 'Not connected')

	def write(self, commandi):
		if  self.demo == True:
			return(True, 'Demo')
		if  self.connected == True:
			command = commandi.strip()
			if command =='':
				return(False, 'Empty command, nothing to send...') # we have to handle itself, some devices (e.g. Rigol DL3031A) freezes permanently after emty command
			try:
				if verbose>70:
					print('Command:' + command)
				reply = self.PVdevice.write(command)
				if verbose>50:
					print(reply)
				return(True, reply)
			except Exception as e:
				if verbose > 50:
					print('  Comand "' + command + '" failed: ' + str(e))
				return(False, str(e))
		else:
			return(False, 'Not connected')

	def query(self, commandi):
		#return(retCode = True/False, retString)
		if  self.demo == True:
			return(True, 'Demo')

		if  self.connected == True:
			command = commandi.strip()
			if command =='':
				return(False, 'Empty command, nothing to send...') # we have to handle itself, some devices (e.g. Rigol DL3031A) freezes permanently after emty command
			try:
				if verbose>70:
					print('Command:' + command)
				reply = self.PVdevice.query(command)
				if verbose>50:
					print(reply)
				return(True, reply)
			except Exception as e:
				if verbose > 70:
					print('  Comand "' + command + '" failed: ' + str(e))
				return(False, str(e))
		else:
			return(False, 'Not connected')


class Load(VisaDevice):

	def measure(self, varName):
		if  self.demo == True:
			i = math.sin( # sinus, period 5s in time
					(time.time()%5) / 5 * 2*3.1415
				)
			if i < 0: #only positive part
				i = 0
			return( i )
		else:
			global verbose
			verbose -= 100
			if varName == 'A':
				retCode, retString = VisaDevice.query(self, ":MEASURE:CURRENT?")
				verbose += 100
				return(float(retString.strip()))
			elif varName == 'V':
				retCode, retString = VisaDevice.query(self, ":MEASURE:VOLTAGE?")
				verbose += 100
				return(float(retString.strip()))
			elif varName == 'W':
				retCode, retString = VisaDevice.query(self, ":MEASURE:POWER?")
				verbose += 100
				return(float(retString.strip()))
			elif varName == 'Wh':
				retCode, retString = VisaDevice.query(self, ":MEASURE:WATThours?")
				verbose += 100
				return(float(retString.strip()))
			else:
				return(False)
			

	def setFunctionCurrent(self):
		if  self.demo == True:
			return()
		VisaDevice.write(self, ":SOURCE:FUNCTION CURRent")    # Set to  mode CURRent

	def setModeBATT(self):
		if  self.demo == True:
			return()
		VisaDevice.write(self, ":SOUR:FUNC:MODE BATT")    # Set to  mode BATTery


	def setStateOn(self, state = False): #True = ON, False=OFF
		if self.demo == True:
			return()
		
		if state  == True:
			return(VisaDevice.write(self, ":SOURCE:INPUT:STATE On"))    # Enable electronic load
		else:
			return(VisaDevice.write(self, ":SOURCE:INPUT:STATE Off"))

	def setCurrent(self, current):
		if  self.demo == True:
			return()
		else:
			PVcommand = ':SOURCE:CURRent:LEVEL:IMMEDIATE ' + str(current)
			if verbose > 100:
				print('PVcommand = '+PVcommand)
			VisaDevice.write(self, PVcommand)


class Wattmeter(VisaDevice):

	def connect(self):
		r, s = VisaDevice.connect(self)
		if r == False:
			return(r, s)
		if self.demo == True:
			return(r, s)
		VisaDevice.write(self, ':NUM:FORM ASCII')
		#todo check ze je ok

		#todo check ze:
		#:integ?
		#kontrolovat ze to je spravne na NORM;0,10,0

		return(r, s)
		#self.connected = True

	def measure(self, varName):
		global verbose
		verbose -= 100
		# ;ITEM1 MATH;ITEM2 TIME;ITEM3 U,1;ITEM4 I,1;ITEM5 P,1;ITEM6 S,1;ITEM7 Q,1;ITEM8 LAMB,1;ITEM9 PHI,1;ITEM10 FU,1;ITEM11 UTHD,1;ITEM12 ITHD,1;ITEM13 LAMB,1;ITEM14 PHI,1;ITEM15 F
		if varName == 'MATH':
			retCode, retString = VisaDevice.query(self, ":NUM:VAL? 1")
			verbose += 100
			return(float(retString.strip()))
		elif varName == 'V':
			retCode, retString = VisaDevice.query(self, ":NUM:VAL? 3")
			verbose += 100
			return(float(retString.strip()))
		elif varName == 'A':
			retCode, retString = VisaDevice.query(self, ":NUM:VAL? 4")
			verbose += 100
			return(float(retString.strip()))
		elif varName == 'W':
			retCode, retString = VisaDevice.query(self, ":NUM:VAL? 5")
			verbose += 100
			return(float(retString.strip()))
		else:
			return(False)

	def integrateStart(self):
		return(VisaDevice.write(self, ":INTEGrate:STARt"))

	def integrateCheck(self):
		retCode, retString = VisaDevice.query(self, ":MEASURE:WATThours?")


class TestACDCadapteru():
	data1 = []
	data2 = []
	semaphore = QSemaphore(0) # semafor na testy:
			# 0 	test is not running
			# 1		test is running
			# 2 	do exit from test (e.g. button pressed)

	#def nice_exit(self):
	#	self.semaphore.tryAcquire(1)

	def do_measure(	self,
			wmeter: Wattmeter,
			load: Load, 
			exportTextEdit: QtWidgets.QTextEdit, 
			plot1: pyqtgraph.PlotWidget, 
			plot2: pyqtgraph.PlotWidget,
			statusLabel: QtWidgets.QLabel,
			):
		statusLabel.setText('Started')
		exportTextEdit.insertHtml('<H1>Test AC/DC adaptéru</H1><BR></BR>')
		now  = datetime.now()
		now_utc = datetime.now(timezone.utc)
		exportTextEdit.insertHtml('<P>Datum: ' + now_utc.isoformat() + '</P><BR></BR>')
		if verbose > 150:
			print('TestACDCadapteru-->do_measure Test started')

		if load.is_connected() == False:
			retCode, retString = load.connect()
			if not retCode:
				statusLabel.setText('Failed to connect Load')
				self.semaphore.tryAcquire(1)
				return(False)
		rc, rs = load.query('*IDN?')
		exportTextEdit.insertHtml('<P>Load IDN: ' + rs + '</P><BR></BR>')


		if wmeter.is_connected() == False:
			retCode, retString = wmeter.connect()
			if not retCode:
				statusLabel.setText('Failed to connect Wattmeter')
				self.semaphore.tryAcquire(1)
				return(False)
		rc, rs = wmeter.query('*IDN?')
		exportTextEdit.insertHtml('<P>Wattmeter IDN: ' + rs + '</P><BR></BR>')

		#region Pstb ------------------------------------------------------------------------------------
		exportTextEdit.insertHtml('<H2>Standby příkon adaptéru - Pstb</H2><BR></BR>')
		exportTextEdit.insertHtml('<P>Měří se 10 minutový průměr příkonu adaptéru bez zátěže - Pstb.</P><BR></BR>')

		load.setStateOn(False)


		#endregion
		if self.semaphore.available() > 1: #stop the test and exit
			if verbose > 150:
				print('TestACDCadapteru-->do_measure Test stopped')
			statusLabel.setText('Stopped')
			return()


		while self.semaphore.available() == 1:
			print(time.time())
			QtTest.QTest.qWait(1000)
			#return by finished
		
		#finished by user stop
		self.semaphore.tryAcquire(2)
		statusLabel.setText('Stopped')
		if verbose > 150:
			print('TestACDCadapteru-->do_measure Test stopped')

	
	

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
# python -m PyQt6.uic.pyuic -o MainWindow.py -x mainwindow.ui


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, *args, obj=None, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setupUi(self)

		QCoreApplication.setOrganizationName("LaMasek")
		QCoreApplication.setOrganizationDomain('lamasek.com')
		QCoreApplication.setApplicationName("tester_adapteru")

		# APP ICONS
		qiconlogo = QtGui.QIcon('images\logo_charger_white.png')
		self.setWindowIcon(qiconlogo)

		self.stop = False  #stop semaphore for running tests

		# for all pyqt graphs in this app:
		self.penColor = color=(205, 205, 205)
		self.pen = pyqtgraph.mkPen(self.penColor, width=1)
		self.cursor = Qt.CursorShape.CrossCursor
		plotMinW = 300
		plotMinH = 150
      # https://www.geeksforgeeks.org/pyqtgraph-symbols/
		#graphvars = [symbol ='o', symbolSize = 5, symbolBrush =(0, 114, 189)]


		#region CONFIG ----------------------------
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
		#endregion

		#region VISA ------------------------------------------------------------------------
		self.visa = VisaDevice(
			VISAresource=self.cfg.get('VISA/VISAresource')
			, demo = self.cfg.get('VISA/demo'))
		self.cfg.add_handler('VISA/VISAresource', self.visa_lineEdit_VISAresource)
		self.visa_lineEdit_VISAresource.textChanged.connect(self.visa_VISAresource_changed)
		self.visa_pushButton_connect.pressed.connect(self.visa_connect)
		self.visa_pushButton_disconnect.pressed.connect(self.visa_disconnect)
		self.cfg.add_handler('VISA/SCPIcommand', self.visa_lineEdit_SCPIcommand)
		self.visa_lineEdit_SCPIcommand.returnPressed.connect(self.visa_send)
		self.visa_pushButton_send.pressed.connect(self.visa_send)
		#endregion


		# CONSOLE -------------------------------------------------------------------


		#region WATTMETER -----------------------------------------------------------------
		self.wattmeter = Wattmeter(
			VISAresource=self.cfg.get('wattmeter/VISAresource'),
			demo=self.cfg.get('wattmeter/demo')
		)
		self.cfg.add_handler('wattmeter/VISAresource', self.wattmeter_lineEdit_VISAresource)
		self.wattmeter_lineEdit_VISAresource.textChanged.connect(self.wattmeter_VISAresource_changed)
		self.cfg.add_handler('wattmeter/demo', self.wattmeter_checkBox_demo)
		self.wattmeter_checkBox_demo.stateChanged.connect(self.wattmeter_demo_pressed)
		self.wattmeter_pushButton_connect.pressed.connect(self.wattmeter_connect)
		self.wattmeter_pushButton_disconnect.pressed.connect(self.wattmeter_disconnect)

		# Wattmeter Measure
		self.wattmeter_mereni_finished = True # semaphor for measuring method
		self.wattmeter_pushButton_start.pressed.connect(self.wattmeter_mereni_start)
		self.wattmeter_pushButton_stop.pressed.connect(self.wattmeter_mereni_stop)
		self.cfg.add_handler('wattmeter/measure_interval', self.wattmeter_spinBox_measure_interval)
		self.wattmeter_pushButton_clearGraphs.pressed.connect(self.wattmeter_mereni_clearGraphs)

		self.cfg.add_handler('wattmeter/measure_W', self.wattmeter_checkBox_measure_W)
		self.wattmeter_checkBox_measure_W.stateChanged.connect(self.wattmeter_checkBox_measure_W_changed)
		self.wattmeter_checkBox_measure_W_changed() # set initial state from config
		self.cfg.add_handler('wattmeter/measure_A', self.wattmeter_checkBox_measure_A)
		self.wattmeter_checkBox_measure_A.stateChanged.connect(self.wattmeter_checkBox_measure_A_changed)
		self.wattmeter_checkBox_measure_A_changed() # set initial state from config
		self.cfg.add_handler('wattmeter/measure_V', self.wattmeter_checkBox_measure_V)
		self.wattmeter_checkBox_measure_V.stateChanged.connect(self.wattmeter_checkBox_measure_V_changed)
		self.wattmeter_checkBox_measure_V_changed() # set initial state from config
		self.cfg.add_handler('wattmeter/measure_MATH', self.wattmeter_checkBox_measure_MATH)
		self.wattmeter_checkBox_measure_MATH.stateChanged.connect(self.wattmeter_checkBox_measure_MATH_changed)
		self.wattmeter_checkBox_measure_MATH_changed() # set initial state from config

		# setup Wattmeter graphs
		# plotWidget1 / W
		self.wattmeter_plotWidget1.setMinimumSize(plotMinW, plotMinH)
		self.wattmeter_plotWidget1.showGrid(x=True, y=True)
		wattmeter_daxis1 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
		self.wattmeter_plotWidget1.setAxisItems({"bottom": wattmeter_daxis1})
		self.wattmeter_plotWidget1.setLabel('left', 'Power/P [W]')
		self.wattmeter_plotWidget1.setCursor(self.cursor)
		self.wattmeter_plotWidget1_dataLine =  self.wattmeter_plotWidget1.plot([], [],
			'Power/P [W]', symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=self.pen)
		# plotWidget2 / A
		self.wattmeter_plotWidget2.setMinimumSize(plotMinW, plotMinH)
		self.wattmeter_plotWidget2.showGrid(x=True, y=True)
		wattmeter_daxis1 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
		self.wattmeter_plotWidget2.setAxisItems({"bottom": wattmeter_daxis1})
		self.wattmeter_plotWidget2.setLabel('left', 'Current/I [A]')
		self.wattmeter_plotWidget2.setCursor(self.cursor)
		self.wattmeter_plotWidget2_dataLine =  self.wattmeter_plotWidget2.plot([], [],
			'Current/I [A]', symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=self.pen)
		# plotWidget3 / U
		self.wattmeter_plotWidget3.setMinimumSize(plotMinW, plotMinH)
		self.wattmeter_plotWidget3.showGrid(x=True, y=True)
		wattmeter_daxis1 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
		self.wattmeter_plotWidget3.setAxisItems({"bottom": wattmeter_daxis1})
		self.wattmeter_plotWidget3.setLabel('left', 'Voltage/U [V]')
		self.wattmeter_plotWidget3.setCursor(self.cursor)
		self.wattmeter_plotWidget3_dataLine =  self.wattmeter_plotWidget3.plot([], [],
			'Voltage/U [V]', symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=self.pen)
		# plotWidget4 / MATH
		self.wattmeter_plotWidget4.setMinimumSize(plotMinW, plotMinH)
		self.wattmeter_plotWidget4.showGrid(x=True, y=True)
		wattmeter_daxis1 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
		self.wattmeter_plotWidget4.setAxisItems({"bottom": wattmeter_daxis1})
		self.wattmeter_plotWidget4.setLabel('left', 'AVG Power 10 min./P [W]')
		self.wattmeter_plotWidget4.setCursor(self.cursor)
		self.wattmeter_plotWidget4_dataLine =  self.wattmeter_plotWidget4.plot([], [],
			'AVG Power 19 min./P [W]', symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=self.pen)
		#endregion

		#region LOAD -----------------------------------------------------
		self.load = Load(
			VISAresource=self.cfg.get('load/VISAresource'),
			demo=self.cfg.get('load/demo')
		)
		self.cfg.add_handler('load/VISAresource', self.load_lineEdit_VISAresource)
		self.load_lineEdit_VISAresource.textChanged.connect(self.load_VISAresource_changed)
		self.cfg.add_handler('load/demo', self.load_checkBox_demo)
		self.load_checkBox_demo.stateChanged.connect(self.load_demo_pressed)
		self.load_pushButton_connect.pressed.connect(self.load_connect)
		self.load_pushButton_disconnect.pressed.connect(self.load_disconnect)
		self.load_pushButton_StateON.pressed.connect(self.load_pushButton_StateON_pressed)
		self.load_pushButton_StateOFF.pressed.connect(self.load_pushButton_StateOFF_pressed)
		
		# LOAD Rem. Ctrl.
		self.load_radioButton_Mode_CC.pressed.connect(self.load.setFunctionCurrent)
		self.load_radioButton_Mode_BATT.pressed.connect(self.load.setModeBATT)
		self.load_doubleSpinBox_BATT_current.valueChanged.connect(self.load_doubleSpinBox_BATT_current_changed)
		self.load_radioButton_BATT_range_6A.pressed.connect( self.load_radioButton_BATT_range_6A_connect )
		self.load_radioButton_BATT_range_60A.pressed.connect(self.load_radioButton_BATT_range_60A_connect)
		self.load_doubleSpinBox_BATT_vstop.valueChanged.connect(self.load_doubleSpinBox_BATT_vstop_changed)

		# LOAD Measure
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

		self.load_mereni_finished = True # semaphor for measuring method


		# setup Load graphs
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
		self.load_plotWidget2.setCursor(self.cursor)
		#self.load_plotWidget2.autoRange(item)
		#self.load_plotWidget2.enableAutoRange(x=True, y=True)
		#self.load_plotWidget2.setAutoVisible(x=True, y=True) # Set whether automatic range uses only visible data when determining the range to show.


		self.load_plotWidget3.setMinimumSize(300, 200)
		self.load_plotWidget3.showGrid(x=True, y=True)
		daxis3 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
		self.load_plotWidget3.setAxisItems({"bottom": daxis3})
		self.load_plotWidget3_dataLine =  self.load_plotWidget3.plot([], [],
			symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189))
		self.load_plotWidget3.setLabel('left', 'Power/P [W]')
		self.load_plotWidget3.setCursor(self.cursor)

		self.load_plotWidget4.setMinimumSize(300, 200)
		self.load_plotWidget4.showGrid(x=True, y=True)
		daxis4 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
		self.load_plotWidget4.setAxisItems({"bottom": daxis4})
		self.load_plotWidget4_dataLine =  self.load_plotWidget4.plot([], [],
			symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=self.pen)
		self.load_plotWidget4.setLabel('left', 'Capacity [Wh]')
		self.load_plotWidget4.setCursor(self.cursor)

		self.load_plotWidget5.setMinimumSize(300, 200)
		self.load_plotWidget5.showGrid(x=True, y=True)
		daxis5 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
		self.load_plotWidget5.setAxisItems({"bottom": daxis5})
		self.load_plotWidget5_dataLine =  self.load_plotWidget5.plot([], [],
			symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=self.pen)
		self.load_plotWidget5.setLabel('left', '?? [X]')
		self.load_plotWidget5.setCursor(self.cursor)
		#endregion


		#region testACDCadapteru ----------------------------------------------
		self.testACDCadapteru = TestACDCadapteru()
			

		self.testACDCadapteru_pushButton_start.pressed.connect(self.testACDCadapteru_start)
		self.testACDCadapteru_pushButton_stop.pressed.connect(self.testACDCadapteru_stop)
		#endregion


		#region TEST ZATIZENI -----------------------------------
		self.mplWidget1.myinit()
		#self.mplWidget1.myinit(theme=configCurrent['plots']['theme'])
		self.mplWidget1.plot_init()

		self.test_zatizeni_running = False
		self.pushButton_test_zatizeni_start.pressed.connect(self.test_zatizeni_start)
		self.pushButton_test_zatizeni_stop.pressed.connect(self.test_zatizeni_stop)
		#endregion

		#region EXPORTS -----------------------
		self.export_textEdit1.setPlaceholderText('nothing measured yet...')
		self.export_textEdit1.clear()
		self.export_pushButton_clear.pressed.connect(self.export_textEdit1.clear)
		#endregion

		# COMMENTS -------------------------------
		self.cfg.add_handler('comments/text', self.comments_plainTextEdit)


		#region HELP -----------------------------------------------------
		f = io.open("help/help.html", mode="r", encoding="utf-8")
		#f.open(QIODevice.ReadOnly | QIODevice.Text)
		#f.open(QFile.ReadOnly | QFile.Text)
		#f.open()
		#istream = QTextStream(f)
		str = ''
		for x in f:
			str += x
		self.help_textEdit.setHtml(str)
		#endregion 



	#region CONFIG ------------------------------------------------
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
		theme = self.cfg.get('GUI/theme')
		try:
			qdarktheme.setup_theme(theme)
		except:
			None
		try:
			if theme == 'auto':
				if darkdetect.isDark():
					theme = 'dark'
				else:
					theme = 'light'
			if theme == 'light':
				self.wattmeter_plotWidget1.setBackground("w")
				self.wattmeter_plotWidget2.setBackground("w")
				self.wattmeter_plotWidget3.setBackground("w")
				self.wattmeter_plotWidget4.setBackground("w")
				self.load_plotWidget1.setBackground("w")
				self.load_plotWidget2.setBackground("w")
				self.load_plotWidget3.setBackground("w")
				self.load_plotWidget4.setBackground("w")
				self.load_plotWidget5.setBackground("w")
			else:
				self.wattmeter_plotWidget1.setBackground("k")
				self.wattmeter_plotWidget2.setBackground("k")
				self.wattmeter_plotWidget3.setBackground("k")
				self.wattmeter_plotWidget4.setBackground("k")
				self.load_plotWidget1.setBackground("k")
				self.load_plotWidget2.setBackground("k")
				self.load_plotWidget3.setBackground("k")
				self.load_plotWidget4.setBackground("k")
				self.load_plotWidget5.setBackground("k")
		except:
			None
	#endregion


	#region VISA ---------------------------------------------------------
	def visa_VISAresource_changed(self):
		self.visa.setVISAresource(self.cfg.get('VISA/VISAresource'))

	def visa_connect(self):
		if  self.visa.is_connected() == True:
			return(True)
		else:
			self.visa_label_status.setText('Trying to connect...')
			self.visa_label_status.setStyleSheet('')
			ret, retStr = self.visa.connect()
			self.visa_plainTextEdit_output.appendPlainText(retStr)
			if ret == False:
				self.visa_label_status.setText('FAILED to connect')
				self.visa_label_status.setStyleSheet('color:red')
				return(False)
			else:
				self.visa_label_status.setText('Connected')
				self.visa_label_status.setStyleSheet('color:green')
				return(True)

	def visa_disconnect(self):
		if  self.visa.is_connected() == True:
			self.visa_label_status.setText('Disconnecting...')
			self.visa_label_status.setStyleSheet(None)
			ret = self.visa.disconnect()
			if ret == False:
				self.visa_label_status.setText('Disconnected, FAILED to nice disconnect')
				self.visa_label_status.setStyleSheet('color:red')
			else:
				self.visa_label_status.setText('Disconnected ')
				self.visa_label_status.setStyleSheet(None)
		else:
			self.visa_label_status.setText('Disconnected ')
			self.visa_label_status.setStyleSheet(None)

	def visa_send(self):
		if  self.visa.is_connected() == True:
			command = self.visa_lineEdit_SCPIcommand.text()
			self.visa_plainTextEdit_output.appendPlainText('Command sent:\t' + command)
			retCode, retStr = self.visa.send(command)
			self.visa_plainTextEdit_output.appendPlainText(retStr)
		else:
			self.visa_plainTextEdit_output.appendPlainText('Not connected...')
	#endregion VISA


	#region classes for wattmeter ------------------------------
	def wattmeter_VISAresource_changed(self):
		self.wattmeter.setVISAresource(self.cfg.get('wattmeter/VISAresource'))

	def wattmeter_demo_pressed(self):
		self.wattmeter.disconnect()
		self.wattmeter_label_status.setText('Disconnected')
		self.wattmeter_label_status.setStyleSheet('')
		self.wattmeter.setDemo(self.wattmeter_checkBox_demo.isChecked())

	def wattmeter_connect(self):
		if  self.wattmeter.is_connected() == True:
			return(True)
		else:
			self.wattmeter_label_status.setText('Trying to connect...')
			self.wattmeter_label_status.setStyleSheet('')
			retCode, retStr = self.wattmeter.connect()
			if retCode == False:
				self.wattmeter_label_status.setText('FAILED to connect, error: ' + retStr)
				self.wattmeter_label_status.setStyleSheet('color:red')
				return(False)
			else:
				self.wattmeter_label_status.setText('Connected to: ' + retStr)
				self.wattmeter_label_status.setStyleSheet('color:green')
				return(True)

	def wattmeter_disconnect(self):
		if  self.wattmeter.is_connected() == True:
			self.wattmeter_label_status.setText('Disconnecting...')
			self.wattmeter_label_status.setStyleSheet(None)
			ret = self.wattmeter.disconnect()
			if ret == False:
				self.wattmeter_label_status.setText('Disconnected, FAILED to nice disconnect')
				self.wattmeter_label_status.setStyleSheet('color:red')
			else:
				self.wattmeter_label_status.setText('Disconnected ')
				self.wattmeter_label_status.setStyleSheet(None)
		else:
			self.wattmeter_label_status.setText('Disconnected ')
			self.wattmeter_label_status.setStyleSheet(None)


	def wattmeter_checkBox_measure_W_changed(self):
		if self.cfg.get('wattmeter/measure_W'):
			self.wattmeter_plotWidget1.show()
		else:
			self.wattmeter_plotWidget1.hide()


	def wattmeter_checkBox_measure_A_changed(self):
		if self.cfg.get('wattmeter/measure_A'):
			self.wattmeter_plotWidget2.show()
		else:
			self.wattmeter_plotWidget2.hide()


	def wattmeter_checkBox_measure_V_changed(self):
		if self.cfg.get('wattmeter/measure_V'):
			self.wattmeter_plotWidget3.show()
		else:
			self.wattmeter_plotWidget3.hide()


	def wattmeter_checkBox_measure_MATH_changed(self):
		if self.cfg.get('wattmeter/measure_MATH'):
			self.wattmeter_plotWidget4.show()
		else:
			self.wattmeter_plotWidget4.hide()


	def wattmeter_mereni_start(self):
		if  self.load.is_connected() == False:
			self.wattmeter_connect()

		#self.label_test_zatizeni.setText('Measuring')
		#self.label_test_zatizeni.setStyleSheet('color:green')

		# schedule Measuring
		self.timer_wattmeter_mereni = QtCore.QTimer()
		self.timer_wattmeter_mereni.setInterval(self.cfg.get('wattmeter/measure_interval')) # ms
		self.timer_wattmeter_mereni.timeout.connect(self.wattmeter_mereni_mer)
		self.timer_wattmeter_mereni.start()


	def wattmeter_mereni_stop(self):
		self.timer_wattmeter_mereni.stop()
		self.wattmeter_mereni_finished = True


	def wattmeter_mereni_mer(self):
		if self.wattmeter_mereni_finished == False:
			print('wattmeter_mereni_mer nestiha!!!!!!!!!!')
			return()
		self.wattmeter_mereni_finished = False
		
		if True: #self.cfg.get('wattmeter/measure_'):
			W = self.wattmeter.measure('W')
			data_wattmeter_W.append(W)
			data_wattmeter_Wtime.append(time.time())
			self.wattmeter_plotWidget1_dataLine.setData(data_wattmeter_Wtime, data_wattmeter_W)

		if True: #self.cfg.get('wattmeter/measure_'):
			A = self.wattmeter.measure('A')
			data_wattmeter_A.append(A)
			data_wattmeter_Atime.append(time.time())
			self.wattmeter_plotWidget2_dataLine.setData(data_wattmeter_Atime, data_wattmeter_A)

		if True: #self.cfg.get('wattmeter/measure_'):
			V = self.wattmeter.measure('V')
			data_wattmeter_V.append(V)
			data_wattmeter_Vtime.append(time.time())
			self.wattmeter_plotWidget3_dataLine.setData(data_wattmeter_Vtime, data_wattmeter_V)

		if True: #self.cfg.get('wattmeter/measure_'):
			MATH = self.wattmeter.measure('MATH')
			if type(MATH) is float:
				data_wattmeter_MATH.append(MATH)
				data_wattmeter_MATHtime.append(time.time())
				self.wattmeter_plotWidget4_dataLine.setData(data_wattmeter_MATHtime, data_wattmeter_MATH)

		self.wattmeter_mereni_finished = True


	def wattmeter_mereni_clearGraphs(self):
		global data_wattmeter_W, data_wattmeter_Wtime
		data_wattmeter_W = []
		data_wattmeter_Wtime = []
		global data_wattmeter_A, data_wattmeter_Atime
		data_wattmeter_A = []
		data_wattmeter_Atime = []
		global data_wattmeter_V, data_wattmeter_Vtime
		data_wattmeter_V = []
		data_wattmeter_Vtime = []
		global data_wattmeter_MATH, data_wattmeter_MATHtime
		data_wattmeter_MATH = []
		data_wattmeter_MATHtime = []

		self.wattmeter_plotWidget1_dataLine.setData([], [])
		self.wattmeter_plotWidget2_dataLine.setData([], [])
		self.wattmeter_plotWidget3_dataLine.setData([], [])
		self.wattmeter_plotWidget4_dataLine.setData([], [])
	#endregion


	#region classes for LOAD ------------------------------
	def load_VISAresource_changed(self):
			self.load.setVISAresource(self.cfg.get('load/VISAresource'))

	def load_demo_pressed(self):
		self.load.disconnect()
		self.load_label_status.setText('Disconnected')
		self.load_label_status.setStyleSheet('')
		self.load.setDemo(self.cfg.get('load/demo'))

	def load_connect(self):
		if  self.load.is_connected() == True:
			return(True)
		else:
			self.load_label_status.setText('Trying to connect...')
			self.load_label_status.setStyleSheet('')
			retCode, retStr = self.load.connect()
			if retCode == False:
				self.load_label_status.setText('FAILED to connect: ' + retStr)
				self.load_label_status.setStyleSheet('color:red')
				return(False)
			else:
				self.load_label_status.setText('Load connected')
				self.load_label_status.setStyleSheet('color:green')
				return(True)

	def load_disconnect(self):
		if  self.load.is_connected() == True:
			self.load_label_status.setText('Disconnecting...')
			self.load_label_status.setStyleSheet(None)
			ret = self.load.disconnect()
			if ret == False:
				self.load_label_status.setText('Disconnected, FAILED to nice disconnect')
				self.load_label_status.setStyleSheet('color:red')
			else:
				self.load_label_status.setText('Disconnected ')
				self.load_label_status.setStyleSheet(None)
		else:
			self.load_label_status.setText('Disconnected ')
			self.load_label_status.setStyleSheet(None)

	
	def load_doubleSpinBox_BATT_current_changed(self):
		self.load.write(':BATT:LEVEL '+str(self.load_doubleSpinBox_BATT_current.value()))

	def load_radioButton_BATT_range_6A_connect(self):
		self.load.write(':BATT:RANG 6')

	def load_radioButton_BATT_range_60A_connect(self):
		self.load.write(':BATT:RANG 60')

	def load_doubleSpinBox_BATT_vstop_changed(self):
		self.load.write(':BATT:VSTOP '+str(self.load_doubleSpinBox_BATT_vstop.value()))

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
		if  self.load.is_connected() == False:
			self.load_connect()
		#self.label_test_zatizeni.setText('Measuring')
		#self.label_test_zatizeni.setStyleSheet('color:green')

		# schedule Measuring
		self.timer_load_mereni = QtCore.QTimer()
		self.timer_load_mereni.setInterval(self.cfg.get('load/measure_interval')) # ms
		self.timer_load_mereni.timeout.connect(self.load_mereni_mer)
		self.timer_load_mereni.start()


	def load_mereni_stop(self):
		self.timer_load_mereni.stop()
		self.load_mereni_finished = True


	def load_mereni_mer(self):
		if self.load_mereni_finished == False:
			print('load_mereni_mereni-nestiha')
			return()
		self.load_mereni_finished = False

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
		#self.export_textEdit1.append(
		#	str(tt)+CSVDELIM+
		#	str(loadA)+CSVDELIM+
		#	str(loadV)+CSVDELIM+
		#	str(loadW)
		#	)
		self.load_mereni_finished = True


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
	#endregion


	#region testACDCadapteru ------------------------------------------------------
	def testACDCadapteru_start(self):
		if verbose > 150:
			print('testACDCadapteru_start - Start button pressed')
		#self.testACDCadapteru_label_status.setText('xxx')
		if self.testACDCadapteru.semaphore.available() == 0:
			self.testACDCadapteru.semaphore.release(1)
			self.testACDCadapteru.do_measure(
				wmeter = self.wattmeter,
				load = self.load, 
				exportTextEdit = self.export_textEdit1, 
				plot1 = self.testACDCadapteru_plotWidget1,
				plot2 = self.testACDCadapteru_plotWidget2,
				statusLabel = self.testACDCadapteru_label_status,
			)
		else:
			if verbose > 150:
				print('testACDCadapteru_start - Start button pressed, already running')



	def testACDCadapteru_stop(self):
		if verbose > 150:
			print('testACDCadapteru_stop - Stop button pressed')
		if self.testACDCadapteru.semaphore.available() == 1:
			self.testACDCadapteru.semaphore.release(1)


	#endregion

	#region TEST_ZATIZENI ----------------------------------------------------------------
	def test_zatizeni_start(self):
		if self.test_zatizeni_running == True: # test already running
			return()

		self.label_test_zatizeni.setText('Init')
		self.label_test_zatizeni.setStyleSheet('')

		global data_test_zatizeni_ReqA
		data_test_zatizeni_ReqA = []
		global data_test_zatizeni_A
		data_test_zatizeni_A = []
		global data_test_zatizeni_V
		data_test_zatizeni_V = []
		global data_test_zatizeni_W
		data_test_zatizeni_W = []
		self.loadstop_mVAttempts = self.cfg.get('test_adapteru/stop_mVAttempts')

		self.mplWidget1.plot_clear()

		if verbose > 100:
			print('Connecting to Load')

		if not self.load.is_connected():
			ret = self.load_connect()
			if ret == True:
				self.label_test_zatizeni.setText('Load connected')
				self.label_test_zatizeni.setStyleSheet('color:green')
			else:
				self.label_test_zatizeni.setText('FAILED to connect Load')
				self.label_test_zatizeni.setStyleSheet('color:red')
				return()


		self.test_zatizeni_running = True

		self.loadReqmA = 0
		self.load.setFunctionCurrent()
		self.load.setCurrent(0)
		self.load.setStateOn(True)

		self.label_test_zatizeni.setText('Measuring')
		self.label_test_zatizeni.setStyleSheet('color:green')

		self.export_textEdit1.append(
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


	def test_zatizeni_stop(self):
		if self.test_zatizeni_running == True:
			self.test_zatizeni_running = False
			self.timer_test_zatizeni.stop()
			ret = self.load.setStateOn(False) #turn OFF the load
			#ret = self.load.disconnect() will break other measuring, better stay connected
			if ret:
				self.label_test_zatizeni.setText('User stopped')
				self.label_test_zatizeni.setStyleSheet(None)
			else:
				self.label_test_zatizeni.setText('User stopped, FAIL to set State OFF')
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
			#time.sleep
			QtTest.QTest.qWait(self.cfg.get('test_adapteru/time_measure_delay'))

			if verbose>150:
				print(' done.')

			loadA = self.load.measure('A')
			loadV = self.load.measure('V')
			loadW = self.load.measure('W')

			data_test_zatizeni_ReqA.append(self.loadReqA) 
			data_test_zatizeni_A.append(loadA)
			data_test_zatizeni_V.append(loadV)
			data_test_zatizeni_W.append(loadW)

			if self.loadReqmA > 0 or self.cfg.get('test_adapteru/reqmAstart') == 0: # next step
				self.loadReqmA += self.cfg.get('test_adapteru/reqmAstep')
			else: # we are at zero and we need to skip to reqmAstart
				self.loadReqmA = self.cfg.get('test_adapteru/reqmAstart')

			self.mplWidget1.plot_update(data_test_zatizeni_ReqA, data_test_zatizeni_A, data_test_zatizeni_V, data_test_zatizeni_W)

			#Update exports
			self.export_textEdit1.append(
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
			#self.load.disconnect()
			self.timer_test_zatizeni.stop()
			# TODO update grafu
			# self.mplWidget1.plotItem.plot(data_test_zatizeni_V)
			self.export_textEdit1.append('#--------------------------------------')
			self.export_textEdit1.append('')
	#endregion


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