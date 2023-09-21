#!python3

verbose = 80


# region   lib_check_install v3 by Josef La Masek ----------------------------
import importlib.util
import subprocess
import sys
#import pip
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
# endregion   --------------------------------------------------------------------


# region  autoUiPy - automatic QT Designer .ui to .py converter ------------------------------
# v 1 , by Josef La Masek  masek2050@gmail.com
# 
# no needs to do manually run 'pyuc' or by creating setup in project in QT Designer / QT Creator
# during startup it checkes for given list, if generated .py files exists and are fresh,
# if they are not, it will regenerate them

autoUiPy_PYUIC = 'PyQt6.uic.pyuic'
autoUiPy_ui_list = ['ui_mainwindow', 'ui_tab_wattmeter']
autoUiPy_enabled = True

# --------------

import os.path

if autoUiPy_enabled:
	for i in autoUiPy_ui_list:
		if os.path.exists(i+'.py'):
			try:
				#print(os.path.getmtime(i+'.ui'))
				#print(os.path.getmtime(i+'.py'))
				if os.path.getmtime(i+'.ui') <= os.path.getmtime(i+'.py'):
					continue
			except:
				print('autoUiPy: something wrong with given filename')
		
		# python -m PyQt6.uic.pyuic -x mainwindow.ui -o ui_mainwindow.py
		autoUiPy_PYUIC_CALL = [sys.executable, '-m', autoUiPy_PYUIC, '-x', i+'.ui', '-o', i+'.py']
		print('autoUiPy: Calling: ', autoUiPy_PYUIC_CALL)
		try:
			subprocess.check_call(autoUiPy_PYUIC_CALL)
		except Exception as e:
			print('autoUiPy: subprocess call failed: ', e)

# endregion ----------------------------------------------------------------

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
import matplotlib.dates

lib_check_install('mplcursors')
import mplcursors

lib_check_install('PyQt6', 'pyqt6')
from PyQt6 import QtWidgets, uic, QtCore, QtGui, QtTest
from PyQt6.QtCore import QCoreApplication, Qt, QFile, QTextStream, QIODevice, QSemaphore, QByteArray
from PyQt6.QtGui import QImage, QTextCursor, QPageSize, QPixmap, QPainter, QCloseEvent
from PyQt6.QtPrintSupport  import QPrinter
from PyQt6.QtWidgets import QFileDialog

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
import pyqtgraph.exporters


# MS windows only
# 'FIX' the apllication logo in the taskbar 
# sets grouping this script as unique app - not Pythonw.exe with python logo
# see https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
# stopped to work in Windows 11 in ?May? 2023 
lib_check_install('ctypes')
try:
    import ctypes
    myappid = u'LaMasek.tester_adapteru' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except all:
    pass

lib_check_install('Netio')
from Netio import Netio



#import shared_functions
#from shared_functions import plot_prepare
from shared_functions import *

from visa_device import VisaDevice

from wattmeter_device import Wattmeter_GUI

from ui_mainwindow import Ui_MainWindow


###### GLOBAL variables - config ####################################################

CONFIG_DEFAULT = {
					'GUI/theme': 'auto', #auto, dark, light
					'GUI/lastTabIndex' : 1,
					'verbose': 80, 
					'plots/theme': 'auto',
					'plots/minWidth': 300,
					'plots/minHeight': 200,
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
					'netio/IP': '10.10.134.11',
					'netio/demo': True,
					'netio/measure_interval': 500,
					'netio/username': 'netio',
					'netio/password': 'netio',
					'netio/output_id': 1,
					'testACDCadapteru/Po':  1, #W
					'testACDCadapteru/Vmax':  10, #V - Maximální/nominální napětí zdroje
					'testACDCadapteru/test': 'All',
					'testACDCadapteru/load8h': False,
					'testACDCadapteru/typAdapteru': '0: Ignore',
					'test_adapteru/reqmAstep': 100, # mA
					'test_adapteru/reqmAstop': 1000, # mA
					'test_adapteru/stop_mV': 1000, # mV
					'test_adapteru/stop_mVAttempts': 5,
					'test_adapteru/time_step_delay': 1000, #ms, musi byt o trochu vetsi nez time_measure_delay
					'test_adapteru/time_measure_delay': 800,
					'export/CSVDELIM': ', ', #delimiter for export window
				}

# GLOBAL VARIABLES ##################################################################

#data = { # all measured data
#	#item_name : { #item is added when new
#	#   data: (value1, value2, ...)
#	#   time:   (time1, time2, ...)
#	#   graphID: graphID
#}


#data_wattmeter_W = []
#data_wattmeter_Wtime = []
#data_wattmeter_A = []
#data_wattmeter_Atime = []
#data_wattmeter_V = []
#data_wattmeter_Vtime = []
#data_wattmeter_MATH = []
#data_wattmeter_MATHtime = []

data_test_zatizeni_ReqA = []
data_test_zatizeni_A = []
data_test_zatizeni_V = []
data_test_zatizeni_W = []




class Load(VisaDevice):

	def measure(self, varName):
		'''
		varName = 'A' | 'V' | 'W' | 'Wh'
		return(float | None)
		'''
		if  self.demo == True:
			i = math.sin( # sinus, period 5s in time
					(time.time()%5) / 5 * 2*3.1415
				)
			if i < 0: #only positive part
				i = 0
			return( i )
		else:
			#global verbose
			if varName == 'A':
				qStr = ":MEASURE:CURRENT?"
			elif varName == 'V':
				qStr = ":MEASURE:VOLTAGE?"
			elif varName == 'W':
				qStr = ":MEASURE:POWER?"
			elif varName == 'Wh':

				qStr = ":MEASURE:WATThours?"
			else:
				return(None)
			
			self.verbose -= 100
			retCode, retString = VisaDevice.query(self, qStr)
			self.verbose += 100
			if retCode == False:
				return(None)
			try:
				f = float(retString.strip())
			except Exception:
				print(f"error converting answer to float, answer: {retString}")
				return(None)
			if type(f) == float:
				return(f)
			else:
				return(None)
				


	def setFunction(self, mode: str):
		#modes
		# 	CC	Constant Current
		# 	CV 	Constant Voltage
		# 	CR	Constant Resistance
		# 	CP	Constant Power
		if  self.demo == True:
			return()

		if mode == 'CC':
			cmd = 'CURRent'
		elif mode == 'CV':
			cmd = 'VOLTage'
		elif mode == 'CR':
			cmd = 'RESistance'
		elif mode == 'CP':
			cmd = 'POWer'
		else:
			return(False, 'Unknown function')
			
		return(VisaDevice.write(self, ":SOURCE:FUNCTION " + cmd))    # Set to  mode CURRent
		

	def setModeBATT(self):
		if  self.demo == True:
			return()
		return(VisaDevice.write(self, ":SOUR:FUNC:MODE BATT"))    # Set to  mode BATTery


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
			if self.verbose > 100:
				print('PVcommand = '+PVcommand)
			VisaDevice.write(self, PVcommand)

	def setPower(self, current):
		if  self.demo == True:
			return()
		else:
			PVcommand = ':SOURCE:POWer:LEVEL:IMMEDIATE ' + str(current)
			if self.verbose > 100:
				print('PVcommand = '+PVcommand)
			VisaDevice.write(self, PVcommand)

class Load_GUI(Load):
	def __init__(self, VISAresource: str, demo: bool, status: QtWidgets.QTextEdit, verbose: int):
		Load. VISAresource = VISAresource
		Load.demo = demo
		self.status = status
		self.verbose = verbose

	def connect(self):
		if  self.is_connected() == True:
			return(True, 'Already connected')
		else:
			self.status.setText('Trying to connect...')
			self.status.setStyleSheet('')
			retCode, retStr = Load.connect(self)
			#retCode, retStr = super().connect()
			if retCode == False:
				self.status.setText('FAILED to connect, error: ' + retStr)
				self.status.setStyleSheet('color:red')
				return(False, retStr)
			else:
				self.status.setText('Connected to: ' + retStr)
				self.status.setStyleSheet('color:green')
				return(True, retStr)

	def disconnect(self):
		if  self.is_connected() == True:
			self.status.setText('Disconnecting...')
			self.status.setStyleSheet(None)
			ret = Load.disconnect(self)
			if ret == False:
				self.status.setText('Disconnected, FAILED to nice disconnect')
				self.status.setStyleSheet('color:red')
			else:
				self.status.setText('Disconnected ')
				self.status.setStyleSheet(None)
		else:
			self.status.setText('Disconnected ')
			self.status.setStyleSheet(None)




