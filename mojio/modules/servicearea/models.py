# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from jsonfield import JSONField

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


class GeoJSONType(object):
    Point = 0
    LineString = 1
    Polygon = 2
    Feature = 3


GeoJSONType_Choices = (
    (GeoJSONType.Point, _('point')),
    (GeoJSONType.LineString, _("linestring")),
    (GeoJSONType.Polygon, _("polygon")),
    (GeoJSONType.Feature, _("feature")),

)

GeoJSONType_Choices_MAPPING = {}
for item in GeoJSONType_Choices:
    GeoJSONType_Choices_MAPPING[str(item[1])] = item[0]


@python_2_unicode_compatible
class ServiceArea(models.Model):
    """
        Defines a service area for a given publisher. A publisher can contain multiple service areas.
    """

    publisher = models.ForeignKey(
        'publishers.Publisher',
        verbose_name=_('Reference to the publisher table'),
    )
    name = models.CharField(_('name'), max_length=254)
    type = models.IntegerField(choices=GeoJSONType_Choices, default=2)
    coordinates = JSONField(default=dict, verbose_name=_('coordinates of the data type defined'))
    date_created = models.DateTimeField(_('date joined'), default=timezone.now)
    price = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this publisher should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))

    class Meta:
        verbose_name = _('Service Area')
        verbose_name_plural = _('Service Areas')

    def __str__(self):
        return self.coordinates

