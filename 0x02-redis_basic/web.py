#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""
import requests
import redis
from functools import wraps
from typing import Callable

# Initialize Redis client
r = redis.Redis()


def track_access_and_cache(func: Callable) -> Callable:
    """Decorator to cache the result of `get_page` and track access count."""
    @wraps(func)
    def wrapper(url: str) -> str:
        # Define the Redis keys for count and cache
        count_key = f"count:{url}"
        cache_key = f"cached:{url}"

        # Increment the access count for this URL
        r.incr(count_key)

        # Check if cached content exists
        cached_content = r.get(cache_key)
        if cached_content:
            return cached_content.decode('utf-8')

        # Fetch the content, cache it, and set expiration if not cached
        content = func(url)
        r.setex(cache_key, 10, content)
        return content

    return wrapper


@track_access_and_cache
def get_page(url: str) -> str:
    """
    Fetch HTML content of a given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
