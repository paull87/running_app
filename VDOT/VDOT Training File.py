from collections import OrderedDict
from settings.converters import convert_to_time, calculate_pace, time_to_string, convert_distance, dec


distances = {
    '1,500': [dec('1.5', 1), convert_distance(dec('1.5', 1), 'km', 'mile')],
    'Mile': [convert_distance(dec('1', 0), 'mile', 'km'), dec('1', 0)],
    '3,000': [dec('3', 0), convert_distance(dec('3', 0), 'km', 'mile')],
    '2mile': [convert_distance(dec('2', 0), 'mile', 'km'), dec('2', 0)],
    '5,000': [dec('5', 0), convert_distance(dec('5', 0), 'km', 'mile')],
    '10K': [dec('10', 0), convert_distance(dec('10', 0), 'km', 'mile')],
    '15K': [dec('15', 0), convert_distance(dec('15', 0), 'km', 'mile')],
    '10Mile': [convert_distance(dec('10', 2), 'mile', 'km'), dec('10', 0)],
    'HalfMarathon': [convert_distance(dec('13.11', 2), 'mile', 'km'), dec('13.11', 2)],
    'Marathon': [convert_distance(dec('26.22', 2), 'mile', 'km'), dec('26.22', 2)]
}

def get_vdot_race_paces(file):
    """Extracts the race paces from the VDOT Races file."""
    vdot = OrderedDict()
    headers = []
    with open(file, 'r') as VDOT_file:
        for line in VDOT_file.readlines():
            cells = line.split()  # Ignore last column as this is repeated.
            if cells[0] == 'VDOT':
                headers += cells[1:]
            else:
                cell_times = [x for x in cells[1:]]
                vdot[int(cells[0])] = dict(zip(headers, cell_times))

    return vdot


def fix_ir_file():
    """Extracts the race paces from the VDOT Races file."""
    new_lines = ''
    with open('VDOT IR.txt', 'r') as VDOT_file:
        for line in VDOT_file.readlines():
            cells = line.split()  # Ignore last column as this is repeated.
            new_lines += ' '.join([cells[-1]] + cells[:-1]) + '\n'
            with open('VDOT IR Fixed.txt', 'w') as new_VDOT_file:
                new_VDOT_file.write(new_lines)
        print('Formatted.')


def get_race_paces(races):
    paces={}
    recovery_km = convert_to_time('01:15')
    recovery_mile = convert_to_time('02:00')
    plus2 = convert_to_time('00:02')
    for vdot, race_times in races.items():
        paces[vdot] = {}
        for race, times in race_times.items():
            if vdot == 30:
                print(race, convert_to_time(times), distances[race][0], distances[race][1])
            paces[vdot][race + '-KM'] = time_hhmm(calculate_pace(convert_to_time(times), distances[race][0], 'km'))
            paces[vdot][race + '-Mile'] = time_hhmm(calculate_pace(convert_to_time(times), distances[race][1], 'mile'))
            if race == 'HalfMarathon':
                paces[vdot]['Recovery-KM'] = time_hhmm(calculate_pace(convert_to_time(times)
                                                                     , distances[race][0], 'km') +
                                                      recovery_km)
                paces[vdot]['Recovery-Mile'] = time_hhmm(calculate_pace(convert_to_time(times)
                                                                       , distances[race][1], 'mile') +
                                                        recovery_mile)
            if race == '15K':
                paces[vdot]['10Mile-Mile'] = time_hhmm(
                    calculate_pace(convert_to_time(times), distances[race][1], 'mile') + plus2)

                paces[vdot]['10Mile-KM'] = time_hhmm(calculate_pace(calculate_pace(
                    convert_to_time(times), distances[race][1], 'mile') + plus2,
                                     1, 'mile', 'km'))

    return paces


def time_hhmm(time):
    """Converts given time to h:mm format"""
    fmt = '{minutes}:{seconds:02d}'
    return time_to_string(time, fmt)


def get_interval_time(intervals, pace):
    """Gets the interval pace based on the longest distance."""
    if intervals['IntervalM'] != '-':
        return intervals['IntervalM'] if pace == 'mile' \
            else time_hhmm(calculate_pace(convert_to_time(intervals['IntervalM']), 1, 'mile', pace))
    elif intervals['Interval1200'] != '-':
        return time_hhmm(calculate_pace(convert_to_time(intervals['Interval1200']), 1200, 'metre', pace))
    elif intervals['IntervalKM'] != '-':
        return intervals['IntervalKM'] if pace == 'km' \
            else time_hhmm(calculate_pace(convert_to_time(intervals['IntervalKM']), 1, 'km', pace))
    else:
        return time_hhmm(calculate_pace(convert_to_time(intervals['Interval400']), 400, 'metre', pace))


