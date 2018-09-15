from __future__ import absolute_import
import logging
import json

from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.views import APIView

from .models import ServiceArea
from .utils import get_publisher_id


logger = logging.getLogger('apps.logs')


class ServiceAreaAPIView(APIView):

    def get(self, request, **wkargs):
        pass

    def put(self, request, **kwags):
        pass

    def delete(self, request, **kwargs):
        pass

    def post(self, request):
        """
            Create a new publisher.
        """
        pass


publisher = PublisherAPIView.as_view()
