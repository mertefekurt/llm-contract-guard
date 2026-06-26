import pytest

from llm_contract_guard.extractor import JsonExtractionError, extract_json


def test_extracts_plain_json_object() -> None:
    assert extract_json('{"ok": true}') == {"ok": True}


def test_extracts_json_from_markdown_fence() -> None:
    text = '```json\n{"score": 0.91}\n```'
    assert extract_json(text) == {"score": 0.91}


def test_extracts_balanced_json_from_surrounding_text() -> None:
    text = 'answer: {"items": [{"name": "a"}], "ok": true} thanks'
    assert extract_json(text) == {"items": [{"name": "a"}], "ok": True}


def test_raises_for_missing_json() -> None:
    with pytest.raises(JsonExtractionError):
        extract_json("I cannot answer that as JSON.")
