# DEV-PLAN.md — 待处理任务清单

> **本文件只放「待处理任务」与「干活必须遵守的规则」。已完成项、批次成果、历史操作流水一律不写入** —— 归档走 `.workbuddy/memory/YYYY-MM-DD.md`；历史全量快照另存 `.workbuddy/memory/archive-devplan-full-2026-09-23.md`。
> **收尾口径（老板 2026-09-21 明确）**：闭环 = 本地 build / 门禁通过 + GitHub 部署成功（Actions run success）。**不做线上产物 MD5 落盘比对、不 sleep、不轮询 API**；纯文档类改动（`*.md`、memory）不等部署。
> **状态（2026-09-23）**：全站 209 分类 §4.1 八项目标已收口；A 级率 96.9%；SEO（title / desc / h1 / JSON-LD）维度已治理。**当前主线 = 96 个小行业（687 页）默认态公式精查**（§十 方向1）。

---

## 一、总体目标

线上大部分工具不合格，需优化成**成熟、可直接线上使用**的工具，且要比竞品更强：功能更全、内容更专业、UI 更现代、结果更可信。

---

## 二、未完成的主要问题（逐条对照验收，已完成项已移除）

1. **专业名称缺外链**（§4.1.7）：**已调研、受阻** —— 百度百科对非浏览器请求一律返回 403（含不存在词条），**无法本地验证词条真实性**，批量加外链的死链风险不可自查。替代方案待老板定：① **站内内链**（工具 deep-dive 术语 → 站内对应工具页 / 指南页；零死链、可校验、内链 SEO 收益确定，推荐）；② 克制版百科外链（仅少量高置信术语、每页 ≤2，需承担死链风险）；③ 不做。

> 原「UI 太丑 / 内容不够丰富 / 逻辑错误 / 缺指南 / 下拉占位 / 结果未验证」六项**全站已收口**，不再列为待办；后续只随精查顺带复查。

---

## 三、注意事项

1. 工具都必须是**纯前端**的；不适合本项目的工具（需后端 / 实时数据 / 登录认证等）直接删。
2. 所有**答题类工具**参考样式：`/tools/psychology/tester-2.html`。
3. 有好建议也可补充，只要能提升用户体验和效率的都能加。
4. 之前项目里不合理的约束可以去掉，按最好的方式开发。

---

## 四、开发规则（强制）

- **恢复逐分类完整优化清单（按热度排序）**：全站 268/268 分类虽已完成 deep-dive 占位真实化，但 §4.1 八项目标的其余维度（UI / 指南 / 下拉 / 外链 / 逻辑验证 / SEO 描述等）仍未全站收口。故按**热度（分类下工具页数量）降序**逐分类推进。
- **进行中的分类**：在「当前进行中分类」登记（分类名 + 工具数 + 当前进度）。
- 分类状态按状态机推进（权威定义见 §4.3）：待办保留在 §7.2；开始后写入「当前进行中分类」；完成即从两处删除。状态须在同一次任务中同步更新。
- 每完成一批（或一个工具）跑 `python3 _build.py` + `python3 _test_static.py`，确保门禁通过、繁体 `zh-tw/` 同步。
- **提交发布节奏**：最好**一个分类提交发布一次**；工具多的分类可分批，**每批至少 10 个工具**。
- **发布前必须跑质量门禁、发布后确认部署**：push 前本地跑 `python3 scripts/run_gates.py` 全过；push 后**单次**查询 GitHub Actions 结论即算闭环（**不再做线上 MD5 落盘比对**，见文首收尾口径）。
- **新建页面防死链**：从范本 copy 的页面必须删掉英文版 `hreflang` 链接与 "🌐 English" 按钮（英文走 `?lang=en-US`）；不引用任何不存在的文件。
- **改 deep-dive / 使用指南等被构建重建的区块，必须改数据源 `i18n/tools/content_deepdive.json`**。

### 4.1 每个分类的强制任务目标

每个分类必须覆盖该分类下的全部工具。每个工具必须同时完成以下八项，缺一项都不能结束分类：

1. **功能**：输入、处理逻辑、输出和异常提示真实可用；专业计算用已知样例、独立公式或 `node` 纯函数验证。
2. **内容**：补真实场景、真实示例、边界说明、参考表或可视化；禁止「常见场景：XXX」「先统一输入单位与口径」等套话。
3. **页面**：检查 UI、移动端布局、输入项、下拉选项、默认值、按钮和结果区。
4. **深度内容**：专业工具必须在 `i18n/tools/content_deepdive.json` 有真实条目（场景 ≥2 / 示例 ≥1 / FAQ ≥2）；需要指南的工具补指南入口与数据。
5. **i18n**：同步中文页、行业 JSON、`slug-en.json`、`_en_override.json`、页面英文元信息、英文可见内容和繁体构建结果。
6. **分类**：核对 `<meta name="toolbox">` 的 `industry` 与 `cat`，错标必须在源 HTML 修正。
7. **SEO 与专业性**：Title、Description、H1、JSON-LD 和面包屑用途一致；关键专业名词按需补权威外链，不制造死链。
8. **发布证据**：构建、五项门禁、远端 Actions 成功和提交 SHA 齐备。

### 4.2 提交与发布文件边界

- 修改前和准备提交前都必须执行 `git status --short` 建立本批文件清单；发现非本任务产生的改动，立即停止并确认。
- 禁止 `git add -A` / `git add .`；必须按已确认清单显式 `git add`。
- `json/*.json`、`sitemap.xml`、`sw.js` 等构建产物只能由 `_build.py` 生成。
- 最终汇报必须列出 commit SHA、实际提交文件范围、门禁结果与部署结论。

### 4.3 分类收口顺序与状态同步

每个分类只能按以下顺序收口，不得跳步：

