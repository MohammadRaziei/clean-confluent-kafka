from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from pathlib import Path

import yaml
from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient

from clean_confluent_kafka.config import KafkaConfigParser, update_conf_dict_with_env
from clean_confluent_kafka.utils import flatten_dict, serializers, deserializers

logger = logging.getLogger(__name__)

SERVER_KEY = "bootstrap.servers"


class KafkaAction:
    def __init__(self, kafka_config, action, debug_mode: Optional[bool] = None):
        self.user_configs = kafka_config
        self.debug_mode = debug_mode if debug_mode is not None \
            else self.user_configs.app.get("debug", False)
        if self.debug_mode:
            logger.debug(self.user_configs.config)
        self.confluent = action(self.user_configs.config)


class KafkaAdmin:
    def __init__(self, data_servers: List[str] | Dict[str, Any] | str):
        if isinstance(data_servers, str):
            self.user_configs = {SERVER_KEY: data_servers}
        elif isinstance(data_servers, list):
            self.user_configs = {SERVER_KEY: ",".join(data_servers)}
        elif isinstance(data_servers, dict):
            self.user_configs = flatten_dict(data_servers)
        else:
            msg = "Invalid Configuration"
            raise ValueError(msg)

        self.confluent = AdminClient(self.user_configs)

    def get_topic(self):
        topics = self.confluent.list_topics().topics
        return topics


class KafkaConsumer(KafkaAction):
    def __init__(self, kafka_config_consumer, topics: Optional[str | List] = None,
                 debug_mode: Optional[bool] = None):
        super().__init__(kafka_config_consumer, Consumer, debug_mode)
        self.topics = topics if topics is not None else self.user_configs.topic
        self.confluent.subscribe(self.topics)
        self.deserializer = deserializers.json_deserializer

    def close(self):
        self.confluent.close()

    def __del__(self):
        self.close()
        if self.debug_mode:
            logger.debug("Consumer closed")

    def consume(self, deserializer=None):
        if deserializer is None:
            deserializer = self.deserializer

        while True:
            message = self.confluent.poll(timeout=1)
            if message is not None:
                break
        return deserializer(message.value())

    def __call__(self, deserializer=None):
        self.consume(deserializer=deserializer)

    def commit(self):
        self.confluent.commit()


class KafkaProducer(KafkaAction):
    DEFAULT_MAX_FOR_FLUSH: int = 100
    KEY_MAX_FOR_FLUSH: str = "max_for_flush"

    def __init__(self, kafka_config_producer, topic=None, debug_mode: Optional[bool] = None):
        super().__init__(kafka_config_producer, Producer, debug_mode)
        self.topic = topic if topic is not None else self.user_configs.topic
        self.serializer = serializers.json_serializer
        self._flush_counter = 0
        self._max_for_flush = self.user_configs.app.get(self.KEY_MAX_FOR_FLUSH,
                                                        self.DEFAULT_MAX_FOR_FLUSH)

    def __del__(self):
        self.flush()

    def flush(self):
        self.confluent.flush()

    def produce(self, data, key=None, auto_flush: bool = False, serializer=None):
        if serializer is None:
            serializer = self.serializer
        self._flush_counter = 0
        try:
            self.confluent.produce(self.user_configs.topic, key=key, value=serializer(data))
            self.confluent.poll(0)
            self._flush_counter += 1
            if self._flush_counter >= self._max_for_flush:
                self.flush()
                self._flush_counter = 0
        except BufferError as bfer:
            logger.error(
                "Error of full producer queue: %s",
                str(bfer))
            self.flush()
            self.confluent.produce(self.user_configs.topic, key=key, value=serializer(data))
        if auto_flush:
            self.flush()

    def __call__(self, data, key=None, auto_flush: bool = False, serializer=None):
        self.produce(data, key=key, auto_flush=auto_flush, serializer=serializer)

    def set_max_for_flush(self, value: int):
        self._max_for_flush = value


def load_yaml_file(filename):
    with open(filename, "r") as f:
        yaml_dict = yaml.safe_load(f)
    return yaml_dict


class KafkaConnection:
    _base_config_path = (Path(__file__).parent / "resources" / "base-kafka.yaml").as_posix()

    def __init__(self, config_path: Optional[str] = "kafka.yaml", extra_configs: Optional[Dict[str, Any]] = None,
                 consumer_topics: Optional[str] = None, consumer_groups: Optional[str] = None,
                 producer_topic: Optional[str] = None, use_base: bool = True):
        self.conf = KafkaConfigParser()

        if use_base:
            self.conf.update_config(load_yaml_file(self._base_config_path))
        if (config_path is not None) and Path(config_path).exists():
            self.conf.update_config(load_yaml_file(config_path))
        if extra_configs is not None:
            self.conf.update_config(extra_configs)
        if consumer_groups is not None:
            self.conf.update_config({"consumer": {"group.id": consumer_groups}})
        update_conf_dict_with_env(self.conf.config)

        self.kafka_config = self.conf.parse()

        #TODO: fuck it
        if self.kafka_config.consumer:
            self.consume = KafkaConsumer(self.kafka_config.consumer, topics=consumer_topics) \
                if SERVER_KEY in self.kafka_config.consumer.config else None
        self.produce = KafkaProducer(self.kafka_config.producer, topic=producer_topic) \
            if SERVER_KEY in self.kafka_config.producer.config else None
        server = self.kafka_config.producer.config.get(SERVER_KEY)
        if server is None:
            server = self.kafka_config.consumer.config.get(SERVER_KEY)
        self.server = server
        self.admin = KafkaAdmin(self.server)

    def export_configs(self, flatten=True):
        return self.conf.export_config(flatten=flatten)

    # def consume(self, *args, **kwargs):
    #     if self.consumer is None:
    #         raise NotImplementedError
    #     return self.consumer.consume(*args, **kwargs)

    # def produce(self, *args, **kwargs):
    #     if self.producer is None:
    #         raise NotImplementedError
    #     return self.producer.produce(*args, **kwargs)

    def commit(self):
        if self.consumer is None:
            raise NotImplementedError
        return self.consumer.commit()

    def flush(self):
        if self.consumer is None:
            raise NotImplementedError
        return self.producer.flush()

    def get_topics(self):
        return self.admin.get_topic()

    def get_topics_list(self):
        return list(self.admin.get_topic())
