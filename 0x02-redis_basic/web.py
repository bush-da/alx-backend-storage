#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable


# Initialize the Redis client
redis_store = redis.Redis()
'''The module-level Redis instance.
'''


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    This decorator increments the access count for the URL and caches
    the output for 10 seconds.
    '''
    @wraps(method)
    def invoker(url: str) -> str:
        '''The wrapper function for caching the output.

        Parameters:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content of the URL.
        '''
        # Increment the access count for this URL
        redis_store.incr(f'count:{url}')

        # Check if cached result exists
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')

        # Fetch the result from the actual request
        result = method(url)

        # Cache the result with an expiration time of 10 seconds
        redis_store.setex(f'result:{url}', 10, result)

        return result

    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.

    Parameters:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    '''
    return requests.get(url).text
