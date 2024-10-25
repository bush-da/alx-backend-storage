#!/usr/bin/env python3
"""Module writing strings to redis"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''returns the given method after incrementing its call counter.
        '''

        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
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
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Generate Redis keys for inputs and outputs"""
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
    """Cache class"""
    def __init__(self):
        """Initialize the Cache instance with
        a Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history  # Apply both decorators to store
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis with a randomly generated key.

        Args:
            data: The data to store, which can be of
        type str, bytes, int, or float.

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


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.

    Args:
        method: The function for which the call history should be displayed.
    """
    # Get the qualified name of the method
    qualname = method.__qualname__

    # Get the call count from Redis
    cache_instance = method.__self__
    call_count = cache_instance._redis.get(qualname)
    if call_count:
        call_count = int(call_count)
    else:
        call_count = 0

    print(f"{qualname} was called {call_count} times:")

    # Retrieve inputs and outputs
    inputs = cache_instance._redis.lrange(f"{qualname}:inputs", 0, -1)
    outputs = cache_instance._redis.lrange(f"{qualname}:outputs", 0, -1)

    # Display each input-output pair
    for input_args, output in zip(inputs, outputs):
        print(f"{qualname}(*{input_args.decode('utf-8')}) -> \
        {output.decode('utf-8')}")
