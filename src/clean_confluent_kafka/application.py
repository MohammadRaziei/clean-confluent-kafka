from clean_confluent_kafka.broker import KafkaBroker


class KafkaApplication:
    def __init__(self, *args, **kwargs):
        self.broker = KafkaBroker(*args, **kwargs)
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


