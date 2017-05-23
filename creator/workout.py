import datetime


def timestamp(date=datetime.datetime.utcnow()):
    """Creates int representation of date based on seconds since UTC 31/12/1989 00:00."""
    date_base = datetime.datetime(year=1989, month=12, day=31)

    return int((date - date_base).total_seconds())


class Workout:
    """Defines a single workout file."""
    # Starting timestamp of the workouts creation.
    next_timestamp = timestamp()

    def __init__(self, name):
        """Initialise the workout."""
        self.name = name
        self.timestamp = Workout._get_next_timestamp()

    @classmethod
    def _get_next_timestamp(cls):
        """Generate the next serial for the container."""
        result = cls.next_timestamp
        cls.next_timestamp += 1
        return result
