
class WorkOutStep:
    """Defines an individual step of a workout."""

    next_id = 0

    def __init__(self, name, durations, targets, intensity=None):
        self.name = name
        self.durations = durations
        self.targets = targets
        self.intensity = intensity
        self.id = WorkOutStep._get_next_id()

    @classmethod
    def _get_next_id(cls):
        """Generate the next serial for the container."""
        result = cls.next_id
        cls.next_id += 1
        return result

    @classmethod
    def reset_id(cls):
        """Generate the next serial for the container."""
        cls.next_id = 0

    def __repr__(self):
        fmt = ',{},"{}",{}'
        line = 'Data,0,workout_step'
        line += fmt.format('wkt_step_name', self.name, '')
        line += fmt.format('message_index', self.id, '')
        line += ''.join([fmt.format(k, *v.split(',') + [''])
                         for k, v in self.durations.items()])
        line += ''.join([fmt.format(k, *v.split(',') + [''])
                         for k, v in self.targets.items()])
        if self.intensity is not None:
            line += fmt.format('intensity', self.intensity, '')
        return line + '\n'

