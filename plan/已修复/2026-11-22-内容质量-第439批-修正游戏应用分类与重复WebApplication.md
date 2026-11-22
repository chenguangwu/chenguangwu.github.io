# 第 439 批：修正游戏类 applicationCategory 与重复 WebApplication

日期：2026-11-22
类型：SEO / 结构化数据
状态：已修复并本地提交（未 push）

## 一、原问题

### 1. 游戏类 `applicationCategory` 拼写错误

全站 72 个页面写成 `GamesApplication`（复数，不是 schema.org 类型），4 个页面写成 `Game`，只有 2 页是正确的 `GameApplication`。错误值会让搜索引擎无法把工具识别为游戏应用。

### 2. 17 个页面存在两个 `WebApplication` JSON-LD

构建的 `_replace_webapp_ld()` 只按紧凑串 `"@type":"WebApplication"` 匹配；历史页面存在缩进美化版 `"@type": "WebApplication"`，没被识别，于是构建在 `</head>` 又插入一个新块，同页出现两个 WebApplication。例如：

- `tools/fun/pong.html`：第 29 行旧的 `Game` 块 + 第 213 行新的 `GameApplication` 块；
- `tools/edu/flashcards.html`、`tools/it/keyword-extractor.html`、`tools/it/summary-generator.html` 等。

## 二、修复内容

1. `_build.py` 的 `app_cat_map`：`game` 映射从 `GamesApplication` 改为 `GameApplication`；
2. `_replace_webapp_ld()` 不再用字符串包含判断，而是逐个 `<script type="application/ld+json">` 解析 JSON，判断 `@type == "WebApplication"` 后统一删除旧块（含缩进/单行/多重历史块），再在首个位置写回唯一规范块；
3. 解析失败的块保持原样，不误删 Breadcrumb / FAQPage。

## 三、验证证据

- 构建：`env -u NODE_OPTIONS python3 _build.py` 成功。
- 全站 WebApplication 统计：
  - `GameApplication`：**72**；
  - `GamesApplication` / `Game`：**0**；
  - 同一页多个 WebApplication：**从 17 页降至 0 页**；
  - WebApplication 总数仍为 **4,606**，无页面丢失。
- 静态门禁：**4,626 passed / 0 failed / 0 warnings**。
- 第 438 批后全量门禁：`/tmp/gates438.log` 结果待本次提交后复跑确认。

## 四、改动范围

- `_build.py`：游戏分类映射；WebApplication 块解析式替换。
- 72 个游戏页 + 17 个重复页的 JSON-LD 重算。
- 共 84 个文件，135 insertions / 347 deletions。
