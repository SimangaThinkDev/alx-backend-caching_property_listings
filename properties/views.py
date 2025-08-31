from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Property
from .serializers import PropertySerializer
from django.http import JsonResponse
from .utils import get_all_properties

# Create your views here.
""" # Notes from docs

IMPORTS:
from django.views.decorators.cache import cache_page

SET_UP -> settings.py

'
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}
' # Less secure as it does not require secrets in the LOCATION atrr

ANNOTATIONS:
# Syntax for annotations, cache page takes a single argument
# Arg1 -> the cache timeout in seconds
# This one is specifically written as 60 * 15 for readability
@cache_page(60 * 15)
def my_view(request): ...

# cache_page can also take an optional keyword argument, 
# cache, which directs the decorator to use a specific 
# cache (from your CACHES setting) when caching view results. 
# By default, the default cache will be used, but you can 
# specify any cache you want:

e.g. -> @cache_page(60 * 15, cache="special_cache")



"""


@api_view(['GET'])
@cache_page(60 * 15)
def property_list(request):
    """
    Returns a list of all properties.
    """
    properties = get_all_properties()
    serializer = PropertySerializer(properties, many=True)
    return JsonResponse({"properties": serializer.data})
