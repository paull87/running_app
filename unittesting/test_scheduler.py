import pytest
import datetime
from creator.scheduler import Scheduler
from settings.settings import Settings
from VDOT.VDOT import VDOT

start_date = datetime.datetime(day=5, month=7, year=2018)
race_date = datetime.datetime(day=23, month=9, year=2018)


@pytest.fixture()
def settings(tmpdir):
    settings = Settings(tmpdir)
    vdot = VDOT(settings.database, settings.vdot)
    vdot.calculate_vdot('HalfMarathon', '01:36:40')
    vdot.save_vdot()
    settings.get_settings()
    return settings


def test_set_race_dates(settings):
    scheduler = Scheduler(settings, 'Half Marathon 47 Miles', 'Test Schedule', start_date=start_date)
    assert scheduler.race_date == race_date


def test_set_start_date(settings):
    current_date = datetime.datetime.now().replace(microsecond=0, second=0, minute=0, hour=0)
    scheduler = Scheduler(settings, 'Half Marathon 47 Miles', 'Test Schedule', race_date=race_date)
    assert scheduler.start_date == current_date


def test_short_schedule(settings):
    short_start_date = start_date + datetime.timedelta(weeks=9)
    scheduler = Scheduler(settings, 'Half Marathon 47 Miles', 'Test Schedule', race_date, short_start_date)
    assert scheduler.schedule_workouts[0][2] >= short_start_date


def test_add_schedule_races(settings):
    Scheduler(settings, 'Half Marathon 47 Miles', 'Test Schedule', race_date, start_date)
    races = [x for x in settings.database.get_calendar_range(start_date, race_date + datetime.timedelta(days=1))
             if x[0] == 'Race']
    assert len(races) > 0


def test_save_schedule_workouts(settings):
    Scheduler(settings, 'Half Marathon 47 Miles', 'Test Schedule', race_date, start_date)
    workouts = [x for x in settings.database.get_calendar_range(start_date, race_date + datetime.timedelta(days=1))
                if x[0] == 'Workout']
    assert len(workouts) > 0
