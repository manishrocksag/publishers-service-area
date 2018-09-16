from __future__ import absolute_import
import logging

from rest_framework.decorators import api_view
from django.http import HttpResponseBadRequest, JsonResponse
from haystack.query import SearchQuerySet


from .models import ServiceArea, GeoJSONType_Choices_MAPPING
from modules.publishers.models import Publisher


logger = logging.getLogger('apps.logs')


@api_view(['GET'])
def get_service_area(request):
    """
    Description: Returns the list of service areas associated with the given publisher.
    parameters:
      - name: publisher_id
        type: string
        required: true
        location: query
    """
    publisher_id = request.GET.get("publisher_id", None)
    if not publisher_id:
        return JsonResponse({"status": "failure", "error": "No publisher found"}, safe=False)
    else:
        try:
            publisher_instance = Publisher.objects.get(publisher_id=publisher_id)
            service_areas = ServiceArea.objects.filter(publisher=publisher_instance)
        except ServiceArea.DoesNotExist as e:
            logger.error(e)
            return JsonResponse({"status": "failure", "error": "No service areas found for given publisher"},
                                safe=False)

    result = []
    for item in service_areas:
        result.append({"publisher_name": item.publisher.name, "type": item.type, "name": item.name,
                       "coordinates": item.coordinates, "price": item.price, "service_area_id": item.id})

    return JsonResponse(result, safe=False)


@api_view(['PUT'])
def update_service_area(request):
    """
    Description: This api updates the service area for a given publisher.
    parameters:
      - name: service_area_id
        type: string
        required: true
        location: form
      - name: name
        type: string
        required: false
        location: form
      - name: type
        type: string
        required: false
        location: form
      - name: coordinates
        type: string
        required: false
        location: form
      - name: price
        type: string
        required: false
        location: form
    """
    name = request.POST.get("name", "")
    type = request.POST.get("type", "polygon")
    coordinates = request.POST.get("coordinates", "")
    price = request.POST.get("price", "")

    type = GeoJSONType_Choices_MAPPING[type.lower()]

    service_area_id = request.POST.get("service_area_id", None)

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


@api_view(['POST'])
def add_service_area(request):
    """
    Description: This api updates the service area for a given publisher.
    parameters:
      - name: publisher_id
        type: string
        required: true
        location: form
      - name: name
        type: string
        required: true
        location: form
      - name: type
        type: string
        required: true
        location: form
      - name: coordinates
        type: string
        required: true
        location: form
      - name: price
        type: string
        required: true
        location: form
    """
    publisher_id = request.POST.get("publisher_id", "")
    name = request.POST.get("name", "")
    coordinates = request.POST.get("coordinates", "")
    type = request.POST.get("type", "polygon")
    price = request.POST.get("price", "")

    mandatory_args = [publisher_id, name, coordinates, type]

    type = GeoJSONType_Choices_MAPPING[type.lower()]

    if not all(mandatory_args):
        raise JsonResponse({"status": "failure", "msg": "mandatory args missing"}, safe=False)

    publisher_instance = Publisher.objects.get(publisher_id=publisher_id)

    if publisher_instance:
        service_area_instance = ServiceArea(publisher=publisher_instance, name=name, coordinates=coordinates,
                                            type=type, price=price)
        service_area_instance.save()

        return JsonResponse({"status": "success", "service_area_id": service_area_instance.id}, safe=False)
    else:
        return JsonResponse({"status": "failure", "msg": "publisher does not exist"}, safe=False)


@api_view(['DELETE'])
def delete_service_area(request):
    """
    Description: Makes the given service area inactive.
    parameters:
      - name: service_area_id
        type: string
        required: true
        location: form
    """
    service_area_id = request.POST.get("service_area_id", None)

    if not service_area_id:
        return JsonResponse({"status": "failure", "msg": "service area does not exist."}, safe=False)

    try:
        servide_area_instance = ServiceArea.objects.get(id=service_area_id)
        servide_area_instance.is_active = False
        servide_area_instance.save()
        return JsonResponse({"status": "success", "msg": "service area deleted"}, safe=False)
    except ServiceArea.DoesNotExist as e:
        logger.error(e)
        return JsonResponse({"status": "failure", "msg": "service area does not exist"}, safe=False)


@api_view(['GET'])
def search(request):
    """
    Description: Makes the given service area inactive.
    parameters:
      - name: q
        type: string
        required: true
        location: query
    """
    search_query = request.GET.get("q", None)
    if not search_query:
        raise JsonResponse({"status": "failure", "msg": "No query params"}, safe=False)

    search_instance = SearchQuerySet().autocomplete(content_auto=search_query)[:5]

    try:
        search_results = map(lambda x: x.object.coordinates, search_instance)
        response = {"results": search_results}
        return JsonResponse(response)
    except Exception:
        JsonResponse({"status": "failure", "msg": "an exception occured"}, safe=False)