1. **建立范围**：读取该分类实际目录，登记全部工具页。
2. **逐工具处理**：逐个完成八项目标；完成一项就从进行中清单删除。
3. **完成前审计**：确认进行中清单为空，且分类下**没有**：占位套话、缺失 deep-dive、英文通用描述、cat 错标、未验证的关键逻辑、缺使用指南、缺专业外链、UI 未现代化、Description 重复。
4. **同步状态**：从「当前进行中分类」和 §7.2 删除该分类条目。
5. **发布收口**：状态同步后才能跑门禁、提交和推送。

> **硬约束（老板 2026-09-11 明确，违反即违规）**：**一个分类必须把 §4.1 八项目标在该分类下全部工具上完全干完，才能开始下一个分类**；**禁止只挑简单任务**（只清占位 / 只补 deep-dive）就标记完成、跳过 UI / 指南 / 外链 / 逻辑验证等难项。

严禁：只把待办改成 `[x]` 不删除、清单未空就开始下一个分类、八项目标有缺项却标记完成。

### 4.4 使用指南增强规则（老板 2026-09-08 明确授权）

- **判定标准**：*专业度高*（计算 / 判定 / 法规 / 工程 / 医疗 / 金融 / 养殖等，结果影响决策或有行业依据）或 *热门*（高频计算器、换算、收益测算）；满足其一且非纯娱乐工具即应补指南。
- **落地动作**：用 `scripts/gen_guide_pages.py` 批量生成 `guides/<slug>-guide.html`，自动合并 `json/guides.json` 并追加 `guides/index.html`；模板须去除英文版链接与独立 `hreflang`。
- **内容要求**：含适用场景、操作步骤、注意事项、针对性 FAQ，禁止套话。
- **⚠️ 克制原则**：指南页只给「有必要的工具」加，**不要全分类铺量**；纯娱乐、纯文本格式转换、纯展示查询类工具**不生成**。

### 4.5 通用修复清单（质量红线，每个分类必做）

1. **公式数字必须与工具 JS 一致（最高频事故）**：写 deep-dive 算例后必须用 `node` / `python` 按工具默认输入**独立复算**一遍，一致才落盘；禁止凭记忆/估算。任何「差 10 倍 / 数量级不符」都是危险信号。
2. **opt-guide / opt-faq 套话块清零**：处理前先 `grep 'class="opt-guide"\|class="opt-faq"'` 全分类，命中即用 `re.sub(r'<section class="opt-guide">.*?</section>\s*','',t,flags=re.S)` 配对清理，目标**前 N 后 0**。
3. **数据源孤儿条目自动新增**：`tools/` 有页但 `content_deepdive.json` 无条目时须**自动新增**而非 `assert` 中断。
4. **缺数字断言防误伤**：算例含中文数字（四/五/十/百）也视为「有数字」；写入脚本用**增量落盘 + 软警告**。
5. **发布证据**：push 后**单次**查询 Actions 结论（`gh run list --limit 1` 或单次 API 调用）；**不再 curl 落盘比对 MD5**。套话占位指纹：①快速复核 ②统一口径(建模·演示) ③统一复核 ④高频复用模板 ⑤在X业务中先把Y标准化后再执行对比 + 复用模板示例 + 保留复用模板 + 结构性泛化短语（减少重复确认成本/标准化再批量/可复核输出/沿用模板逐项核对/形成标准复核清单/边界样本建议单独标注/降低上手门槛）。
6. **指南页克制**：见 §4.4 末条。
7. **套话指纹持续扩充**：另有变体 `本生成器依据指定格式规范…`、`本速查内容依据权威标准…`、`本计算基于标准数学定义…`。**数量达标 ≠ 内容达标**，必须逐条看内容。**指纹会误伤正常措辞**（如「统一口径」在「先约定统计口径」语境下合法），命中后先判断是否真套话。
8. **审计要查「达标率」而非「覆盖率」**：`content_deepdive.json` 有条目 ≠ 满足 §4.1.4。收口审计必须按「场景 ≥2 且 示例 ≥1 且 FAQ ≥2 且无套话」逐条算达标率。

---

## 五、验收标准

> 验收 = §4.1 八项目标的可勾选版。每个分类收口前逐项确认全部达标。

- [ ] 1. 功能：真实可用 + 独立验证
- [ ] 2. 内容：真实场景 / 示例 / 参考表 / 可视化
- [ ] 3. 页面：UI / 移动端 / 下拉 / 按钮
- [ ] 4. 深度内容：deep-dive 真实条目 + 指南
- [ ] 5. i18n：中 / 英 / 繁完整
- [ ] 6. 分类：industry / cat 无误标
- [ ] 7. SEO 与专业性：Title / Description / H1 / 外链
- [ ] 8. 发布证据：构建 + 门禁 + Actions + SHA

---

## 六、踩坑 / 约束备忘（环境级 / 工程级）

