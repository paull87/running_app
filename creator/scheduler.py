from settings.settings import Settings
from settings.converters import timestamp, convert_to_date, dec
import os
import subprocess
import datetime
import shutil
import uuid

#settings = Settings()
#workouts = settings.database.get_workouts()

class Scheduler():
    """Class for the workout plan scheduler."""
    def __init__(self, settings, plan, plan_name, race_date=None, start_date=None):
        self.settings = settings
        self.plan_name = plan_name
        self.plan = plan
        self.race_date = race_date
        self.start_date = start_date if start_date else datetime.datetime.now().replace(microsecond=0, second=0,
                                                                                        minute=0, hour=0)
        self.schedule_workouts = list()
        self.add_schedule_workouts()
        if self.schedule_workouts:
            self.save_schedule_workouts()

    def add_schedule_workouts(self):
        """Adds the workouts of the plan that are between the start and race dates."""
        workouts = self.settings.database.get_schedule_workouts(self.plan)
        if not self.race_date:
            self.race_date = set_race_dates(self.start_date, workouts)
        for workout in workouts:
            workout_date = self.race_date - datetime.timedelta(days=workout.DaysFromEnd)
            if workout_date < self.start_date:
                continue
            race_id = None if not workout.RaceDistance else self.add_schedule_races(workout.DistanceID, workout_date)
            self.schedule_workouts.append((workout.ScheduleID, workout.ScheduleWorkoutID, workout_date, race_id))

    def save_schedule_workouts(self):
        """Adds the plan workouts to the schedule."""
        schedule_id = int(self.schedule_workouts[0][0])
        self.settings.database.schedule_workouts([x[1:] for x in self.schedule_workouts], self.start_date,
                                                 self.race_date, schedule_id, self.plan_name, str(self.settings.vdot))

    def add_schedule_races(self, distance, race_date):
        race_id = self.settings.database.schedule_race(distance, race_date)
        return race_id if race_id > 0 else None


def set_race_dates(start_date, workouts):
    """Sets the race date when none is provided based on the start date."""
    all_days = [int(x.DaysFromEnd) for x in workouts if x.WorkoutWeekDay >= start_date.isoweekday()]
    plan_days_to_race = max(all_days)
    extra_days = 7 - (plan_days_to_race % 7)
    return start_date + datetime.timedelta(days=plan_days_to_race + (extra_days - start_date.isoweekday()))


if __name__ == '__main__':

    settings = Settings()
    Scheduler(settings, 'Half Marathon 47 Miles', 'Chistlehurst Half Marathon',
                  start_date=datetime.datetime(day=25, month=3, year=2019),
                  race_date=datetime.datetime(day=19, month=5, year=2019))

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


