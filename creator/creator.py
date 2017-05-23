from template.template import get_workout_template
from workout import Workout
from settings.settings import WORKOUTS_PATH

workout = Workout('Easy 12 Mile')

print(workout.timestamp)
print(workout.name)

with open('{}{}.csv'.format(WORKOUTS_PATH, workout.timestamp), 'w') as template_file:
    template_file.write(get_workout_template().format(workout.timestamp, workout.name))

