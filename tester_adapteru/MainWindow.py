# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(629, 466)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_config = QtWidgets.QWidget()
        self.tab_config.setObjectName("tab_config")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_config)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.config_pushButton_ClearToDefault = QtWidgets.QPushButton(parent=self.tab_config)
        self.config_pushButton_ClearToDefault.setObjectName("config_pushButton_ClearToDefault")
        self.gridLayout.addWidget(self.config_pushButton_ClearToDefault, 0, 0, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout)
        self.config_plainTextEdit = QtWidgets.QPlainTextEdit(parent=self.tab_config)
        self.config_plainTextEdit.setObjectName("config_plainTextEdit")
        self.verticalLayout_6.addWidget(self.config_plainTextEdit)
        self.tabWidget.addTab(self.tab_config, "")
        self.tab_console = QtWidgets.QWidget()
        self.tab_console.setObjectName("tab_console")
        self.tabWidget.addTab(self.tab_console, "")
        self.tab_Load = QtWidgets.QWidget()
        self.tab_Load.setObjectName("tab_Load")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_Load)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(parent=self.tab_Load)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.load_lineEdit_VISAresource = QtWidgets.QLineEdit(parent=self.tab_Load)
        self.load_lineEdit_VISAresource.setObjectName("load_lineEdit_VISAresource")
        self.horizontalLayout.addWidget(self.load_lineEdit_VISAresource)
        self.verticalLayout_7.addLayout(self.horizontalLayout)
        self.verticalLayout_8.addLayout(self.verticalLayout_7)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.tab_Load)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_5.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.tab_Load)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_5.addWidget(self.pushButton_5)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_5)
        self.verticalLayout_8.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_3 = QtWidgets.QLabel(parent=self.tab_Load)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_6.addWidget(self.label_3)
        self.load_label_status = QtWidgets.QLabel(parent=self.tab_Load)
        self.load_label_status.setObjectName("load_label_status")
        self.horizontalLayout_6.addWidget(self.load_label_status)
        self.verticalLayout_8.addLayout(self.horizontalLayout_6)
        self.widget = QtWidgets.QWidget(parent=self.tab_Load)
        self.widget.setObjectName("widget")
        self.verticalLayout_8.addWidget(self.widget)
        self.verticalLayout_8.setStretch(3, 10)
        self.tabWidget.addTab(self.tab_Load, "")
        self.tab_Main = QtWidgets.QWidget()
        self.tab_Main.setObjectName("tab_Main")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_Main)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_8 = QtWidgets.QLabel(parent=self.tab_Main)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.pushButton_test_zatizeni_start = QtWidgets.QPushButton(parent=self.tab_Main)
        self.pushButton_test_zatizeni_start.setObjectName("pushButton_test_zatizeni_start")
        self.horizontalLayout_2.addWidget(self.pushButton_test_zatizeni_start)
        self.pushButton_test_zatizeni_stop = QtWidgets.QPushButton(parent=self.tab_Main)
        self.pushButton_test_zatizeni_stop.setObjectName("pushButton_test_zatizeni_stop")
        self.horizontalLayout_2.addWidget(self.pushButton_test_zatizeni_stop)
        self.label_test_zatizeni = QtWidgets.QLabel(parent=self.tab_Main)
        self.label_test_zatizeni.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.label_test_zatizeni.setObjectName("label_test_zatizeni")
        self.horizontalLayout_2.addWidget(self.label_test_zatizeni)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(parent=self.tab_Main)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.spinBox_time_step_delay = QtWidgets.QSpinBox(parent=self.tab_Main)
        self.spinBox_time_step_delay.setMaximum(1000000)
        self.spinBox_time_step_delay.setSingleStep(100)
        self.spinBox_time_step_delay.setObjectName("spinBox_time_step_delay")
        self.gridLayout_2.addWidget(self.spinBox_time_step_delay, 2, 1, 1, 1)
        self.spinBox_time_measure_delay = QtWidgets.QSpinBox(parent=self.tab_Main)
        self.spinBox_time_measure_delay.setMaximum(1000000)
        self.spinBox_time_measure_delay.setSingleStep(100)
        self.spinBox_time_measure_delay.setObjectName("spinBox_time_measure_delay")
        self.gridLayout_2.addWidget(self.spinBox_time_measure_delay, 2, 3, 1, 1)
        self.label_10 = QtWidgets.QLabel(parent=self.tab_Main)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.tab_Main)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 4, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.label_12 = QtWidgets.QLabel(parent=self.tab_Main)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 2, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.spinBox_stop_mVAttempts = QtWidgets.QSpinBox(parent=self.tab_Main)
        self.spinBox_stop_mVAttempts.setObjectName("spinBox_stop_mVAttempts")
        self.gridLayout_2.addWidget(self.spinBox_stop_mVAttempts, 3, 3, 1, 1)
        self.spinBox_stop_mV = QtWidgets.QSpinBox(parent=self.tab_Main)
        self.spinBox_stop_mV.setMaximum(1000000)
        self.spinBox_stop_mV.setObjectName("spinBox_stop_mV")
        self.gridLayout_2.addWidget(self.spinBox_stop_mV, 3, 1, 1, 1)
        self.spinBox_reqmAstart = QtWidgets.QSpinBox(parent=self.tab_Main)
        self.spinBox_reqmAstart.setMaximum(1000000)
        self.spinBox_reqmAstart.setSingleStep(1000)
        self.spinBox_reqmAstart.setStepType(QtWidgets.QAbstractSpinBox.StepType.AdaptiveDecimalStepType)
        self.spinBox_reqmAstart.setDisplayIntegerBase(10)
        self.spinBox_reqmAstart.setObjectName("spinBox_reqmAstart")
        self.gridLayout_2.addWidget(self.spinBox_reqmAstart, 0, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(parent=self.tab_Main)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 3, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.label_9 = QtWidgets.QLabel(parent=self.tab_Main)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)
        self.spinBox_reqmAstop = QtWidgets.QSpinBox(parent=self.tab_Main)
        self.spinBox_reqmAstop.setMaximum(1000000)
        self.spinBox_reqmAstop.setSingleStep(1000)
        self.spinBox_reqmAstop.setObjectName("spinBox_reqmAstop")
        self.gridLayout_2.addWidget(self.spinBox_reqmAstop, 0, 5, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.tab_Main)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.spinBox_reqmAstep = QtWidgets.QSpinBox(parent=self.tab_Main)
        self.spinBox_reqmAstep.setMaximum(1000000)
        self.spinBox_reqmAstep.setSingleStep(10)
        self.spinBox_reqmAstep.setObjectName("spinBox_reqmAstep")
        self.gridLayout_2.addWidget(self.spinBox_reqmAstep, 0, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.mplWidget1 = MplWidget(parent=self.tab_Main)
        self.mplWidget1.setObjectName("mplWidget1")
        self.horizontalLayout_3.addWidget(self.mplWidget1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout.setStretch(2, 10)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab_Main, "")
        self.tab_export = QtWidgets.QWidget()
        self.tab_export.setObjectName("tab_export")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_export)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.export_plainTextEdit1 = QtWidgets.QPlainTextEdit(parent=self.tab_export)
        self.export_plainTextEdit1.setObjectName("export_plainTextEdit1")
        self.verticalLayout_4.addWidget(self.export_plainTextEdit1)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.tabWidget.addTab(self.tab_export, "")
        self.tab_help = QtWidgets.QWidget()
        self.tab_help.setObjectName("tab_help")
        self.tabWidget.addTab(self.tab_help, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 629, 17))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.config_pushButton_ClearToDefault.setText(_translate("MainWindow", "Clear to default"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_config), _translate("MainWindow", "Config"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_console), _translate("MainWindow", "Console"))
        self.label_2.setText(_translate("MainWindow", "VISA  resource"))
        self.pushButton_4.setText(_translate("MainWindow", "Connect"))
        self.pushButton_5.setText(_translate("MainWindow", "Disconnect"))
        self.label_3.setText(_translate("MainWindow", "Status: "))
        self.load_label_status.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Load), _translate("MainWindow", "Load"))
        self.label_8.setText(_translate("MainWindow", "Test zatížení"))
        self.pushButton_test_zatizeni_start.setText(_translate("MainWindow", "Start"))
        self.pushButton_test_zatizeni_stop.setText(_translate("MainWindow", "Stop"))
        self.label_test_zatizeni.setText(_translate("MainWindow", "None"))
        self.label_4.setText(_translate("MainWindow", "Requested Current: Start [mA]"))
        self.spinBox_time_step_delay.setToolTip(_translate("MainWindow", "<html><head/><body><p>Cas mezi jednotlivymi merenimi</p></body></html>"))
        self.spinBox_time_measure_delay.setToolTip(_translate("MainWindow", "<html><head/><body><p>Zpozdeni mezi nastavenim pozadovaneho proudu a merenim</p><p>Musi byt mensi nez Step delay</p></body></html>"))
        self.label_10.setText(_translate("MainWindow", "Stop at Vmin [V]"))
        self.label_5.setText(_translate("MainWindow", "Stop [mA]"))
        self.label_12.setText(_translate("MainWindow", "Measure delay [ms]"))
        self.label_11.setText(_translate("MainWindow", "Stop At Vmin - Attempts"))
        self.label_9.setText(_translate("MainWindow", "Step delay [ms]"))
        self.label_6.setText(_translate("MainWindow", "Step [mA]"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Main), _translate("MainWindow", "Main"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_export), _translate("MainWindow", "Export"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_help), _translate("MainWindow", "Help"))
from mplwidget import MplWidget
