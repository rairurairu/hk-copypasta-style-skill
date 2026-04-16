# HK Copypasta Style Skill

這是一個 `SKILL.md` skill（同時支援 Claude Code 同 Codex），用嚟學習同研究香港網絡潮文嘅寫法。佢會根據使用者提供嘅題材、立場、產品、事件或陳述，參考指定潮文嘅結構、節奏同語氣，仿作成一段新嘅繁體中文／港式中文文章。

English version: `README.en.md`

本 skill 及其研究語料只供學習和研究用途，主要用來分析香港網絡文字風格、改寫結構和語氣轉換方式。請勿用作冒充原作者、誤導讀者文章出處，或將來源文章當成自己的原創作品重新發布。

## 內容

- `hk-copypasta-style/`：可安裝的 skill（同時支援 Claude Code 及 Codex）。
- `hk-copypasta-style/references/source_index.md`：精選來源清單及來源 ID。
- `hk-copypasta-style/references/style_profiles.md`：整理後的結構、節奏和風格 profile。
- `hk-copypasta-style/scripts/fetch_evchk_corpus.py`：抓取來源 wikitext 的工具。
- `research/raw-corpus/`：本地 EVCHK/Fandom 原始 wikitext 暫存資料夾。**不會包含在這個 repo**，需自行執行 fetcher 抓取（見「初次設定」）。

## 用法

使用時應明確指出想參考哪一篇潮文，以及新的題材：

```text
參考白汁雞皇飯潮文仿作一篇爆旋陀螺的文章
用爆旋陀螺重寫火腩飯潮文
仿Android潮文寫一篇關於Linux桌面嘅潮文
```

當指定來源出現在 `source_index.md`，skill 應先讀取相應原文：

```text
research/raw-corpus/<source-id>.wiki.txt
```

如果是其他 EVCHK 來源，則使用 `research/raw-corpus/manifest.json` 將標題對應到本地原文檔案。

如果指定來源不在 `source_index.md`，亦不能在 raw corpus manifest 找到，skill 不應憑空猜測原文結構。它應要求使用者貼上原文，或先取得使用者同意後再搜尋網頁。

## 初次設定

EVCHK 原始 wikitext 語料**不會包含在這個 repo 內**（授權說明見 `NOTICE.zh-Hant.md`）。啟用 skill 之前，先在本地執行 fetcher 抓取一次：

```powershell
python .\hk-copypasta-style\scripts\fetch_evchk_corpus.py --from-index --include-seeds --timeout 30 --sleep 0.1 --resume
```

抓取完成後，`research/raw-corpus/` 會出現 `manifest.json` 及每篇來源對應的 `<source-id>.wiki.txt`，每個檔案 header 都會寫入來源 URL、修訂時間及出處標示。日後想更新語料，再執行同一條指令即可。

如果未抓取語料，skill 仍可使用，但只會 fallback 到 `hk-copypasta-style/references/style_profiles.md` 入面 curated 的 profile。需要精確查閱原文、融合多篇潮文、或讓 skill 自動由整個語料庫揀選來源時，必須先抓取語料。

## 啟用方式

### Codex

將 skill 和 raw corpus 以相鄰資料夾形式安裝到 Codex skills folder：

```powershell
$skills = "$env:USERPROFILE\.codex\skills"
New-Item -ItemType Directory -Force $skills | Out-Null
Copy-Item -Recurse -Force .\hk-copypasta-style $skills
Copy-Item -Recurse -Force .\research $skills
```

開新的 Codex session 後，可以讓 skill 根據請求自動觸發，或明確指定：

```text
Use $hk-copypasta-style 參考白汁雞皇飯潮文仿作一篇爆旋陀螺的文章
```

### Claude Code

Claude Code 亦支援 `SKILL.md` skills。安裝成個人 skill：

```powershell
$skills = "$env:USERPROFILE\.claude\skills"
New-Item -ItemType Directory -Force $skills | Out-Null
Copy-Item -Recurse -Force .\hk-copypasta-style $skills
Copy-Item -Recurse -Force .\research $skills
```

重啟 Claude Code 後，Claude 可以按請求自動使用 skill，也可以直接用 slash command：

```text
/hk-copypasta-style 參考白汁雞皇飯潮文仿作一篇爆旋陀螺的文章
```

如要安裝成 Claude Code project-level skill，將 skill 放在 `.claude/skills/hk-copypasta-style/`，並將 `research/raw-corpus/` 保留在 repository root。

## 鳴謝

本專案使用及轉化來自 Fandom「香港網絡大典」的文字／參考資料，尤其是「潮文」索引：

https://evchk.fandom.com/zh/wiki/%E6%BD%AE%E6%96%87

詳細出處及授權說明見 `NOTICE.zh-Hant.md` 及 `NOTICE.md`。本專案與香港網絡大典、Fandom、高登討論區、LIHKG 或任何被引用社群均無從屬或官方關係。
