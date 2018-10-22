from typing import re

from settings.converters import dec
from settings.db_deployment import deploy_database
from settings.database import DB
from dateutil.relativedelta import relativedelta
import json
import os
import sqlite3
import datetime


class Settings:
    """Class containing the settings of the app."""
    def __init__(self):
        """Initialise the settings."""
        self.WORKOUTS_PATH = '..\\Workouts\\'
        self.FIT_PATH = '..\\Workouts\\FIT\\'
        self.VDOT_RACES = '..\\VDOT\\VDOT Races.txt'
        self.VDOT_TRAINING = '..\\VDOT\\VDOT Training.txt'
        self.CONFIG = temp_path('config.tmp')
        #self.WORKOUT_TEMPLATES = '..\\template\\workout templates.json' #  temp_path('workout templates.json')
        self.WORKOUT_PLANS = '..\\template\\plans\\'
        self.SCHEDULE_PLANS = '..\\Workouts\\schedule\\'
        self.DATABASE_PATH = appdata_path('FitnessDB.db')
        self.database = DB(self.DATABASE_PATH)
        self.get_settings()
        self.zones = self.get_zones()
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

    def get_settings(self):
        """Gets the current settings from the database."""
        vdot, hr, units = (self.database.get_current_settings())
        self.vdot = dec(vdot, 2)
        self.max_hr = hr
        self.units = units

    def get_zones(self):
        """Gets the current pace and heart rate zones for workouts."""
        return self.database.get_targets(self.units)

    def get_run_types(self):
        """returns the list of run types."""
        return self.database.get_run_types()

    def update_settings(self, field, value):
        """Updates the settings."""
        self.database.update_settings(field, value)

    def get_config(self):
        """Returns the cofig file contents."""
        self._check_config_exists()
        try:
            with open(self.CONFIG, 'r') as config_file:
                config_json = json.loads(config_file.read())
            return config_json
        except Exception as e:
            print('Unable to open config file: ', e)

    def _check_config_exists(self):
        """Create the config if it doesn't exist."""
        if not os.path.isfile(self.CONFIG):
            self._create_config()

    def _create_config(self):
        """Creates a default empty config file."""
        FILE_ATTRIBUTE_HIDDEN = 0x02
        empty_file = {
            "vdot": "",
            "paces": "",
            "max_hr": "200"
        }
        try:
            with open(self.CONFIG, 'w') as file:
                json.dump(empty_file, file)
        except Exception as e:
            print('Unable to create config file: ', e)

    def amend_config(self, key, value):
        """Amends the value of existing configs."""
        config = self.get_config()
        config[key] = value
        try:
            with open(self.CONFIG, 'w') as file:
                json.dump(config, file)
        except Exception as e:
            print('Unable to amend config file: ', e)

    def get_workouts(self):
        """Returns the workout contents."""
        return self.database.get_workouts()

    def get_single_workout(self, name):
        """Returns the given workout."""
        return self.database.get_single_workout(name)

    def update_workout(self, workout):
        """Updates the workout details."""
        self.database.update_workout(workout)

    def schedule_workouts(self, workouts, start_date, end_date, schedule_id, plan_name, vdot):
        """Adds schedule workouts to the planned schedules."""
        self.database.schedule_workouts(workouts, start_date, end_date, schedule_id, plan_name, vdot)

    def schedule_race(self, distance_id, race_date, race_name=None):
        """Adds the given race detail to race schedule."""
        return self.database.schedule_race(distance_id, race_date, race_name)

    def list_plans(self):
        """Returns list of default plans available."""
        return ['.'.join(x.split('.')[:-1]) for x in os.listdir(self.WORKOUT_PLANS)]

    def get_plan_schedule(self, name):
        """Returns the plan of the given name."""
        return self.database.get_schedule_workouts(name)

    def get_calendar(self, month, year):
        """Returns the calendar file contents."""
        date_from = datetime.datetime(day=1, month=month, year=year)
        date_to = date_from + relativedelta(months=1)
        return self.database.get_calendar_range(date_from, date_to)

    def amend_calendar(self, day, value):
        """Amends the day of existing calendar."""
        calendar = self.get_calendar()
        calendar[day] = value
        try:
            with open(self.CALENDAR, 'w') as file:
                json.dump(calendar, file)
        except Exception as e:
            print('Unable to amend calendar file: ', e)

    def add_diary(self, diary_entry):
        """Adds or amends a diary entry."""
        return self.database.add_diary_entry(diary_entry)


    def _connect_db(self):
        """Checks if database exists and creates it if not."""
        if not os.path.isfile(self.DATABASE_PATH):
            deploy_database(self.DATABASE_PATH)
        try:
            return sqlite3.connect(self.DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        except Exception as e:
            print('Unable to connect to database: ', e)

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


if __name__ == '__main__':
    settings = Settings()

    config_test = settings.get_config()
    print(config_test)

    settings.amend_config('vdot', str(dec('51.2', 1)))

    config_test = settings.get_config()
    print(config_test)

    print(settings.list_plans())