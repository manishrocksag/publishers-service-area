from __future__ import absolute_import

from django.conf.urls import url

from .api_views import servicearea


urlpatterns = [
    url(r'', servicearea, name='service area apis apis'),

]

