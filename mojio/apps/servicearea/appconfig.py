from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ServiceAreaApp(AppConfig):
    name = 'apps.servicearea'
    test = True
    verbose_name = _('servicearea')

    def ready(self):
        super(ServiceAreaApp, self).ready()