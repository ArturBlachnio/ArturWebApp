from datetime import datetime

# Choices for SelectFiles
STRATEGY_CATEGORY_CHOICES = [(1, 'Strategic'), (2, 'Productive'), (3, 'Untracked')]

TASK_CATEGORY_CHOICES = [(1, 'Action'), (2, 'Learning'), (3, 'Idea')]
TASK_FREQUENCY_CHOICES = [(1, 'OneTime'), (2, 'Repeatable')]

PROJECT_CATEGORY_CHOICES = [(1, 'Project'), (2, 'Learning'), (3, 'Idea')]


# Timeline management
POSTPONE_HOURS = 2
POSTPONE_DAYS = 1

# LATER_HRS = 4
# DISPLAY_LATER_TILL_HOUR = 22  # After 19:00 Later timeline will not be displayed at all
# DISPLAY_EVENING_TILL_HOUR = 20  # After 20:00 evening timeline will not be displayed at all
