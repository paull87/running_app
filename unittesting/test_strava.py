import pytest
import datetime
from settings.strava import Strava


class MockStravaCallLimit(Strava):
    _calls = 599

    def check_calls(self):
        while self._calls > 600:
            if self._current15 != self._current15 + 1:
                self._calls = 1
                self._current15 = self._current15 + 1


@pytest.fixture()
def mock_strava_call_limit():
    return MockStravaCallLimit()


@pytest.fixture()
def strava_connection():
    return Strava()


before_date = datetime.datetime(year=2018, month=10, day=8)
after_date = datetime.datetime(year=2018, month=9, day=8)


def test_strava():
    strava = Strava()
    assert isinstance(strava, Strava)


def test_connect_to_strava(strava_connection):
    assert strava_connection.athlete == 'Paul Lucas'


def test_calls_made_start(strava_connection):
    assert strava_connection.calls == 1


def test_get_activities(strava_connection):
    activities = strava_connection.get_activities(after=after_date, before=before_date)
    assert len(list(activities)) > 0
    assert strava_connection.calls == 2


def test_get_laps(strava_connection):
    activities = strava_connection.get_activities(after=after_date, before=before_date)
    laps = strava_connection.get_laps(next(activities).id)
    assert len(list(laps)) > 0
    assert strava_connection.calls == 3


def test_get_gear(strava_connection):
    activities = strava_connection.get_activities(after=after_date, before=before_date)
    gear = strava_connection.get_gear(next(activities).gear_id)
    assert gear.name is not None
    assert strava_connection.calls == 3


def test_calls_limit(mock_strava_call_limit):
    assert mock_strava_call_limit.calls == 600
    activities = mock_strava_call_limit.get_activities(after=after_date, before=before_date)
    assert len(list(activities)) > 0
    assert mock_strava_call_limit.calls == 1
