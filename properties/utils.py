from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try to get existing cache
    if cache.get('all_properties'):
        return cache.get( 'all_properties' )
    query_set = Property.objects.all()
    cache.set('all_properties', query_set, 3600)
    return query_set

