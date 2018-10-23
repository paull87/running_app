from settings.settings import Settings
from settings.converters import timestamp, convert_to_date, dec
import os
import subprocess
import datetime
import shutil
import uuid

settings = Settings()
workouts = settings.database.get_workouts()


def schedule_plan(settings, plan, plan_name, race_date=None, start_date=None):
    """Adds the given plan for the scheduled dates."""
    workouts = settings.get_plan_schedule(plan)
    if not start_date:
        start_date = datetime.datetime.now().replace(microsecond=0, second=0, minute=0, hour=0)
    if not race_date:
        race_date = set_race_dates(start_date, workouts)
    workout_atts = list()
    for workout in workouts:
        workout_date = race_date - datetime.timedelta(days=workout.DaysFromEnd)
        race_id = None if not workout.RaceDistance else add_schedule_races(workout.DistanceID, workout_date)
        workout_atts.append((workout.ScheduleID, workout.ScheduleWorkoutID, workout_date, race_id))
    add_schedule_workouts(tuple(x for x in workout_atts if x[-2] >= start_date),
                          start_date, race_date, plan_name, str(settings.vdot))


def set_race_dates(start_date, workouts):
    """Sets the race date when none is provided based on the start date."""
    all_days = [int(x.DaysFromEnd) for x in workouts if x.WorkoutWeekDay >= start_date.isoweekday()]
    plan_days_to_race = max(all_days)
    extra_days = 7 - (plan_days_to_race % 7)
    return start_date + datetime.timedelta(days=plan_days_to_race + (extra_days - start_date.isoweekday()))


def add_schedule_workouts(workouts, start_date, end_date, plan_name, vdot):
    """Adds the plan workouts to the schedule."""
    schedule_id = int(workouts[0][0])
    settings.database.schedule_workouts([x[1:] for x in workouts], start_date, end_date, schedule_id, plan_name, vdot)


def add_schedule_races(distance, race_date):
    race_id = settings.database.schedule_race(distance, race_date)
    return race_id if race_id > 0 else None


if __name__ == '__main__':

    settings = Settings()

    schedule_plan(settings, 'Half Marathon 47 Miles', 'Birmingham Half 2018',
                  start_date=datetime.datetime(day=1, month=7, year=2018),
                  race_date=datetime.datetime(day=14, month=10, year=2018))

    #create_schedule('Half Marathon 47 Miles', '04/03/2018')
    #plans = ['Half Marathon 47 Miles', 'Half Marathon 63 Miles', 'Marathon 55 Miles', '5K 40 Miles', '10K 42 Miles']
#
    #for plan_name in plans:
    #    plan = settings.get_plan_schedule(plan_name)
    #    weeks = 0
    #    for day, name in sorted([(int(k), v) for k, v in plan.items()], reverse=True):
    #        if weeks == 0:
    #            weeks = int(day / 7) + 1
    #        current = (
    #            plan_name,
    #            name[3:] if name.startswith('PP') else name,
    #            day,
    #            weeks - int(day / 7),
    #            7 - (day % 7),
    #            ' '.join(name.split()[:-1]) if name.endswith('Race') else None
#
#
    #        )
    #        print(current, ',')


