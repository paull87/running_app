import datetime

from settings.converters import dec

today_date = datetime.datetime(1, 1, 1, 0, 0, 0)

race_pace = datetime.time(hour=0, minute=7, second=37)

easy_pace = datetime.time(hour=0, minute=8, second=56)

print(race_pace)
print(easy_pace)
print(datetime.datetime.combine(today_date, easy_pace) - datetime.datetime.combine(today_date, race_pace))

race_pace = datetime.timedelta(minutes=7, seconds=37)
easy_pace = datetime.timedelta(minutes=8, seconds=56)

print(race_pace.total_seconds())

print(easy_pace / race_pace)

print('CHECKING JD FORMULA\n')

my_time = datetime.timedelta(hours=1, minutes=39, seconds=10)

time_45 = datetime.timedelta(hours=1, minutes=40, seconds=20)
time_46 = datetime.timedelta(hours=1, minutes=38, seconds=27)

between_times = time_45 - time_46
my_time_diff = my_time - time_46

print(between_times, my_time_diff)

print(1 - (my_time_diff / between_times))

print(between_times * 0.61)

print(divmod(race_pace.seconds, 60))


print(' '.join(['{}'] * 3))

score = dec('0.26', 2)

print(int(score))

print(between_times.total_seconds())
print(dec(dec(between_times.total_seconds()) * score, 0))


print(list(range(12.5)))
