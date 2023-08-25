#!python3

verbose =80


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

from visa_device import VisaDevice

from wattmeter_device import Wattmeter_GUI

from ui_mainwindow import Ui_MainWindow


###### GLOBAL variables - config ####################################################

CONFIG_DEFAULT = {
					'GUI/theme': 'auto', #auto, dark, light
					'GUI/lastTabIndex' : 1,
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
					'testACDCadapteru/Po':  1, #W
					'testACDCadapteru/Vmax':  10, #V - Maximální/nominální napětí zdroje
					'testACDCadapteru/test': 'All',
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

#data_wattmeter_W = []
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




class Load(VisaDevice):

	def measure(self, varName):
		#return(False | float)
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
			if verbose > 100:
				print('PVcommand = '+PVcommand)
			VisaDevice.write(self, PVcommand)

	def setPower(self, current):
		if  self.demo == True:
			return()
		else:
			PVcommand = ':SOURCE:POWer:LEVEL:IMMEDIATE ' + str(current)
			if verbose > 100:
				print('PVcommand = '+PVcommand)
			VisaDevice.write(self, PVcommand)

class Load_GUI(Load):
	def __init__(self, VISAresource: str, demo: bool, status: QtWidgets.QTextEdit):
		Load. VISAresource = VISAresource
		Load.demo = demo
		self.status = status

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
		self.mw.config_plainTextEdit.setPlaceholderText('Config not read yet...')
		self.cfg.updated.connect(self.config_show)
		self.config_show()
		self.mw.config_pushButton_ClearToDefault.clicked.connect(self.config_set_to_default)

		self.mw.config_comboBox_GUItheme.addItems(('auto', 'dark', 'light'))
		self.cfg.add_handler('GUI/theme', self.mw.config_comboBox_GUItheme)
		self.config_GUItheme_changed()
		mw.config_comboBox_GUItheme.currentTextChanged.connect(self.config_GUItheme_changed)

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
		try:
			if theme == 'auto':
				if darkdetect.isDark():
					theme = 'dark'
				else:
					theme = 'light'
			if theme == 'light':
				self.mw.wattmeter_plotWidget1.setBackground("w")
				self.mw.wattmeter_plotWidget2.setBackground("w")
				self.mw.wattmeter_plotWidget3.setBackground("w")
				self.mw.wattmeter_plotWidget4.setBackground("w")
				self.mw.load_plotWidget1.setBackground("w")
				self.mw.load_plotWidget2.setBackground("w")
				self.mw.load_plotWidget3.setBackground("w")
				self.mw.load_plotWidget4.setBackground("w")
				self.mw.testACDCadapteru_plotWidget1.setBackground("w")
				self.mw.testACDCadapteru_plotWidget2.setBackground("w")
				self.mw.testACDCadapteru_plotWidget3.setBackground("w")
			else:
				self.mw.wattmeter_plotWidget1.setBackground("k")
				self.mw.wattmeter_plotWidget2.setBackground("k")
				self.mw.wattmeter_plotWidget3.setBackground("k")
				self.mw.wattmeter_plotWidget4.setBackground("k")
				self.mw.load_plotWidget1.setBackground("k")
				self.mw.load_plotWidget2.setBackground("k")
				self.mw.load_plotWidget3.setBackground("k")
				self.mw.load_plotWidget4.setBackground("k")
				self.mw.testACDCadapteru_plotWidget1.setBackground("k")
				self.mw.testACDCadapteru_plotWidget2.setBackground("k")
				self.mw.testACDCadapteru_plotWidget3.setBackground("k")
		except:
			None
	#endregion



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
		dataX, dataY,
		width = 600,
		height = 400, 
		xlabel ='', 
		ylabel = '', 
		title = '',
		formatXasTime = False, # on X axis is unix timestamps and will be converted as H:M:S
		**kwargs):
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
			self.semaphore.tryAcquire(2)
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


		if wmeter.is_connected() == False:
			retCode, retString = wmeter.connect()
			if not retCode:
				statusLabel.setText('Failed to connect Wattmeter')
				self.semaphore.tryAcquire(1)
				return(False)
		rc, rs = wmeter.query('*IDN?')
		exportTextEdit.insertHtml('<P>Wattmeter IDN: ' + rs + '</P><BR></BR>')

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
					wmeter.integrateReset()
					break

			if not iState.startswith('TIM'): # failed to measure
				exportTextEdit.insertHtml('<H2>Měření Pstb selhalo, zobrazené hodnoty jsou pro kratší čas než požadovaný</H2><BR></BR>')
				statusLabel.setText('Test Pstb - Failed')


			#Pstb = ldata_wattmeter_MATH[-1] 
			vPstb = wmeter.measureNoNAN('MATH')
			wmeter.integrateReset()
			exportTextEdit.insertHtml(f'<H3>Standby příkon adaptéru - <B>Pstb</B>: {vPstb:.4f} W</H3><BR></BR>')
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
			vPo = cfg.get('testACDCadapteru/Po')
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
			exportTextEdit.insertHtml('<H4>Průměrná účinnost při malém zatížení (10%) - <B>P10 = </B>' +
					str(xP10) + '</H4><BR></BR>')


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
					'<TR><TD>25%</TD><TD>' + str(vPo*0.25) + '</TD><TD>' + str(loadW25) + '</TD>' +
						'<TD>' + str(wmeterW25) + '</TD><TD>' + str(xP25) + '</TD></TR>'
					'<TR><TD>50%</TD><TD>' + str(vPo*0.5) + '</TD><TD>' + str(loadW50) + '</TD>' +
						'<TD>' + str(wmeterW50) + '</TD><TD>' + str(xP50) + '</TD></TR>'
					'<TR><TD>75%</TD><TD>' + str(vPo*0.75) + '</TD><TD>' + str(loadW75) + '</TD>' +
						'<TD>' + str(wmeterW75) + '</TD><TD>' + str(xP75) + '</TD></TR>'
					'<TR><TD>100%</TD><TD>' + str(vPo) + '</TD><TD>' + str(loadW100) + '</TD>' +
						'<TD>' + str(wmeterW100) + '</TD><TD>' + str(xP100) + '</TD></TR>'
				'</TABLE><BR></BR>')
			exportTextEdit.insertHtml('<H3>Průměrná účinnost v aktivním režimu - <B>Pa = </B>' +
					str(vPa) + '</H3><BR></BR>')
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


			exportTextEdit.insertHtml('<P>VA charakteristika' + '<BR></BR>')
			img = data2plot2qimg(dataLoadA, dataLoadV, ylabel='Voltage [V]', xlabel='Current [A]', height=400)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			exportTextEdit.insertHtml('<P>Průběh požadovaného výkonu na zátěži během měření (hodí se pro vizuální kontrolu ' +
					'chyb v měření, měl by plynule růst od 0 do 110% Po)<BR></BR>')
			img = data2plot2qimg(dataLoadReqWtime, dataLoadReqW, ylabel='Requested P [W]',
					height=200, formatXasTime=True)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			dataUcinnostP = []
			for i in range(len(dataLoadW)):
				try:
					xP = dataLoadW[i]/dataWmeterW[i]
					if xP > 1:
						print(f'Error: i={i}, dataLoadW[i]={dataLoadW[i]}, dataWmeterW[i]={dataWmeterW[i]}, xp={xp}')
					else:
						dataUcinnostP.append(xP)
				except:
					dataUcinnostP.append(0)
			exportTextEdit.insertHtml('<P>Učinnost vzhledem k zatížení' + '<BR></BR>')
			img = data2plot2qimg(dataLoadW, dataUcinnostP, ylabel='Účinnost [0-1]', xlabel='Power [W]', height=400)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')
			statusLabel.setText('Test VA char.: Finished')
		#endregion

		#region Měření VA charakteristiky při přetížení------------------------------
		if cfg.get('testACDCadapteru/test') in {'All', 'VA char. overcur.'}: 
			statusLabel.setText('Test VA char. overcur.: Started')
			exportTextEdit.insertHtml('<H2>Měření <B>VA charakteristiky při přetížení</B></H2><BR></BR>')
			exportTextEdit.insertHtml('Měří se časový průběh U a I při zátěži od 80% Po' + 
					'až do přetížení plus 0.5 minuty nebo 10*Pa')

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
					height=200, formatXasTime=True)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			exportTextEdit.insertHtml('<P>Průběh změřeného výkonu na zátěži během měření:<BR></BR>')
			img = data2plot2qimg(dataLoadWtime, dataLoadW, ylabel='Measured P [W]',
					height=200, formatXasTime=True)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			exportTextEdit.insertHtml('<P>Průběh proudu při přetížení' + '<BR></BR>')
			img = data2plot2qimg(dataLoadAtime, dataLoadA, ylabel='Current [I]', height=400, formatXasTime=True)
			textEditAppendImg(exportTextEdit, img)
			exportTextEdit.insertHtml('</P>')

			exportTextEdit.insertHtml('<P>Průběh napětí při přetížení' + '<BR></BR>')
			img = data2plot2qimg(dataLoadVtime, dataLoadV, ylabel='Voltage [V]', height=400, formatXasTime=True)
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
				tstop = time.time() + 10 # 3 seconds
				stepTime = 5
			else:
				tstop = time.time() + 30 # 30 seconds
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
					statusLabel.setText('Short test stopped - current over 55A')
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
			statusLabel.setText('Test Short: Started')
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

			load.setStateOn(False)
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
		#endregion 

		#region Load +8 hodin





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

		self.stop = False  #stop semaphore for running tests

		self.cfg = QSettingsManager()

		self.cfg.set_defaults(CONFIG_DEFAULT)
		self.tab_Config = Tab_Config(self, self.cfg)

		self.tabWidget.setCurrentIndex(self.cfg.get('GUI/lastTabIndex'))

		#region CONFIG ----------------------------

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

		#region for all pyqt graphs in this app:
		self.penColor = color=(205, 205, 205)
		self.pen = pyqtgraph.mkPen(self.penColor, width=1)
		self.cursor = Qt.CursorShape.CrossCursor
		plotMinW = self.cfg.get('plots/minWidth')
		plotMinH = self.cfg.get('plots/minHeight')
      # https://www.geeksforgeeks.org/pyqtgraph-symbols/
		#endregion

		self.visa = VisaDevice(
			VISAresource=self.cfg.get('VISA/VISAresource')
			, demo = self.cfg.get('VISA/demo'))
		self.tab_visa = Tab_VISA(self, self.cfg, self.visa)

		#region WATTMETER -----------------------------------------------------------------
		self.wattmeter = Wattmeter_GUI(
			VISAresource=self.cfg.get('wattmeter/VISAresource'),
			demo=self.cfg.get('wattmeter/demo'),
			status = self.tab_Wattmeter_widget.ui_status
		)

		self.tab_Wattmeter_widget.myinit(cfg=self.cfg, wattmeter=self.wattmeter, export=self.export_textEdit1)

		#endregion 

		#region LOAD -----------------------------------------------------
		self.load = Load_GUI(
			VISAresource=self.cfg.get('load/VISAresource'),
			demo=self.cfg.get('load/demo'),
			status = self.load_label_status,
		)
		self.timer_load_mereni = QtCore.QTimer()

		self.cfg.add_handler('load/VISAresource', self.load_lineEdit_VISAresource)
		self.load_lineEdit_VISAresource.textChanged.connect(self.load_VISAresource_changed)
		self.cfg.add_handler('load/demo', self.load_checkBox_demo)
		self.load_checkBox_demo.stateChanged.connect(self.load_demo_pressed)
		self.load_pushButton_connect.pressed.connect(self.load.connect)
		self.load_pushButton_disconnect.pressed.connect(self.load.disconnect)
		self.load_pushButton_StateON.pressed.connect(self.load_pushButton_StateON_pressed)
		self.load_pushButton_StateOFF.pressed.connect(self.load_pushButton_StateOFF_pressed)
		
		# LOAD Rem. Ctrl.
		self.load_radioButton_Mode_CC.pressed.connect(self.load_radioButton_Mode_CC_pressed)
		self.load_radioButton_Mode_BATT.pressed.connect(self.load.setModeBATT)
		self.load_doubleSpinBox_BATT_current.valueChanged.connect(self.load_doubleSpinBox_BATT_current_changed)
		self.load_radioButton_BATT_range_6A.pressed.connect( self.load_radioButton_BATT_range_6A_connect )
		self.load_radioButton_BATT_range_60A.pressed.connect(self.load_radioButton_BATT_range_60A_connect)
		self.load_doubleSpinBox_BATT_vstop.valueChanged.connect(self.load_doubleSpinBox_BATT_vstop_changed)

		# LOAD Measure
		self.load_pushButton_mereni_start.pressed.connect(self.load_mereni_start)
		self.load_pushButton_mereni_stop.pressed.connect(self.load_mereni_stop)
		self.load_pushButton_export.pressed.connect(self.load_mereni_export)

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
		self.load_plotWidget1_dataLine2 = self.load_plotWidget1.plot([], [], symbol='+', symbolSize = 0)

		self.load_plotWidget2.setMinimumSize(300, 200)
		self.load_plotWidget2.showGrid(x=True, y=True)
		daxis2 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
		self.load_plotWidget2.setAxisItems({"bottom": daxis2})
		self.load_plotWidget2_dataLine =  self.load_plotWidget2.plot([], [],
			symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=self.pen)
		self.load_plotWidget2.setLabel('left', 'Voltage/U [V]')
		self.load_plotWidget2.setCursor(self.cursor)
		self.load_plotWidget2_dataLine2 = self.load_plotWidget2.plot([], [], symbol='+', symbolSize = 0)
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
		self.load_plotWidget3_dataLine2 = self.load_plotWidget3.plot([], [], symbol='+', symbolSize = 0)

		self.load_plotWidget4.setMinimumSize(300, 200)
		self.load_plotWidget4.showGrid(x=True, y=True)
		daxis4 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
		self.load_plotWidget4.setAxisItems({"bottom": daxis4})
		self.load_plotWidget4_dataLine =  self.load_plotWidget4.plot([], [],
			symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=self.pen)
		self.load_plotWidget4.setLabel('left', 'Capacity [Wh]')
		self.load_plotWidget4.setCursor(self.cursor)
		self.load_plotWidget4_dataLine2 = self.load_plotWidget4.plot([], [], symbol='+', symbolSize = 0)

		#endregion


		#region testACDCadapteru ----------------------------------------------
		self.testACDCadapteru = TestACDCadapteru(self, self.cfg, self.load, self.wattmeter)
		self.cfg.add_handler('testACDCadapteru/Po', self.testACDCadapteru_doubleSpinBox_Po)
		#testACDCadapteru_comboBox_typAdapteru
		self.testACDCadapteru_pushButton_start.pressed.connect(self.testACDCadapteru_start)
		self.testACDCadapteru_pushButton_stop.pressed.connect(self.testACDCadapteru_stop)
		self.testACDCadapteru_comboBox_test.addItems(['All', 'Pstb', 'Pa', 'VA char.', 'VA char. overcur.', 'Short', '1 hour load'])
		self.cfg.add_handler('testACDCadapteru/test', self.testACDCadapteru_comboBox_test)
		#endregion


		#region TEST ZATIZENI -----------------------------------
		self.mplWidget1.myinit()
		#self.mplWidget1.myinit(theme=configCurrent['plots']['theme'])
		self.mplWidget1.plot_init()

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


	#region classes for wattmeter ------------------------------
	'''
	def wattmeter_VISAresource_changed(self):
		self.wattmeter.setVISAresource(self.cfg.get('wattmeter/VISAresource'))

	def wattmeter_demo_pressed(self):
		self.wattmeter.disconnect()
		self.wattmeter_lineEdit_status.setText('Disconnected')
		self.wattmeter_lineEdit_status.setStyleSheet('')
		self.wattmeter.setDemo(self.wattmeter_checkBox_demo.isChecked())


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
		self.wattmeter.connect()
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
			if type(W) is float or int:
				data_wattmeter_W.append(W)
				data_wattmeter_Wtime.append(time.time())
				self.wattmeter_plotWidget1_dataLine.setData(data_wattmeter_Wtime, data_wattmeter_W)
				if len(data_wattmeter_W) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
					self.wattmeter_plotWidget1_dataLine2.setData([time.time()], [0])


		if True: #self.cfg.get('wattmeter/measure_'):
			A = self.wattmeter.measure('A')
			if type(A) is float or int:
				data_wattmeter_A.append(A)
				data_wattmeter_Atime.append(time.time())
				self.wattmeter_plotWidget2_dataLine.setData(data_wattmeter_Atime, data_wattmeter_A)
				if len(data_wattmeter_A) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
					self.wattmeter_plotWidget2_dataLine2.setData([time.time()], [0])

		if True: #self.cfg.get('wattmeter/measure_'):
			V = self.wattmeter.measure('V')
			if type(V) is float or int:
				data_wattmeter_V.append(V)
				data_wattmeter_Vtime.append(time.time())
				self.wattmeter_plotWidget3_dataLine.setData(data_wattmeter_Vtime, data_wattmeter_V)
				if len(data_wattmeter_V) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
					self.wattmeter_plotWidget3_dataLine2.setData([time.time()], [0])

		if True: #self.cfg.get('wattmeter/measure_'):
			MATH = self.wattmeter.measure('MATH')
			if type(MATH) is float or int:
				data_wattmeter_MATH.append(MATH)
				data_wattmeter_MATHtime.append(time.time())
				self.wattmeter_plotWidget4_dataLine.setData(data_wattmeter_MATHtime, data_wattmeter_MATH)
				if len(data_wattmeter_MATH) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
					self.wattmeter_plotWidget4_dataLine2.setData([time.time()], [0])

		self.wattmeter_mereni_finished = True

	#region wattmeter_mereni_export
	def wattmeter_mereni_export(self):
		self.export_textEdit1.insertHtml('<BR></BR><H1>Export naměřených hodnot wattmetrem</H1><BR></BR>')
		CSVDELIM = self.cfg.get('export/CSVDELIM')
		if self.cfg.get('wattmeter/measure_W'):
			self.export_textEdit1.insertHtml('<H2>Výkon [W]</H2><BR></BR>')
			self.export_textEdit1.append(f'Time [seconds since 1970]{CSVDELIM}P [W]')
			for i in range(len(data_wattmeter_W)):
				self.export_textEdit1.append(
					str(data_wattmeter_Wtime[i])+CSVDELIM+
					str(data_wattmeter_W[i])
				)
			self.export_textEdit1.append('')
			self.export_textEdit1.insertHtml('<BR></BR>')


		if self.cfg.get('wattmeter/measure_A'):
			self.export_textEdit1.insertHtml('<H2>Proud [A]</H2><BR></BR>')
			self.export_textEdit1.append(f'Time [seconds since 1970]{CSVDELIM}I [A]')
			for i in range(len(data_wattmeter_A)):
				self.export_textEdit1.append(
					str(data_wattmeter_Atime[i])+CSVDELIM+
					str(data_wattmeter_A[i])
				)
			self.export_textEdit1.append('')
			self.export_textEdit1.insertHtml('<BR></BR>')

		if self.cfg.get('wattmeter/measure_V'):
			self.export_textEdit1.insertHtml('<H2>Napětí [V]</H2><BR></BR>')
			self.export_textEdit1.append(f'Time [seconds since 1970]{CSVDELIM}U [V]')
			for i in range(len(data_wattmeter_V)):
				self.export_textEdit1.append(
					str(data_wattmeter_Vtime[i])+CSVDELIM+
					str(data_wattmeter_V[i])
				)
			self.export_textEdit1.append('')
			self.export_textEdit1.insertHtml('<BR></BR>')

		if self.cfg.get('wattmeter/measure_MATH'):
			data_wattmeter_MATH
			data_wattmeter_MATHtime
			self.export_textEdit1.insertHtml('<H2>MATH - Energie [W]</H2><BR></BR>')
			self.export_textEdit1.append(f'Time [seconds since 1970]{CSVDELIM}MATH [W]')
			for i in range(len(data_wattmeter_MATH)):
				self.export_textEdit1.append(
					str(data_wattmeter_MATHtime[i])+CSVDELIM+
					str(data_wattmeter_MATH[i])
				)
			self.export_textEdit1.append('')
			self.export_textEdit1.insertHtml('<BR></BR>')
	#endregion wattmeter_mereni_export


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
'''
	#endregion

	#region classes for LOAD ------------------------------
	def load_VISAresource_changed(self):
			self.load.setVISAresource(self.cfg.get('load/VISAresource'))

	def load_demo_pressed(self):
		self.load.disconnect()
		self.load_label_status.setText('Disconnected')
		self.load_label_status.setStyleSheet('')
		self.load.setDemo(self.cfg.get('load/demo'))


	def load_radioButton_Mode_CC_pressed(self):
		self.load.load.setFunction('CC')
	
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

	def load_mereni_start(self):
		if  self.load.is_connected() == False:
			self.load.connect()
		#self.label_test_zatizeni.setText('Measuring')
		#self.label_test_zatizeni.setStyleSheet('color:green')

		# schedule Measuring
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
			if len(data_loadA) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
				self.load_plotWidget1_dataLine2.setData([time.time()], [0])

		if self.cfg.get('load/measure_V'):
			global data_loadV
			loadV = self.load.measure('V')
			data_loadV.append(loadV)
			data_loadVtime.append(time.time())
			self.load_plotWidget2_dataLine.setData(data_loadVtime, data_loadV)
			if len(data_loadV) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
				self.load_plotWidget2_dataLine2.setData([time.time()], [0])

		if self.cfg.get('load/measure_W'):
			global data_loadW
			loadW = self.load.measure('W')
			data_loadW.append(loadW)
			data_loadWtime.append(time.time())
			self.load_plotWidget3_dataLine.setData(data_loadWtime, data_loadW)
			if len(data_loadW) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
				self.load_plotWidget3_dataLine2.setData([time.time()], [0])

		if self.cfg.get('load/measure_Wh'):
			global data_loadWh
			loadWh = self.load.measure('Wh')
			data_loadWh.append(loadWh)
			data_loadWhtime.append(time.time())
			self.load_plotWidget4_dataLine.setData(data_loadWhtime, data_loadWh)
			if len(data_loadWh) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
				self.load_plotWidget4_dataLine2.setData([time.time()], [0])

		self.load_mereni_finished = True

	def load_mereni_export(self):
		self.export_textEdit1.insertHtml('<BR></BR><H1>Export naměřených hodnot zátěže</H1><BR></BR>')
		CSVDELIM = self.cfg.get('export/CSVDELIM')

		if self.cfg.get('load/measure_A'):
			self.export_textEdit1.insertHtml('<H2>Proud [A]</H2><BR></BR>')
			self.export_textEdit1.append(f'Time [seconds since 1970]{CSVDELIM}I [A]')
			for i in range(len(data_loadA)):
				self.export_textEdit1.append(
					str(data_loadAtime[i])+CSVDELIM+
					str(data_loadA[i])
				)
			self.export_textEdit1.append('')
			self.export_textEdit1.insertHtml('<BR></BR>')

		if self.cfg.get('load/measure_V'):
			self.export_textEdit1.insertHtml('<H2>Napětí [V]</H2><BR></BR>')
			self.export_textEdit1.append(f'Time [seconds since 1970]{CSVDELIM}U [V]')
			for i in range(len(data_loadV)):
				self.export_textEdit1.append(
					str(data_loadVtime[i])+CSVDELIM+
					str(data_loadV[i])
				)
			self.export_textEdit1.append('')
			self.export_textEdit1.insertHtml('<BR></BR>')

		if self.cfg.get('load/measure_W'):
			self.export_textEdit1.insertHtml('<H2>Výkon [W]</H2><BR></BR>')
			self.export_textEdit1.append(f'Time [seconds since 1970]{CSVDELIM}P [W]')
			for i in range(len(data_loadW)):
				self.export_textEdit1.append(
					str(data_loadWtime[i])+CSVDELIM+
					str(data_loadW[i])
				)
			self.export_textEdit1.append('')
			self.export_textEdit1.insertHtml('<BR></BR>')

		if self.cfg.get('load/measure_Wh'):
			self.export_textEdit1.insertHtml('<H2>Energie [Wh]</H2><BR></BR>')
			self.export_textEdit1.append(f'Time [seconds since 1970]{CSVDELIM} [Wh]')
			for i in range(len(data_loadWh)):
				self.export_textEdit1.append(
					str(data_loadWhtime[i])+CSVDELIM+
					str(data_loadWh[i])
				)
			self.export_textEdit1.append('')
			self.export_textEdit1.insertHtml('<BR></BR>')

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