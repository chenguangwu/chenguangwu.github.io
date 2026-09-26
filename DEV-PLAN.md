# DEV-PLAN.md — 待处理任务清单

> **本文件只放「待处理任务」与「干活必须遵守的规则」。已完成项、批次成果、历史操作流水一律不写入** —— 归档走 `.workbuddy/memory/YYYY-MM-DD.md`；历史全量快照另存 `.workbuddy/memory/archive-devplan-full-2026-09-23.md`。
> **⚠️ 体积红线（硬约束）**：`wc -c DEV-PLAN.md` **> 60 KB 即说明有批次流水混入，先清理再干活**。每批收尾**只允许**更新 ① §10.2 的计数行 ② §10.3 的存量数与不可注入清单 ③ §九/§7.1 的**待办增删**；**禁止把「本批处理了哪些例、逐例打法、验证过程」写进本文件**（这些一律进 memory 与 skill）。清理时先把全文快照存入 `.workbuddy/memory/archive-devplan-full-YYYY-MM-DD.md` 再删。
> **收尾口径（老板 2026-09-21 明确）**：闭环 = 本地 build / 门禁通过 + GitHub 部署成功（Actions run success）。**不做线上产物 MD5 落盘比对、不 sleep、不轮询 API**；纯文档类改动（`*.md`、memory）不等部署。
> **状态（2026-09-23）**：全站 209 分类 §4.1 已收口；A 级率 **99.2%**；SEO 与术语内链（1591 页 / 2268 条）已治理；小行业精查已闭环（见 §10.6）。**当前无进行中批次，待办见 §九。**

---

## 一、总体目标

线上大部分工具不合格，需优化成**成熟、可直接线上使用**的工具，且要比竞品更强：功能更全、内容更专业、UI 更现代、结果更可信。

---

## 二、未完成的主要问题（逐条对照验收，已完成项已移除）

> **当前为空 —— 原列 7 项已全部处置。** 前 6 项（「UI 太丑 / 内容不够丰富 / 逻辑错误 / 缺指南 / 下拉占位 / 结果未验证」）全站已收口；第 7 项「专业名称缺外链」因**百度百科对非浏览器请求一律 403、无法本地验证词条真实性**，经老板拍板改走**站内内链**方案并已落地（机制与现状见 §六 术语内链条目）。后续只随精查顺带复查。

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
7. **SEO 与专业性**：Title、Description、H1、JSON-LD 和面包屑用途一致；deep-dive 正文的关键专业名词由构建期 `linkify_terms()` 自动补**站内内链**（零死链，不链站外）。
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
- **术语内链唯一源 = `_build.py::linkify_terms()`**（§4.1.7「SEO 与专业性」）：把 deep-dive 正文（场景 / 示例 / FAQ）里的专业名词链到站内工具页 / 指南页。术语 = 工具中文名 + 剥通用后缀的核心词（`_TERM_LINK_SUFFIXES`）+ 指南标题去「使用指南」；**目标必须存在且非 `TOOLBOX-REDIRECT` 存根**（结构性零死链）。细则：逐字符最长匹配（`first_map` 首字母索引，实测 1.3s 全量）、`TERM_LINK_MIN_LEN=3`（2 字泛词会大面积误链——「公式」曾命中 844 次）、每目标页每页只链一次、单页总上限 `TERM_LINK_MAX_PER_PAGE=6`（跨字段共享状态）、不链自身、ASCII 术语要求词边界（防 `CSS` 命中 `CSS3`）。**禁在页面手改内链**（会被构建覆盖）。现状：1591 页 / 2268 条 / 唯一目标 630。
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
- **仓库体积（`.git`）维护**：`du -sh .git` > **800M** 即跑 `git repack -a -d` + `git prune-packed`（合并全 pack、**不 prune 任何不可达对象**，零工作区影响、可随时重跑）—— 参考实测 860M（29 pack）→ 662M（1 pack）。另注：仓库另有约 103M **不可达对象**（经查全是 `git stash` 残留），清理须 `git prune`（**不可恢复 → 须老板拍板**，Agent 只报数据不做）。
- **同一逻辑在多个分类重复实现时，抽通用脚本而非复制**：新分类开工前先 `ls scripts/` 查是否有可加 `--industry` 的现成脚本（老板明确偏好复用而非复制）。
- **formula-box 覆盖率全站已 100%**：注入脚本 `extract_formula.py` + `inject_formula_generic.py`（幂等）；锚点 = 标准副标题 `<p>`，**已有 formula-box 的文件一律跳过**；无简单赋值的 calc 诚实 fallback，**绝不写伪公式**。

---

## 七、未完成任务清单

### 7.1 孤立未完成任务（按优先级）

> 跨分类 / 独立的系统性问题，可穿插推进。

**P0 — 已闭环**（原 `upload-pages-artifact` 隐藏文件修复：工作流已用 `@v3` + `include-hidden-files:true`，`.hidden` 文件不漏装）。

