import pytest
import os
import datetime
from decimal import Decimal
from creator.scheduler import Scheduler
from settings.settings import Settings


start_date = datetime.datetime(day=5, month=7, year=2018)
race_date = datetime.datetime(day=23, month=9, year=2018)


@pytest.fixture()
def settings(tmpdir):
    settings = Settings(tmpdir)
    return settings


def test_workouts_path(settings, tmpdir):
    assert settings.WORKOUTS_PATH == os.path.join(tmpdir, 'Workouts')


def test_fit_path(settings, tmpdir):
    assert settings.FIT_PATH == os.path.join(tmpdir, 'Workouts', 'FIT')


def test_database_path(settings, tmpdir):
    assert settings.DATABASE_PATH == os.path.join(tmpdir, 'FitnessDB.db')


def test_get_settings(settings):
    assert settings.vdot == Decimal(0)
    assert settings.username == 'Enter Name'
    assert settings.max_hr == 200
    assert settings.dob == datetime.datetime(1900, 1, 1)
    assert settings.units == 'mile'


def test_get_zones(settings):
    assert settings.zones == settings.database.get_targets('mile')


def test_update_settings(settings):
    settings.update_settings('Name', 'TestName')
    assert settings.username == 'TestName'


def test_get_calendar(settings):
    Scheduler(settings, 'Half Marathon 47 Miles', 'Test Schedule', race_date, start_date)
    calendar_items = [x[2] for x in settings.get_calendar(8, 2018)]
    date_from = datetime.datetime(day=1, month=8, year=2018)
    date_to = datetime.datetime(day=1, month=9, year=2018)
    assert min(calendar_items) >= date_from
    assert max(calendar_items) < date_to


def test_calculate_intensity_points(settings):
    assert settings.calculate_intensity_points(170, datetime.timedelta(minutes=2)) == Decimal('0.467') * 2
