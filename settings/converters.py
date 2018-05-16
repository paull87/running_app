import datetime
from decimal import Decimal


def dec(number, place=None, rounding='ROUND_HALF_EVEN'):
    """Returns the given Decimal in two places."""
    if place is None:
        return Decimal(str(number))
    dec_point = Decimal('0.' + ('0' * place)) if place > 0 else Decimal('0')
    return Decimal(number).quantize(dec_point, rounding=rounding)

metres_in_mile = dec('1609.34')
miles_in_metre = dec('0.000621371')
miles_in_km = dec('0.621371')
km_in_mile = dec('1.60934')

converter_dict = {
    'metre-mile': miles_in_metre,
    'mile-metre': metres_in_mile,
    'km-metre': dec('1000'),
    'metre-km': dec('0.001'),
    'km-mile': miles_in_km,
    'mile-km': km_in_mile
}


def convert_to_date(string):
    """Converts date in format DD/MM/YYYY to a date."""
    try:
        date_elements = string.split('/')
        date = datetime.datetime(day=int(date_elements[0]),
                                      month=int(date_elements[1]),
                                      year=int(date_elements[2]))
        return date
    except:
        raise ValueError('Date is not in format DD/MM/YYYY')


def timestamp(date=datetime.datetime.utcnow()):
    """Creates int representation of date based on seconds since UTC 31/12/1989 00:00."""
    date_base = datetime.datetime(year=1989, month=12, day=31)
    return int((date - date_base).total_seconds())

def convert_to_time(string):
    """Converts given string in format 00:00:00 to datetime."""
    times = [0] * 3
    for i, time in enumerate(reversed(string.split(':'))):
        times[i] = float(time)
    return datetime.timedelta(hours=times[2], minutes=times[1], seconds=times[0])


def convert_distance(distance, from_dis, to_dis):
    """Converts the given distance."""
    return dec(distance * determine_distance_type(from_dis, to_dis))


def calculate_metres_per_sec(pace, dist_type):
    """Convert a given pace to metres per second speed."""
    if dist_type == 'metre':
        seconds = dec(pace.total_seconds())
    else:
        seconds = convert_distance(dec(pace.total_seconds()), 'metre', dist_type)
    metres_per_hour = dec(3600 / seconds)
    return dec(metres_per_hour / 3600, 3)


def calculate_pace(time, distance, dis_type, pace=None):
    """Converts the given time and distance to a miles pace."""
    conversion = determine_distance_type(dis_type, pace) if pace else 1
    percentage = dec(1 / (distance * conversion))
    seconds = dec(dec(time.total_seconds()) * percentage, 2)
    return datetime.timedelta(seconds=float(seconds))


def determine_distance_type(dis_from, dis_to):
    """Returns the conversion number between the two distance types."""
    return converter_dict['{}-{}'.format(dis_from, dis_to)]


def time_to_string(time, fmt):
    """Converts timedelta to the given format."""
    d = {}
    d['hours'], rem = divmod(time.seconds, 3600)
    d['minutes'], d['seconds'] = divmod(rem, 60)
    return fmt.format(**d)


if __name__ == '__main__':
    print('Mile Conversions')
    miles = dec('2')
    print(convert_distance(miles, 'mile', 'metre'))
    print(convert_distance(miles, 'mile', 'km'))

    print('\nKM Conversions')
    km = dec('1')
    print(convert_distance(km, 'km', 'mile'))

    print('\nMetre Conversions')
    metres_test = dec('400')
    metre_to_mile_test = convert_distance(metres_test, 'metre', 'mile')
    print(metre_to_mile_test)
    print(dec(convert_distance(metre_to_mile_test, 'mile', 'metre'), 0))


    print('\nMile Paces')
    milepace = datetime.timedelta(minutes=6, seconds=54)
    metres_per_sec = calculate_metres_per_sec(milepace, 'mile')
    print(metres_per_sec)
    print(str(metres_per_sec) + ',m/s')
    print(calculate_pace(milepace, 1, 'mile', 'km'))
    print(calculate_metres_per_sec(milepace, 'mile'))

    print('\nKM Paces')
    km_pace = datetime.timedelta(minutes=3, seconds=54)
    print(calculate_pace(km_pace, 1, 'km', 'mile'))
    print(calculate_metres_per_sec(km_pace, 'km'))

    another_pace = datetime.timedelta(minutes=45, seconds=16)
    print(calculate_pace(another_pace, 10, 'km', 'mile'))

    print(time_to_string(another_pace, '{minutes}:{seconds}'))


    metres = convert_distance(100 * 12, 'metre', 'mile')
    miles = dec('2.0', 1)
    miles += dec('2.25', 1)

    print(metres + miles)

    print('\nKM Conversions')
    km = dec('15')
    print(convert_distance(km, 'km', 'mile'))

    print('Mile Conversions')
    miles = dec('10')
    print(convert_distance(miles, 'mile', 'km'))
