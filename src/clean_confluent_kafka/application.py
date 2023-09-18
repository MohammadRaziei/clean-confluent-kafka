from __future__ import annotations
from clean_confluent_kafka.connection import KafkaConnection


class KafkaApplication:
    def __init__(self, *args, **kwargs):
        self.broker = KafkaConnection(*args, **kwargs)
        raise NotImplementedError

    def consume(self):
        def decorator(func):
            # @wraps(func)
            # def wrapper(*args, **kwargs):
            messages = self.broker.consume()
            func(messages)
            return func
            # return wrapper
        return decorator

    def produce(self, key=None, auto_flush: bool = True):
        def decorator(func):
            # @wraps(func)
            # def wrapper(*args, **kwargs):
            data = func()
            self.broker.produce(data, key, auto_flush)
            # return wrapper
            return func
        return decorator

    # def __call__(self):


