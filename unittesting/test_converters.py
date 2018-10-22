import pytest
from settings.converters import *
from decimal import Decimal
import datetime


def test_dec_is_decimal():
    num = dec(9)
    assert isinstance(num, Decimal)


def test_dec_decimal_point():
    num = dec('9.1234567', 2)
    assert num == Decimal('9.12')


def test_dec_round_up():
    num = dec('9.123', 2, 'ROUND_UP')
    assert num == Decimal('9.13')


def test_dec_round_down():
    num = dec('9.123', 2, 'ROUND_DOWN')
    assert num == Decimal('9.12')


def test_convert_to_date():
    date_string = '24/11/2018'
    assert convert_to_date(date_string) == datetime.datetime(2018, 11, 24)


def test_convert_to_date_error():
    date_string = 'dd/mm/yyyy'
    with pytest.raises(ValueError):
        convert_to_date(date_string)


def test_timestamp():
    date = datetime.datetime(2018, 11, 24)
    assert timestamp(date) == 911952000


def test_convert_to_time_hhmmss():
    time_string = '14:32:54'
    assert convert_to_time(time_string) == datetime.timedelta(hours=14, minutes=32, seconds=54)


def test_convert_to_time_mmss():
    time_string = '32:54'
    assert convert_to_time(time_string) == datetime.timedelta(minutes=32, seconds=54)


def test_convert_to_time_ss():
    time_string = '54'
    assert convert_to_time(time_string) == datetime.timedelta(seconds=54)


def test_convert_distance_mile_to_metre():
    assert convert_distance(5, 'mile', 'metre') == Decimal('8046.72')


def test_convert_distance_mile_to_km():
    assert convert_distance(5, 'mile', 'km') == Decimal('8.04672')


def test_convert_distance_metre_to_mile():
    assert convert_distance(5, 'metre', 'mile') == Decimal('0.003106856')


def test_convert_distance_metre_to_km():
    assert convert_distance(5, 'metre', 'km') == Decimal('0.005')


def test_convert_distance_km_to_metre():
    assert convert_distance(5, 'km', 'metre') == Decimal('5000')


def test_convert_distance_km_to_mile():
    assert convert_distance(5, 'km', 'mile') == Decimal('3.106856')


def test_calculate_metres_per_sec_metre():
    pace_time = datetime.timedelta(minutes=1, seconds=30)
    assert calculate_metres_per_sec(pace_time, 'metre') == Decimal('0.011')


def test_calculate_metres_per_sec_km():
    pace_time = datetime.timedelta(minutes=4, seconds=30)
    assert calculate_metres_per_sec(pace_time, 'km') == Decimal('3.704')


def test_calculate_metres_per_sec_mile():
    pace_time = datetime.timedelta(minutes=8, seconds=30)
    assert calculate_metres_per_sec(pace_time, 'mile') == Decimal('3.156')


def test_calculate_pace_mile():
    pace_time = datetime.timedelta(minutes=17, seconds=30)
    assert calculate_pace(pace_time, 2, 'mile') == datetime.timedelta(seconds=525)


def test_calculate_pace_mile_to_metre():
    pace_time = datetime.timedelta(minutes=17, seconds=30)
    assert calculate_pace(pace_time, 2, 'mile', 'metre') == datetime.timedelta(seconds=0.33)


def test_calculate_pace_mile_to_km():
    pace_time = datetime.timedelta(minutes=17, seconds=30)
    assert calculate_pace(pace_time, 2, 'mile', 'km') == datetime.timedelta(seconds=326.22)


def test_calculate_pace_km():
    pace_time = datetime.timedelta(minutes=17, seconds=30)
    assert calculate_pace(pace_time, 5, 'km') == datetime.timedelta(seconds=210)


def test_calculate_pace_km_to_metre():
    pace_time = datetime.timedelta(minutes=17, seconds=30)
    assert calculate_pace(pace_time, 5, 'km', 'metre') == datetime.timedelta(seconds=0.21)


def test_calculate_pace_km_to_mile():
    pace_time = datetime.timedelta(minutes=17, seconds=30)
    assert calculate_pace(pace_time, 5, 'km', 'mile') == datetime.timedelta(seconds=337.96)


def test_calculate_pace_metre():
    pace_time = datetime.timedelta(seconds=35)
    assert calculate_pace(pace_time, 200, 'metre') == datetime.timedelta(seconds=0.18)


def test_calculate_pace_metre_to_km():
    pace_time = datetime.timedelta(seconds=35)
    assert calculate_pace(pace_time, 200, 'metre', 'km') == datetime.timedelta(seconds=175)


def test_calculate_pace_metre_to_mile():
    pace_time = datetime.timedelta(seconds=35)
    assert calculate_pace(pace_time, 200, 'metre', 'mile') == datetime.timedelta(seconds=281.64)

def test_determine_distance_type_mile_metre():
    assert determine_distance_type('mile', 'metre') == Decimal('1609.344')


def test_determine_distance_type_mile_km():
    assert determine_distance_type('mile', 'km') == Decimal('1.609344')


def test_determine_distance_type_km_metre():
    assert determine_distance_type('km', 'metre') == Decimal('1000')


def test_determine_distance_type_km_mile():
    assert determine_distance_type('km', 'mile') == Decimal('0.6213712')


def test_determine_distance_type_metre_mile():
    assert determine_distance_type('metre', 'mile') == Decimal('0.0006213712')


def test_determine_distance_type_metre_km():
    assert determine_distance_type('metre', 'km') == Decimal('0.001')


def test_time_to_string_hhmmss():
    assert time_to_string(datetime.timedelta(hours=15, minutes=14, seconds=56), '{hours}:{minutes}:{seconds}') == '15:14:56'


def test_time_to_string_mmss():
    assert time_to_string(datetime.timedelta(hours=15, minutes=14, seconds=56), '{minutes}:{seconds}') == '14:56'


def test_time_to_string_ss():
    assert time_to_string(datetime.timedelta(hours=15, minutes=14, seconds=56), '{seconds}') == '56'
