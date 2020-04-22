from datetime import timedelta, datetime, date
import re
from awa.iplan._initial_setup import LATER_HRS, DISPLAY_EVENING_TILL_HOUR, DISPLAY_LATER_TILL_HOUR


class TimeLine:
    # List of all potential categories/choices.
    _now = 'Now'
    _later = 'Later Today'
    _thisweek = 'This Week'
    _nextweek = 'Next Week'
    _thismonth = 'This Month'
    _thisyear = 'This Year'
    categories = [_now, _later, _thisweek, _nextweek, _thismonth, _thisyear]

    # Timeline with warning indicators [(category, timeUoM, (warning, danger))]
    _progress_indidators = [(_now, 'h', (2, 6)),
                            (_later, 'h', (4, 8)),
                            (_thisweek, 'd', (2, 4)),
                            (_nextweek, 'w', (1, 3)),
                            (_thismonth, 'm', (1, 6)),
                            (_thisyear, 'm', (1, 6))]

    _progress_colors = {'attention': 'badge badge-secondary','warning': 'badge badge-warning', 'danger': 'badge badge-danger'}
    _seconds_in_unites = {'h': 3600, 'd': 24 * 3600, 'w': 7 * 24 * 3600, 'm': 30.416 * 24 * 3600}

    @staticmethod
    def selectfield_choices():
        """ Returns list of choices for SelectField. [(c1, c1), ... (cN, cN)]. """
        return [(x, x) for x in TimeLine.categories]

    @staticmethod
    def get_timeline_index(current_timeline):
        """ Returns positon (index) in timeline. Used for ordering task. """
        return TimeLine.categories.index(current_timeline)

    @staticmethod
    def move_in_timeline(current_timeline, direction):
        """ Returns new position in timeline depending on direction (right: next, left: previous). """
        index_timeline = TimeLine.categories.index(current_timeline)

        index_next = min(index_timeline + 1, len(TimeLine.categories) - 1)
        index_prev = max(index_timeline - 1, 0)

        if direction == 'next':
            return TimeLine.categories[index_next]
        elif direction == 'previous':
            return TimeLine.categories[index_prev]
        else:
            return current_timeline

    @staticmethod
    def progress_indicator(time_creation, timeline_category):
        for indicator in TimeLine._progress_indidators:
            if timeline_category == indicator[0]:  # Check on timeline category
                seconds_since_creation = (datetime.now()-time_creation).total_seconds()
                uom_since_creation = int(seconds_since_creation / TimeLine._seconds_in_unites[indicator[1]])
                if uom_since_creation >= indicator[2][0] and uom_since_creation < indicator[2][1]:
                    return f'{uom_since_creation}{indicator[1]}', TimeLine._progress_colors['attention']
                elif uom_since_creation >= indicator[2][1]:
                    return f'{uom_since_creation}{indicator[1]}', TimeLine._progress_colors['warning']
                else:
                    return None
                break


def reverse_dict(x):
    """ Applied for SelectField choices in updating forms
    Creates dict from list of tuples [(1,a), (9,z)] -> {a:1, z:9} """
    # todo - just to be sure, remove possibility of have 2 same values for 1 key (pick first one)
    return {v: k for (k, v) in dict(x).items()}


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
