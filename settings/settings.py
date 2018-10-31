import os
import datetime
from settings.converters import dec
from settings.database import DB
from dateutil.relativedelta import relativedelta


class Settings:
    """Class containing the settings of the app."""
    def __init__(self, app_path='..'):
        """Initialise the settings."""
        self.APP_PATH = os.path.abspath(app_path)
        self.WORKOUTS_PATH = os.path.join(self.APP_PATH, 'Workouts')
        self.FIT_PATH = os.path.join(self.APP_PATH, 'Workouts', 'FIT')
        #self.VDOT_RACES = '..\\VDOT\\VDOT Races.txt'
        #self.VDOT_TRAINING = '..\\VDOT\\VDOT Training.txt'
        #self.CONFIG = temp_path('config.tmp')
        #self.WORKOUT_PLANS = '..\\template\\plans\\'
        #self.SCHEDULE_PLANS = '..\\Workouts\\schedule\\'
        self.DATABASE_PATH = os.path.join(self.APP_PATH, 'FitnessDB.db')
        self.database = DB(self.DATABASE_PATH)
        self.setup_environment()
        self.get_settings()
        self.get_zones()
        self.targets = {
            'target_type': '2',
        }

        self.durations = {
            'duration_type': '5',
        }

        self.schedule_template = """Type,Local Number,Message,Field 1,Value 1,Units 1,Field 2,Value 2,Units 2,Field 3,Value 3,Units 3,Field 4,Value 4,Units 4,Field 5,Value 5,Units 5,Field 6,Value 6,Units 6,Field 7,Value 7,Units 7,
Definition,0,file_id,type,1,,manufacturer,1,,product,1,,time_created,1,,serial_number,1,,number,1,,,,,
Data,0,file_id,type,"7",,manufacturer,"1",,garmin_product,"65534",,time_created,"{}",,serial_number,"1",,number,"1",,,,,
Definition,0,file_creator,software_version,1,,hardware_version,1,,,,,,,,,,,,,,,,,
Data,0,file_creator,software_version,"17",,hardware_version,"0",,,,,,,,,,,,,,,,,
Definition,0,schedule,manufacturer,1,,product,1,,serial_number,1,,time_created,1,,type,1,,scheduled_time,1,,completed,1,,
"""

        self.workout_template = """Type,Local Number,Message,Field 1,Value 1,Units 1,Field 2,Value 2,Units 2,Field 3,Value 3,Units 3,Field 4,Value 4,Units 4,Field 5,Value 5,Units 5,Field 6,Value 6,Units 6,Field 7,Value 7,Units 7,Field 8,Value 8,Units 8,Field 9,Value 9,Units 9,
Definition,0,file_id,serial_number,1,,time_created,1,,manufacturer,1,,product,1,,number,1,,type,1,,,,,,,,,,,
Data,0,file_id,serial_number,"{0}",,time_created,"{1}",,manufacturer,"1",,garmin_product,"65534",,type,"5",,,,,,,,,,,,,,
Definition,0,file_creator,software_version,1,,hardware_version,1,,,,,,,,,,,,,,,,,,,,,,,
Data,0,file_creator,software_version,"1509",,hardware_version,"0",,,,,,,,,,,,,,,,,,,,,,,
Definition,0,workout,capabilities,1,,wkt_name,16,,num_valid_steps,1,,,,,,,,,,,,,,,,,,,,
Data,0,workout,capabilities,"32",,wkt_name,"{2}",,num_valid_steps,"{3}",,sport,"1",,,,,,,,,,,,,,,,,
"""

    def setup_environment(self):
        """Creates the folders if they do not already exist."""
        if not os.path.isdir(self.WORKOUTS_PATH):
            os.mkdir(self.WORKOUTS_PATH)
        if not os.path.isdir(self.FIT_PATH):
            os.mkdir(self.FIT_PATH)


    def get_settings(self):
        """Gets the current settings from the database."""
        name, dob, vdot, hr, units = (self.database.get_current_settings())
        self.username = name
        self.dob = dob
        self.vdot = dec(vdot, 2)
        self.max_hr = hr
        self.units = units

    def get_zones(self):
        """Gets the current pace and heart rate zones for workouts."""
        self.zones = self.database.get_targets(self.units)

    def update_settings(self, field, value):
        """Updates the settings."""
        self.database.update_settings(field, value)
        self.get_settings()

    def get_calendar(self, month, year):
        """Returns the calendar file contents."""
        date_from = datetime.datetime(day=1, month=month, year=year)
        date_to = date_from + relativedelta(months=1)
        return self.database.get_calendar_range(date_from, date_to)

    def calculate_intensity_points(self, hr, time_taken):
        """Calculates the intensity points for the given hr and time."""
        max_hr_percent = dec((hr / self.max_hr), 2) * 100
        mins = dec(time_taken.total_seconds() / 60, 2)
        points = dec(self.database.get_points(max_hr_percent))
        total_points = points * mins
        return dec(total_points, 3)


def temp_path(filename):
    """Returns path to use for the config file."""
    try:
        path = os.environ['TEMP']
    except:
        path = '.'
    return os.path.join(path, filename)


def appdata_path(filename):
    """Returns app data path to use for the config file."""
    try:
        path = os.path.join(os.environ['APPDATA'], 'FitnessApp')
        _create_appdata_folder(path)
    except:
        path = '.'
        _create_appdata_folder(path)
    return os.path.join(path, filename)


def _create_appdata_folder(path):
    """Creates the FitnessApp folder if not exists."""
    if not os.path.isdir(path):
        os.mkdir(path)