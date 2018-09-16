from __future__ import absolute_import

from django.conf.urls import url, include

from .api_views import add_service_area, update_service_area, delete_service_area, get_service_area, search


urlpatterns = [
    url(r'add', add_service_area, name='add a new service area '),
    url(r'update', update_service_area, name='add a new service area '),
    url(r'delete', delete_service_area, name='add a new service area '),
    url(r'get', get_service_area, name='add a new service area '),
    url(r'^search/', search, name='search coordinates'),

]

