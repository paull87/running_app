import datetime
from settings.converters import convert_to_time, dec
from collections import namedtuple


training_pace = namedtuple('TrainingPaces', ['Distance', 'Mile', 'KM'])
race_pace = namedtuple('RacePaces', ['Distance', 'Time'])
race_time = namedtuple('RaceTimes', ['Distance', 'Time', 'Mile', 'KM'])


class VDOT:
    """Contains the VDOT values for the race and training paces."""
    def __init__(self, db, current_vdot=None):
        self.db = db
        self.VDOT_paces = self.db.get_vdot_paces()
        self.VDOT_racetimes = self.db.get_vdot_race_times()
        self.current_vdot = current_vdot
        self.vdot_score = current_vdot
        self.training_paces = self.db.get_training_paces()
        self.race_times = self.db.get_race_paces()

    def __getitem__(self, item):
        return self.VDOT_paces[item]

    def __repr__(self):
        return 'VDOT({}, {})'.format(self.db, self.current_vdot)

    def calculate_vdot(self, distance, time):
        """Calculates the vdot for a person based on the finish time of the distance."""
        time_seconds = convert_to_time(time).total_seconds()
        vdot, max_time, min_time = self.db.vdot_range(distance, time_seconds)
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
        km_range, mile_range = self._pace_ranges()
        ranges = len(km_range)
        for key in mile_range[0]._fields:
            if key in ('xVDOT', 'xUnit'):
                continue
            if ranges == 1:
                km_pace = getattr(km_range[0], key)
                mile_pace = getattr(km_range[0], key)
            else:
                pace_diff = getattr(mile_range[0], key) - getattr(mile_range[0], key)
                pace_add = int(dec(dec(pace_diff) * vdot_diff, 0))
                mile_pace = getattr(mile_range[0], key) - pace_add

                pace_diff = getattr(km_range[0], key) - getattr(km_range[0], key)
                pace_add = int(dec(dec(pace_diff) * vdot_diff, 0))
                km_pace = getattr(km_range[0], key) - pace_add
            data.append(training_pace(key[1:], mile_pace, km_pace))
        self.training_paces = data

    def _calculate_race_times(self, vdot_diff):
        """Calculates the race times based on the vdot score."""
        data = list()
        vdot_score = int(self.vdot_score)
        #vdot_df = self.VDOT_racetimes[(self.VDOT_racetimes.VDOT >= vdot_score)].iloc[:2, :]
        vdot_df = [x for x in self.VDOT_racetimes if x.xVDOT >= vdot_score]
        for head in vdot_df[0]._fields:
            if head == 'xVDOT':
                continue
            if len(vdot_df) == 1:
                pace_add = 0
            else:
                pace_diff = getattr(vdot_df[0], head) - getattr(vdot_df[1], head)
                pace_add = int(dec(dec(pace_diff) * vdot_diff, 0))
            data.append(race_pace(head[1:], getattr(vdot_df[0], head) - pace_add))
        race_paces = [x for x in self.training_paces if x.Distance in [y.Distance for y in data]]
        self.race_times = [race_time(x[0].Distance, x[0].Time, x[1].Mile, x[1].KM) for x in
            tuple(zip(sorted(data, key=lambda x: x.Distance), sorted(race_paces, key=lambda x: x.Distance)))]

    def _vdot_dec(self):
        """Returns the decimal of the current vdot score."""
        return self.vdot_score - dec(self.vdot_score, 0, 'ROUND_FLOOR')

    def save_vdot(self):
        """Saves the paces and vdot to the config for later use."""
        self.save_race_paces()
        self.save_training_paces()
        if self.vdot_score != self.current_vdot:
            self.db.update_vdot(str(self.vdot_score))
            self.save_race_paces()
            self.save_training_paces()
            self.current_vdot = self.vdot_score

    def save_training_paces(self):
        """Formats the times of the paces so they can be saved to the config."""
        self.db.update_training_pace([(x.Mile, x.KM, x.Distance) for x in self.training_paces])

    def save_race_paces(self):
        """Formats the times of the paces so they can be saved to the config."""
        self.db.update_race_pace([(x.Time, x.Mile, x.KM, x.Distance) for x in self.race_times])

    def _pace_ranges(self):
        """Returns the vdots that the current vdot score sits between for miles and KM"""
        vdot_score = int(self.vdot_score)
        km = [x for x in self.VDOT_paces if x.xVDOT >= vdot_score and x.xUnit == 'KM']
        mile = [x for x in self.VDOT_paces if x.xVDOT >= vdot_score and x.xUnit =='Mile']
        if len(km) > 1:
            return km[:2], mile[:2]
        else:
            return km, mile


if __name__ == '__main__':
    from settings.settings import Settings
    settings = Settings()
    db = settings.database

    import timeit
    VDOT_values = VDOT(db)

    print(VDOT_values.race_times)

    VDOT_values.calculate_vdot('HalfMarathon', '01:39:00')
    print('Current score:', VDOT_values.vdot_score)
    #settings.update_settings('MaxHR', 189)
    #settings.update_settings('Name', 'Paul Lucas')
    #settings.update_settings('DateOfBirth', datetime.datetime(year=1987, month=6, day=26))

    print('\nTraining')
    for k, m, km in VDOT_values.training_paces:
        print(k.ljust(15), datetime.timedelta(seconds=m), datetime.timedelta(seconds=km))
    print('\nRaces')
    print(VDOT_values.race_times)

    #print(VDOT_values.VDOT_paces)



    print(str(VDOT_values.vdot_score))

    print(VDOT_values.vdot_score - dec(VDOT_values.vdot_score, 0, 'ROUND_FLOOR'))

    VDOT_values.save_vdot()
    settings.get_zones()

    print('SETTINGS')
    for r in db.connection.execute("""
SELECT
COALESCE(VDOTHistory.VDOT, 0) AS VDOT,
MaxHR
Units,
DateOfBirth
FROM Settings
LEFT JOIN VDOTHistory
    ON Settings.VDOTHistoryID = VDOTHistory.VDOTHistoryID;
"""):
        print(r)

    print('VDOT')
    for r in db.connection.execute("SELECT * FROM VDOTHistory"):
        print(r)

    print('100 runs took: {}'.format(timeit.timeit(stmt="VDOT(db)", number=100, globals=globals())))

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