**P1 — 待办**

- **harness 输入桩能力现状（2026-09-24 定型，勿再重估）**：可注入手段共 **6 种** —— `inputs`（表单控件）、`checkIds`（`getElementById(id).checked`）、`radios`（`getElementsByName`）、`checks`（`querySelector('…:checked')`，**仅在「无 inputs」分支计入弱用例判定**）、`clicks`（页面作用域 direct eval，命中即 `via="click"`，配套动态 DOM 登记）、`dynDom`。**「纯 checkbox 量表页不可注入」的旧结论已失效**。逐批成果与逐例打法归档在 `.workbuddy/memory/2026-09-2*.md` 与 skill `toolbox-weakcase-hardening`，**本文件不再记录批次流水**。
- **仍未闭环的残留（转 P3 顺带，不单独成批）**：
  - ✅ **纯 checkbox 量表页已闭环（2026-09-26 核实）**：含 `checkbox` 页 353 个，有用例的 162 个**均带注入通道**、弱用例 0；另 191 个无任何用例 ⇒ 覆盖缺口，见 §7.4。
  - ✅ **fim-scale / gingival-index 已闭环**：两例均有真实 `inputs` + 独立复算 `ref`（fim 全填 7 ⇒ 运动分 13×7=91/91、独立率 100%；gingival t16 四位点 3 / BOP 1 ⇒ GI 12/24=0.50、BOP 1/6=16.67%→17%），默认态均失配。
  - ✅ **`womac` / `load-curve` 系失效引用，已删**：`tools/rehabilitation/` 下**不存在**这两个文件；`rehabilitation` 现有 18 例用例全部带注入通道。
- **`metalwork/tester-19` ≤1kV 耐压分支无法构造判别用例**：该分支输出恒为常数 `3.5 kV`（与 `ratedV` 取值无关），任何 `expect` 都会在**默认态**命中 → 必被判逃生项，故**刻意不补用例**；该修复（`0.0 kV → 3.5 kV`）只能靠隔离器人工跑 + 代码评审保真，回归时注意。
- **「多页签（mode）」页面的非默认页签分支无法被 harness 覆盖**：切页签必须带参调用 `setMode(1)`，而 harness 只无参调用候选函数 → 双样本 / 第二种模式分支永不执行，`expect` 只对默认页签有效。**复核口径**：复制页面到 `tools/<ind>/_tmp-xxx.html`，把 `let currentMode=0;` 改成 `1` → 隔离器单跑 → **立即删除副本**（勿留待提交）。
- **永久排除（不下架）**：同名异功能 `finance/salary-after-tax` ↔ `payroll-calculator`、`ophthalmology/self-assess-2` ↔ `osdi-scale`；跨行业同名编号页（`calc-N`/`rater-N` 等 17 个 basename）经内容哈希取证均为不同工具、内容各异，非重复，不处理。


**P2 — 低优先级**

- **指南英文副本（`guides/*.en.html` 100 篇）软隔离已办**：已配为孤儿文件（sitemap 排除 + hreflang/入口移除 + 索引 state 清理）。**文件保留至约 2026-10-21 再物理删除**（到期前勿动）。

### 7.2 分类收口待办清单（按 §4.1 维度）

> 完成一个分类从本节删一个。判定标准见 §4.1 / §4.5。
>
> **当前为空** —— 全站 209 分类已全部收口（2026-09-19 收官）。

### 7.3 C→A 质量提升专项（目标：A 级率 →75%）

> **判定口径**（`_build.py:1701-1744`）：A = `rich 且 own_len≥800` / `own_len≥6000` / `own_len≥3000 且 inputs≥3`。`rich` = canvas/data-viz 或 formula-box 正文 ≥`FORMULA_BOX_MIN_TEXT`(20) 字。
> **状态：目标已达成并超额** —— A 级率 70.0%→**99.2%**（4693/4729，build 口径）；bucket1（`own_len≥800 且非 rich`，补真实 formula-box）、bucket3 前置段（own_len 700-799 + 真实派生量）、缺陷 J/L/M 全部闭环。
> **明确排除（度量盲区，勿强改）**：`ai/ocr`、`ai/image-classification`（及同类 `ai/*`）逻辑写在 `<script type="module">` 中，而 `own_len` 正则只匹配**裸 `<script>`** → 永远够不到 800。属**度量口径盲区、非页面缺陷**，强行补裸脚本 = 代码膨胀凑数，**不做**。若日后需修正，应改 `_build.py` 的 `own_len` 正则纳入 `type="module"`（框架改动、须单独评估；全站仅 5 页命中）。
> **手法**：计算器补「真实公式说明面板」（含实际公式 + 一句说明，非代码膨胀）；非计算器补真实原理/参考表。
> **复用纪律**：动手前先做全站查重（`tools.json` name 归一化相似度 + 关键词），能存根就存根（成本远低于重做）；存根须留 `TOOLBOX-REDIRECT`（保 URL 零 404，canonical 指向真工具）。
> 逐批明细见 `.workbuddy/memory/2026-09-2*.md` 与全量快照归档。

