import pytest
import os
import datetime
from collections import namedtuple
from creator import scheduler
from settings.settings import Settings


test_workout = namedtuple('Tests', 'WorkoutWeekDay DaysFromEnd')
start_date = datetime.datetime(2018, 8, 8)  # 3rd day of week
workouts = (test_workout(2, 10), test_workout(3, 9))

@pytest.fixture()
def settings(tmpdir):
    return Settings(os.path.join(tmpdir, 'db.db'))



def test_set_race_dates():
    assert scheduler.set_race_dates(start_date, workouts) == datetime.datetime(2018, 8, 19)


def test_schedule_plan_start_end_dates():
    scheduler.schedule_plan(settings, 'Half Marathon 47 Miles', 'Birmingham Half 2018',
                  start_date=datetime.datetime(day=1, month=7, year=2018),
                  race_date=datetime.datetime(day=14, month=10, year=2018))
