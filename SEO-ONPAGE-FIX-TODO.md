# SEO 站内元数据修复清单（自模拟搜索引擎，零三方数据）

> 背景：SEO-D / Analytics-C 原卡"需连续周期 Bing/Clarity 真实流量数据"。老板指示不卡三方数据，用项目自有能力**模拟搜索引擎**跑一遍。
> 方法：`scripts/audit_seo.py`（纯静态读 HTML 源，零三方依赖）、`scripts/audit_seo_d.py`（读 `json/tools.json` 的 quality 做薄内容/重复识别）。两者本就无需三方数据。
> 原则：只修**安全项**（on-page 元数据文本、重复标题差异化、裸尖括号转义），**不动 URL、不删页、不加 noindex**；破坏性动作（noindex/合并/删除重复页）单列待老板拍板。

---

## 一、模拟搜索引擎发现的问题

| # | 问题 | 性质 | 数量 | 处理 |
|---|------|------|------|------|
| 1 | 页面 `<title>` 含裸 `<`（未转义，HTML 截断） | 真 bug（阻断 title 渲染） | 1（insurance/combined-ratio） | ✅ 已修（构建期被中文字典覆盖，部署无 `<`） |
| 2 | 工具页与指南页标题完全相同（tool×guide 同名） | 重复内容信号 | 30 组 | ✅ 指南页加「使用指南」/「 Guide」后缀 |
| 3 | 跨行业同名工具标题相同（tool×tool 同名） | 重复内容信号 | 6 组/12 页 | ✅ 加行业限定词到 `zh-CN.title` |
| 4 | 工具页 `meta description` 过短（<30 字） | 弱描述 | 1（stroop-test，28字） | ✅ 扩 `zh-CN.intro` 为 desc 首句 |
| 5 | 标题重复（title_missing/desc_missing 误报） | 审计 false positive | — | 排除：guides 用 `data-i18n` 写法、重定向桩 TOOLBOX-REDIRECT 被误算 |

### 根因补充（关键，防再犯）
- `combined-ratio` 裸 `<`：数据源头 `json/tools.json` 的 `name` 含裸 `<`，但 HTML `<title>` 由 `_build.py` 的 `_zh_title_of(industry,base) or t['name']` 生成，`_zh_title_of` 读 `i18n/tools/<ind>.json` 的 `zh-CN.title` 且**优先**——中文字典返回无 `<` 版本，部署无 `<`。
- **标题权威源是 `i18n/tools/<ind>.json` 的 `zh-CN.title`，不是 `t['name']`**：最初修 `name` 不粘，改 `zh-CN.title` 才生效。
- **描述权威源是 `i18n/tools/<ind>.json` 的 `zh-CN.desc/intro`**（经 `extract_zh_desc`，`intro` 优先于 `desc`），不是源文件 meta——改源 meta 会被 `_build.py` 重写回退。
- `audit_seo.py` 两个 bug 已修：① `ROOT` 算错一级；② 未跳过 `TOOLBOX-REDIRECT` 桩导致 false positive。

---

## 二、已执行的安全修复（落盘 + 已重建）

1. `scripts/fix_seo_title_dups.py` 干跑确认 43 项（1 转义 + 30 guide 后缀 + 12 tool 限定词），`--apply` 写入源文件标题（指南页后缀）与 `tools.json` name。
2. `scripts/fix_title_dup_zh.py` 给 12 个跨行业同名工具的 `i18n/tools/<ind>.json` 的 `zh-CN.title` 加行业限定词（幂等、不动 URL）。
3. `i18n/tools/cognition.json` 的 `stroop-test.zh-CN.intro` 扩为 60 字（desc 首句，事实一致）。
4. `scripts/audit_seo.py` 修 `ROOT` + 加重定向桩跳过（让体检可正确工作，非发布改动）。
5. `_build.py` 重建全站（同步繁体、tools.json、分类页、搜索索引）。

---

## 三、待老板拍板的破坏性项（未执行）

| 项 | 内容 | 风险 |
|----|------|------|
| SEO-D 薄内容 | `audit_seo_d.py` 无 C 级（全部 A）。名称相似度 ≥0.82 重复对 187 对（去重 152，高置信仅 4 对）——可合并/删，但删页改 URL 影响 SEO | 需拍板是否合并或 301 |
| Analytics-C 高曝光低点击 | 需重写 Title/Description，首批 21 页已做；扩面需数据 | 仍建议等周期数据，但纯 on-page 重写可继续 |

---

## 四、验证（已执行）
- `_build.py` 重建：A 级 5008 100%，繁体同步，SW 版本戳更新。
- `scripts/run_gates.py` 五道门禁全过（含死链 0）。
- `scripts/audit_seo.py` 重跑权威结果：
  - **title 重复组数: 0，涉及页面: 0** ✅（12 同名工具全部差异化）
  - **desc 重复组数: 0** ✅
  - **description 重复: 0** ✅
  - `title_missing/desc_missing` 仅 `guides/bmi-calculator-guide.html`：**false positive**——该页 title/desc 由 `data-i18n` 运行时注入（i18n 双轨架构），源文件无静态标签，Google 执行 JS 可抓取，非真缺失。
  - `og_*/tw_*/jsonld/canonical_missing` 全在 `sitemap.html`/`404.html` 系统页，本就不该有 OG/canonical，合理。
- stroop intro 已扩（源文件 meta 60 字）、12 同名工具 `zh-CN.title` 已带行业限定词、30 指南页已加「使用指南」后缀——均经重建粘住。
- 线上验收：待推送后轮询（旧 URL 404 / 新 URL 200 / 标题差异化生效）。

## 五、经验（防再犯）
- **标题权威源 = `i18n/tools/<ind>.json` 的 `zh-CN.title`**，不是 `json/tools.json` 的 `name`——改 `name` 不粘，被 `_zh_title_of` 覆盖。
- **描述权威源 = `i18n/tools/<ind>.json` 的 `zh-CN.desc/intro`**（`extract_zh_desc` 中 `intro` 优先于 `desc`），改源文件 meta 会被 `_build.py` 重写回退。
- `audit_seo.py` 已修 `ROOT` 算错一级 + 跳过 `TOOLBOX-REDIRECT` 桩，否则大量 false positive。
- 验证修复是否粘住**不能只看源文件**，必须重建后重跑 `audit_seo.py` 用权威数字确认（期望值手写易错，以审计为准）。
- guides 页用 `data-i18n` 写法，静态审计会报 title/desc missing，属架构性 false positive，不计入真问题。
