from collections import OrderedDict
import datetime
from settings.converters import convert_to_time, dec, time_to_string
from settings.settings import Settings
import json
import os

settings = Settings()


class VDOT:
    """Contains the VDOT values for the race and training paces."""
    def __init__(self):
        self.VDOT_paces = set_vdots()
        self.vdot_score = dec('0.00', 2)
        self.training_paces = {}
        self.race_times = {}

    def __getitem__(self, item):
        return self.VDOT_paces[item]

    def __repr__(self):
        return repr(self.VDOT_paces)

    def calculate_vdot(self, distance, time):
        """Calculates the vdot for a person based on the finish time of the distance."""
        race_time = convert_to_time(time)
        full_vdot = self.current_vdot(distance, race_time)
        vdot_distance_diff = self._vdot_difference(full_vdot, distance)
        finish_distance_diff = self._vdot_finish_diff(full_vdot, distance, race_time)
        self.vdot_score = full_vdot + dec(finish_distance_diff / vdot_distance_diff, 2, 'ROUND_FLOOR')
        self._get_training_paces()

    def current_vdot(self, distance, time):
        """Gets the VDOT for the given time."""
        all_vdot = [x for x, y in self.VDOT_paces.items() if time <= y[distance]]
        try:
            return all_vdot[-1]
        except KeyError:
            return self.VDOT_paces.keys()[0]

    def _vdot_difference(self, score, distance):
        """Determines the time difference between a given VDOT score and the next level up for a given distance."""
        current_vdot = self.VDOT_paces[score]
        next_vdot = self.VDOT_paces[score+1]
        return current_vdot[distance] - next_vdot[distance]

    def _vdot_finish_diff(self, score, distance, time):
        """Calculates the difference in time between the given vdot and the finish time of a distance."""
        vdot_time = self.VDOT_paces[score][distance]
        return vdot_time - time

    def _get_training_paces(self):
        """Returns the training paces for the current vdot score."""
        if self.vdot_score == dec('0.00', 2):
            return
        vdot_diff = self._vdot_dec()
        self._calculate_training_paces(vdot_diff)
        return None

    def _calculate_training_paces(self, vdot_diff):
        """Calculates the difference between the vdot score and the given race time."""
        vdot_score = int(self.vdot_score)
        for distance, current_pace in self.VDOT_paces[vdot_score].items(): #[(k, v) for k, v in self.VDOT_paces[vdot_score].items()
                                       #if k.endswith('-KM') or k.endswith('-Mile')]:
            pace_diff = self._vdot_difference(vdot_score, distance)
            pace_to_add = datetime.timedelta(seconds=int(dec(dec(pace_diff.total_seconds()) * vdot_diff, 0)))
            if distance.endswith('-KM') or distance.endswith('-Mile'):
                self.training_paces[distance] = current_pace - pace_to_add
            else:
                self.race_times[distance] = current_pace - pace_to_add

    def _vdot_dec(self):
        """Returns the decimal of the current vdot score."""
        return self.vdot_score - dec(self.vdot_score, 0, 'ROUND_FLOOR')

    def save_vdot(self):
        """Saves the paces and vdot to the config for later use."""
        settings.amend_config('paces', self.format_training_paces())
        settings.amend_config('vdot', str(self.vdot_score))
        settings.amend_config('race_times', self.format_race_paces())

    def format_training_paces(self):
        """Formats the times of the paces so they can be saved to the config."""
        fmt = '{minutes}:{seconds:02}'
        return {k: time_to_string(v, fmt) for k, v in self.training_paces.items()}

    def format_race_paces(self):
        """Formats the times of the paces so they can be saved to the config."""
        fmt = '{hours}:{minutes}:{seconds:02}'
        return {k: time_to_string(v, fmt) for k, v in self.race_times.items()}


def set_vdots():
    """Creates a dictionary from the combined extracts of vdot race and training paces."""
    vdots = OrderedDict()
    vdots = get_vdot_race_paces(vdots, settings.VDOT_RACES)
    vdots = get_vdot_race_paces(vdots, settings.VDOT_TRAINING)
    return vdots


def get_vdot_race_paces(vdots, file_name):
    """Extracts the race paces from the VDOT Races file."""
    headers = []
    with open(file_name, 'r') as vdot_file:
        for line in vdot_file.readlines():
            cells = line.split()  # [:-1] # Ignore last column as this is repeated.
            if cells[0] == 'VDOT':
                headers += cells[1:]
            else:
                cell_times = [convert_to_time(x) if x != '-' else None for x in cells[1:]]
                vdots.setdefault(int(cells[0]), {})
                vdots[int(cells[0])].update(dict(zip(headers, cell_times)))

    return vdots


if __name__ == '__main__':

    VDOT_values = VDOT()
    # print(str(VDOT_values))

    # print(VDOT_values[51])
    print('\n51 Times')
    for k1, v1 in [(k1, v1) for k1, v1 in VDOT_values[51].items()
                   if k1.endswith('-KM') or k1.endswith('-Mile')]:
        print('{} - {}'.format(k1, v1))

    print('\n52 Times')
    for k1, v1 in [(k1, v1) for k1, v1 in VDOT_values[52].items()
                   if k1.endswith('-KM') or k1.endswith('-Mile')]:
        print('{} - {}'.format(k1, v1))

    # print(VDOT_values.current_vdot('Marathon', '3:15:45'))
    VDOT_values.calculate_vdot('HalfMarathon', '1:41:00')

    print('\nTraining Paces')
    for k1, v1 in VDOT_values.training_paces.items():
        if k1.endswith('-Mile'):
            print('{} - {}'.format(k1, v1))

    print('\nRace Times')
    for k1, v1 in VDOT_values.race_times.items():
        print('{} - {}'.format(k1, v1))

    print(VDOT_values.vdot_score)

    print(VDOT_values.vdot_score - dec(VDOT_values.vdot_score, 0, 'ROUND_FLOOR'))

    VDOT_values.save_vdot()
