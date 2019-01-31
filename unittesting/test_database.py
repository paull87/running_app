import pytest
import os
import datetime
from settings.database import DB


@pytest.fixture()
def database(tmpdir):
    return DB(os.path.join(tmpdir, 'db.db'))


def test_get_hr_zones(database):
    zone_names = sorted([x.name for x in database.get_hr_zones()])
    assert zone_names == ['easy', 'interval', 'long', 'recovery', 'repetition', 'threshold']


def test_get_current_settings(database):
    settings = database.get_current_settings()
    assert settings == ('Enter Name', datetime.datetime(1900, 1, 1), 0, 200, 'mile')


def test_update_settings_name(database):
    database.update_settings('Name', 'New Name')
    settings = database.get_current_settings()
    assert settings[0] == 'New Name'


def test_update_settings_dateofbirth(database):
    database.update_settings('DateOfBirth', datetime.datetime(1980, 11, 23))
    settings = database.get_current_settings()
    assert settings[1] == datetime.datetime(1980, 11, 23)


def test_update_settings_maxhr(database):
    database.update_settings('MaxHR', 170)
    settings = database.get_current_settings()
    assert settings[3] == 170


def test_update_settings_units(database):
    database.update_settings('Units', 'km')
    settings = database.get_current_settings()
    assert settings[4] == 'km'


def test_get_vdot_paces_vdots(database):
    vdots = [(x.xVDOT, x.xUnit) for x in database.get_vdot_paces()]
    assert vdots == [(x, y) for y in ['KM', 'Mile'] for x in list(range(30, 86))]


def test_get_vdot_paces_fields(database):
    fields = database.get_vdot_paces()[0]._fields
    assert fields == ('xVDOT', 'xUnit', 'xRecovery', 'xEasy', 'xLong', 'xThreshold', 'xInterval', 'xRepetition',
                      'x1500', 'xMile', 'x2Mile', 'x3000', 'x5000', 'x10K', 'x15K', 'x10Mile', 'xHalfMarathon',
                      'xMarathon')


def test_get_vdot_race_times_vdots(database):
    vdots = [x.xVDOT for x in database.get_vdot_race_times()]
    assert vdots == list(range(30, 86))


def test_get_vdot_race_times_fields(database):
    fields = database.get_vdot_race_times()[0]._fields
    assert fields == ('xVDOT', 'x1500', 'xMile', 'x2Mile', 'x3000', 'x5000', 'x10K', 'x15K', 'x10Mile', 'xHalfMarathon',
                      'xMarathon')


def test_vdot_range_mid(database):
    time = datetime.timedelta(hours=3, minutes=30)
    vdots = database.vdot_range('marathon', time.total_seconds())
    assert vdots[0] == 45


def test_vdot_range_higher_boundary(database):
    time = datetime.timedelta(hours=2)
    vdots = database.vdot_range('marathon', time.total_seconds())
    assert vdots[0] == 85


def test_vdot_range_lower_boundary(database):
    time = datetime.timedelta(hours=20)
    vdots = database.vdot_range('marathon', time.total_seconds())
    assert vdots[0] == 30


def test_update_vdot(database):
    database.update_vdot(50)
    assert database.get_current_settings()[2] == 50


def test_get_race_paces(database):
    distance = sorted([x.Distance for x in database.get_race_paces()])
    assert distance == ['10K', '10Mile', '1500', '15K', '2Mile', '3000', '5000', 'HalfMarathon', 'Marathon', 'Mile']


def test_update_race_pace(database):
    database.update_race_pace(((1, 2, 3, '10K'),))
    distance = [x for x in database.get_race_paces() if x.Distance == '10K'][0]
    assert distance == ('10K', 1, 2, 3)


def test_get_distances(database):
    distance = sorted([x.Name for x in database.get_distances()])
    assert distance == ['10K', '10Mile', '1500', '15K', '2Mile', '3000', '5000', 'HalfMarathon', 'Marathon', 'Mile']


def test_get_training_paces(database):
    distance = sorted([x.Distance for x in database.get_training_paces()])
    assert distance == ['Easy', 'Interval', 'Long', 'Recovery', 'Repetition', 'Threshold']


def test_update_training_pace(database):
    database.update_training_pace(((1, 2, 'Interval'),))
    distance = [x for x in database.get_training_paces() if x.Distance == 'Interval'][0]
    assert distance == ('Interval', 1, 2)


def test_get_targets_km(database):
    targets = sorted([x.Name for x in database.get_targets('KM')])
    assert targets == ['10k', '10mile', '1500', '15k', '2mile', '3000', '5000', 'easy', 'halfmarathon', 'interval',
                       'long', 'marathon', 'mile', 'recovery', 'repetition', 'threshold']


def test_get_targets_mile(database):
    targets = sorted([x.Name for x in database.get_targets('Mile')])
    assert targets == ['10k', '10mile', '1500', '15k', '2mile', '3000', '5000', 'easy', 'halfmarathon', 'interval',
                       'long', 'marathon', 'mile', 'recovery', 'repetition', 'threshold']


