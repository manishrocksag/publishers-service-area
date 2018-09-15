from __future__ import absolute_import

from django.conf.urls import url

from .api_views import publisher

urlpatterns = [
    url(r'^publisher', publisher, name='publisher apis'),
]

