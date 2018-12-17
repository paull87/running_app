from decimal import Decimal as D
import datetime

two_places = D('0.00')
one_place = D('0')


my_time = datetime.timedelta(hours=1, minutes=40, seconds=00)

time_45 = datetime.timedelta(hours=1, minutes=40, seconds=20)
time_46 = datetime.timedelta(hours=1, minutes=38, seconds=27)

print(time_45 - time_46)
print(time_45 - my_time)

time_diff = time_45 - time_46
my_diff = time_45 - my_time

print(D(my_diff / time_diff).quantize(two_places))

print(D(D(time_diff.total_seconds()) * D(my_diff / time_diff).quantize(two_places)).quantize(D('0'), rounding='ROUND_FLOOR'))


print(datetime.datetime(year=1989, month=12, day=31))

print(int((datetime.datetime.utcnow() - datetime.datetime(year=1989, month=12, day=31)).total_seconds()))
print((datetime.datetime.utcnow() - datetime.datetime(year=1989, month=12, day=31)).total_seconds())


print(datetime.timedelta(minutes=62, seconds=20))

print(datetime.timedelta(hours=3, minutes=15, seconds=45))

vdot_diff = datetime.timedelta(hours=3, minutes=17, seconds=29) - datetime.timedelta(hours=3, minutes=14, seconds=6)

time_diff = datetime.timedelta(hours=3, minutes=17, seconds=29) - datetime.timedelta(hours=3, minutes=15, seconds=45)

print(vdot_diff.total_seconds())
print(time_diff.total_seconds())

print(D(time_diff / vdot_diff).quantize(two_places))

pace = datetime.timedelta(minutes=8, seconds=0)

hour = datetime.timedelta(minutes=60, seconds=0)
