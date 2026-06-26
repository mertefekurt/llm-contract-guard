from __future__ import annotations

import json
import re
from typing import Any


class JsonExtractionError(ValueError):
    """Raised when no valid JSON object or array can be extracted."""


FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.IGNORECASE | re.DOTALL)


def extract_json(text: str) -> Any:
    """Extract the first valid JSON object or array from a model response."""
    stripped = text.strip()
    if not stripped:
        raise JsonExtractionError("empty input")

    fenced = FENCE_RE.search(stripped)
    candidates = [fenced.group(1).strip()] if fenced else []
    candidates.append(stripped)
    candidates.extend(_balanced_candidates(stripped))

    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue

    raise JsonExtractionError("could not extract a valid JSON object or array")


def _balanced_candidates(text: str) -> list[str]:
    candidates: list[str] = []
    for opening, closing in (("{", "}"), ("[", "]")):
        start = text.find(opening)
        while start != -1:
            candidate = _scan_balanced(text, start, opening, closing)
            if candidate is not None:
                candidates.append(candidate)
            start = text.find(opening, start + 1)
    return candidates


def _scan_balanced(text: str, start: int, opening: str, closing: str) -> str | None:
    depth = 0
    in_string = False
    escaped = False

    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return text[start : index + 1]

    return None