---

### 7.4 verify 用例覆盖缺口（2026-09-26 全站核实，新线）


**核实结论（勿再重估）**：

- 全站含 `<input type="checkbox">` 的页面 **353** 个，其中**有用例的 162 个已全部带注入通道**，**无注入通道的弱用例 = 0** ⇒ 存量弱用例线与 checkbox 无关，`no_inputs` / `all_default` 的 14 例已全部定性。
- **但另有 191 个含 checkbox 的页面在全站任何 verify 文件中都没有用例**（`design/*` 11 页、`edu/*` 40 页、`biz/*` 文本类为主）。
- 判定口径注意：用例块的键名**常不带引号**（`slug: "x"` / `inputs: {}` / `checkIds: [...]`），扫描脚本必须写成 `"?slug"?\s*:\s*"([^"]+)"`，否则会大量误报「无用例 / 无注入通道」（本次两次误报均源于此）。

**处置**：属新线（补用例 ≠ 改弱用例），单独立批；须守 §8.1（expect 独立复算）。**已交付 160 例**（`design/*` 84 + `edu/*` 32 + `biz/*` 44，逐例锚点见各用例 `ref`）。剩余 **100** 页待补（`design/*` 45、`edu/*` 21、`biz/*` 34）。【按 `tools/**` 真实文件数重校】`design/image-resizer`（`generate()` 首行 `if(!origImg) return` + 依赖 canvas 解码）、`edu/exam-study-planner`（localStorage 桩只写不读 ⇒ 统计分子/分母不可达）**结构性不可注入，不硬写用例**。

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
- **隔离器报的 `err` 必须先过 jsdom 三态复核才能判定为缺陷**：隔离器是桩环境，`mermaid`/`PDFLib`/`pdfjsLib`/`AudioContext`/canvas `ctx.*`/动态 select 等缺桩会让**真机正常的页**报错。口径 = jsdom 加载真实 DOM → DEF / ZERO（输入全 0）/ EMPTY（输入全空）三态 → 读结果容器文本查 `NaN|Infinity`；**三态干净即判「桩盲区」并排除，不得据此改页**。
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
- **dry-run 命中 ≠ 存在缺陷：必须先过「jsdom 真机模拟 + 源码兜底核验」两道**（2026-09-23 实证，若不查会白改一批线上页）：全站 dry-run 报 **36 页** `WILL_INJECT`，逐页核验后**全部为静态误报**（真机无 NaN 路径）—— ① jsdom 加载页面后清空**全部**输入控件（number/text/textarea → `''`、select → `selectedIndex=-1`）再触发事件，36 页仅 3 页命中，而这 3 页 select **无空值选项且有默认选中项** ⇒ 真机用户无法构造该状态；② 源码兜底核验（如 `hvac/fresh-air-load` 的 `num()` 把 `isNaN` 转 `null`、`fmt()` 把 null/NaN 渲染为 `'--'`）。**判定结论固化在 `scripts/output_guard_exclude.txt`（v8 默认加载，dry-run 已归零）**。另：注入验证必须用「注入 → 跑 verify → 回退 → 再跑 verify」对比锁定归因 —— 本批 3 页（`dentistry/gingival-index`、`hvac/fresh-air-load`、`tcm-chemistry/response-factor`）一一对应为 **harness 桩盲区**（headless 无真实 DOM），**不是页面缺陷**。

---

## 九、发现但未修的真实缺陷（待老板定夺）

> **缺陷 A–U 已闭环归档**（根因/防复发进 §八，明细见 memory 2026-09-2*.md 与全量快照）。本节只留**未处理**项。

- **未处理（疑似口径）**：`legal/calc-8`（年终奖计税）把「社保/专项附加」按**年度值**扣除、未 ×12；若语义是「月缴」则应税所得高估、税额偏低。等老板确认语义。
- **未处理（非缺陷）**：`ai/ocr`、`ai/image-classification` 等 5 个 `<script type="module">` 页的 `own_len` 度量盲区（§7.3 结论：不改）。
- **未处理（字段错位真缺陷）**：`chinese/chinese-radical-lookup` 的 `DATA[c]` 实为 `[部首,部首名,总笔画,字形描述,拼音,本字]`，而 `query()` 错取 `d[3]` 当读音、`d[4]` 当字形 ⇒ 输出「读音：水流」「字形：hé（河）」。修法：① 改模板对调 d[3]/d[4]（1 处）；② 改 DATA 顺序（面大）。未改页面，等定夺。
- **站点级 `showToast(i18nText())` 显示 `undefined`（待定夺）**：`i18nText` 在 key 与 fallback 均空时 `return key` ⇒ `undefined`，`showToast` 写入 `textContent` 被 WebIDL 转字符串 `undefined`。全站 **3208 处 / 1073 页**（`copyText` 另 200 处）；空输入/复制失败分支弹 `undefined` 气泡（BATCH105 实测）。影响面大、属文案层，**未改**。建议（待拍板）：`showToast`/`copyText` 入口加「空/undefined 回落默认中文」兜底（改 `js/common.js` 1 处、页面零改动）；逐页补 `i18nText` 需改 1073 文件，不建议。

