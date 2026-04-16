---
name: hk-copypasta-style
description: Generate a custom Hong Kong forum 潮文/copypasta paragraph in Traditional Chinese/Cantonese from a user-provided topic, opinion, product, brand, event, or statement. Use when the user writes $hk-copypasta-style, hk-copypasta-style, asks to activate/use the HK copypasta skill, explicitly mentions 潮文, 仿作, 改寫, 重寫, 參考某篇潮文, asks to automatically choose from the EVCHK/reference corpus, asks to mix/fuse/combine/融合/混合/混搭 multiple 潮文 styles, or asks for prompts like "參考白汁雞皇飯潮文仿作一篇關於X的文章", "用X重寫火腩飯潮文", "將Android潮文改成X版", or "以是咁的開頭寫一篇X潮文". Covers the full local EVCHK raw-corpus manifest when available, plus curated 香港網絡大典/Gordon/LIHKG-style profiles such as 火腩飯 romantic monologue, 家姐被炒 rumor escalation, food/consumer/transport/ad parody, forum reply rants, public-scene punchlines, and "是咁的" setup posts.
---

# HK Copypasta Style

Generate one polished HK 潮文-style paragraph by default. If the user does not name a genre/source 潮文, choose freely across all available corpus genres and archetypes before drafting. After selecting a source family, preserve its rhythm, structure, and rhetorical moves while rebuilding the wording around the user's topic and stance.

Activation note: skills auto-activate from the frontmatter `name` and `description`, or from explicit `$hk-copypasta-style` / `hk-copypasta-style` mentions. `/hk-copypasta-style` is a slash command and may be intercepted by the client before Codex can use this skill.

Use this skill for learning and research purposes only: study structure, rhythm, and transformation patterns; do not impersonate original authors or present copied source material as original work.

Default rewrite mode is close structural imitation only after a source family has been selected. Retain the chosen source's sentence count, sentence order, clause shape, punctuation rhythm, repeated wording pattern, and approximate length as much as possible. If the user gives only a topic, first select from the full corpus/archetype space; do not assume one of the curated profiles by default. Avoid adding or deleting sentences and avoid adding extra explanatory words unless the user explicitly asks for a looser rewrite, stronger parody, more jokes, or a different length.

## Trigger Examples

Use this skill for requests phrased like:

- `參考白汁雞皇飯潮文仿作一篇爆船陀螺的文章`
- `用爆船陀螺重寫白汁雞皇飯潮文`
- `將火腩飯潮文改成Cursor太貴但又真係好用版`
- `仿Android潮文寫一篇關於Linux桌面嘅潮文`
- `以是咁的開頭，寫一篇關於AI寫code要review嘅潮文`
- `參考82年百事潮文，寫一篇講便利店叮飯嘅文`
- `自動喺reference入面揀最啱嘅潮文，寫一篇關於三哥米線`
- `融合火腩飯同Android潮文，寫一篇關於Cursor嘅潮文`
- `十八件麥樂雞`  # no genre/source named; choose across all corpus genres
- `潮文：白水 topic：十八件麥樂雞`  # 白水 is a style profile alias; topic is the payload

## Workflow

1. Extract the user's payload:
   - topic/object/person/event
   - opinion or statement to express
   - named reference/profile key, if any, such as `潮文：白水`, `reference 白水`, or `參考 白水`
   - requested source style, if any
   - tone intensity: mild, medium, aggressive; default to medium
   - constraints: names to avoid, vulgarity level, source tone
2. Resolve named reference/profile notes:
   - Parse labeled prompt fields before choosing a source. Recognize `topic:`, `topic：`, `題目:`, `題目：`, `主題:`, `主題：` as the payload/topic field.
   - Recognize `潮文:`, `潮文：`, `style:`, `style：`, `genre:`, `genre：`, `reference:`, `reference：`, `參考:`, and `參考：` as a possible source-style or reference field.
   - Resolve the field value against profile IDs and aliases in `references/style_profiles.md`.
   - If a `潮文:`/`style:`/`genre:` field value matches a style profile, use that profile. For example, `潮文：白水 topic：十八件麥樂雞` resolves `白水` to `baak-seoi-argument-correction` and `十八件麥樂雞` as the topic.
   - If the resolved profile has a `Structure`, `Slot map`, or `Length`, obey those constraints unless the user explicitly asks for a freer or longer version.
   - The requested payload/topic remains the main content unless the user explicitly asks to keep the reference's original topic. Slot-map the profile's original subjects, causes, and targets onto the requested topic instead of letting the profile's original topic dominate.
