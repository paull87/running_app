from template.template import get_schedule_template
from settings.settings import Settings
from settings.converters import timestamp, convert_to_date, dec
import os
import subprocess
import datetime
import shutil
import uuid

settings = Settings()
workouts = settings.get_templates()
calendar = settings.get_calendar()


def find_workout(workout_name):
    """Returns the current filename of the given workout."""
    try:
        filename = workouts[workout_name]['filename']
        serial = workouts[workout_name]['serial']
        if filename == '':
            raise ValueError('File has not been created for workout. Make sure you fill in VDOT.')
        else:
            return filename, serial
    except (KeyError, TypeError):
        return None, None


def run_fitcsvtool(path=os.path.abspath(settings.SCHEDULE_PLANS)):
    """Calls the FitCSVTool.jar to convert the csv file to the fit file."""
    new_name = str(uuid.uuid4()) + '.FIT'
    csv_path = os.path.join(path, 'SCHEDULE.csv')
    fit_path = os.path.join(path, new_name)
    args = ['java', '-jar', 'FitCSVTool.jar', '-c', csv_path, fit_path]
    fnull = open(os.devnull, 'w')
    subprocess.call(args, stdout=fnull, stderr=subprocess.STDOUT)


def create_schedule_diary_line(weeks, day, workout_date, name):
    """Creates a line for the schedule diary."""
    fmt = '{},{},{},{},{}\n'
    workout_week = weeks - int(day / 7)
    diary_fmt = 'W{:02}D{:02}'.format(workout_week, workout_date.weekday() + 1)
    return fmt.format(diary_fmt, workout_date.strftime("%A"), day, workout_date.strftime('%d/%m/%Y'), name)


def create_schedule_diary(entries):
    """Creates a schedule"""
    header = 'Schedule,Day,Days From Race,Date,Workout\n'
    with open(os.path.join(os.path.abspath(settings.SCHEDULE_PLANS), 'schedule_plan.csv'), 'w') as schedule_file:
        schedule_file.write(header)
        schedule_file.writelines(entries)


def create_single_schedule_file(schedule, race_date):
    """Creates the csv file for the schedule and collects the relevant fit files."""
    weeks = 0
    clear_schedule()
    schedule_diary = []
    total_weeks = max([dec(int(d) / 7, 0, 'ROUND_CEILING') for d in schedule.keys()])
    with open(os.path.join(settings.SCHEDULE_PLANS, 'SCHEDULE.csv'), 'w') as schedule_file:
        schedule_file.write(get_schedule_template().format(timestamp()))
        for day, name in sorted([(int(k), v) for k, v in schedule.items()], reverse=True):
            filename, serial = find_workout(name)
            workout_day = race_date - datetime.timedelta(days=day)
            schedule_diary.append(create_schedule_diary_line(total_weeks, day, workout_day, name))
            #if workout_day < datetime.datetime.utcnow():
            #    continue
            if filename:
                schedule_file.write(schedule_step(serial, filename, timestamp(workout_day)))
                move_workout(str(filename))
            if weeks != int(day / 7):
                weeks = int(day / 7)
                print('{} Weeks to Race'.format(weeks))
            fmt = 'W{:02}D{:02}'.format(total_weeks - weeks, workout_day.weekday() + 1)
            print('\t{} {:10} {} - {} : {}'.format(fmt, workout_day.strftime("%A"), day, workout_day, name))
    #print(schedule_diary)
    create_schedule_diary(schedule_diary)
    run_fitcsvtool()


