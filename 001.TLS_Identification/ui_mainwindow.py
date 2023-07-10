# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow2.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(886, 800)
        self.actionoptics = QAction(MainWindow)
        self.actionoptics.setObjectName(u"actionoptics")
        self.actionthreshold = QAction(MainWindow)
        self.actionthreshold.setObjectName(u"actionthreshold")
        self.actioncolor = QAction(MainWindow)
        self.actioncolor.setObjectName(u"actioncolor")
        self.actionchangebg = QAction(MainWindow)
        self.actionchangebg.setObjectName(u"actionchangebg")
        self.actiondraw = QAction(MainWindow)
        self.actiondraw.setObjectName(u"actiondraw")
        self.actionddownloadoptics = QAction(MainWindow)
        self.actionddownloadoptics.setObjectName(u"actionddownloadoptics")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.graphicsView_main = QGraphicsView(self.centralwidget)
        self.graphicsView_main.setObjectName(u"graphicsView_main")
        self.graphicsView_main.setGeometry(QRect(410, 0, 480, 480))
        self.graphicsView_main.setMouseTracking(True)
        self.graphicsView_main.optics_label = QLabel(self.graphicsView_main)
        self.graphicsView_main.optics_label.setText(None)
        self.graphicsView_main.optics_label.move(0, 0)
        self.graphicsView_main.optics_label.resize(100, 20)
        self.graphicsView_merge = QGraphicsView(self.centralwidget)
        self.graphicsView_merge.setObjectName(u"graphicsView_merge")
        self.graphicsView_merge.setGeometry(QRect(30, 0, 300, 300))
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(30, 490, 841, 261))
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1286, 259))
        self.horizontalLayout = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_1 = QVBoxLayout()
        self.verticalLayout_1.setObjectName(u"verticalLayout_1")
        self.graphicsView_1 = QGraphicsView(self.scrollAreaWidgetContents)
        self.graphicsView_1.setObjectName(u"graphicsView_1")
        self.graphicsView_1.setMinimumSize(QSize(200, 200))
        self.graphicsView_1.setMaximumSize(QSize(200, 200))

        self.verticalLayout_1.addWidget(self.graphicsView_1)

        self.label_1 = QLabel(self.scrollAreaWidgetContents)
        self.label_1.setObjectName(u"label_1")
        self.label_1.setMinimumSize(QSize(200, 20))
        self.label_1.setMaximumSize(QSize(200, 20))

        self.verticalLayout_1.addWidget(self.label_1)


        self.horizontalLayout.addLayout(self.verticalLayout_1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.graphicsView_2 = QGraphicsView(self.scrollAreaWidgetContents)
        self.graphicsView_2.setObjectName(u"graphicsView_2")
        self.graphicsView_2.setMinimumSize(QSize(200, 200))
        self.graphicsView_2.setMaximumSize(QSize(200, 200))

        self.verticalLayout_2.addWidget(self.graphicsView_2)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(200, 20))
        self.label_2.setMaximumSize(QSize(200, 20))

        self.verticalLayout_2.addWidget(self.label_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.graphicsView_3 = QGraphicsView(self.scrollAreaWidgetContents)
        self.graphicsView_3.setObjectName(u"graphicsView_3")
        self.graphicsView_3.setMinimumSize(QSize(200, 200))
        self.graphicsView_3.setMaximumSize(QSize(200, 200))

        self.verticalLayout_3.addWidget(self.graphicsView_3)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(200, 20))
        self.label_3.setMaximumSize(QSize(200, 20))

        self.verticalLayout_3.addWidget(self.label_3)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.graphicsView_4 = QGraphicsView(self.scrollAreaWidgetContents)
        self.graphicsView_4.setObjectName(u"graphicsView_4")
        self.graphicsView_4.setMinimumSize(QSize(200, 200))
        self.graphicsView_4.setMaximumSize(QSize(200, 200))

        self.verticalLayout_4.addWidget(self.graphicsView_4)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(200, 20))
        self.label_4.setMaximumSize(QSize(200, 20))

        self.verticalLayout_4.addWidget(self.label_4)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.graphicsView_5 = QGraphicsView(self.scrollAreaWidgetContents)
        self.graphicsView_5.setObjectName(u"graphicsView_5")
        self.graphicsView_5.setMinimumSize(QSize(200, 200))
        self.graphicsView_5.setMaximumSize(QSize(200, 200))

        self.verticalLayout_5.addWidget(self.graphicsView_5)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(200, 20))
        self.label_5.setMaximumSize(QSize(200, 20))

        self.verticalLayout_5.addWidget(self.label_5)


        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.graphicsView_6 = QGraphicsView(self.scrollAreaWidgetContents)
        self.graphicsView_6.setObjectName(u"graphicsView_6")
        self.graphicsView_6.setMinimumSize(QSize(200, 200))
        self.graphicsView_6.setMaximumSize(QSize(200, 200))

        self.verticalLayout_6.addWidget(self.graphicsView_6)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(200, 20))
        self.label_6.setMaximumSize(QSize(200, 20))

        self.verticalLayout_6.addWidget(self.label_6)


        self.horizontalLayout.addLayout(self.verticalLayout_6)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 886, 24))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionoptics)
        self.menu.addAction(self.actionthreshold)
        self.menu.addAction(self.actioncolor)
        self.menu.addAction(self.actionchangebg)
        self.menu.addAction(self.actiondraw)
        self.menu.addAction(self.actionddownloadoptics)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionoptics.setText(QCoreApplication.translate("MainWindow", u"Parameters for Optics", None))
        self.actionthreshold.setText(QCoreApplication.translate("MainWindow", u"Threshold for Signatures", None))
        self.actioncolor.setText(QCoreApplication.translate("MainWindow", u"Color(Not Available)", None))
        self.actionchangebg.setText(QCoreApplication.translate("MainWindow", u"Change Background", None))
        self.actiondraw.setText(QCoreApplication.translate("MainWindow", u"Manual Refinement ", None))
        self.actionddownloadoptics.setText(QCoreApplication.translate("MainWindow", u"Output Results", None))
        self.label_1.setText(QCoreApplication.translate("MainWindow", u"Label 1", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Label 2", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Label 3", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Label 4", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Label 5", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Label 6", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
    # retranslateUi

