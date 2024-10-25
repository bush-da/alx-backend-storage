#!/usr/bin/env python3
"""Module writing strings to redis"""
import redis
import uuid
from typing import Union, Callable, Optional
import functools


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


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a method.

    Args:
        method: The method to be decorated.

    Returns:
        A wrapped method that stores input and output history.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Generate Redis keys for inputs and outputs
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the input arguments as a string in Redis
        self._redis.rpush(input_key, str(args))

        # Execute the method and store its output
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))

        return result
    return wrapper


class Cache:
    def __init__(self):
        """Initialize the Cache instance with a Redis
        client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history  # Apply both decorators to store
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis with a randomly generated key.

        Args:
            data: The data to store, which can be
        of type str, bytes, int, or float.

        Returns:
            The key under which the data is stored in Redis.
        """
        key = str(uuid.uuid4())  # Generate a random key
        self._redis.set(key, data)  # Store data in Redis with the random key
        return key

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieve a string from Redis."""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieve an integer from Redis."""
        return self.get(key, fn=int)