def test_get_workouts_fields(database):
    fields = database.get_workouts()[0]._fields
    assert fields == ('Name', 'WorkoutJSON', 'FileName', 'SerialNumber', 'IsCustom')


def test_update_workout(database):
    database.update_workout(('Updated File', 'Updated Serial', 'Long 20M'))
    workout = [x for x in database.get_workouts() if x.Name == 'Long 20M'][0]
    assert workout.FileName == 'Updated File'
    assert workout.SerialNumber == 'Updated Serial'


def test_schedule_race(database):
    database.get_distances()
    assert database.schedule_race(1, datetime.datetime(2018, 10, 14), 'Unknown 1500') == 1


def test_get_schedules(database):
    assert database.get_schedules() == ["5K 40 Miles", "10K 42 Miles", "Half Marathon 47 Miles",
                                        "Half Marathon 63 Miles", "Marathon 55 Miles"]


def test_get_schedule_workouts_fields(database):
    fields = database.get_schedule_workouts("10K 42 Miles")[0]._fields
    assert fields == ('ScheduleName', 'ScheduleID', 'ScheduleWorkoutID', 'WorkoutName', 'WorkoutID', 'DaysFromEnd',
                      'WorkoutWeek', 'WorkoutWeekDay', 'DistanceID', 'RaceDistance')


start_date = datetime.datetime(2018, 11, 2)
end_date = datetime.datetime(2018, 11, 4)


def schedule_workouts(database):
    workouts = [(x.ScheduleWorkoutID, start_date + datetime.timedelta(days=y), None)
                for y, x in enumerate(database.get_schedule_workouts("10K 42 Miles")[:2])]
    database.schedule_workouts(workouts, start_date, end_date, 1, '10K 42 Miles', 35)


def test_schedule_workouts(database):
    schedule_workouts(database)
    assert len(database.get_calendar_range(start_date, end_date)) == 2


def test_delete_plan(database):
    schedule_workouts(database)
    assert len(database.get_calendar_range(start_date, end_date)) == 2
    database.delete_workout_plan(1)
    assert len(database.get_calendar_range(start_date, end_date)) == 0


def test_add_diary_entry(database):
    diary_entry = [None, start_date + datetime.timedelta(hours=7, minutes=45),
                   datetime.timedelta(hours=0, minutes=45, seconds=34).total_seconds(), 1, 6.2, 10, 7.5, 10.5, 600, 500,
                   152, None, None, 4, 3, None, None, 2.54, 2.54, 0]
    database.add_diary_entry(diary_entry)
    assert len(database.get_calendar_range(start_date, end_date)) == 1


def test_get_run_types(database):
    run_types = [x[1] for x in database.get_run_types()]
    assert run_types == ["Easy", "Fartlek", "Interval", "Long", "Parkrun", "Race", "Regular", "Steady", "Tempo",
                         "Threshold"]


def test_get_points_low(database):
    assert database.get_points(10) == 0.1


def test_get_points_high(database):
    assert database.get_points(100) == 1


def test_get_points_mid(database):
    assert database.get_points(87) == 0.517


def test_get_shoe_list(database):
    print(database.get_shoe_list_detail())
    assert database.get_shoe_list() == [(0, 'Unknown', 0)]


def test_add_shoe(database):
    assert database.add_amend_shoe((None, 'TestShoe', 'TestBrand', 'TestDes', datetime.datetime(2018, 11, 1), None, 0,
                                    0, 1)) == 1
    assert database.get_shoe_list() == [(0, 'Unknown', 0), (1, 'TestShoe', 1)]


def test_amend_shoe(database):
    database.add_amend_shoe((None, 'TestShoe', 'TestBrand', 'TestDes', datetime.datetime(2018, 11, 1), None, 0, 0, 1))
    database.add_amend_shoe((1, 'TestShoeChanged', 'TestBrand', 'TestDes', datetime.datetime(2018, 11, 1), None, 0, 0,
                             0))
    assert database.get_shoe_list() == [(0, 'Unknown', 0), (1, 'TestShoeChanged', 0)]


def test_get_scheduled_workout_details(database):
    schedule_workouts(database)
    fields = database.get_scheduled_workout_details(datetime.datetime(2018, 1, 1))[0]._fields
    assert fields == ('Name', 'WorkoutJSON', 'FileName', 'SerialNumber', 'ScheduleDate')


def test_get_shoe_list_detail_no_shoes(database):
    assert database.get_shoe_list_detail() == list()


def test_get_shoe_list_detail_no_shoes(database):
    database.add_amend_shoe((None, 'TestShoe', 'TestBrand', 'TestDes', datetime.datetime(2018, 11, 1), None, 0, 0, 1))
    assert database.get_shoe_list_detail() == [(1, 'TestShoe', 'TestBrand', datetime.datetime(2018, 11, 1), None,
                                               0, 0, 0, 0, 0, 1)]