
# Clean Confluent Kafka

<!-- !\\[GitHub Workflow Status\\]([26](https://badgen.net/github/status/MohammadRaziei/clean-confluent-kafka/main)) -->
<!-- !\\[PyPI\\]([27](https://badgen.net/pypi/v/clean-confluent-kafka)) -->
<!-- !\\[License\\]([28](https://badgen.net/github/license/MohammadRaziei/clean-confluent-kafka)) -->

This project is a wrapper around the [confluent-kafka-python](^1^) library that provides a clean and easy-to-use interface for producing and consuming messages from Kafka topics.

## Features

- Supports both synchronous and asynchronous modes of operation
- Supports SSL and SASL authentication
- Supports Avro, JSON, and plain text serialization
- Supports custom partitioners and serializers
- Supports priority of Kafka configs from different sources
- Supports topic auto-creation and configuration

## Installation

To install this project, you need to have Python 3.6 or higher and pip installed. Then, run the following command:

```bash
pip install clean-confluent-kafka
```

## Usage

To use this project, you need to create a `KafkaConnection` object and pass in the configuration parameters for your Kafka cluster, such as bootstrap servers, security protocol, and consumer groups. For example:

```python
from clean_confluent_kafka import KafkaConnection

# Create a connection
conn = KafkaConnection(
    bootstrap_servers="localhost:9092",
    consumer_groups="a"
)

# Print the connection configuration
print("conn")
print(conn.conf.export_config())

# Consume a message from a topic
message = conn.consume()
print(message.value())
```

You can also use the `Producer` and `Consumer` classes to produce and consume messages from specific topics. For more details and examples, please refer to the [documentation](^2^).

## Priority of Kafka configs

This project supports the following order of precedence for Kafka configuration:

- Environment variables (if enabled)
- Input arguments
- List of configs
- Kafka.yml file (if exists)

You can enable or disable the use of environment variables by setting the `use_env` parameter to `True` or `False` when creating a `KafkaConnection` object. For example:

```python
# Enable the use of environment variables
conn = KafkaConnection(use_env=True)

# Disable the use of environment variables
conn = KafkaConnection(use_env=False)
```

You can also specify the path to the Kafka.yml file by setting the `config_file` parameter when creating a `KafkaConnection` object. For example:

```python
# Use the default path (./kafka.yml)
conn = KafkaConnection()

# Use a custom path
conn = KafkaConnection(config_file="/path/to/kafka.yml")
```

The Kafka.yml file should follow the YAML syntax and contain the configuration parameters for the producer and/or the consumer. For example:

```yaml
producer:
  bootstrap.servers: "localhost:9092"
  security.protocol: "PLAINTEXT"
  topic: "test-topic"

consumer:
  bootstrap.servers: "localhost:9092"
  security.protocol: "PLAINTEXT"
  topic: "test-topic"
  group.id: "test-group"
```

## Contributing

Contributions are welcome and appreciated. If you want to contribute to this project, please follow these steps:

- Fork the repository and clone it to your local machine.
- Create a new branch with a descriptive name for your feature or bug fix.
- Make your changes and commit them with a clear and concise message.
- Push your branch to your forked repository and create a pull request to the main branch.
- Wait for your pull request to be reviewed and merged.

Please make sure to follow the [PEP 8](^3^) style guide and write tests for your code if possible.

## License

This project is licensed under the [MIT License](^4^). See the [LICENSE](^5^) file for more details.


>I hope this helps you with your project. If you have any feedback or questions, please let me know. 😊