---

## 十、优先级与当前主线

> **主线 = 优化 `tools/**` 页面本身**。`scripts/` 验证脚本除门禁必需外不单独投入，只在优化分类时顺手改，不单独立批。

### 10.1 优先级总纲

| 级别 | 内容 | 状态 |
|---|---|---|
| **P0** | 页面级真实缺陷修复（§九 清单） | A–U 已闭环（含 96 小行业 687 页默认态 + 边界态精查）；**当前无进行中批次**，§九 仅余 `ai/*` 度量盲区（评估为不改） |
| **P1** | 按热度逐分类 §4.1 八项目标收口 | **全站 209 分类已收口**（§7.2 为空） |
| **P2** | ✅ 工具质量分级提升（C→A） | **已达成：A 级率 70.0% → 99.2%**（§7.3） |
| **P3** | `scripts/` 用例与基线维护（弱用例去默认化等） | **仅随 P0/P1 顺带处理**；门禁必需项（`run_gates.py` 链路）除外 |

### 10.2 现状（实测基线）

- `all_default 4 / no_inputs 10 / escape 0`；门禁 `run_gates.py` **216 项全过**、逃生项 0（判别器已检 **3252** 例 / 跳过 50）。
- A 级率 **99.2%**（A 4693 / B 32 / C 4）；术语内链 **1591 页 / 2268 条**（零死链、零自链）。
- 弱用例口径与选批规则见 §10.3。
  - **注意：弱用例整体处于判别器盲区** —— 「注入值等于默认值」的用例被判 `usable=false` 直接跳过（§10.5）⇒ `escape=0` 只说明强用例无逃生项；每批改造后须重跑判别器确认其由「跳过」转为「已检且变红」。

### 10.3 弱用例去默认化（仅在 P0/P1 顺带时执行）

**存量 14 例**（`no_inputs=10` / `all_default=4`）。**已全部有判死或注入结论并写进各用例 `ref`**（唯一源）：4 例 `all_default` 全判死；10 例 `no_inputs` 判死（判据 §10.5 B 组）。两处「顺序保持型筛选」翻案（`office/excel-formula-reference`、`gardening2/pruning-time`）均锚**过滤后跨条目相邻串**（§10.5 C.7④）。**转 P3 顺带，不单独成批**；逐批成果与逐例打法归档在 `.workbuddy/memory/2026-09-2*.md` 与 skill `toolbox-weakcase-hardening`，**本文件不再记录批次流水**。

**选批口径**：① 按「可注入数」降序挑批次；② **结构性不可注入的不要选**（判据 §10.5 B 组）—— 保留 `no_inputs` 并在 `ref` 写明理由；③ 每批 8–11 例，走 §10.4 六步。

**结构判死的唯一依据是各用例 `ref`**；旧清单里 19 条已被 `clicks`/`inputs` 翻案却仍标「勿重复评估」的条目（`music/sheet-music`、`dermatology/*`、`travel/aim-trainer` 等）已删除，免得后续批次跳过可行候选。

### 10.4 每批收口流程（顺带改造时六步，缺一不可）

1. 改写 `scripts/verify_<cat>_calc.js`（非默认输入 + Python 独立复算 expect）
2. 单跑 100% 通过 → `node scripts/discriminate_check.js verify_<cat>_calc.js` **0 逃生项**
3. 被「跳过」的用例（textarea / 动态 id `q0..qN`）必须**自建同口径探针**补验「注入 PASS + 回退默认 FAIL」
4. 更新 `scripts/falsepass_baseline.json` 与 `scripts/discriminate_baseline.json`（**只准降不准增**，按 selfcheck/discriminate 实测值同步）
5. `python3 scripts/run_gates.py`（全量 217 项）全过 → `git commit` + push、**单次**确认部署
6. 归档 `.workbuddy/memory/YYYY-MM-DD.md`（**批次玩法、逐例打法只写这里与 skill `toolbox-weakcase-hardening`，禁止写进本文件**；本文件只更新 §10.2 计数与 §10.3 清单），清理 `/tmp` 临时脚本

### 10.5 harness 已知限制（选批与定 expect 前必读）

