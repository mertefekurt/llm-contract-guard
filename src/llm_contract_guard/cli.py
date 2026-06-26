from __future__ import annotations

import argparse
import sys
from pathlib import Path

from llm_contract_guard.io import load_records, load_schema
from llm_contract_guard.report import render_json, render_text
from llm_contract_guard.validator import GuardConfig, validate_records


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="llm-contract-guard",
        description="Validate LLM JSON outputs against a JSON Schema contract.",
    )
    parser.add_argument("input", type=Path, help="text file or JSONL file with model outputs")
    parser.add_argument("--schema", type=Path, required=True, help="JSON Schema contract file")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="report format",
    )
    parser.add_argument(
        "--coerce",
        action="store_true",
        help="coerce simple string numbers and booleans before validation",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="stop after the first invalid record",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        schema = load_schema(args.schema)
        records = load_records(args.input)
        results = validate_records(
            records,
            GuardConfig(schema=schema, coerce=args.coerce, fail_fast=args.fail_fast),
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    renderer = render_json if args.format == "json" else render_text
    print(renderer(results))
    return 1 if any(not result.ok for result in results) else 0
