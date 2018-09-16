"""A collection of functions that are used in different components of the application"""


from django.utils.crypto import get_random_string


def get_random_id(length):
    """
    The django method `get_random_string` returns only alphanumeric string. This has an advantage for
    us as we can perform certain string operations on special characters such as '/', '*', '&' as we
    know that these cannot be generated
    """

    return unicode(get_random_string(length))

