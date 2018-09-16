from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PublishersApp(AppConfig):
    name = 'modules.publishers'
    test = True
    verbose_name = _('publishers')

    def ready(self):
        super(PublishersApp, self).ready()