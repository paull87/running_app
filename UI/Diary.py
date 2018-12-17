# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\PythonScripts\FitnessApp\UI\Diary.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_Diary(object):
    def setupUi(self, Diary):
        Diary.setObjectName(_fromUtf8("Diary"))
        Diary.resize(800, 600)
        Diary.setStyleSheet(_fromUtf8(""))
        self.centralwidget = QtWidgets.QWidget(Diary)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.comboShoe = QtWidgets.QComboBox(self.centralwidget)
        self.comboShoe.setGeometry(QtCore.QRect(70, 200, 69, 22))
        self.comboShoe.setObjectName(_fromUtf8("comboShoe"))
        self.lineDistance = QtWidgets.QLineEdit(self.centralwidget)
        self.lineDistance.setGeometry(QtCore.QRect(80, 250, 113, 20))
        self.lineDistance.setFrame(True)
        self.lineDistance.setObjectName(_fromUtf8("lineDistance"))
        self.comboRunType = QtWidgets.QComboBox(self.centralwidget)
        self.comboRunType.setGeometry(QtCore.QRect(70, 160, 113, 22))
        self.comboRunType.setObjectName(_fromUtf8("comboRunType"))
        self.lineSpeed = QtWidgets.QLineEdit(self.centralwidget)
        self.lineSpeed.setGeometry(QtCore.QRect(80, 290, 113, 20))
        self.lineSpeed.setObjectName(_fromUtf8("lineSpeed"))
        self.comboDistance = QtWidgets.QComboBox(self.centralwidget)
        self.comboDistance.setGeometry(QtCore.QRect(200, 250, 69, 22))
        self.comboDistance.setObjectName(_fromUtf8("comboDistance"))
        self.comboDistance.addItem(_fromUtf8(""))
        self.comboDistance.addItem(_fromUtf8(""))
        self.linePace = QtWidgets.QLineEdit(self.centralwidget)
        self.linePace.setGeometry(QtCore.QRect(80, 330, 113, 20))
        self.linePace.setObjectName(_fromUtf8("linePace"))
        self.comboSpeed = QtWidgets.QComboBox(self.centralwidget)
        self.comboSpeed.setGeometry(QtCore.QRect(200, 290, 69, 22))
        self.comboSpeed.setObjectName(_fromUtf8("comboSpeed"))
        self.comboSpeed.addItem(_fromUtf8(""))
        self.comboSpeed.addItem(_fromUtf8(""))
        self.comboPace = QtWidgets.QComboBox(self.centralwidget)
        self.comboPace.setGeometry(QtCore.QRect(200, 330, 69, 22))
        self.comboPace.setObjectName(_fromUtf8("comboPace"))
        self.comboPace.addItem(_fromUtf8(""))
        self.comboPace.addItem(_fromUtf8(""))
        self.lineAvgHR = QtWidgets.QLineEdit(self.centralwidget)
        self.lineAvgHR.setGeometry(QtCore.QRect(80, 370, 61, 20))
        self.lineAvgHR.setObjectName(_fromUtf8("lineAvgHR"))
        self.lineNotes = QtWidgets.QLineEdit(self.centralwidget)
        self.lineNotes.setGeometry(QtCore.QRect(80, 410, 271, 91))
        self.lineNotes.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lineNotes.setObjectName(_fromUtf8("lineNotes"))
        self.lineWeight = QtWidgets.QLineEdit(self.centralwidget)
        self.lineWeight.setGeometry(QtCore.QRect(80, 520, 61, 20))
        self.lineWeight.setObjectName(_fromUtf8("lineWeight"))
        self.lineRestingHR = QtWidgets.QLineEdit(self.centralwidget)
        self.lineRestingHR.setGeometry(QtCore.QRect(160, 520, 61, 20))
        self.lineRestingHR.setObjectName(_fromUtf8("lineRestingHR"))
        self.buttonSave = QtWidgets.QPushButton(self.centralwidget)
        self.buttonSave.setGeometry(QtCore.QRect(450, 440, 75, 23))
        self.buttonSave.setObjectName(_fromUtf8("buttonSave"))
        self.timeDiary = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeDiary.setGeometry(QtCore.QRect(210, 110, 118, 22))
        self.timeDiary.setCalendarPopup(False)
        self.timeDiary.setObjectName(_fromUtf8("timeDiary"))
        self.DateDiary = QtWidgets.QDateEdit(self.centralwidget)
        self.DateDiary.setGeometry(QtCore.QRect(70, 110, 110, 22))
        self.DateDiary.setCalendarPopup(True)
        self.DateDiary.setObjectName(_fromUtf8("DateDiary"))
        self.webView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.webView.setGeometry(QtCore.QRect(410, 80, 371, 291))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.lineStravaID = QtWidgets.QLineEdit(self.centralwidget)
        self.lineStravaID.setGeometry(QtCore.QRect(270, 520, 61, 20))
        self.lineStravaID.setObjectName(_fromUtf8("lineStravaID"))
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(530, 390, 264, 155))
        self.calendarWidget.setStyleSheet(_fromUtf8("QToolButton {\n"
"height: 20px;\n"
"width: 70px;\n"
"color: white;\n"
"font-size: 14px;\n"
"icon-size: 20px, 20px;\n"
"background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333);\n"
"}\n"
"QMenu {\n"
"width: 150px;\n"
"left: 20px;\n"
"color: white;\n"
"font-size: 14px;\n"
"background-color: rgb(100, 100, 100);\n"
"}\n"
"QSpinBox { \n"
"width: 70px; \n"
"font-size:14px; \n"
"color: white;  \n"
"background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333);\n"
"selection-background-color: transparent;\n"
"selection-color: rgb(255, 255, 255);\n"
"}\n"
"QSpinBox::up-button { subcontrol-origin: border; subcontrol-position: top right; width:20px; }\n"
"QSpinBox::down-button {subcontrol-origin: border; subcontrol-position: bottom right; width:20px;}\n"
"QSpinBox::up-arrow { width:10px; height:20px; }\n"
"QSpinBox::down-arrow { width:10px; height:20px; }\n"
"QWidget { alternate-background-color: rgb(128, 128, 128); }\n"
"QAbstractItemView:enabled \n"
"{\n"
"font-size:10px; \n"
"color: rgb(180, 180, 180); \n"
"background-color: black; \n"
"selection-background-color: rgb(64, 64, 64); \n"
"selection-color: rgb(0, 255, 0); \n"
"}\n"
"QWidget#qt_calendar_navigationbar\n"
"{ \n"
"background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333); \n"
"}\n"
"\n"
"QAbstractItemView:disabled \n"
"{ \n"
"color: rgb(64, 64, 64); \n"
"}"))
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(True)
        self.calendarWidget.setObjectName(_fromUtf8("calendarWidget"))
        Diary.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Diary)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        Diary.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Diary)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Diary.setStatusBar(self.statusbar)

        self.DateDiary.setCalendarWidget(self.calendarWidget)

        icon_back = QtGui.QIcon()
        icon_back.addPixmap(QtGui.QPixmap(_fromUtf8(":/MenuImages/icons8-back-26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon_forward = QtGui.QIcon()
        icon_forward.addPixmap(QtGui.QPixmap(_fromUtf8(":/MenuImages/icons8-forward-26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)


        for child in self.calendarWidget.children():
            for c in child.children():
                if c.objectName() == 'qt_calendar_prevmonth':
                    c.setIcon(icon_back)
                    #c.setText(_translate("Diary", "P", None))
                if c.objectName() == 'qt_calendar_nextmonth':
                    c.setIcon(icon_forward)
                    #c.setText(_translate("Diary", "N", None))

        self.retranslateUi(Diary)

        QtCore.QMetaObject.connectSlotsByName(Diary)

    def retranslateUi(self, Diary):
        Diary.setWindowTitle(_translate("Diary", "MainWindow", None))
        self.lineDistance.setPlaceholderText(_translate("Diary", "Distance", None))
        self.lineSpeed.setPlaceholderText(_translate("Diary", "Speed", None))
        self.comboDistance.setItemText(0, _translate("Diary", "Mile", None))
        self.comboDistance.setItemText(1, _translate("Diary", "KM", None))
        self.linePace.setPlaceholderText(_translate("Diary", "Pace", None))
        self.comboSpeed.setItemText(0, _translate("Diary", "mph", None))
        self.comboSpeed.setItemText(1, _translate("Diary", "kmph", None))
        self.comboPace.setItemText(0, _translate("Diary", "Mile/min", None))
        self.comboPace.setItemText(1, _translate("Diary", "KM/min", None))
        self.lineAvgHR.setPlaceholderText(_translate("Diary", "Avg HR", None))
        self.lineNotes.setPlaceholderText(_translate("Diary", "Commet...", None))
        self.lineWeight.setPlaceholderText(_translate("Diary", "Weight", None))
        self.lineRestingHR.setPlaceholderText(_translate("Diary", "Rest HR", None))
        self.buttonSave.setText(_translate("Diary", "Save", None))
        self.lineStravaID.setPlaceholderText(_translate("Diary", "StravaID", None))

import resources_rc

#from PyQt5 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Diary = QtGui.QMainWindow()
    ui = Ui_Diary()
    ui.setupUi(Diary)
    Diary.show()
    sys.exit(app.exec_())

