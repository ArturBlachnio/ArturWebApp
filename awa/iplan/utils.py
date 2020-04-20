from datetime import timedelta, datetime, date
import re
from awa.iplan._initial_setup import LATER_HRS, DISPLAY_EVENING_TILL_HOUR, DISPLAY_LATER_TILL_HOUR

"""
timeline_category - Now, Later (+xh), in the evening,...
timeline_timestamp - datetime.timestamps for a given timeline_category 
"""

def reverse_dict(x):
    """ Applied for SelectField choices in updating forms
    Creates dict from list of tuples [(1,a), (9,z)] -> {a:1, z:9} """
    # todo - just to be sure, remove possibility of have 2 same values for 1 key (pick first one)
    return {v: k for (k, v) in dict(x).items()}


def generate_fields_for_timeline(_testing_days_up=0, LATER_HRS=LATER_HRS):
    """ Returns choices for time_due SelectField.
    Shape: [(datetime1, category1), (datetimeN, categoryN)]
    """
    today = datetime.fromordinal(date.today().toordinal()) + timedelta(days=_testing_days_up)
    _now = datetime.now()
    _today = (today, 'Now')

    # LATER_HRS after 20.00 will be adjusted to not go for next day (e.g. if it's 22.00 it will be 23.59)
    if 24 - LATER_HRS <= _now.hour:
        LATER_HRS = 24 - _now.hour - 1
    _later = (datetime(year=_now.year, month=_now.month, day=_now.day, hour=_now.hour) + timedelta(hours=LATER_HRS), f'Later (+{LATER_HRS}h)')
    _evening = (today + timedelta(hours=20), 'In the evening')
    _tomorrow = (today + timedelta(days=1), 'Tomorrow')
    _in2days = (today + timedelta(days=2), f'On {(today + timedelta(days=2)).strftime("%A")}')

    # _nextweek must be at least 1day later then _in2days
    _nextweek = (today + timedelta(days=8-today.isoweekday()), 'Next week')
    if _nextweek[0] <= _in2days[0]:
        _nextweek = (_in2days[0] + timedelta(days=1), _nextweek[1])

    # _nextmonth must be at least in next month counting from _nextweek
    if today.month == 12:
        _nextmonth = (datetime(year=today.year+1, month=1, day=1), 'Next month')
    else:
        _nextmonth = (datetime(year=today.year, month=today.month+1, day=1), 'Next month')
    if _nextmonth[0] <= _nextweek[0]:
        if today.month == 12:
            _nextmonth = (datetime(year=today.year + 1, month=2, day=1), _nextmonth[1])
        else:
            _nextmonth = (datetime(year=today.year, month=today.month+2, day=1), _nextmonth[1])

    # _thisyear - last day in this year
    _thisyear = (datetime(year=today.year+1, month=1, day=1)-timedelta(days=1), 'This year')

    # _nextyear - last day in this year
    _nextyear = (datetime(year=today.year+2, month=1, day=1)-timedelta(days=1), 'Next year')

    choices = [_today, _later, _evening, _tomorrow, _in2days, _nextweek, _nextmonth, _thisyear, _nextyear]
    # Do not display _later and _evening choices if they are not displayed anymote (in function timeline_ranges)
    if datetime.now().hour > DISPLAY_LATER_TILL_HOUR:
        choices.remove(_later)
    if datetime.now().hour > DISPLAY_EVENING_TILL_HOUR:
        choices.remove(_evening)
    timestamp_choices = [(int(item[0].timestamp()), item[1]) for item in choices]
    return timestamp_choices

# for item in generate_fields_for_timeline():
#     print(item, datetime.fromtimestamp(item[0]))


