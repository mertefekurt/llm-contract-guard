from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_schema(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"schema file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"schema file is not valid JSON: {exc.msg}") from exc

    if not isinstance(data, dict):
        raise ValueError("schema must be a JSON object")
    return data


def load_records(path: Path) -> list[tuple[str, str]]:
    if path.suffix.lower() == ".jsonl":
        return _load_jsonl_records(path)
    return [(path.name, path.read_text(encoding="utf-8"))]


def _load_jsonl_records(path: Path) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise ValueError(f"input file not found: {path}") from exc

    for index, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{index} is not valid JSONL: {exc.msg}") from exc

        record_id = str(payload.get("id", index)) if isinstance(payload, dict) else str(index)
        raw_text = _extract_raw_text(payload)
        records.append((record_id, raw_text))
    return records


def _extract_raw_text(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        for key in ("output", "response", "content", "text"):
            value = payload.get(key)
            if isinstance(value, str):
                return value
        return json.dumps(payload)
    return json.dumps(payload)
