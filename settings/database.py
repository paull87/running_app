import sqlite3
from settings import sql_queries
import pandas


class DB:
    """Class containing the database connection."""
    def __init__(self, connection):
        self.connection = connection

    def get_current_settings(self):
        """Returns the current settings."""
        return self.connection.cursor().execute(sql_queries.get_current_settings).fetchone()

    def get_hr_zones(self):
        """Returns the current hr zones for each training interval."""
        return pandas.read_sql(sql_queries.get_hr_zones, self.connection)

    def get_vdot_paces(self):
        """Returns all of the vdot paces."""
        return pandas.read_sql(sql_queries.vdot_paces, self.connection)

    def get_vdot_race_times(self):
        """Returns all of the vdot race times."""
        return pandas.read_sql(sql_queries.vdot_racetimes, self.connection)

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
        """Returns all fo the distances."""
        return pandas.read_sql(sql_queries.get_distances, self.connection)

    def get_race_paces(self):
        """Returns existing race paces."""
        return pandas.read_sql(sql_queries.get_race_paces, self.connection, index_col="Distance")

    def get_training_paces(self):
        """Returns existing training paces."""
        return pandas.read_sql(sql_queries.get_training_paces, self.connection, index_col="Distance")

    def get_targets(self, unit):
        """Returns existing target paces and hr zones."""
        return pandas.read_sql(sql_queries.get_targets.format(unit), self.connection, index_col="Name")

    def get_workouts(self):
        """Returns all workouts and their details."""
        return pandas.read_sql(sql_queries.get_workout_templates, self.connection, index_col="Name")

    def update_workout(self, workout):
        """Updates the given workout."""
        cursor = self.connection.cursor()
        cursor.execute(sql_queries.update_workout, workout)
        self.connection.commit()

    def get_schedule_workouts(self, schedule):
        """Returns all workouts for a schedule."""
        return pandas.read_sql(sql_queries.get_schedule_workouts, self.connection, params=(schedule,))

    def schedule_workouts(self, workouts, start_date, end_date, schedule_id):
        """Adds a new planned schedule record and the workouts associated with it."""
        cursor = self.connection.cursor()
        cursor.execute(sql_queries.add_planned_schedule, (schedule_id, start_date, end_date))
        workouts['PlannedScheduleID'] = cursor.lastrowid
        cursor.executemany(sql_queries.add_schedule_plan, workouts.values.tolist())
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
        return self.connection.cursor().execute(sql_queries.get_calendar_range, (date_from.date(), date_to.date())).fetchall()

    def get_shoe_list(self):
        """Returns all available shoes."""
        return self.connection.cursor().execute(sql_queries.get_shoe_list)

    # TODO: Add logic to add or amend shoes
    def add_amend_shoe(self, shoe_details):
        """Adds the given shoe if it doesn't exist or updates it if it does."""
        pass

    # TODO: Add logic to add new diary entries
    def add_diary_entry(self):
        """Adds a new diary entry."""
        pass

