# HK Copypasta Style

`hk-copypasta-style` is a `SKILL.md` skill for generating Hong Kong forum 潮文/copypasta-style writing in Traditional Chinese/Cantonese. It rewrites a user-provided topic or stance through a selected HK copypasta structure while preserving source rhythm, approximate length, and comic timing.

The skill works with both **Claude Code** and **Codex**.

To trigger it, mention `$hk-copypasta-style` or `hk-copypasta-style` in a prompt. In Claude Code you can also invoke `/hk-copypasta-style` directly; in Codex, prefer the `$`-prefixed or plain mention because slash commands can be intercepted by the client before the skill is reached.

## Install

### Codex

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.codex\skills\hk-copypasta-style"
```

### Claude Code

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.claude\skills\hk-copypasta-style"
```

Restart or reload the host so the skill metadata is discovered. For project-scope use in Claude Code, place the folder at `.claude/skills/hk-copypasta-style/` inside your project instead.

## Usage

### Create From A Topic

If no genre/source 潮文 is named, the skill chooses across the available corpus genres and archetypes.

```text
hk-copypasta-style 三哥過橋米線
```

### Beat-By-Beat Rewrite

Name a source 潮文 and a new topic. The skill follows the source sentence order, emotional turns, repeated structures, and ending rhythm.

```text
hk-copypasta-style 用火腩飯潮文改寫三哥過橋米線
```

### Named Profile

Use a built-in profile or alias from `references/style_profiles.md`.

```text
hk-copypasta-style 潮文：白水 topic：十八件麥樂雞
```

Here `白水` resolves to `baak-seoi-argument-correction`, while `十八件麥樂雞` remains the main topic. The profile supplies structure and stance; it does not lock the output to the profile's original subject matter.

### Fusion Mode

Blend multiple source families. One source supplies the primary skeleton; secondary sources add diction, motifs, escalation devices, slogan shape, or punchline flavor.

```text
hk-copypasta-style 用火腩飯做骨架，加82年百事語氣，寫便利店叮飯
```

### Pasted Source

Paste an unindexed source and ask the skill to transform that structure.

```text
hk-copypasta-style 以下係原文，幫我改成關於X
```

### Useful Controls

- `mild`, `medium`, `aggressive`
- `少啲粗口`, `粗口多啲`
- `更LIHKG`, `更文青`, `更荒謬`
- `短啲`, `長啲`, `一句起兩句止`
- `beat map only`
- `side-by-side beat map`
- `出3個版本：火腩飯、白汁雞皇飯、82年百事`

## Behavior Rules

- Preserve source structure and approximate length by default.
- Keep short source forms short; do not inflate them into essays unless asked.
- If a topic already appears in the corpus as a 仿作例子, avoid reusing that same source skeleton unless explicitly requested.
- If the user gives `topic:`, that topic remains the main content even when a named profile is used.
- Prefer transformed structure over copied source text.
- Output only the finished paragraph unless the user asks for variants, notes, or analysis.

## References And Corpus

The installable skill includes distilled profiles and routing notes only:

- `references/style_profiles.md`
- `references/source_index.md`
- `references/corpus_router.md`

Raw EVCHK/Fandom wikitext is not bundled. To build a local research corpus outside the skill:

```powershell
python .\scripts\fetch_evchk_corpus.py --from-index --include-seeds --timeout 30 --sleep 0.1 --resume
```

The generated corpus is written to `../research/raw-corpus/` by default and is ignored by git. Use `scripts/search_corpus.py` to search a generated manifest:

```powershell
python .\scripts\search_corpus.py --manifest ..\research\raw-corpus\manifest.json --query "火腩飯"
```

Generated raw corpus files include upstream attribution headers. Review upstream licensing before redistributing generated corpus data.

## Repository Layout

```text
SKILL.md                    # Skill instructions and trigger metadata (read by Claude Code and Codex)
agents/openai.yaml          # Codex-only UI metadata; ignored by Claude Code
references/                 # Distilled profiles and routing notes
scripts/                    # Optional corpus helper scripts
LICENSE                     # Project license for this skill folder
NOTICE                      # Upstream attribution and affiliation notice
```

## License

This repository's original code and documentation are released under the MIT License. See `LICENSE`.

Optional raw corpus data fetched from EVCHK/Fandom is not included in this repository and remains under its upstream license, typically CC BY-SA 3.0 unless an upstream page states otherwise. See `NOTICE`.
