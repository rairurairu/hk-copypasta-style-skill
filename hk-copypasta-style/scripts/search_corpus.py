#!/usr/bin/env python3
"""Search an EVCHK raw-corpus manifest without loading it into prompt context."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def resolve_local_file(manifest_path: Path, local_file: str) -> Path:
    raw_path = Path(local_file)
    if raw_path.is_absolute():
        return raw_path

    manifest_path = manifest_path.resolve()
    candidates = [
        Path.cwd() / raw_path,
        manifest_path.parent / raw_path.name,
        manifest_path.parent.parent.parent / raw_path,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[-1]


def score_item(item: dict, terms: list[str]) -> int:
    title = str(item.get("title", "")).casefold()
    item_id = str(item.get("id", "")).casefold()
    url = str(item.get("url", "")).casefold()

    score = 0
    for term in terms:
        if not term:
            continue
        needle = term.casefold()
        if needle == title:
            score += 100
        if needle in title:
            score += 25
        if needle in item_id:
            score += 10
        if needle in url:
            score += 3
    return score


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default="../research/raw-corpus/manifest.json")
    parser.add_argument("--query", required=True, help="Space-separated title/topic terms.")
    parser.add_argument("--limit", type=int, default=12)
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"manifest not found: {manifest_path}", file=sys.stderr)
        return 2

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    terms = args.query.replace("，", " ").replace(",", " ").split()

    scored = []
    for item in data.get("items", []):
        score = score_item(item, terms)
        if score:
            scored.append((score, item))

    scored.sort(key=lambda pair: (-pair[0], pair[1].get("title", "")))

    for score, item in scored[: args.limit]:
        local_file = str(item.get("local_file", ""))
        resolved_file = resolve_local_file(manifest_path, local_file) if local_file else Path("")
        print(
            "\t".join(
                [
                    str(score),
                    str(item.get("id", "")),
                    str(item.get("title", "")),
                    str(item.get("sensitivity", "")),
                    local_file,
                    str(resolved_file),
                ]
            )
        )

    if not scored:
        print("NO_MATCH")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