- **deep-dive 由 `_build.py` 按 `i18n/tools/content_deepdive.json` 重建**：直接改源 html 会被覆盖。改 deep-dive / 场景 / 示例 / FAQ → 改 JSON 数据源。
- **FAQPage 结构化数据不被重建**：手动加的 JSON-LD 会保留，但注入坏 JSON 不会自动修复，须自测解析合法。
- **繁体 `zh-tw/` 是构建产物**：勿手动改（被 `.gitignore` 忽略）；其子树不含 `js/`，引用站内 JS 必须绝对路径 `/js/x.js`。
- **i18n 八件套**：标题/简介走 `_en_override.json` + `slug-en.json`；行业 i18n 走 `i18n/tools/<ind>.json`；凡引 `common.js` 的静态页须引 `i18n.js`。
- **门禁**：`python3 _test_static.py` 须 0 失败 0 告警；死链与资产审计须 exit 0。
- **计算函数名不统一**：`calcTool()` / `calc()` / `calcBelt()` 等。抽取时在整个 html 里多候选 `function <name>(` + 花括号配平，勿用 `max(scripts, key=count('calcTool'))`（会选中 stub）。依赖 select 与常量表的工具须先抽 `<select id=...>` 默认项与 `const X = {` 常量表。
- **deep-dive JSON 格式**：仓库规范 `indent=1`，apply 脚本须 `json.dump(indent=1)`，否则全量重排成噪音 diff。
- **英文 p 三种机制（改法不同）**：① `data-zh` —— 英文写在源 HTML，改源文件；② 裸 `<p>中文</p>` —— build 用 `<ind>-body.json` 覆盖，**必须改数据源**；③ `data-i18n` —— 由 build 注入，同样改数据源。
- **英文态数据源三处（最易漏）**：`i18n/tools/<ind>-body.json`（title/h1/intro）、`i18n/tools/<ind>.json` 的 `en-US`（同时是 industry JSON 的 `ed` 最高优先级源）、`_en_override.json`（en/ed）。
- **build 预渲染陷阱（最高频事故）**：`_prerender_tool_body` 用 `count=1` 命中文档**首个 `<p>`**，任何插在首个 `<p>` 前的中文 `<p>` 都会被 intro 覆盖。修法：改成 `<div>` 或补 `data-zh`。该函数**幂等**，故改数据源后必须先把页面「还原」再 build。
- **`desc-en` meta 权威源是 build**：无需手改 meta，改 EN_MAP / 数据源即可。
- **英文管线关键 BUG（已修，勿复现）**：`gen_en_override.py` 曾读 `t.get('i')` 而 `tools.json` 字段是 `industry` → override 全 miss。修法：`t.get('industry') or t.get('i')`。`slug_to_intro` 默认模板恰是审计判定短语，**新增默认文案须避开** `is a free online (tool|...)` / `is available directly in your browser` / `check and validate online` / `Generate results online for free` / `VERB online` 五类指纹。
- **英文副标题 p 已英文不重渲染**：`_prerender_tool_body` 对**已是英文**的副标题 `<p>` 不重渲染，故清副标题必须**直接改写 HTML p 内文**（或扩展重渲染逻辑），不能只改数据源。
- **§8 英文态判据读的是 body 顶层 `intro`，不是 `en.intro`**：后续任何英文 intro 治理必须以顶层 `intro` 为准。
- **指南页模板化识别**：审计判据——核心功能 ≠ 适用场景、使用步骤 ≠ 示例标题且 ≥5 条、实用技巧 ≥4 条。跨分类重名用 `--prefix`。
- **跨分类重名 slug 的指南必须走 `--prefix`**：`guides.json` 按 basename 去重，重名会互覆。`_build.py` 靠指南页正文的**绝对 URL** 反查行业，相对路径不会建立精确映射。
- **计算验证 DOM stub 框架六条踩坑**：① 页面多用 DOMContentLoaded，stub 须收集并执行；② 大量工具用内联 `oninput=`，须解析 HTML 属性；③ 内联 handler 在全局作用域执行，window 须指向 globalThis 且把 `new Function` 顶层函数导出到全局；④ 顶层函数枚举须含 `async function` 且 await 结果；⑤ 结果可能写 textContent 或 appendChild，采集须覆盖 value/innerHTML/textContent；⑥ 用例间须清理挂到 globalThis 的页面函数。**依赖「今天」的日期类用例不可纳入**。
- **静态审计两处已知误报（勿报）**：无 `id="result"`、无 `data-theme` 均为**非缺陷**。
- **deep-dive「覆盖率 ≠ 达标率」有三层套话**：分三处独立查——① `scenarios`/`faqs` 模板 ② `examples` 模板 ③ 英文名嵌入中文（`[A-Z][a-z]+ Validator` 出现在中文句里 = 代号型套话）。
- **Python `a = b = []` 多变量共享同一 list**：写审计脚本时多列表必须逐个独立赋值；计数异常一致时先怀疑脚本。
- **同一逻辑在多个分类重复实现时，抽通用脚本而非复制**：新分类开工前先 `ls scripts/` 查是否有可加 `--industry` 的现成脚本（老板明确偏好复用而非复制）。
- **formula-box 覆盖率全站已 100%**：注入脚本 `extract_formula.py` + `inject_formula_generic.py`（幂等）；锚点 = 标准副标题 `<p>`，**已有 formula-box 的文件一律跳过**；无简单赋值的 calc 诚实 fallback，**绝不写伪公式**。

---

## 七、未完成任务清单

### 7.1 孤立未完成任务（按优先级）

> 跨分类 / 独立的系统性问题，可穿插推进。

**P0 — 已闭环**（原 `upload-pages-artifact` 隐藏文件修复：工作流已用 `@v3` + `include-hidden-files:true`，`.hidden` 文件不漏装）。

**P1 — 待办**

- **隔离器桩缺口两项，未修**：① `document.querySelector('input[name=x]:checked')` 恒返回 null → 单选/复选门控页输出 `undefined`/`NaN`（`optical/progressive-corridor` 等）；② `innerHTML=` 动态生成的控件（`fim-scale`/`womac`/`gingival-index`/`load-curve` 等，静态 HTML `grep id=` 为 0）取不到值。
  - **2026-09-23 实测补记（勿再盲改 harness）**：对 ② 在正式门禁 `scripts/verify_it_calc.js` 实施「`innerHTML` setter 解析 `id=` 注册桩元素」改造，全量门禁立即暴露 `psychology/calc-12` 崩溃（该页用 `innerHTML` 渲染滑块，`getElementById` 读到空桩后读 `.length`/`.trim` 即崩）。**根因**：harness 缺「真实 DOM 行为」模拟，单点 `id` 注册会误伤**所有用 innerHTML 渲染 UI 的页**。已 `git checkout HEAD -- scripts/verify_it_calc.js` 还原，216/216 恢复全绿。**结论**：② 不能靠 `id` 注册解决，须立项「innerHTML 真实 DOM 模拟」专项（大工程，需评估工期）；在此之前**维持原纪律"盲区先排除，再回源码复核"**。缺口 ① 同理风险更高，未实施。
