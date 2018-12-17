import pytest
import os
import datetime
from creator.scheduler import Scheduler
from creator.schedule_sync import WorkoutSync
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
    settings.get_zones()
    Scheduler(settings, 'Half Marathon 47 Miles', 'Test Schedule', race_date, start_date)
    return settings


@pytest.fixture()
def temp_workout_sync(settings):
    workout_sync = WorkoutSync(settings, start_date)
    workout_sync.create_workout(workout_sync.get_scheduled_workouts()[0])
    return workout_sync


def test_schedule_sync_date(settings):
    workout_sync = WorkoutSync(settings, start_date)
    assert workout_sync.from_date == start_date


def test_schedule_sync_default_date(settings):
    workout_sync = WorkoutSync(settings)
    assert workout_sync.from_date == datetime.datetime.now().replace(microsecond=0, second=0, minute=0, hour=0)


def test_get_scheduled_workouts(temp_workout_sync):
    assert isinstance(temp_workout_sync.get_scheduled_workouts(), tuple)
    assert len(temp_workout_sync.get_scheduled_workouts()) > 0


def test_create_workout_csv(temp_workout_sync, settings):
    assert len([x for x in os.listdir(settings.WORKOUTS_PATH) if os.path.splitext(x)[1] == '.csv']) > 0


def test_clear_files_csv(temp_workout_sync, settings):
    temp_workout_sync.clear_files(csv_files=1)
    assert len([x for x in os.listdir(settings.WORKOUTS_PATH) if os.path.splitext(x)[1] == '.csv']) == 0


def test_create_fit_file(temp_workout_sync, settings):
    filename = temp_workout_sync.get_scheduled_workouts()[0].FileName
    temp_workout_sync.create_fit_file(filename)
    assert os.path.isfile(os.path.join(settings.WORKOUTS_PATH, filename + '.FIT'))


def test_clear_files_fit(temp_workout_sync, settings):
    test_create_fit_file(temp_workout_sync, settings)
    assert len([x for x in os.listdir(settings.WORKOUTS_PATH) if os.path.splitext(x)[1] == '.FIT']) > 0
    temp_workout_sync.clear_files(fit_files=1)
    assert len([x for x in os.listdir(settings.WORKOUTS_PATH) if os.path.splitext(x)[1] == '.FIT']) == 0


def test_create_schedule_file(temp_workout_sync, settings):
    temp_workout_sync.create_schedule_file()
    assert os.path.isfile(os.path.join(settings.WORKOUTS_PATH, 'SCHEDULE.csv'))


def test_create_schedule(temp_workout_sync, settings):
    temp_workout_sync.create_schedule()
    assert 0 < len([x for x in os.listdir(settings.WORKOUTS_PATH) if os.path.splitext(x)[1] == '.FIT']) <= 31
    assert len([x for x in os.listdir(settings.WORKOUTS_PATH) if os.path.splitext(x)[1] == '.csv']) == 0

# Test create schedule
# Test only return 30 workout files.
