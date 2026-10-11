import pytest

from tinyconf import ConfigError, dump, dumps, load, loads


def test_loads_typed_values_and_ignores_comments_and_blank_lines():
    text = '# server\nhost = "localhost"\n\nport = 8080\ndebug = false\nratio = 0.75\n'
    assert loads(text) == {"host": "localhost", "port": 8080, "debug": False, "ratio": 0.75}


def test_dumps_round_trips_in_insertion_order():
    values = {"host": "localhost", "port": 8080, "debug": True, "ratio": 0.75}
    assert loads(dumps(values)) == values
    assert dumps(values).splitlines()[0] == 'host = "localhost"'


@pytest.mark.parametrize("text", ["port 8080", "= 1", "x = maybe", "a = 1\na = 2"])
def test_malformed_input_raises_config_error(text):
    with pytest.raises(ConfigError):
        loads(text)


def test_dumps_refuses_unsupported_types():
    with pytest.raises(ConfigError):
        dumps({"items": [1, 2]})


def test_load_and_dump_use_files(tmp_path):
    path = tmp_path / "app.conf"
    dump({"name": "fixture", "retries": 3}, path)
    assert load(path) == {"name": "fixture", "retries": 3}
