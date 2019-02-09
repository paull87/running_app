# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShoeDetail.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from settings.settings import Settings
import datetime

settings= Settings()

class Ui_ShoeDetail(object):
    def setupUi(self, ShoeDetail):
        ShoeDetail.setObjectName("ShoeDetail")
        ShoeDetail.resize(800, 600)
        ShoeDetail.setWindowModality(QtCore.Qt.ApplicationModal)
        self.parent_window = None
        self.centralwidget = QtWidgets.QWidget(ShoeDetail)
        self.centralwidget.setObjectName("centralwidget")
        self.lineName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineName.setGeometry(QtCore.QRect(30, 30, 151, 20))
        self.lineName.setObjectName("lineName")
        self.dateBought = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateBought.setGeometry(QtCore.QRect(30, 140, 111, 22))
        self.dateBought.setCalendarPopup(True)
        self.dateBought.setObjectName("dateBought")
        self.dateRetired = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateRetired.setGeometry(QtCore.QRect(30, 170, 111, 22))
        self.dateRetired.setCalendarPopup(True)
        self.dateRetired.setObjectName("dateRetired")
        self.lineBrand = QtWidgets.QLineEdit(self.centralwidget)
        self.lineBrand.setGeometry(QtCore.QRect(30, 60, 151, 20))
        self.lineBrand.setObjectName("lineBrand")
        self.lineDescription = QtWidgets.QLineEdit(self.centralwidget)
        self.lineDescription.setGeometry(QtCore.QRect(30, 90, 191, 41))
        self.lineDescription.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lineDescription.setObjectName("lineDescription")
        self.linePrevMiles = QtWidgets.QLineEdit(self.centralwidget)
        self.linePrevMiles.setGeometry(QtCore.QRect(30, 200, 111, 20))
        self.linePrevMiles.setObjectName("linePrevMiles")
        self.linePrevKM = QtWidgets.QLineEdit(self.centralwidget)
        self.linePrevKM.setGeometry(QtCore.QRect(30, 230, 111, 20))
        self.linePrevKM.setObjectName("linePrevKM")
        self.radioDefault = QtWidgets.QRadioButton(self.centralwidget)
        self.radioDefault.setGeometry(QtCore.QRect(30, 260, 101, 20))
        self.radioDefault.setObjectName("radioDefault")
        self.buttonSave = QtWidgets.QPushButton(self.centralwidget)
        self.buttonSave.setGeometry(QtCore.QRect(30, 310, 114, 32))
        self.buttonSave.setObjectName("buttonSave")
        self.buttonSave.clicked.connect(self.save_shoe)
        ShoeDetail.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ShoeDetail)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        ShoeDetail.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ShoeDetail)
        self.statusbar.setObjectName("statusbar")
        ShoeDetail.setStatusBar(self.statusbar)
        self.reset_shoe_detail()

        self.retranslateUi(ShoeDetail)
        QtCore.QMetaObject.connectSlotsByName(ShoeDetail)

    def reset_shoe_detail(self):
        self.shoeID = None
        self.lineName.setText(None)
        self.lineBrand.setText(None)
        self.lineDescription.setText(None)
        self.radioDefault.setChecked(False)
        self.dateBought.setSpecialValueText(" ")
        self.dateBought.setDate(QtCore.QDate.fromString("01/01/0001", "dd/MM/yyyy"))
        self.dateRetired.setSpecialValueText(" ")
        self.dateRetired.setDate(QtCore.QDate.fromString("01/01/0001", "dd/MM/yyyy"))
        self.linePrevMiles.setText(str(0))
        self.linePrevKM.setText(str(0))

    def get_shoe_detail(self, shoe_id):
        self.shoeID = shoe_id
        shoe = settings.database.get_shoe_detail(shoe_id)
        self.lineName.setText(shoe.ShoeName)
        self.lineBrand.setText(shoe.Brand)
        self.lineDescription.setText(shoe.Description)
        self.radioDefault.setChecked(bool(shoe.IsDefault))
        if shoe.StartDate is not None:
            date_bought = QtCore.QDate(shoe.StartDate.year, shoe.StartDate.month, shoe.StartDate.day)
            self.dateBought.setDate(date_bought)
        if shoe.DateRetired is not None:
            date_retired = QtCore.QDate(shoe.DateRetired.year, shoe.DateRetired.month, shoe.DateRetired.day)
            self.dateRetired.setDate(date_retired)
        self.linePrevMiles.setText(str(shoe.PreviousMiles))
        self.linePrevKM.setText(str(shoe.PreviousKM))

    def save_shoe(self):
        date_bought = (None if str(self.dateBought.date().toPyDate()) == '1752-09-14'
                       else datetime.datetime.combine(self.dateBought.date().toPyDate(), datetime.datetime.min.time()))
        date_retired = (None if str(self.dateRetired.date().toPyDate()) == '1752-09-14'
                        else datetime.datetime.combine(self.dateRetired.date().toPyDate(), datetime.datetime.min.time()))
        shoe_details = (self.shoeID, self.lineName.text(), self.lineBrand.text(), self.lineDescription.text(),
                        date_bought, date_retired, self.linePrevMiles.text(), self.linePrevKM.text(),
                        self.radioDefault.isChecked())

        try:
            settings.database.add_amend_shoe(shoe_details)
            if self.parent_window:
                self.parent_window.insert_shoes()
            self.hide()
            print('saved')
        except Exception as e:
            print(f'error: {e}')

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

