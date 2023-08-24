
import time

from pyqtconfig import QSettingsManager

import pyqtgraph
from pyqtgraph import mkPen
import pyqtgraph.exporters


from PyQt6.QtWidgets import*
from PyQt6 import QtCore

from ui_tab_wattmeter import Ui_TabWattmeterContent


import visa_device
from visa_device import VisaDevice

import wattmeter_device
from wattmeter_device import Wattmeter_GUI


class Tab_Wattmeter(QWidget, Ui_TabWattmeterContent):
    cfg : QSettingsManager

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        print('XX1')


    def myinit(self, cfg: QSettingsManager, wattmeter: Wattmeter_GUI):
        print('XX2')
        self.cfg = cfg
        self.wattmeter = wattmeter
        print(self.cfg.get('wattmeter/VISAresource'))
        self.cfg.add_handler('wattmeter/VISAresource', self.ui_VISAresource)

        self.ui_VISAresource.textChanged.connect(self.wattmeter_VISAresource_changed)
        self.cfg.add_handler('wattmeter/demo', self.ui_demo)
        self.ui_demo.stateChanged.connect(self.wattmeter_demo_pressed)
        self.ui_connect.pressed.connect(self.wattmeter.connect)
        self.ui_disconnect.pressed.connect(self.wattmeter.disconnect)


    def xxx(self):
        #self.cfg.add_handler('wattmeter/VISAresource', self.wattmeter_lineEdit_VISAresource)
        #self.wattmeter_lineEdit_VISAresource.textChanged.connect(self.wattmeter_VISAresource_changed)
        #self.cfg.add_handler('wattmeter/demo', self.wattmeter_checkBox_demo)
        #self.wattmeter_checkBox_demo.stateChanged.connect(self.wattmeter_demo_pressed)
        #self.wattmeter_pushButton_connect.pressed.connect(self.wattmeter.connect)
        #self.wattmeter_pushButton_disconnect.pressed.connect(self.wattmeter.disconnect)

        # Wattmeter Measure
        self.wattmeter_mereni_finished = True # semaphor for measuring method
        self.wattmeter_pushButton_start.pressed.connect(self.wattmeter_mereni_start)
        self.wattmeter_pushButton_stop.pressed.connect(self.wattmeter_mereni_stop)
        self.cfg.add_handler('wattmeter/measure_interval', self.wattmeter_spinBox_measure_interval)
        #self.cfg.add_handler('wattmeter/autorange', self.wattmeter_checkBox_autorange)
        self.wattmeter_pushButton_export.pressed.connect(self.wattmeter_mereni_export)
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
        #line2 contains just 0 to force autorange go from 0
        self.wattmeter_plotWidget1_dataLine2 = self.wattmeter_plotWidget1.plot([], [], symbol='+', symbolSize = 0)

        # plotWidget2 / A
        self.wattmeter_plotWidget2.setMinimumSize(plotMinW, plotMinH)
        self.wattmeter_plotWidget2.showGrid(x=True, y=True)
        wattmeter_daxis1 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
        self.wattmeter_plotWidget2.setAxisItems({"bottom": wattmeter_daxis1})
        self.wattmeter_plotWidget2.setLabel('left', 'Current/I [A]')
        self.wattmeter_plotWidget2.setCursor(self.cursor)
        self.wattmeter_plotWidget2_dataLine =  self.wattmeter_plotWidget2.plot([], [],
            'Current/I [A]', symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=self.pen)
        self.wattmeter_plotWidget2_dataLine2 = self.wattmeter_plotWidget2.plot([], [], symbol='+', symbolSize = 0)

        # plotWidget3 / U
        self.wattmeter_plotWidget3.setMinimumSize(plotMinW, plotMinH)
        self.wattmeter_plotWidget3.showGrid(x=True, y=True)
        wattmeter_daxis1 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
        self.wattmeter_plotWidget3.setAxisItems({"bottom": wattmeter_daxis1})
        self.wattmeter_plotWidget3.setLabel('left', 'Voltage/U [V]')
        self.wattmeter_plotWidget3.setCursor(self.cursor)
        self.wattmeter_plotWidget3_dataLine =  self.wattmeter_plotWidget3.plot([], [],
            'Voltage/U [V]', symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=self.pen)
        self.wattmeter_plotWidget3_dataLine2 = self.wattmeter_plotWidget3.plot([], [], symbol='+', symbolSize = 0)

        # plotWidget4 / MATH
        self.wattmeter_plotWidget4.setMinimumSize(plotMinW, plotMinH)
        self.wattmeter_plotWidget4.showGrid(x=True, y=True)
        wattmeter_daxis1 = pyqtgraph.graphicsItems.DateAxisItem.DateAxisItem(orientation='bottom')
        self.wattmeter_plotWidget4.setAxisItems({"bottom": wattmeter_daxis1})
        self.wattmeter_plotWidget4.setLabel('left', 'AVG Power 10 min./P [W]')
        self.wattmeter_plotWidget4.setCursor(self.cursor)
        self.wattmeter_plotWidget4_dataLine =  self.wattmeter_plotWidget4.plot([], [],
            'AVG Power 19 min./P [W]', symbol='o', symbolSize = 5, symbolBrush =(0, 114, 189), pen=self.pen)
        self.wattmeter_plotWidget4_dataLine2 = self.wattmeter_plotWidget4.plot([], [], symbol='+', symbolSize = 0)


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
