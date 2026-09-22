import httpx
import pytest


async def test_fetch_json_returns_parsed_body(cli, local_server):
    async with httpx.AsyncClient() as client:
        data = await cli.fetch_json(client, f"{local_server}/data")

    assert data["user"]["name"] == "Ada"


async def test_fetch_json_raises_on_404(cli, local_server):
    async with httpx.AsyncClient() as client:
        with pytest.raises(httpx.HTTPStatusError):
            await cli.fetch_json(client, f"{local_server}/does-not-exist")


def test_extract_field_nested(cli):
    data = {"user": {"address": {"city": "London"}}}

    assert cli.extract_field(data, "user.address.city") == "London"


def test_extract_field_top_level(cli):
    assert cli.extract_field({"status": "ok"}, "status") == "ok"


def test_extract_field_missing_raises_key_error(cli):
    data = {"user": {}}

    with pytest.raises(KeyError):
        cli.extract_field(data, "user.address.city")


async def test_run_end_to_end(cli, local_server):
    result = await cli.run(f"{local_server}/data", "user.name")

    assert result == "Ada"


async def test_run_propagates_http_errors(cli, local_server):
    with pytest.raises(httpx.HTTPStatusError):
        await cli.run(f"{local_server}/does-not-exist", "user.name")


def test_main_success_prints_value_and_returns_zero(cli, local_server, capsys):
    exit_code = cli.main([f"{local_server}/data", "user.name"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "Ada"


def test_main_http_error_returns_one_and_prints_to_stderr(cli, local_server, capsys):
    exit_code = cli.main([f"{local_server}/does-not-exist", "user.name"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error" in captured.err


def test_main_missing_field_returns_one_and_prints_to_stderr(cli, local_server, capsys):
    exit_code = cli.main([f"{local_server}/data", "user.nonexistent"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error" in captured.err
