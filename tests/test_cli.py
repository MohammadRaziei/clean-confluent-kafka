from typer.testing import CliRunner

from clean_confluent_kafka.__main__ import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["create", "Hi"])
    assert result.exit_code == 0
    assert "" in result.stdout
    # assert "" in result.stdout