from typer.testing import CliRunner

from clean_confluent_kafka.__main__ import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["create", "localhost:8080", "--consumer-topics", "mytopic",
                                 "--echo"])
    assert result.exit_code == 0
    assert "group.id: mytopic_group" in result.stdout
