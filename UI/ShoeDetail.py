# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShoeDetail.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ShoeDetail(object):
    def setupUi(self, ShoeDetail):
        ShoeDetail.setObjectName("ShoeDetail")
        ShoeDetail.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(ShoeDetail)
        self.centralwidget.setObjectName("centralwidget")
        self.lineName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineName.setGeometry(QtCore.QRect(30, 30, 151, 20))
        self.lineName.setInputMask("")
        self.lineName.setText("")
        self.lineName.setObjectName("lineName")
        self.dateBought = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateBought.setGeometry(QtCore.QRect(30, 140, 111, 22))
        self.dateBought.setDate(QtCore.QDate(2018, 1, 1))
        self.dateBought.setCalendarPopup(True)
        self.dateBought.setObjectName("dateBought")
        self.dateRetired = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateRetired.setGeometry(QtCore.QRect(30, 170, 111, 22))
        self.dateRetired.setDate(QtCore.QDate(2018, 1, 1))
        self.dateRetired.setCalendarPopup(True)
        self.dateRetired.setObjectName("dateRetired")
        self.lineBrand = QtWidgets.QLineEdit(self.centralwidget)
        self.lineBrand.setGeometry(QtCore.QRect(30, 60, 151, 20))
        self.lineBrand.setText("")
        self.lineBrand.setObjectName("lineBrand")
        self.lineDescription = QtWidgets.QLineEdit(self.centralwidget)
        self.lineDescription.setGeometry(QtCore.QRect(30, 90, 191, 41))
        self.lineDescription.setText("")
        self.lineDescription.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lineDescription.setObjectName("lineDescription")
        self.linePrevMiles = QtWidgets.QLineEdit(self.centralwidget)
        self.linePrevMiles.setGeometry(QtCore.QRect(30, 200, 111, 20))
        self.linePrevMiles.setText("")
        self.linePrevMiles.setObjectName("linePrevMiles")
        self.linePrevKM = QtWidgets.QLineEdit(self.centralwidget)
        self.linePrevKM.setGeometry(QtCore.QRect(30, 230, 111, 20))
        self.linePrevKM.setText("")
        self.linePrevKM.setObjectName("linePrevKM")
        self.radioDefault = QtWidgets.QRadioButton(self.centralwidget)
        self.radioDefault.setGeometry(QtCore.QRect(30, 260, 101, 20))
        self.radioDefault.setObjectName("radioDefault")
        self.buttonSave = QtWidgets.QPushButton(self.centralwidget)
        self.buttonSave.setGeometry(QtCore.QRect(30, 310, 114, 32))
        self.buttonSave.setObjectName("buttonSave")
        ShoeDetail.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ShoeDetail)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        ShoeDetail.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ShoeDetail)
        self.statusbar.setObjectName("statusbar")
        ShoeDetail.setStatusBar(self.statusbar)

        self.retranslateUi(ShoeDetail)
        QtCore.QMetaObject.connectSlotsByName(ShoeDetail)

    def retranslateUi(self, ShoeDetail):
        _translate = QtCore.QCoreApplication.translate
        ShoeDetail.setWindowTitle(_translate("ShoeDetail", "Shoe Detail"))
        self.lineName.setPlaceholderText(_translate("ShoeDetail", "Name"))
        self.dateBought.setDisplayFormat(_translate("ShoeDetail", "dd/MM/yyyy"))
        self.dateRetired.setDisplayFormat(_translate("ShoeDetail", "dd/MM/yyyy"))
        self.lineBrand.setPlaceholderText(_translate("ShoeDetail", "Brand"))
        self.lineDescription.setPlaceholderText(_translate("ShoeDetail", "Description"))
        self.linePrevMiles.setPlaceholderText(_translate("ShoeDetail", "Previous Miles"))
        self.linePrevKM.setPlaceholderText(_translate("ShoeDetail", "Previous KM"))
        self.radioDefault.setText(_translate("ShoeDetail", "Default"))
        self.buttonSave.setText(_translate("ShoeDetail", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ShoeDetail = QtWidgets.QMainWindow()
    ui = Ui_ShoeDetail()
    ui.setupUi(ShoeDetail)
    ShoeDetail.show()
    sys.exit(app.exec_())