- **`metalwork/tester-19` ≤1kV 耐压分支无法构造判别用例**：该分支输出恒为常数 `3.5 kV`（与 `ratedV` 取值无关），任何 `expect` 都会在**默认态**命中 → 必被判逃生项，故**刻意不补用例**；该修复（`0.0 kV → 3.5 kV`）只能靠隔离器人工跑 + 代码评审保真，回归时注意。
- **「多页签（mode）」页面的非默认页签分支无法被 harness 覆盖**：切页签必须带参调用 `setMode(1)`，而 harness 只无参调用候选函数 → 双样本/第二种模式分支永不执行，`expect` 只对默认页签有效。**复核口径**：复制页面到 `tools/<ind>/_tmp-xxx.html`，把 `let currentMode=0;` 改成 `1` → 隔离器单跑 → **立即删除副本**（勿留待提交）。
- **96 个小行业（<15 页，687 页）未做默认态公式精查**（当前主线，见 §十 方向1）。
- **永久排除（不下架）**：同名异功能 `finance/salary-after-tax`↔`payroll-calculator`、`ophthalmology/self-assess-2`↔`osdi-scale`；跨行业同名编号页（calc-N/rater-N 等 17 个 basename）经内容哈希取证均为不同工具、内容各异，非重复，不处理。

**P2 — 低优先级**

- **指南英文副本（`guides/*.en.html` 100 篇）软隔离已办**：已配为孤儿文件（sitemap 排除 + hreflang/入口移除 + 索引 state 清理）。**文件保留至约 2026-10-21 再物理删除**。
- **`content_deepdive.json` 内 `tools/` 已不存在的孤儿键**：构建不渲染，属冗余；清理时须全站通查（含已下架行业残留）。

### 7.2 分类收口待办清单（按 §4.1 维度）

> 完成一个分类从本节删一个。判定标准见 §4.1 / §4.5。
>
> **当前为空** —— 全站 209 分类已全部收口（2026-09-19 收官）。

### 7.3 C→A 质量提升专项（目标：A 级率 →75%）

> **判定口径**（`_build.py:1701-1744`）：A = `rich 且 own_len≥800` / `own_len≥6000` / `own_len≥3000 且 inputs≥3`。`rich` = canvas/data-viz 或 formula-box 正文 ≥`FORMULA_BOX_MIN_TEXT`(20) 字。
> **状态：目标已达成并超额** —— A 级率 70.0%→**96.9%**（42 批升级）；bucket1（`own_len≥800 且非 rich`，补真实 formula-box）、bucket3 前置段（own_len 700-799 + 真实派生量）、缺陷 J/L/M 全部闭环。
> **明确排除（度量盲区，勿强改）**：`ai/ocr`、`ai/image-classification`（及同类 `ai/*`）逻辑写在 `<script type="module">` 中，而 `own_len` 正则只匹配**裸 `<script>`** → 永远够不到 800。属**度量口径盲区、非页面缺陷**，强行补裸脚本 = 代码膨胀凑数，**不做**。若日后需修正，应改 `_build.py` 的 `own_len` 正则纳入 `type="module"`（框架改动、须单独评估；全站仅 5 页命中）。
> **手法**：计算器补「真实公式说明面板」（含实际公式 + 一句说明，非代码膨胀）；非计算器补真实原理/参考表。
> **复用纪律**：动手前先做全站查重（`tools.json` name 归一化相似度 + 关键词），能存根就存根（成本远低于重做）；存根须留 `TOOLBOX-REDIRECT`（保 URL 零 404，canonical 指向真工具）。
> 逐批明细见 `.workbuddy/memory/2026-09-2*.md` 与全量快照归档。

---

## 八、反模式与防复发（铁律）

> 共性根因只有一句：**动手前拿「我以为的结构」当依据，而不是先验证；且对「爆炸半径」验证不足。**
> 铁律：**任何「完成」结论 = 门禁真跑 + 产物落盘比对双证据。口头打包票一律视为未做。**

### 8.1 假门禁 / 虚假「全收口」声明（最严重）

- **犯错**：把「门禁注册了 + 跑绿」当成「已验证收口」；占位 expect / 缺 `_selfcheck` 标记空跑通过。
- **根因**：**「跑了」≠「过了」** —— 没验证用例是否真正触发页面计算逻辑就报通过。
- **防复发**：报绿灯前必须确认 ① 用例有真实 inputs；② expect **独立复算**（严禁取页面自身输出当期望 = 自证循环）；③ 随机/二进制不可派生页须登记排除，不得凑数。

### 8.2 逃生项 —— 比撞默认值更隐蔽的假通过

**机制**：verify 框架是「`expect` 任一命中即通过」。**只要 expect 里混入一个「不依赖被测输入」的项，输入注入即使完全失败，用例照样 PASS —— 这样的项叫「逃生项」。**

**为什么「零交集断言」防不住它**：零交集只保证「新 expect 不在默认输出里」，但页面常**部分使用输入、部分硬编码** —— 被注入的部分确实不在默认输出中（零交集通过），而**被测点本身没变**，用例无从察觉。

**铁律（写死，每批必须执行）**：
1. **`expect` 的每一项都必须依赖被测点**，不得混入只依赖其它输入或与被测点无关的中间量（df、样本量、求和系数、固定换算常数等）。
2. **避免超短 expect 串**，子串 `includes` 极易误命中。
3. **改造后必须跑判别力验证器**：`node scripts/discriminate_check.js [脚本名]`（模拟注入失败，用例应全部变红）。全站仅约 1 秒。
4. **关键用例必须做反向验证**：临时把被测逻辑改回错误实现，确认用例**真的会红**。

**已固化为门禁**：`scripts/discriminate_check.js` 接入 `run_gates.py`（anti-regression 项），配 `scripts/discriminate_baseline.json` —— **只准降不准增**，下降时必须同步下调基线。

**存量分批专项（见 §10.3）**：改 expect 若取自页面自身输出即「自证循环」，正确修法须**逐例按标准公式独立复算**，故分批推进。

### 8.3 弱用例改造口径（每批固定四步）

