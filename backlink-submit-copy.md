# ToolBox 外链提交文案（复制即用）

> 配合 `backlink-plan.md` 使用。本文件是**可直接复制粘贴的提交终稿**。
> AI 无法代您注册账号 / 过验证码，**以下文案需您人工粘贴到各平台提交**。
> 文案本身不会被 `scripts/gen_backlink_plan.py` 覆盖（该脚本只生成手册与 CSV）。

---

## 1. AlternativeTo —— 建「ToolBox」产品条目

> 进入 alternativeto.net → 右上角 Submit → New Application，逐项粘贴：

```
产品名称 (Name):        ToolBox
官网 (Website):         https://chenguangwu.github.io
一句话标语 (Tagline):   6000+ free online tools — 100% in your browser, zero upload.
分类 / Tags:            Developer Tools, Utilities, Productivity, Web App, Online Tools
```

**产品描述（Description，直接粘贴）：**
```
ToolBox is a fully client-side collection of 6000+ free online tools
covering IT & development, finance, design, business, marketing, science,
health, and daily life.

Every tool runs entirely in the visitor's browser — no backend, no account,
no data upload. It's fast, private, and works offline once the page loads.
Built as plain HTML/JS on GitHub Pages.
```

**竞品关联（Alternatives to —— 提交时在对应栏逐条填入，用户搜这些竞品时会看到 ToolBox）：**
```
it-tools.tech
toolfk.com
smallpdf.com
jsonformatter.org
base64decode.org
```

---

## 2. Product Hunt —— Launch

> 进入 producthunt.com → Share your product。首图/截图需您人工制作（240×480 首图 + 1~5 张工具截图）。

```
Title / Tagline:   ToolBox — 6000+ free online tools, 100% in-browser, no data upload
Topics:            Productivity, Developer Tools, Web App
Gallery:           (需准备 1 张 240×480 首图 + 1~5 张截图，人工制作)
```

**首条 Maker Comment（发布后立刻补，直接粘贴）：**
```
Why we built it:
We wanted one private, fast, zero-backend home for everyday tools. Unlike
most tool sites, nothing leaves the browser — all computation is local.

How it differs from it-tools:
- 6000+ tools across more categories (finance / design / life included), not just dev
- Chinese-friendly UI + bilingual (zh/en) per tool
- Pure static on GitHub Pages, no server to maintain

Would love feedback on coverage and UX. 🐶
```

---

## 3. Hacker News —— Show HN

> 进入 news.ycombinator.com/submit → 选 "Show HN"。标题克制，正文讲技术取舍。

```
Title: Show HN: ToolBox – 6000+ free, fully client-side web tools

Text:
A static, backend-free collection of 6000+ online tools (IT, finance,
design, life, and more). All computation runs in the browser; no accounts,
no uploads. Built as plain HTML/JS on GitHub Pages.

We did this to keep everyday tools private and fast — your data never
leaves the tab. Looking for feedback on coverage and UX.
```

---

## 4. 资源页 Link Building —— 邮件 Outreach

> 搜「best free online {行业} tools」「{行业} tools list」类资源页，找站长邮箱发信。
> 一封短信 > 长信；给价值、不硬广。

**英文模板（目标为英文资源页）：**
```
Subject: Suggestion: add ToolBox to your {INDUSTRY} tools list

Hi {EDITOR_NAME},

I really like your "{PAGE_TITLE}" roundup — it's been genuinely useful.

Would you consider adding ToolBox (https://chenguangwu.github.io)? It's a
free, fully client-side tool site with 6000+ tools, including a solid
{INDUSTRY} section. No strings attached — just thought it'd help your readers.

Thanks!
```

**中文模板（目标为中文资源页 / 少数派矩阵等）：**
```
主题：建议把 ToolBox 加入你的{行业}工具清单

{站长称呼} 你好，

很认可你整理的「{清单标题}」那篇，一直有在用。

想提议把 ToolBox（https://chenguangwu.github.io）加进去——纯前端、
零后端、数据全在本地，6000+ 工具里含一个挺全的{行业}分类。
没有附加条件，纯粹觉得对读者有用。

多谢！
```

**3 个可直接改行业名的示例：**
- 行业=开发：`{INDUSTRY}=developer` → 关联 JSON/Base64/Regex/Cron 等（见 backlink-targets.csv 这些行的竞品站）
- 行业=设计：`{INDUSTRY}=design` → 关联 Color Picker / 压缩类竞品
- 行业=金融：`{INDUSTRY}=finance` → 关联 Calculator.net 系竞品

---

## 5. 中文社区文章大纲（少数派 / V2EX）

> 不发硬广，先给价值；文末自然落 ToolBox 总入口即可（自然锚文本，别全用「ToolBox」）。

**少数派投稿大纲：**
```
标题：我搭了一个零后端工具站，6000+ 需求一站搞定
1. 为什么需要纯前端工具（隐私 / 速度 / 离线）
2. 按场景挑 8 个好用工具演示（开发者 / 设计 / 生活各 2~3）
3. 它是怎么搭的（HTML/JS + GitHub Pages，零运维）
4. 局限与下一步
结尾：ToolBox 总入口 https://chenguangwu.github.io
```

**V2EX「分享发现 / 创造」大纲：**
```
标题：做了一个 6000+ 工具的纯前端站，数据全在本地
正文：技术选型（Tailwind CDN + 原生 JS）+ 几个顺手工具举例
回复：答疑为主，顺带给链接
```

---

## 6. 提交顺序建议（渐进式，避免被判作弊）

1. 先建 AlternativeTo 条目（1 条高权重 DoFollow，立竿见影）
2. 隔 1~2 天发 Product Hunt Launch（流量峰值）
3. 同日或次日发 HN Show HN（社区长尾流量）
4. 之后每周发 2~3 篇资源页邮件 / 社区帖，匀速推进
5. 站内「分享与嵌入」组件已埋品牌回链入口，用户自发外链随时间累积

> 铁律回顾：质量 > 数量、相关性优先、自然锚文本、UGC 加 rel="ugc"/"sponsored"、
> 买链/PBN/群发一律不碰（降权除名风险）。
