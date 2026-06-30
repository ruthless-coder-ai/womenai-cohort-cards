# womenai-cohort-cards

A [Claude](https://claude.com/claude-code) **skill** that turns WoMen AI Lab
founding-cohort "build in public" survey answers into ready-to-post
小红书 / Xiaohongshu carousel cards, following the community's visual system,
and renders them to 2160×2880 PNGs.

Claude writes the card copy (the creative part); the layout, colours, header/footer,
page numbers, watermark, and the fixed community blurb are locked into the renderer,
so every set stays on-brand.

## What's inside

```
womenai-cohort-cards/
├── SKILL.md                    # workflow + cards.json schema (Claude reads this)
├── assets/style.css            # the visual system — colours, type sizes, spacing
├── scripts/build_cards.py      # cards.json → HTML → 2× PNG (Playwright)
└── references/visual-system.md # full spec + language rules + field mapping
```

## Install (as a Claude Code skill)

Clone it into your skills directory:

```bash
# personal (available everywhere)
git clone https://github.com/ruthless-coder-ai/womenai-cohort-cards \
  ~/.claude/skills/womenai-cohort-cards

# or project-scoped (travels with one repo)
git clone https://github.com/ruthless-coder-ai/womenai-cohort-cards \
  <your-project>/.claude/skills/womenai-cohort-cards
```

Then in Claude Code just ask, e.g. *"做这期的小红书卡片"* / *"make this session's cohort cards"*,
and hand over the survey export.

## Use the renderer directly

```bash
# one-time setup
pip install playwright
python -m playwright install chromium

# render a card set
python3 scripts/build_cards.py path/to/cards.json --out ./out
# preview structure only, skip rendering:
python3 scripts/build_cards.py path/to/cards.json --html-only
```

See `SKILL.md` for the `cards.json` schema and a worked example.

## Customising the look

All colours, font sizes and margins live in `assets/style.css` — edit there.
The full visual + language spec is in `references/visual-system.md`.

## 🔒 Privacy

This repo is **templates and tooling only**. Survey exports, members' answers,
real names, and social handles are **personal information** — keep them local and
never commit them. `.gitignore` already blocks the common file patterns
(`*.csv`, `cards-source/`, rendered card folders), but double-check before pushing.

## License

MIT — see [LICENSE](LICENSE).
