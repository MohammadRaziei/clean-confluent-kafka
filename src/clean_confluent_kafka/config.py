from __future__ import annotations

from collections import namedtuple
from typing import Dict, Optional, Any
import os

from clean_confluent_kafka.utils import flatten_dict, reverse_flatten_dict, unflatten_dict
from clean_confluent_kafka.utils import convert_string_to_real_number as string_handler


def update_conf_dict_with_env(conf_dict, key_prefix=""):
    for key in conf_dict:
        # Check if the key is defined in the environment
        key_env = (key_prefix + key.replace(".", "_")).upper()
        env_var = os.environ.get(key_env, None)
        if env_var is not None:
            conf_dict[key] = string_handler(env_var)


class KafkaConfigParser:
    ParsedConfigResult = namedtuple("ParsedConfigResult", ["consumer", "producer", "app"])
    ParsedConfig = namedtuple("ParsedConfig", ["config", "topic", "app"])

    @staticmethod
    def from_path(path):
        import yaml
        with open(path) as f:
            config = yaml.safe_load(f)
        return KafkaConfigParser(config)

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config if config is not None else dict()
        self.config = flatten_dict(self.config)

    def update_config(self, config: Dict[str, Any]):
        self.config.update(flatten_dict(config))

    def _get(self, name):
        _configs = unflatten_dict(self.config).get(name, None)
        if _configs is None:
            _configs = dict()
        return _configs

    def _create_parsed_config(self, name):
        kafka_configs = reverse_flatten_dict(self._get(name))
        if name == "consumer":
            topic = kafka_configs.pop("topics", [])
            if not isinstance(topic, list):
                topic = [topic]
        else:
            topic = kafka_configs.pop("topic", "")
        config_app = kafka_configs.pop("app", None)
        if config_app is not None:
            config_app = reverse_flatten_dict(config_app)
        return self.ParsedConfig(flatten_dict(kafka_configs), topic, config_app)

    def parse(self):
        app_configs = reverse_flatten_dict(self._get("app"))
        return self.ParsedConfigResult(
            consumer=self._create_parsed_config("consumer"),
            producer=self._create_parsed_config("producer"),
            app=app_configs
        )
        # self.config = flatten_dict(self.config)

    def export_config(self, flatten=True):
        # config = flatten_dict(self.config)
        config = flatten_dict(self.config) if flatten else reverse_flatten_dict(self.config)
        return config
