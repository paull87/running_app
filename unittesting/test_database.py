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
                   152, None, None, 4, 3, None, None, 2.54, 2.54, "Test Description", 0]
    database.add_diary_entry(diary_entry)
    assert len(database.get_calendar_range(start_date, end_date)) == 1


def test_get_diary_entry(database):
    diary_entry = [None, start_date + datetime.timedelta(hours=7, minutes=45),
                   datetime.timedelta(hours=0, minutes=45, seconds=34).total_seconds(), 1, 6.2, 10, 7.5, 10.5, 600, 500,
                   152, None, None, 4, 3, None, None, 2.54, 2.54, "Test Description", 0]
    diary_id = database.add_diary_entry(diary_entry)
    diary_entry[0] = diary_id
    assert database.get_diary_entry(diary_id) == tuple(diary_entry)


def test_amend_diary_entry(database):
    diary_entry = [None, start_date + datetime.timedelta(hours=7, minutes=45),
                   datetime.timedelta(hours=0, minutes=45, seconds=34).total_seconds(), 1, 6.2, 10, 7.5, 10.5, 600, 500,
                   152, None, None, 4, 3, None, None, 2.54, 2.54, "Test Description", 0]
    diary_id = database.add_diary_entry(diary_entry)
    new_diary_entry = [diary_id, start_date + datetime.timedelta(hours=9, minutes=57),
                   datetime.timedelta(hours=0, minutes=34, seconds=1).total_seconds(), 3, 99, 11, 5.3, 8.7, 888, 444,
                   176, None, None, 1, 5, None, None, 7.54, 7.54, "Test Change Description", 0]
    database.add_diary_entry(new_diary_entry)
    assert database.get_diary_entry(diary_id) == tuple(new_diary_entry)


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
    assert database.get_shoe_list() == [(0, 'Unknown', 0)]


def test_add_shoe(database):
    assert database.add_amend_shoe((None, 'TestShoe', 'TestBrand', 'TestDes', datetime.datetime(2018, 11, 1), None, 0,
                                    0, 1)) == 1
    assert database.get_shoe_list() == [(1, 'TestShoe', 1), (0, 'Unknown', 0)]


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


def test_get_shoe_list_detail_single_shoe(database):
    database.add_amend_shoe((None, 'TestShoe', 'TestBrand', 'TestDes', datetime.datetime(2018, 11, 1), None, 0, 0, 1))
    assert database.get_shoe_list_detail() == [(1, 'TestShoe', 'TestBrand', datetime.datetime(2018, 11, 1), None,
                                               0, 0, 0, 0, 0, 1)]


def test_get_shoe_detail_fields(database):
    database.add_amend_shoe((None, 'TestShoe', 'TestBrand', 'TestDes', datetime.datetime(2018, 11, 1), None, 0, 0, 1))
    assert database.get_shoe_detail(1)._fields == ('ShoeID', 'ShoeName', 'Brand', 'Description', 'StartDate', 'DateRetired',
                                                  'PreviousMiles', 'PreviousKM', 'IsDefault')


def test_add_health_stats(database):
    health_stats = (start_date, 10, 5, 50)
    database.add_health_stats(health_stats)
    assert database.get_health_stats(start_date) == health_stats


def test_amend_health_stats(database):
    health_stats = (start_date, 10, 5, 50)
    database.add_health_stats(health_stats)
    assert database.get_health_stats(start_date) == health_stats
    new_health_stats = (start_date, 99, 88, 77)
    database.add_health_stats(new_health_stats)
    assert database.get_health_stats(start_date) == new_health_stats


def test_add_strava_laps(database):
    lap = (12345, 54321, start_date, 300, 3.1, 5, 10.5, 20.5, 100, 200, 150, 99.99, 77.77)
    database.add_strava_lap(lap)
    assert database.get_strava_laps(54321) == [lap, ]


def test_amend_strava_lap(database):
    lap = (12345, 54321, start_date, 300, 3.1, 5, 10.5, 20.5, 100, 200, 150, 99.99, 77.77)
    database.add_strava_lap(lap)
    assert database.get_strava_laps(54321) == [lap,]
    new_lap = (12345, 54321, start_date, 999, 6, 9.7, 5.5, 34.5, 699, 400, 150, 99.99, 67.77)
    database.add_strava_lap(new_lap)
    assert database.get_strava_laps(54321) == [new_lap, ]


def test_add_race(database):
    race = [None, 'Test Race Name', '10K']
    race_id = database.add_race(race)
    assert race_id == 11


def test_get_race_list(database):
    races = ((None, 'Test Race Name', '10K'), (None, 'Test Race Name2', 'HalfMarathon'))
    for race in races:
        database.add_race(race)
    assert database.get_race_list() == [x[1:] for x in races]


def test_amend_race(database):
    race = [None, 'Test Race Name', '10K']
    race_id = database.add_race(race)
    new_race = (race_id, 'Changed Name', '10Mile')
    database.add_race(new_race)
    assert database.get_race_list() == [new_race[1:]]


def test_add_race_detail(database):
    race = (None, 'Test Race Name', '10K')
    database.add_race(race)
    race_datail = (None, *race[1:], start_date, 420, None)
    race_detail_id = database.add_amend_race_detail(race_datail)
    assert race_detail_id == 1


def test_get_race_details(database):
    race = (None, 'Test Race Name', '10K')
    database.add_race(race)
    race_datail = (None, *race[1:], start_date, 420, None)
    race_detail_id = database.add_amend_race_detail(race_datail)
    race_datail = (race_detail_id,) + race_datail[1:]
    assert database.get_race_detail(race_detail_id) == race_datail


def test_amend_race_detail(database):
    race = (None, 'Test Race Name', '10K')
    database.add_race(race)
    race_datail = (None, *race[1:], start_date, 420, None)
    race_detail_id = database.add_amend_race_detail(race_datail)
    new_race_detail = (race_detail_id, *race[1:], start_date, 420, 430)
    database.add_amend_race_detail(new_race_detail)
    assert database.get_race_detail(race_detail_id) == new_race_detail


def test_get_week_summaries(database):
    diary_entries = [[None, start_date + datetime.timedelta(hours=7, minutes=45),
                   datetime.timedelta(hours=0, minutes=45, seconds=34).total_seconds(), 1, 6.2, 10, 7.5, 10.5, 600, 500,
                   152, None, None, 4, 3, None, None, 2.54, 2.54, "Test Description", 0],
                     [None, start_date + datetime.timedelta(hours=7, minutes=45) + datetime.timedelta(days=1),
                      datetime.timedelta(hours=0, minutes=45, seconds=34).total_seconds(), 1, 6.2, 10, 7.5, 10.5, 600,
                      500,
                      152, None, None, 4, 3, None, None, 2.54, 2.54, "Test Description", 0],
                     ]
    for entry in diary_entries:
        database.add_diary_entry(entry)
    summaries = database.get_week_summaries(start_date.month, start_date.year)
    assert summaries[0].Week == '2018-11-04'
    assert summaries[0].TotalTime == 5468
    assert summaries[0].TotalDistance == 12.4