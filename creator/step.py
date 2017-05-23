
class WorkOutStep:
    """Defines an individual step of a workout."""

    next_id = 0

    def __init__(self, name, duration_type, duration, target_type, target, intensity):
        self.name = name
        self.duration_type = duration_type
        self.duration = duration
        self.target_type = target_type
        self.target = target
        self.intensity = intensity
        self.id = WorkOutStep._get_next_id()

    @classmethod
    def _get_next_id(cls):
        """Generate the next serial for the container."""
        result = cls.next_id
        cls.next_id += 1
        return result
