from stravalib.client import Client
from functools import wraps
import datetime
import time
from settings.converters import dec, convert_distance, calculate_pace, calculate_speed


def current15():
    return datetime.datetime.now().minute - (datetime.datetime.now().minute % 15)


class Strava:
    _calls = 0
    _current15 = current15()

    def __init__(self):
        self._client = get_client()
        self.athlete = self.get_athlete()

    def _increase_calls(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            args[0]._calls += 1
            args[0].check_calls()
            return func(*args, **kwargs)
        return wrapper

    @property
    def calls(self):
        return self._calls

    @classmethod
    def increase_calls(cls):
        cls._calls += 1

    def check_calls(self):
        while self._calls > 599:
            if self._current15 != current15():
                self._calls = 1
                self._current15 = current15()
            time.sleep(10)

    @_increase_calls
    def get_athlete(self):
        fmt = '{a.firstname} {a.lastname}'
        return fmt.format(a=self._client.get_athlete())

    @_increase_calls
    def get_activities(self, before=None, after=None):
        for activity in self._client.get_activities(after=after, before=before):
            distance = str(activity.distance).split()[0]
            activity.distance_miles = dec(convert_distance(dec(distance), 'metre', 'mile'))
            activity.distance_km = dec(convert_distance(dec(distance), 'metre', 'km'))
            activity.pace_mile = calculate_pace(activity.moving_time, activity.distance_miles, 'mile')
            activity.pace_km = calculate_pace(activity.moving_time, activity.distance_km, 'km')
            activity.speed_mile = calculate_speed(activity.distance_miles, activity.moving_time)
            activity.speed_km = calculate_speed(activity.distance_km, activity.moving_time)
            yield activity

    @_increase_calls
    def get_laps(self, activity_id):
        for lap in self._client.get_activity_laps(activity_id):
            distance = str(lap.distance).split()[0]
            lap.distance_miles = dec(convert_distance(dec(distance), 'metre', 'mile'))
            lap.distance_km = dec(convert_distance(dec(distance), 'metre', 'km'))
            lap.pace_mile = calculate_pace(lap.moving_time, lap.distance_miles, 'mile')
            lap.pace_km = calculate_pace(lap.moving_time, lap.distance_km, 'km')
            lap.speed_mile = calculate_speed(lap.distance_miles, lap.moving_time)
            lap.speed_km = calculate_speed(lap.distance_km, lap.moving_time)
            yield lap

    @_increase_calls
    def get_gear(self, gear_id):
        return self._client.get_gear(gear_id)


def get_client():
    client = Client()
    authorize_url = client.authorization_url(client_id=26273, redirect_uri='localhost')
    client.access_token = '44c3f25ffc9eb06465da267eaa76b3d9d664dc21'
    return client