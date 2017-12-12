from settings.converters import timestamp
from settings.settings import Settings

settings = Settings()


def get_schedule_template():
    """Gets the schedule template needed to create a schedule file."""
    try:
        with open(settings.SCHEDULE_PATH, 'r') as template:
            return template.read()
    except Exception:
        raise FileNotFoundError('Unable to open the schedule file.') from None


def get_workout_template():
    """Gets the workout template needed to create a workout file."""
    try:
        with open(settings.TEMPLATE_PATH, 'r') as template:
            return template.read()
    except Exception:
        raise FileNotFoundError('Unable to open the template file.') from None


if __name__ == '__main__':
    workout_template = get_workout_template()

    print(workout_template.format(timestamp(), 'This is a Test Run.', 9999))
