from settings.converters import dec, convert_distance, convert_to_date, convert_to_time
from settings.settings import Settings
import os
import datetime

settings = Settings()

threshold_time = convert_to_time('00:18:00')
threshold_pace = convert_to_time('00:07:00')

rest_time = convert_to_time('00:08:00')
rest_pace = convert_to_time('00:09:00')

rest_distance = dec(rest_time.total_seconds() / rest_pace.total_seconds(), 2)

distance = dec(threshold_time.total_seconds() / threshold_pace.total_seconds(), 2)

print(distance)
print(rest_distance)

intervals = (1500 * 3) + (1200 * 3)#+ (800)
metres = convert_distance(intervals, 'metre', 'mile')
miles = dec('1.5', 1)
miles += dec('1.5', 1)

print(distance + miles + rest_distance)

settings.WORKOUT_PLANS = 'template\\plans\\'
settings.WORKOUT_TEMPLATES = 'template\\workout templates.json'

plan = settings.db.get_plan_schedule('Half Marathon 47 Miles')
templates = settings.db.get_workouts()

#for k, v in sorted([(int(k),v) for k,v in plan.items()]):
#    print(k, v)

print(len(templates.index.values))

for x in sorted(templates.index.values):
    print(x)

sorted_plan = sorted(set(plan.values()))

# print(len(sorted_plan))
print('\nCheck templates\n')
for x in [x for x in templates if x not in sorted_plan]:
    print(x)

print('\nCheck plan\n')
for x in [x for x in sorted_plan if x not in templates]:
    print(x)


def check_dates():
    race_date = convert_to_date('15/10/2017')

    current = []
    i = 0
    print('\nDates\n')
    for k, v in sorted([(int(k), v) for k, v in plan.items()], reverse=True):
        i += 1
        if v not in current:
            current.append(v)
        days_from = datetime.timedelta(days=int(k))
        print(i, race_date - days_from)
        if len(current) == 30:
            print('break here')
