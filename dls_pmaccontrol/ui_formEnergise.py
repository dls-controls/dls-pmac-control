# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dls_pmaccontrol/formEnergise.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_formEnergise(object):
    def setupUi(self, formEnergise):
        formEnergise.setObjectName("formEnergise")
        formEnergise.resize(192, 252)
        self.gridlayout = QtWidgets.QGridLayout(formEnergise)
        self.gridlayout.setContentsMargins(11, 11, 11, 11)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")
        self.btnSend = QtWidgets.QPushButton(formEnergise)
        self.btnSend.setObjectName("btnSend")
        self.gridlayout.addWidget(self.btnSend, 1, 0, 1, 1)
        self.btnClose = QtWidgets.QPushButton(formEnergise)
        self.btnClose.setObjectName("btnClose")
        self.gridlayout.addWidget(self.btnClose, 1, 1, 1, 1)
        self.chkGroup = QtWidgets.QGroupBox(formEnergise)
        self.chkGroup.setObjectName("chkGroup")
        self.gridlayout1 = QtWidgets.QGridLayout(self.chkGroup)
        self.gridlayout1.setContentsMargins(11, 11, 11, 11)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")
        self.gridlayout.addWidget(self.chkGroup, 0, 0, 1, 2)

        self.retranslateUi(formEnergise)
        self.btnClose.clicked.connect(formEnergise.close)
        self.btnSend.clicked.connect(formEnergise.sendCommand)
        QtCore.QMetaObject.connectSlotsByName(formEnergise)

    def retranslateUi(self, formEnergise):
        _translate = QtCore.QCoreApplication.translate
        formEnergise.setWindowTitle(_translate("formEnergise", "Energise axis"))
        self.btnSend.setText(_translate("formEnergise", "send"))
        self.btnClose.setText(_translate("formEnergise", "close"))
        self.chkGroup.setTitle(_translate("formEnergise", "Axis"))

