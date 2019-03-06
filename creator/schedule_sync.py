from settings.settings import Settings
from settings.converters import timestamp, convert_to_date, dec
import os
import subprocess
import datetime
import shutil
import uuid
import ast
from creator.workout import Workout

# TODO: move create_schedule to its own script and treat as "export scheduled workouts".


class WorkoutSync:
    """Creates the workouts files to sync with Garmin device."""
    jar_file = os.path.join(os.path.abspath('..'), 'FitCSVTool.jar')

    def __init__(self, settings, from_date=None):
        self.settings = settings
        self.from_date = from_date if from_date else datetime.datetime.now().replace(microsecond=0, second=0, minute=0,
                                                                                     hour=0)

    def get_scheduled_workouts(self):
        """Returns the workouts to be synced."""
        return self.settings.database.get_scheduled_workout_details(self.from_date)

    def create_workout_file(self, workout, template):
        with open(os.path.join(self.settings.WORKOUTS_PATH, '{}.csv'.format(workout.timestamp)), 'w') as workout_file:
            workout_file.write(template.format(workout.serial, workout.timestamp, workout.name,
                                               len(workout.steps)))
            for step in workout.steps:
                workout_file.write(str(step))

    def create_workout(self, scheduled_workout):
        """Creates the workouts files to be synced."""
        workout = Workout(scheduled_workout.Name, self.settings.zones,
                          ast.literal_eval(scheduled_workout.WorkoutJSON), self.settings.units,
                          self.settings.max_hr)
        self.create_workout_file(workout, self.settings.workout_template)
        return workout

    def clear_files(self, csv_files=0, fit_files=0):
        """Clears the files for the extensions that equal 1."""
        extensions = list()
        if csv_files == 1:
            extensions.append('.csv')
        if fit_files == 1:
            extensions.append('.FIT')
        for file in [x for x in os.listdir(self.settings.WORKOUTS_PATH) if os.path.splitext(x)[1] in extensions]:
            os.remove(os.path.join(self.settings.WORKOUTS_PATH, file))

    def run_fitcsvtool(self, csv_path, fit_path):
        """Calls the FitCSVTool.jar to convert the csv file to the fit file."""
        args = ['java', '-jar', self.jar_file, '-c', csv_path, fit_path]
        FNULL = open(os.devnull, 'w')
        subprocess.call(args, stdout=FNULL, stderr=subprocess.STDOUT)

    def create_fit_file(self, workout):
        """Creates the csv and fit file paths and calls the FitCSVTool.jar to convert the csv file."""
        csv_path = os.path.join(os.path.abspath(self.settings.WORKOUTS_PATH), str(workout) + '.csv')
        fit_name = workout if workout !=  'SCHEDULE' else uuid.uuid4()
        fit_path = os.path.join(os.path.abspath(self.settings.WORKOUTS_PATH), str(fit_name) + '.FIT')
        self.run_fitcsvtool(csv_path, fit_path)

    def create_schedule_file(self):
        """Creates the schedule csv container."""
        return open(os.path.join(self.settings.WORKOUTS_PATH, 'SCHEDULE.csv'), 'w')

    def create_schedule(self):
        """Creates the schedule fit files for the next 30 distinct workouts."""
        self.clear_files(csv_files=1, fit_files=1)
        files = set()
        with self.create_schedule_file() as schedule_file:
            schedule_file.write(self.settings.schedule_template.format(timestamp()))
            for scheduled_workout in self.get_scheduled_workouts():
                if len(files) == 30:
                    break
                workout = self.create_workout(scheduled_workout)
                self.create_fit_file(workout.timestamp)
                schedule_file.write(schedule_step(workout.serial, workout.timestamp,
                                                  timestamp(scheduled_workout.ScheduleDate)))
                files.add(workout.timestamp)
        self.create_fit_file('SCHEDULE')
        self.clear_files(csv_files=1)


def schedule_step(serial, workout, schedule_date):
    """Creates the line for that workout in the schedule."""
    # schedule = 'Data,2,schedule,serial_number,"{}",,time_created,"{}",,scheduled_time,"{}",,manufacturer,"1",,' \
    # 'garmin_product,"65534",,completed,"0",,type,"0",,,,,\n'
    schedule = 'Data,0,schedule,manufacturer,"1",,garmin_product,"65534",,serial_number,"{}",,' \
               'time_created,"{}",,type,"0",,scheduled_time,"{}",,completed,"0",,\n'
    return schedule.format(serial, workout, schedule_date)


if __name__ == '__main__':

    settings = Settings()

    sync = WorkoutSync(settings)
    sync.create_schedule()