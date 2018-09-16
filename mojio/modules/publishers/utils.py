"""A collection of functions that are used in different components of the application"""

import os
from django.utils.crypto import get_random_string

# Use this module to define all the global variables that could be used in multiple modules
APP_NAME = os.path.basename(os.path.dirname(__file__))
TRUE_VALUES = ['t', 'T', 'true', 'True', 'TRUE', '1', 1, True]


def get_random_id(length):
    """
    The django method `get_random_string` returns only alphanumeric string. This has an advantage for
    us as we can perform certain string operations on special characters such as '/', '*', '&' as we
    know that these cannot be generated
    """

    return unicode(get_random_string(length))


# get a randomly generated publisher id
def get_publisher_id():
    length = 30
    return get_random_id(length)


