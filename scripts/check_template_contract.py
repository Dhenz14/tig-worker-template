#!/usr/bin/env python3
"""Validate the public TIG worker template contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def documented_commands(document: str, token: str) -> list[str]:
    lines = document.splitlines()
    commands: list[str] = []
    line_index = 0
    while line_index < len(lines):
        line = lines[line_index]
        if token in line:
            block = [line.strip()]
            while block[-1].rstrip().endswith("\\") and line_index + 1 < len(lines):
                line_index += 1
                block.append(lines[line_index].strip())
            commands.append(" ".join(part.rstrip("\\").strip() for part in block))
        line_index += 1
    return commands


def has_cli_flag(command: str, flag: str) -> bool:
    return re.search(rf"(^|\s){re.escape(flag)}(?:=|\s|$)", command) is not None


def require_signed_submit_docs(document: str, label: str) -> None:
    commands = documented_commands(document, "hiveai tig submit")
    require(commands, f"{label} must document hiveai tig submit")
    for command in commands:
        require(has_cli_flag(command, "--key"), f"{label} submit docs must include --key")
        require(has_cli_flag(command, "--host"), f"{label} submit docs must include --host")


def main() -> int:
    capabilities = read("capabilities.yaml")
    publish = read("PUBLISH.md")
    readme = read("README.md")
    makefile = read("Makefile")
    example_solution = read("example_solution.py")

    require("repo: tig-worker-template" in capabilities, "capabilities.yaml must declare repo")
    require("schema_version: hiveai.unified_capability.v1" in capabilities, "capabilities.yaml must use canonical schema")
    require("contracts:" in capabilities, "capabilities.yaml must define contracts")
    require(not re.search(r"^\\s+status:", capabilities, re.MULTILINE), "capabilities.yaml must not use legacy status")
    require(not re.search(r"^\\s+source_file:", capabilities, re.MULTILINE), "capabilities.yaml must not use legacy source_file")
    require(capabilities.count("gap_status: LIVE") == 7, "capabilities.yaml must expose seven LIVE surfaces")

    for feature in [
        "tig-list-challenges",
        "tig-fetch-challenge",
        "tig-rehearse-solution",
        "tig-submit-solution",
        "tig-auto-mine",
        "tig-keygen",
        "tig-leaderboard",
    ]:
        require(f"feature: {feature}" in capabilities, f"missing capability {feature}")

    stale_publish_phrases = [
        "currently lives inside the Hive-AI monorepo",
        "promote it to its own repo",
        "gh repo create Dhenz14/tig-worker-template",
        "One-time publish",
    ]

    for phrase in stale_publish_phrases:
        require(phrase not in publish, f"PUBLISH.md still contains stale phrase: {phrase}")

    require("is already the public standalone repository" in publish, "PUBLISH.md must state the current public repo posture")

    forbidden_model_literals = [
        "claude:opus-4-7",
        "gpt-4",
        "gemini",
    ]

    for phrase in forbidden_model_literals:
        require(phrase not in readme, f"README.md hardcodes model literal: {phrase}")
        require(phrase not in makefile, f"Makefile hardcodes model literal: {phrase}")

    require('MODEL=<provider:model>' in readme, "README.md must show BYOM model selection")
    require("MODEL ?= $(HIVEAI_TIG_MODEL)" in makefile, "Makefile must default MODEL from HIVEAI_TIG_MODEL")
    require(re.search(r"Set MODEL=<provider:model> or HIVEAI_TIG_MODEL", makefile), "Makefile auto-mine must fail closed without a model")
    require_signed_submit_docs(readme, "README.md")
    require_signed_submit_docs(example_solution, "example_solution.py")

    print("[tig-template-contract] PASS: canonical capabilities, current publish docs, BYOM auto-mine, signed submit docs")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"[tig-template-contract] FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
