# Raw Corpus

This folder is the local cache for raw EVCHK wiki text used for exact-source lookup during skill execution. It sits outside `hk-copypasta-style/` so the installable skill stays compact.

**This folder is empty in a fresh clone.** The corpus is not committed to the repo (see the root `NOTICE.md` for licensing rationale). Populate it from the project root with:

```powershell
python ..\hk-copypasta-style\scripts\fetch_evchk_corpus.py --from-index --include-seeds --timeout 30 --sleep 0.1 --resume
```

Or, from the repo root:

```powershell
python .\hk-copypasta-style\scripts\fetch_evchk_corpus.py --from-index --include-seeds --timeout 30 --sleep 0.1 --resume
```

After running, this folder contains:

- `manifest.json` — fetched-file registry, including dead/missing index links.
- `<source-id>.wiki.txt` — one raw wikitext file per source, with source URL, fetch timestamp, and revision timestamp in the header.

Re-run the same command at any time to refresh.