3. Choose a source family:
   - First read `references/corpus_router.md` when the user asks for automatic source selection, names a source outside the curated profile list, asks for fusion, or gives only a topic with no source style.
   - If the user gives only a topic and does not specify a genre/source 潮文, route across all available corpus genres/archetypes. This is the default path, not an optional mode.
   - If `../research/raw-corpus/manifest.json` exists, treat every manifest item as selectable source material. Do not limit selection to the curated profile list in `references/style_profiles.md`.
   - If the user's topic already appears inside the corpus as a derivative, variant, adaptation, or `===[[...]]版===` example, do not use that enclosing source's structure as the primary template. Treat it as a topic collision: use it only to understand what has already been done, then choose a different source family/archetype so the output creates a new transformation.
   - Only use an existing same-topic derivative as the primary structure when the user explicitly asks for that exact derivative/version or asks for beat-by-beat analysis of it.
   - If the user names a source 潮文 listed in `references/source_index.md`, resolve its ID and automatically read the matching raw file from `../research/raw-corpus/<id>.wiki.txt` before drafting.
   - If the user names a source/article not listed in `references/source_index.md`, search `../research/raw-corpus/manifest.json` by title and open the matching `local_file`. Manifest `local_file` values are project-root-relative; from this skill folder, `research/raw-corpus/<file>` usually resolves to `../research/raw-corpus/<file>`. Use `scripts/search_corpus.py` if direct search is faster.
   - After reading the raw file, use a matching distilled profile from `references/style_profiles.md` only when one exists. Otherwise derive a temporary beat map from the raw source using `references/corpus_router.md`.
   - If the user asks for fusion/mix/combine/融合/混合/混搭 mode, resolve all named source families. Use the first named source, or the source explicitly called `primary`, `main`, `骨架`, or `主體`, as the beat skeleton. Use secondary sources only for diction, motifs, framing, escalation devices, and punchline flavor.
   - If the user names a source/article that is not listed in `references/source_index.md` and cannot be resolved through `../research/raw-corpus/manifest.json`, do not guess the source. Ask the user to paste the original article, or ask for permission to search the web for the source.
   - If no style is named, search the manifest, consider all routing archetypes, and inspect 1-3 likely raw files. Fall back to `references/source_index.md` and `references/style_profiles.md` only when corpus search has no clear fit or the raw corpus is unavailable.
4. If the local raw corpus is available, inspect the exact source before drafting:
   - The raw corpus is not bundled inside the installed skill. Resolve corpus paths relative to the current workspace first, not only relative to the skill installation folder.
   - Check for `../research/raw-corpus/manifest.json`, `./research/raw-corpus/manifest.json`, then `../../../research/raw-corpus/manifest.json` when installed as a nested project skill.
   - For curated source-index entries, raw corpus files are normally at `../research/raw-corpus/<source-id>.wiki.txt` when the current workspace is the skill repo.
   - If installed as a nested project skill, also check `../../../research/raw-corpus/<source-id>.wiki.txt`.
   - For expanded index-crawled entries, if `../research/raw-corpus/manifest.json` exists, look up the requested title there, resolve the listed `local_file`, then open that raw source file.
   - If no local raw source can be found for a requested article, stop and request either pasted source text or web-search permission before generating.
   - For EVCHK wikitext, find the relevant `==原文==`, `==翻譯版==`, or named variant section.
   - Extract the exact beat sequence, sentence count, paragraph/line count, rough character length, transitions, price/number logic, repeated punctuation, and ending rhythm.
   - Use that beat map to guide the rewrite. Do not rely only on the rough profile when the exact source is available.
5. Build a slot map before drafting:
   - sacred object or target
   - rejected alternatives
   - scene/location
   - witness or counterparty
   - escalation trigger
   - final identity, slogan, or punchline
6. Draft in Traditional Chinese with Hong Kong Cantonese/forum wording where natural. Keep the user's stance legible; do not let style overwhelm the message.
7. Output only the finished paragraph unless the user asks for variants, notes, or a profile explanation.

## Style Rules

