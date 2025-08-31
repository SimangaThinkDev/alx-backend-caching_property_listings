from django.core.cache import cache
from .models import Property
from redis_cache import get_redis_connection
import logging



def get_all_properties():
    # Try to get existing cache
    if cache.get('all_properties'):
        return cache.get( 'all_properties' )
    query_set = Property.objects.all()
    cache.set('all_properties', query_set, 3600)
    return query_set


logger = logging.getLogger(__name__) # Gets the logger for the current module

def get_redis_cache_metrics():
    """
    Connects to Redis, gets keyspace metrics, calculates the hit ratio,
    logs the metrics, and returns a dictionary.
    """
    try:
        # Connect to Redis using the 'default' cache alias
        redis_conn = get_redis_connection("default")
        
        # Get keyspace hits and misses from the INFO command
        info = redis_conn.info("Keyspace")
        
        # Extract the metrics
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate the hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = 0.0
        if total_requests > 0:
            hit_ratio = keyspace_hits / total_requests
            
        # Log the metrics
        logger.info(f"Redis Keyspace Hits: {keyspace_hits}")
        logger.info(f"Redis Keyspace Misses: {keyspace_misses}")
        logger.info(f"Redis Hit Ratio: {hit_ratio:.2f}")

        # Return the metrics as a dictionary
        return {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'hit_ratio': round(hit_ratio, 2),
        }

    except Exception as e:
        logger.error(f"Error getting Redis metrics: {e}")
        return {
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'hit_ratio': 0.0,
            'error': str(e)
        }
