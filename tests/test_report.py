import json

from llm_contract_guard.report import render_json, render_text, summarize
from llm_contract_guard.validator import ContractResult, RecordError


def test_summary_counts_passed_and_failed_records() -> None:
    results = [
        ContractResult("ok", True, {}, ()),
        ContractResult("bad", False, None, (RecordError("bad", "$", "invalid"),)),
    ]

    assert summarize(results) == {"total": 2, "passed": 1, "failed": 1, "failure_rate": 0.5}


def test_text_report_includes_failure_details() -> None:
    report = render_text(
        [ContractResult("bad", False, None, (RecordError("bad", "$.name", "is required"),))]
    )

    assert "LLM contract report" in report
    assert "$.name: is required" in report


def test_json_report_is_machine_readable() -> None:
    payload = json.loads(render_json([ContractResult("ok", True, {"x": 1}, ())]))

    assert payload["summary"]["passed"] == 1
    assert payload["results"][0]["data"] == {"x": 1}
