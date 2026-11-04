# Eight tiny pages for goal-aware change monitoring

Firecrawl's [/monitor](https://www.firecrawl.dev/blog/monitor-website-changes-firecrawl) combines page diffs with an optional natural-language goal so that notifications can focus on meaningful changes. This repository is a **synthetic fixture set**, not a test of Firecrawl. It asks: for the goal “alert only when the current checkout price changes,” which page edits should trigger a notification?

The eight pairs include a footer clock, review count, CSS rename, changed current price, changed crossed-out old price, changed structured checkout price with unchanged visible text, and a promo banner. Each pair has a ground-truth label in `fixtures.json`. The small evaluator compares three local baselines: raw HTML diff, visible-text diff, and a field-specific price extractor.

```sh
python3 evaluate.py > report.json
```

On this fixture set, raw HTML diff yields five false alerts; visible-text diff yields four false alerts and misses the attribute-only checkout price change; field-specific extraction matches the eight labels. These are results for the supplied toy pages only. They do not measure Firecrawl's AI judge, extraction quality, credit use, or behavior on real sites.

The useful research question is how a monitor can choose between cheap page-level diffs and a more costly field- or goal-aware check, while bounding both missed changes and alert noise. A more serious follow-up would test many real pages, rendering modes, ambiguous goals, and the actual API with consent and a fixed budget.
