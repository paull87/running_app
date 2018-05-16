import datetime
from settings.converters import convert_to_time, dec, time_to_string
from settings.database import DB
import pandas


class VDOT:
    """Contains the VDOT values for the race and training paces."""
    def __init__(self, db, current_vdot=None):
        self.VDOT_paces = db.get_vdot_paces()
        self.VDOT_racetimes = db.get_vdot_race_times()
        self.vdot_score = current_vdot
        self.training_paces = db.get_training_paces()
        self.race_times = db.get_race_paces()

    def __getitem__(self, item):
        return self.VDOT_paces[item]

    def __repr__(self):
        return repr(self.VDOT_paces)

    def calculate_vdot(self, distance, time):
        """Calculates the vdot for a person based on the finish time of the distance."""
        time_seconds = convert_to_time(time).total_seconds()
        vdot, max_time, min_time = db.vdot_range(distance, time_seconds)
        vdot_distance_diff = max_time - min_time
        finish_distance_diff = min_time - time_seconds
        if vdot_distance_diff == 0:
            self.vdot_score = int(vdot)
        else:
            self.vdot_score = int(vdot) + dec(finish_distance_diff / vdot_distance_diff, 2, 'ROUND_FLOOR')
        self._calculate_paces()

    def _calculate_paces(self):
        """Returns the training paces for the current vdot score."""
        if self.vdot_score == dec('0.00', 2):
            return
        vdot_diff = self._vdot_dec()
        self._calculate_training_paces(vdot_diff)
        self._calculate_race_times(vdot_diff)
        return None

    def _calculate_training_paces(self, vdot_diff):
        """Calculates the paces based on the vdot score."""
        data = list()
        headers = ['Distance', 'Mile', 'KM']
        vdot_score = int(self.vdot_score)
        vdot_df_km = self.VDOT_paces[(self.VDOT_paces.VDOT >= vdot_score)
                                         & (self.VDOT_paces.Unit == 'KM')].iloc[:2, :].copy().reset_index(drop=True)
        vdot_df_mile = self.VDOT_paces[(self.VDOT_paces.VDOT >= vdot_score)
                                           & (self.VDOT_paces.Unit == 'Mile')].iloc[:2, :].copy().reset_index(drop=True)
        for head in list(vdot_df_km):
            if head in ('VDOT', 'Unit'):
                continue
            pace_diff = vdot_df_mile.at[0, head] - vdot_df_mile.at[1, head]
            pace_add = int(dec(dec(pace_diff) * vdot_diff, 0))
            mile_pace = vdot_df_mile.at[0, head] - pace_add

            pace_diff = vdot_df_km.at[0, head] - vdot_df_km.at[1, head]
            pace_add = int(dec(dec(pace_diff) * vdot_diff, 0))
            km_pace = vdot_df_km.at[0, head] - pace_add
            data.append([head, mile_pace, km_pace])

        self.training_paces = pandas.DataFrame(data, columns=headers)
        self.training_paces.set_index('Distance', inplace=True)

    def _calculate_race_times(self, vdot_diff):
        """Calculates the race times based on the vdot score."""
        data = list()
        vdot_score = int(self.vdot_score)
        vdot_df = self.VDOT_racetimes[(self.VDOT_racetimes.VDOT >= vdot_score)].iloc[:2, :]
        for head in list(vdot_df):
            if head == 'VDOT':
                continue
            pace_diff = vdot_df.iloc[0][head] - vdot_df.iloc[1][head]
            pace_add = int(dec(dec(pace_diff) * vdot_diff, 0))
            data.append([head, vdot_df.iloc[0][head] - pace_add])

        race_times_paces = pandas.DataFrame(data, columns=['Distance', 'Time'])
        race_times_paces.set_index('Distance', inplace=True)
        self.race_times = pandas.concat([race_times_paces, self.training_paces], axis=1, join='inner')

    def _vdot_dec(self):
        """Returns the decimal of the current vdot score."""
        return self.vdot_score - dec(self.vdot_score, 0, 'ROUND_FLOOR')

    def save_vdot(self):
        """Saves the paces and vdot to the config for later use."""
        if self.vdot_score != settings.vdot:
            db.update_vdot(str(self.vdot_score))
            self.save_race_paces()
            self.save_training_paces()

    def save_training_paces(self):
        """Formats the times of the paces so they can be saved to the config."""
        fmt = '{hours:02d}:{minutes:02d}:{seconds:02d}'
        details = list()
        for distance, mile, km in self.training_paces.itertuples():
            details.append((mile, km, distance))
        db.update_training_pace(details)

    def save_race_paces(self):
        """Formats the times of the paces so they can be saved to the config."""
        details = list()
        for distance, time, mile, km in self.race_times.itertuples():
            details.append((time, mile, km, distance))
        db.update_race_pace(details)


if __name__ == '__main__':

    settings = Settings()
    db = settings.database

    import timeit
    VDOT_values = VDOT(db)

    print(VDOT_values.race_times)

    VDOT_values.calculate_vdot('HalfMarathon', '01:37:39')
    print('Current score:', VDOT_values.vdot_score)
    settings.update_settings('MaxHR', 189)
    settings.update_settings('Name', 'Paul Lucas')
    settings.update_settings('DateOfBirth', '26/06/1987')

    print('\nTraining')
    print(VDOT_values.training_paces)
    for k, m, km in VDOT_values.training_paces.itertuples():
        print(k.ljust(15), datetime.timedelta(seconds=m), datetime.timedelta(seconds=km))
    print('\nRaces')
    print(VDOT_values.race_times)

    #print(VDOT_values.VDOT_paces)



    print(str(VDOT_values.vdot_score))

    print(VDOT_values.vdot_score - dec(VDOT_values.vdot_score, 0, 'ROUND_FLOOR'))

    VDOT_values.save_vdot()
    settings.get_zones()

    print('SETTINGS')
    for r in db.connection.execute("SELECT * FROM Settings"):
        print(r)

    print('VDOT')
    for r in db.connection.execute("SELECT * FROM VDOTHistory"):
        print(r)

    print(settings.get_workouts().loc['Easy 10M'])

    #print(timeit.timeit(stmt="VDOT(db)", number=100, setup="from __main__ import VDOT"))

    print(settings.zones)

    #print('Settings')
    #for k, v in settings.get_workouts().items():
    #    current = (
    #        k[3:],
    #        str(v['workout']),
    #        v['filename'],
    #        v['serial'],
    #        0
    #    )
    #    print(current, ',')