def get_repetition_time(repetition, pace):
    """Gets the interval pace based on the longest distance."""
    if repetition['Repetition800'] != '-':
        return time_hhmm(calculate_pace(convert_to_time(repetition['Repetition800']), 800, 'metre', pace))
    elif repetition['Repetition600'] != '-':
        return time_hhmm(calculate_pace(convert_to_time(repetition['Repetition600']), 600, 'metre', pace))
    elif repetition['Repetition400'] != '-':
        return time_hhmm(calculate_pace(convert_to_time(repetition['Repetition400']), 400, 'metre', pace))
    elif repetition['Repetition300'] != '-':
        return time_hhmm(calculate_pace(convert_to_time(repetition['Repetition300']), 300, 'metre', pace))
    else:
        return time_hhmm(calculate_pace(convert_to_time(repetition['Repetition200']), 200, 'metre', pace))




if __name__ == '__main__':
    fix_ir_file()

    vdots = get_vdot_race_paces('VDOT EMT.txt')
    vdots_ir = get_vdot_race_paces('VDOT IR Fixed.txt')

    vdot_races = get_vdot_race_paces('VDOT Races.txt')
    race_paces = get_race_paces(vdot_races)

    vdot_lines = [
        'VDOT Easy-KM Easy-Mile Long-KM Long-Mile Marathon-KM Marathon-Mile Threshold-KM Threshold-Mile' +
        ' Recovery-KM Recovery-Mile' +
        # ' Interval400 IntervalKM Interval1200 IntervalM' +
        # ' Repetition200 Repetition300 Repetition400 Repetition600 Repetition800' +
        ' Interval-KM Interval-Mile Repetition-KM Repetition-Mile' +
        ' 1,500-KM 1,500-Mile Mile-KM Mile-Mile 3,000-KM 3,000-Mile 2Mile-KM 2Mile-Mile 5,000-KM 5,000-Mile' +
        ' 10K-KM 10K-Mile 15K-KM 15K-Mile 10Mile-KM 10Mile-Mile HalfMarathon-KM HalfMarathon-Mile Marathon-KM Marathon-Mile\n'
    ]

    line_fmt = ' '.join(['{}'] * len(vdot_lines[0].split())) + '\n'

    for k, v in vdots.items():
        vdot_lines.append(line_fmt.format(
            k,
            v['Easy/LongKM'].split('-')[0],
            v['Easy/LongM'].split('-')[0],
            v['Easy/LongKM'].split('-')[1],
            v['Easy/LongM'].split('-')[1],
            v['MarathonKM'],
            v['MarathonM'],
            # v['Threshold400'],
            v['ThresholdKM'],
            v['ThresholdM'],
            race_paces[k]['Recovery-KM'],
            race_paces[k]['Recovery-Mile'],
            # vdots_ir[k]['Interval400'],
            # vdots_ir[k]['IntervalKM'],
            # vdots_ir[k]['Interval1200'],
            # vdots_ir[k]['IntervalM'],
            # vdots_ir[k]['Repetition200'],
            # vdots_ir[k]['Repetition300'],
            # vdots_ir[k]['Repetition400'],
            # vdots_ir[k]['Repetition600'],
            # vdots_ir[k]['Repetition800'],
            get_interval_time(vdots_ir[k], 'km'),
            get_interval_time(vdots_ir[k], 'mile'),
            get_repetition_time(vdots_ir[k], 'km'),
            get_repetition_time(vdots_ir[k], 'mile'),
            race_paces[k]['1,500-KM'],
            race_paces[k]['1,500-Mile'],
            race_paces[k]['Mile-KM'],
            race_paces[k]['Mile-Mile'],
            race_paces[k]['2mile-KM'],
            race_paces[k]['2mile-Mile'],
            race_paces[k]['3,000-KM'],
            race_paces[k]['3,000-Mile'],
            race_paces[k]['5,000-KM'],
            race_paces[k]['5,000-Mile'],
            race_paces[k]['10K-KM'],
            race_paces[k]['10K-Mile'],
            race_paces[k]['15K-KM'],
            race_paces[k]['15K-Mile'],
            race_paces[k]['10Mile-KM'],
            race_paces[k]['10Mile-Mile'],
            race_paces[k]['HalfMarathon-KM'],
            race_paces[k]['HalfMarathon-Mile'],
            race_paces[k]['Marathon-KM'],
            race_paces[k]['Marathon-Mile'],
        ))

    with open('VDOT Training.txt', 'w') as training_file:
        training_file.writelines(vdot_lines)
