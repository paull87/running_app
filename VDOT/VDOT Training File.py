from collections import OrderedDict
from settings.converters import convert_to_time, calculate_pace, time_to_string

def get_vdot_race_paces_EMT():
    """Extracts the race paces from the VDOT Races file."""
    VDOT = OrderedDict()
    headers = []
    with open('VDOT EMT.txt', 'r') as VDOT_file:
        for line in VDOT_file.readlines():
            cells = line.split() # Ignore last column as this is repeated.
            if cells[0] == 'VDOT':
                headers += cells[1:]
            else:
                cell_times = [x for x in cells[1:]]
                VDOT[int(cells[0])] = dict(zip(headers, cell_times))

    return VDOT

def get_vdot_race_paces_IR():
    """Extracts the race paces from the VDOT Races file."""
    VDOT = OrderedDict()
    headers = []
    with open('VDOT IR.txt', 'r') as VDOT_file:
        for line in VDOT_file.readlines():
            cells = line.split()  # Ignore last column as this is repeated.
            if cells[-1] == 'VDOT':
                headers += cells[:-1]
            else:
                cell_times = [x for x in cells[:-1]]
                VDOT[int(cells[-1])] = dict(zip(headers, cell_times))

    return VDOT


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
    vdots = get_vdot_race_paces_EMT()
    vdots_ir = get_vdot_race_paces_IR()

    vdot_lines = [
        'VDOT Easy-KM Easy-Mile Long-KM Long-Mile Marathon-KM Marathon-Mile Threshold-400 Threshold-KM Threshold-Mile' +
        # ' Interval400 IntervalKM Interval1200 IntervalM' +
        # ' Repetition200 Repetition300 Repetition400 Repetition600 Repetition800' +
        ' Interval-KM Interval-Mile Repetition-KM Repetition-Mile\n'
    ]

    line = ' '.join(['{}'] * len(vdot_lines[0].split())) + '\n'

    for k, v in vdots.items():
        vdot_lines.append(line.format(
            k,
            v['Easy/LongKM'].split('-')[0],
            v['Easy/LongM'].split('-')[0],
            v['Easy/LongKM'].split('-')[1],
            v['Easy/LongM'].split('-')[1],
            v['MarathonKM'],
            v['MarathonM'],
            v['Threshold400'],
            v['ThresholdKM'],
            v['ThresholdM'],
            #vdots_ir[k]['Interval400'],
            #vdots_ir[k]['IntervalKM'],
            #vdots_ir[k]['Interval1200'],
            #vdots_ir[k]['IntervalM'],
            #vdots_ir[k]['Repetition200'],
            #vdots_ir[k]['Repetition300'],
            #vdots_ir[k]['Repetition400'],
            #vdots_ir[k]['Repetition600'],
            #vdots_ir[k]['Repetition800'],
            get_interval_time(vdots_ir[k], 'mile'),
            get_interval_time(vdots_ir[k], 'km'),
            get_repetition_time(vdots_ir[k], 'mile'),
            get_repetition_time(vdots_ir[k], 'km')
        ))

    with open('VDOT Training.txt', 'w') as training_file:
        training_file.writelines(vdot_lines)
