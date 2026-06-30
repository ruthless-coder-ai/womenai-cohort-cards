#!/usr/bin/env python3
"""
Build WoMen AI Lab 小红书 cards from a content JSON.

Usage:
    python build_cards.py <cards.json> [--out <dir>] [--html-only]

The JSON carries *content only*; layout/visual system lives in assets/style.css.
Page numbers, brand, series label, and the fixed "Who We Are" copy are injected
automatically so the writer only thinks about words.

Content string conventions (apply to every text field):
    <g>...</g>   -> mint-green highlight (this is how we emphasise, NOT quotes)
    \n           -> line break
"""
import argparse
import html as html_lib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
CSS_PATH = os.path.join(SKILL_DIR, "assets", "style.css")

# Fixed community copy — use verbatim, do not rewrite.
WHO_WE_ARE = (
    "WoMen AI Lab 是一个由女性组成的小型共创社群。我们一起学习、实验、失败、成长，"
    "探索在 AI 时代如何保持创造力、主体性，以及真实的人性。\n\n"
    "小而深，有意识，保持实验，保持人性。"
)
DEFAULT_CTA = "想加入或了解更多，欢迎私信我们 ✦"


def fmt(text):
    """Escape HTML, then re-enable our two markup conventions: <g> and \\n."""
    if text is None:
        return ""
    esc = html_lib.escape(str(text))
    esc = esc.replace("&lt;g&gt;", '<span class="g">').replace("&lt;/g&gt;", "</span>")
    esc = esc.replace("\n", "<br>")
    return esc


def header(series):
    return (
        '<div class="top-bar"></div>'
        '<div class="header">'
        '<div class="brand">WoMen <span class="ai">AI</span> Lab</div>'
        f'<div class="header-right">{fmt(series)}</div>'
        '</div>'
        '<div class="divider"></div>'
    )


def footer(page, total):
    return (
        '<div class="footer">'
        '<div class="footer-left"><span class="dot"></span> WoMen AI Lab</div>'
        f'<div class="footer-right">{page:02d} / {total:02d}</div>'
        '</div>'
    )


def watermark(ch=None):
    # Brand watermark is always "AI" — keep the corner mark consistent across every card.
    return '<div class="wm">AI</div>'


def render_cover(c, series, page, total):
    swipe = c.get("swipe", "→ 滑动查看")
    return (
        '<div class="card">'
        + header(series)
        + '<div class="body cover-body">'
        + f'<div class="tag">{fmt(c.get("tag", ""))}</div>'
        + f'<div class="cover-title">{fmt(c.get("title", ""))}</div>'
        + (f'<div class="cover-sub">{fmt(c["sub"])}</div>' if c.get("sub") else "")
        + (f'<div class="swipe">{fmt(swipe)}</div>' if swipe else "")
        + '</div>'
        + footer(page, total)
        + watermark(c.get("watermark"))
        + '</div>'
    )


def render_middle(c, series, page, total):
    parts = [
        '<div class="card">',
        header(series),
        '<div class="body">',
        f'<div class="tag mid-tag">— {page:02d} / {total:02d} —</div>',
        f'<div class="mid-title">{fmt(c.get("title", ""))}</div>',
    ]
    if c.get("body"):
        parts.append(f'<div class="mid-body">{fmt(c["body"])}</div>')
    if c.get("list"):
        items = "".join(f'<div class="li">{fmt(li)}</div>' for li in c["list"])
        parts.append(f'<div class="mlist">{items}</div>')
    if c.get("body2"):
        parts.append(f'<div class="mid-body-2">{fmt(c["body2"])}</div>')
    if c.get("section_title") or c.get("section_body"):
        parts.append('<div class="short-line"></div>')
        if c.get("section_title"):
            parts.append(f'<div class="sec-title">{fmt(c["section_title"])}</div>')
        if c.get("section_body"):
            parts.append(f'<div class="sec-body">{fmt(c["section_body"])}</div>')
    parts += ['</div>', footer(page, total), watermark(c.get("watermark")), '</div>']
    return "".join(parts)


def render_end(c, series, page, total):
    return (
        '<div class="card">'
        + header(series)
        + '<div class="body">'
        + '<div class="end-block-title">Who I am</div>'
        + f'<div class="end-block-body">{fmt(c.get("whoami", ""))}</div>'
        + '<div class="end-line"></div>'
        + '<div class="end-block-title">Who We Are</div>'
        + f'<div class="end-block-body">{fmt(WHO_WE_ARE)}</div>'
        + f'<div class="end-cta">{fmt(c.get("cta", DEFAULT_CTA))}</div>'
        + '</div>'
        + footer(page, total)
        + watermark(c.get("watermark"))
        + '</div>'
    )


RENDERERS = {"cover": render_cover, "middle": render_middle, "end": render_end}


def build_html(data):
    with open(CSS_PATH, encoding="utf-8") as f:
        css = f.read()
    series = data.get("series", "founding cohort · build in public")
    cards = data["cards"]
    total = len(cards)
    blocks = []
    for i, c in enumerate(cards, start=1):
        ctype = c.get("type", "middle")
        if ctype not in RENDERERS:
            raise SystemExit(f"Unknown card type '{ctype}' on card {i}")
        blocks.append(RENDERERS[ctype](c, series, i, total))
    body = "\n".join(blocks)
    return f"<!DOCTYPE html><html lang='zh'><head><meta charset='UTF-8'><style>{css}</style></head><body>{body}</body></html>"


def slugify(card, idx):
    base = card.get("name") or card.get("type") or "card"
    base = re.sub(r"[^0-9a-zA-Z_-]+", "-", str(base)).strip("-").lower() or "card"
    return f"{idx:02d}_{base}"


def render_pngs(html, cards, out_dir):
    from playwright.sync_api import sync_playwright

    html_path = os.path.join(out_dir, "_cards.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    saved = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=2,
                                viewport={"width": 1160, "height": 1520})
        page.goto("file://" + html_path)
        page.wait_for_timeout(600)
        els = page.query_selector_all(".card")
        for idx, (el, card) in enumerate(zip(els, cards), start=1):
            fname = slugify(card, idx) + ".png"
            el.screenshot(path=os.path.join(out_dir, fname))
            saved.append(fname)
        browser.close()
    return saved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", help="path to cards.json")
    ap.add_argument("--out", help="output dir (default: ./<person>-cards or ./out)")
    ap.add_argument("--html-only", action="store_true", help="write HTML, skip PNG render")
    args = ap.parse_args()

    with open(args.json, encoding="utf-8") as f:
        data = json.load(f)

    out_dir = args.out or data.get("output_dir")
    if not out_dir:
        person = data.get("person", "out")
        out_dir = os.path.join(os.getcwd(), f"{person}-cards")
    os.makedirs(out_dir, exist_ok=True)

    html = build_html(data)
    with open(os.path.join(out_dir, "_cards.html"), "w", encoding="utf-8") as f:
        f.write(html)

    if args.html_only:
        print(f"HTML written to {out_dir}/_cards.html ({len(data['cards'])} cards)")
        return

    saved = render_pngs(html, data["cards"], out_dir)
    print(f"Rendered {len(saved)} cards (2160x2880) to {out_dir}:")
    for s in saved:
        print("  " + s)


if __name__ == "__main__":
    main()
