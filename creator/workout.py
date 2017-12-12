from settings.converters import timestamp, calculate_metres_per_sec, convert_distance, dec, convert_to_time
from settings.settings import Settings
from step import WorkOutStep
import datetime
import random

settings = Settings()
pace_add = datetime.timedelta(seconds=10)


class Workout:
    """Defines a single workout file."""
    # Starting timestamp of the workouts creation.
    next_timestamp = timestamp()
    next_serial = random.randrange(10000000, 99990000)


    def __init__(self, name, paces, run): # warmup=None, cooldown=None, intervals=None, run=None, splits=1):
        """Initialise the workout."""
        self.name = name
        self.timestamp = Workout._get_next_timestamp()
        self.serial = Workout._get_serial_number()
        #self.workout_type = workout_type
        self.run = run
        self.paces = paces
        self.steps = []
        self._decide_workout()

        WorkOutStep.reset_id()

    @classmethod
    def _get_next_timestamp(cls):
        """Generate the next serial for the container."""
        result = cls.next_timestamp
        cls.next_timestamp += 1
        return result

    @classmethod
    def _get_serial_number(cls):
        """Generates the serial number based on the timestamp"""
        result = cls.next_serial
        cls.next_serial += 1
        return result


    def _decide_workout(self):
        """Decides which workout needs to be created depending on type."""
        # if self.workout_type in ['easy', 'long', 'recovery']:
        #    self.create_standard_workout()
        for step in self.run:
            if type(step) == dict:
                self.create_interval(step)
            else:
                self.create_standard_step(step)

    def create_interval(self, interval):
        """Creates an interval step"""
        active = interval['active']
        rest = interval['rest']
        repeat = interval['repeat']

        # Process active step
        repeat_id = self.check_step_type(active)
        # Process rest step if given
        if rest:
            self.create_standard_step(rest)

        # Process repeat step if given
        if repeat:
            self.steps.append(create_repeat_step(repeat_id, repeat))

        return repeat_id

    def create_standard_step(self, run):
        """Creates a standard workout for a distance or length of time"""
        steps = []
        workout_type, run_target, run_duration, splits, intensity = run

        if run_target == '':
            run_target = determine_target(workout_type)

        run_duration_type, run_duration_value, run_duration_unit = format_duration(run_duration)

        # Create mile/km splits if greater than 1
        if run_duration_type == 'distance' and splits == 1 and run_duration_unit != 'metre':
            run_duration_rounded = int(dec(run_duration_value, 0, 'ROUND_FLOOR'))
            run_duration_remainder = dec(run_duration_value.remainder_near(1), 1, 'ROUND_UP').copy_abs()
            step = self.create_step(workout_type, run_target, run_duration_type, 1, run_duration_unit)
            steps.append(step)
            if run_duration_rounded > 1:  # Only create a repeat if there are more than one.
                repeat_step = create_repeat_step(step.id, run_duration_rounded)
                steps.append(repeat_step)
            if run_duration_remainder > 0:
                remainder_step = self.create_step(workout_type, run_target, run_duration_type,
                                                  run_duration_remainder, run_duration_unit)
                steps.append(remainder_step)
        else:
            step = self.create_step(workout_type, run_target, run_duration_type, run_duration_value, run_duration_unit)
            steps.append(step)
        self.steps += steps
        return steps[0].id

    def create_step(self, workout_type, run_target, run_duration_type, run_duration, run_duration_unit):
        """Creates the step for a workout."""
        # Create targets
        if run_target == 'pace':
            run_pace = self.paces[workout_type]
            target_value_low = calculate_metres_per_sec(run_pace, settings.units)
            target_value_high = calculate_metres_per_sec(run_pace - pace_add, settings.units)
            targets = settings.get_pace_targets(target_value_high, target_value_low)
        elif run_target == 'hr':
            target_value_low = settings.zones[workout_type][0] + 100
            target_value_high = settings.zones[workout_type][1] + 100
            targets = settings.get_hr_targets(target_value_high, target_value_low)
        else:  # run_target == 'none':
            targets = settings.get_open_targets()

        # Create duration
        if run_duration_type == 'distance':
            if run_duration_unit != 'metre':
                run_duration = convert_distance(run_duration, run_duration_unit, 'metre')
            durations = settings.get_distance_durations(run_duration)
        elif run_duration_type == 'time':
            durations = settings.get_time_durations(run_duration)
        else:  # run_duration_type == 'none':
            durations = settings.get_open_durations()

        return WorkOutStep('Run', durations, targets, 0)

    def check_step_type(self, step):
        """Checks whether the step is an interval or one-off step."""
        if type(step) == dict:
            first_step_id = self.create_interval(step)
        else:
            first_step_id = self.create_standard_step(step)
        return first_step_id


