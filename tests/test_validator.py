from llm_contract_guard.validator import GuardConfig, validate_records

SCHEMA = {
    "type": "object",
    "required": ["label", "confidence", "safe"],
    "additionalProperties": False,
    "properties": {
        "label": {"type": "string", "enum": ["allow", "block"]},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "safe": {"type": "boolean"},
    },
}


def test_validates_matching_record() -> None:
    results = validate_records(
        [("1", '{"label": "allow", "confidence": 0.7, "safe": true}')],
        GuardConfig(schema=SCHEMA),
    )

    assert results[0].ok is True
    assert results[0].errors == ()


def test_reports_schema_errors_with_paths() -> None:
    results = validate_records(
        [("bad", '{"label": "review", "confidence": 2, "safe": true}')],
        GuardConfig(schema=SCHEMA),
    )

    assert results[0].ok is False
    assert {error.path for error in results[0].errors} == {"$.confidence", "$.label"}


def test_coerces_simple_types_when_enabled() -> None:
    results = validate_records(
        [("2", '{"label": "block", "confidence": "0.64", "safe": "false"}')],
        GuardConfig(schema=SCHEMA, coerce=True),
    )

    assert results[0].ok is True
    assert results[0].data == {"label": "block", "confidence": 0.64, "safe": False}


def test_does_not_coerce_without_flag() -> None:
    results = validate_records(
        [("2", '{"label": "block", "confidence": "0.64", "safe": "false"}')],
        GuardConfig(schema=SCHEMA),
    )

    assert results[0].ok is False
    assert {error.path for error in results[0].errors} == {"$.confidence", "$.safe"}


def test_fail_fast_stops_after_first_failure() -> None:
    results = validate_records(
        [
            ("bad", "not json"),
            ("good", '{"label": "allow", "confidence": 0.7, "safe": true}'),
        ],
        GuardConfig(schema=SCHEMA, fail_fast=True),
    )

    assert [result.record_id for result in results] == ["bad"]
