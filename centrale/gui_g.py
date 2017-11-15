from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from threading import Thread
from pyqtgraph import PlotWidget
import numpy as np
from controllers import SerialController, DataController
from enums import Command, SensorType
import time
import atexit

# TODO fix some minor bugs with disconnecting arduino's
# TODO fix the 255 cm of the distance to 400
# TODO fix the thread closing (optional)

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(802, 472)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../centrale/icons/arduino_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        #####################################################################################################
        # The serial controller
        self.serial_controller = SerialController()
        #####################################################################################################
        # timers & threads
        self.graphTimer = QtCore.QTimer()
        self.exit = False
        atexit.register(self.stopThread)  # register the stopThread funtion to get out of the infinite loop
        self.thread = Thread(target=self.updateData)  # Start a thread to read data
        self.command_thread = Thread(target=self.submitSettings_flow)  # build a thread to execute the commands
        #####################################################################################################
        self.selected_controller = None
        self.controllers = []
        self.controllers_data = {}
        #####################################################################################################
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #####################################################################################################
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        #####################################################################################################
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        #####################################################################################################
        self.arduino1 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arduino1.sizePolicy().hasHeightForWidth())
        self.arduino1.setSizePolicy(sizePolicy)
        self.arduino1.setObjectName("arduino1")
        self.verticalLayout.addWidget(self.arduino1)
        #####################################################################################################
        self.arduino2 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arduino2.sizePolicy().hasHeightForWidth())
        self.arduino2.setSizePolicy(sizePolicy)
        self.arduino2.setStyleSheet("")
        self.arduino2.setObjectName("arduino2")
        self.verticalLayout.addWidget(self.arduino2)
        #####################################################################################################
        self.arduino3 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arduino3.sizePolicy().hasHeightForWidth())
        self.arduino3.setSizePolicy(sizePolicy)
        self.arduino3.setObjectName("arduino3")
        self.verticalLayout.addWidget(self.arduino3)
        #####################################################################################################
        self.arduino4 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arduino4.sizePolicy().hasHeightForWidth())
        self.arduino4.setSizePolicy(sizePolicy)
        self.arduino4.setObjectName("arduino4")
        self.verticalLayout.addWidget(self.arduino4)
        #####################################################################################################
        self.arduino5 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arduino5.sizePolicy().hasHeightForWidth())
        self.arduino5.setSizePolicy(sizePolicy)
        self.arduino5.setObjectName("arduino5")
        self.verticalLayout.addWidget(self.arduino5)
        #####################################################################################################
        self.horizontalLayout.addLayout(self.verticalLayout)
        #####################################################################################################
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        #####################################################################################################
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        #####################################################################################################
        self.graphs = QtWidgets.QWidget()
        self.graphs.setObjectName("graphs")
        #####################################################################################################
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.graphs)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        #####################################################################################################
        self.label_6 = QtWidgets.QLabel(self.graphs)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        #####################################################################################################
        self.graphicsView = PlotWidget(self.graphs)
        self.graphicsView.setObjectName("graphicsView")
        self.light_plot = self.graphicsView.plot([])
        self.verticalLayout_3.addWidget(self.graphicsView)
        #####################################################################################################
        self.label_10 = QtWidgets.QLabel(self.graphs)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_3.addWidget(self.label_10)
        #####################################################################################################
        self.graphicsView_2 = PlotWidget(self.graphs)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.temp_plot = self.graphicsView_2.plot([])
        self.verticalLayout_3.addWidget(self.graphicsView_2)
        #####################################################################################################
        self.label_11 = QtWidgets.QLabel(self.graphs)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_3.addWidget(self.label_11)
        #####################################################################################################
        self.label_12 = QtWidgets.QLabel(self.graphs)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_3.addWidget(self.label_12)
        #####################################################################################################
        self.tabWidget.addTab(self.graphs, "")
        #####################################################################################################
        self.settings = QtWidgets.QWidget()
        self.settings.setObjectName("settings")
        self.gridLayout = QtWidgets.QGridLayout(self.settings)
        self.gridLayout.setObjectName("gridLayout")
        #####################################################################################################
        self.label_4 = QtWidgets.QLabel(self.settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)
        #####################################################################################################
        self.label_7 = QtWidgets.QLabel(self.settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 1, 1, 1)
        #####################################################################################################
        self.label = QtWidgets.QLabel(self.settings)
        self.label.setWhatsThis("")
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        #####################################################################################################
        self.label_2 = QtWidgets.QLabel(self.settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        #####################################################################################################
        self.tempscroll_down = QtWidgets.QSlider(self.settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tempscroll_down.sizePolicy().hasHeightForWidth())
        self.tempscroll_down.setSizePolicy(sizePolicy)
        self.tempscroll_down.setMinimum(-40)
        self.tempscroll_down.setMaximum(60)
        self.tempscroll_down.setOrientation(QtCore.Qt.Horizontal)
        self.tempscroll_down.setObjectName("tempscroll_down")
        self.gridLayout.addWidget(self.tempscroll_down, 3, 2, 1, 1)
        #####################################################################################################
        self.label_9 = QtWidgets.QLabel(self.settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)
        #####################################################################################################
        self.label_8 = QtWidgets.QLabel(self.settings)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        #####################################################################################################
        self.label_3 = QtWidgets.QLabel(self.settings)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        #####################################################################################################
        self.lightdown_slider = QtWidgets.QSlider(self.settings)
        self.lightdown_slider.setOrientation(QtCore.Qt.Horizontal)
        self.lightdown_slider.setObjectName("lightdown_slider")
        self.gridLayout.addWidget(self.lightdown_slider, 1, 2, 1, 1)
        #####################################################################################################
        self.scrollout_min = QtWidgets.QSlider(self.settings)
        self.scrollout_min.setMinimum(2)
        self.scrollout_min.setMaximum(400)
        self.scrollout_min.setOrientation(QtCore.Qt.Horizontal)
        self.scrollout_min.setObjectName("scrollout_min")
        self.gridLayout.addWidget(self.scrollout_min, 5, 2, 1, 1)
        #####################################################################################################
        self.label_14 = QtWidgets.QLabel(self.settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 5, 1, 1, 1)
        #####################################################################################################
        self.scrollout_max = QtWidgets.QSlider(self.settings)
        self.scrollout_max.setMinimum(2)
        self.scrollout_max.setMaximum(255)
        self.scrollout_max.setOrientation(QtCore.Qt.Horizontal)
        self.scrollout_max.setObjectName("scrollout_max")
        self.gridLayout.addWidget(self.scrollout_max, 4, 2, 1, 1)
        #####################################################################################################
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        #####################################################################################################
        self.scrollup = QtWidgets.QPushButton(self.settings)
        self.scrollup.setObjectName("scrollup")
        self.gridLayout_2.addWidget(self.scrollup, 1, 0, 1, 1)
        #####################################################################################################
        self.scrolldown = QtWidgets.QPushButton(self.settings)
        self.scrolldown.setObjectName("scrolldown")
        self.gridLayout_2.addWidget(self.scrolldown, 1, 1, 1, 1)
        #####################################################################################################
        self.lightcheck = QtWidgets.QCheckBox(self.settings)
        self.lightcheck.setObjectName("lightcheck")
        self.gridLayout_2.addWidget(self.lightcheck, 0, 0, 1, 1)
        #####################################################################################################
        self.tempcheck = QtWidgets.QCheckBox(self.settings)
        self.tempcheck.setObjectName("tempcheck")
        self.gridLayout_2.addWidget(self.tempcheck, 0, 1, 1, 1)
        #####################################################################################################
        self.submit = QtWidgets.QPushButton(self.settings)
        self.submit.setObjectName("submit")
        self.gridLayout_2.addWidget(self.submit, 1, 2, 1, 1)
        #####################################################################################################
        self.scrolloutcheck = QtWidgets.QCheckBox(self.settings)
        self.scrolloutcheck.setObjectName("scrolloutcheck")
        self.gridLayout_2.addWidget(self.scrolloutcheck, 0, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 6, 0, 1, 4)
        #####################################################################################################
        self.lightup_slider = QtWidgets.QSlider(self.settings)
        self.lightup_slider.setOrientation(QtCore.Qt.Horizontal)
        self.lightup_slider.setObjectName("lightup_slider")
        self.gridLayout.addWidget(self.lightup_slider, 0, 2, 1, 1)
        #####################################################################################################
        self.lightup_bar = QtWidgets.QProgressBar(self.settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lightup_bar.sizePolicy().hasHeightForWidth())
        self.lightup_bar.setSizePolicy(sizePolicy)
        self.lightup_bar.setProperty("value", 0)
        self.lightup_bar.setObjectName("lightup_bar")
        self.gridLayout.addWidget(self.lightup_bar, 0, 3, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.settings)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 4, 1, 1, 1)
        #####################################################################################################
        self.lightdown_bar = QtWidgets.QProgressBar(self.settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lightdown_bar.sizePolicy().hasHeightForWidth())
        self.lightdown_bar.setSizePolicy(sizePolicy)
        self.lightdown_bar.setProperty("value", 0)
        self.lightdown_bar.setObjectName("lightdown_bar")
        self.gridLayout.addWidget(self.lightdown_bar, 1, 3, 1, 1)
        #####################################################################################################
        self.label_5 = QtWidgets.QLabel(self.settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 1, 1, 1)
        #####################################################################################################
        self.tempnumber_up = QtWidgets.QLabel(self.settings)
        self.tempnumber_up.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tempnumber_up.setObjectName("tempnumber_up")
        self.gridLayout.addWidget(self.tempnumber_up, 2, 3, 1, 1)
        #####################################################################################################
        self.tempnumber_down = QtWidgets.QLabel(self.settings)
        self.tempnumber_down.setObjectName("tempnumber_down")
        self.gridLayout.addWidget(self.tempnumber_down, 3, 3, 1, 1)
        #####################################################################################################
        self.sminout = QtWidgets.QLabel(self.settings)
        self.sminout.setObjectName("sminout")
        self.gridLayout.addWidget(self.sminout, 5, 3, 1, 1)
        #####################################################################################################
        self.smaxout = QtWidgets.QLabel(self.settings)
        self.smaxout.setObjectName("smaxout")
        self.gridLayout.addWidget(self.smaxout, 4, 3, 1, 1)
        #####################################################################################################
        self.tempscroll_up = QtWidgets.QSlider(self.settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tempscroll_up.sizePolicy().hasHeightForWidth())
        self.tempscroll_up.setSizePolicy(sizePolicy)
        self.tempscroll_up.setMinimum(-40)
        self.tempscroll_up.setMaximum(60)
        self.tempscroll_up.setProperty("value", 0)
        self.tempscroll_up.setOrientation(QtCore.Qt.Horizontal)
        self.tempscroll_up.setObjectName("tempscroll_up")
        self.gridLayout.addWidget(self.tempscroll_up, 2, 2, 1, 1)
        #####################################################################################################
        self.tabWidget.addTab(self.settings, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        #####################################################################################################
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 22))
        self.menubar.setObjectName("menubar")
        #####################################################################################################
        self.menu = QtWidgets.QMenu(self.menubar)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("..\centrale\icons\if_menu_2639862.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu.setIcon(icon1)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        #####################################################################################################
        self.actionClose = QtWidgets.QAction(MainWindow)
        iconquit = QtGui.QIcon()
        iconquit.addPixmap(QtGui.QPixmap("..\centrale\icons\if_minus_2639865.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClose.setIcon(iconquit)
        self.actionClose.setObjectName("actionClose")
        #####################################################################################################
        self.actionRefresh = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("..\centrale\icons\if_refresh_2639897.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon2)
        self.actionRefresh.setObjectName("actionRefresh")
        #####################################################################################################
        self.menu.addSeparator()
        self.menu.addAction(self.actionRefresh)
        self.menu.addAction(self.actionClose)
        self.menubar.addAction(self.menu.menuAction())
        #####################################################################################################
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.lightup_slider.sliderMoved['int'].connect(self.lightup_bar.setValue)
        self.lightdown_slider.sliderMoved['int'].connect(self.lightdown_bar.setValue)
        self.tempscroll_up.sliderMoved['int'].connect(self.tempnumber_up.setNum)
        self.tempscroll_down.sliderMoved['int'].connect(self.tempnumber_down.setNum)
        self.scrollout_max.sliderMoved['int'].connect(self.smaxout.setNum)
        self.scrollout_min.sliderMoved['int'].connect(self.sminout.setNum)
        #####################################################################################################
        # Add actions to the GUI
        self.actionClose.triggered.connect(self.quit_application)
        self.actionRefresh.triggered.connect(self.refresh)
        self.arduino1.clicked.connect(self.selectArduino1)
        self.arduino2.clicked.connect(self.selectArduino2)
        self.arduino3.clicked.connect(self.selectArduino3)
        self.arduino4.clicked.connect(self.selectArduino4)
        self.arduino5.clicked.connect(self.selectArduino5)
        self.scrollup.clicked.connect(self.scrollUp)
        self.scrolldown.clicked.connect(self.scrollDown)
        self.submit.clicked.connect(self.submitSettings)
        #####################################################################################################
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Central Control"))
        self.arduino1.setText(_translate("MainWindow", "Arduino - Not connected"))
        self.arduino2.setText(_translate("MainWindow", "Arduino - Not connected"))
        self.arduino3.setText(_translate("MainWindow", "Arduino - Not connected"))
        self.arduino4.setText(_translate("MainWindow", "Arduino - Not connected"))
        self.arduino5.setText(_translate("MainWindow", "Arduino - Not connected"))
        self.label_6.setText(_translate("MainWindow", "Light Graph"))
        self.label_10.setText(_translate("MainWindow", "temperature Graph"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.graphs), _translate("MainWindow", "Graphs"))
        self.label_4.setText(_translate("MainWindow", "Scroll up"))
        self.label_7.setText(_translate("MainWindow", "Scroll down"))
        self.label.setText(_translate("MainWindow", "Light"))
        self.label_2.setText(_translate("MainWindow", "Scroll up"))
        self.label_9.setText(_translate("MainWindow", "Scroll out"))
        self.label_8.setText(_translate("MainWindow", "Temperature"))
        self.label_11.setText(_translate("MainWindow", "Distance"))
        # self.label_12.setText(_translate("MainWindow", "255 cm"))
        self.label_12.setText("unknown")
        self.label_14.setText(_translate("MainWindow", "Min"))
        self.scrollup.setText(_translate("MainWindow", "Scroll up"))
        self.scrolldown.setText(_translate("MainWindow", "Scroll down"))
        self.lightcheck.setText(_translate("MainWindow", "Light"))
        self.tempcheck.setText(_translate("MainWindow", "Temperature"))
        self.submit.setText(_translate("MainWindow", "Submit"))
        self.scrolloutcheck.setText(_translate("MainWindow", "Scroll out"))
        self.lightup_bar.setFormat(_translate("MainWindow", "%p%"))
        self.label_13.setText(_translate("MainWindow", "Max"))
        self.label_5.setText(_translate("MainWindow", "Scroll down"))
        self.tempnumber_up.setText(_translate("MainWindow", "0 °C"))
        self.tempnumber_down.setText(_translate("MainWindow", "0 °C"))
        self.sminout.setText(_translate("MainWindow", "2 cm"))
        self.smaxout.setText(_translate("MainWindow", "2 cm"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings), _translate("MainWindow", "Settings"))
        self.menu.setTitle(_translate("MainWindow", "Menu"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionRefresh.setText(_translate("MainWindow", "Refresh"))

    def refresh(self):
        self.controllers = self.serial_controller.connect_ports()
        # Set the datacontroller for each device that is connected
        for controller in self.controllers:
            if controller not in self.controllers_data.keys():
                self.controllers_data[controller] = DataController()
                self.controllers_data[controller].set_data_types('light', 'temp', 'dist')
        # Update the gui to show the connected devices
        if self.exit:
            self.exit = False
            self.thread = Thread(target=self.updateData)
        if not self.thread.is_alive():
            self.thread.start()
        # start the thread if not already running
        device_number = 0
        _translate = QtCore.QCoreApplication.translate
        self.setArduinotextEmtpy(_translate)
        for controller in self.controllers:
            if device_number == 0:
                self.arduino1.setText(_translate("MainWindow", "Arduino - Connected: %s" % controller))
            elif device_number == 1:
                self.arduino2.setText(_translate("MainWindow", "Arduino - Connected: %s" % controller))
            elif device_number == 2:
                self.arduino3.setText(_translate("MainWindow", "Arduino - Connected: %s" % controller))
            elif device_number == 3:
                self.arduino4.setText(_translate("MainWindow", "Arduino - Connected: %s" % controller))
            elif device_number == 4:
                self.arduino5.setText(_translate("MainWindow", "Arduino - Connected: %s" % controller))
            else:
                break;
            device_number += 1

    def setArduinotextEmtpy(self, translate):
        # set all the text to not connected
        self.arduino1.setText(translate("MainWindow", "Arduino - Not connected"))
        self.arduino2.setText(translate("MainWindow", "Arduino - Not connected"))
        self.arduino3.setText(translate("MainWindow", "Arduino - Not connected"))
        self.arduino4.setText(translate("MainWindow", "Arduino - Not connected"))
        self.arduino5.setText(translate("MainWindow", "Arduino - Not connected"))

    def setArduinoStyleSheet(self):
        # decolor the buttons
        self.arduino1.setStyleSheet("")
        self.arduino2.setStyleSheet("")
        self.arduino3.setStyleSheet("")
        self.arduino4.setStyleSheet("")
        self.arduino5.setStyleSheet("")

    def updateData(self):
        while self.exit is not True:
            data = self.serial_controller.read_ports()
            print(data)
            if data is not None:
                for data_block in data:
                    if self.controllers_data[data_block[0]] is not None:
                        if data_block[1] == SensorType.LIGHT.value:
                            self.controllers_data[data_block[0]].update(data_type='light', data=data_block[2])
                        elif data_block[1] == SensorType.TEMP.value:
                            if data_block[2] < 60:
                                self.controllers_data[data_block[0]].update(data_type='temp', data=data_block[2])
                        elif data_block[1] == SensorType.DIST.value:
                            self.label_12.setText(str(data_block[2]) + " cm")
                            self.controllers_data[data_block[0]].update(data_type='dist', data=data_block[2])

    def updateGraph(self, graph, data):
        graph.setData(data)

    def updateGraph1(self):
        # print(self.controllers_data[self.controllers[0]].getData('temp'))  # for debugging purposes
        # self.updateGraph(self.light_plot, [1,2,3,4,5])   # for debugging purposes
        # self.label_12.setText(str(self.controllers_data[self.controllers[0]].getData('dist')) + " cm")  # TODO check the distance data
        self.updateGraph(self.light_plot, self.controllers_data[self.controllers[0]].getData('light'))  # update light graph
        self.updateGraph(self.temp_plot, self.controllers_data[self.controllers[0]].getData('temp'))  # update temperature graph

    def doNothing(self):
        pass

    def selectArduino1(self):
        try:
            if self.selected_controller is self.controllers[0]:
                self.selected_controller = None
                self.setArduinoStyleSheet()
                self.graphTimer.stop()
            else:
                self.selected_controller = self.controllers[0]  # select the controller
                self.graphTimer = QtCore.QTimer()
                self.graphTimer.timeout.connect(self.updateGraph1)
                self.graphTimer.start(1000)
                self.setArduinoStyleSheet()
                self.arduino1.setStyleSheet("background-color: rgb(182, 187, 235)")  # color the button

        except Exception as e:
            self.selected_controller = None
            pass

    def updateGraph2(self):
        self.updateGraph(self.light_plot, self.controllers_data[self.controllers[1]].getData('light'))  # update light graph
        self.updateGraph(self.temp_plot, self.controllers_data[self.controllers[1]].getData('temp'))  # update temperature graph

    def selectArduino2(self):
        try:
            self.selected_controller = self.controllers[1]  # select the controller
            self.graphTimer = QtCore.QTimer()
            self.graphTimer.timeout.connect(self.updateGraph2)
            self.graphTimer.start(1000)
            self.setArduinoStyleSheet()
            self.arduino2.setStyleSheet("background-color: rgb(182, 187, 235)")  # color the button
        except Exception as e:
            self.selected_controller = None
            pass

    def updateGraph3(self):
        self.updateGraph(self.light_plot, self.controllers_data[self.controllers[2]].getData('light'))  # update light graph
        self.updateGraph(self.temp_plot, self.controllers_data[self.controllers[2]].getData('temp'))  # update temperature graph

    def selectArduino3(self):
        try:
            self.selected_controller = self.controllers[2]  # select the controller
            self.graphTimer = QtCore.QTimer()
            self.graphTimer.timeout.connect(self.updateGraph3)
            self.graphTimer.start(1000)
            self.setArduinoStyleSheet()
            self.arduino3.setStyleSheet("background-color: rgb(182, 187, 235)")  # color the button
        except Exception as e:
            self.selected_controller = None
            pass

    def updateGraph4(self):
        self.updateGraph(self.light_plot, self.controllers_data[self.controllers[3]].getData('light'))  # update light graph
        self.updateGraph(self.temp_plot, self.controllers_data[self.controllers[3]].getData('temp'))  # update temperature graph

    def selectArduino4(self):
        try:
            self.selected_controller = self.controllers[3]  # select the controller
            self.graphTimer = QtCore.QTimer()
            self.graphTimer.timeout.connect(self.updateGraph4)
            self.graphTimer.start(1000)
            self.setArduinoStyleSheet()
            self.arduino4.setStyleSheet("background-color: rgb(182, 187, 235)")  # color the button
        except Exception as e:
            self.selected_controller = None
            pass

    def updateGraph5(self):
        self.updateGraph(self.light_plot, self.controllers_data[self.controllers[4]].getData('light'))  # update light graph
        self.updateGraph(self.temp_plot, self.controllers_data[self.controllers[4]].getData('temp'))  # update temperature graph

    def selectArduino5(self):
        try:
            if self.selected_controller :
                self.selected_controller = None
                self.setArduinoStyleSheet()
            self.selected_controller = self.controllers[4]  # select the controller
            self.graphTimer = QtCore.QTimer()
            self.graphTimer.timeout.connect(self.updateGraph5)
            self.graphTimer.start(1000)
            self.setArduinoStyleSheet()
            self.arduino5.setStyleSheet("background-color: rgb(182, 187, 235)")  # color the button
        except Exception as e:
            self.selected_controller = None
            pass

    def submitSettings(self):
        if self.selected_controller is None:
            return
        # check if settings thread is finished to start a new thread
        if not self.command_thread.is_alive():
            self.command_thread.start()

    def submitSettings_flow(self):
        commands = []  # list that contains all the commands to execute
        if self.lightcheck.isChecked():
            commands.append([Command.LIGHT_ROL_OUT.value, self.lightdown_slider.value()])  # append command and value
            commands.append([Command.LIGHT_ROL_IN.value, self.lightup_slider.value()])
        if self.tempcheck.isChecked():
            commands.append([Command.TEMP_ROL_IN.value, self.tempscroll_up.value()])
            commands.append([Command.TEMP_ROL_OUT.value, self.tempscroll_down.value()])
        if self.scrolloutcheck.isChecked():
            commands.append([Command.MAX_ROL_OUT.value, self.scrollout_max.value()])
            commands.append([Command.MIN_ROL_OUT.value, self.scrollout_min.value()])
        for command in commands:
            self.serial_controller.send_command(self.selected_controller, command[0], command[1])  # send all the commands selected
            time.sleep(1)  # sleep for 1 millisec to give the device time to proces the commands

    def scrollUp(self):
        if self.selected_controller is None:
            return
        self.serial_controller.send_command(self.selected_controller, Command.ROL_IN.value, content=0)  # content is not important in this command

    def scrollDown(self):
        if self.selected_controller is None:
            return
        self.serial_controller.send_command(self.selected_controller, Command.ROL_OUT.value, content=0)  # content is not important in this command

    def quit_application(self):
        self.stopThread()

    def stopThread(self):
        # print("Tried to stop the Thread")  # print for debugging purposes
        self.exit = True


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
