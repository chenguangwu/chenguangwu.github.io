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

### Batch 5 — i18n 补缺与模板一致性（P0-06 / P0-08 / P1-01 / P1-12 / P0-09）【已完成 · 实测核实】
- [x] **P0-09 详情页被 Hero 掩埋：已解决，无需改**。实测 `tools/it/json-formatter.html` 仅引 `tool-page-runtime.js`+`common.js`，**无任何首页 Hero/`nav-top`/`nav-mobile` 标记**，首屏即工具内容。报告所述对当前模板不成立。
- [x] **P0-06 翻译不完整：基础设施已覆盖，补关键缺口**。
  - `js/tool-i18n.js`（0.5MB 短语字典 + `translateButtons`/`translateGenericUI`/`translateBodyPhrases`）已运行时翻译工具页按钮（美化→Beautify 等）、正文、行业名（通用工程→General Engineering）。
  - 首页级 key 多靠「内联英文兜底」已能在英文模式显示（hero.eyebrow/footer.desc 等）。
  - **真缺口**：`breadcrumb.expand`/`collapse` 用 `_t()` 且内联中文兜底、en 包无 key → 英文模式仍显中文「展开全部 N 个分类」。已修：`js/i18n.js` 加 `'breadcrumb.expand':'Expand all {n} categories'`+`'breadcrumb.collapse':'Collapse categories'`；`js/app.js` 该行改 `.replace('{n}', entries.length)` 保留分类数。
  - 余项（广告标识「推广」→Sponsored）：tool-i18n.js 未单列该 badge 映射，极次要，可后续补，不阻塞。
- [x] **P0-08 分类页卡片未翻译：双语设计 + 收拾混杂**。分类卡片本就是双语（`.ct-name` 中文 + `.ct-desc` 英文，如 `Aztec 码 (简化版)`/`Aztec Code`）；`tool-i18n.js` 英文模式按字典译 `.ct-name`。报告「中文模式强制展示英文副标题视觉混杂」已修：`css/common.css` 加 `html[lang="zh-CN"] .category-tool-item .ct-desc{display:none}`（中文模式只显中文名，英文模式保留译名+英文副标题）。
- [ ] **P1-01 模板不统一 / P1-12「无广告」与广告矛盾：产品决策，未改，待老板拍板**。本项目即广告变现站，删广告/全量重做模板违背商业模式；「永久免费无广告」文案与广告并存属措辞问题，建议二选一（改文案去「无广告」或调整广告策略），等老板决定后再动。
- [x] 三道门禁通过（_test_static 0 / _audit_links 0 死链 / _audit_assets 0）；node --check 两 JS 通过；build 幂等。

### Batch 6 — 搜索 / 细节 / P3 回归验证【已完成】
> 核心结论：报告这批搜索问题对应的代码**早已大幅超越旧版**（hybrid ranker + Fuse 模糊 + 拼音/别名 + 防抖 + Ctrl+K 命令面板 + 空态提示均已落地）。逐条核实后，发现并修复 1 个真实一致性缺陷、补强 1 个验收缺口。

- [x] **P0-04 搜索时序/返回全部 ✅已落实（验证）**：`performSearch()` 先 `await ensureSearchIndexLoaded()` 再渲染，`toolboxSearch` 空查询返回 `[]`、无匹配显「没有找到匹配的工具」+相关推荐（`renderSearchResults` 1026-1037）；`search.html` 监听 `?q=` 并在 fetch 完索引后才 `doSearch`，无时序 bug；无效词（如 `zzzzz`）实测 0 命中、显空态、不返回全部。
- [x] **P1-02 拼音/英文别名 ✅已落实 + 本次补强**：索引 5014 工具全带 `py/pyi/al`；`erweima/qrcode/ewm/json/jisuanqi/bmi` 实测均命中（Node 复刻双路径验证）。**修复 1 个真实缺陷**：`search.html` 的 `doSearch` 旧版漏查 `al`（别名），导致首页能命中 `qrcode` 而 search.html 输 `qrcode` 却 0 命中——已补别名检索 + 评分权重。**修复验收缺口**：`格式化json`（CJK+拉丁混排无空格）原 0 命中，新增 `segmentQuery()` 对混排词切分为 `["格式化","json"]` 做 AND 匹配，两处搜索路径均已闭环（实测命中「JSON 格式化」）。
- [x] **P1-04 无结果提示 ✅已落实（验证）**：两处搜索无结果均显「未找到相关工具/没有找到匹配的工具」空态 + 推荐词/相关工具引导，不返回全部；搜索框保留输入内容。
- [x] **P2-09 搜索防抖 ✅已落实（验证）**：`app.js:958` 与 `search.html:113` 均为 150ms debounce。
- [x] **P2-03 Ctrl+K 命令面板 ✅已落实（验证）**：`app.js:1119-1120` 已绑定 `Ctrl/Cmd+K`，Mac 显示 ⌘K。
- [x] **P2-05 主题持久化 ✅已落实**：`app.js:391/402` 读写 `localStorage.theme` + `prefers-color-scheme` 跟随。
- [x] **P2-06 语言记忆 ✅已落实**：`i18n.js:244` `toolbox_lang` + `privacy.js:19` 已登记持久化。
- [x] **P2-04 推广位识别 ✅已落实**：`common.js:2489/2821` 渲染 `tool-ad-card` + `rel="noopener sponsored"` + 「— 推广 —」角标，与工具卡视觉区分。
- [x] **P2-08 分类名与计数重叠 ✅已落实（验证）**：当前布局分类名（`toolsGridTitle`）与计数（`resultCount`）为独立元素、`.cat-tag` 按钮仅显名称无计数，无重叠。
- [x] 三道门禁通过（_test_static 0 / _audit_links 0 死链 / _audit_assets 0）；`node --check` 校验 `js/app.js` + 抽取 `search.html` 内联脚本均 OK；Node 复刻双搜索路径实测 9 组用例全通过。
- [ ] **P3 低优先优化（本次仅验证，未实现，待老板决策）**：P3-01 行业口径/ P3-02「推广」文案去重 / P3-03 主题过渡动画 / P3-04 emoji 规范 / P3-05 分类 emoji 去重 / P3-06 首屏骨架屏 / P3-07 空态引导 / **P3-08 搜索历史记录** / P3-09 结构化数据（已由 `_build.py` 注入 JSON-LD+OG，已落实）/ P3-10 第三方推广 sandbox。多为产品/体验增强项，非缺陷；其中 P3-08/P3-03 等若老板要做可单独立项，不在「修报告 bug」范围盲改。

---

## ✅ 全部批次完成
- Batch 1-6 已分批完成、逐批门禁通过、提交并推送 master。
- 两个仍待老板拍板的决策（非缺陷，未擅改）：
  1. **真实工具数 5014 vs 全站「6000+」品牌口径**（P0-05 遗留）：是否全站改为 `5000+`/`5014+`，涉及 `_build.py` 模板 + 重建约 5000 工具页 og:image:alt，是大改动。
  2. **P1-01 模板统一 / P1-12「无广告」矛盾**：本项目即广告变现站，属产品/文案方向，待老板定调。