def create_repeat_step(step_id, repeats):
    """Creates a repeat of the given step and number."""
    step_name = 'Repeat Step {} x{}'.format(step_id + 1, repeats)
    durations = settings.get_repeat_durations(step_id, repeats)
    targets = {}
    return WorkOutStep(step_name, durations, targets)


def format_duration(duration):
    """Formats the duration of workout."""
    if type(duration) == list:  # List is for distance based
        duration_type = 'distance'
        duration_value = dec(duration[0], 2)
        duration_unit = duration[1]
        if duration_unit != 'metre' and duration_unit != settings.units:
            duration_value = convert_distance(duration_value, duration_unit, settings.units)
    elif duration:
        duration_type = 'time'
        duration_value = convert_to_time(duration).total_seconds()
        duration_unit = None
    else:
        duration_type = 'none'
        duration_value = None
        duration_unit = None
    return duration_type, duration_value, duration_unit


def determine_target(workout_type):
    """Determines the target based on settings for that type of run."""
    try:
        return settings.default_targets[workout_type]
    except KeyError as e:  # return pace as key error assumes it is race distance.
        return 'pace'



if __name__ == '__main__':
    from VDOT.VDOT import VDOT

    VDOT_values = VDOT()
    VDOT_values.calculate_vdot('HalfMarathon', '1:29:38')
    paces = {k.split('-')[0].lower(): v for k, v in VDOT_values.training_paces.items() if settings.units in k.lower()}
    print(paces)
    print(VDOT_values.training_paces)

    test_workout = Workout('Test Easy Run', paces, run=[
        ('easy', 'hr', ['10.5', 'mile'], 1, 0),
        ('interval', 'pace', ['6', 'km'], 1, 1)
    ])

    print('\nTest Workout\n')
    for step in test_workout.steps:
        print(step)

    test_interval_workout = Workout('Test Interval Run', paces, run=[
        ('easy', 'hr', ['1.5', 'mile'], 1, 1),
        {
            'active': ('interval', 'pace', ['0.5', 'mile'], 0, 1),
            'rest': ('easy', 'none', '00:04:00', 0, 0),
            'repeat': 5
        },
        ('easy', 'hr', ['2.5', 'mile'], 1, 1)
    ])

    print('\nTest Interval\n')
    for step in test_interval_workout.steps:
        print(step)


    test_interval_interval_workout = Workout('Test Interval x2 Run', paces, run=[
        ('easy', 'hr', ['2.5', 'mile'], 1, 1),
        {
            'active': {
                'active': ('interval', 'pace', ['400', 'metre'], 0, 1),
                'rest': ('easy', 'none', ['0.25', 'mile'], 0, 0),
                'repeat': 3
            },
            'rest': ('easy', 'none', '00:04:00', 0, 0),
            'repeat': 2
        },
        ('easy', 'hr', ['2.5', 'mile'], 1, 1)
    ])

    print('\nTest Interval In Interval\n')
    for step in test_interval_interval_workout.steps:
        print(step)