#region Tab_Config -----------------------------------------------------
class Tab_Config():
	def __init__(self, mw: Ui_MainWindow, cfg: QSettingsManager):
		self.cfg = cfg
		self.mw = mw
		self.mw.config_plainTextEdit.setPlaceholderText('Trying to read config...')
		self.cfg.updated.connect(self.config_show)
		self.config_show()
		self.mw.config_pushButton_ClearToDefault.clicked.connect(self.config_set_to_default)

		self.mw.config_GUItheme.addItems(('auto', 'dark', 'light'))
		self.cfg.add_handler('GUI/theme', self.mw.config_GUItheme)
		self.config_GUItheme_changed()
		mw.config_GUItheme.currentTextChanged.connect(self.config_GUItheme_changed)
		
		self.cfg.add_handler('verbose', self.mw.config_verbose)
		self.config_verbose_changed()
		


	def config_show(self):
		self.mw.config_plainTextEdit.clear()
		try:
			d = self.cfg.as_dict()
			for key in d:
				self.mw.config_plainTextEdit.appendPlainText(str(key)+': \t'+ str(d[key]))
		except:
			print('config_show: problem to load previous config, clearing all config.')
			QtCore.QSettings().clear()
			print('config_show: Pls. exit from app. and run it again.')
			

		self.mw.config_plainTextEdit.appendPlainText('')
		self.mw.config_plainTextEdit.appendPlainText('DEFAULT config: -----------------------')
		d = CONFIG_DEFAULT
		for key in d:
			self.mw.config_plainTextEdit.appendPlainText(str(key)+': \t'+ str(d[key]))

	def config_set_to_default(self):
		for key in CONFIG_DEFAULT:
			self.cfg.set(key, CONFIG_DEFAULT[key])

	def config_GUItheme_changed(self):
		if verbose > 80:
			print('GUI Theme changed')
		theme = self.cfg.get('GUI/theme')
		try:
			qdarktheme.setup_theme(theme)
		except:
			None

		themeName: str
		if theme == 'auto':
			try:
				if darkdetect.isDark():
					themeName = 'k'
				else:
					themeName = 'w'
			except:
				None
				themeName = 'w'
		elif theme == 'light':
			themeName = 'w'
		elif theme == 'dark':
			themeName = 'k'
		else:
			print('config_GUItheme_changed: ERROR: unknown theme: ' + str(theme))
			
		
		self.mw.tab_Wattmeter_widget.plot1.setBackground(themeName)
		self.mw.tab_Wattmeter_widget.plot1.setBackground(themeName)
		self.mw.tab_Wattmeter_widget.plot1.setBackground(themeName)
		self.mw.tab_Wattmeter_widget.plot1.setBackground(themeName)
		self.mw.load_plotWidget1.setBackground(themeName)
		self.mw.load_plotWidget2.setBackground(themeName)
		self.mw.load_plotWidget3.setBackground(themeName)
		self.mw.load_plotWidget4.setBackground(themeName)
		self.mw.testACDCadapteru_plotWidget1.setBackground(themeName)
		self.mw.testACDCadapteru_plotWidget2.setBackground(themeName)
		self.mw.testACDCadapteru_plotWidget3.setBackground(themeName)

	#endregion

	def config_verbose_changed(self):
		global verbose
		newVerbose = self.cfg.get('verbose')
		if verbose > 80:
			print(f'config_verbose_changed, verbose changed from: {verbose} to: {newVerbose}')
		verbose = newVerbose



#region Tab_VISA -----------------------------------------------------
class Tab_VISA():
	def __init__(self, mw: Ui_MainWindow, cfg: QSettingsManager, visa: VisaDevice):
		self.mw = mw
		self.cfg = cfg
		self.visa = visa

		self.status = self.mw.visa_label_status
		cfg.add_handler('VISA/VISAresource', mw.visa_lineEdit_VISAresource)
		mw.visa_lineEdit_VISAresource.textChanged.connect(self.visa_VISAresource_changed)
		self.mw.visa_pushButton_connect.pressed.connect(self.visa_connect)
		mw.visa_pushButton_disconnect.pressed.connect(self.visa_disconnect)
		cfg.add_handler('VISA/SCPIcommand', mw.visa_lineEdit_SCPIcommand)
		mw.visa_lineEdit_SCPIcommand.returnPressed.connect(self.visa_send)
		mw.visa_pushButton_send.pressed.connect(self.visa_send)


	def visa_VISAresource_changed(self):
		self.visa.setVISAresource(self.cfg.get('VISA/VISAresource'))

	def visa_connect(self):
		if  self.visa.is_connected() == True:
			return(True)
		else:
			self.status.setText('Trying to connect...')
			self.status.setStyleSheet('')
			ret, retStr = self.visa.connect()
			self.mw.visa_plainTextEdit_output.appendPlainText(retStr)
			if ret == False:
				self.status.setText('FAILED to connect')
				self.status.setStyleSheet('color:red')
				return(False)
			else:
				self.status.setText('Connected')
				self.status.setStyleSheet('color:green')
				return(True)

	def visa_disconnect(self):
		if  self.visa.is_connected() == True:
			self.status.setText('Disconnecting...')
			self.status.setStyleSheet(None)
			ret = self.visa.disconnect()
			if ret == False:
				self.status.setText('Disconnected, FAILED to nice disconnect')
				self.status.setStyleSheet('color:red')
			else:
				self.status.setText('Disconnected ')
				self.status.setStyleSheet(None)
		else:
			self.status.setText('Disconnected ')
			self.status.setStyleSheet(None)

	def visa_send(self):
		if  self.visa.is_connected() == True:
			command = self.mw.visa_lineEdit_SCPIcommand.text()
			self.mw.visa_plainTextEdit_output.appendPlainText('Command sent:\t' + command)
			retCode, retStr = self.visa.send(command)
			self.mw.visa_plainTextEdit_output.appendPlainText(retStr)
		else:
			self.mw.visa_plainTextEdit_output.appendPlainText('Not connected...')

#endregion --------------------------------------------------------

