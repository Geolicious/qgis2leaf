# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qgis2leaf.ui'
#
# Created: Sat May  3 15:38:59 2014
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
        qgis2leaf.resize(461, 616)
        self.gridLayoutWidget = QtGui.QWidget(qgis2leaf)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 400, 443, 210))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEdit_2 = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout.addWidget(self.lineEdit_2, 5, 1, 1, 1)
        self.okButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.gridLayout.addWidget(self.okButton, 6, 2, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 5, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans"))
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(self.gridLayoutWidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 4, 1, 1, 1)
        self.comboBox_2 = QtGui.QComboBox(self.gridLayoutWidget)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.gridLayout.addWidget(self.comboBox_2, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans"))
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans"))
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans"))
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.radioButton = QtGui.QRadioButton(self.gridLayoutWidget)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.gridLayout.addWidget(self.radioButton, 1, 2, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.width_box = QtGui.QLineEdit(self.gridLayoutWidget)
        self.width_box.setObjectName(_fromUtf8("width_box"))
        self.horizontalLayout_2.addWidget(self.width_box)
        self.label_7 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans"))
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_2.addWidget(self.label_7)
        self.height_box = QtGui.QLineEdit(self.gridLayoutWidget)
        self.height_box.setObjectName(_fromUtf8("height_box"))
        self.horizontalLayout_2.addWidget(self.height_box)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans"))
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)
        self.comboBox_3 = QtGui.QComboBox(self.gridLayoutWidget)
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.gridLayout.addWidget(self.comboBox_3, 3, 1, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout_4.addWidget(self.cancelButton)
        self.gridLayout.addLayout(self.horizontalLayout_4, 6, 1, 1, 1)
        self.label = QtGui.QLabel(qgis2leaf)
        self.label.setGeometry(QtCore.QRect(10, 10, 131, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(qgis2leaf)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 431, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans"))
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.line = QtGui.QFrame(qgis2leaf)
        self.line.setGeometry(QtCore.QRect(10, 50, 441, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.listWidget = QtGui.QListWidget(qgis2leaf)
        self.listWidget.setGeometry(QtCore.QRect(10, 230, 341, 151))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.getButton = QtGui.QPushButton(qgis2leaf)
        self.getButton.setGeometry(QtCore.QRect(354, 350, 101, 31))
        self.getButton.setObjectName(_fromUtf8("getButton"))
        self.line_2 = QtGui.QFrame(qgis2leaf)
        self.line_2.setGeometry(QtCore.QRect(0, 380, 451, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.line_3 = QtGui.QFrame(qgis2leaf)
        self.line_3.setGeometry(QtCore.QRect(10, 210, 441, 16))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.textBrowser = QtGui.QTextBrowser(qgis2leaf)
        self.textBrowser.setGeometry(QtCore.QRect(10, 70, 441, 141))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.actionLoadList = QtGui.QAction(qgis2leaf)
        self.actionLoadList.setObjectName(_fromUtf8("actionLoadList"))

        self.retranslateUi(qgis2leaf)
        QtCore.QMetaObject.connectSlotsByName(qgis2leaf)

    def retranslateUi(self, qgis2leaf):
        qgis2leaf.setWindowTitle(_translate("qgis2leaf", "qgis2leaf", None))
        self.okButton.setText(_translate("qgis2leaf", "OK", None))
        self.pushButton_2.setText(_translate("qgis2leaf", "...", None))
        self.label_3.setText(_translate("qgis2leaf", "Output project folder:", None))
        self.label_4.setText(_translate("qgis2leaf", "Basemap:", None))
        self.label_6.setText(_translate("qgis2leaf", "Extent:", None))
        self.label_5.setText(_translate("qgis2leaf", "Frame width / height:", None))
        self.radioButton.setText(_translate("qgis2leaf", "full screen", None))
        self.label_7.setText(_translate("qgis2leaf", "/", None))
        self.label_9.setText(_translate("qgis2leaf", "Visible layers:", None))
        self.cancelButton.setText(_translate("qgis2leaf", "Cancel", None))
        self.label.setText(_translate("qgis2leaf", "QGIS 2 Leaflet", None))
        self.label_2.setText(_translate("qgis2leaf", "Export your current vector features to a working leaflet based webmap", None))
        self.getButton.setText(_translate("qgis2leaf", "get layers", None))
        self.textBrowser.setHtml(_translate("qgis2leaf", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">help: </span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Press &quot;<span style=\" font-weight:600;\">get layers</span>&quot; to add/reload your vector layers to the plugin </li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Frame width</span> defines the map dimension in the html page</li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Extent: <span style=\" font-weight:600;\">canvas extent - </span>QGIS canvas will influence initial leaflet view / choose <span style=\" font-weight:600;\">layer extent</span> to set the leaflet webmap extent to the extent of all vector layers</li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">For large datasets set the <span style=\" font-weight:600;\">visible layers</span> to &quot;show none&quot;. Visibility can be toggled in the webmap afterwards as you have a layer switcher</li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Choose one of the available <span style=\" font-weight:600;\">basemaps</span>. </li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">As <span style=\" font-weight:600;\">output project folder</span> you should choose a separate folder. There will be a designated folder in it with your current export files and folders.</li></ul></body></html>", None))
        self.actionLoadList.setText(_translate("qgis2leaf", "loadList", None))

