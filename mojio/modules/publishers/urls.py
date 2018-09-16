from __future__ import absolute_import

from django.conf.urls import url

from .api_views import add_publisher, update_publisher, get_publishers, delete_publisher

urlpatterns = [
    url(r'add', add_publisher, name='add a new publisher'),
    url(r'update', update_publisher, name='update a new publisher'),
    url(r'delete', delete_publisher, name='delete a new publisher'),
    url(r'get', get_publishers, name='get the publisher list'),
]

