#!/usr/bin/env python3
"""Module writing strings to redis"""
import redis
import uuid
from typing import Union


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
