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
        MainWindow.resize(585, 439)
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
        self.gridLayoutWidget = QtWidgets.QWidget(parent=self.tab_config)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 20, 441, 301))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(parent=self.gridLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.gridLayoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.gridLayoutWidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 3, 1, 1, 1)
        self.tabWidget.addTab(self.tab_config, "")
        self.tab_console = QtWidgets.QWidget()
        self.tab_console.setObjectName("tab_console")
        self.tabWidget.addTab(self.tab_console, "")
        self.tab_Main = QtWidgets.QWidget()
        self.tab_Main.setObjectName("tab_Main")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_Main)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_test_zatizeni = QtWidgets.QPushButton(parent=self.tab_Main)
        self.pushButton_test_zatizeni.setObjectName("pushButton_test_zatizeni")
        self.horizontalLayout_2.addWidget(self.pushButton_test_zatizeni)
        self.label_test_zatizeni = QtWidgets.QLabel(parent=self.tab_Main)
        self.label_test_zatizeni.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.label_test_zatizeni.setObjectName("label_test_zatizeni")
        self.horizontalLayout_2.addWidget(self.label_test_zatizeni)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.mplWidget1 = MplWidget(parent=self.tab_Main)
        self.mplWidget1.setObjectName("mplWidget1")
        self.horizontalLayout_3.addWidget(self.mplWidget1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.tab_Main)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab_Main, "")
        self.tab_export = QtWidgets.QWidget()
        self.tab_export.setObjectName("tab_export")
        self.tabWidget.addTab(self.tab_export, "")
        self.tab_help = QtWidgets.QWidget()
        self.tab_help.setObjectName("tab_help")
        self.tabWidget.addTab(self.tab_help, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 585, 17))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_config), _translate("MainWindow", "Config"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_console), _translate("MainWindow", "Console"))
        self.pushButton_test_zatizeni.setText(_translate("MainWindow", "Test zatizeni"))
        self.label_test_zatizeni.setText(_translate("MainWindow", "None"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Main), _translate("MainWindow", "Main"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_export), _translate("MainWindow", "Export"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_help), _translate("MainWindow", "Help"))
from mplwidget import MplWidget