def create_multi_schedule_file(schedule, race_date):
    """Creates the csv file for the schedule and collects the relevant fit files."""
    weeks = 0
    clear_schedule()
    schedule_diary = []
    current_workouts = []
    schedule_directory = ''
    schedule_file = open(os.devnull, 'w')
    i = 0
    total_weeks = max([dec(int(d) / 7, 0, 'ROUND_CEILING') for d in schedule.keys()])
    for day, name in sorted([(int(k), v) for k, v in schedule.items()], reverse=True):
        filename, serial = find_workout(name)
        workout_day = race_date - datetime.timedelta(days=day)
        schedule_diary.append(create_schedule_diary_line(total_weeks, day, workout_day, name))
        if workout_day < datetime.datetime.utcnow() - datetime.timedelta(4):
            continue
        # Create a new schedule when the limit of 30 workouts is reached.
        if (i % 29 == 0 or i == 0) and (filename or filename in current_workouts):
            if i > 0:
                current_workouts = []
                schedule_file.close()
                run_fitcsvtool(schedule_directory)
            schedule_directory = create_directory(workout_day.strftime('%Y%m%d'))
            schedule_file = create_file(schedule_directory)
            schedule_file.write(get_schedule_template().format(timestamp()))
            print(schedule_directory)
        if filename:
            schedule_file.write(schedule_step(serial, filename, timestamp(workout_day)))
            if filename not in current_workouts:
                move_workout(schedule_directory, str(filename))
                current_workouts.append(filename)
                i += 1
        if weeks != int(day / 7):
            weeks = int(day / 7)
            print('{} Weeks to Race'.format(weeks))
        schedule_day = 'W{:02}D{}'.format(total_weeks - weeks, workout_day.weekday() + 1)

        print(i, '\t{} {:10} {} - {} : {}'.format(schedule_day, workout_day.strftime("%A"), day, workout_day, name))
        add_calendar_entry(workout_day.strftime("%Y%m%d"), schedule_day + ' ' + name)
    schedule_file.close()
    run_fitcsvtool(schedule_directory)
    create_schedule_diary(schedule_diary)


def create_directory(folder):
    """Creates a new directory to hold section of schedule."""
    directory = os.path.join(os.path.abspath(settings.SCHEDULE_PLANS), folder)
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory


def create_file(folder):
    """Creates a new directory to hold section of schedule."""
    file = open(os.path.join(folder, 'SCHEDULE.csv'), 'w')
    return file


def add_calendar_entry(day, workout):
    """Adds the scheduled workout to the calendar."""
    calendar.setdefault(day, list())
    calendar[day].append(workout)
    settings.amend_calendar(day, calendar[day])


def move_workout(path, name):
    """Copies the workout file to the schedule."""
    new_name = 'workout_' + str(uuid.uuid4())
    if not os.path.exists(os.path.join(os.path.abspath(settings.SCHEDULE_PLANS), name + '.csv')):
        shutil.copyfile(
            os.path.join(os.path.abspath(settings.FIT_PATH), name + '.FIT'),
            os.path.join(path, new_name + '.FIT')
        )


def schedule_step(serial, workout, schedule_date):
    """Creates the line for that workout in the schedule."""
    # schedule = 'Data,2,schedule,serial_number,"{}",,time_created,"{}",,scheduled_time,"{}",,manufacturer,"1",,' \
    # 'garmin_product,"65534",,completed,"0",,type,"0",,,,,\n'
    schedule = 'Data,0,schedule,manufacturer,"1",,garmin_product,"65534",,serial_number,"{}",,' \
               'time_created,"{}",,type,"0",,scheduled_time,"{}",,completed,"0",,\n'
    return schedule.format(serial, workout, schedule_date)


def create_schedule(training_plan, end_date):
    """Creates the schedule working back from the given race date."""
    race_date = convert_to_date(end_date)
    plan = settings.get_plan_schedule(training_plan)
    #create_single_schedule_file(plan, race_date)
    create_multi_schedule_file(plan, race_date)


def clear_schedule(path=settings.SCHEDULE_PLANS):
    """Clears any existing schedules."""
    for file_name in os.listdir(path):
        file = os.path.join(path, file_name)
        if os.path.isfile(file):
            os.remove(file)
        else:
            clear_schedule(file)
    if path != settings.SCHEDULE_PLANS:
        os.rmdir(path)

if __name__ == '__main__':

    create_schedule('Half Marathon 47 Miles', '04/03/2018')
