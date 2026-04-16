# HK Copypasta Style Skill

A `SKILL.md` skill for both **Claude Code** and **Codex** that writes custom Hong Kong forum-style 潮文 in Traditional Chinese/Cantonese. It takes a user topic, opinion, product, event, or statement, then rewrites it using the structure and rhythm of a referenced 潮文.

Traditional Chinese version (default): `README.md`

This skill and its bundled research corpus are provided for learning and research purposes only, especially for studying Hong Kong internet writing patterns, remix structures, and style transformation. Do not use it to impersonate original authors, mislead readers about authorship, or republish source articles as original work.

## Contents

- `hk-copypasta-style/`: the installable skill (works for both Claude Code and Codex).
- `hk-copypasta-style/references/source_index.md`: curated source list and source IDs.
- `hk-copypasta-style/references/style_profiles.md`: distilled structure and beat profiles.
- `hk-copypasta-style/scripts/fetch_evchk_corpus.py`: utility for fetching source wikitext.
- `research/raw-corpus/`: local cache for raw EVCHK/Fandom wikitext. **Not committed to this repo** — populated by running the fetcher (see Setup).

## Usage

Use prompts that name the source 潮文 and the new topic:

```text
參考白汁雞皇飯潮文仿作一篇爆旋陀螺的文章
用爆旋陀螺重寫火腩飯潮文
仿Android潮文寫一篇關於Linux桌面嘅潮文
```

When a named source appears in `source_index.md`, the skill should read the matching raw file from:

```text
research/raw-corpus/<source-id>.wiki.txt
```

For other EVCHK sources, use `research/raw-corpus/manifest.json` to resolve the title to a local raw file.

If the requested source article is not listed in `source_index.md` and cannot be found in the raw corpus manifest, the skill should not invent the source structure. Ask the user to paste the original article, or ask for permission to search the web for it.

## Setup

The raw EVCHK wikitext corpus is **not bundled** with this repo (see `NOTICE.md` for licensing). Fetch it locally before activating the skill:

```powershell
python .\hk-copypasta-style\scripts\fetch_evchk_corpus.py --from-index --include-seeds --timeout 30 --sleep 0.1 --resume
```

This populates `research/raw-corpus/` with `manifest.json` and one `<source-id>.wiki.txt` per article, with source URL, revision timestamp, and attribution metadata in each file header. Re-run the same command to refresh later.

The skill works without the corpus by falling back to the curated profiles in `hk-copypasta-style/references/style_profiles.md`, but exact-source lookup, fusion, and automatic corpus-wide selection require the fetched corpus.

## Activation

### Codex

Install the skill and raw corpus as siblings under your Codex skills folder:

```powershell
$skills = "$env:USERPROFILE\.codex\skills"
New-Item -ItemType Directory -Force $skills | Out-Null
Copy-Item -Recurse -Force .\hk-copypasta-style $skills
Copy-Item -Recurse -Force .\research $skills
```

Start a new Codex session, then either let the skill activate from a matching request or mention it explicitly:

```text
Use $hk-copypasta-style 參考白汁雞皇飯潮文仿作一篇爆旋陀螺的文章
```

### Claude Code

Claude Code also supports `SKILL.md` skills. For a personal skill:

```powershell
$skills = "$env:USERPROFILE\.claude\skills"
New-Item -ItemType Directory -Force $skills | Out-Null
Copy-Item -Recurse -Force .\hk-copypasta-style $skills
Copy-Item -Recurse -Force .\research $skills
```

Restart Claude Code. Claude can auto-use the skill when the request matches, or you can invoke it directly as a slash command:

```text
/hk-copypasta-style 參考白汁雞皇飯潮文仿作一篇爆旋陀螺的文章
```

For a project-level Claude Code skill, place the skill at `.claude/skills/hk-copypasta-style/` and keep `research/raw-corpus/` at the repository root.

## Credits

This project uses and transforms text/reference material from 香港網絡大典 on Fandom, especially the 潮文 index:

https://evchk.fandom.com/zh/wiki/%E6%BD%AE%E6%96%87

See `NOTICE.md` for attribution and licensing notes. This project is not affiliated with 香港網絡大典, Fandom, 高登討論區, LIHKG, or any referenced communities.