#region Tab_Load -----------------------------------------------------
class Tab_Load():

	#def myinit(self, cfg: QSettingsManager, load: Load_GUI, export: QTextEdit):
	#	self.cfg = cfg
	#	self.load = load
	#	self.export = export

	data_A = []
	data_Atime = []
	data_V = []
	data_Vtime = []
	data_W = []
	data_Wtime = []
	data_Ah = []
	data_Ahtime = []
	data_Wh = []
	data_Whtime = []



	def __init__(self, mw: Ui_MainWindow, cfg: QSettingsManager, load: Load_GUI, export: QTextEdit):
		#self.setupUi(self)

		self.cfg = cfg
		self.load = load
		self.export = export
		self.mw = mw
		self.status = self.mw.load_status
				
		self.timer_load_mereni = QtCore.QTimer()
		self.timer_load_mereni.timeout.connect(self.load_mereni_mer)


		self.cfg.add_handler('load/VISAresource', self.mw.load_lineEdit_VISAresource)
		self.mw.load_lineEdit_VISAresource.textChanged.connect(self.load_VISAresource_changed)
		self.cfg.add_handler('load/demo', self.mw.load_checkBox_demo)
		self.mw.load_checkBox_demo.stateChanged.connect(self.load_demo_changed)
		#self.mw.load_checkBox_demo.stateChanged.connect(self.load_checkBox_demo_changed)

		self.mw.load_pushButton_connect.pressed.connect(self.load.connect)
		self.mw.load_pushButton_disconnect.pressed.connect(self.load.disconnect)
		self.mw.load_pushButton_StateON.pressed.connect(self.load_pushButton_StateON_pressed)
		self.mw.load_pushButton_StateOFF.pressed.connect(self.load_pushButton_StateOFF_pressed)
		
		# LOAD Rem. Ctrl.
		self.mw.load_radioButton_Mode_CC.pressed.connect(self.load_radioButton_Mode_CC_pressed)
		self.mw.load_radioButton_Mode_BATT.pressed.connect(self.load.setModeBATT)
		self.mw.load_doubleSpinBox_BATT_current.valueChanged.connect(self.load_doubleSpinBox_BATT_current_changed)
		self.mw.load_radioButton_BATT_range_6A.pressed.connect( self.load_radioButton_BATT_range_6A_connect )
		self.mw.load_radioButton_BATT_range_60A.pressed.connect(self.load_radioButton_BATT_range_60A_connect)
		self.mw.load_doubleSpinBox_BATT_vstop.valueChanged.connect(self.load_doubleSpinBox_BATT_vstop_changed)

		# LOAD Measure
		self.mw.load_pushButton_mereni_start.pressed.connect(self.load_mereni_start)
		self.mw.load_pushButton_mereni_stop.pressed.connect(self.load_mereni_stop)
		self.mw.load_pushButton_export.pressed.connect(self.load_mereni_export)

		self.cfg.add_handler('load/measure_interval', self.mw.load_spinBox_measure_interval)
		self.mw.load_pushButton_clearGraphs.pressed.connect(self.load_mereni_clearGraphs)

		self.cfg.add_handler('load/measure_A', self.mw.load_checkBox_measure_A)
		self.mw.load_checkBox_measure_A.stateChanged.connect(self.load_checkBox_measure_A_changed)
		self.load_checkBox_measure_A_changed() # set initial state from config
		self.cfg.add_handler('load/measure_V', self.mw.load_checkBox_measure_V)
		self.mw.load_checkBox_measure_V.stateChanged.connect(self.load_checkBox_measure_V_changed)
		self.load_checkBox_measure_V_changed() # set initial state from config
		self.cfg.add_handler('load/measure_W', self.mw.load_checkBox_measure_W)
		self.mw.load_checkBox_measure_W.stateChanged.connect(self.load_checkBox_measure_W_changed)
		self.load_checkBox_measure_W_changed() # set initial state from config
		self.cfg.add_handler('load/measure_Wh', self.mw.load_checkBox_measure_Wh)
		self.mw.load_checkBox_measure_Wh.stateChanged.connect(self.load_checkBox_measure_Wh_changed)
		self.load_checkBox_measure_Wh_changed() # set initial state from config

		self.load_mereni_finished = True # semaphor for measuring method


		self.plot1_dataLine0, self.plot1_dataLine = plot_prepare(cfg, self.mw.load_plotWidget1, 'Current/I [A]', addLine2Zero=True)
		self.plot2_dataLine0, self.plot2_dataLine = plot_prepare(cfg, self.mw.load_plotWidget2, 'Voltage/U [V]', addLine2Zero=True)
		self.plot3_dataLine0, self.plot3_dataLine = plot_prepare(cfg, self.mw.load_plotWidget3, 'Power/P [W]', addLine2Zero=True)
		self.plot4_dataLine0, self.plot4_dataLine = plot_prepare(cfg, self.mw.load_plotWidget4, 'Capacity [Wh]', addLine2Zero=True)

	def load_VISAresource_changed(self):
			self.load.setVISAresource(self.cfg.get('load/VISAresource'))

	def load_demo_changed(self):
		self.load.disconnect()
		self.status.setText('Disconnected')
		self.status.setStyleSheet('')
		self.load.setDemo(self.cfg.get('load/demo'))

	def load_radioButton_Mode_CC_pressed(self):
		self.load.setFunction('CC')
	
	def load_doubleSpinBox_BATT_current_changed(self):
		self.load.write(':BATT:LEVEL '+str(self.mw.load_doubleSpinBox_BATT_current.value()))

	def load_radioButton_BATT_range_6A_connect(self):
		self.load.write(':BATT:RANG 6')

	def load_radioButton_BATT_range_60A_connect(self):
		self.load.write(':BATT:RANG 60')

	def load_doubleSpinBox_BATT_vstop_changed(self):
		self.load.write(':BATT:VSTOP '+str(self.mw.load_doubleSpinBox_BATT_vstop.value()))

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

	def load_checkBox_measure_A_changed(self):
		if self.cfg.get('load/measure_A'):
			self.mw.load_plotWidget1.show()
		else:
			self.mw.load_plotWidget1.hide()

	def load_checkBox_measure_V_changed(self):
		if self.cfg.get('load/measure_V'):
			self.mw.load_plotWidget2.show()
		else:
			self.mw.load_plotWidget2.hide()

	def load_checkBox_measure_W_changed(self):
		if self.cfg.get('load/measure_W'):
			self.mw.load_plotWidget3.show()
		else:
			self.mw.load_plotWidget3.hide()

	def load_checkBox_measure_Wh_changed(self):
		if self.cfg.get('load/measure_Wh'):
			self.mw.load_plotWidget4.show()
		else:
			self.mw.load_plotWidget4.hide()

	def load_mereni_start(self):
		if  self.load.is_connected() == False:
			self.load.connect()
		#self.label_test_zatizeni.setText('Measuring')
		#self.label_test_zatizeni.setStyleSheet('color:green')

		if  self.load.is_connected() == True:
			# schedule Measuring
			self.timer_load_mereni.setInterval(self.cfg.get('load/measure_interval')) # ms
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
			loadA = self.load.measure('A')
			self.data_A.append(loadA)
			self.data_Atime.append(time.time())
			self.plot1_dataLine.setData(self.data_Atime, self.data_A)
			if len(self.data_A) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
				self.plot1_dataLine0.setData([time.time()], [0])

		if self.cfg.get('load/measure_V'):
			loadV = self.load.measure('V')
			self.data_V.append(loadV)
			self.data_Vtime.append(time.time())
			self.plot2_dataLine.setData(self.data_Vtime, self.data_V)
			if len(self.data_V) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
				self.plot2_dataLine0.setData([time.time()], [0])

		if self.cfg.get('load/measure_W'):
			loadW = self.load.measure('W')
			self.data_W.append(loadW)
			self.data_Wtime.append(time.time())
			self.plot3_dataLine.setData(self.data_Wtime, self.data_W)
			if len(self.data_W) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
				self.plot3_dataLine0.setData([time.time()], [0])

		if self.cfg.get('load/measure_Wh'):
			loadWh = self.load.measure('Wh')
			self.data_Wh.append(loadWh)
			self.data_Whtime.append(time.time())
			self.plot4_dataLine.setData(self.data_Whtime, self.data_Wh)
			if len(self.data_Wh) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
				self.plot4_dataLine0.setData([time.time()], [0])

		self.load_mereni_finished = True

	def load_mereni_export(self):
		self.export_textEdit1.insertHtml('<BR></BR><H1>Export naměřených hodnot zátěže</H1><BR></BR>')
		CSVDELIM = self.cfg.get('export/CSVDELIM')

		if self.cfg.get('load/measure_A'):
			self.export_textEdit1.insertHtml('<H2>Proud [A]</H2><BR></BR>')
			self.export_textEdit1.append(f'Time [seconds since 1970]{CSVDELIM}I [A]')
			for i in range(len(self.data_A)):
				self.export_textEdit1.append(
					str(self.data_Atime[i])+CSVDELIM+
					str(self.data_A[i])
				)
			self.export_textEdit1.append('')
			self.export_textEdit1.insertHtml('<BR></BR>')

		if self.cfg.get('load/measure_V'):
			self.export_textEdit1.insertHtml('<H2>Napětí [V]</H2><BR></BR>')
			self.export_textEdit1.append(f'Time [seconds since 1970]{CSVDELIM}U [V]')
			for i in range(len(self.data_V)):
				self.export_textEdit1.append(
					str(self.data_Vtime[i])+CSVDELIM+
					str(self.data_V[i])
				)
			self.export_textEdit1.append('')
			self.export_textEdit1.insertHtml('<BR></BR>')

		if self.cfg.get('load/measure_W'):
			self.export_textEdit1.insertHtml('<H2>Výkon [W]</H2><BR></BR>')
			self.export_textEdit1.append(f'Time [seconds since 1970]{CSVDELIM}P [W]')
			for i in range(len(self.data_W)):
				self.export_textEdit1.append(
					str(self.data_Wtime[i])+CSVDELIM+
					str(self.data_W[i])
				)
			self.export_textEdit1.append('')
			self.export_textEdit1.insertHtml('<BR></BR>')

		if self.cfg.get('load/measure_Wh'):
			self.export_textEdit1.insertHtml('<H2>Energie [Wh]</H2><BR></BR>')
			self.export_textEdit1.append(f'Time [seconds since 1970]{CSVDELIM} [Wh]')
			for i in range(len(self.data_Wh)):
				self.export_textEdit1.append(
					str(self.data_Whtime[i])+CSVDELIM+
					str(self.data_Wh[i])
				)
			self.export_textEdit1.append('')
			self.export_textEdit1.insertHtml('<BR></BR>')

	def load_mereni_clearGraphs(self):
		self.data_A = []
		self.data_Atime = []
		self.data_V = []
		self.data_Vtime = []
		self.data_W = []
		self.data_Wtime = []
		self.data_Wh = []
		self.data_Whtime = []

		self.plot1_dataLine0.setData([], [])
		self.plot1_dataLine.setData([], [])
		self.plot2_dataLine0.setData([], [])
		self.plot2_dataLine.setData([], [])
		self.plot3_dataLine0.setData([], [])
		self.plot3_dataLine.setData([], [])
		self.plot4_dataLine0.setData([], [])
		self.plot4_dataLine.setData([], [])

#endregion 

#region Netio_GUI -----------------------------------------------------
class Netio_GUI:

	netio: Netio
	connected = False

	def __init__(self, cfg: QSettingsManager, status: QtWidgets.QTextEdit):
		self.cfg = cfg
		self.status = status
		self.verbose = cfg.get('verbose')
		

	def connect(self):
		if  self.connected == False:
			self.status.setText('Trying to connect...')
			self.status.setStyleSheet('')

			netio_json_url = 'http://'+self.cfg.get('netio/IP')+'/netio.json'
			username = self.cfg.get('netio/username')
			password = self.cfg.get('netio/password')
			try:
				self.netio = Netio(netio_json_url, auth_rw=(username, password), timeout=3) # timeout in seconds
			except Exception as e:
				print(f'Netio_GUI Connection Error: {e}')
				self.status.setText('FAILED to connect, error: ' + str(e))
				self.status.setStyleSheet('color:red')
				return(False)
			self.status.setText('Connected to: ' + str(self.netio))
			self.status.setStyleSheet('color:green')
			self.connected = True
			return(True)

	def disconnect(self):
		if  self.connected == True:
			self.status.setText('Disconnecting...')
			self.status.setStyleSheet(None)
			del self.netio
			#self.netio = None
			#if ret == False:
			#	self.status.setText('Disconnected, FAILED to nice disconnect')
			#		self.status.setStyleSheet('color:red')
			self.status.setText('Disconnected ')
			self.status.setStyleSheet(None)
			self.connected = False
		else:
			self.status.setText('Disconnected ')
			self.status.setStyleSheet(None)
			self.connected = False


#endregion ------------------------------------------------------------

