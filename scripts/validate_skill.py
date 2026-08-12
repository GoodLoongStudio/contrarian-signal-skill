#!/usr/bin/env python3
"""Lightweight repository validator for contrarian-signal-skill."""
from __future__ import annotations

import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_FILES = [
    "SKILL.md",
    "references/risk-and-compliance.md",
    "references/evidence-ladder.md",
    "references/research-sources.md",
    "references/public-person-evaluation.md",
    "references/event-model.md",
    "references/scoring-rules.md",
    "references/style-model.md",
    "assets/report-template.md",
    "evals/test-cases.md",
    "agents/openai.yaml",
    "scripts/calc_score.py",
]


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter closing delimiter missing")
    data: dict[str, str] = {}
    for line in text[4:end].strip().splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data


def main() -> None:
    root = (Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()).resolve()
    errors: list[str] = []

    skill = root / "SKILL.md"
    if not skill.exists():
        errors.append("missing SKILL.md")
    else:
        try:
            data = parse_frontmatter(skill.read_text(encoding="utf-8"))
        except ValueError as exc:
            errors.append(str(exc))
            data = {}

        name = data.get("name", "")
        description = data.get("description", "")
        if not name:
            errors.append("frontmatter.name is required")
        elif not NAME_RE.match(name):
            errors.append("name must use lowercase letters, numbers, and hyphens")
        if len(name) > 64:
            errors.append("name exceeds 64 characters")
        if name and root.name != name:
            errors.append(f"parent directory '{root.name}' must match name '{name}'")
        if not description:
            errors.append("frontmatter.description is required")
        elif len(description) > 1024:
            errors.append(f"description exceeds 1024 characters: {len(description)}")

        body = skill.read_text(encoding="utf-8")
        required_phrases = [
            "不构成投资建议",
            "不生成买卖指令",
            "PARTIAL",
            "ACTION",
            "OPINION",
        ]
        for phrase in required_phrases:
            if phrase not in body:
                errors.append(f"SKILL.md missing required safety/method phrase: {phrase}")

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"missing required file: {rel}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    print(f"OK: {root.name}; release structure and safety boundary validated")


if __name__ == "__main__":
    main()
