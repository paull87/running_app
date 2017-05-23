from collections import OrderedDict
from settings.converters import convert_to_time, dec
from settings.settings import VDOT_RACES, VDOT_TRAINING

class VDOT:
    """Contains the VDOT values for the race and training paces."""
    def __init__(self):
        self.VDOT_paces = set_vdots()

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
        return full_vdot + dec(finish_distance_diff / vdot_distance_diff, 2, 'ROUND_FLOOR')

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


def set_vdots():
    """Creates a dictionary from the combined extracts of vdot race and training paces."""
    vdots = OrderedDict()
    vdots = get_vdot_race_paces(vdots, VDOT_RACES)
    vdots = get_vdot_race_paces(vdots, VDOT_TRAINING)

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
    #print(str(VDOT_values))

    print(VDOT_values[46])

    #print(VDOT_values.current_vdot('Marathon', '3:15:45'))
    print(VDOT_values.calculate_vdot('HalfMarathon', '1:29:38'))

