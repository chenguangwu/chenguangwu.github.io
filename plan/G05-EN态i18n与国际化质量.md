# G05 · EN 态 i18n 与国际化质量（全站）

## 现状
- 门禁 EN CJK BAD=0 多轮通过（表层合格）；图表注入批全部走 isEn() 双语分支，词典零残留。

## 深水区问题（未系统排查）
### P1. 第三层词典覆盖缺口
- 描述：`i18n/tools/en/<ind>/<slug>.json` 按需新增，历史页面 dd/FAQ 长文本可能未全覆盖 → EN 态回退中文（运行时 textContent 查表 miss）。
- 方案：写只读探针（puppeteer EN 态全站抽样 getClientRects 可见 CJK），产出缺口清单后补词典。
- 受影响：全站（重点：dd/FAQ 长文页面）

### P2. 术语一致性
- 描述：同领域术语在不同页 EN 译法不一（如 eGFR/肌酐清除率、PSA 密度），影响专业感。
- 方案：按大分类建术语表（en 词典共享层 `_common.json` 扩充），统一译名。
- 受影响：i18n/tools/en/**

### P3. 繁体（zh-tw）口径
- 描述：构建自动转换，但「专有名词/药名」简繁一多对应偶有生硬（如「信息素/信息素」类）。
- 方案：OpenCC 覆盖词典按分类补条目（源 `zh-tw` 转换配置）。
- 受影响：繁体全站

### P4. 数字/单位本地化
- 描述：EN 态单位写法（如 m²、mg/dL、kcal）与千分位应随 locale；当前多为硬编码中文页口径。
- 方案：低优先级；在 G06 重设计时统一。

## 进度
- 🔴 P1-P3 待排查/开发（P1 建议先行，产出量化缺口）

## 2026-11-03 审计补充（只读审计）

### 待补门禁：预设按钮英文标签
- 建议加入针对 `labelEn` 值包含汉字的静态门禁，防止英文态出现中英混排（见 G08）。

### 疑似待验证 G05-B：第三层词典对新预设页面的覆盖未量化
- 问题：P1（第三层词典覆盖缺口）仍无量化清单；本轮只能确认页面模板级 i18n 引用齐全（`common.js` 缺 `i18n.js` = 0），无法证明 3845 个 preset 页的说明文案在 EN 态全部命中。
- 证据：`js/tool-i18n.js:613` 动态加载 `/js/tool-i18n-en.js`（681KB）；`i18n/tools/en/**` 按工具一文件；本轮未运行 EN 态真机探针（项目规则要求 `scripts/_en_i18n_probe.mjs --check`，属可执行门禁，本轮只读未跑）。
- 影响：全站英文态。
- 方案：第二轮用 `scripts/_en_i18n_probe.mjs --check` 抽样 50 个新增 preset 页，产出 miss 清单后补第三层；禁止只改 HTML 内联（构建会还原场景外的数据源文案）。

### 已修 G05-D：heat-stress-index head 结构丢失实为陈旧 zh-tw 产物（2026-11-04）
- 现象：集成线报「`<head>` 被整块替换，丢 WebApplication/FAQPage LD、privacy/统计/i18n 脚本、hreflang、`TOOLBOX-SECURITY`」，且 `zh-tw` 对应页同样缺失。
- 核对：源页 `tools/livestock/heat-stress-index.html` 与 HEAD 逐字节一致（`git status` 干净），3 个 LD 块（WebApplication / BreadcrumbList / FAQPage）全部 `json.loads` 通过；`js/i18n.js` / `js/privacy.js` / `js/metrics.js` / `js/analytics.js` / `hreflang`×4 / `TOOLBOX-SECURITY` 计数均与 HEAD 同值。真正缺损的是 `zh-tw/` 构建产物（565 行、仅 1 个 LD、无脚本引用）——它在 22:46 源页处于损坏状态时被构建，源页 22:50 复原后未重建。
- 处理：`node scripts/gen_opencc_locales.mjs` 重建 8333 个繁体页；该页恢复 3 个 LD + 全部脚本/hreflang/安全 meta（598 行），三块 LD 均可解析。
- 英文态：`_en_i18n_probe.mjs --check livestock/heat-stress-index` 仅 4 条既有残留（1 条公式说明、3 条 placeholder），非整页回退中文；残留属第三层词典缺口，与本次 head 无关。
- 教训：① 批量文案/结构脚本**禁止整段替换 head**，必须逐块解析、写盘前后比对结构计数（即 `opt_faq_ld_sync.py` 的六项守卫）；② 源页修复后必须重建 `zh-tw`，否则构建产物仍带旧缺陷，集成线会直接判红。

## 2026-11-05 只读扫描：英文元数据成批退化为占位串

### 结论
- **是成批污染，且是结构性的**，范围远超此前发现的 2 页；污染源不在 HTML，而在 `scripts/gen_en_override.py` 的英文名/描述生成链。
- 全站 4705 个工具页（不含行业 index）分级结果：
  - **P1（标题退化，丢失工具实义）674 页（14.3%）**；
  - **P2（描述只剩「通用前缀 + 套话」）36 页（0.8%）**；
  - **P3（中英长度严重不匹配 / 语义错译，如质量分数→`Quality Fraction`）47 页（1.0%）**；
  - 另计**广义模板描述**：`desc-en` 命中 `「英文名 - online utility on ToolBox.」` 一类模板句者 **4386/4705（93.2%）**（含工具名，故不计入 P2 严格口径）。
- 分层：`_en_override.en` 命中退化判据 **609 条**；页面 `title-en` 已退化 **674 页**；两者同时退化 **605 页**；页面已手修但源字典仍退化（重建即回退）**4 页**；源正常但页面陈旧 **68 页**。

### 根因（逐条对应代码）
1. `scripts/gen_en_override.py::translate_name()` 只译出中文名首个通用词，括号里的具体限定被丢弃（财务(分析/决策/预测)模型→`Finance`、质量(标准/检查/提升)体系→`Quality`、检测→`Detect`）→ P1 单通用词 111 页 + P2。
2. 回退 `slug_to_name()` 把无意义编号 slug 直接 title-case（`generator-35`→`Generator 35`、`detector-173`→`Detector 173`、`analysis-28`→`Analysis 28`）→ P1 编号占位 **502 页**；`PLACEHOLDER_KEY` 只覆盖 `calc-N` 与少量拼音 slug，未覆盖 `generator-N / detector-N / analysis-N / rater-N` 等编号族。
3. `slug_to_intro()` 按 slug 关键词固定拼 14 条套话（`- produce results instantly in your browser.` / `- online utility on ToolBox.` / `- compute values online with accurate results.` 等）→ 广义模板 4386 页。
4. 机翻重复词/模板碎片：`AST AST View Device`、`Reference Reference Format Convert`、`Quality - ( Check / Evaluate / Improvement ) Mechanism`。

### 回归风险（关键）
- 2026-11-05 的 `2c81d57a36`（“补全占位英文标题并修正退化元描述”）只在 **HTML 侧手工修了 5 页**；其中 **4 页的源字典仍是退化值**：`data/generator-35`、`finance/generator-report-1`、`fitness/generator`、`realestate/generator-assessor`。
- `_build.py` 第 4.0 段以 `EN_OVERRIDE[slug]` 的 `en`/`ed` **无条件覆写** `<meta name="title-en">` / `<meta name="desc-en">`（见 [_build.py](file:///Users/cgw/project/cgw/chenguangwu.github.io/_build.py#L3840-L3935)）⇒ **下一次构建会把手工修复整批回退**。只改 HTML 不修源字典 = 白做。

### 真机复核（Chrome headless，`?lang=en-US`，20 页抽样）
- **18/20 页 `document.title` 确为退化串**（P1 抽样 18 页全部命中）；2 页为已手工修复的对照页（`fitness/generator`、`hematology/generator-analysis`），当前正确但源字典仍退化。
- 其中 **5/20 页可见 h1 也退化**；其余页 h1 由运行时第三层词典补成正确英文名。
- **结论：退化主要伤 SEO/社交元数据（title / meta description），不一定伤首屏可见 h1**——搜索引擎抓 `title-en`/`desc-en`，“页面看得见正常”不代表“收录正常”。
- 误报 0：抽样前已将「编号 slug」「单通用词」「词序错乱」与同行业正常页（`it/json-diff`、`accounting/asset-turnover`、`it/ipv4-range-expander`、`it/ksuid-generator`）做基线对照，短标题未被误抓。

### 行业排行（P1 前 10）
`general` 35 / `sports` 29 / `machinery` 28 / `realestate` 25 / `automotive` 13 / `electrical` 13 / `metalwork` 13 / `agriculture` 12 / `eco` 12 / `life` 12 / `materials` 12 / `hydraulic` 11（共 131 个行业目录有 P1，其余多为个位数）。

### 处理建议（未执行，待批准）
1. **先修源**：`translate_name()` 保留中文括号限定；`slug_to_name()` 对 `通用词+编号` 返回 `None` 并扩 `PLACEHOLDER_KEY`（或直接从中文标题直译）；`slug_to_intro()` 去模板套话。
2. **再重生成 + 重建**：`python3 scripts/gen_en_override.py` → `python3 _build.py`（否则 4 页手工修复必被回退）。
3. **加门禁**：静态断言 `title-en` 不得为单通用词/`[A-Za-z]+ \d+`/词序错乱三元组；`desc-en` 不得只剩套话；把 `_en_override.json` 与 `slug-en.json` 的差异也纳入校验（两者英文值已出现分叉）。
4. 完整清单（P1 674 行、P2 36 行、P3 47 行 + 20 页真机结果）见本轮只读产物 `/tmp/en-meta-degenerate.md`，可按需复制到本台账附录。

