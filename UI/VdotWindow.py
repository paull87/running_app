from PyQt5 import QtCore, QtWidgets
from settings.settings import Settings
from settings.converters import time_to_string
from VDOT.VDOT import VDOT
import datetime

settings = Settings()
vdot = VDOT(settings.database, settings.vdot)

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class UiVDOT(object):

    def setup_ui(self, vdot_widget):
        vdot_widget.resize(700, 400)
        vdot_widget.setWindowModality(QtCore.Qt.ApplicationModal)
        vdot_widget.setWindowTitle(_translate("VDOT", "VDOT", None))
        self.central_widget = QtWidgets.QWidget(vdot_widget)
        self.vdot = VDOT(settings.database, settings.vdot)

        self.combo_race_distance = QtWidgets.QComboBox(self.central_widget)
        self.combo_race_distance.setGeometry(QtCore.QRect(50, 20, 130, 25))

        self.race_time = QtWidgets.QTimeEdit(self.central_widget)
        self.race_time.setGeometry(QtCore.QRect(190, 20, 80, 25))
        self.race_time.setCalendarPopup(False)
        self.race_time.setDisplayFormat('HH:mm:ss')

        self.button_update = QtWidgets.QPushButton(self.central_widget)
        self.button_update.setGeometry(QtCore.QRect(270, 20, 75, 30))
        self.button_update.setText(_translate("VDOT", "Update", None))
        self.button_update.clicked.connect(self.update_vdot)

        self.button_save = QtWidgets.QPushButton(self.central_widget)
        self.button_save.setGeometry(QtCore.QRect(240, 340, 75, 30))
        self.button_save.setText(_translate("VDOT", "Save", None))
        self.button_save.clicked.connect(self.save_vdot)

        self.race_paces = QtWidgets.QTextEdit(self.central_widget)
        self.race_paces.setGeometry(QtCore.QRect(50, 50, 250, 280))

        self.training_paces = QtWidgets.QTextEdit(self.central_widget)
        self.training_paces.setGeometry(QtCore.QRect(350, 50, 250, 280))

        vdot_widget.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(vdot_widget)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        vdot_widget.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(vdot_widget)
        vdot_widget.setStatusBar(self.status_bar)

        QtCore.QMetaObject.connectSlotsByName(vdot_widget)

        self.reset_form()
        self.update_race_paces()
        self.update_training_paces()

    def set_race_distance_combo(self):
        """Sets the values for the combo_race_distance."""
        self.combo_race_distance.clear()
        self.combo_race_distance.addItem('', 0)
        for distance in settings.database.get_distances():
            self.combo_race_distance.addItem(distance.PrintName, distance.Name)

    def reset_form(self):
        """Reset the form values."""
        self.vdot = VDOT(settings.database, settings.vdot)
        self.set_race_distance_combo()
        self.race_time.setTime(QtCore.QTime(0, 0, 0))

    def complete_form(self):
        """Checks that the form has been completed before saving/editing."""
        return (self.combo_race_distance.currentIndex() > 0
                and self.race_time.time() > QtCore.QTime(0, 0, 0)
                )

    def save_vdot(self):
        """Saves the current race and race detail."""
        if self.complete_form():
            # settings.database.add_amend_race_detail(self.convert_race_entry())
            self.status_bar.showMessage('VDOT Saved', 5000)

    def update_vdot(self):
        self.vdot.calculate_vdot(
            self.combo_race_distance.itemData(self.combo_race_distance.currentIndex()),
            self.race_time.time().toString('hh:mm:ss'))
        self.update_race_paces()
        self.update_training_paces()

    def update_race_paces(self):
        self.race_paces.clear()
        text = ''
        for pace in sorted(self.vdot.race_times, key=lambda x: x.Time):
            pace_time = datetime.timedelta(seconds=pace.Time)
            pace_mile = datetime.timedelta(seconds=pace.Mile)
            text += '<p><b>{}</b> {} {}</p>\n'.format(pace.Distance, time_to_string(pace_time),
                                      time_to_string(pace_mile, '{minutes:02d}:{seconds:02d}'))
        self.race_paces.setText(text)

    def update_training_paces(self):
        self.training_paces.clear()
        text = ''
        training_paces = [x for x in self.vdot.training_paces
                          if x.Distance not in [x.Distance for x in self.vdot.race_times]]
        for pace in sorted(training_paces, key=lambda x: x.Mile):
            pace_mile = datetime.timedelta(seconds=pace.Mile)
            text += '<p><b>{}</b> {}</p>\n'.format(pace.Distance, time_to_string(pace_mile,
                                                                                 '{minutes:02d}:{seconds:02d}'))
        self.training_paces.setText(text)

    def get_race_name_combo_id(self, race_name):
        combo_id = self.combo_race_name.findText(race_name)
        combo_id = 0 if combo_id == -1 else combo_id
        return combo_id

    def get_race_distance_combo_id(self, distance):
        combo_id = self.combo_race_distance.findData(distance)
        combo_id = 0 if combo_id == -1 else combo_id
        return combo_id

    def get_race_details(self, vdot):
        self.reset_form()
        self.vdot = vdot


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    vdot_win = QtWidgets.QMainWindow()
    ui = UiVDOT()
    ui.setup_ui(vdot_win)
    vdot_win.show()
    sys.exit(app.exec_())
