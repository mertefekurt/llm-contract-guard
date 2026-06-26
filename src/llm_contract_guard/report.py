from __future__ import annotations

import json
from typing import Any

from llm_contract_guard.validator import ContractResult


def summarize(results: list[ContractResult]) -> dict[str, Any]:
    total = len(results)
    failed = sum(not result.ok for result in results)
    return {
        "total": total,
        "passed": total - failed,
        "failed": failed,
        "failure_rate": round(failed / total, 4) if total else 0.0,
    }


def render_text(results: list[ContractResult]) -> str:
    summary = summarize(results)
    lines = [
        "LLM contract report",
        f"records: {summary['total']} | passed: {summary['passed']} | failed: {summary['failed']}",
    ]
    failures = [result for result in results if not result.ok]
    if not failures:
        lines.append("status: all records match the contract")
        return "\n".join(lines)

    lines.append("")
    for result in failures:
        lines.append(f"- {result.record_id}")
        for error in result.errors:
            lines.append(f"  {error.path}: {error.message}")
    return "\n".join(lines)


def render_json(results: list[ContractResult]) -> str:
    payload = {
        "summary": summarize(results),
        "results": [
            {
                "id": result.record_id,
                "ok": result.ok,
                "errors": [
                    {"path": error.path, "message": error.message} for error in result.errors
                ],
                "data": result.data,
            }
            for result in results
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True)
