# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'optics.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_Optics_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(478, 120)
        self.max_eps_label = QLabel("Max EPS:", Dialog)
        self.max_eps_label.setGeometry(QRect(10, 40, 60, 31))
        self.comboBox = QComboBox(Dialog)
        self.comboBox.addItem("1")
        self.comboBox.addItem("1.5")
        self.comboBox.addItem("2")
        self.comboBox.addItem("2.5")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.setGeometry(QRect(60, 40, 141, 31))
        self.min_samples_label = QLabel("Min Samples:", Dialog)
        self.min_samples_label.setGeometry(QRect(250, 40, 90, 31))
        self.spinBox = QSpinBox(Dialog)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setDisabled(True)
        self.spinBox.setGeometry(QRect(340, 40, 131, 22))
        self.close_button = QPushButton(Dialog)
        self.close_button.setObjectName(u"close_button")
        self.close_button.setGeometry(QRect(140, 80, 181, 30))
        self.close_button.setText("Close Operation")

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"5 points", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"9 points", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Dialog", u"13 points", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Dialog", u"21 points", None))
    # retranslateUi


