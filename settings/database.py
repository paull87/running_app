from settings import sql_queries
from settings.db_deployment import deploy_database
from collections import namedtuple
import os
import re
import sqlite3


class DB:
    """Class containing the database connection."""
    def __init__(self, db_path):
        self._db_path = db_path
        self.connection = self._connect_db()

    def _connect_db(self):
        """Checks if database exists and creates it if not."""
        if not os.path.isfile(self._db_path):
            deploy_database(self._db_path)
        try:
            return sqlite3.connect(self._db_path, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        except Exception as e:
            print('Unable to connect to database: ', e)

    def get_current_settings(self):
        """Returns the current settings."""
        return self.connection.cursor().execute(sql_queries.get_current_settings).fetchone()

    def get_hr_zones(self):
        """Returns the current hr zones for each training interval."""
        return named_tuple_result('HRZones', self.connection.execute(sql_queries.get_hr_zones))

    def get_vdot_paces(self):
        """Returns all of the vdot paces."""
        return named_tuple_result('VDOTPaces', self.connection.execute(sql_queries.vdot_paces))

    def get_vdot_race_times(self):
        """Returns all of the vdot race times."""
        return named_tuple_result('VDOTRaces', self.connection.execute(sql_queries.vdot_racetimes))

    def vdot_range(self, distance, time):
        """Returns the range that distance time falls between."""
        self.connection.executescript(sql_queries.vdot_range_population.format(distance, time))
        result = self.connection.cursor().execute(sql_queries.vdot_range).fetchone()
        self.connection.executescript(sql_queries.clear_table)
        self.connection.commit()
        return result

    def update_vdot(self, vdot_score):
        """Updates the history of the VDOT score and updates settings."""
        cursor = self.connection.cursor()
        cursor.execute(sql_queries.insert_vdot, (vdot_score,))
        self.connection.commit()
        self.update_settings('VDOTHistoryID', cursor.lastrowid)

    def update_settings(self, field, value):
        """Updates the given setting field and value."""
        cursor = self.connection.cursor()
        cursor.execute(sql_queries.update_settings.format(field), (value,))
        self.connection.commit()

    def update_race_pace(self, details):
        """Updates the race paces and times."""
        cursor = self.connection.cursor()
        cursor.executemany(sql_queries.update_race_times, details)
        self.connection.commit()

    def update_training_pace(self, details):
        """Updates the training paces."""
        cursor = self.connection.cursor()
        cursor.executemany(sql_queries.update_training_paces, details)
        self.connection.commit()

    def get_distances(self):
        """Returns all of the distances."""
        return named_tuple_result('Distance', self.connection.execute(sql_queries.get_distances))

    def get_race_paces(self):
        """Returns existing race paces."""
        return named_tuple_result('RacePace', self.connection.execute(sql_queries.get_race_paces))

    def get_training_paces(self):
        """Returns existing training paces."""
        return named_tuple_result('TrainingPace', self.connection.execute(sql_queries.get_training_paces))

    def get_targets(self, unit):
        """Returns existing target paces and hr zones."""
        return named_tuple_result('Targets', self.connection.execute(sql_queries.get_targets.format(unit)))

    def get_workouts(self):
        """Returns all workouts and their details."""
        return named_tuple_result('Workouts', self.connection.execute(sql_queries.get_workout_templates))

    def update_workout(self, workout):
        """Updates the given workout."""
        cursor = self.connection.cursor()
        cursor.execute(sql_queries.update_workout, workout)
        self.connection.commit()

    def get_schedules(self):
        return sorted([x[0] for x in self.connection.execute(sql_queries.get_schedules).fetchall()], key=natural_sort())

    def get_schedule_workouts(self, schedule):
        """Returns all workouts for a schedule."""
        return named_tuple_result('ScheduleWorkouts', self.connection.execute(sql_queries.get_schedule_workouts,
                                                                              (schedule,)))

    def schedule_workouts(self, workouts, start_date, end_date, schedule_id, plan_name, vdot):
        """Adds a new planned schedule record and the workouts associated with it."""
        cursor = self.connection.cursor()
        print((schedule_id, start_date, end_date, plan_name, vdot))
        cursor.execute(sql_queries.add_planned_schedule, (schedule_id, start_date, end_date, plan_name, vdot))
        planned_schedule_id = cursor.lastrowid
        cursor.executemany(sql_queries.add_schedule_plan, [x + (planned_schedule_id,) for x in workouts])
        self.connection.commit()

    def schedule_race(self, distance_id, race_date, race_name):
        """Adds a new race schedule record."""
        cursor = self.connection.cursor()
        if race_name:
            cursor.execute(sql_queries.add_schedule_race, (race_date, distance_id, race_name))
        else:
            cursor.execute(sql_queries.add_default_schedule_race, (race_date, distance_id, race_date))
        self.connection.commit()
        return cursor.lastrowid

    def get_calendar_range(self, date_from, date_to):
        """Returns the calendar items for a given date range."""
        return self.connection.cursor().execute(sql_queries.get_calendar_range, (date_from.date(), date_to.date())
                                                ).fetchall()

    def get_shoe_list(self):
        """Returns all available shoes."""
        return self.connection.cursor().execute(sql_queries.get_shoe_list).fetchall()

    def delete_workout_plan(self, plan_id):
        """Deletes the given plan ID."""
        self.connection.execute(sql_queries.delete_schedule_plan_workouts, (plan_id,))
        self.connection.execute(sql_queries.delete_schedule_plan, (plan_id,))
        self.connection.commit()

    def add_amend_shoe(self, shoe_details):
        """Adds the given shoe if it doesn't exist or updates it if it does."""
        cursor = self.connection.cursor()
        if shoe_details[-1] == 1:
            cursor.execute(sql_queries.reset_default_shoe)
        if shoe_details[0] is None:
            cursor.execute(sql_queries.add_shoe, shoe_details[1:])
        else:
            cursor.execute(sql_queries.amend_shoe, tuple(shoe_details[1:]) + (shoe_details[0],))
        shoe_id = cursor.lastrowid
        self.connection.commit()
        return shoe_id

    def add_diary_entry(self, diary_entry):
        """Adds or amends a diary entry."""
        cursor = self.connection.cursor()
        if diary_entry[0] is None:
            cursor.execute(sql_queries.add_diary_entry, diary_entry[1:])
        else:
            cursor.execute(sql_queries.edit_diary_entry, tuple(diary_entry[1:]) + (diary_entry[0],))
        diary_id = cursor.lastrowid
        self.connection.commit()
        return diary_id

    def get_run_types(self):
        return self.connection.cursor().execute(sql_queries.get_run_types).fetchall()

    def get_points(self, hr):
        """Returns the points for the given HR."""
        result = self.connection.cursor().execute(sql_queries.get_points, (str(hr),)).fetchone()
        return result[0] if result else 0.0


def named_tuple_result(name, results):
    """Creates a named tuple result set for the given results."""
    pre = 'x' if [x for x in results.description if x[0].isdigit()] else ''
    names = [pre + description[0] for description in results.description]
    nt = namedtuple(name, names)
    return tuple([nt(*x) for x in results.fetchall()])


def natural_sort():
    """Sorts the given list into a natural sort. i.e 1a, 2b, 15c, etc."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return alphanum_key
