#!/usr/bin/env python3
"""context-governor-audit.py — expose high_roi.rs audit functions as CLI.

Subcommands:
  audit-tool-surface   — audit MCP tool descriptions for split-instruction/selection risks
  eval-governed-memory  — evaluate memory governance cases
  eval-rag-leakage      — evaluate retrieval leakage-free RAG
  screen-conflicts      — screen knowledge claims for conflicts
  select-route          — select retrieval route for a query

Missing or failed native owners return typed failures and nonzero exit status.
The wrapper never synthesizes native governance receipts.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

DEFAULT_BINARY = (
    os.environ.get("CONTEXT_GOVERNOR_BIN")
    or shutil.which("context-governor")
    or os.path.join(os.path.expanduser("~"), ".cargo", "bin", "context-governor")
)


def fail(code: str, detail: str, exit_code: int = 1) -> None:
    print(json.dumps({"schema": "KitNativeInvocationFailureV1", "status": "failed",
                      "code": code, "detail": detail, "owner": "context-governor"}))
    raise SystemExit(exit_code)


def run_cg(binary_path: str, args: list[str], stdin: str | None = None) -> str:
    """Return the native JSON receipt unchanged, or a typed non-success."""
    if not os.path.isfile(binary_path) or not os.access(binary_path, os.X_OK):
        fail("OWNER_UNAVAILABLE", "context-governor binary is not executable", 127)
    try:
        result = subprocess.run([binary_path] + args, input=stdin,
                                capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        fail("OWNER_TIMEOUT", "context-governor exceeded 60 seconds", 124)
    except OSError as exc:
        fail("OWNER_UNAVAILABLE", str(exc), 127)
    if result.returncode != 0:
        fail("OWNER_FAILED", f"context-governor exited {result.returncode}")
    try:
        receipt = json.loads(result.stdout)
    except json.JSONDecodeError:
        fail("INVALID_OWNER_RESPONSE", "context-governor did not return JSON")
    if not isinstance(receipt, dict) or not isinstance(receipt.get("schema"), str):
        fail("INVALID_OWNER_RESPONSE", "native response lacks a schema")
    return result.stdout


def cmd_audit_tool_surface(args: argparse.Namespace) -> None:
    tools_json = args.tools_json or json.dumps([])
    output = run_cg(args.binary_path, ["audit-tool-surface", "--tools-json", tools_json])
    print(output)


def cmd_eval_governed_memory(args: argparse.Namespace) -> None:
    cases_json = args.cases_json or json.dumps([])
    output = run_cg(
        args.binary_path,
        [
            "eval-governed-memory",
            "--harness-id",
            args.harness_id or "default",
            "--cases-json",
            cases_json,
        ],
    )
    print(output)


def cmd_eval_rag_leakage(args: argparse.Namespace) -> None:
    cg_args = [
        "eval-rag-leakage",
        "--task-id",
        args.task_id or "default",
        "--closed-book-correct",
        "true" if args.closed_book_correct else "false",
        "--retrieved-correct",
        "true" if args.retrieved_correct else "false",
        "--retrieval-used",
        "true" if args.retrieval_used else "false",
    ]
    output = run_cg(args.binary_path, cg_args)
    print(output)


def cmd_screen_conflicts(args: argparse.Namespace) -> None:
    claims_json = args.claims_json or json.dumps([])
    output = run_cg(args.binary_path, ["screen-conflicts", "--claims-json", claims_json])
    print(output)


def cmd_audit_compression_boundary(args: argparse.Namespace) -> None:
    try:
        request = json.loads(args.request_json or "{}")
    except json.JSONDecodeError:
        fail("INVALID_REQUEST", "boundary request is not JSON", 64)
    if not isinstance(request, dict):
        fail("INVALID_REQUEST", "boundary request must be an object", 64)
    # Accept the native request only. No lossy alias conversion or audit substitute.
    if set(request) != {"source_fragments", "compressed_summary"}:
        fail("INVALID_REQUEST", "use native source_fragments and compressed_summary fields", 64)
    if (not isinstance(request["source_fragments"], list)
            or any(not isinstance(x, str) for x in request["source_fragments"])
            or not isinstance(request["compressed_summary"], str)):
        fail("INVALID_REQUEST", "invalid boundary request field types", 64)
    print(run_cg(args.binary_path, ["boundary-audit"], json.dumps(request)))


def cmd_select_route(args: argparse.Namespace) -> None:
    output = run_cg(args.binary_path, ["select-route", "--query", args.query or ""])
    print(output)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="context-governor high_roi audit wrapper"
    )
    parser.add_argument(
        "--binary-path",
        default=DEFAULT_BINARY,
        help="path to context-governor binary",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("audit-tool-surface")
    p.add_argument("--tools-json", help="JSON array of {name, description}")
    p.set_defaults(func=cmd_audit_tool_surface)

    p = sub.add_parser("audit-compression-boundary")
    p.add_argument("--request-json", help="JSON compression boundary audit request")
    p.set_defaults(func=cmd_audit_compression_boundary)

    p = sub.add_parser("eval-governed-memory")
    p.add_argument("--harness-id")
    p.add_argument("--cases-json", help="JSON array of GovernanceCase")
    p.set_defaults(func=cmd_eval_governed_memory)

    p = sub.add_parser("eval-rag-leakage")
    p.add_argument("--task-id")
    p.add_argument(
        "--closed-book-correct", action="store_true", help="Model was correct without retrieval"
    )
    p.add_argument(
        "--retrieved-correct", action="store_true", help="Model was correct with retrieval"
    )
    p.add_argument(
        "--retrieval-used", action="store_true", default=True, help="Retrieval was used"
    )
    p.set_defaults(func=cmd_eval_rag_leakage)

    p = sub.add_parser("screen-conflicts")
    p.add_argument("--claims-json", help="JSON array of {id, text}")
    p.set_defaults(func=cmd_screen_conflicts)

    p = sub.add_parser("select-route")
    p.add_argument("--query", required=True)
    p.set_defaults(func=cmd_select_route)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()