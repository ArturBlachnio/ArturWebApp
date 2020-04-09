from datetime import timedelta, datetime, date
import re


def reverse_dict(x):
    """ Applied for SelectField choices in updating forms
    Creates dict from list of tuples [(1,a), (9,z)] -> {a:1, z:9} """
    # todo - just to be sure, remove possibility of have 2 same values for 1 key (pick first one)
    return {v: k for (k, v) in dict(x).items()}


def generate_fields_for_timeline(_testing_days_up=0):
    """ Returns choices for time_line SelectField.
    Shape: [(datetime1, category1), (datetimeN, categoryN)]
    """
    categories = ['Today', 'Tomorrow', 'In two days', 'Next week', 'Next month', 'This year', 'Unspecified']
    today = date.today() + timedelta(days=_testing_days_up)
    _today = (today, 'Today')
    _tomorrow = (today + timedelta(days=1), 'Tomorrow')
    _in2days = (today + timedelta(days=2), f'On {(today + timedelta(days=2)).strftime("%A")}')

    # _nextweek must be at least 1day later then _in2days
    _nextweek = (today + timedelta(days=8-today.isoweekday()), 'Next week')
    if _nextweek[0] <= _in2days[0]:
        _nextweek = (_in2days[0] + timedelta(days=1), _nextweek[1])

    # _nextmonth must be at least in next month counting from _nextweek
    if today.month == 12:
        _nextmonth = (date(year=today.year+1, month=1, day=1), 'Next month')
    else:
        _nextmonth = (date(year=today.year, month=today.month+1, day=1), 'Next month')
    if _nextmonth[0] <= _nextweek[0]:
        if today.month == 12:
            _nextmonth = (date(year=today.year + 1, month=2, day=1), _nextmonth[1])
        else:
            _nextmonth = (date(year=today.year, month=today.month+2, day=1), _nextmonth[1])

    # _thisyear - last day in this year
    _thisyear = (date(year=today.year+1, month=1, day=1)-timedelta(days=1), 'This year')

    # _nextyear - last day in this year
    _nextyear = (date(year=today.year+2, month=1, day=1)-timedelta(days=1), 'Next year')

    choices = [_today, _tomorrow, _in2days, _nextweek, _nextmonth, _thisyear, _nextyear]
    ordinal_choices = [(item[0].toordinal(), item[1]) for item in choices]
    return ordinal_choices


def timeline_ranges(_testing_days_up=0):
    a = [(date(year=1970, month=1, day=1).toordinal(), 'Today')]
    a.extend(generate_fields_for_timeline(_testing_days_up)[1:])
    a.append(((date(year=date.today().year+1000, month=1, day=1)-timedelta(days=1)).toordinal(), '100 years from now'))
    ranges = []
    for i in range(len(a)-1):
        ranges.append((a[i][0], a[i+1][0], a[i][1]))
    return ranges

# for i in range(270, 275):
#     print(i)
#     generate_fields_for_timeline(i)
# generate_fields_for_timeline()

def duration_from_string(x):
    """ Converts string to valid datatime.timedelta
    Valid string format examples: 3d, 10h 5m, 1h 3s, 30m2s, etc
    - Each value must be followed by d-day, h-hour, m-minute, s-second
    - Sequence is not important: 1h 30m = 30m 1h
    """
    if x is None:
        return timedelta(0)

    # Dict of period: value pairs: {'h': '3', 'd': '4', 'm': '30', 's': '22'}
    duration_dict = dict(zip(re.findall('[dhms]', x), re.findall('\d+', x)))
    days = int(duration_dict.get('d', 0))
    hours = int(duration_dict.get('h', 0))
    minutes = int(duration_dict.get('m', 0))
    seconds = int(duration_dict.get('s', 0))
    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)


def string_from_duration(x):
    """ Converts datatime.timedelta into string
    Function is used to update plan and actual of task model
    """
    if x is None or x.total_seconds() == 0:
        return '0h 0m'

    total_seconds = x.total_seconds()
    days = total_seconds // 86400
    total_seconds -= days * 86400
    hours = total_seconds // 3600
    total_seconds -= hours * 3600
    minutes = total_seconds // 60
    total_seconds -= minutes * 60
    seconds = total_seconds

    outcome = ''
    for item in [(days, 'd'), (hours, 'h'), (minutes, 'm'), (seconds, 's')]:
        if item[0] != 0:
            outcome += f'{int(item[0])}{item[1]} '
    return outcome[:-1]


def reorder_tasks(direction, task_id, current_order_of_ids):
    """ Takes current task id and ids of all other tasks (in scope) and returns dict or id and new order
    If task_id not in list, returns same order_of_list
    Directions can be:
    up - move one position up
    down - move one position down
    top - move to the beginning
    bottom - move to the end
    """
    if task_id not in current_order_of_ids:
        return current_order_of_ids

    task_index = current_order_of_ids.index(task_id)

    new_order = current_order_of_ids.copy()
    new_order.pop(task_index)

    if direction == 'up':
        # If gets to -1 it's getting from end of list
        new_order.insert(max(0, task_index - 1), task_id)
    elif direction == 'down':
        # Can not get higher than lenght of list
        new_order.insert(min((len(new_order)), task_index + 1), task_id)
    elif direction == 'top':
        new_order.insert(0, task_id)
    elif direction == 'bottom':
        new_order.insert(len(new_order), task_id)
    else:
        new_order.insert(task_index, task_id)

    outcome_order = []
    for i in current_order_of_ids:
        outcome_order.append(new_order.index(i))
    return outcome_order
