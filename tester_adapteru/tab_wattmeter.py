
import time

import pyqtgraph
from pyqtgraph import mkPen
import pyqtgraph.exporters


from PyQt6.QtWidgets import*
from PyQt6 import QtCore
from PyQt6.QtGui import QImage, QTextCursor, QPageSize, QPixmap, QPainter, QCloseEvent
from PyQt6.QtCore import QCoreApplication, Qt, QFile, QTextStream, QIODevice, QSemaphore, QByteArray

from pyqtconfig import QSettingsManager



from ui_tab_wattmeter import Ui_TabWattmeterContent

import visa_device
from visa_device import VisaDevice

import wattmeter_device
from wattmeter_device import Wattmeter_GUI

#import shared_functions
#from shared_functions import plot_prepare
from shared_functions import *



class Tab_Wattmeter(QWidget, Ui_TabWattmeterContent):

	cfg : QSettingsManager
	wattmeter: Wattmeter_GUI
	export: QTextEdit

	data_W = []
	data_Wtime = []
	data_A = []
	data_Atime = []
	data_V = []
	data_Vtime = []
	data_MATH = []
	data_MATHtime = []

	def __init__(self, parent = None):
		QWidget.__init__(self, parent)
		self.setupUi(self)


	def myinit(self, cfg: QSettingsManager, wattmeter: Wattmeter_GUI, export: QTextEdit):
		self.cfg = cfg
		self.wattmeter = wattmeter
		self.export = export

		self.cfg.add_handler('wattmeter/VISAresource', self.ui_VISAresource)

		self.mereni_timer = QtCore.QTimer()
		self.mereni_timer.timeout.connect(self.wattmeter_mereni_mer)

		self.ui_VISAresource.textChanged.connect(self.wattmeter_VISAresource_changed)
		self.cfg.add_handler('wattmeter/demo', self.ui_demo)
		self.ui_demo.stateChanged.connect(self.wattmeter_demo_pressed)
		self.ui_connect.pressed.connect(self.wattmeter.connect)
		self.ui_disconnect.pressed.connect(self.wattmeter.disconnect)
		self.ui_status.setText('Not connected')

		self.wattmeter_mereni_finished = True # semaphor for measuring method
		self.ui_start.pressed.connect(self.wattmeter_mereni_start)
		self.ui_stop.pressed.connect(self.wattmeter_mereni_stop)
		self.cfg.add_handler('wattmeter/measure_interval', self.ui_measure_interval)
		#self.cfg.add_handler('wattmeter/autorange', self.ui_autorange)
		self.ui_export.pressed.connect(self.wattmeter_mereni_export)
		self.ui_clear_graphs.pressed.connect(self.wattmeter_mereni_clear_graphs)


		self.cfg.add_handler('wattmeter/measure_W', self.ui_measure_W)
		self.ui_measure_W.stateChanged.connect(self.ui_measure_W_changed)
		self.ui_measure_W_changed() # set initial state from config
		self.cfg.add_handler('wattmeter/measure_A', self.ui_measure_A)
		self.ui_measure_A.stateChanged.connect(self.ui_measure_A_changed)
		self.ui_measure_A_changed() # set initial state from config
		self.cfg.add_handler('wattmeter/measure_V', self.ui_measure_V)
		self.ui_measure_V.stateChanged.connect(self.ui_measure_V_changed)
		self.ui_measure_V_changed() # set initial state from config
		self.cfg.add_handler('wattmeter/measure_MATH', self.ui_measure_MATH)
		self.ui_measure_MATH.stateChanged.connect(self.ui_measure_MATH_changed)
		self.ui_measure_MATH_changed() # set initial state from config


		self.plot1_dataLine0, self.plot1_dataLine = plot_prepare(cfg, self.plot1, 'Power/P [W]', addLine2Zero=True)
		self.plot2_dataLine0, self.plot2_dataLine = plot_prepare(cfg, self.plot2, 'Current/I [A]', addLine2Zero=True)
		self.plot3_dataLine0, self.plot3_dataLine = plot_prepare(cfg, self.plot3, 'Voltage/U [V]', addLine2Zero=True)
		self.plot4_dataLine0, self.plot4_dataLine = plot_prepare(cfg, self.plot4, 'AVG Power 10 min./P [W]', addLine2Zero=True)


	def wattmeter_VISAresource_changed(self):
		self.wattmeter.setVISAresource(self.cfg.get('wattmeter/VISAresource'))

	def wattmeter_demo_pressed(self):
		self.wattmeter.disconnect()
		self.ui_status.setText('Disconnected')
		self.ui_status.setStyleSheet('')
		self.wattmeter.setDemo(self.ui_demo.isChecked())


	def ui_measure_W_changed(self):
		if self.cfg.get('wattmeter/measure_W'):
			self.plot1.show()
		else:
			self.plot1.hide()


	def ui_measure_A_changed(self):
		if self.cfg.get('wattmeter/measure_A'):
			self.plot2.show()
		else:
			self.plot2.hide()


	def ui_measure_V_changed(self):
		if self.cfg.get('wattmeter/measure_V'):
			self.plot3.show()
		else:
			self.plot3.hide()


	def ui_measure_MATH_changed(self):
		if self.cfg.get('wattmeter/measure_MATH'):
			self.plot4.show()
		else:
			self.plot4.hide()


	def wattmeter_mereni_start(self):
		self.wattmeter.connect()
		# schedule Measuring
		self.mereni_timer.setInterval(self.cfg.get('wattmeter/measure_interval')) # ms
		self.mereni_timer.start()


	def wattmeter_mereni_stop(self):
		self.mereni_timer.stop()
		self.wattmeter_mereni_finished = True


	def wattmeter_mereni_mer(self):
		if self.wattmeter_mereni_finished == False:
			print('wattmeter_mereni_mer nestiha!!!!!!!!!!')
			return()
		self.wattmeter_mereni_finished = False
		if True: #self.cfg.get('wattmeter/measure_'):
			W = self.wattmeter.measure('W')
			if type(W) is float or int:
				self.data_W.append(W)
				self.data_Wtime.append(time.time())
				self.plot1_dataLine.setData(self.data_Wtime, self.data_W)
				if len(self.data_W) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
					self.plot1_dataLine0.setData([time.time()], [0])


		if True: #self.cfg.get('wattmeter/measure_'):
			A = self.wattmeter.measure('A')
			if type(A) is float or int:
				self.data_A.append(A)
				self.data_Atime.append(time.time())
				self.plot2_dataLine.setData(self.data_Atime, self.data_A)
				if len(self.data_A) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
					self.plot2_dataLine0.setData([time.time()], [0])

		if True: #self.cfg.get('wattmeter/measure_'):
			V = self.wattmeter.measure('V')
			if type(V) is float or int:
				self.data_V.append(V)
				self.data_Vtime.append(time.time())
				self.plot3_dataLine.setData(self.data_Vtime, self.data_V)
				if len(self.data_V) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
					self.plot3_dataLine0.setData([time.time()], [0])

		if True: #self.cfg.get('wattmeter/measure_'):
			MATH = self.wattmeter.measure('MATH')
			if type(MATH) is float or int:
				self.data_MATH.append(MATH)
				self.data_MATHtime.append(time.time())
				self.plot4_dataLine.setData(self.data_MATHtime, self.data_MATH)
				if len(self.data_MATH) == 1: #at begin of measuring we add 0 to line2 to force autorange work from 0
					self.plot4_dataLine0.setData([time.time()], [0])

		self.wattmeter_mereni_finished = True

	#region wattmeter_mereni_export
	def wattmeter_mereni_export(self):
		self.export.insertHtml('<BR></BR><H1>Export naměřených hodnot wattmetrem</H1><BR></BR>')
		CSVDELIM = self.cfg.get('export/CSVDELIM')
		if self.cfg.get('wattmeter/measure_W'):
			self.export.insertHtml('<H2>Výkon [W]</H2><BR></BR>')
			self.export.append(f'Time [seconds since 1970]{CSVDELIM}P [W]')
			for i in range(len(self.data_W)):
				self.export.append(
					str(self.data_Wtime[i])+CSVDELIM+
					str(self.data_W[i])
				)
			self.export.append('')
			self.export.insertHtml('<BR></BR>')


		if self.cfg.get('wattmeter/measure_A'):
			self.export.insertHtml('<H2>Proud [A]</H2><BR></BR>')
			self.export.append(f'Time [seconds since 1970]{CSVDELIM}I [A]')
			for i in range(len(self.data_A)):
				self.export.append(
					str(self.data_Atime[i])+CSVDELIM+
					str(self.data_A[i])
				)
			self.export.append('')
			self.export.insertHtml('<BR></BR>')

		if self.cfg.get('wattmeter/measure_V'):
			self.export.insertHtml('<H2>Napětí [V]</H2><BR></BR>')
			self.export.append(f'Time [seconds since 1970]{CSVDELIM}U [V]')
			for i in range(len(self.data_V)):
				self.export.append(
					str(self.data_Vtime[i])+CSVDELIM+
					str(self.data_V[i])
				)
			self.export.append('')
			self.export.insertHtml('<BR></BR>')

		if self.cfg.get('wattmeter/measure_MATH'):
			self.data_MATH
			self.data_MATHtime
			self.export.insertHtml('<H2>MATH - Energie [W]</H2><BR></BR>')
			self.export.append(f'Time [seconds since 1970]{CSVDELIM}MATH [W]')
			for i in range(len(self.data_MATH)):
				self.export.append(
					str(self.data_MATHtime[i])+CSVDELIM+
					str(self.data_MATH[i])
				)
			self.export.append('')
			self.export.insertHtml('<BR></BR>')
	#endregion wattmeter_mereni_export


	def wattmeter_mereni_clear_graphs(self):
		self.data_W = []
		self.data_Wtime = []
		self.data_A = []
		self.data_Atime = []
		self.data_V = []
		self.data_Vtime = []
		self.data_MATH = []
		self.data_MATHtime = []

		self.plot1_dataLine.setData([], [])
		self.plot2_dataLine.setData([], [])
		self.plot3_dataLine.setData([], [])
		self.plot4_dataLine.setData([], [])
