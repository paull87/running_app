# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\PythonScripts\FitnessApp\UI\MainMenu.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

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

class Ui_RunningApp(object):
    def setupUi(self, RunningApp):
        RunningApp.setObjectName(_fromUtf8("RunningApp"))
        RunningApp.resize(501, 457)
        RunningApp.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/MenuImages/icons8-exercise-filled-50.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        RunningApp.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(RunningApp)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.buttonDiary = QtWidgets.QPushButton(self.centralwidget)
        self.buttonDiary.setGeometry(QtCore.QRect(100, 170, 101, 81))
        self.buttonDiary.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/MenuImages/icons8-spiral-bound-booklet-80.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonDiary.setIcon(icon1)
        self.buttonDiary.setIconSize(QtCore.QSize(64, 64))
        self.buttonDiary.setObjectName(_fromUtf8("buttonDiary"))
        self.buttonCalendar = QtWidgets.QPushButton(self.centralwidget)
        self.buttonCalendar.setGeometry(QtCore.QRect(230, 170, 101, 81))
        self.buttonCalendar.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/MenuImages/icons8-calendar-80.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonCalendar.setIcon(icon2)
        self.buttonCalendar.setIconSize(QtCore.QSize(64, 64))
        self.buttonCalendar.setObjectName(_fromUtf8("buttonCalendar"))
        self.buttonShoe = QtWidgets.QPushButton(self.centralwidget)
        self.buttonShoe.setGeometry(QtCore.QRect(100, 260, 101, 81))
        self.buttonShoe.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/MenuImages/icons8-trainers-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonShoe.setIcon(icon3)
        self.buttonShoe.setIconSize(QtCore.QSize(64, 64))
        self.buttonShoe.setObjectName("buttonShoe")
        RunningApp.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RunningApp)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 501, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        RunningApp.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RunningApp)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        RunningApp.setStatusBar(self.statusbar)

        self.retranslateUi(RunningApp)
        QtCore.QMetaObject.connectSlotsByName(RunningApp)

    def retranslateUi(self, RunningApp):
        RunningApp.setWindowTitle(_translate("RunningApp", "Running App", None))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RunningApp = QtGui.QMainWindow()
    ui = Ui_RunningApp()
    ui.setupUi(RunningApp)
    RunningApp.show()
    sys.exit(app.exec_())

