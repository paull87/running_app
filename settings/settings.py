from settings.converters import dec
import json
import os


class Settings:
    """Class containing the settings of the app."""
    def __init__(self):
        """Initialise the settings."""
        self.TEMPLATE_PATH = '..\\template\\template.txt'
        self.CALENDAR = '..\\Calendar\\calendar.json'
        self.SCHEDULE_PATH = '..\\template\\schedule.txt'
        self.WORKOUTS_PATH = '..\\Workouts\\'
        self.FIT_PATH = '..\\Workouts\\FIT\\'
        self.VDOT_RACES = '..\\VDOT\\VDOT Races.txt'
        self.VDOT_TRAINING = '..\\VDOT\\VDOT Training.txt'
        self.CONFIG = temp_path('config.tmp')
        self.WORKOUT_TEMPLATES = '..\\template\\workout templates.json' #  temp_path('workout templates.json')
        self.WORKOUT_PLANS = '..\\template\\plans\\'
        self.SCHEDULE_PLANS = '..\\Workouts\\schedule\\'
        self.DATABASE_PATH = appdata_path('FitnessDB.db')
        self.units = 'mile'
        self.max_hr = 189
        self.zones = {
            'easy': [dec(dec('0.7', 2) * dec(self.max_hr, 0), 0, 'ROUND_FLOOR'),
                     dec(dec('0.81', 2) * dec(self.max_hr, 0), 0, 'ROUND_CEILING')],
            'long': [dec(dec('0.74', 2) * dec(self.max_hr, 0), 0, 'ROUND_FLOOR'),
                     dec(dec('0.84', 2) * dec(self.max_hr, 0), 0, 'ROUND_CEILING')],
            'recovery': [dec(dec('0.5', 2) * dec(self.max_hr, 0), 0, 'ROUND_FLOOR'),
                         dec(dec('0.76', 2) * dec(self.max_hr, 0), 0, 'ROUND_CEILING')],
            'interval': [dec(dec('0.94', 2) * dec(self.max_hr, 0), 0, 'ROUND_FLOOR'),
                         dec(dec('0.98', 2) * dec(self.max_hr, 0), 0, 'ROUND_CEILING')],
            'threshold': [dec(dec('0.8', 2) * dec(self.max_hr, 0), 0, 'ROUND_FLOOR'),
                          dec(dec('0.91', 2) * dec(self.max_hr, 0), 0, 'ROUND_CEILING')],
            'repetition': [dec(dec('0.9', 2) * dec(self.max_hr, 0), 0, 'ROUND_FLOOR'),
                           dec(dec('1', 2) * dec(self.max_hr, 0), 0, 'ROUND_CEILING')],
        }
        self.targets = {
            'target_type': '2',
        }

        self.durations = {
            'duration_type': '5',
        }
        self.default_targets = {
            'easy': 'hr',
            'long': 'hr',
            'recovery': 'hr',
            'interval': 'pace',
            'threshold': 'pace',
            'repetition': 'pace'
        }

    def get_pace_targets(self, target_high, target_low):
        """Creates targets based on given paces"""
        pace_targets = self.targets.copy()
        pace_targets['target_type'] = '0'
        pace_targets['target_speed_zone'] = '0'
        pace_targets['custom_target_speed_low'] = str(target_low) + ',m/s'
        pace_targets['custom_target_speed_high'] = str(target_high) + ',m/s'
        return pace_targets

    def get_hr_targets(self, target_high, target_low):
        """Creates targets based on given heart rate"""
        hr_targets = self.targets.copy()
        hr_targets['target_type'] = '1'
        hr_targets['target_hr_zone'] = '0'
        hr_targets['custom_target_heart_rate_low'] = str(target_low) + ',% or bpm'
        hr_targets['custom_target_heart_rate_high'] = str(target_high) + ',% or bpm'
        return hr_targets

    def get_open_targets(self):
        """Creates open targets."""
        open_targets = self.targets.copy()
        open_targets['target_value'] = '0'
        return open_targets

    def get_time_durations(self, duration):
        """Creates durations based on time."""
        time_durations = self.durations.copy()
        time_durations['duration_type'] = '0'
        time_durations['duration_time'] = str(duration) + ',s'
        return time_durations

    def get_distance_durations(self, duration):
        """Creates durations based on distance."""
        distance_durations = self.durations.copy()
        distance_durations['duration_type'] = '1'
        distance_durations['duration_distance'] = str(duration) + ',m'
        return distance_durations

    def get_repeat_durations(self, step_id, repeats):
        """Creates durations based on repeats."""
        repeat_durations = self.durations.copy()
        repeat_durations['duration_type'] = '6'
        repeat_durations['duration_step'] = str(step_id)
        repeat_durations['repeat_steps'] = str(repeats)
        return repeat_durations

    def get_open_durations(self):
        """Creates durations based on repeats."""
        open_durations = self.durations.copy()
        open_durations['duration_value'] = '0'
        return open_durations

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

    def get_templates(self):
        """Returns the templates file contents."""
        self._check_templates_exists()
        try:
            with open(self.WORKOUT_TEMPLATES, 'r') as templates_file:
                templates_json = json.loads(templates_file.read())
            return templates_json
        except Exception as e:
            print('Unable to open templates file: ', e)

    def _check_templates_exists(self):
        """Create the config if it doesn't exist."""
        if not os.path.isfile(self.WORKOUT_TEMPLATES):
            self._create_templates()

    def _create_templates(self):
        """Creates a default empty config file."""
        FILE_ATTRIBUTE_HIDDEN = 0x02
        empty_file = {}
        try:
            with open(self.WORKOUT_TEMPLATES, 'w') as file:
                json.dump(empty_file, file)
        except Exception as e:
            print('Unable to create Templates file: ', e)

    def update_template_filename(self, name, filename, serial):
        """Updates the filename of the template"""
        templates = self.get_templates()
        templates[name]['filename'] = filename
        templates[name]['serial'] = serial
        try:
            with open(self.WORKOUT_TEMPLATES, 'w') as file:
                json.dump(templates, file)
        except Exception as e:
            print('Unable to amend template: ', e)

    def list_plans(self):
        """Returns list of default plans available."""
        return ['.'.join(x.split('.')[:-1]) for x in os.listdir(self.WORKOUT_PLANS)]

    def get_plan_schedule(self, name):
        """Returns the plan of the given name."""
        plan = os.path.join(self.WORKOUT_PLANS, name + '.json')
        try:
            with open(plan, 'r') as plan_file:
                plan_json = json.loads(plan_file.read())
            return plan_json
        except Exception as e:
            print('Unable to open plan file: ', e)

    def get_calendar(self):
        """Returns the calendar file contents."""
        self._check_calendar_exists()
        try:
            with open(self.CALENDAR, 'r') as calendar_file:
                calendar_json = json.loads(calendar_file.read())
            return calendar_json
        except Exception as e:
            print('Unable to open calendar file: ', e)

    def _check_calendar_exists(self):
        """Create the calendar if it doesn't exist."""
        if not os.path.isfile(self.CALENDAR):
            self._create_calendar()

    def _create_calendar(self):
        """Creates a default empty calendar file."""
        FILE_ATTRIBUTE_HIDDEN = 0x02
        empty_file = {}
        try:
            with open(self.CALENDAR, 'w') as file:
                json.dump(empty_file, file)
        except Exception as e:
            print('Unable to create calendar file: ', e)

    def amend_calendar(self, day, value):
        """Amends the day of existing calendar."""
        calendar = self.get_calendar()
        calendar[day] = value
        try:
            with open(self.CALENDAR, 'w') as file:
                json.dump(calendar, file)
        except Exception as e:
            print('Unable to amend calendar file: ', e)


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