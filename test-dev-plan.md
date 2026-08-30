# test-dev-plan · ToolBox 测试报告问题修复分批计划

- **来源**：`ToolBox测试报告_三方合并+补充验证终版_v2.1.md`（44 问题：P0×11 / P1×12 / P2×11 / P3×10）
- **总原则**：先核实再改，不照抄报告盲改；抽样问题必须排查扩散（死链 / 公式名 / 裸露 key 等）；每批走 `修复 → build/门禁 → 验证 → commit → push`。
- **已先核实的结论**（避免误改，报告部分说法已过时/不准）：
  - **P0-01 / P0-02 死链 ✅确认**：`unit-converter.html`、`uuid-v4-generator.html` 才存在；`HOT_TOOLS` 两处 + `404.html` 的 `PATH_MAP` + `404.html` 的 `HOT_TOOLS` 都指向已删除旧路径（`converter.html` / `uuid.html`）。
  - **P0-03 倒计时器默认秒表 ✅确认**：`stopwatch.html` 的 `currentMode='stopwatch'`，但卡片叫「倒计时器」。
  - **P0-07 i18n key 裸露 ✅确认**：`I18N_MSG` 缺 `tool.copy`/`tool.related`/`common.loading`，且三处 `i18nText()` 无 fallback；zh 包为空 → 回退裸 key。
  - **P0-04 搜索返回全部/时序 ⚠️疑似已修复**：`app.js` 已用 `toolboxSearch`+debounce+空结果态，标记为「回归验证」。
  - **P0-05 统计数字不一 ✅确认**：hero `6000+` / sub `5014+` / why-card `6060+` / footer `6000+` 口径混乱。
  - **P0-06 / 08 / 09 / 10 / 11 / P1-01 / P1-12 等**：多为已通过 `data-i18n-fb` 或现有组件覆盖，逐条核实后针对性处理，不做表面修改。
  - **P1-09 索引名称异常 ✅确认扩散**：报告举例 `bercent`/`ending-` 已随重建消失，但现存在 **164 个「公式字符串作为名称」** 的工具（math/statistics/banking/economics/investment/optics/fluid/robotics/quantum/nuclear/aerospace/dynamics/kinematics/process/astronomy…）。根因：源页 `<title>`/`<og:title>` 被公式替换，`<h1>` 正确。修复：用 `<h1>` 回写 `<title>`/`<og:title>` 后重建索引。
  - **P1-08 套壳模板**：全量扫描 0 命中，暂无需处理。

---

## 批次

### Batch 1 — P0 死链 + i18n 裸露 + 默认标签（高置信 / 低风险）【已完成 · 已提交 0e707620】
- [ ] P0-01 `js/app.js` `HOT_TOOLS[6]` → `tools/life/unit-converter.html`
- [ ] P0-01 `404.html` `PATH_MAP.converter` + `HOT_TOOLS` 单位换算 → `unit-converter.html`
- [ ] P0-02 `js/app.js` `HOT_TOOLS[10]` → `tools/it/uuid-v4-generator.html`
- [ ] P0-02 `404.html` `PATH_MAP.uuid` + `HOT_TOOLS` UUID → `uuid-v4-generator.html`
- [ ] P0-07 `js/common.js` 加 `I18N_MSG` 三键 + 三处 `i18nText` 补 fallback
- [ ] P0-03 `tools/it/stopwatch.html` 默认标签改 `countdown`
- 验证：`node --check` 两 JS；手动确认两死链 200；build 非必须（未改工具页）

### Batch 2 — P1-09 公式名称坏数据（164 工具，抽样扩散发现）【已完成 · 已提交 63dca724】
- [ ] 脚本：用 `<h1>` 正确名回写 164 页 `<title>`/`<og:title>`/`<twitter:title>`
- [ ] `_build.py` 重建索引
- [ ] 验证：`search-index.json` 公式名 = 0；`_test_static.py` 门禁

### Batch 3 — P0-05 统计数字统一 + 404 增强【已完成】
- [x] 首页四处数字统一口径为品牌 `6000+`：
  - `index.html:643` `hero.sub` fb `等5014+实用工具` → `等6000+实用工具`
  - `index.html:712` `why.c4_title` fb `6060+ 全覆盖` → `6000+ 全覆盖`
  - `js/i18n.js:161` `why.c4_title` 英文包 `6060+ full coverage` → `6000+ full coverage`
  - `_build.py:1736` 不再注入真实工具数（原 `等%d+`→ 真实 5014），改为固定 `等6000+实用工具`，否则 build 会把 hero.sub 覆盖回真实数
- [x] 404 自动跳转确认：PATH_MAP 在 Batch1 已修（`uuid.html`→`uuid-v4-generator.html`、`converter.html`→`unit-converter.html`），逻辑正确，无需再改
- [x] 三道门禁通过（_test_static 0 / _audit_links 0 死链 / _audit_assets 0）
- ⚠️ 遗留品牌决策（待老板确认，未擅自改）：build 实算当前真实工具数 = **5014**，全站品牌口径却写「6000+ 工具」（title/description/og:image:alt/footer/manifest/search/404 页约数千处）。若要求「数字真实」，需全站改为 `5000+`/`5014+`，涉及改 `_build.py` 模板并重建约 5000 工具页 og:image:alt，是大改动，等老板拍板再做。P0-05 本条仅解决「首页三处数字不一」的不一致问题。

### Batch 4 — P0-10 / P0-11 移动端搜索入口 + 分类按钮截断【已完成】
- [x] P0-10 移动端搜索入口：经查 `.nav-mobile`（顶部移动导航，含搜索按钮 625 行）基础 `display:none` 且无 `@media(max-width:767px)` 覆盖 → 移动端整条隐藏，搜索按钮不可见；底部 `.tab-bar` 可见但无搜索项。`openMobileSearch()` 函数本身正常。修复：在底部 `.tab-bar` 第 3 位插入搜索按钮（`tabBarSearch` → `openMobileSearch()`，图标+`data-i18n="tabbar.search"` 中/英「搜索/Search」），移动端 1 步可达搜索。
- [x] P0-11 分类按钮截断：报告说的 `.ind-btn` 在本代码库不存在，真实分类按钮类是 `.industry-card`（`js/app.js:422` 渲染，原无 `title`）。修复：① `renderIndustries()` 按钮加 `title="${_ind(info, key)}"`（悬浮看全名）；② `.industry-name` CSS 加 `white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0`，截断为干净省略号而非硬裁。
- [x] 补充 i18n：`js/i18n.js` 加 `'tabbar.search': 'Search'`
- [x] 三道门禁通过（_test_static 0 / _audit_links 0 死链 / _audit_assets 0）；node --check 两 JS 通过；build 幂等（底部搜索按钮与 CSS 改动未被 build 覆盖，已验证）

### Batch 5 — i18n 补缺与模板一致性（P0-06 / P0-08 / P1-01 / P1-12 / P0-09）
- [ ] 逐条核实，已覆盖的标记跳过，缺的补充 key
- [ ] 工具页模板 / 广告一致性核查

### Batch 6 — 搜索 / 细节 / P3 回归验证
- [ ] P0-04 / P1-02 / P1-04 / P2-xx / P3-xx 回归（多为已实现，验证为主）
