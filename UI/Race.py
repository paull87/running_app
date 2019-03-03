from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from settings.settings import Settings

settings = Settings()

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

class Ui_Race(object):
    def setupUi(self, Race):
        Race.setObjectName(_fromUtf8("Race"))
        Race.resize(400, 300)
        Race.setStyleSheet(_fromUtf8(""))
        Race.setWindowModality(QtCore.Qt.ApplicationModal)
        self.race_id = None
        self.centralwidget = QtWidgets.QWidget(Race)

        self.date_race = QtWidgets.QDateEdit(self.centralwidget)
        self.date_race.setGeometry(QtCore.QRect(50, 50, 120, 25))
        self.date_race.setCalendarPopup(True)

        item_delegate = QtWidgets.QStyledItemDelegate()

        self.combo_race_name = QtWidgets.QComboBox(self.centralwidget)
        self.combo_race_name.setGeometry(QtCore.QRect(50, 90, 240, 25))
        self.combo_race_name.setEditable(True)
        self.combo_race_name.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.combo_race_name.lineEdit().setPlaceholderText('Enter Race Name')
        self.combo_race_name.setItemDelegate(item_delegate)
        self.combo_race_name.currentTextChanged.connect(self.race_name_change)

        self.combo_race_distance = QtWidgets.QComboBox(self.centralwidget)
        self.combo_race_distance.setGeometry(QtCore.QRect(50, 130, 130, 25))

        self.time_goal = QtWidgets.QTimeEdit(self.centralwidget)
        self.time_goal.setGeometry(QtCore.QRect(50, 170, 80, 25))
        self.time_goal.setCalendarPopup(False)
        self.time_goal.setDisplayFormat('HH:mm:ss')

        self.time_actual = QtWidgets.QTimeEdit(self.centralwidget)
        self.time_actual.setGeometry(QtCore.QRect(50, 210, 80, 25))
        self.time_actual.setCalendarPopup(False)
        self.time_actual.setDisplayFormat('HH:mm:ss')

        self.button_save = QtWidgets.QPushButton(self.centralwidget)
        self.button_save.setGeometry(QtCore.QRect(240, 240, 75, 30))
        self.button_save.setText(_translate("Race", "Save", None))
        self.button_save.clicked.connect(self.save_race)

        Race.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Race)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        Race.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Race)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Race.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(Race)
        self.retranslateUi(Race)

        self.reset_form()

    def race_name_change(self):
        self.combo_race_name.setEditable(self.combo_race_name.currentIndex() == 0)
        print(self.combo_race_name.currentIndex(), self.combo_race_name.currentText())

    def set_race_distance_combo(self):
        """Sets the values for the combo_race_distance."""
        self.combo_race_distance.clear()
        self.combo_race_distance.addItem('', 0)
        for distance in settings.database.get_distances():
            self.combo_race_distance.addItem(distance.PrintName, distance.Name)

    def set_race_name_combo(self):
        """Sets the values for the combo_race_name."""
        self.combo_race_name.clear()
        self.combo_race_name.addItem('', '')
        for race_name in settings.database.get_race_list():
            self.combo_race_name.addItem(race_name[0], race_name[1])

    def reset_form(self):
        """Reset the form values."""
        self.date_race.setDate(QtCore.QDate.currentDate())
        self.set_race_distance_combo()
        self.set_race_name_combo()
        self.time_goal.setTime(QtCore.QTime(0, 0, 0))
        self.time_actual.setTime(QtCore.QTime(0, 0, 0))

    def save_race(self):
        """Saves the current race and race detail."""
        pass


    def retranslateUi(self, Race):
        Race.setWindowTitle(_translate("Race", "Race", None))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Race = QtWidgets.QMainWindow()
    ui = Ui_Race()
    ui.setupUi(Race)
    Race.show()
    sys.exit(app.exec_())
