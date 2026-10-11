"""tinyconf — read and write flat ``key = value`` configuration files with typed values.

Values are integers, floats, booleans (``true``/``false``) or double-quoted strings. Blank lines
and lines starting with ``#`` are ignored. The API is stable; see README.md.
"""

from __future__ import annotations

import os
from pathlib import Path

__all__ = ["ConfigError", "loads", "dumps", "load", "dump"]

Value = int | float | bool | str


class ConfigError(ValueError):
    """A malformed line, an unsupported value, or a duplicate key."""


def _parse_value(raw: str, line_no: int) -> Value:
    raw = raw.strip()
    if raw == "true":
        return True
    if raw == "false":
        return False
    if len(raw) >= 2 and raw[0] == '"' and raw[-1] == '"':
        return raw[1:-1]
    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        raise ConfigError(f"line {line_no}: unsupported value {raw!r}") from None


def loads(text: str) -> dict[str, Value]:
    """Parse configuration text into a dict, keys in file order."""
    values: dict[str, Value] = {}
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            raise ConfigError(f"line {line_no}: expected 'key = value'")
        key, _, raw = stripped.partition("=")
        key = key.strip()
        if not key:
            raise ConfigError(f"line {line_no}: empty key")
        if key in values:
            raise ConfigError(f"line {line_no}: duplicate key {key!r}")
        values[key] = _parse_value(raw, line_no)
    return values


def dumps(values: dict[str, Value]) -> str:
    """Render a dict as configuration text, strings quoted, one key per line."""
    lines: list[str] = []
    for key, value in values.items():
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        elif isinstance(value, (int, float)):
            rendered = repr(value)
        elif isinstance(value, str):
            rendered = '"' + value + '"'
        else:
            raise ConfigError(f"key {key!r}: unsupported value type {type(value).__name__}")
        lines.append(f"{key} = {rendered}")
    return "\n".join(lines) + ("\n" if lines else "")


def load(path: str | os.PathLike[str]) -> dict[str, Value]:
    """loads() over a file's UTF-8 contents."""
    return loads(Path(path).read_text(encoding="utf-8"))


def dump(values: dict[str, Value], path: str | os.PathLike[str]) -> None:
    """Write dumps(values) to a file as UTF-8."""
    Path(path).write_text(dumps(values), encoding="utf-8")