- Use recognizable structures, not verbatim source paragraphs.
- Keep exact source anchor phrases short and sparse, such as `是咁的` or `我不禁倒抽一口涼氣`.
- Prefer exact source beat order over polished generic storytelling when the user names a specific 潮文.
- Length matching is a whole-skill rule. By default, keep the output approximately close to the selected original/profile length, with similar sentence count and paragraph/line count. For short originals, stay short; do not inflate them into essays.
- By default, keep the same number of sentences and do not add/delete sentence-level content. Swap slots and adapt wording inside the original frame.
- Only relax sentence preservation when the user explicitly asks for freer adaptation, stronger criticism, more humor, shorter/longer output, or a different format.
- In fusion mode, keep one primary beat sequence. Do not alternate source styles sentence by sentence or make an equal-weight collage. Add one to three secondary-source signatures, such as a slogan shape, luxury tasting-note diction, customer-service logic break, or forum reply rhythm.
- When the corpus contains an existing same-topic 仿作例子, avoid repeating its source skeleton. Pick a different primary structure and make the new output feel like a fresh 潮文, not a cleaned-up copy of the archived variant.
- Prefer transformed imagery, changed scene details, and new slot values over copied nouns from the source.
- Do not reproduce more than one short sentence from any source example.
- Follow the user's requested stance and intensity. If a claim concerns real people or companies, preserve whether the user is asking for parody, opinion, allegation, or fictionalization rather than imposing a softer stance.
- For a named profile with a required argument skeleton, keep all required moves in order. Do not merely sprinkle reference keywords into an unrelated source structure.
- For any selected source/profile with a `Length` note or extractable raw source, keep close to that length unless the user asks for longer.
- For a named profile, distinguish the profile's original topic from the user's requested topic. The user's requested topic should be visibly central in every major move.
- If the selected profile normally contains slurs, sexual insults, or explicit material, soften by default unless the user explicitly requests a rougher forum tone.

## Profile Use

Use `references/corpus_router.md` to select from the full raw corpus when `../research/raw-corpus/manifest.json` exists. The curated profiles below are safe defaults and reusable archetypes, not a complete list of supported 潮文.

Read only the needed profile from `references/style_profiles.md` when the selected source maps to one of these curated IDs:

- `huo-nam-romantic-object`: absurdly sincere monologue praising a mundane object.
- `ga-je-rumor-escalation`: fake-serious complaint escalating through workplace/customer-service details.
- `forum-definition`: cynical Q&A defining a community, scene, app, workplace, or fandom.
- `public-scene-punchline`: short public-location anecdote ending in silence or exposure.
- `mc-hardship-romance`: relationship/value essay around humble everyday hardship.
- `food-1999-counter`: broken transaction logic and confused counter-service absurdity.
- `premium-cheap-object`: luxury tasting-note treatment of cheap consumer goods.
- `tech-tribal-wisdom`: smug product-tribe superiority and lifestyle philosophy.
- `mtr-apology-slogan`: public-service apology slogan parody.
- `jackie-ad-testimonial`: hesitant testimonial/ad monologue with repeated reassurance.
- `see-gum-dik-setup`: classic forum story opener and setup rhythm.
- `cold-breath-concern`: formal concern sentence with exaggerated moral alarm.
- `baak-seoi-argument-correction` / `白水`: compact four-move argumentative correction with required slot mapping and short length.

The curated profiles are the safest default choices. If the user names or the router selects another EVCHK 潮文, inspect that raw file and derive a beat map before writing.

For any source that appears in `references/source_index.md`, do not draft from the profile alone when the raw corpus file exists. Read the raw article first, then use the profile to interpret the source's structure.

For uncategorized manifest entries, do not create a permanent profile unless the source becomes a recurring template. Use a temporary beat map for the current request to save context.

## Output Check

Before finalizing, verify:

- It expresses the user's actual opinion.
- If a named profile/reference was used, it preserves any required argument structure and length constraint from that profile/reference.
- It is approximately close to the selected original/profile length unless the user requested a different length.
- If a named profile/reference was used with a separate `topic:`, the output is mainly about the requested topic, not mainly about the profile/reference's original subject matter.
- It reads like HK forum copypasta rather than generic Cantonese prose.
- The source style is transformed enough that it is not a copied version with nouns swapped.
- It follows the user's requested stance and intensity without adding unrelated claims.

## Quality Notes

- Do not treat source fidelity as sufficient. A rewrite can copy the argument structure well and still fail as 潮文 if it lacks human comic timing.
- For argumentative sources, avoid merely restating the original reasoning with new nouns. Find the human joke: contradiction, over-seriousness, social awkwardness, bad faith, repeated verbal tic, or sudden tonal mismatch.
- Avoid lazy self-referential over-explanation. A test rewrite about "白水評論白水" that repeatedly said 白水/父權/構成 was judged worse, because the joke became too obvious and mechanical.
- Prefer one sharp absurd turn over several explanatory jokes.