**读页面公式 → 选一组与默认不同的输入 → Python 独立复算 → `runCase` 验证 `via=input event`**

| 环节 | 口径 |
|---|---|
| 选输入 | 至少一项数值 ≠ 页面默认；**避免与默认成比例**（比值/乘积巧合会让判别失效） |
| 复算 | 一律用 Python 高精度算（`math` / `Decimal`），不手算尾位；`toFixed` 边界以 Python `format(x,'.1f')` 为准 |
| 验证 | `runCase` 必须 `ok=true` **且 `via=input event`**；`via` 为空说明该串只在兜底阶段出现，等于没验证 |
| 收尾 | `discriminate_check.js <脚本>` 必须 0 逃生项 |

**定位逃生项用「逐项二分」**：把 inputs 换回页面默认值，对 expect **逐项单独**跑 `runCase`，仍 `ok` 的即逃生项。**切勿用 `fullBlob.includes()` 判定**（blob 元素集合不同，会全判为「无逃生」）。判定只看 `blob1`。

### 8.4 批量改动纪律

- **批量改页面前必 dry-run + 逐文件 diff 预览**；改完必做 `grep -rIl` 全仓残留引用复核；遍历一律递归 `**/*.html`，路径一律按 `ind+slug` 精确构造（禁子串 glob，防 `rater-3` 误伤 `rater-30`）。
- **非确定性输入一律种子化**：禁用 `Math.random` / `Date.now` 当输入（harness 已注入 `FrozenDate` 冻结基准日 + `mulberry32` 确定性 PRNG；但新增用例仍不得断言绝对日期或随机命中串）。
- **清理「已完成」标记须同时 grep 全部变体**：`✅` 归档块 + `- [x]` 勾选 + `~~` 删除线，只认一种必漏。
- **同一文件的多处修改必须串行 Edit**：并行发多条 Edit 会出现写回竞态（工具仍报 "Successfully edited"，实际被旧快照覆盖）。改完必须 `grep` 复核关键行。
- **`json/related-tools-curated.json` 的每条引用必须做存在性校验**：构建对指向不存在工具的条目**只打 `WARN` 并静默丢弃该卡片**。改名 / 迁移 / 重定向后必须重跑校验。该文件格式为 `indent=1` **无尾换行**，改它禁止整体重排。

### 8.5 自引用 URL 与「构建兜不住的字段」

- **改名 / 迁移必须同批改 `canonical` + `og:url` 为自指新路径**（179 页曾漏改，canonical 指向永不存在的 `tool-NNN-N.html`，是 Google 明示的可能去索引信号）。**构建兜不住**：`_build.py` 只在缺失时**新增** canonical，已有错值不会纠正。核查命令（应为 0）：
  ```bash
  python3 - <<'PY'
  import glob,os,re
  bad=0
  for p in glob.glob('tools/**/*.html',recursive=True):
      c=open(p,encoding='utf-8').read(); rel=os.path.relpath(p,'.')
      m=re.search(r'<link rel="canonical" href="(https://chenguangwu\.github\.io/tools/[^"]+)"',c)
      if m and m.group(1)!='https://chenguangwu.github.io/'+rel and not os.path.exists(m.group(1).replace('https://chenguangwu.github.io/','')):
          bad+=1
  print('BROKEN canonical:',bad)
  PY
  ```
- **同类「构建兜不住」字段清单（改名/重做时必须同批改）**：`<title>`、`<h1>`、`<meta name="description">`、`og:url`、`canonical`、`title-en`/`desc-en`、`h2[data-zh]`。其余（`formula-box`、deep-dive、关联卡、图标）由构建从权威源重建，改源即可传导。
- **zh-tw 变体的 canonical/og:url 由 `scripts/gen_opencc_locales.mjs` 按路径重写**（不继承源页错值）→ 修源后重跑构建即自动传导，勿手改 `zh-tw/`。

### 8.6 构建期文本注入必须避开 `<script>` 区域

- **任何「按标签正则改全文」的构建期注入都必须先把 `<script>…</script>` 切出去**（`_prerender_tool_body()` 曾对全文首个 `<p>…</p>` 注入英文 intro，命中 `el.innerHTML='<p …>提示</p>'` 这类 JS 字符串 → 撇号/换行未转义 → **脚本整块 SyntaxError、计算器静默失效，且线上可复现**）。
- **写进 JS 字符串的文案必须转义**：单引号串里的 `'` 要写 `\'`；**禁止插入裸换行**（单引号串不可跨行）。
- **门禁 `inline js syntax`（`scripts/check_inline_js_syntax.js`）**：改 `_build.py` 注入逻辑、或批量改 `tools/**` 后必跑；它逐块 `new Function` 只做语法解析，能拦住这一类"静态结构/链接/资源/calc 冒烟/用例断言全过、但脚本已死"的 P0。

### 8.7 公式系数 / 量纲必须逐项核对（公式-脚本一致性精查的产出）