> harness = `scripts/verify_it_calc.js`。**三阶段判定**：① 覆盖 `c.inputs` 后触发 `input/change/keyup` 并**立即**查 expect（命中即 `via:"input event"`，判定只看 `blob1`）→ ② `clicks` 注入（命中即 `via:"click"`）→ ③ 未命中才兜底**无参遍历调用各候选函数**（命中即 `via:<函数名>`；`DESTRUCTIVE` 正则跳过 `reset|clear|restore|save|swap|history|^set[A-Z]`）。
> `collectStrings(elements)` 对每个元素收集 `value`/`innerHTML`/`textContent` 三路非空串，剥标签压缩后**换行拼成单个字符串** ⇒ `blob.includes(want)` 是**子串**匹配；**不采集 `style`**。

**A. 可注入手段（6 种）**

| 手段 | 用法与判据 |
|---|---|
| `inputs` | 表单控件注入；**仅对静态 HTML 内已有 id 的控件有效**（运行期 `innerHTML` 生成的控件无效，见 B1） |
| `checkIds: ["c","u"]` | `getElementById(id).checked` 型（纯复选框量表页） |
| `radios: { htn: "1" }` | `getElementsByName(name)` 型 |
| `checks: ["3"]` | `querySelector('input[name=x]:checked')` 的返回值，即「哪一项被选中」；**仅在「无 inputs」分支计入 `no_inputs` 判定，不参与 `all_default`**（它可能只是 inputs 的修饰项） |
| `clicks: ["pick(0,3)", …]` | **页面作用域 direct eval**，在 inputs 注入后、兜底前按序执行，命中即 `via="click"`；配套**用例级动态 DOM 登记**（`innerHTML` setter 按容器 id 分桶解析 `{tag,id,class}`，同容器以最后一次渲染为准）—— 以 `DYN.on` 开关隔离，仅当用例声明 `clicks`/`dynDom` 时启用，其余用例逐字节不变 |
| `dynDom` | 单独开启动态 DOM 登记（不注入值时用） |

> `clicks` 内的状态驱动优先级：**页面顶层 `var`/`let` 绑定直接赋值 > 模拟点按钮 > 注入 DOM 选中态**（真正被 `calc()` 读取的往往是顶层状态，`grade`/`scores`/`sel`/`reviewData`/`materials`；`let` 声明的顶层数组同样可直接改元素）。**带 DOM 形参的 click 函数不算不可注入**：`selectFluor(btn,i)` / `selectStage(grade,el)` 的 `btn`/`el` 只做 `classList` 增删 ⇒ 传哑对象 `{classList:{add:function(){},remove:function(){}}}`、或直接省略（页面内 `if(el)` 判空）；内层 `querySelectorAll('.xxx').forEach` 对空数组安全。

**B. 「能不能注入」判据（静态 HTML `grep -cE '<input|<select|<textarea'` 为 0 时逐条排查）**

| 判据 | 结论 |
|---|---|
| B1 控件由运行期 `innerHTML` 生成（id 形如 `d{di}i{ii}`、`spot{i}`、`c{i}`），或**静态 `<select>` 存在但 option 由 JS 填充** | 前者写 `inputs` 会被判 `usable=false` 静默 `skip`；后者判别器取默认空串、回退 `+''=0` 落首项。两者都用 `clicks` 赋值后**显式**调 `calc()`/`compare()`（这类 select 常无 `onchange`）。**副产品**：这些键不进弱用例清单，正好靠 `clicks` 计入可检 |
| B2 驱动语句是 class 选择器（`querySelectorAll('.'+cls)` / `'.s8'`） | 桩的 `querySelectorAll` **仅对选择器串含 `checked`** 的调用返回 `c.checks`，纯 class 选择器恒返回 `[]` ⇒ 复选框注入不了，保留 `no_inputs` |
| B3 行由 `createElement + #rows.appendChild` 建立，靠 `querySelectorAll('#容器 .行类名')` 取值 | 桩的 `dynRecord` 只登记 `innerHTML` 字符串里解析出的标签、**不含容器 div 自身** ⇒ 选择器恒空 ⇒ 结构性不可注入（容器 `innerHTML` 里仍能看到全部表单标签，**极易误判为「行已建好」**） |
| B4 控件位于默认 `display:none` 的 hidden / tab 面板 | **注入阶段与 `calc()` 阶段不是同一份 DOM 实例** ⇒ `inputs` 与 `clicks` 内赋值**都改不动** `calc()` 读到的值（`hvac/duct-calculator` 的 `diaD`）；只能锚由已验证可注入字段派生的量 |
| B5 有 id 的控件注入后输出**逐字不变** | 该控件的处理函数不在 harness 实际调用链上（仅 `saveList()` 写 localStorage 时用到）⇒ 输出无关，保留 `no_inputs` 并写明 `ref` |
| B6 纯浏览页：无 `#result`、交互仅 `classList.toggle`（不进 blob）/ 写剪贴板 | 不存在任何随输入变化的输出 ⇒ 结构性不可注入 |
| B7 需点按钮写 localStorage、写操作对渲染零影响的页 | 同 B6（`setLastClean` 类还被 `DESTRUCTIVE` 的 `^set[A-Z]` 排除）。**例外**：若数据**读取**走 `localStorage.getItem`，可在 `clicks` 内覆写它注入数据（等价于「用户本就有数据」），已验证可行 |
| B8 `confirm`/`prompt` 做闸门 | harness 无 `confirm` 桩 ⇒ 未填满时 `calcScore()` 抛错被兜底 catch、结果区恒空。须在 `clicks` 里预置状态绕开闸门（如把全部题目填 5） |
| B9 `.length` 判空但入参是对象 | `render()` 写 `if(!list.length)`、而 `list` 是对象 ⇒ 恒真 ⇒ **整页功能恒定不工作**（`travel/travel-adapter-guide` 的搜索恒显示「未找到」）⇒ 属 **P0 真缺陷**，改 `if(!list\|\|!Object.keys(list).length)`。**遇「整页功能恒定不工作」先怀疑判空/类型错，别急着归类为「不可注入」** |

