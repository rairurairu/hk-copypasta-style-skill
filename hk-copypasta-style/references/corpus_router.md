# Corpus Router

Use this file to choose from the full EVCHK raw corpus without loading the whole manifest into context. This router is the default path whenever the user gives a topic but does not name a genre/source 潮文.

## Principle

The 12 curated profiles in `style_profiles.md` are safe defaults, not the full supported set. When `../research/raw-corpus/manifest.json` exists, treat every manifest item and every routing archetype as available source material.

If no genre/source is specified, do not default to 火腩飯 or any other curated profile just because it is familiar. Search broadly, classify the user's topic by comedic engine, and choose the source family that creates the freshest transformation.

## Candidate Discovery

First find the corpus manifest. The raw corpus is intentionally outside the installed skill. Check workspace-relative paths such as `../research/raw-corpus/manifest.json`, `./research/raw-corpus/manifest.json`, and project-skill paths such as `../../../research/raw-corpus/manifest.json`.

1. If the user names a source, search exact and fuzzy title matches in `manifest.json`.
2. If the user gives only a topic, search the manifest title list for related nouns, brands, settings, media, products, and forum phrases.
3. If no source/genre is named, consider all routing archetypes below before choosing. Do not restrict selection to the 12 curated profiles.
4. If title search is weak, pick 3-5 likely archetypes below, then search raw files for repeated phrases or topic-adjacent words.
5. Inspect only the top 1-3 candidate raw files before drafting.
6. If no candidate clearly fits, fall back to the closest curated profile.

Use `scripts/search_corpus.py` when available:

```powershell
python .\scripts\search_corpus.py --manifest ..\research\raw-corpus\manifest.json --query "三哥 米線"
```

The helper prints score, ID, title, sensitivity, manifest path, and resolved raw-file path. Open the resolved raw-file path when present.

## Topic Collision Rule

If the user's topic already appears in the corpus as a derivative, variant, or adaptation example, do not reuse that enclosing source as the primary structure.

Examples of collision sections include headings like `===[[18件麥樂雞]]版===`, `===X版===`, `==衍生潮文==`, `==改編==`, `==變奏==`, or any raw section where the requested topic is already the transformed payload rather than the original source.

When this happens:

1. Mark the enclosing source as `collision-primary-blocked`.
2. Use the existing derivative only as a negative reference: avoid its wording, slot choices, and source skeleton.
3. Choose another source family or archetype that fits the topic's joke but gives a fresh structure.
4. Prefer a different comedic engine, such as consumer absurdity, mock luxury review, testimonial ad, public-scene punchline, official apology, or forum definition.
5. If the user explicitly asks for the existing derivative, exact version, or beat-by-beat analysis, then use it as requested.

For example, if the topic is `十八件麥樂雞` and the 火腩飯 raw file already contains an `18件麥樂雞` variant, do not generate another 火腩飯-structure rewrite by default. Choose a different primary reference instead.

## Routing Archetypes

- **Object / food worship**: sincere melodrama about a mundane object, food, tool, brand, hobby, or routine. Good for restaurants, daily items, apps, fandoms, lifestyle choices.
- **Consumer absurdity**: broken menu, checkout, customer service, pricing, queue, delivery, platform UX, or bureaucracy. Good for shops, apps, banks, schools, transport, subscriptions.
- **Mock luxury review**: treat cheap or ordinary goods as rare, vintage, refined, or philosophical. Good for drinks, snacks, instant food, budget purchases, low-end gadgets.
- **Forum definition / tribe identity**: define a forum, app, workplace, fandom, school, city, or scene with cynical rules and in-group logic.
- **Complaint / rumor escalation**: fake-serious chain of injustice, accusation, warning, HR/customer-service consequence, or social drama. Use caution with real people.
- **Public scene punchline**: short scene in train, bus, shop, classroom, office, lift, or street ending in exposure, silence, or awkward reversal.
- **Romance / hardship value essay**: relationship, loyalty, class anxiety, humble choice, shared suffering, or "real value" argument.
- **Product-tribe wisdom**: smug comparison between rival platforms, brands, operating systems, tools, schools, districts, teams, or lifestyles.
- **Ad testimonial**: suspicious first-person endorsement, "I tried it first", no fake effects, celebrity/influencer review, marketing promise.
- **Official apology / public-service slogan**: institution explains inconvenience with caring language while users suffer.
- **Moral alarm / concern sentence**: exaggerated formal disappointment, chilling concern, public morality, education, society, or standards.
- **Story opener / setup**: `是咁的` confession, incident report, fake-serious explanation, or forum anecdote opener. Usually pair it with another archetype.

## Dynamic Beat Extraction

For uncategorized corpus entries:

1. Locate `==原文==`, `==潮文內容==`, `==內容==`, or the first long quoted section.
2. Ignore encyclopedic page intro, references, navigation, and category text.
3. Extract sentence/line count, rough character length, repeated phrases, dialogue turns, escalation points, concrete objects, and ending rhythm.
4. Build a temporary beat map in notes before drafting.
5. Transform the structure into the user's topic; do not copy source wording except for very short anchor phrases.
6. Keep the output close to the selected source's length. If the source is a short 4-line argument, output a short 4-line argument; if the source is a long monologue, output a comparable monologue. Do not expand short sources into essays unless the user asks.

## Selection Bias

Prefer a source whose human joke matches the user's payload:

- absurd seriousness for ordinary things
- bureaucratic contradiction for services and systems
- identity superiority for tribes and product choices
- awkward social reversal for public scenes
- fake-formal concern for public affairs
- testimonial rhythm for brands and products

When choosing automatically, source-fit matters more than source fame.