def timeline_ranges(_testing_days_up=0):
    """ Used in timeline.html. Displays timeline divs and checks if task belongs to category. """
    a = [(int(datetime(year=1980, month=1, day=1).timestamp()), 'Now')]
    a.extend(generate_fields_for_timeline(_testing_days_up)[1:])
    a.append((int(datetime(year=date.today().year+100, month=1, day=1).timestamp()), '100 years from now'))
    # Between _now & _later: replace 'till moment'  with datetime.now()
    # Do not display at all after 19:00
    if datetime.now().hour < DISPLAY_LATER_TILL_HOUR:
        a[1] = (int((datetime.now()).timestamp()), a[1][1])
    else:
        for i, item in enumerate(a):
            if item[1] == f'Later (+{LATER_HRS}h)':
                a.pop(i)
                break

    # Between _later & _evening: replace 'till moment'  with max(datetime.now() & 20:00).
    # Do not display at all after 20:00
    if datetime.now().hour < DISPLAY_EVENING_TILL_HOUR:
        a[2] = (max(a[2][0], int((datetime.now()).timestamp())), a[2][1])
    else:
        for i, item in enumerate(a):
            if item[1] == 'In the evening':
                a.pop(i)
                break
    # Make from-to-name tuples
    ranges = []
    for i in range(len(a)-1):
        ranges.append((a[i][0], a[i+1][0], a[i][1]))
    return ranges


def get_index_in_timeline_for_current_task(current_timeline):
    """ Returns index of (displayed) timeline. Used to order tasks."""
    # Get index of current timeline
    index_timeline = 0
    for i, time_range in enumerate(timeline_ranges()):
        if current_timeline.timestamp() >= time_range[0] and current_timeline.timestamp() < time_range[1]:
            index_timeline = i
            break
    return index_timeline

def get_timestamp_for_timeline_category(timeline_category='Now'):
    """ Used to create New Task with preassigned timeline_category (e.g Now, Later (+4h).
    Returns datetime.timestamp for given timeline_category as used in SelectField"""

    timeline_timestamp = None

    for item in generate_fields_for_timeline():
        if item[1] == timeline_category:
            timeline_timestamp = item[0]
    return timeline_timestamp


def get_moment_in_timeline(current_timeline, direction='next'):
    """ Returns task new position (as datetime) on timeline depending on direction (right: next, left: previous).
    """
    # Get index of current timeline
    index_timeline = get_index_in_timeline_for_current_task(current_timeline=current_timeline)

    index_next = min(index_timeline + 1, len(timeline_ranges())-1)
    index_prev = max(index_timeline - 1, 0)

    # For testing
    # print('current:', index_timeline, datetime.fromtimestamp(timeline_ranges()[index_timeline][0]), datetime.fromtimestamp(timeline_ranges()[index_timeline][1]))
    # print('next:', index_next, datetime.fromtimestamp(timeline_ranges()[index_next][0]), datetime.fromtimestamp(timeline_ranges()[index_next][1]))
    # print('prev:', index_prev, datetime.fromtimestamp(timeline_ranges()[index_prev][0]), datetime.fromtimestamp(timeline_ranges()[index_prev][1]))

    # Return last possible time minus 1 minute
    if direction == 'next':
        return datetime.fromtimestamp(timeline_ranges()[index_next][1]) - timedelta(minutes=1)
    elif direction == 'previous':
        return datetime.fromtimestamp(timeline_ranges()[index_prev][1]) - timedelta(minutes=1)
    else:
        return datetime.now()

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

    # Compact display: if nb of none-zero items > 2 than drop seconds.
    duration_items = [(days, 'd'), (hours, 'h'), (minutes, 'm'), (seconds, 's')]
    non_zero_items = 0
    for item in duration_items:
        if item[0] != 0:
            non_zero_items += 1

    if non_zero_items > 2:
        duration_items.pop(-1)

    # Final output
    outcome = ''
    for item in duration_items:
        if item[0] != 0:
            outcome += f'{int(item[0])}{item[1]} '
    return outcome[:-1]


def reorder_tasks(direction, task_id, current_order_of_ids):
    """ Takes current task id plus ids of all other tasks (in scope) and returns dict of id and new order
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
    for task_id in current_order_of_ids:
        outcome_order.append(new_order.index(task_id))
    return outcome_order
