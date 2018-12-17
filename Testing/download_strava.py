from settings.strava import Strava
import datetime
from collections import defaultdict
import csv

csv.register_dialect('unixpwd', delimiter=':', quoting=csv.QUOTE_NONE)

strava_connection = Strava()

header = 'DiaryDate,RunTime,RunType,DistanceMiles,DistanceKM,PaceMile,PaceKM,AverageHR,ShoeID,StravaID,Comment\n'
fmt = '{a.start_date_local},{a.elapsed_time},{a.distance_miles},{a.distance_km},{a.average_heartrate},{a.gear_id},{a.id},{a.description}\n'

shoes = dict()

def default_shoe(gear_id):
    if not gear_id:
        return
    if gear_id not in shoes.keys():
        shoes[gear_id] = strava_connection.get_gear(gear_id).name

    return shoes[gear_id]


with open('strava_activities.csv', 'w', newline='') as open_file:
    writer = csv.writer(open_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['DiaryDate', 'RunTime', 'RunType', 'DistanceMiles', 'DistanceKM', 'SpeedMPH', 'SpeedKPH',
                     'PaceMile', 'PaceKM', 'AverageHR', 'ShoeID', 'ShoeName', 'StravaID', 'Comment'])
    for a in strava_connection.get_activities(after=datetime.datetime(2016, 1, 1)):

        writer.writerow([a.start_date_local, a.elapsed_time, a.workout_type, a.distance_miles, a.distance_km,
                         a.speed_mile, a.speed_km, a.pace_mile, a.pace_km, a.average_heartrate, a.gear_id,
                         shoes.setdefault(a.gear_id, default_shoe(a.gear_id)), a.id, a.description])