**C. 定 expect 的硬规则**

1. **锚点只依赖被测点且形态安全**：禁混入表头 / info-box 常驻文案 / 按钮文本 / 页脚免责 / 静态 SVG 文本 / 下拉 option value 等**页面常量**。`blob.includes` 是**子串**匹配 ⇒ `达标` ⊂ `未达标`，否定式结论词须锚**完整结论串**；数值须与标签绑成连续串（`18.75 最大弯矩 M (kN·m)`），否则裸数值会被明细大表 / 兜底模板命中；含 `<` 的输出会被标签剥离吞掉。
2. **双态核验 + 默认态逐串比对**：dump 注入态与默认态逐串比对，**只有「注入态有、默认态无」的串能进 expect**（防同值巧合；兜底会无参调用 `genPassword` / `loadDefault` 产出另一套结果 ⇒ 锚可能与其**同串或成子串**，如「23 总物料数」含「3 总物料数」）。`inputs` 逐字等于页面默认值 ⇒ 判别器判 `usable=false` 直接 `skipped++` ⇒ **凡 `all_default` 例一律视为零判别力、须重写**；零影响键不要写进 `inputs`（会造成「看似非默认」的假象）。
3. **兜底污染三则**：① 兜底无参调用候选函数会**改状态后重算**、把结果区重写成另一套值 ⇒ expect 避开任何无参函数能产出的串；② `clicks` 型 expect 必须在阶段 ② 命中，否则 **`FAIL` 的 `fullBlob` 是「兜底后」视图**（与默认态逐字相同）⇒ 不能据此判断 clicks 是否生效；③ **expect 出现 `undefined` / `NaN` 字面量几乎必是兜底产物**（无参 `selectDate()` → `undefined-NaN-undefined`）⇒ 先辨段再改锚。
4. **锚点优先级 + checkbox 反向利用**：① 非兜底分支独有的文案（`if/else` 的**非 else** 路）；② 只由注入值派生、兜底无法复现的数值；③ 跨档 / 跨分支的等级词（改前先手算是否落同档）。桩内 checkbox 恒未勾 ⇒ 默认态渲染「xx缺失」并给低分 ⇒ **勾满 `checkIds` 抢「全部达标」分支做正向强锚**。
5. **数值合法性与齐次量**：有界量（决定系数 / 概率 / p 值 / 覆盖率 / 率）越界即公式错，交付前必查 `[0,1]`；「基础分 − 扣分」式先算最小值是否越界；**凡输出物理不可能值必查公式本身**。比值 / 密度 / 单价 / 覆盖率换值前先确认不是等比缩放，改完须实测输出是否跟着变。
6. **日期与随机**：日期相关量一律不锚（随运行日漂移）；禁 `Math.random` / `Date.now` 当输入。`clicks` 内改**进程级全局对象**（`Math` / `Date` / `Array.prototype`）**必须用完即恢复**（`var __r=Math.random;Math.random=fn;gen();Math.random=__r`），否则污染同进程后续用例的默认态 —— 只有双态核验能抓到。钉死随机值后锚「多列连续复合串」把巧合概率压到 10⁻⁶。
7. **默认态已全量渲染的页面，锚点要换区**：① 同引擎多段渲染（注入段 + 兜底 `loadSample()` 段）共用常量串 ⇒ 只锚注入段独有串；示例文本即逃生项，注入数据须与样本用词错开。② 「kw 空输出全量」型过滤页 ⇒ 反向注入**不存在的关键词**、锚「未找到匹配项」类空结果提示。③ 「卡片 + 详情」双区页 ⇒ 只锚详情区独有文案。④ **筛选型图鉴页（默认渲染全表）**⇒ 只锚**过滤态成立的跨行相邻串**（`office/excel-formula-reference`：注入「数字」⇒ 命中 SUM/AVERAGE/TEXT，AVERAGE 与 TEXT 过滤态紧邻、全表却隔 6 项）。**锚不得取「整条目渲染串」**（默认全量里本就连续）。**入口筛选函数常有「状态变量 + 按钮」双参签名，直调 `setFilter(f,btn)` 会 btn 为 undefined 抛错 ⇒ 绕过它、只改状态变量再重渲**（`gardening2/pruning-time`：`currentFilter='before';render();`）。
8. **注入与格式口径**：`select` 的 `selected` 属性在桩里不生效 ⇒ 默认选中项必须**显式注入**（`selfcheck` 取 JS 设定的真实默认、`discriminate_check` 取首个 option，口径不同）。`inputs` 键若是模板串残留（`${f}` / `pri${i}`）会同时骗过两把锁（不进棘轮 + 记「正确变红」）⇒ 巡检 `verify_*_calc.js` 里形如 `${` 的键。`fmt()` 走 `toLocaleString()` 默认截 3 位小数 ⇒ 定 expect 避开被截断处。
9. **clicks 锚「不读输入的全量函数」必误判逃生项**：判别器模拟注入失败是**清空 clicks 后跑**（含兜底遍历）。若 expect 锚 `checkAll()` 类「不读输入、恒产全量」输出（如 `36/36`），兜底重调仍同值 ⇒ 判「仍 PASS」= 逃生项 ✅ 改用**具体输入态**（`toggleItem(0,0/0,1/0,2)` 勾 N 项 → `N/总数`），默认态 0 项不命中。
10. **空结果提示不可锚两形态**：① 提示同时被兜底链复现（`selectXxx()` 无参置全局态 `undefined` ⇒ 过滤集恒空、渲同一提示）⇒ 注入态与失败态同串，判逃生项。② 提示在**独立静态元素**内、仅 `style.display` 切换 ⇒ 不写入结果容器 ⇒ blob 永不含该串。✅ 定锚前用探针双态 dump 比对，只取「注入态有 / 默认态无且兜底不复现」的串。
11. **「名 + 参数」型 option 文本是逃生项**：`<select>` 的 `option.textContent` 会进 `collectStrings` ⇒ `东京（日本）UTC+9` 这类串在**默认态 select 里本就存在** ✅ 只锚**随注入值变化的派生量**。「写 localStorage 再读回」链路在 harness 下**只写不读**（`getItem` 缺失 ⇒ `getTasks()` 恒 `[]`）**不可注入**（`edu/exam-study-planner`）。
12. **调试陷阱（会把「没生效」误判成 bug）**：① `verify_it_calc.js` **必须留在 `scripts/` 下**跑 —— `TOOLS_DIR` 取自 `__dirname`，拷到仓库外会整页返「文件不存在」且 `errs=[]`（看似「clicks 静默失败」）；要插日志就在 `scripts/` 下临时副本改完删。② 确认 clicks 是否真执行：用 `clicks:["throw new Error('RAN')"]`，`errs` 出现 `RAN` 即已执行（比 DOM 探针可靠）。③ 带连字符的 id 在用例对象里**必须加引号**（`{ "focus-mins": "50" }`），裸写 `focus-mins:` 直接 SyntaxError。
13. **「textarea + 预览区」双元页（Markdown / 富文本类）**：blob 同时含**注入原文回显**（textarea 的 `value`）与**渲染产物** ⇒「渲染产物文本 ⊂ 注入原文」的锚（`<strong>bold</strong>` 剥标签后的 `bold`、`# H1` 剥标签后的 `H1`）**测不到渲染**，属伪锚。✅ 只锚**渲染独有的连排串**：剥标签后**标签被换成空格**，同元素内相邻 cell 连成 `甲 乙 24 36 81 90`，而原文 `| 甲 | 乙 |` 里 `甲 乙 24` 并不连续 ⇒ 天然非回显。**expect 也不能写 `<strong>…</strong>` / `<h2>…</h2>` 这类带标签形式**（写了必 FAIL，易误读成「渲染没生效」，实为锚错）。
15. **多行 textarea 的产出串，换行在 blob 里被归一成空格 ⇒ 锚要写 `bbb aaa ccc`，不能写 `bbb\naaa`**（首版按 `\n` 写必 FAIL，极易误读成「去重没生效」）。✅ 排序/去重类工具一律锚**整段连排**（`fig pear apple`）；**单字符或极短锚（`c`）在默认态示例行里本就存在 ⇒ 逃生项**，定锚前先 dump 默认态。凡「换个方向再跑一遍」能给出反向串的（`length-asc`→`length-desc`），两个方向都写进同一用例的 `expect`，可防「排序根本没生效」的假通过。
16. **「输入 textarea + 结果区」提取器类（正则抽邮箱 / URL / 日期一类）：输入回显与提取结果并存**
⇒ 直接锚被提取内容（`a1@toolbox.com`）测的是**回显**，清空注入后仍从 textarea 命中 ⇒ 伪锚 ✅ 锚落在**结果区独有的形态**：`text-extract-emails` 每封邮箱后跟「复制」按钮 ⇒ 锚「邮箱 + 空格 + 复制」；`text-extract-urls` 锚两段 URL 连排，原文用「与」隔开使之不连续。另 `text-split` 的「序号+段内容」锚（`3 cherry`）默认态示例里本就有 ⇒ 改用段数标签「（共 3 段）」。 （补）这类页常由 n 个 checkbox 决定抽不抽，**缺 `checkIds` 时 `extract()` 在首个 `getElementById(x).checked` 处抛错中断** ⇒ 结果区恒为初始值，画面与「无匹配」**完全一致**，极易误判成「页无功能」⇒ **注入后结果区逐字不变就先怀疑它**，须声明全部默认勾选项（`biz/text-extract-numbers`/`dates` 同形）

