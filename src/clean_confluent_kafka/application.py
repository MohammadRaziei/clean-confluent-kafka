from clean_confluent_kafka.broker import KafkaBroker


class KafkaApplication(KafkaBroker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


