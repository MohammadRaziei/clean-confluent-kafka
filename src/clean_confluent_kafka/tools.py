from __future__ import annotations
from pathlib import Path
from typing import Optional

from jinja2 import Template


class KafkaConfigsGenerator:
    KAFKA_TEMPLATE_PATH = Path(__file__).parent / "resources" / "kafka-template.yaml"

    def __init__(self, server_port: str):
        with open(self.KAFKA_TEMPLATE_PATH) as f:
            template_text = f.read()
        self._template = Template(template_text)
        self._template_configs = {"kafka_servers": server_port}

    def add_consumer(self, consumer_topics: str, consumer_group: Optional[str] = None) -> "KafkaConfigsGenerator":
        consumer_group = consumer_group if consumer_group is not None else f"{consumer_topics}_group"
        self._template_configs.update(enable_consumer=True,
                                      consumer_topics=consumer_topics,
                                      consumer_group=consumer_group)
        return self

    def add_producer(self, producer_topic: str) -> "KafkaConfigsGenerator":
        self._template_configs.update(enable_producer=True, producer_topic=producer_topic)
        return self

    @property
    def text(self) -> str:
        kafka_configs_text = self._template.render(self._template_configs).strip()
        _kafka_configs_text = ""
        while _kafka_configs_text != kafka_configs_text:
            _kafka_configs_text = kafka_configs_text
            kafka_configs_text = kafka_configs_text.replace("\n\n\n", "\n\n")
        return kafka_configs_text + "\n"

    def save(self, path: str):
        kafka_configs_text = self.text
        with open(path, "w") as f:
            f.write(kafka_configs_text)
        return kafka_configs_text

    def parse(self):
        import yaml
        yaml.safe_load(self.text)

