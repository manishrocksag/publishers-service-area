from __future__ import absolute_import
import logging


from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.views import APIView

from .models import ServiceArea
from modules.publishers.models import Publisher


logger = logging.getLogger('apps.logs')


class ServiceAreaAPIView(APIView):

    def get(self, request, **wkargs):
        publisher_id = request.GET.get("publisher_id", None)
        if not publisher_id:
            return JsonResponse({"status": "failure", "error": "No publisher found"}, safe=False)
        else:
            try:
                publisher_instance = Publisher.objects.get(publisher_id=publisher_id)
                service_areas = ServiceArea.objects.filter(publisher=publisher_instance)
            except ServiceArea.DoesNotExist as e:
                logger.error(e)
                return JsonResponse({"status": "failure", "error": "No service areas found for given publisher"}, safe=False)

        result = []
        for item in service_areas:
            result.append({"publisher_name": item.publisher["name"], "type": item["type"], "name": item["name"],
                           "coordinates": item["coordinates"], "price": item["price"]})

        return JsonResponse(result, safe=False)

    def put(self, request, **kwags):
        name = request.PUT.get("name", "")
        type = request.PUT.get("type", "")
        coordinates = request.PUT.get("coordinates", "")
        price = request.PUT.get("price", "")

        service_area_id = request.PUT.get("service_area_id", None)

        try:
            service_area_instance = ServiceArea.objects.get(id=service_area_id)
            if service_area_instance:
                if name:
                    service_area_instance.name = name
                if type:
                    service_area_instance.type = type
                if coordinates:
                    service_area_instance.phone_number = coordinates
                if price:
                    service_area_instance.currency = price

                service_area_instance.save()
                return JsonResponse({"status": "success", "error": "service area records updated."}, safe=False)
            return JsonResponse({"status": "failure", "error": "No service area found"}, safe=False)
        except ServiceArea.DoesNotExist as e:
            logger.error(e)
            return JsonResponse({"status": "failure", "error": "No publisher found"}, safe=False)

    def delete(self, request, **kwargs):
        service_area_id = request.DELETE.get("service_area_id", None)

        if not service_area_id:
            return HttpResponseBadRequest()
        try:
            servide_area_instance = ServiceArea.objects.get(id=service_area_id)
            servide_area_instance.is_active = False
            servide_area_instance.save()
            return JsonResponse({"status": "success", "msg": "service area deleted"}, safe=False)
        except ServiceArea.DoesNotExist as e:
            logger.error(e)
            return JsonResponse({"status": "failure", "msg": "service area does not exist"}, safe=False)

    def post(self, request):
        """
            Create a new service area.
        """
        publisher_id = request.POST.get("publisher_id", "")
        name = request.POST.get("name", "")
        coordinates = request.POST.get("coordinates", "")
        type = request.POST.get("type", "")
        price = request.POST.get("price", "")

        mandatory_args = [publisher_id, name, coordinates, type]

        if not all(mandatory_args):
            raise HttpResponseBadRequest()

        publisher_instance = Publisher.objects.get(publisher_id=publisher_id)

        if publisher_instance:
            service_area_instance = ServiceArea(publisher=publisher_instance, name=name, coordinates=coordinates,
                                                type=type, price=price)
            service_area_instance.save()

            return JsonResponse({"status": "success", "service_area_id": service_area_instance.id}, safe=False)
        else:
            return JsonResponse({"status": "failure", "msg": "publisher does not exist"}, safe=False)


servicearea = ServiceAreaAPIView.as_view()

