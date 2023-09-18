from __future__ import annotations

from typing import Optional

import typer

from clean_confluent_kafka.tools import KafkaConfigsGenerator

app = typer.Typer(no_args_is_help=True)


@app.command(help="With prompt for configuration")
def ask(server: str = typer.Option(..., prompt=True)):
    gen = KafkaConfigsGenerator(server)
    enable_consumer = typer.confirm("Adding consumer?", default=True)
    if enable_consumer:
        consumer_topics = typer.prompt("Consumer topics?", type=str)
        consumer_group = typer.prompt("Consumer Group?", default=consumer_topics+"_group", type=str)
        if len(consumer_group) == 0:
            consumer_group = None
        gen.add_consumer(consumer_topics, consumer_group)

    enable_producer = typer.confirm("Adding producer?", default=True)
    if enable_producer:
        producer_topic = typer.prompt("Producer topic?", type=str)
        gen.add_producer(producer_topic)

    save = typer.confirm("Do you want to save it?", default=True)
    if save:
        save_path = typer.prompt("choose a save path ", default="kafka.yaml", type=str)
        gen.save(save_path)
    else:
        typer.echo(gen.text)


@app.command(help="without prompt for configuration")
def create(server: str,
           consumer_topics: Optional[str] = None,
           consumer_group: Optional[str] = None,
           producer_topic: Optional[str] = None,
           save_path: Optional[str] = None,
           echo: bool = False):
    gen = KafkaConfigsGenerator(server)
    if consumer_topics is not None:
        gen.add_consumer(consumer_topics, consumer_group)
    if producer_topic is not None:
        gen.add_producer(producer_topic)
    if save_path is None:
        if echo:
            typer.echo(gen.text)
        else:
            gen.save("kafka.yaml")
    else:
        text = gen.save(save_path)
        if echo:
            typer.echo(text)


if __name__ == "__main__":
    app()
