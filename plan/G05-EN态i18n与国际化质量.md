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

### 确认缺陷 G05-A：预设按钮 `labelEn` 混入中文（高，5 条 / 3 页）
- 问题：英文态下场景预设按钮直接使用 `labelEn`，其中 5 条含汉字，EN 态出现中英混排；属第三层词典之外的「页面内联文案」漏网。
- 证据（逐条）：
  - `tools/encode/convert-4.html:397` — `"labelEn":"Char 中 to code point"`
  - `tools/optical/photochromic-lens.html:524` — `"labelEn":"Plateau UV fast变色"`
  - `tools/property/fee-allocation.html:572` — `"8万 by area"`、`"3万 by household"`、`"12万 by area"`
- 影响：3 页的英文态；不触发运行时词典（labelEn 是内联属性，不走第三层 map）。
- 方案：改成纯英文（`Chinese char to code point` / `Plateau UV fast tinting` / `80,000 by area` 等）；同类问题应加入「预设 labelEn 禁止 CJK」的静态门禁（见 G08）。
- 复核方式：`grep -n 'labelEn.*[一-龥]' tools/**/*.html` 应为 0（排除 `labelEn` 值为纯符号/数字）。

### 疑似待验证 G05-B：第三层词典对新预设页面的覆盖未量化
- 问题：P1（第三层词典覆盖缺口）仍无量化清单；本轮只能确认页面模板级 i18n 引用齐全（`common.js` 缺 `i18n.js` = 0），无法证明 3845 个 preset 页的说明文案在 EN 态全部命中。
- 证据：`js/tool-i18n.js:613` 动态加载 `/js/tool-i18n-en.js`（681KB）；`i18n/tools/en/**` 按工具一文件；本轮未运行 EN 态真机探针（项目规则要求 `scripts/_en_i18n_probe.mjs --check`，属可执行门禁，本轮只读未跑）。
- 影响：全站英文态。
- 方案：第二轮用 `scripts/_en_i18n_probe.mjs --check` 抽样 50 个新增 preset 页，产出 miss 清单后补第三层；禁止只改 HTML 内联（构建会还原场景外的数据源文案）。

### 已修 G05-C：`opt_faq_ld_sync.py` 整段正则吞行（2026-11-04，commit 随脚本落地）
- 症状：旧实现正则 `(<script …ld+json>\s*)(\{.*?"@type":"FAQPage".*?\})(</script>)` 的 `.*?` 含换行，会从**页面第一个** ld+json 块的 `{` 一路跨到 FAQPage 块的 `}`，把中间的 `WebApplication` LD、`TOOLBOX-SECURITY` meta、privacy/metrics/i18n/nav 脚本、hreflang 整段当成「old」替换掉。实测 `tools/livestock/heat-stress-index.html` 少 47 行（结构全丢）。
- 复现页面：`tools/livestock/heat-stress-index.html`（多行 LD，第一个块是 WebApplication，FAQPage 在第三个块）。
- 修法：改为逐块匹配 `<script type="application/ld+json">…</script>`，每块单独 `json.loads`，只替换 `@type=="FAQPage"` 且含套话的那块，其余块字节原样保留；默认 dry-run，写盘需 `--apply`。
- 自检：落盘前后比对 `application/ld+json` / `<meta name="toolbox"` / `TOOLBOX-SECURITY` / `js/privacy.js` / `js/i18n.js` / `hreflang` 六项计数，任一变化即中止且不写盘；单行 LD 块额外校验文件行数不变。
- 回归：取 `f723934c82^` 的 `heat-stress-index` / `feed-conversion-ratio` / `inbreeding-coefficient` 三页副本跑 `--apply`，行数 605/588/592 **零减少**，`diff` 仅 1 个 hunk、只替换 FAQ 那一行。

