#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """
import requests
import redis
from typing import Callable
from functools import wraps

# Initialize Redis connection
r = redis.Redis()


def cache_page(func: Callable) -> Callable:
    """Decorator to cache a page and track URL access count."""
    @wraps(func)
    def wrapper(url: str) -> str:
        # Track access count
        count_key = f"count:{url}"
        r.incr(count_key)

        # Check if cached data exists
        cache_key = f"cached:{url}"
        cached_content = r.get(cache_key)
        if cached_content:
            return cached_content.decode('utf-8')

        # If not cached, get the page content and cache it
        content = func(url)
        r.setex(cache_key, 10, content)  # Cache with 10-second expiration
        return content

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Fetches the HTML content of the given URL.

    Args:
        url: The URL to fetch.

    Returns:
        The HTML content as a string.
    """
    response = requests.get(url)
    return response.text