#region Tab_Netio -----------------------------------------------------
class Tab_Netio():

	output_id: int


	data_A = []
	data_Atime = []
	data_V = []
	data_Vtime = []
	data_W = []
	data_Wtime = []
	data_Ah = []
	data_Ahtime = []
	data_Wh = []
	data_Whtime = []

	mereni_finished = True


	def __init__(self, mw: Ui_MainWindow, netio_gui: Netio_GUI, cfg: QSettingsManager, export: QTextEdit):
		#self.setupUi(self)

		self.mw = mw
		self.netio_gui = netio_gui
		self.cfg = cfg
		self.export = export
		self.status = self.mw.netio_status

		self.output_id = cfg.get('netio/output_id')


		self.mw.netio_demo.setVisible(False)

		self.timer_mereni = QtCore.QTimer()
		self.timer_mereni.timeout.connect(self.mereni_mer)


		self.cfg.add_handler('netio/IP', self.mw.netio_IP)
		#self.mw.netio_IP.textChanged.connect(self.IP_changed)
		self.cfg.add_handler('netio/demo', self.mw.netio_demo)
		self.mw.netio_demo.stateChanged.connect(self.demo_changed)
		self.mw.netio_connect.pressed.connect(self.netio_gui.connect)
		self.mw.netio_disconnect.pressed.connect(self.netio_gui.disconnect)

		self.mw.netio_on.pressed.connect(self.on_pressed)
		self.mw.netio_off.pressed.connect(self.off_pressed)


		self.mw.netio_start.pressed.connect(self.mereni_start)
		self.mw.netio_stop.pressed.connect(self.mereni_stop)
		#self.mw.load_pushButton_export.pressed.connect(self.load_mereni_export)

		self.cfg.add_handler('netio/measure_interval', self.mw.netio_measure_interval)
		self.mw.netio_clear.pressed.connect(self.mereni_clear)

		self.plot1_dataLine0, self.plot1_dataLine = plot_prepare(cfg, self.mw.netio_plot1, 'Current/I [A]', addLine2Zero=True)


	def demo_changed(self):
		self.netio_gui.disconnect()
		#self.load.setDemo(self.cfg.get('load/demo'))

	def on_pressed(self):
		if self.netio_gui.connected == False:
			return()
		if verbose > 120:
			print('Netio turning ON')
		self.netio_gui.netio.set_output(self.output_id, 1)

	def off_pressed(self):
		if self.netio_gui.connected == False:
			return()
		if verbose > 120:
			print('Netio turning OFF')
		self.netio_gui.netio.set_output(self.output_id, 0)

	def mereni_start(self):
		if  self.netio_gui.connected == False:
			self.netio_gui.connect()
		#self.label_test_zatizeni.setText('Measuring')
		#self.label_test_zatizeni.setStyleSheet('color:green')

		if  self.netio_gui.connected == True:
			# schedule Measuring
			self.timer_mereni.setInterval(self.cfg.get('netio/measure_interval')) # ms
			self.timer_mereni.start()


	def mereni_stop(self):
		self.timer_mereni.stop()
		self.mereni_finished = True


	def mereni_mer(self):
		if self.mereni_finished == False:
			print('netio mereni_mereni-nestiha')
			return()
		self.mereni_finished = False


		netio_get_output = self.netio_gui.netio.get_output(self.output_id)
		#print(netio_get_output)
		#Output(ID=1, Name='Power output 1', State=0, Action=<ACTION.IGNORED: 6>, Delay=2020, Current=0,
		#  PowerFactor=1.0, Load=0, Energy=5056)
		#ps_current = ps_get_output[5]

		xA = float(netio_get_output[5]/1000)
		self.data_A.append(xA)
		self.data_Atime.append(time.time())
		self.plot1_dataLine.setData(self.data_Atime, self.data_A)
		if len(self.data_A) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
			self.plot1_dataLine0.setData([time.time()], [0])

		self.mereni_finished = True


	def mereni_clear(self):
		self.data_A = []
		self.data_Atime = []
		self.data_V = []
		self.data_Vtime = []
		self.data_W = []
		self.data_Wtime = []
		self.data_Wh = []
		self.data_Whtime = []

		self.plot1_dataLine0.setData([], [])
		self.plot1_dataLine.setData([], [])
		#self.plot2_dataLine0.setData([], [])
		#self.plot2_dataLine.setData([], [])
		#self.plot3_dataLine0.setData([], [])
		#self.plot3_dataLine.setData([], [])
		#elf.plot4_dataLine0.setData([], [])
		#self.plot4_dataLine.setData([], [])

#endregion 

#region Tab_help -----------------------------------------------------
class Tab_help(Ui_MainWindow):
	def __init__(self, mw: Ui_MainWindow):
		f = io.open("help/help.html", mode="r", encoding="utf-8")
		#f.open(QIODevice.ReadOnly | QIODevice.Text)
		#f.open(QFile.ReadOnly | QFile.Text)
		#f.open()
		#istream = QTextStream(f)
		str = ''
		for x in f:
			str += x
		mw.help_textEdit.setHtml(str)
#endregion 


def plotWidget2qimage(plot: pyqtgraph.PlotWidget):
		#verze s exportem pyqtgraph do qimage
		plot.setMinimumSize(400, 400)
		exporter = pyqtgraph.exporters.ImageExporter(plot.plotItem)
		exporter.parameters()['width'] = 600   # (note this also affects height parameter)
		#byteArr = QByteArray
		img = QImage
		img = exporter.export(toBytes = True)
		return(img)

def textEditAppendImg(te: QtWidgets.QTextEdit, img: QImage):
	cursor = QTextCursor(te.document())
	cursor.movePosition(QTextCursor.MoveOperation.End)
	cursor.insertImage(img)
	te.insertHtml('<BR></BR>')
	te.insertHtml('<BR></BR>')

'''
def plot_prepare(cfg, plot: pyqtgraph.PlotWidget, labelY: str, addLine2Zero = True, *kwargs):
	penColor = color=(205, 205, 205)
	pen = pyqtgraph.mkPen(penColor, width=1)
	cursor = Qt.CursorShape.CrossCursor
	# https://www.geeksforgeeks.org/pyqtgraph-symbols/

	plot.show()
	plot.clear()
	plot.setMinimumSize(cfg.get('plots/minWidth'), cfg.get('plots/minHeight'))
	#plot1.showGrid(x=True, y=True)
	daxis = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
	plot.setAxisItems({"bottom": daxis})
	plot.setLabel('left', labelY)
	#plot.setCursor(self.cursor)
	plot_dataLine =  plot.plot([], [],
		labelY, symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=pen)
	
	if addLine2Zero:
		plot_dataLine2 = plot.plot([], [], symbol='+', symbolSize = 0)
		plot_dataLine2.setData([time.time()], [0])

	return(plot_dataLine)
'''

def data2plot2qimg_old(dataX, dataY, width = 600, height=400, 
		   xlabel='', 
		   ylabel = '', 
		   title = '',
		   formatXasTime = False, # on X axis is unix timestamps and will be converted as H:M:S
		   **kwargs):
	#prevede data na matplotlib obrazek a z nej udela Qimage
	fig = Figure()
	canvas = FigureCanvas(fig)
	canvas.setFixedHeight(height)
	canvas.setFixedWidth(width)
	
	ax1 = fig.add_subplot()
	#plt.rc('figure', dpi=200)
	#fig.tight_layout() # radeji nepouzivat casto mizi popisky
	canvas.draw()
	#ax1.cla()  # Clear the canvas.
	linesA = ax1.plot(dataX, dataY, marker='o', label=ylabel)
	ax1.set(ylim=(0, None))
	#axs[0].tick_linesArams(axis='y', colors=linesA.get_color())
	ax1.legend(loc='best', shadow=True)


	# show dataX in unix timestamps to string dates
	#  https://rowannicholls.github.io/python/graphs/time_data.html
	#ax=plt.gca()
	if formatXasTime:
		fmt = matplotlib.ticker.FuncFormatter(lambda x, pos: time.strftime('%H:%M:%S', time.localtime(x)))
		ax1.xaxis.set_major_formatter(fmt)

	#https://saturncloud.io/blog/python-matplotlib-pyqt-plotting-to-qpixmap/
	pixmap = QPixmap(width, height)
	painter = QPainter(pixmap)
	canvas.render(painter)
	painter.end()
	img = pixmap.toImage()
	return img


def data2plot2qimg(
		dataX: list, dataY: list,
		width = 600,
		height = 400, 
		xlabel ='', 
		ylabel = '', 
		title = '',
		formatXasTime = False, # on X axis is unix timestamps and will be converted as H:M:S
		yMaxInLegend = False,
		):
	#prevede data na matplotlib obrazek a z nej udela Qimage

	plt.clf()
	#plt.figure().set_figwidth(str(width)+'*px')
	#plt.figure().set_figheight(str(height)+'*px')
	#plt.rcParams['figure.figsize'] = [4, 4] # 4x4 inche


	fig, ax = plt.subplots()
	#plt.rc('figure', dpi=200)
	#fig.tight_layout() # radeji nepouzivat casto mizi popisky

	linesA, = ax.plot(dataX, dataY, marker='o')
	#linesA = ax.plot(dataX, dataY, marker='o', label=ylabel)

	if xlabel != '': 
		ax.set(xlabel=xlabel)
	if xlabel =='' and formatXasTime == True:
		ax.set(xlabel='Time [H:M:S]')
	if ylabel != '': 
		ax.set(ylabel=ylabel)
	if title != '': 
		ax.set(title=title)

	ax.set(ylim=(0, None))
	#axs[0].tick_linesArams(axis='y', colors=linesA.get_color())
	#plt.legend(loc='best', shadow=True)


	# show dataX in unix timestamps to string dates
	#  https://rowannicholls.github.io/python/graphs/time_data.html
	#ax=plt.gca()
	if formatXasTime:
		fmt = matplotlib.ticker.FuncFormatter(lambda x, pos: time.strftime('%H:%M:%S', time.localtime(x)))
		ax.xaxis.set_major_formatter(fmt)

	if yMaxInLegend == True:
		#bbox = dict(boxstyle ="round", fc ="0.8")
		yMax = max(dataY)
		#xMax = dataX[dataY.index(max(dataY))]
		#plt.annotate(f'maximum = ({xMax},{yMax})', xy=(xMax, yMax), bbox = bbox)
		ax.legend([f'Maximum = {yMax:.3f}'], loc='best', shadow=True)


	bIO = io.BytesIO()
	plt.savefig(bIO, format='png', dpi=100)
	#plt.savefig('test.png')
	plt.close()
	bIO.seek(0)
	data = bIO.read()
	img = QImage()
	img.loadFromData(data, format='png')

	return(img)


