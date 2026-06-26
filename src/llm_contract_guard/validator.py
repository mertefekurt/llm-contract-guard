from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from llm_contract_guard.coerce import coerce_value
from llm_contract_guard.extractor import JsonExtractionError, extract_json


@dataclass(frozen=True)
class GuardConfig:
    schema: dict[str, Any]
    coerce: bool = False
    fail_fast: bool = False


@dataclass(frozen=True)
class RecordError:
    record_id: str
    path: str
    message: str


@dataclass(frozen=True)
class ContractResult:
    record_id: str
    ok: bool
    data: Any | None
    errors: tuple[RecordError, ...]


def validate_records(records: list[tuple[str, str]], config: GuardConfig) -> list[ContractResult]:
    """Validate raw LLM responses and return per-record contract results."""
    try:
        validator = Draft202012Validator(config.schema)
        validator.check_schema(config.schema)
    except SchemaError as exc:
        raise ValueError(f"invalid JSON Schema: {exc.message}") from exc

    results: list[ContractResult] = []
    for record_id, raw_text in records:
        result = _validate_one(record_id, raw_text, validator, config)
        results.append(result)
        if config.fail_fast and not result.ok:
            break
    return results


def _validate_one(
    record_id: str,
    raw_text: str,
    validator: Draft202012Validator,
    config: GuardConfig,
) -> ContractResult:
    try:
        data = extract_json(raw_text)
    except JsonExtractionError as exc:
        error = RecordError(record_id=record_id, path="$", message=str(exc))
        return ContractResult(record_id=record_id, ok=False, data=None, errors=(error,))

    if config.coerce:
        data = coerce_value(data, config.schema)

    errors = tuple(
        RecordError(record_id=record_id, path=_format_path(error.path), message=error.message)
        for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path))
    )
    return ContractResult(record_id=record_id, ok=not errors, data=data, errors=errors)


def _format_path(path_parts: Any) -> str:
    parts = list(path_parts)
    if not parts:
        return "$"
    rendered = "$"
    for part in parts:
        rendered += f"[{part}]" if isinstance(part, int) else f".{part}"
    return rendered
