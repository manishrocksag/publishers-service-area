"""A collection of functions that are used in different components of the application"""

import pytz
from datetime import datetime

from django.utils.crypto import get_random_string


def get_random_id(length):
    """
    The django method `get_random_string` returns only alphanumeric string. This has an advantage for
    us as we can perform certain string operations on special characters such as '/', '*', '&' as we
    know that these cannot be generated
    """

    return unicode(get_random_string(length))


def epoch_to_utc(ts):
    """Given epoch should be in seconds"""
    utc = pytz.timezone('utc')
    epoch_utc = utc.localize(datetime.utcfromtimestamp(ts))
    return epoch_utc


def utc_to_epoch(dt):
    """Return epoch time of given datetime"""
    epoch_dt = datetime.utcfromtimestamp(0)
    utc = pytz.timezone('utc')
    epoch_utc = utc.localize(epoch_dt)
    return (dt - epoch_utc).total_seconds()


def iso_8601_to_utc(iso_str):
    """Convert ISO 8601 string to python datetime"""
    dt_obj = datetime.strptime(iso_str,
                               "%Y-%m-%dT%H:%M:%S.%fZ")
    utc = pytz.timezone('utc')
    utc_obj = utc.localize(dt_obj)
    return utc_obj
