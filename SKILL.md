---
name: womenai-cohort-cards
description: >-
  Turn WoMen AI Lab founding-cohort survey responses (exported from the cohort
  "build in public" survey as CSV/JSON, or pasted in) into ready-to-post
  小红书 / Xiaohongshu / Instagram carousel cards that follow the WoMen AI Lab
  visual system, then render them to 2160×2880 PNGs. Use this whenever the user
  wants to make social-media cards, 小红书图, carousel slides, or "build in public"
  posts from a member's survey answers — including phrasings like "把某位成员的回答做成卡片",
  "generate cohort cards", "做几页适合发小红书的内容", or when they hand over a survey
  export and want it turned into shareable graphics. Also use to tweak copy, change
  the 栏目名/日期, add/remove pages, or re-render an existing card set.
---

# WoMen AI Lab 共创社群 · 小红书卡片

把 founding cohort 的问卷回答，做成一组符合社群视觉系统、可直接发布的小红书卡片，并渲染成 2 倍分辨率 PNG。

文案由你（Claude）来写——这是创意活；版式、配色、页眉页脚、页码、固定社群文案都已固化在脚本里，你不用碰。

## 流程

### 1. 拿到数据
数据来自社群「build in public」问卷导出表，字段固定为：
`Name · What Are You Building · Why It Matters · Progress Since Last Session · One Thing Learned · Support Needed · Content Permission · Social Handle · Anything Else · Submitted At`

用户可能：导出 CSV/JSON 丢给你、贴一段、或让你去读。读 CSV/JSON 直接解析即可——**不要用浏览器一格格抠**，那很慢。

> 隐私：问卷导出和回答属于个人信息，留在本地，**不要提交进这个公开仓库**。

### 2. 按授权过滤（先做，避免白做工）
看 `Content Permission`，决定能不能对外发、怎么署名。规则见
`references/visual-system.md` 的「发布授权」一节。`Community only` 的人直接跳过。
如果用户只点名某一个人（如「只做某位成员的」），就只处理那个人。

### 3. 写文案
通读这个人的全部回答，按 `references/visual-system.md`：
- **内容映射**：问卷字段是叙事骨架（building→产品页，why→缘起，progress→进展，learned→金句，support/anything else→尾页或副标题）。
- **语言风格（务必读，最容易出错）**：不用引号强调、不用破折号、不用「不是A而是B」对仗句、第一人称「我们/我」、高亮克制。
- 结构：首页 1 + 中间页 N + 尾页 1，默认 4–6 张。
- 挑最有画面感的真实细节当钩子（比如某句用户原话、某个具体场景），别写成通用宣传。

把文案写进一个 `cards.json`（schema 见下）。**只写内容**，页码/页眉/Who We Are 文案脚本会自动加。

### 4. 渲染
```bash
python3 "$SKILL_DIR/scripts/build_cards.py" <cards.json> --out <输出目录>
```
（`$SKILL_DIR` = 这个 skill 的目录）。需要 Python + Playwright（见 README 的安装说明）。
先 `--html-only` 预览结构、确认无误再渲染也可以。

### 5. 交付 + 确认
渲染出的 PNG 是 2160×2880。把图复制到用户方便拿的地方（项目文件夹/桌面），按文件名顺序就是发布顺序。
**做尾页前**，如果 Social Handle 不是真实小红书 ID，先跟用户确认真实 handle。

## cards.json schema

下面是一个**虚构示例**，演示三种卡片类型和绿色高亮的用法（请换成真实文案）：

```json
{
  "series": "founding cohort · build in public · 2026.06",
  "person": "example",
  "output_dir": "/绝对路径/example-cards",
  "cards": [
    {
      "type": "cover",
      "name": "cover",
      "tag": "— 一个 AI 项目 —",
      "title": "我给自己做了一个\n每天写三行的\n<g>记录小工具</g>",
      "sub": "一句话副标题，\n点明这组图要讲什么",
      "watermark": "AI"
    },
    {
      "type": "middle",
      "name": "why",
      "title": "为什么\n<g>从这里开始</g>",
      "body": "正文，约 42px 米色。讲缘起或动机，用具体的生活场景，不要堆术语。",
      "body2": "可选的第二段，暗调，用来补充信息。",
      "list": ["可选要点一", "可选要点二", "可选要点三"],
      "section_title": "小栏目标题（含英文词时英文标绿）",
      "section_body": "加粗白色，最关键一句<g>标绿</g>。"
    },
    {
      "type": "end",
      "name": "end",
      "whoami": "我是 <g>你的署名</g>。一句话身份 + 正在做的项目。"
    }
  ]
}
```

字段说明：
- 文案里 `<g>...</g>` = 薄荷绿高亮（这是唯一的强调方式，别用引号）；`\n` = 换行。
- `series` 默认栏目格式：`founding cohort · build in public · YYYY.MM`。
- `name` 决定输出文件名（如 `02_why.png`），可省略（默认用 type）。
- middle 卡的 `body / body2 / list / section_*` 都可选，按需组合。
- end 卡的 Who We Are 文案和页码由脚本自动注入，不要手写；`cta` 可覆盖默认行动引导。
- 右下角水印固定为「AI」，无需手写。
- 页码（01 / N）按卡片顺序与总数自动生成。

## 改版式
配色/间距/字号集中在 `assets/style.css`，改那里就行，不用动脚本。
完整规范见 `references/visual-system.md`。
