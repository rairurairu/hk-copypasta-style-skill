#!/usr/bin/env python3
"""Fetch EVCHK wiki pages into a raw research corpus outside the skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


API_URL = "https://evchk.fandom.com/zh/api.php"
INDEX_TITLE = "潮文"

CAUTION_KEYWORDS = [
    "女友",
    "毒撚",
    "屌",
    "姦",
    "肉便器",
    "叫雞",
    "打飛機",
    "淫",
    "AV",
]

SEED_SOURCES = [
    {
        "id": "huo-nam-romantic-object",
        "title": "火腩飯潮文",
        "url": "https://evchk.fandom.com/zh/wiki/%E7%81%AB%E8%85%A9%E9%A3%AF%E6%BD%AE%E6%96%87",
        "sensitivity": "safe",
    },
    {
        "id": "ga-je-rumor-escalation",
        "title": "家姐被炒潮文",
        "url": "https://evchk.fandom.com/zh/wiki/%E5%AE%B6%E5%A7%90%E8%A2%AB%E7%82%92%E6%BD%AE%E6%96%87",
        "sensitivity": "caution-real-person-allegation-style",
    },
    {
        "id": "forum-definition",
        "title": "有人問我 : 高登係一個點既論壇?",
        "url": "https://evchk.fandom.com/zh/wiki/%E6%9C%89%E4%BA%BA%E5%95%8F%E6%88%91_%3A_%E9%AB%98%E7%99%BB%E4%BF%82%E4%B8%80%E5%80%8B%E9%BB%9E%E6%97%A2%E8%AB%96%E5%A3%87%3F",
        "sensitivity": "safe",
    },
    {
        "id": "public-scene-punchline",
        "title": "女友一句，全車靜晒",
        "url": "https://evchk.fandom.com/zh/wiki/%E5%A5%B3%E5%8F%8B%E4%B8%80%E5%8F%A5%EF%BC%8C%E5%85%A8%E8%BB%8A%E9%9D%9C%E6%99%92",
        "sensitivity": "caution-crude-source",
    },
    {
        "id": "mc-hardship-romance",
        "title": "男人一生，只為尋覓一個肯同自己挨麥記嘅女人",
        "url": "https://evchk.fandom.com/zh/wiki/%E7%94%B7%E4%BA%BA%E4%B8%80%E7%94%9F%EF%BC%8C%E5%8F%AA%E7%82%BA%E5%B0%8B%E8%A6%93%E4%B8%80%E5%80%8B%E8%82%AF%E5%90%8C%E8%87%AA%E5%B7%B1%E6%8C%A8%E9%BA%A5%E8%A8%98%E5%98%85%E5%A5%B3%E4%BA%BA",
        "sensitivity": "safe",
    },
    {
        "id": "food-1999-counter",
        "title": "大家樂白汁雞皇飯潮文",
        "url": "https://evchk.fandom.com/zh/wiki/%E5%A4%A7%E5%AE%B6%E6%A8%82%E7%99%BD%E6%B1%81%E9%9B%9E%E7%9A%87%E9%A3%AF%E6%BD%AE%E6%96%87",
        "sensitivity": "safe",
    },
    {
        "id": "premium-cheap-object",
        "title": "82年百事潮文",
        "url": "https://evchk.fandom.com/zh/wiki/82%E5%B9%B4%E7%99%BE%E4%BA%8B%E6%BD%AE%E6%96%87",
        "sensitivity": "safe",
    },
    {
        "id": "tech-tribal-wisdom",
        "title": "Android潮文",
        "url": "https://evchk.fandom.com/zh/wiki/Android%E6%BD%AE%E6%96%87",
        "sensitivity": "caution-gendered-source",
    },
    {
        "id": "mtr-apology-slogan",
        "title": "港鐵唔好意思廣告討論熱潮",
        "url": "https://evchk.fandom.com/zh/wiki/%E6%B8%AF%E9%90%B5%E5%94%94%E5%A5%BD%E6%84%8F%E6%80%9D%E5%BB%A3%E5%91%8A%E8%A8%8E%E8%AB%96%E7%86%B1%E6%BD%AE",
        "sensitivity": "mild-public-affairs",
    },
    {
        "id": "jackie-ad-testimonial",
        "title": "成龍洗頭水潮文",
        "url": "https://evchk.fandom.com/zh/wiki/%E6%88%90%E9%BE%8D%E6%B4%97%E9%A0%AD%E6%B0%B4%E6%BD%AE%E6%96%87",
        "sensitivity": "safe",
    },
    {
        "id": "see-gum-dik-setup",
        "title": "是咁的",
        "url": "https://evchk.fandom.com/zh/wiki/%E6%98%AF%E5%92%81%E7%9A%84",
        "sensitivity": "safe",
    },
    {
        "id": "cold-breath-concern",
        "title": "我不禁倒抽一口涼氣",
        "url": "https://evchk.fandom.com/zh/wiki/%E6%88%91%E4%B8%8D%E7%A6%81%E5%80%92%E6%8A%BD%E4%B8%80%E5%8F%A3%E6%B6%BC%E6%B0%A3",
        "sensitivity": "mild-public-affairs",
    },
]


def default_output_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "research" / "raw-corpus"


def wiki_url(title: str) -> str:
    return "https://evchk.fandom.com/zh/wiki/" + urllib.parse.quote(title.replace(" ", "_"), safe="")


def ascii_id(title: str, prefix: str = "evchk") -> str:
    digest = hashlib.sha1(title.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"


def classify_sensitivity(title: str) -> str:
    if any(keyword in title for keyword in CAUTION_KEYWORDS):
        return "caution-offensive-or-crude-source"
    return "unreviewed"


def fetch_index_titles(index_title: str, timeout: int) -> list[str]:
    params = {
        "action": "parse",
        "page": index_title,
        "prop": "links",
        "format": "json",
        "formatversion": "2",
    }
    url = API_URL + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": "hk-copypasta-style-corpus-fetch/1.1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))

    titles = []
    seen = set()
    for link in payload.get("parse", {}).get("links", []):
        if link.get("ns") != 0:
            continue
        title = link.get("title", "").strip()
        if not title or title == index_title or title in seen:
            continue
        seen.add(title)
        titles.append(title)
    return titles


def sources_from_index(index_title: str, timeout: int) -> list[dict]:
    sources = []
    for title in fetch_index_titles(index_title, timeout):
        sensitivity = classify_sensitivity(title)
        sources.append({
            "id": ascii_id(title),
            "title": title,
            "url": wiki_url(title),
            "sensitivity": sensitivity,
            "origin": f"index:{index_title}",
        })
    return sources


def merge_sources(*source_lists: list[dict]) -> list[dict]:
    merged = []
    seen_titles = set()
    for source_list in source_lists:
        for source in source_list:
            title = source["title"]
            if title in seen_titles:
                continue
            seen_titles.add(title)
            merged.append(source)
    return merged


def fetch_wikitext(title: str, timeout: int) -> dict:
    params = {
        "action": "query",
        "prop": "revisions",
        "rvprop": "content|timestamp",
        "titles": title,
        "format": "json",
        "formatversion": "2",
    }
    url = API_URL + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": "hk-copypasta-style-corpus-fetch/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))

    page = payload["query"]["pages"][0]
    if page.get("missing"):
        raise RuntimeError(f"missing page: {title}")

    revision = page["revisions"][0]
    content = revision.get("content")
    if content is None:
        content = revision.get("slots", {}).get("main", {}).get("content", "")

    return {
        "pageid": page.get("pageid"),
        "title": page.get("title", title),
        "revision_timestamp": revision.get("timestamp"),
        "content": content,
    }


def write_source(output_dir: Path, source: dict, fetched: dict, fetched_at: str) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{source['id']}.wiki.txt"
    header = [
        f"Title: {fetched['title']}",
        f"Source URL: {source['url']}",
        f"Fetched at: {fetched_at}",
        f"Revision timestamp: {fetched.get('revision_timestamp') or 'unknown'}",
        f"Sensitivity: {source['sensitivity']}",
        "Upstream text license: CC BY-SA 3.0 unless otherwise noted on the source page.",
        "Attribution: 香港網絡大典 contributors at Fandom; see Source URL and page history.",
        "",
        "This raw wikitext is research material. Do not bundle it into the installable skill.",
        "",
        "---",
        "",
    ]
    path.write_text("\n".join(header) + fetched["content"], encoding="utf-8")
    return {
        **source,
        "pageid": fetched.get("pageid"),
        "revision_timestamp": fetched.get("revision_timestamp"),
        "local_file": local_file_ref(path),
    }


def cached_source(output_dir: Path, source: dict) -> dict | None:
    path = output_dir / f"{source['id']}.wiki.txt"
    if not path.exists():
        return None
    return {
        **source,
        "pageid": None,
        "revision_timestamp": None,
        "local_file": local_file_ref(path),
        "cached": True,
    }


def local_file_ref(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()).as_posix())
    except ValueError:
        return str(path.as_posix())


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=default_output_dir(), help="directory for raw wiki text")
    parser.add_argument("--timeout", type=int, default=20, help="HTTP timeout in seconds")
    parser.add_argument("--sleep", type=float, default=0.2, help="delay between requests")
    parser.add_argument("--dry-run", action="store_true", help="print selected pages without fetching")
    parser.add_argument("--from-index", action="store_true", help="crawl links from the EVCHK 潮文 index")
    parser.add_argument("--index-title", default=INDEX_TITLE, help="EVCHK page title to crawl when --from-index is used")
    parser.add_argument("--include-seeds", action="store_true", help="include the curated seed set with an index crawl")
    parser.add_argument("--max-pages", type=int, default=0, help="limit fetched pages after filtering; 0 means no limit")
    parser.add_argument("--resume", action="store_true", help="skip already fetched files and include them in the manifest")
    args = parser.parse_args()

    if args.from_index:
        index_sources = sources_from_index(args.index_title, args.timeout)
        sources = merge_sources(SEED_SOURCES if args.include_seeds else [], index_sources)
    else:
        sources = SEED_SOURCES

    if args.max_pages > 0:
        sources = sources[: args.max_pages]

    if args.dry_run:
        for source in sources:
            print(f"{source['id']}\t{source['title']}\t{source['sensitivity']}")
        return 0

    fetched_at = datetime.now(timezone.utc).isoformat()
    manifest = []
    errors = []

    for source in sources:
        if args.resume:
            cached = cached_source(args.output, source)
            if cached:
                manifest.append(cached)
                print(f"[CACHED] {source['id']}: {source['title']}")
                continue
        try:
            fetched = fetch_wikitext(source["title"], args.timeout)
            manifest.append(write_source(args.output, source, fetched, fetched_at))
            print(f"[OK] {source['id']}: {fetched['title']}")
            time.sleep(args.sleep)
        except Exception as exc:  # noqa: BLE001 - report and continue corpus fetches.
            errors.append({"id": source["id"], "title": source["title"], "error": str(exc)})
            print(f"[FAIL] {source['id']}: {exc}", file=sys.stderr)

    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "manifest.json").write_text(
        json.dumps(
            {
                "fetched_at": fetched_at,
                "source": API_URL,
                "mode": "index" if args.from_index else "seed",
                "index_title": args.index_title if args.from_index else None,
                "items": manifest,
                "errors": errors,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