**D. 工具与方法**

| 工具 | 用途 |
|---|---|
| **常驻 runner（scan / dump / multi）** | `~/.workbuddy/skills/toolbox-weakcase-hardening/assets/weakcase_runner.js`（cwd 为仓库根），**每批直接调用、不要重建**。`clicks` 末尾回写结果到 `__p`（兜底不碰）⇒ FAIL 时仍读到真实注入输出；容器 id 不在内置清单时用 `dumpIds` 覆盖。|
| **标记串探针** | 判断写入路径是否通：`clicks:["getElementById('stats').value='MARK_V'"]` + `expect:["MARK_V"]`（命中即通），区分「clicks 未生效」与「锚点错」 |
| **「双态」核验** | 每例必须**注入态 PASS + 默认态（剥 inputs/checks/clicks）FAIL** 双跑；判别器取不到默认值的页尤其只能靠它 |
| **逐项二分** | 定位逃生项用「逐项单独 `runCase`」，**禁用 `fullBlob.includes()` 判定**（blob 元素集合不同，会全判「无逃生」） |
| **批量改用例** | 能用精确 `Edit` 就别用正则替换器（全数组重建会吃掉被改块的块前注释、normalize 块间空行）。`verify_*_calc.js` 有**带引号键**（`"slug":`）与**无引号键**（`slug:`）两种风格，换文件前先 `grep -c '"slug":'` 探格式 |
| **页面真缺陷精查** | 见 §8.7（隔离器 `scripts/_audit_iso_small.js` + jsdom 三态复核）与 §8.11（输出守卫 v8） |

