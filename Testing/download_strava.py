from settings.strava import Strava
import datetime
from collections import defaultdict
import csv
from settings.settings import Settings
from settings.converters import dec

csv.register_dialect('unixpwd', delimiter=':', quoting=csv.QUOTE_NONE)

strava_connection = Strava()
settings = Settings()

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
    for a in strava_connection.get_activities(after=datetime.datetime(2014, 1, 1)):
        a.start_date_local = a.start_date_local.replace(second=0)
        ref = settings.database.connection.execute('SELECT DiaryID, DiaryDate FROM Diary WHERE DiaryDate = ?',
                                             (a.start_date_local,)).fetchone()
        if ref:
            cursor = settings.database.connection.cursor()
            cursor.execute('UPDATE Diary SET StravaID = ? WHERE DiaryID = ?;', (a.id, ref[0]))
            settings.database.connection.commit()
        elif a.start_date_local > datetime.datetime(2016, 3, 27):
            settings.database.add_diary_entry((
                None,
                a.start_date_local,
                a.elapsed_time.total_seconds(),
                0,
                str(dec(a.distance_miles, 2)),
                str(dec(a.distance_km, 2)),
                str(a.speed_mile),
                str(a.speed_km),
                a.pace_mile.total_seconds(),
                a.pace_km.total_seconds(),
                a.average_heartrate,
                0,
                None,
                None,
                None,
                None,
                a.id,
                None,
                None,
                shoes.setdefault(a.gear_id, default_shoe(a.gear_id)),
                False)
            )
        #writer.writerow([a.start_date_local, a.elapsed_time, a.workout_type, a.distance_miles, a.distance_km,
        #                 a.speed_mile, a.speed_km, a.pace_mile, a.pace_km, a.average_heartrate, a.gear_id,
        #                 shoes.setdefault(a.gear_id, default_shoe(a.gear_id)), a.id, a.description])
