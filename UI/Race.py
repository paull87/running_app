from PyQt5 import QtCore, QtWidgets
from settings.settings import Settings
import datetime

settings = Settings()

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class UiRace(object):

    def __init__(self):
        self.race_id = None
        self.central_widget = None
        self.date_race = None
        self.combo_race_name = None
        self.combo_race_distance = None
        self.time_goal = None
        self.time_actual = None
        self.button_save = None
        self.menu_bar = None
        self.status_bar = None

    def setup_ui(self, race):
        race.resize(400, 300)
        race.setWindowModality(QtCore.Qt.ApplicationModal)
        race.setWindowTitle(_translate("Race", "Race", None))
        self.central_widget = QtWidgets.QWidget(race)

        self.date_race = QtWidgets.QDateEdit(self.central_widget)
        self.date_race.setGeometry(QtCore.QRect(50, 50, 120, 25))
        self.date_race.setCalendarPopup(True)

        item_delegate = QtWidgets.QStyledItemDelegate()

        self.combo_race_name = QtWidgets.QComboBox(self.central_widget)
        self.combo_race_name.setGeometry(QtCore.QRect(50, 90, 240, 25))
        self.combo_race_name.setEditable(True)
        self.combo_race_name.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.combo_race_name.lineEdit().setPlaceholderText('Enter Race Name')
        self.combo_race_name.setItemDelegate(item_delegate)
        self.combo_race_name.currentTextChanged.connect(self.race_name_change)

        self.combo_race_distance = QtWidgets.QComboBox(self.central_widget)
        self.combo_race_distance.setGeometry(QtCore.QRect(50, 130, 130, 25))

        self.time_goal = QtWidgets.QTimeEdit(self.central_widget)
        self.time_goal.setGeometry(QtCore.QRect(50, 170, 80, 25))
        self.time_goal.setCalendarPopup(False)
        self.time_goal.setDisplayFormat('HH:mm:ss')

        self.time_actual = QtWidgets.QTimeEdit(self.central_widget)
        self.time_actual.setGeometry(QtCore.QRect(50, 210, 80, 25))
        self.time_actual.setCalendarPopup(False)
        self.time_actual.setDisplayFormat('HH:mm:ss')

        self.button_save = QtWidgets.QPushButton(self.central_widget)
        self.button_save.setGeometry(QtCore.QRect(240, 240, 75, 30))
        self.button_save.setText(_translate("Race", "Save", None))
        self.button_save.clicked.connect(self.save_race)

        Race.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(Race)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        Race.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(Race)
        Race.setStatusBar(self.status_bar)

        QtCore.QMetaObject.connectSlotsByName(Race)

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

    def complete_form(self):
        """Checks that the form has been completed before saving/editing."""
        return (self.combo_race_name.currentText() != ''
                and self.combo_race_distance.currentIndex() > 0
                and self.time_goal.time() > QtCore.QTime(0, 0, 0)
                )

    def convert_race_entry(self):
        return (
            datetime.datetime.combine(self.date_race.date().toPyDate(), datetime.datetime.min.time()),
            self.combo_race_name.currentText(),
            self.combo_race_distance.itemData(self.combo_race_distance.currentIndex()),
            (datetime.datetime.combine(datetime.date.min, self.time_goal.time().toPyTime())
             - datetime.datetime.min).total_seconds(),
            (datetime.datetime.combine(datetime.date.min, self.time_actual.time().toPyTime())
             - datetime.datetime.min).total_seconds()
        )

    def save_race(self):
        """Saves the current race and race detail."""
        if self.complete_form():
            print(self.convert_race_entry())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Race = QtWidgets.QMainWindow()
    ui = UiRace()
    ui.setup_ui(Race)
    Race.show()
    sys.exit(app.exec_())