- **精查引擎**（本地 `scripts/_audit_iso_small.js`，`_*.js` 按 `.gitignore` 不入库；支持 `node 脚本 <industry,ind2,...>`）：用**预设 HTML 默认 value 的隔离器**直调真实 `calc()`，收集所有写入容器，筛 `NaN` / `Infinity` / 异常负号 / 荒谬量级。**harness 不预填默认 value 是主要误报源**（`selectedOptions[0]`、`getContext` 缺桩 → 误报 ERR），判读前先确认桩完整。
- **三条高频真缺陷形态**：① 系数写错（`60f/p` 应为 `120f/p`）；② **量纲多乘/少乘 10**（紧度 `d×(P/10)×100` 应为 `d×P`；`kN/cm²→MPa` 漏乘 10）；③ p 值 / 概率类输出越界（`p=1.046>1`）。
- **凡输出「物理上不可能」的值（概率 >1、转差率为负、紧度/覆盖率为负、量级差 10 倍）必查公式本身**，勿以"口径偏差"放过。
- **deep-dive 文案（`faqs`/`examples`/`tips`）是构建产物**：必须改 **JSON 源**（`json.dumps(indent=1)+'\n'`）。若 FAQ 出现「本工具算错了…该项仅作参考」式**免责说明**，说明是已知未修缺陷，应改公式而不是留免责文案。
- **修完页面必回头查 verify 用例**：① 用例 `expect` 可能锚在旧错误输出上；② 该页可能**根本没有用例**（缺陷漏网的直接原因，补一条）；③ 新用例的 `expect` 若在**页面默认输出**里也命中，会被门禁第 217 项判为**逃生项** —— 非默认输入必须使「默认态」不命中。
- **隔离器 `tagAttrs` 必须支持「裸属性」**：只认带值属性的正则会把 `<option … selected>` / `<input … checked>` 整条丢弃 → `preset` 恒落回 `opts[0]`，**全站含 `<select>` 的页默认值都被读成首项**。修法：`([a-zA-Z-]+)(?:="([^"]*)")?`，缺值补 `''`。**凡「引擎默认值与源码 `selected`/`checked` 不符」先查这一条。**
- **deep-dive 主题错配（页面讲 A、词条写 B）是中批量改写的连带产物**：判据 = 词条 `title`/`scenarios` 与页面**当前** `<h2 data-zh>` 不是同一工具。修法：按页面**真实 `calc()` 算法**重写。
- **隔离器桩必须补齐（否则把「未审计」伪装成「桩盲区/无输出」）**：`<textarea>` 默认文本、逐个触发器（一旦写出结果即止）、无 `calc` 命名时取「函数最多」的脚本块、`innerHTML` setter 里 parse `input`/`textarea`/`select` 注册回 `store`、以及 `MutationObserver`/`getElementsByName`/`style.setProperty`/`cloneNode`/`insertAdjacentHTML`/`toBlob`/`ctx.{setTransform,rotate,strokeRect,roundRect}` 等。**升级前的「空 OUT / 请输入数据」不能作为「页面无默认输出」的证据。**
- **判据类修复不要追求「十进制精确」**：几何量常为无理数，严格不等式判据必然误报。**存在性/一致性判据一律留 1% 量级容差。**

### 8.8 有界量的口径自检 + 门禁用例文件「静默失效」自检

- **口径铁律**：凡输出**有天然取值域**的量（决定系数 / 解释方差比例 / 概率 / p 值 / 覆盖率），交付前必查是否越界 —— **越界即公式错**。实例：`science/effect-size-calculator` 把 Cohen's d 的 r² 直接写成 `d²`（d=1.5 → 225%）。**d 与 r 不同量纲，禁止互相替代**。
- **门禁用例文件「静默失效」自检**：`selfcheck_false_pass.js::extractCases` 是「字符串感知」括号匹配器但**不识别注释** —— 用例数组内/前的行注释里出现撇号（如 `// ── Cohen's d → U₃ ──`）会被当作字符串起始 → 括号层级错位 → `extractCases` 返回 undefined → **该文件全部用例静默消失**（`checked=0`、不打印 SKIP、门禁照旧全绿）。**判据：任何 verify 文件的 `checked` 必须等于其用例条数，不等即命中此坑**。

### 8.9 角度标签与公式的「对边一致性」+ 同类换算页交叉核对

- **角度卡片铁律**：凡输出带标签的角（∠A / ∠B / 角 A / 角 B），**公式里的「对边」必须与标签一致**：∠A 的对边是 a，故 `tan A = a/b`、`cos A = (b²+c²−a²)/(2bc)`。**复核口径：取退化特例手算**（如 a=b 时两锐角必为 45°、a≪b 时 ∠A 必接近 0°），不符即错。
- **「夹角」类名要落到定义**：标签含「夹角/之间」的，先用向量点积推导一遍再写代码（矩形两对角线夹角 = `2·arctan(min/max)`，不是 `atan(h/w)`）。
- **同类换算页必须交叉核对**：**同站内存在多个同类换算页时，逐页比对符号与量级，一页错一页对是极强的缺陷信号**（`sphere-volume` 的 1 m³=1000 L 曾写成 `V/1000`，而 `ellipsoid-volume` 正确）。
- **同一物理量跨页必须口径一致**：把「同站实现同一物理量的所有页」列成一组横向比对，公式常数项与分档阈值都要对。
- **组合计数类「×2 / 之和」别手滑**：中位线×2 应为上下底之和；长方体 12 条棱总长应为 `4(l+w+h)` 而非 `2(l+w+h)`。

### 8.10 边界探针（零值 / 空值）+「分支标签自证」+ 个位数 expect

- **默认态全对 ≠ 边界没问题（必跑零值/空值探针）**：`ai` 分类 56 页默认输出只有 1 处语义错，但把「全部输入置 0」与「全部置空」各跑一遍，**31 页（55%）立刻吐 `NaN`/`Infinity`**（全是 0/0 或 x/0）。**精查 SOP 必须包含变体跑：DEF / ZERO / EMPTY（必要时加 NEG），输出只要出现 `NaN|Infinity|undefined` 即立项。**
- **守卫的落地方式（可脚本化，勿逐页手写）**：在 `calc()` 开头注入 `const __fin=(v)=>Number.isFinite(v);`，把每个 `${__vN.toFixed(d)}` 改成 `${__fin(__vN)?__vN.toFixed(d):'—'}`，并在赋值前追加 `const __bad=[...].some(v=>typeof v==='number'&&!Number.isFinite(v)); if(__bad) html += '<p style="color:var(--danger);">⚠ 部分结果无定义（分母为 0 或输入为空），请检查输入。</p>';`。默认态无 NaN ⇒ 输出零回归，可安全批量。
- **「对比分支」标签必须自证**：凡页面并列多档对比（低温/高温、乐观/悲观、快速/慢速），每档必须真的用不同参数，并在标签里写明。**深度解析里的概率/数值算例一律用脚本重算后再写**。
- **个位数 expect 极易被默认输出吃掉**：expect 出现一位数时，换输入让它变成两位以上，或直接剔除该项。

