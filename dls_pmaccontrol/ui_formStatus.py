# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dls_pmaccontrol/formStatus.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_formStatus(object):
    def setupUi(self, formStatus):
        formStatus.setObjectName("formStatus")
        formStatus.resize(99, 189)
        self.gridlayout = QtWidgets.QGridLayout(formStatus)
        self.gridlayout.setContentsMargins(11, 11, 11, 11)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")
        self.ledGroup = QtWidgets.QGroupBox(formStatus)
        self.ledGroup.setObjectName("ledGroup")
        self.gridlayout1 = QtWidgets.QGridLayout(self.ledGroup)
        self.gridlayout1.setContentsMargins(11, 11, 11, 11)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")
        self.gridlayout.addWidget(self.ledGroup, 0, 0, 1, 2)

        self.retranslateUi(formStatus)
        QtCore.QMetaObject.connectSlotsByName(formStatus)

    def retranslateUi(self, formStatus):
        _translate = QtCore.QCoreApplication.translate
        formStatus.setWindowTitle(_translate("formStatus", "Status bits"))
        self.ledGroup.setTitle(_translate("formStatus", "Axis"))