class TestACDCadapteru():
	semaphore = QSemaphore(0) # semafor na testy:
			# 0 	test is not running
			# 1		test is running
			# 2 	do exit from test (e.g. button pressed)

	def __init__(self, mw: Ui_MainWindow, cfg: QSettingsManager, load: Load_GUI, wmeter: Wattmeter_GUI):
		self.mw = mw
		self.cfg = cfg
		self.load = load
		self.wmeter = wmeter
		self.exportTextEdit = self.mw.export_textEdit1
		#testACDCadapteru_checkBox_load8h

	def check_exit(self, statusLabel):
		if self.semaphore.available() > 1: #stop the test and exit
			if verbose > 150:
				print('TestACDCadapteru-->do_measure Test stopped by user')
			statusLabel.setText('Stopped by user')
			self.semaphore.tryAcquire(1)
			return(True)
		else:
			return(False)


	def do_measure(	self,
			wmeter: Wattmeter_GUI,
			load: Load_GUI, 
			exportTextEdit: QtWidgets.QTextEdit, 
			plot1: pyqtgraph.PlotWidget, 
			plot2: pyqtgraph.PlotWidget,
			plot3: pyqtgraph.PlotWidget,
			statusLabel: QtWidgets.QLabel,
			cfg: QSettingsManager,
			):
		statusLabel.setText('Started')
		exportTextEdit.insertHtml('<H1>Test AC/DC adaptéru</H1><BR></BR>')
		#now  = datetime.now()
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
		load.write(':SOUR:CURR:RANG 60')  # nutne pro short test atp.


		if wmeter.is_connected() == False:
			retCode, retString = wmeter.connect()
			if not retCode:
				statusLabel.setText('Failed to connect Wattmeter')
				self.semaphore.tryAcquire(1)
				return(False)
		rc, rs = wmeter.query('*IDN?')
		exportTextEdit.insertHtml('<P>Wattmeter IDN: ' + rs + '</P><BR></BR>')



		vPo = cfg.get('testACDCadapteru/Po')
		vTypAdapteru = cfg.get('testACDCadapteru/typAdapteru')
		#	['0: Ignore', '2: Low voltage <6V >=550mA', '3: AC-DC >=6V', '4: Multiple outputs'

		if vTypAdapteru[0] == '0':
			vPstbMax = 0
			vPaMin = 0
			vPaMinStr = 'Ignored'
		elif vTypAdapteru[0] == '2': #'2: Low voltage <6V >=550mA'
			if vPo <= 1:
				vPstbMax = 0.1
				vPaMin = 0.517*vPo + 0.087
				vPaMinStr = '0,517*Po/1W + 0,087'
			elif vPo <= 49:
				vPstbMax = 0.1
				vPaMin = 0.0834*math.log(vPo) - 0.0014*vPo + 0,609
				vPaMinStr = '0,0834*ln(Po/1W) - 0,0014*Po/1W + 0,609'
			else:
				vPstbMax = 0.21
				vPaMin = 0.87
				vPaMinStr = '0,87'
		elif vTypAdapteru[0] == '3': #'3: AC-DC >=6V'
			if vPo <= 1:
				vPstbMax = 0.1
				vPaMin = 0.5*vPo + 0.160
				vPaMinStr = '0,5*Po/1W + 0,160'
			elif vPo <= 49:
				vPstbMax = 0.1
				vPaMin = 0.071*math.log(vPo) - 0.0014*vPo + 0,67
				vPaMinStr = '0,071*ln(Po/1W) - 0,0014*Po/1W + 0,67'
			else:
				vPstbMax = 0.21
				vPaMin = 0.88
				vPaMinStr = '0,88'
		elif vTypAdapteru[0] == '4': #'4: Multiple outputs'
			vPstbMax = 0.3
			if vPo <= 1:
				vPaMin = 0.497*vPo + 0.067
				vPaMinStr = '0,497*Po/1W + 0,067'
			elif vPo <= 49:
				vPaMin = 0.075*math.log(vPo) + 0.561
				vPaMinStr = '0,075*ln(Po/1W) + 0,561'
			else:
				vPaMin = 0.86
				vPaMinStr = '0,86'

		#plot1.hide()
		#plot2.hide()
		#plot3.hide()

		#region test_Pstb -------------------------------------------------------------------
		if cfg.get('testACDCadapteru/test') in {'All', 'Pstb'}: 
			statusLabel.setText('Test Pstb Started')

			exportTextEdit.insertHtml('<H2>Standby příkon adaptéru - <B>Pstb</B></H2><BR></BR>')
			exportTextEdit.insertHtml('<P>Měří se 10 minutový průměr příkonu adaptéru bez zátěže - Pstb.</P><BR></BR>')

			plot1_dataLine = plot_prepare(cfg, plot1, 'Power/P [W]')
			plot2_dataLine = plot_prepare(cfg, plot2, 'MATH - Avg Power/P [W]')
			plot3_dataLine = plot_prepare(cfg, plot3, 'MATH Time [h:m:s]')
			

			load.setStateOn(False) #no Load
			ldata_wattmeter_W = []
			ldata_wattmeter_Wtime = []
			ldata_wattmeter_MATH = []
			ldata_wattmeter_MATHtime = []
			ldata_wattmeter_TIME = []
			ldata_wattmeter_TIMEtime = []

			wmeter.integrateReset()
			wmeter.integrateStart()
			if wmeter.demo != True:
				stepTime = 200
				QtTest.QTest.qWait(1000)
			else: 
				stepTime = 20

			retCode, iState = wmeter.integrateState()
			statusLabel.setText('Test Pstb - Measuring')

			while iState.startswith('STAR'):

				W = wmeter.measure('W')
				ldata_wattmeter_W.append(W)
				ldata_wattmeter_Wtime.append(time.time())
				plot1_dataLine.setData(ldata_wattmeter_Wtime, ldata_wattmeter_W)

				MATH = wmeter.measure('MATH')
				ldata_wattmeter_MATH.append(MATH)
				ldata_wattmeter_MATHtime.append(time.time())
				plot2_dataLine.setData(ldata_wattmeter_MATHtime, ldata_wattmeter_MATH)

				TIME = wmeter.measure('TIME')
				ldata_wattmeter_TIME.append(TIME)
				ldata_wattmeter_TIMEtime.append(time.time())
				plot3_dataLine.setData(ldata_wattmeter_TIMEtime, ldata_wattmeter_TIME)

				retCode, iState = wmeter.integrateState()
				
				QtTest.QTest.qWait(stepTime)

				if self.check_exit(statusLabel): #stop the test and exit
					exportTextEdit.insertHtml('<H2>Měření <B> PŘERUŠENO UŽIVATELEM</B> - naměřená data, '
			       		+ 'grafy a vyhodnocení jsou pouze částečné - jejich vyhodnocení je na uživateli</H2><BR></BR>')
					statusLabel.setText('Test Pstb - Stopped by user')
					vPstbLast = MATH
					wmeter.integrateReset()
					break

			if not iState.startswith('TIM'): # failed to measure
				exportTextEdit.insertHtml('<H2>Měření Pstb selhalo, zobrazené hodnoty jsou pro kratší čas než požadovaný</H2><BR></BR>')
				statusLabel.setText('Test Pstb - Failed')


			#Pstb = ldata_wattmeter_MATH[-1] 
			vPstb = wmeter.measureNoNAN('MATH')
			wmeter.integrateReset()
			if not vPstb > 0:
				exportTextEdit.insertHtml(f'<H3>Pstb nelze načíst jako výsledek z wattmetru, bereme poslední hodnotu z grafu.</H3><BR></BR>')
				vPstb = vPstbLast

			exportTextEdit.insertHtml(f'<H3>Standby příkon adaptéru - <B>Pstb</B>: {vPstb:.3f} W</H3><BR></BR>')
			exportTextEdit.insertHtml('<BR></BR>')

			if vPstbMax > 0:
				if vPstb <= vPstbMax:
					vPstbSplnil = 'ANO'
				else:
					vPstbSplnil = 'NE'
				exportTextEdit.insertHtml(f'<H3>Maximální povolený Pstb dle NAŘÍZENÍ KOMISE (EU) 2019/1782 ze dne 1. října 2019.</H3><BR></BR>')
				exportTextEdit.insertHtml(f'<H4>&nbsp;&nbsp;&nbsp;PstbMax: {vPstbMax} W</H4><BR></BR>')
				exportTextEdit.insertHtml(f'<H4>&nbsp;&nbsp;&nbsp;Splnil (ANO/NE): <B>{vPstbSplnil}</B></H4><BR></BR>')
				exportTextEdit.insertHtml('<BR></BR>')

			exportTextEdit.insertHtml('<P>Průběh spotřeby během měření:<BR></BR>')
			img = data2plot2qimg(ldata_wattmeter_Wtime, ldata_wattmeter_W, 
					ylabel='Power [W]', xlabel='Time [H:M:S]', formatXasTime=True, width=1200)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			exportTextEdit.insertHtml('<P>Průběh Pstb během měření (hodí se pro vizuální kontrolu ' +
					'chyb v měření):<BR></BR>')
			img = data2plot2qimg(ldata_wattmeter_Wtime, ldata_wattmeter_MATH, 
					ylabel='MATH = AVG Power [W]', height=200, formatXasTime=True, width=1200)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			exportTextEdit.insertHtml('<P>Průběh času během měření (hodí se pro vizuální kontrolu ' +
					'chyb v měření, měl by plynule růst od 0 do 10 minut):<BR></BR>')
			img = data2plot2qimg(ldata_wattmeter_TIMEtime, ldata_wattmeter_TIME, ylabel='MATH Time [H:M:S]',
					height=200, formatXasTime=True)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			statusLabel.setText('Test Pstb - Finished')
		#endregion -------------------------------------------------------------

		#region test Pa -------------------------------------------------------------
		# ucinnost v aktivnim rezimu - pri 25, 50, 75 a 100%
		if cfg.get('testACDCadapteru/test') in {'All', 'Pa'}: 
			statusLabel.setText('Test Pa Started')

			exportTextEdit.insertHtml('<H2>Měření účinnosti v aktivním režimu  - <B>Pa</B></H2><BR></BR>')
			exportTextEdit.insertHtml('<P>Měří se účinnost adaptéru (příkon na wattmetru děleno výkonem na zátěži)' +
					'při 25%, 50%, 75%, 100% zatížení z maxima, z toho aritmetický průměr.</P><BR></BR>')
			exportTextEdit.insertHtml('<P>Na zátěži je nastaven mód Constant Power, změřená účinnost bude ' + 
					'horší než reálná díky ztrátám napětí na měřících kabelech a konektorech</P><BR></BR>')
			exportTextEdit.insertHtml('<P>Po nastavení zátěže se čeká 5 vteřin, než se začne měřit.' + 
					'Na wattmetru se měří 10x a z toho se použije aritmetický průměr.</P><BR></BR>')
			#TODO 'NAŘÍZENÍ KOMISE (EU) 2019/1782 ze dne 1. října 2019, kterým se stanoví požadavky na ekodesign vnějších napájecích zdrojů podle směrnice Evropského parlamentu a Rady 2009/125/ES'
			exportTextEdit.insertHtml('<H3>Nominální/maximální výkon adaptéru - <B>Po = ' + str(vPo) + 
					' W</B></H3><BR></BR>')

			load.setStateOn(False)
			load.setFunction('CP')
			load.setPower(0)
			load.setStateOn(True)

			if wmeter.demo == True:
				twait = 100
			else:
				twait = 3000
			load.setStateOn(True)

			load.setPower(vPo*0.1)
			QtTest.QTest.qWait(twait)
			wmeterW10 = wmeter.measure10Avg('W')
			loadW10 = load.measure('W')
			statusLabel.setText('Power in 10%')

			load.setPower(vPo*0.25)
			QtTest.QTest.qWait(twait)
			wmeterW25 = wmeter.measure10Avg('W')
			loadW25 = load.measure('W')
			statusLabel.setText('P in 25%')

			load.setPower(vPo*0.5)
			QtTest.QTest.qWait(twait)
			wmeterW50 = wmeter.measure10Avg('W')
			loadW50 = load.measure('W')
			statusLabel.setText('P in 50%')

			load.setPower(vPo*0.75)
			QtTest.QTest.qWait(twait)
			wmeterW75 = wmeter.measure10Avg('W')
			loadW75 = load.measure('W')
			statusLabel.setText('P in 75%')

			load.setPower(vPo)
			QtTest.QTest.qWait(twait)
			wmeterW100 = wmeter.measure10Avg('W')
			loadW100 = load.measure('W')
			statusLabel.setText('P in 100%')

			try:
				xP10 = loadW10/wmeterW10
			except:
				xP10 = 0
			exportTextEdit.insertHtml(f'<H4>Průměrná účinnost při malém zatížení (10%) - <B>P10 = {xP10:.3f}</B></H4><BR></BR>')


			try:
				xP25 = loadW25/wmeterW25
			except:
				xP25 = 0
			try:
				xP50 = loadW50/wmeterW50
			except:
				xP50 = 0
			try:
				xP75 = loadW75/wmeterW75
			except:
				xP75 = 0
			try:
				xP100 = loadW100/wmeterW100
			except:
				xP100 = 0

			vPa = (xP25 + xP50 + xP75 + xP100)/4
			exportTextEdit.insertHtml(
				'<TABLE BORDER="1">' +
					'<TR><TH>% z Po</TH><TH>Požadovaný P [W]</TH><TH>Naměřený P na zátěži [W]</TH>' +
						'<TH>Naměřený P na wattmetru [W]</TH><TH>Vypočtená účinnost [0-1]</TH></TR>' +
					f'<TR><TD>25%</TD><TD>{vPo*0.25}</TD><TD>{loadW25:.3f}</TD>' +
						f'<TD>{wmeterW25:.3f}</TD><TD>{xP25:.3f}</TD></TR>'
					f'<TR><TD>50%</TD><TD>{vPo*0.5}</TD><TD>{loadW50:.3f}</TD>' +
						f'<TD>{wmeterW50:.3f}</TD><TD>{xP50:.3f}</TD></TR>'
					f'<TR><TD>75%</TD><TD>{vPo*0.75}</TD><TD>{loadW75:.3f}</TD>' +
						f'<TD>{wmeterW75:.3f}</TD><TD>{xP75:.3f}</TD></TR>'
					f'<TR><TD>100%</TD><TD>{vPo}</TD><TD>{loadW100:.3f}</TD>' +
						f'<TD>{wmeterW100:.3f}</TD><TD>{xP100:.3f}</TD></TR>'
				'</TABLE><BR></BR>')
			exportTextEdit.insertHtml('<H3>Průměrná účinnost v aktivním režimu - <B>Pa = </B>' +
					f'{vPa:.3f}</H3><BR></BR>')
			exportTextEdit.insertHtml('<BR></BR>')

			load.setStateOn(False)
			statusLabel.setText('Test Pa finished.')
		#endregion -------------------------------------------------------------

		#region test VA charakteristika  -------------------------------------------------------------
		if cfg.get('testACDCadapteru/test') in {'All', 'VA char.'}: 
			statusLabel.setText('Test VA char.: Started')
			exportTextEdit.insertHtml('<P><H2>Měření <B>VA charakteristiky</B> při normálním zatížení</H2>')
			exportTextEdit.insertHtml('''
						<UL>
							<LI>postupně se zvyšuje požadovaný výkon na zátěži 0-100%</LI>
							<LI>měří se U a I na zátěži, výsledek je VA charakteristika zdroje<LI>
							<LI>měří se P na zátěži i na wattmetru a výsledek je graf účinnosti vzhledem k zátěži</LI>
						</UL></P><BR></BR>''')

			load.setStateOn(False)
			load.setFunction('CP')
			load.setPower(0)
			QtTest.QTest.qWait(100)
			load.setStateOn(True)

			dataLoadA = []
			dataLoadAtime = []
			dataLoadV = []
			dataLoadVtime = []
			dataLoadW = []
			dataLoadWtime = []
			dataLoadReqW = []
			dataLoadReqWtime = []

			dataWmeterW = []
			dataWmeterWtime = []

			plot1_dataLine = plot_prepare(cfg, plot1, 'Load Measured I [A]')
			plot2_dataLine = plot_prepare(cfg, plot2, 'Load measured U [V]')
			plot3_dataLine = plot_prepare(cfg, plot3, 'Load Requested P [W]')

			xPo = cfg.get('testACDCadapteru/Po')
			loadReqW = 0
			if wmeter.demo == True:
				stepTime = 1
				stepW = xPo/60 # merime 0,1 minutu
			else:
				stepTime = 100
				stepW = xPo/600 # merime 1,1 minutu
			while loadReqW < xPo:
				load.setPower(loadReqW)
				QtTest.QTest.qWait(stepTime)
				
				dataLoadA.append(load.measure('A'))
				dataLoadAtime.append(time.time())
				dataLoadV.append(load.measure('V'))
				dataLoadVtime.append(time.time())
				dataLoadW.append(load.measure('W'))
				dataLoadWtime.append(time.time())
				dataLoadReqW.append(loadReqW)
				dataLoadReqWtime.append(time.time())

				dataWmeterW.append(wmeter.measure('W'))
				dataWmeterWtime.append(time)

				plot1_dataLine.setData(dataLoadAtime, dataLoadA)
				plot2_dataLine.setData(dataLoadVtime, dataLoadV)
				plot3_dataLine.setData(dataLoadReqWtime, dataLoadReqW)


				loadReqW += stepW

				if self.check_exit(statusLabel): #stop the test
					exportTextEdit.insertHtml('<H2>Měření <B> PŘERUŠENO UŽIVATELEM</B> - naměřená data, '
			       		+ 'grafy a vyhodnocení jsou pouze částečné - jejich vyhodnocení je na uživateli</H2><BR></BR>')
					statusLabel.setText('Test VA char - Stopped by user')
					load.setStateOn(False)
					break

			load.setStateOn(False)

			exportTextEdit.insertHtml('<P>VA charakteristika' + '<BR></BR>')
			img = data2plot2qimg(dataLoadA, dataLoadV, ylabel='Voltage [V]', xlabel='Current [A]', height=400)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			exportTextEdit.insertHtml('<P>Průběh požadovaného výkonu na zátěži během měření (hodí se pro vizuální kontrolu ' +
					'chyb v měření, měl by plynule růst od 0 do 100% Po)<BR></BR>')
			img = data2plot2qimg(dataLoadReqWtime, dataLoadReqW, ylabel='Requested P [W]',
					height=200, formatXasTime=True)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			dataUcinnostP = []
			for i in range(len(dataLoadW)):
				try:
					xP = dataLoadW[i]/dataWmeterW[i]
					if xP > 1:
						print(f'Error: i={i}, dataLoadW[i]={dataLoadW[i]}, dataWmeterW[i]={dataWmeterW[i]}, xp={xP}')
					else:
						dataUcinnostP.append(xP)
				except:
					dataUcinnostP.append(0)
			exportTextEdit.insertHtml('<P>Učinnost vzhledem k zatížení' + '<BR></BR>')
			img = data2plot2qimg(dataLoadW, dataUcinnostP, ylabel='Účinnost [0-1]', xlabel='Measured Power on Load [W]', height=400)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')
			statusLabel.setText('Test VA char.: Finished')
		#endregion

		#region Měření VA charakteristiky při přetížení------------------------------
		if cfg.get('testACDCadapteru/test') in {'All', 'VA char. overcur.'}: 
			statusLabel.setText('Test VA char. overcur.: Started')
			exportTextEdit.insertHtml('<H2>Měření <B>VA charakteristiky při přetížení</B></H2><BR></BR>')
			exportTextEdit.insertHtml('Měří se časový průběh U a I při zátěži od 80% Po' + 
					'až do přetížení plus 0.5 minuty nebo 10*Pa<BR></BR>')

			load.setStateOn(False)
			load.setFunction('CP')
			load.setPower(0)
			QtTest.QTest.qWait(100)
			load.setStateOn(True)

			dataLoadA = []
			dataLoadAtime = []
			dataLoadV = []
			dataLoadVtime = []
			dataLoadW = []
			dataLoadWtime = []
			dataLoadReqW = []
			dataLoadReqWtime = []

			dataWmeterW = []
			dataWmeterWtime = []

			plot1_dataLine = plot_prepare(cfg, plot1, 'Load Measured I [A]')
			plot2_dataLine = plot_prepare(cfg, plot2, 'Load measured U [V]')
			plot3_dataLine = plot_prepare(cfg, plot3, 'Load Requested P [W]')

			xPo = cfg.get('testACDCadapteru/Po')
			loadReqW = xPo*0.5
			overloadedAttempts = 600 #1 minuta
			if wmeter.demo == True:
				stepTime = 1
				stepW = xPo/60 # merime 0,1 minutu
				overloadedAttempts = 10 #10 pokusu => 1s

			else:
				stepTime = 100
				stepW = xPo/600 # merime 1 minutu
				overloadedAttempts = 300 # 300 pokusu => 0.5 minuty

			while loadReqW < xPo*10:
				load.setPower(loadReqW)
				QtTest.QTest.qWait(stepTime)
				
				dataLoadA.append(load.measure('A'))
				dataLoadAtime.append(time.time())
				dataLoadV.append(load.measure('V'))
				dataLoadVtime.append(time.time())
				loadW = load.measure('W')
				dataLoadW.append(loadW)
				dataLoadWtime.append(time.time())
				dataLoadReqW.append(loadReqW)
				dataLoadReqWtime.append(time.time())

				plot1_dataLine.setData(dataLoadAtime, dataLoadA)
				plot2_dataLine.setData(dataLoadVtime, dataLoadV)
				plot3_dataLine.setData(dataLoadReqWtime, dataLoadReqW)

				
				loadReqW += stepW
				if loadW < loadReqW*0.1:
					overloadedAttempts -= 1
					statusLabel.setText(f'Test VA char overload: overloadedAttempts={overloadedAttempts}')
				if overloadedAttempts < 0:
					break

				if self.check_exit(statusLabel): #stop the test and exit
					exportTextEdit.insertHtml('<H2>Měření <B> PŘERUŠENO UŽIVATELEM</B> - naměřená data, '
			       		+ 'grafy a vyhodnocení jsou pouze částečné - jejich vyhodnocení je na uživateli</H2><BR></BR>')
					statusLabel.setText('Test VA char overload - Stopped by user')
					load.setStateOn(False)
					break

			load.setStateOn(False)

			exportTextEdit.insertHtml('<P>Průběh požadovaného výkonu na zátěži (hodí se pro vizuální srovnání a kontrolu ' +
					'chyb v měření. Měl by plynule růst od 50% Po až do přetížení, plus cca 30 sekund.)<BR></BR>')
			img = data2plot2qimg(dataLoadReqWtime, dataLoadReqW, ylabel='Requested P [W]',
					height=200, formatXasTime=True, yMaxInLegend=True)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			exportTextEdit.insertHtml('<P>Průběh změřeného výkonu na zátěži během měření:<BR></BR>')
			img = data2plot2qimg(dataLoadWtime, dataLoadW, ylabel='Measured P [W]',
					height=200, formatXasTime=True, yMaxInLegend=True)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			exportTextEdit.insertHtml('<P>Průběh proudu při přetížení' + '<BR></BR>')
			img = data2plot2qimg(dataLoadAtime, dataLoadA, ylabel='Current [I]', height=400, formatXasTime=True, yMaxInLegend=True)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			exportTextEdit.insertHtml('<P>Průběh napětí při přetížení' + '<BR></BR>')
			img = data2plot2qimg(dataLoadVtime, dataLoadV, ylabel='Voltage [V]', height=400, formatXasTime=True, yMaxInLegend=True)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			statusLabel.setText('Test VA char. overcur.: Finished')
		#endregion Měření VA charakteristiky při přetížení - VA charakteristika a časový průběh U a I

		#region test zkrat ---------------------------------------------------
		if cfg.get('testACDCadapteru/test') in {'All', 'Short'}: 
			statusLabel.setText('Test Short: Started')
			exportTextEdit.insertHtml('<H2>Měření charakteristik při <B>zkratu (Short)</B></H2><BR></BR>')
			exportTextEdit.insertHtml('<P>Na zátěži se nastaví maximální výkon 60A (pokud dá zdroj méně než 60A '
			     + 'tak se pro něj jeví jako zkrat) a měří se časový průběh I a U</P><BR></BR>')

			load.setStateOn(False)
			load.setFunction('CC')
			load.setCurrent(60) # 60A = maximal current of Rigol DL3031

			dataLoadA = []
			dataLoadAtime = []
			dataLoadV = []
			dataLoadVtime = []

			plot1_dataLine = plot_prepare(cfg, plot1, 'Load Measured I [A]')
			plot2_dataLine = plot_prepare(cfg, plot2, 'Load measured U [V]')
			plot3_dataLine = plot_prepare(cfg, plot3, '')


			if load.demo == True:
				tstop = time.time() + 5 # 3 seconds
				stepTime = 5
			else:
				tstop = time.time() + 15 # 30 seconds
				stepTime = 50 # ms
				QtTest.QTest.qWait(100)

			startOnce = True
			while time.time() < tstop:
				loadA = load.measure('A')
				if loadA > 55:
					load.setStateOn(False)
					exportTextEdit.insertHtml('<H2>Test zkratu přerušen - I je větší než 55 A - hrozí poškození zátěže.</H2><BR></BR>')
					statusLabel.setText('Short test stopped - current over 55A')
					break

				dataLoadA.append(loadA)
				dataLoadAtime.append(time.time())
				dataLoadV.append(load.measure('V'))
				dataLoadVtime.append(time.time())

				plot1_dataLine.setData(dataLoadAtime, dataLoadA)
				plot2_dataLine.setData(dataLoadVtime, dataLoadV)

				QtTest.QTest.qWait(stepTime)
				if startOnce:
					load.setStateOn(True)
					startOnce = False

				if self.check_exit(statusLabel): #stop the test and exit
					exportTextEdit.insertHtml('<H2>Měření <B> PŘERUŠENO UŽIVATELEM</B> - naměřená data, '
			       		+ 'grafy a vyhodnocení jsou pouze částečné - jejich vyhodnocení je na uživateli</H2><BR></BR>')
					statusLabel.setText('Short test stopped - by user')
					load.setStateOn(False)
					break

			load.setStateOn(False)

			exportTextEdit.insertHtml('<P>Průběh proudu při zkratu' + '<BR></BR>')
			img = data2plot2qimg(dataLoadAtime, dataLoadA, ylabel='Current [I]', height=400, formatXasTime=True)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			exportTextEdit.insertHtml('<P>Průběh napětí při zkratu' + '<BR></BR>')
			img = data2plot2qimg(dataLoadVtime, dataLoadV, ylabel='Voltage [V]', height=400, formatXasTime=True)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')
			statusLabel.setText('Test Short: Finished')
		#endregion test zkrat


		#region zátěž 1 hodina max.  ---------------------------------------------------
		if cfg.get('testACDCadapteru/test') in {'All', '1 hour load'}: 
			statusLabel.setText('Test 1 hour load: Started')
			exportTextEdit.insertHtml('<H2>Měření chování při <B>zátěži na maximální výkon po dobu 1 hodiny</B></H2><BR></BR>')
			exportTextEdit.insertHtml('<P>Na zátěži se nastaví maximální výkon adaptéru a měří se časový průběh I, U a P po dobu 1 hodina<BR></BR>')
			exportTextEdit.insertHtml('<P>Pokud je vybrána volba Wait on last, měření po 1 hodině pokračuje až do zastavení uživatelem nebo maximálně dalších 8 hodin </P><BR></BR>')

			load.setStateOn(False)
			load.setFunction('CP')
			load.setPower(cfg.get('testACDCadapteru/Po'))
			QtTest.QTest.qWait(100)
			load.setStateOn(True)

			dataLoadA = []
			dataLoadAtime = []
			dataLoadV = []
			dataLoadVtime = []
			dataLoadW = []
			dataLoadWtime = []

			plot1_dataLine = plot_prepare(cfg, plot1, 'Load Measured I [A]')
			plot2_dataLine = plot_prepare(cfg, plot2, 'Load measured U [V]')
			plot3_dataLine = plot_prepare(cfg, plot3, 'Load measured P [W]')

			if load.demo == True:
				tstop = time.time() + 10 # 10 seconds
			else:
				tstop = time.time() + 60*60 # 1 hour
			
			tlabel = 0
			while time.time() < tstop:
				
				dataLoadA.append(load.measure('A'))
				dataLoadAtime.append(time.time())
				dataLoadV.append(load.measure('V'))
				dataLoadVtime.append(time.time())
				dataLoadW.append(load.measure('W'))
				dataLoadWtime.append(time.time())

				plot1_dataLine.setData(dataLoadAtime, dataLoadA)
				plot2_dataLine.setData(dataLoadVtime, dataLoadV)
				plot3_dataLine.setData(dataLoadWtime, dataLoadW)

				if wmeter.demo == True:
					QtTest.QTest.qWait(1)
				else:
					QtTest.QTest.qWait(100)

				if tlabel > 8: #each 9 rounds update label
					tleft = int(tstop-time.time())
					statusLabel.setText(f'Test 1 hour load: {tleft}')
					tlabel = 0
				tlabel += 1

				if self.check_exit(statusLabel): #stop the test and exit
					exportTextEdit.insertHtml('<H2>Měření <B> PŘERUŠENO UŽIVATELEM</B> - naměřená data, '
			       		+ 'grafy a vyhodnocení jsou pouze částečné - jejich vyhodnocení je na uživateli</H2><BR></BR>')
					statusLabel.setText('1 hour load test stopped by user')
					#load.setStateOn(False)
					break

			statusLabel.setText('Test 1 hour load: finished')


			exportTextEdit.insertHtml('<P>Průběh proudu při maximální zátěži po dobu 1 hodina' + '<BR></BR>')
			img = data2plot2qimg(dataLoadAtime, dataLoadA, ylabel='Current [I]', height=400, formatXasTime=True)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			exportTextEdit.insertHtml('<P>Průběh napětí při maximální zátěži po dobu 1 hodina' + '<BR></BR>')
			img = data2plot2qimg(dataLoadVtime, dataLoadV, ylabel='Voltage [V]', height=400, formatXasTime=True)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			exportTextEdit.insertHtml('<P>Průběh výkonu při maximální zátěži po dobu 1 hodina' + '<BR></BR>')
			img = data2plot2qimg(dataLoadWtime, dataLoadW, ylabel='Power [W]', height=400, formatXasTime=True)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')
			statusLabel.setText('Test 1 hour load: Finished')


			if cfg.get('testACDCadapteru/load8h'): # plus next * hours 

				statusLabel.setText('Test 1+8 hour load: Started')

				if load.demo == True:
					tstop = time.time() + 10 # 10 seconds
				else:
					tstop = time.time() + 60*60*8 # 1 hour
				
				tlabel = 0
				while time.time() < tstop:
					
					dataLoadA.append(load.measure('A'))
					dataLoadAtime.append(time.time())
					dataLoadV.append(load.measure('V'))
					dataLoadVtime.append(time.time())
					dataLoadW.append(load.measure('W'))
					dataLoadWtime.append(time.time())

					plot1_dataLine.setData(dataLoadAtime, dataLoadA)
					plot2_dataLine.setData(dataLoadVtime, dataLoadV)
					plot3_dataLine.setData(dataLoadWtime, dataLoadW)

					if wmeter.demo == True:
						QtTest.QTest.qWait(1)
					else:
						QtTest.QTest.qWait(100)

					if tlabel > 8: #each 9 rounds update label
						tleft = int(tstop-time.time())
						statusLabel.setText(f'Test 1+8 hour load: {tleft}')
						tlabel = 0
					tlabel += 1

					if self.check_exit(statusLabel): #stop the test and exit
						statusLabel.setText('Test 1+8 hour load: test stopped by user')
						#load.setStateOn(False)
						break

				statusLabel.setText('Test 1+8 hour load: finished')


			load.setStateOn(False)


		#endregion 




		#finished with no errors
		self.semaphore.tryAcquire(1) #normal exit
		self.semaphore.tryAcquire(1) #user stopped during normal exit
		#statusLabel.setText('Finished')
		if verbose > 150:
			print('TestACDCadapteru-->do_measure Finished')

	
	

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
# pyuic6 mainwindow.ui -o ui_mainwindow.py 
# or if something went wrong with PATH, .... you can use:
# python -m PyQt6.uic.pyuic -x mainwindow.ui -o ui_mainwindow.py 



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

		self.cfg = QSettingsManager()

		self.cfg.set_defaults(CONFIG_DEFAULT)

		self.tabWidget.setCurrentIndex(self.cfg.get('GUI/lastTabIndex'))


		#region CONFIG ----------------------------
		self.tab_Config = Tab_Config(self, self.cfg)

		#endregion


		self.visa = VisaDevice(
			VISAresource=self.cfg.get('VISA/VISAresource')
			, demo = self.cfg.get('VISA/demo'))
		self.tab_visa = Tab_VISA(self, self.cfg, self.visa)

		#region WATTMETER -----------------------------------------------------------------
		self.wattmeter = Wattmeter_GUI(
			VISAresource=self.cfg.get('wattmeter/VISAresource'),
			demo=self.cfg.get('wattmeter/demo'),
			status = self.tab_Wattmeter_widget.ui_status,
			verbose = verbose,
		)

		self.tab_Wattmeter_widget.myinit(cfg=self.cfg, wattmeter=self.wattmeter, export=self.export_textEdit1)

		#endregion 

		#region LOAD -----------------------------------------------------
		self.load = Load_GUI(
			VISAresource=self.cfg.get('load/VISAresource'),
			demo=self.cfg.get('load/demo'),
			status = self.load_status,
			verbose = verbose,
		)
		self.tab_load = Tab_Load(mw = self, cfg=self.cfg, load=self.load, export=self.export_textEdit1)

		#endregion

		#region Netio -------------------------------------------------------------
		self.netio_gui = Netio_GUI(cfg=self.cfg, status=self.netio_status)

		self.tab_netio = Tab_Netio(mw=self, cfg=self.cfg, netio_gui= self.netio_gui, export=self.export_textEdit1)



		#endregion ----------------------------------------------------------------

		#region testACDCadapteru ----------------------------------------------
		self.testACDCadapteru = TestACDCadapteru(self, self.cfg, self.load, self.wattmeter)
		self.cfg.add_handler('testACDCadapteru/Po', self.testACDCadapteru_doubleSpinBox_Po)
		
		self.testACDCadapteru_typAdapteru.addItems(['0: Ignore', '2: Low voltage <6V >=550mA', '3: AC-DC >=6V', '4: Multiple outputs'])
		self.cfg.add_handler('testACDCadapteru/typAdapteru', self.testACDCadapteru_typAdapteru)
		
		#testACDCadapteru_comboBox_typAdapteru
		self.testACDCadapteru_comboBox_test.addItems(['All', 'Pstb', 'Pa', 'VA char.', 'VA char. overcur.', 'Short', '1 hour load'])
		self.cfg.add_handler('testACDCadapteru/test', self.testACDCadapteru_comboBox_test)
		self.testACDCadapteru_pushButton_start.pressed.connect(self.testACDCadapteru_start)
		self.testACDCadapteru_pushButton_stop.pressed.connect(self.testACDCadapteru_stop)
		self.cfg.add_handler('testACDCadapteru/load8h', self.testACDCadapteru_checkBox_load8h)


		#endregion


		#region TEST ZATIZENI -----------------------------------
		#self.config_init()
		self.cfg.add_handler('test_adapteru/reqmAstart', self.spinBox_reqmAstart)
		self.cfg.add_handler('test_adapteru/reqmAstop', self.spinBox_reqmAstop)
		self.cfg.add_handler('test_adapteru/reqmAstep', self.spinBox_reqmAstep)
		self.cfg.add_handler('test_adapteru/time_step_delay', self.spinBox_time_step_delay)
		self.cfg.add_handler('test_adapteru/time_measure_delay', self.spinBox_time_measure_delay)
		self.cfg.add_handler('test_adapteru/stop_mV', self.spinBox_stop_mV)
		self.cfg.add_handler('test_adapteru/stop_mVAttempts', self.spinBox_stop_mVAttempts)
		
		self.loadstop_mVAttempts = self.cfg.get('test_adapteru/stop_mVAttempts')


		self.mplWidget1.myinit()
		#self.mplWidget1.myinit(theme=configCurrent['plots']['theme'])
		self.mplWidget1.plot_init()

		self.timer_test_zatizeni = QtCore.QTimer()
		self.timer_test_zatizeni.timeout.connect(self.test_zatizeni_mereni)


		self.test_zatizeni_running = False
		self.pushButton_test_zatizeni_start.pressed.connect(self.test_zatizeni_start)
		self.pushButton_test_zatizeni_stop.pressed.connect(self.test_zatizeni_stop)
		#endregion

		#region EXPORT -----------------------
		self.export_textEdit1.setPlaceholderText('nothing measured yet...')
		self.export_textEdit1.clear()
		self.export_pushButton_clear.pressed.connect(self.export_textEdit1.clear)
		self.export_pushButton_save_as_text.pressed.connect(self.export_save_as_text)
		self.export_pushButton_save_as_pdf.pressed.connect(self.export_save_as_pdf)
		#endregion

		# COMMENTS -------------------------------
		self.cfg.add_handler('comments/text', self.comments_plainTextEdit)


		tab_help = Tab_help(self)


	def closeEvent(self, event: QCloseEvent):
		if verbose > 100:
			print('GUI closeEvent...')
		self.cfg.set('GUI/lastTabIndex', self.tabWidget.currentIndex())



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
				plot3 = self.testACDCadapteru_plotWidget3,
				statusLabel = self.testACDCadapteru_label_status,
				cfg = self.cfg,
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

		if not self.load.is_connected():
			retCode, retString = self.load.connect()
			if retCode == False:
				return()
		self.load.setFunction('CC')


		self.test_zatizeni_running = True

		self.loadReqmA = 0
		self.load.setFunction('CC')
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
		self.timer_test_zatizeni.setInterval(self.cfg.get('test_adapteru/time_step_delay')) # ms
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


	#region export text
	def export_save_as_text(self):
		dlg = QFileDialog()
		fileName, fileType = dlg.getSaveFileName()
		print(fileName)
		if fileName == '':
			return

		with open(fileName, 'w') as yourFile:
			yourFile.write(str(self.export_textEdit1.toPlainText()))

	#endregion

	#region export pdf
	def export_save_as_pdf(self):
		dlg = QFileDialog()
		#dlg.
		fileName, fileType = dlg.getSaveFileName()
		print(fileName)
		if fileName == '':
			return
		printer = QPrinter()
		#printer.setPageSize(QPageSize.PageSizeId.A4)
		#printer.setPageSize(QPrinter.Unit.Millimeter)
		printer.setResolution(600)
		printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
		printer.setOutputFileName(fileName)
		#paint = QPainter(printer)
		self.export_textEdit1.print(printer)
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