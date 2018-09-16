from __future__ import absolute_import
import logging

from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view
from django.db import IntegrityError


from .models import Publisher, LANGUAGE_CHOICES_MAPPING, CURRENCY_CHOICES_MAPPING
from .utils import get_publisher_id


logger = logging.getLogger('apps.logs')


@api_view(['GET'])
def get_publishers(request):
    """
    Description: This api queries a publisher. If no publisher id is passed it returns the list of all the
                 publishers. If a publisher id is passed it returns that particular publisher.
    parameters:
      - name: publisher_id
        type: string
        required: false
        location: query
    """
    publisher_id = request.GET.get("publisher_id", None)
    if not publisher_id:
        publishers = Publisher.objects.filter(is_active=True)
    else:
        try:
            publishers = [Publisher.objects.get(publisher_id=publisher_id)]
        except Publisher.DoesNotExist as e:
            logger.error(e)
            return JsonResponse({"status": "failure", "error": "No publisher found"}, safe=False)

    result = []
    for item in publishers:
        result.append({"name": item.name, "email": item.email, "phone_number": item.phone_number,
                       "language": item.language, "currency": item.currency, "publisher_id": item.publisher_id})

    return JsonResponse(result, safe=False)


@api_view(['POST'])
def add_publisher(request):
    """
        Description: Creates a new publisher.
        parameters:
          - name: name
            type: string
            required: true
            location: form
          - name: email
            type: string
            required: true
            location: form
          - name: phone_number
            type: string
            required: true
            location: form
          - name: currency
            type: string
            required: true
            location: form
          - name: language
            type: string
            required: true
            location: form
    """
    name = request.POST.get("name", "")
    email = request.POST.get("email", "")
    phone_number = request.POST.get("phone_number", "")
    currency = request.POST.get("currency", "usd")
    language = request.POST.get("language", "en")

    currency = CURRENCY_CHOICES_MAPPING[currency.lower()]
    language = LANGUAGE_CHOICES_MAPPING[language.lower()]

    mandatory_args = [name, email, phone_number, currency, language]

    if not all(mandatory_args):
        JsonResponse({"status": "failure", "error": "mandatory args missing"}, safe=False)

    publisher_id = get_publisher_id()

    publisher_obj = Publisher(publisher_id=publisher_id, name=name, email=email, phone_number=phone_number,
                              currency=currency, language=language)

    try:
        publisher_obj.save()
    except IntegrityError as e:
        logger.error(e)
        return JsonResponse({"status": "failure", "error": "record already exists"}, safe=False)

    return JsonResponse({"status": "success", "publisher_id": publisher_obj.publisher_id}, safe=False)


@api_view(['PUT'])
def update_publisher(request):
    """
        Description: Updates a publisher data if any field is passed.
        parameters:
          - name: publisher_id
            type: string
            required: true
            location: form
          - name: name
            type: string
            required: false
            location: form
          - name: email
            type: string
            required: false
            location: form
          - name: phone_number
            type: string
            required: false
            location: form
          - name: currency
            type: string
            required: false
            location: form
          - name: language
            type: string
            required: false
            location: form
    """
    name = request.POST.get("name", "")
    email = request.POST.get("email", "")
    phone_number = request.POST.get("phone_number", "")
    currency = request.POST.get("currency", "")
    language = request.POST.get("language", "")

    publisher_id = request.POST.get("publisher_id", None)

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
                currency = CURRENCY_CHOICES_MAPPING[currency.lower()]
                publisher_obj.currency = currency
            if language:
                language = LANGUAGE_CHOICES_MAPPING[language.lower()]
                publisher_obj.language = language
            publisher_obj.save()
            return JsonResponse({"status": "success", "error": "publisher records updated."}, safe=False)
        return JsonResponse({"status": "failure", "error": "No publisher found"}, safe=False)
    except Publisher.DoesNotExist as e:
        logger.error(e)
        return JsonResponse({"status": "failure", "error": "No publisher found"}, safe=False)


@api_view(['DELETE'])
def delete_publisher(request):
    """
            Description: This API deletes a publisher. IT does not perform hard deletion. It sets is_active field of the
                publisher to false.
            parameters:
              - name: publisher_id
                type: string
                required: true
                location: form
            """
    publisher_id = request.POST.get("publisher_id", None)

    if not publisher_id:
        return JsonResponse({"status": "failure", "error": "No publisher id found"}, safe=False)
    try:
        publisher_obj = Publisher.objects.get(publisher_id=publisher_id)
        publisher_obj.is_active = False
        publisher_obj.save()
        return JsonResponse({"status": "success", "msg": "publisher deleted"}, safe=False)
    except Publisher.DoesNotExist as e:
        logger.error(e)
        return JsonResponse({"status": "failure", "msg": "publisher does not exist"}, safe=False)












































