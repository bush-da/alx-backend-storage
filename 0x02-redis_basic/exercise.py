#!/usr/bin/env python3
"""Module writing strings to redis"""
import redis
import uuid
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        method: The method to be wrapped and counted.

    Returns:
        A wrapped method that increments a call count each time it is called.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Increment the call count in Redis using the method's qualified name
        key = method.__qualname__
        self._redis.incr(key)
        # Call the original method
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """Cache class"""
    def __init__(self):
        """Initialize the Cache instance with a Redis client
        and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis with a randomly generated key.

        Args:
            data: The data to store, which can be of type str,
        bytes, int, or float.

        Returns:
            The key under which the data is stored in Redis.
        """
        key = str(uuid.uuid4())  # Generate a random key
        self._redis.set(key, data)  # Store data in Redis with the random key
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float,
                                                    None]:
        """
        Retrieve data from Redis, optionally converting it
        using a provided callable.

        Args:
            key: The key of the data to retrieve.
            fn: A callable used to convert the data back to the desired format.

        Returns:
            The data retrieved from Redis, optionally converted using `fn`.
        """
        data = self._redis.get(key)  # Retrieve data from Redis
        if data is None:
            return None  # If the key does not exist, return None
        if fn:
            return fn(data)  # Apply the conversion function if provided
        return data  # Return raw data if no conversion is applied

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieve a string from Redis."""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieve an integer from Redis."""
        return self.get(key, fn=int)
