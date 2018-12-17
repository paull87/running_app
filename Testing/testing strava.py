from settings.converters import dec, convert_distance, convert_to_date, convert_to_time, calculate_pace
from settings.settings import Settings
import datetime
from stravalib.client import Client

settings = Settings()

client = Client()
authorize_url = client.authorization_url(client_id=26273, redirect_uri='localhost')
client.access_token = '44c3f25ffc9eb06465da267eaa76b3d9d664dc21'

athlete = client.get_athlete()

calls = 0
afterdate = datetime.datetime(year=2018, month=1, day=18)
beforedate = datetime.datetime(year=2018, month=1, day=19)


def get_activities(afterdate, beforedate):
    global calls
    calls += 1
    for activity in client.get_activities(after=afterdate, before=beforedate):
        distance = str(activity.distance).split()[0]
        activity.distance_miles = dec(convert_distance(dec(distance), 'metre', 'mile'))
        activity.distance_km = dec(convert_distance(dec(distance), 'metre', 'km'))
        activity.gear_name = activity_gear(activity.gear_id)
        yield activity


def get_laps(activity_id):
    global calls
    calls += 1
    for lap in client.get_activity_laps(activity_id):
        distance = str(lap.distance).split()[0]
        lap.distance_miles = dec(convert_distance(dec(distance), 'metre', 'mile'))
        lap.distance_km = dec(convert_distance(dec(distance), 'metre', 'km'))
        yield lap


def activity_gear(gear_id):
    global calls
    calls += 1
    gear = client.get_gear(str(gear_id))
    return gear.name


fmt = '{a.id}, {a.start_date_local}, {a.workout_type}, {a.elapsed_time}, {a.distance}, {a.distance_miles}, {a.distance_km}, {a.average_heartrate}, {a.gear_name} {a.comments} {a.name}'
lap_fmt = '{l.name}, {l.moving_time}, {l.distance}, {l.distance_miles:.2}, {l.distance_km:.2}, {l.total_elevation_gain}, {l.split}, {l.average_heartrate}'
for a in get_activities(afterdate, beforedate):
    print(fmt.format(a=a))
    points = 0
    #for l in get_laps(a.id):
    #    pass
        #lap_points = settings.calculate_intensity_points(l.average_heartrate, l.elapsed_time)
        #points += lap_points
        #pace = calculate_pace(l.moving_time, l.distance_km, 'km', 'mile')
#
        #print(dec(l.distance_km, 2), calculate_pace(l.moving_time, l.distance_km, 'km', 'mile'))
        #print(dec(l.distance_miles, 2), calculate_pace(l.moving_time, l.distance_miles, 'mile'))
        #print(pace)
        #print('Points: {}'.format(lap_points), lap_fmt.format(l=l))
    print('Total Points:', points)

print('Total Calls: {}'.format(calls))