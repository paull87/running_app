import datetime
from collections import OrderedDict
from decimal import Decimal as D

two_places = D('0.00')
one_places = D('0.0')
no_place = D('0')

class VDOT:
    """Contains the VDOT values for the race and training paces."""
    def __init__(self):
        self.VDOT_race = get_vdot_race_paces()

    def __getitem__(self, item):
        return self.VDOT_race[item]

    def __repr__(self):
        return repr(self.VDOT_race)

    def calculate_vdot(self, distance, time):
        """Calculates the vdot for a person based on the finish time of the distance."""
        race_time = convert_to_time(time)
        print(race_time)
        full_vdot = self.current_vdot(distance, race_time)
        vdot_distance_diff = self._vdot_difference(full_vdot, distance)
        finish_distance_diff = self._vdot_finish_diff(full_vdot, distance, race_time)
        return full_vdot + D(finish_distance_diff / vdot_distance_diff).quantize(two_places, rounding='ROUND_FLOOR')

    def current_vdot(self, distance, time):
        """Gets the VDOT for the given time."""
        all_vdot = [x for x, y in self.VDOT_race.items() if time <= y[distance]]
        try:
            return all_vdot[-1]
        except KeyError:
            return self.VDOT_race.keys()[0]

    def _vdot_difference(self, score, distance):
        """Determines the time difference between a given VDOT score and the next level up for a given distance."""
        current_vdot = self.VDOT_race[score]
        next_vdot = self.VDOT_race[score+1]

        return current_vdot[distance] - next_vdot[distance]

    def _vdot_finish_diff(self, score, distance, time):
        """Calculates the difference in time between the given vdot and the finish time of a distance."""
        vdot_time = self.VDOT_race[score][distance]
        return vdot_time - time


def get_vdot_race_paces():
    """Extracts the race paces from the VDOT Races file."""
    VDOT = OrderedDict()
    headers = []
    with open('VDOT Races.txt', 'r') as VDOT_file:
        for line in VDOT_file.readlines():
            cells = line.split()[:-1] # Ignore last column as this is repeated.
            if cells[0] == 'VDOT':
                headers += cells[1:]
            else:
                cell_times = [convert_to_time(x) for x in cells[1:]]
                VDOT[int(cells[0])] = dict(zip(headers, cell_times))

    return VDOT


def convert_to_time(string):
    """Converts given string in format 00:00:00 to datetime."""
    times = [0] * 3
    for i, time in enumerate(reversed(string.split(':'))):
        times[i] = float(time)
    return datetime.timedelta(hours=times[2], minutes=times[1], seconds=times[0])


if __name__ == '__main__':

    VDOT_values = VDOT()
    #print(str(VDOT_values))

    #print(VDOT_values[84]['1,500'])

    #print(VDOT_values.current_vdot('Marathon', '3:15:45'))
    print(VDOT_values.calculate_vdot('HalfMarathon', '1:29:38'))

