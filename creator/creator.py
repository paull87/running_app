from creator.workout import Workout
from settings.settings import Settings
import os
import ast
import subprocess


def refresh_workouts(settings):
    """Refreshes the workouts according to the current vdot."""
    print(os.path.abspath(settings.WORKOUTS_PATH))
    for name, workout, filename, serial, _ in settings.get_workouts().itertuples():
        print(name, filename, serial)
        workout = Workout(name, settings.zones, ast.literal_eval(workout), settings.units, settings.max_hr, filename, serial)
        create_workout_file(workout, settings.workout_template)
        delete_fit_workout(filename)
        if filename != workout.timestamp or serial != workout.serial:
            settings.update_workout((workout.timestamp, workout.serial, name))
        print(workout.steps)
        create_fit_file(workout.timestamp)
        delete_csv_workout(workout.timestamp)


def delete_csv_workout(workout):
    """Removes the csv file for the workout once it is no longer needed."""
    csv_path = os.path.join(os.path.abspath(settings.WORKOUTS_PATH), str(workout) + '.csv')
    if os.path.isfile(csv_path):
        os.remove(csv_path)


def delete_fit_workout(workout):
    """Removes the FIT file for the workout once it is no longer needed."""
    fit_path = os.path.join(os.path.abspath(settings.FIT_PATH), str(workout) + '.FIT')
    if os.path.isfile(fit_path):
        os.remove(fit_path)


def create_fit_file(workout):
    """Creates the csv and fit file paths and calls the FitCSVTool.jar to convert the csv file."""
    csv_path = os.path.join(os.path.abspath(settings.WORKOUTS_PATH), str(workout) + '.csv')
    fit_path = os.path.join(os.path.abspath(settings.FIT_PATH), str(workout) + '.FIT')
    print(csv_path)
    run_fitcsvtool(csv_path, fit_path)


def run_fitcsvtool(csv_path, fit_path):
    """Calls the FitCSVTool.jar to convert the csv file to the fit file."""
    args = ['java', '-jar', 'FitCSVTool.jar', '-c', csv_path, fit_path]
    FNULL = open(os.devnull, 'w')
    subprocess.call(args, stdout=FNULL, stderr=subprocess.STDOUT)


def create_workout_file(workout, template):
    with open('{}{}.csv'.format(settings.WORKOUTS_PATH, workout.timestamp), 'w') as workout_file:
        workout_file.write(template.format(workout.serial, workout.timestamp, workout.name,
                                                         len(workout.steps)))
        for step in workout.steps:
            workout_file.write(str(step))


if __name__ == '__main__':
    settings = Settings()

    #VDOT_values = VDOT()
    #VDOT_values.calculate_vdot('HalfMarathon', '1:45:00')
    #paces = {k.split('-')[0].lower(): v for k, v in VDOT_values.training_paces.items() if settings.units in k.lower()}

    refresh_workouts(settings)

    ###test_workout = Workout('Test Easy Run', paces, run=[
    ###    ['easy', '', ['6', 'mile'], 1, 1],
    ###    ('easy', 'hr', ['10.5', 'mile'], 1, 0),
    ###    ('interval', 'pace', ['6', 'km'], 1, 1)
    ###])

    #create_workout_file(test_workout)



    # Interval file test
    ##test_interval_workout = Workout('Test Interval Time Run', paces, run=[
    ##    ('easy', 'hr', ['2.5', 'mile'], 1, 1),
    ##    {
    ##        'active': ('interval', 'pace', ['0.5', 'mile'], 0, 1),
    ##        'rest': ('easy', 'none', '00:04:00', 0, 0),
    ##        'repeat': 5
    ##    },
    ##    ('easy', 'hr', ['2.5', 'mile'], 1, 1)
    ##])

    # create_workout_file(test_interval_workout)

    # Interval file test
    #test_interval_interval_workout = Workout('Test Interval x2 Run', paces, run=[
    #    ('easy', 'hr', ['2.5', 'mile'], 1, 1),
    #    {
    #        'active': {
    #            'active': ('interval', 'pace', ['400', 'metre'], 0, 1),
    #            'rest': ('easy', 'none', ['0.25', 'mile'], 0, 0),
    #            'repeat': 3
    #        },
    #        'rest': ('easy', 'none', '00:04:00', 0, 0),
    #        'repeat': 2
    #    },
    #    ('easy', 'hr', ['2.5', 'mile'], 1, 1)
    #])

    #create_workout_file(test_interval_interval_workout)