### 8.11 「过滤器 / 硬化函数」必须验证真的被调用（定义 ≠ 生效）

- **`_inject_output_guard_v7.py` 的 `expr_is_safe_to_guard` 只被定义、从未在 `transform()` 里调用** —— "保守过滤"从未生效。**教训：凡"加了过滤 / 白名单 / 守卫"的改动，必须用一条反面样本证明它真的拦住了**（喂一个应被拦下的输入，确认输出不变）；否则"定义即生效"只是错觉。
- **过滤"过宽"与"未接线"同样有害**：静态字符串含独立 NaN 词或等于 `'Infinity'` 的 RHS 全站命中 **0 处**，而模板串 / 字符串拼接 / 动态容器变量的守卫**真机上确能拦截 NaN 经插值泄漏到页面**。若跳过模板字面量 / 字符串 / method 链，反而**削弱真机防护**；v8 只跳过"纯静态字符串字面量 RHS"。
- **守卫只应注入「数值输出页」**：对纯文本/工具页（如 `it/html-escape`、`it/code-runner`）注入含 `NaN` 文本检测的守卫会**误伤正常输出**（转义后的 JS 代码里出现 `NaN` 就被判为无效值）。**注入前先判页面是否有数值输出/`type=number` 输入。**
- **harness 盲区页无法静态识别，只能试错**：正确流程是 **注入 → 跑该行业 verify → 失败页写入 `--skip` 清单 → 带 `--skip` 重跑 → 直到全绿**（v8 已实现）。

---

## 九、发现但未修的真实缺陷（待老板定夺）

> **已闭环的缺陷 A / C / D / E / G / I / J / K / L / M / N / O / P / Q / R / S / T / U 均已修复并归档** —— 根因与防复发铁律已提炼进 §八，逐批明细见 `.workbuddy/memory/2026-09-2*.md` 与全量快照归档。本节只留**仍未处理**的项。

- **缺陷 B**（`scripts/verify_it_calc.js` 兜底阶段的 `DESTRUCTIVE` 正则只拦 `reset|clear|restore|save|swap|history`，未拦 `set*`/`del*` 类设值/删除函数）：**评估结论 = 不修**。`runCase` 被全站 200+ 脚本复用，补充 `set*`/`del*` 会同时改写全站门禁兜底行为，回归风险远大于收益（`set`/`del` 无参调用通常 crash 或无效，不产出错误结果）。**归档为已知项**。
- **`martial/routine-timer` 默认态输出 `速度比率：Infinity%`**：`loadStandard()` 在页面加载时即调 `compare()`，而 `myTime=0` → `speedPct = std/0*100 = Infinity`，并据 0 秒算出「预计扣分 35.0 分」。**属待修 P0**（页面加载即显示物理不可能值与虚构扣分）。
- **小行业精查进行中**：96 个小行业（687 页）默认态精查已启动，确凿缺陷按「修 calc + 补/改用例 + 门禁」闭环（见 §十 方向1）。

---

## 十、优先级与当前主线

> **主线 = 优化工具页面本身（`tools/**`）。** `scripts/` 下多数验证脚本是历史遗留，**除门禁必需外不单独投入**；只在优化某分类、确实碰到该分类用例时**顺手改**，不单独立批次、不为改脚本而改脚本。

### 10.1 优先级总纲

| 级别 | 内容 | 状态 |
|---|---|---|
| **P0** | 页面级真实缺陷修复（§九 清单） | A/C/D/E/G/I/J/K/L/M/N/O–U 已闭环；**小行业精查进行中**，后续随精查顺带处理碰到的页面缺陷 |
| **P1** | 按热度逐分类 §4.1 八项目标收口 | **全站 209 分类已收口**（§7.2 为空） |
| **P2** | ✅ 工具质量分级提升（C→A） | **已达成：A 级率 70.0% → 96.9%**（§7.3） |
| **P3** | `scripts/` 用例与基线维护（弱用例去默认化等） | **仅随 P0/P1 顺带处理**；门禁必需项（`run_gates.py` 链路）除外 |

### 10.2 现状（实测基线）

- `all_default 237 / no_inputs 212 / escape 0`；门禁 `run_gates.py` **217 项全过**、逃生项 0。
- 存量弱用例 **449 例**（`no_inputs=212` / `all_default=237`），**转 P3 顺带**，不单独成批。

### 10.3 弱用例去默认化（仅在 P0/P1 顺带时执行）

**存量 449 例**。可注入性预筛清单（弱例数 / 页面含静态表单控件数）：

dermatology 14/11、engineering 14/11、signal 11/11、design 10/10、rheumatology 14/9、endocrinology 10/9、mining 10/9、gas 9/9、mechanical 9/9、travel 9/7、gardening 8/7、finance 7/7、sports 7/7、fire 7/6、chemical 9/5、cleaning 7/5

### 每批收口流程（顺带改造时六步，缺一不可）

1. 改写 `scripts/verify_<cat>_calc.js`（非默认输入 + Python 独立复算 expect）
2. 单跑 100% 通过 → `node scripts/discriminate_check.js verify_<cat>_calc.js` **0 逃生项**
3. 被「跳过」的用例（textarea / 动态 id / 无 value input）必须**自建同口径探针**补验「注入 PASS + 回退默认 FAIL」
4. 更新 `scripts/falsepass_baseline.json` 与 `scripts/discriminate_baseline.json`（**只准降不准增**，按 selfcheck/discriminate 实测值同步）
5. `python3 scripts/run_gates.py`（全量 217 项）全过 → `git commit` + push、**单次**确认部署
6. 归档 `.workbuddy/memory/YYYY-MM-DD.md`，清理 `/tmp` 临时脚本

### harness 已知限制（选批与定 expect 前必读）

