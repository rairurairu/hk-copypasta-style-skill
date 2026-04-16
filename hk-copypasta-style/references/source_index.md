# Source Index

Use this file for curated source families. It is not the complete corpus. For automatic source selection across all fetched EVCHK 潮文, use `references/corpus_router.md` plus `research/raw-corpus/manifest.json`.

Primary index: https://evchk.fandom.com/zh/wiki/%E6%BD%AE%E6%96%87

The broader raw corpus can be generated outside this skill at `research/raw-corpus/manifest.json`. Use it for exact-source lookup when a user names a source not listed in the curated table below, and for automatic source selection when the user gives only a topic.

When a user names a source in this table, automatically read `research/raw-corpus/<ID>.wiki.txt` before drafting, then use `style_profiles.md` as the distilled guide.

When the user asks to choose from "all references" or "all 潮文", do not add every source here. Search the manifest, inspect the top candidate raw files, and derive a temporary beat map.

| ID | Source family | Category | URL | Sensitivity | Use for |
| --- | --- | --- | --- | --- | --- |
| `huo-nam-romantic-object` | 火腩飯潮文 | food / object romance | https://evchk.fandom.com/zh/wiki/%E7%81%AB%E8%85%A9%E9%A3%AF%E6%BD%AE%E6%96%87 | safe | Over-serious praise of a mundane object, product, food, identity, or hobby |
| `ga-je-rumor-escalation` | 家姐被炒潮文 | rumor / fake complaint | https://evchk.fandom.com/zh/wiki/%E5%AE%B6%E5%A7%90%E8%A2%AB%E7%82%92%E6%BD%AE%E6%96%87 | caution: real-person allegation style | Workplace, customer-service, celebrity/brand complaint escalation |
| `forum-definition` | 有人問我 : 高登係一個點既論壇? | forum culture | https://evchk.fandom.com/zh/wiki/%E6%9C%89%E4%BA%BA%E5%95%8F%E6%88%91_%3A_%E9%AB%98%E7%99%BB%E4%BF%82%E4%B8%80%E5%80%8B%E9%BB%9E%E6%97%A2%E8%AB%96%E5%A3%87%3F | safe | Defining a group, app, workplace, fandom, or online culture with cynical humor |
| `public-scene-punchline` | 女友一句，全車靜晒 | relationship / public scene | https://evchk.fandom.com/zh/wiki/%E5%A5%B3%E5%8F%8B%E4%B8%80%E5%8F%A5%EF%BC%8C%E5%85%A8%E8%BB%8A%E9%9D%9C%E6%99%92 | caution: crude punchline source | Short scene with dialogue and a sudden embarrassing reveal |
| `mc-hardship-romance` | 男人一生，只為尋覓一個肯同自己挨麥記嘅女人 | romance / value essay | https://evchk.fandom.com/zh/wiki/%E7%94%B7%E4%BA%BA%E4%B8%80%E7%94%9F%EF%BC%8C%E5%8F%AA%E7%82%BA%E5%B0%8B%E8%A6%93%E4%B8%80%E5%80%8B%E8%82%AF%E5%90%8C%E8%87%AA%E5%B7%B1%E6%8C%A8%E9%BA%A5%E8%A8%98%E5%98%85%E5%A5%B3%E4%BA%BA | safe | Sincere comic essay about values, relationships, class, and everyday hardship |
| `food-1999-counter` | 大家樂白汁雞皇飯潮文 | food / absurd transaction | https://evchk.fandom.com/zh/wiki/%E5%A4%A7%E5%AE%B6%E6%A8%82%E7%99%BD%E6%B1%81%E9%9B%9E%E7%9A%87%E9%A3%AF%E6%BD%AE%E6%96%87 | safe | Short chaotic restaurant/shop counter confusion |
| `premium-cheap-object` | 82年百事潮文 | consumer goods / mock luxury | https://evchk.fandom.com/zh/wiki/82%E5%B9%B4%E7%99%BE%E4%BA%8B%E6%BD%AE%E6%96%87 | safe | Treating cheap or ordinary goods as rare, premium, or philosophical |
| `tech-tribal-wisdom` | Android潮文 | tech / product tribe | https://evchk.fandom.com/zh/wiki/Android%E6%BD%AE%E6%96%87 | caution: gendered source wording | Smug comparison between rival products, platforms, or lifestyles |
| `mtr-apology-slogan` | 港鐵唔好意思廣告討論熱潮 | transport / public-service parody | https://evchk.fandom.com/zh/wiki/%E6%B8%AF%E9%90%B5%E5%94%94%E5%A5%BD%E6%84%8F%E6%80%9D%E5%BB%A3%E5%91%8A%E8%A8%8E%E8%AB%96%E7%86%B1%E6%BD%AE | mild public affairs | Corporate apology, infrastructure, service disruption, bureaucratic inconvenience |
| `jackie-ad-testimonial` | 成龍洗頭水潮文 | ad parody | https://evchk.fandom.com/zh/wiki/%E6%88%90%E9%BE%8D%E6%B4%97%E9%A0%AD%E6%B0%B4%E6%BD%AE%E6%96%87 | safe | First-person testimonial, product claims, "I tried it first" ad rhythm |
| `see-gum-dik-setup` | 是咁的 | golden sentence / setup | https://evchk.fandom.com/zh/wiki/%E6%98%AF%E5%92%81%E7%9A%84 | safe | Opening a story, confession, rant, or fake-serious post |
| `cold-breath-concern` | 我不禁倒抽一口涼氣 | golden sentence / moral alarm | https://evchk.fandom.com/zh/wiki/%E6%88%91%E4%B8%8D%E7%A6%81%E5%80%92%E6%8A%BD%E4%B8%80%E5%8F%A3%E6%B6%BC%E6%B0%A3 | mild public affairs | Mock-formal concern, moral panic, exaggerated disappointment |

## Adding More Sources

When adding an EVCHK source:

1. Add the URL and a short sensitivity tag here.
2. Put raw fetched text, if needed, under `research/raw-corpus/`, not inside this skill.
3. Add a distilled profile in `style_profiles.md` when the source becomes a recurring template.

## Corpus Refresh

Use the fetcher to rebuild the broader local corpus from the EVCHK 潮文 index:

```powershell
python .\hk-copypasta-style\scripts\fetch_evchk_corpus.py --from-index --include-seeds --timeout 30 --sleep 0.1 --resume
```
