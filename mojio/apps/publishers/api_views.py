from __future__ import absolute_import
import logging

from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.views import APIView

from .models import Publisher
from .utils import get_publisher_id


logger = logging.getLogger('apps.logs')


class PublisherAPIView(APIView):

    def get(self, request, publisher_id):
        if not publisher_id:
            publishers = Publisher.objects.filter(is_active=True)
        else:
            try:
                publishers = [Publisher.objects.get(publisher_id=publisher_id)]
            except Publisher.DoesNotExist as e:
                logger.error(e)
                return JsonResponse({"status": "failure", "error": "No publisher found"})

        result = []
        for item in publishers:
            result.append({"name": item["name"], "email": item["email"], "phone_number": item["phone_number"],
                           "language": item["language"], "currency": item["currency"]})

        return JsonResponse(result)

    def put(self, request, publisher_id):
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone_number = request.POST.get("phone_number", "")
        currency = request.POST.get("currency", "")
        language = request.POST.get("language", "")

        try:
            publisher_obj = Publisher.objects.get(publisher_id=publisher_id)
            if publisher_obj:
                if name:
                    publisher_obj.name = name
                if email:
                    publisher_obj.email = email
                if phone_number:
                    publisher_obj.phone_number = phone_number
                if currency:
                    publisher_obj.currency = currency
                if language:
                    publisher_obj.currency = currency
                publisher_obj.save()
                return JsonResponse({"status": "success", "error": "publisher records updated."})
            return JsonResponse({"status": "failure", "error": "No publisher found"})
        except Publisher.DoesNotExist as e:
            logger.error(e)
            return JsonResponse({"status": "failure", "error": "No publisher found"})

    def delete(self, request, publisher_id):
        if not publisher_id:
            return HttpResponseBadRequest()
        try:
            publisher_obj = Publisher.objects.get(publisher_id=publisher_id)
            publisher_obj.is_active = False
            publisher_obj.save()
            return JsonResponse({"status": "success", "msg": "publisher deleted"})
        except Publisher.DoesNotExist as e:
            logger.error(e)
            return JsonResponse({"status": "failure", "msg": "publisher does not exist"})

    def post(self, request):
        """
            Create a new publisher.
        """
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone_number = request.POST.get("phone_number", "")
        currency = request.POST.get("currency", "")
        language = request.POST.get("language", "")

        mandatory_args = [name, email, phone_number, currency, language]

        if not all(mandatory_args):
            raise HttpResponseBadRequest()

        publisher_id = get_publisher_id()

        publisher_obj = Publisher(publisher_id=publisher_id, name=name, email=email, phone_number=phone_number, currency=currency, language=language)
        publisher_obj.save()

        return JsonResponse({"status": "success", "publisher_id": publisher_obj.publisher_id})


publisher = Publisher.as_view()