| 限制 | 后果 / 处置 |
|---|---|
| **纯 checkbox 评分页不可注入**：`makeEl` 桩 `checked` 恒 false，注入只写 `.value` | `c.checks` **只作用于 `querySelector(':checked')`/`querySelectorAll('…checked')`** —— 只有用选择器读选中态的页面才可注入。其余判结构性 `no_inputs`。**被 checkbox 门控的页面可改判「门控前的派生量」** |
| **动态 id（`q0..qN`）会同时骗过两道静态校验** | `discriminate_check` 判「跳过」、`selfcheck` 判 `null` 不计入 → **基线会「虚降」**。须自建探针补验「注入 PASS + 回退默认 FAIL」，并另用浏览器真实默认值再跑一遍 |
| **textarea / 无 value 的 input 在判别器里必落「跳过」** | `discriminate_check.pageDefaults()` 不解析 textarea、无 value input 返回 undefined → 整例跳过。须自建同口径探针补验 |
| **判定发生在 `blob1`（注入后立即收集），不是 `fullBlob`** | 用 `expect:["@@NOMATCH@@"]` 取输出「看结果」是错的。定位逃生项只看 `blob1` |
| **页面源码字面量 + 静态参考表 + 恒定文案都进 blob** | 凡页面含「参考表/换算表」容器且带 id、深度解析示例、图例文案，其数值/词汇均不可作 expect。定 expect 前先 `grep -c "该串" tools/<slug>.html` |
| **「暂无…记录」等占位串是常量型逃生项（命中率最高）** | 凡页面含 `saveHistory/renderHistory/historyBox`（写 localStorage，harness 无实现 → 恒显占位），该串一律不得作 expect |
| **长数字的后缀会吞掉短 expect** | 光「加长」不够，还要防默认态存在以它为后缀的更长数字（`5000.0 g` 被 `15000.0 g` 包含）。修法：合并为跨格连续串 |
| **等级词/分类词须「跨档」** | 定等级类 expect 前必须先算一遍默认态的同档位，不跨档就换锚点数值 |
| **select 在两道校验里取值口径不同** | `selfcheck._pageDefaults` 读全文（取 JS 设定的真实默认），`discriminate_check.pageDefaults` 取**首个 option**。凡页面对 select 值做三元兜底，非预期值会与另一选项同分支 → 这类词不可作 expect |
| **兜底函数的「随机态」会命中等级词** | 凡页面存在 `randomXxx()`/`shuffle` 类兜底函数，等级词一律不用，改断言只由注入值派生的量 |
| **含 `<` 的输出会被标签剥离吞掉** | 如 `< 0.001`，不可作 expect；改锚 Z 统计量 / 置信区间 / 结论文案 |
| **检索/过滤型图鉴页的结果是全量列表的「子集」** | 任何「单卡片内文本」在默认全量态同样存在，作 expect 必为逃生项 |
| **兜底阶段会调用 `swapValues()`（`DESTRUCTIVE` 的 `swap\b` 对它无效）** | 该函数把两个输入**互换后重算** → **二值判读词**（偏高/正常、力度偏大/适中、A 优于 B…）在交换态必命中其中一档 → 判定词一律**不得作 expect**，只锚依赖被测输入的数值项 |
| **`blob.includes(want)` 是子串匹配**（`collectStrings` 返回拼接后的单字符串） | expect 会被默认输出包含：`达标` ⊂ `未达标`、`5.00%` ⊂ `25.00%`。定 expect 前须做「默认态 + 交换态」**双侧子串**检查，必要时给 expect 加标签前缀 |
| **expect 与「默认态输出」字符串一致 → 逃生项**（即便注入的是另一组输入） | 只看 `x/x 全过` 会漏判。**新增用例后必须跑 `discriminate_check`（或先手算默认态输出）**，并换一组能跨分支/跨档的数据 |
| **`select` 的 `selected` 属性在 harness 里不生效**（桩取**首个 option**） | 页面「默认选中项」类改动无法用默认态用例验证 —— 必须**显式注入该 select 的值**；判断真实浏览器行为只认 HTML 标准 |
| **页面自带的 `fmt()` 常走 `toLocaleString()`（默认截 3 位小数）** | `0.0025` 会显示成 `0.003`，使「分步计算」文案无法自校验、也易被误判为算术错。凡步骤/卡片要展示小数量，改用带参 `toFixed(n)`；定 expect 时避开被截断的位置 |

### 方向1 公式-脚本一致性精查（进行中 · 老板选定）

- **目标**：逐页独立复算计算类页 `calc()` 输出的数学/物理正确性（与标准公式/权威向量比），找"用户拿到错钱数/错物理量"的真缺陷（§4.5 红线第一条最高频事故）。
- **已完成覆盖**：10 高热度行业（science / math / geometry / photo / ai / sports / agriculture / finance + 首批 finance 残页）+ 金融周边集群（banking/investment/tax/realestate/accounting/insurance/economics/statistics/forex/futures ~334 页）**全量闭环**；中低热度 113 个行业（页≥15）默认态**全健康**；边界 NaN 守卫已铺开（含 4 个待办分类 86 页 + 7 个物理工程行业 194 页）。
- **未覆盖（本批）**：**96 个小行业（<15 页，687 页）**从未精查。工具：`scripts/_audit_iso_small.js`（隔离器增强版：动态 `<select>` 注册、按文档序拼接内联 JS 块、补齐 MutationObserver/getElementsByName/style.setProperty/cloneNode/insertAdjacentHTML/toBlob/ctx.* 等桩）。
- **SOP**：① 隔离器扫 DEF 态 → 筛 `NaN`/`Infinity`/越界值/`err`；② 每条 `err` 先判「桩盲区」还是「真缺陷」（回源码 + 必要时用 jsdom 跑）；③ 变体跑 ZERO / EMPTY 找边界 NaN；④ 确凿缺陷才改页，改完补/改用例。
- **纪律**：确凿真缺陷前不改页面；找到即立项闭环（修 calc + 修/注册 verify 用例 + run_gates + 提交推送）。
