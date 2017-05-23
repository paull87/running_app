from settings.converters import timestamp
from settings.settings import TEMPLATE_PATH


def get_workout_template():
    """Gets the workout """
    try:
        with open(TEMPLATE_PATH, 'r') as template:
            return template.read()
    except Exception as e:
        raise FileNotFoundError('Unable to open the template file.') from None


if __name__ == '__main__':
    workout_template = get_workout_template()

    print(workout_template.format(timestamp(), 'This is a Test Run.'))
