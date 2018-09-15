import os
from apps.utilities.toolkit.funcs import get_random_id

# Use this module to define all the global variables that could be used in multiple modules
APP_NAME = os.path.basename(os.path.dirname(__file__))
TRUE_VALUES = ['t', 'T', 'true', 'True', 'TRUE', '1', 1, True]


def get_publisher_id():
    length = 30
    return get_random_id(length)