**E. 待办 / 历史残留**

- 全站 `verify_*_calc.js` 共 **62 条「同 slug 多份」重复条目**（`realestate` 12、`math` 14…，其中 61 条内容不同）：门禁把同页跑两遍、计数虚高，按 slug 的批量替换器会**同时改掉两份**。**暂不清理**（删条目须同步改三个基线数，属独立批次）。
- `selfcheck_false_pass.js` 全站 `--exec` 会崩（某页脚本污染全局 `process`）：**取基线请用结构模式** `node scripts/selfcheck_false_pass.js scripts`（与门禁同口径）。

### 10.6 方向1：公式-脚本一致性精查（**全量闭环** · 老板选定）

- **目标**：逐页独立复算计算类页 `calc()` 输出的数学/物理正确性（与标准公式/权威向量比），找"用户拿到错钱数/错物理量"的真缺陷（§4.5 红线第一条最高频事故）。
- **覆盖（已全量闭环）**：10 高热度行业 + 金融周边集群 ~334 页 + 中低热度 113 个行业（页≥15）+ 96 个小行业（687 页）的默认态与 ZERO/EMPTY 边界态；边界 NaN 守卫已铺开。
- **工具（均在本地，`_*.js` 按 `.gitignore` 不入库）**：
  - `scripts/_audit_iso_small.js` —— 批量隔离器。`node 脚本 <industry,...>`；`DUMP=1` 另写 `/tmp/iso_small.json`。**不要用「函数名必须含 calc」的窄口径过滤入口**（会漏掉 `compare()`/`update()` 类页，687 页里因此漏审 168 页）；桩需覆盖 `MutationObserver`/`getElementsByName`/`style.setProperty`/`cloneNode`/`toBlob`/`window.X=` 透传 globalThis/`<select>`+`<option>` 注册。
  - `/tmp/jsdom_probe.cjs` —— jsdom 真实 DOM 复核探针，对候选页跑 DEF/ZERO/EMPTY 三态。**判据：隔离器报的 `err` 一律先过 jsdom 复核，无 NaN/Infinity ⇒ 桩盲区，立排除、不改页。**
- **SOP**：① 隔离器扫 DEF 态 → 筛 `NaN`/`Infinity`/越界值/`err`；② 每条 `err` 过 jsdom 三态复核，区分「桩盲区」与「真缺陷」；③ 确凿缺陷才改页，改完补/改用例。
- **纪律**：确凿真缺陷前不改页面；找到即立项闭环（修 calc + 修/注册 verify 用例 + run_gates + 提交推送）。

