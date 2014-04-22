# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qgis2leaf.ui'
#
# Created: Tue Apr 22 23:24:45 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_qgis2leaf(object):
    def setupUi(self, qgis2leaf):
        qgis2leaf.setObjectName(_fromUtf8("qgis2leaf"))
        qgis2leaf.resize(405, 223)
        self.label_3 = QtGui.QLabel(qgis2leaf)
        self.label_3.setGeometry(QtCore.QRect(0, 80, 387, 15))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit_2 = QtGui.QLineEdit(qgis2leaf)
        self.lineEdit_2.setGeometry(QtCore.QRect(0, 100, 294, 31))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.pushButton_2 = QtGui.QPushButton(qgis2leaf)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 100, 85, 31))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.okButton = QtGui.QPushButton(qgis2leaf)
        self.okButton.setGeometry(QtCore.QRect(310, 180, 85, 27))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.cancelButton = QtGui.QPushButton(qgis2leaf)
        self.cancelButton.setGeometry(QtCore.QRect(220, 180, 85, 27))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.actionLoadList = QtGui.QAction(qgis2leaf)
        self.actionLoadList.setObjectName(_fromUtf8("actionLoadList"))

        self.retranslateUi(qgis2leaf)
        QtCore.QMetaObject.connectSlotsByName(qgis2leaf)

    def retranslateUi(self, qgis2leaf):
        qgis2leaf.setWindowTitle(_translate("qgis2leaf", "qgis2leaf", None))
        self.label_3.setText(_translate("qgis2leaf", "Output project Name:", None))
        self.pushButton_2.setText(_translate("qgis2leaf", "...", None))
        self.okButton.setText(_translate("qgis2leaf", "OK", None))
        self.cancelButton.setText(_translate("qgis2leaf", "Cancel", None))
        self.actionLoadList.setText(_translate("qgis2leaf", "loadList", None))

