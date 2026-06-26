from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def coerce_value(value: Any, schema: Mapping[str, Any]) -> Any:
    expected = schema.get("type")
    if isinstance(expected, list):
        expected_types = [item for item in expected if item != "null"]
        expected = expected_types[0] if expected_types else None

    if expected == "object" and isinstance(value, dict):
        return _coerce_object(value, schema)
    if expected == "array" and isinstance(value, list):
        return _coerce_array(value, schema)

    scalar_coercers = {
        "integer": _to_integer,
        "number": _to_number,
        "boolean": _to_boolean,
        "string": _to_string,
    }
    coercer = scalar_coercers.get(expected)
    return coercer(value) if coercer else value


def _coerce_object(value: dict[str, Any], schema: Mapping[str, Any]) -> dict[str, Any]:
    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        return value

    coerced = dict(value)
    for key, property_schema in properties.items():
        if key in coerced and isinstance(property_schema, dict):
            coerced[key] = coerce_value(coerced[key], property_schema)
    return coerced


def _coerce_array(value: list[Any], schema: Mapping[str, Any]) -> list[Any]:
    item_schema = schema.get("items")
    if not isinstance(item_schema, dict):
        return value
    return [coerce_value(item, item_schema) for item in value]


def _to_integer(value: Any) -> Any:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        try:
            parsed = float(value.strip())
        except ValueError:
            return value
        if parsed.is_integer():
            return int(parsed)
    return value


def _to_number(value: Any) -> Any:
    if isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return value
    return value


def _to_string(value: Any) -> Any:
    return str(value) if value is not None else value


def _to_boolean(value: Any) -> Any:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "yes", "1"}:
            return True
        if normalized in {"false", "no", "0"}:
            return False
    return value
