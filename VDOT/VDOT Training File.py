from collections import OrderedDict
from settings.converters import convert_to_time, calculate_pace

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


if __name__ == '__main__':
    vdots = get_vdot_race_paces_EMT()
    vdots_ir = get_vdot_race_paces_IR()

    #print(vdots)
    #print(vdots_ir)

    vdot_lines = [
        'VDOT Easy-KM Easy-Mile Long-KM Long-Mile Marathon-KM Marathon-Mile Threshold-400 Threshold-KM Threshold-Mile' +
        ' Interval400 IntervalKM Interval1200 IntervalM' +
        ' Repetition200 Repetition300 Repetition400 Repetition600 Repetition800 Interval-Pace\n'
    ]

    for k, v in vdots.items():
        line = '{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'
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
            vdots_ir[k]['Interval400'],
            vdots_ir[k]['IntervalKM'],
            vdots_ir[k]['Interval1200'],
            vdots_ir[k]['IntervalM'],
            vdots_ir[k]['Repetition200'],
            vdots_ir[k]['Repetition300'],
            vdots_ir[k]['Repetition400'],
            vdots_ir[k]['Repetition600'],
            vdots_ir[k]['Repetition800'],
            calculate_pace(convert_to_time(vdots_ir[k]['Interval400']), 400, 'metre', 'mile')
        ))

    with open('VDOT Training.txt', 'w') as training_file:
        training_file.writelines(vdot_lines)
