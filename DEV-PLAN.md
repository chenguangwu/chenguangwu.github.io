# DEV-PLAN.md — 待处理任务清单

> **本文件只放「待处理任务」与「干活必须遵守的规则」。已完成项、批次成果、历史操作流水一律不写入** —— 归档走 `.workbuddy/memory/YYYY-MM-DD.md`；历史全量快照另存 `.workbuddy/memory/archive-devplan-full-2026-09-23.md`。
> **收尾口径（老板 2026-09-21 明确）**：闭环 = 本地 build / 门禁通过 + GitHub 部署成功（Actions run success）。**不做线上产物 MD5 落盘比对、不 sleep、不轮询 API**；纯文档类改动（`*.md`、memory）不等部署。
> **状态（2026-09-23）**：全站 209 分类 §4.1 八项目标已收口；A 级率 **99.2%**（4693/4729，build 口径）；SEO（title / desc / h1 / JSON-LD）维度已治理；§4.1.7 专业名词**站内内链**已落地（1591 页 / 2268 条，见 §六）；96 个小行业（687 页）默认态 + 边界态精查**已闭环**（见 §10.6 方向1）。**当前无进行中批次，待办见 §九。**

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
- **仓库体积（`.git`）维护**：大构建批次会把数千页快照写进 pack，**多轮大提交后 pack 会严重碎片化**。2026-09-23 实测：`.git` 达 **860M**（29 个 pack / 716M + 103M 松散对象），逼近 GitHub Pages **1GB 软上限** → 跑 `git repack -a -d`（合并全 pack，**不 prune 任何不可达对象**）+ `git prune-packed` 后降至 **662M**（1 pack / 508M），27 秒完成、**零工作区影响、可随时重跑**。**冒烟阈值：`du -sh .git` > 800M 即应 repack**。另注：仓库还有约 103M **不可达对象**（4 commit + 9537 blob + 225 tree），经查全是 `git stash` 残留（`On master:` / `WIP on master:` / `index on master:` 类提交），内容抽查确认已落 HEAD；清理须 `git prune`（**不可恢复 → 须老板拍板**，Agent 只报数据不做）。
- **同一逻辑在多个分类重复实现时，抽通用脚本而非复制**：新分类开工前先 `ls scripts/` 查是否有可加 `--industry` 的现成脚本（老板明确偏好复用而非复制）。
- **formula-box 覆盖率全站已 100%**：注入脚本 `extract_formula.py` + `inject_formula_generic.py`（幂等）；锚点 = 标准副标题 `<p>`，**已有 formula-box 的文件一律跳过**；无简单赋值的 calc 诚实 fallback，**绝不写伪公式**。

---

## 七、未完成任务清单

### 7.1 孤立未完成任务（按优先级）

> 跨分类 / 独立的系统性问题，可穿插推进。

**P0 — 已闭环**（原 `upload-pages-artifact` 隐藏文件修复：工作流已用 `@v3` + `include-hidden-files:true`，`.hidden` 文件不漏装）。

**P1 — 待办**

- **harness 输入桩覆盖现状（2026-09-24 更新）**：
  - ✅ **复选框 / 单选组已可注入**（本日闭环）：harness 新增 `checkIds: ["c","u"]`（`getElementById(id).checked` 型，纯复选框量表页）与 `radios: { htn: "1" }`（`getElementsByName` 型）两个注入字段；`optical/progressive-corridor` 那类 `querySelector('input[name=x]:checked')` 用既有 `c.checks` 即可。**三者合起来使「纯 checkbox 量表页不可注入」的旧结论失效** —— 全站 26 例此类弱用例不再属结构性 `no_inputs`（已改 5 例示范：`curb65` / `stop-bang` / `wells-pe` / `has-bled` / `rater-33`，剩余按 P3 顺带推进）。配套：`selfcheck_false_pass.js` 与 `discriminate_check.js` 均已识别这两个字段（判别器做法 = 清空注入模拟失败，用例必须变红）。
  - ⚠️ **`innerHTML=` 动态生成的控件仍未覆盖**（`fim-scale`/`womac`/`gingival-index`/`load-curve` 等，静态 HTML `grep id=` 为 0）→ 取不到值，按旧纪律「盲区先排除、再回源码复核」。**2026-09-23 实测教训**：对它在正式门禁实施「`innerHTML` setter 解析 `id=` 注册桩元素」会使全量门禁暴露 `psychology/calc-12` 崩溃（该页用 `innerHTML` 渲染滑块，`getElementById` 读到空桩后读 `.length`/`.trim` 即崩）——harness 缺「真实 DOM 行为」模拟，单点 `id` 注册会误伤**所有用 innerHTML 渲染 UI 的页**。已还原。须走「innerHTML 真实 DOM 模拟」专项。
  - ✅ **HTML 默认选中态已生效**（本日闭环）：`querySelector(':checked')` / `querySelectorAll('…checked')` / `getElementsByName(name)` 在**用例未声明 `c.checks`/`c.radios` 时回落到页面的 `checked` 属性**（预解析 name→全部带 checked 的 value；无 name 控件按 `#id` 归组）。收益：`optical/progressive-corridor`（`querySelector('input[name=design]:checked').value`）由抛 TypeError 恢复为可验证（真机默认 `standard`）。**副作用已逐一核实**：全量 3091 条可执行用例扫描**仅 `cardiology/aortic-dissection` 一例失配** —— 其原 expect「非复杂型Stanford B型」本就建立在旧失真上（该页 `extent` 组真机默认 `ascDesc` = A 型，旧桩 `getRadio` 抛 0 才落入 B 型），已重写为显式 `radios{extent:"descOnly"}` + `checkIds:["malPerf"]` → 紧急 TEVAR。**纪律**：新用例优先**显式声明**输入，不要依赖默认选中态。
  - ✅ **兜底调用排除集已补 `^set[A-Z]`**（本日闭环，原缺陷 B）：`DESTRUCTIVE` 正则原只拦 `reset|clear|restore|save|swap|history`，零参 `setXxx()` 会**先改写页面状态再重算**，使一批用例的 expect 实由兜底产出、与注入无关（真逃生项）。补齐后 7 个脚本 11 例失配，全部重写（明细见 §九 缺陷 B）。**残留**：`selectSize`/`setPet` 这类「名含 set 但不以 `set[A-Z]` 开头」的设值函数仍不被拦 —— 定 expect 时必须自行核算「零参调用全部设值函数后的最终态值」并避开（见 §10.5）。
- **`metalwork/tester-19` ≤1kV 耐压分支无法构造判别用例**：该分支输出恒为常数 `3.5 kV`（与 `ratedV` 取值无关），任何 `expect` 都会在**默认态**命中 → 必被判逃生项，故**刻意不补用例**；该修复（`0.0 kV → 3.5 kV`）只能靠隔离器人工跑 + 代码评审保真，回归时注意。
- **「多页签（mode）」页面的非默认页签分支无法被 harness 覆盖**：切页签必须带参调用 `setMode(1)`，而 harness 只无参调用候选函数 → 双样本/第二种模式分支永不执行，`expect` 只对默认页签有效。**复核口径**：复制页面到 `tools/<ind>/_tmp-xxx.html`，把 `let currentMode=0;` 改成 `1` → 隔离器单跑 → **立即删除副本**（勿留待提交）。
- **永久排除（不下架）**：同名异功能 `finance/salary-after-tax`↔`payroll-calculator`、`ophthalmology/self-assess-2`↔`osdi-scale`；跨行业同名编号页（calc-N/rater-N 等 17 个 basename）经内容哈希取证均为不同工具、内容各异，非重复，不处理。

**P2 — 低优先级**

- **指南英文副本（`guides/*.en.html` 100 篇）软隔离已办**：已配为孤儿文件（sitemap 排除 + hreflang/入口移除 + 索引 state 清理）。**文件保留至约 2026-10-21 再物理删除**（到期前勿动）。

### 7.2 分类收口待办清单（按 §4.1 维度）

> 完成一个分类从本节删一个。判定标准见 §4.1 / §4.5。
>
> **当前为空** —— 全站 209 分类已全部收口（2026-09-19 收官）。

### 7.3 C→A 质量提升专项（目标：A 级率 →75%）

> **判定口径**（`_build.py:1701-1744`）：A = `rich 且 own_len≥800` / `own_len≥6000` / `own_len≥3000 且 inputs≥3`。`rich` = canvas/data-viz 或 formula-box 正文 ≥`FORMULA_BOX_MIN_TEXT`(20) 字。
> **状态：目标已达成并超额** —— A 级率 70.0%→**99.2%**（4693/4729，build 口径；更早记录的「96.9%」为陈旧基线，未随 BATCH43–62 同步）；bucket1（`own_len≥800 且非 rich`，补真实 formula-box）、bucket3 前置段（own_len 700-799 + 真实派生量）、缺陷 J/L/M 全部闭环。
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
- **隔离器报的 `err` 必须先过 jsdom 三态复核才能判定为缺陷**（2026-09-23 新增）：隔离器是桩环境，`mermaid`/`PDFLib`/`pdfjsLib`/`AudioContext`/canvas `ctx.*`/动态 select 等缺桩会让**真机正常的页**报错。口径 = jsdom 加载真实 DOM → DEF / ZERO（输入全 0）/ EMPTY（输入全空）三态 → 读结果容器文本查 `NaN|Infinity`；**三态干净即判「桩盲区」并排除，不得据此改页**（本批 31 条 `err` 经复核 0 条真缺陷）。
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

> **已闭环的缺陷 A / B / C / D / E / G / I / J / K / L / M / N / O / P / Q / R / S / T / U 均已修复并归档** —— 根因与防复发铁律已提炼进 §八，逐批明细见 `.workbuddy/memory/2026-09-2*.md` 与全量快照归档。本节只留**仍未处理**的项。

- **缺陷 B 已闭环（2026-09-24）**：`scripts/verify_it_calc.js` 兜底阶段的 `DESTRUCTIVE` 正则已补 `^set[A-Z]`（原只拦 `reset|clear|restore|save|swap|history`）。原「评估结论 = 不修」被实证推翻：零参 `setXxx()`（如 `sheet-music` 的 `setKey()`、`pets/kennel-space` 的 `selectSize()`、过滤页的 `setType()`）会**先改写页面状态再重算**，而 `set[A-Z]` 前缀**不在**原正则覆盖内 ⇒ 相当一批用例的 expect 实际由该兜底调用产出、与注入值无关（真逃生项，且因「模拟注入失败后该串消失」而骗过 `discriminate_check`）。补充后全站 7 个脚本 11 例失配，逐例定性并全部按 §10.4 流程重写：4 例「过滤页假用例」（gardening×3 + tcm-chemistry，靠零参 `setType()` 改写筛选条件产出「未找到…」）、4 例「expect 已漂移」（pets×3 + hotel，断言的是旧版页面输出）、2 例真假用例（music/sheet-music、misc/statistics-distribution）、1 例真回归（ophthalmology/visual-acuity-converter，expect「0.0)」只是 type 输入提示文案）。修补后逃生项仍 0。`del*` 类未扩展（本次全站无由此产出的逃生项，按「只加有实证的项」原则不预扩）。**新增铁律**：见 §八「零参 `setXxx()` 兜底会产出 expect」与 §10.5 对应行。
- **未处理（待定夺，非缺陷）**：`ai/ocr`、`ai/image-classification` 等 5 个 `<script type="module">` 页的 `own_len` 度量盲区（§7.3 已给结论：不改）。

---

## 十、优先级与当前主线

> **主线 = 优化工具页面本身（`tools/**`）。** `scripts/` 下多数验证脚本是历史遗留，**除门禁必需外不单独投入**；只在优化某分类、确实碰到该分类用例时**顺手改**，不单独立批次、不为改脚本而改脚本。

### 10.1 优先级总纲

| 级别 | 内容 | 状态 |
|---|---|---|
| **P0** | 页面级真实缺陷修复（§九 清单） | A–U 已闭环（含 96 小行业 687 页默认态 + 边界态精查）；**当前无进行中批次**，§九 仅余 `ai/*` 度量盲区（评估为不改） |
| **P1** | 按热度逐分类 §4.1 八项目标收口 | **全站 209 分类已收口**（§7.2 为空） |
| **P2** | ✅ 工具质量分级提升（C→A） | **已达成：A 级率 70.0% → 96.9%**（§7.3） |
| **P3** | `scripts/` 用例与基线维护（弱用例去默认化等） | **仅随 P0/P1 顺带处理**；门禁必需项（`run_gates.py` 链路）除外 |

### 10.2 现状（实测基线）

- `all_default 128 / no_inputs 174 / escape 0`；`checked=3161`；门禁 `run_gates.py` **217 项全过**、逃生项 0（判别器已检 **2828** 例 / 跳过 333）。
- A 级率 **99.2%**（A 4693 / B 32 / C 4，共 4729）；deep-dive 术语内链 **1591 页 / 2268 条 / 唯一目标 630**（零死链、零自链、单页 ≤6 条）。**注：内链不影响质量分级**（`own_len` 只统计 `<script>` 内容）。
- 存量弱用例 **302 例**（`no_inputs=174` / `all_default=128`），**转 P3 顺带**，不单独成批。
  - **注意：弱用例整体处于判别器盲区** —— `discriminate_check` 对「注入值本就等于默认值」的用例判 `usable=false` ⇒ **直接跳过**（§10.5）。故 `escape=0` 只说明「强用例无逃生项」，弱用例的逃生项从未被检查；每批改造弱用例后必须重跑判别器确认其由「跳过」转为「已检且变红」。

### 10.3 弱用例去默认化（仅在 P0/P1 顺带时执行）

**存量 302 例**（`no_inputs=174` / `all_default=128`，selfcheck 口径；含 textarea/动态 id/结构性不可注入的「skip」类全站 333）。

**选批预筛清单（2026-09-24 实测 · 弱例数 / 其中可注入数）** —— 按「可注入数」降序挑批次，**不可注入的不要选**（页面静态 HTML 里 `grep 'id='` 为 0，控件由 innerHTML 动态生成，属 §7.1 保留项）：

language 6/5、aquaculture 5/5、bridge 5/5、glass 5/5、life 5/5、manufacturing 5/5、maritime 5/5、medical2 5/5。

**不可注入（结构性，勿选）**：`psychiatry` 24 例里 **18 例**页面只有 `id="quiz"` + innerHTML 渲染（`gad7`/`phq9`/`pcl5`/`mdq`/`asrs`/`cage`/`isi`/`ybocs`/`bis11`/`cdrisc`/`lsas`/`panss`/`pdss`/`phq15`/`eat26`/`cssrs`/`aq`/`les`），`tcm-diagnosis` 14 例同类；`chemical` 6 例、`mining` 9 例已于 2026-09-24 清零（chemical 判别力「已检 10 / 全数变红」，`checker-15` 因 id 由 JS 模板拼接被判跳过、已自建探针补验；mining 判别力「已检 11 / 全数变红」，`estimate-reserve` 属结构性不可注入 —— 块段由 `addBlock()` 按钮 + class 选择器动态生成，静态 HTML 无带 id 控件）；`engineering`、`signal`、`design`、`gas`、`mechanical` 已于 2026-09-24 清零（判别力分别由「已检 0 / 跳过 14」→「已检 14」、「已检 13 / 跳过 11」→「已检 24」、「已检 5 / 跳过 9」→「已检 14」、「已检 2 / 跳过 9」→「已检 11」、「已检 5 / 跳过 8」→「已检 12」，均为全数变红）；`cleaning` 同日改掉 6 例（判别力「已检 5 / 全数变红」），**残留 1 例** `appliance-cycle` 属结构性不可注入（见 §10.5 三类形态）；`finance` 同日 7 例清零（判别力「已检 21 / 全数变红」）；`sports` 同日 7 例清零（判别力「已检 29 / 全数变红」）；`dermatology` 同日 12 例改掉 9 例（判别力「已检 20 / 全数变红」），**残留 3 例** `contact-dermatitis-patch`/`miliaria-classification`/`wood-lamp` 属结构性不可注入（三页 `input/select/textarea` 计数为 0，交互全靠 JS 模板生成的按钮 onclick，见 §10.5）；`travel` 同日 9 例改掉 6 例（判别力「已检 17 / 全数变红」）并**顺带修掉 1 个 P0 页面缺陷**（`travel-adapter-guide` 的 `render()` 对对象用 `.length` 判空 ⇒ 整页搜索恒显示「未找到」，见 §10.5），**残留 3 例** `aim-trainer`/`emergency-phrasebook`/`packing-list` 属结构性不可注入；`endocrinology` 同日 21 例里改掉 7 例（判别力「已检 19 / 全数变红」），**残留 1 例** `ti-rads`（0 表单控件）；`fire` 同日 11 例里改掉 6 例（判别力「已检 10 / 全数变红」），**残留 1 例** `response-drill`（场景随机、按钮驱动）；`rheumatology` 同日 25 例里改掉 5 例（判别力「已检 20 / 全数变红」），**残留 2 例** `bvas`/`sledai` 属结构性不可注入（按 class 选择器 `.g1/.g2`、`.s8/.s4/.s2/.s1` 读取无 id 复选框，harness 的 `querySelectorAll` 仅对含 `checked` 的选择器返回注入项，纯 class 选择器恒返回空数组）。

### 10.4 每批收口流程（顺带改造时六步，缺一不可）

1. 改写 `scripts/verify_<cat>_calc.js`（非默认输入 + Python 独立复算 expect）
2. 单跑 100% 通过 → `node scripts/discriminate_check.js verify_<cat>_calc.js` **0 逃生项**
3. 被「跳过」的用例（textarea / 动态 id `q0..qN`）必须**自建同口径探针**补验「注入 PASS + 回退默认 FAIL」
4. 更新 `scripts/falsepass_baseline.json` 与 `scripts/discriminate_baseline.json`（**只准降不准增**，按 selfcheck/discriminate 实测值同步）
5. `python3 scripts/run_gates.py`（全量 217 项）全过 → `git commit` + push、**单次**确认部署
6. 归档 `.workbuddy/memory/YYYY-MM-DD.md`，清理 `/tmp` 临时脚本

### 10.5 harness 已知限制（选批与定 expect 前必读）

| 限制 | 后果 / 处置 |
|---|---|
| **复选框 / 单选组注入字段（2026-09-24 起）** | `checkIds: ["c","u"]` → `getElementById(id).checked`（纯复选框量表页）；`radios: { htn: "1" }` → `getElementsByName(name)`；`c.checks` → `querySelector(':checked')`/`querySelectorAll('…checked')`。三者均已获 `selfcheck`（算有效注入）与 `discriminate`（清空注入即模拟失败）识别 ⇒ 纯 checkbox 量表页**不再判结构性 `no_inputs`**。**被 checkbox 门控的页面仍可改判「门控前的派生量」** |
| **HTML 默认选中态已生效（2026-09-24）** | `querySelector(':checked')` / `querySelectorAll('…checked')` / `getElementsByName` 在用例未声明 `c.checks`/`c.radios` 时**回落页面 `checked` 属性** ⇒ 默认输出与真机一致（曾使 `optical/progressive-corridor` 抛 TypeError）。**选批注意**：① 新用例优先**显式声明** `checkIds`/`radios`，勿依赖默认态；② 旧 expect 若曾建立于「默认未选中」的失真输出上会失配（本次全量扫描仅 `cardiology/aortic-dissection` 一例，已重写） |
| **动态 id（`q0..qN`）会同时骗过两道静态校验** | `discriminate_check` 判「跳过」、`selfcheck` 判 `null` 不计入 → **基线会「虚降」**。须自建探针补验「注入 PASS + 回退默认 FAIL」，并另用浏览器真实默认值再跑一遍 |
| **表单控件位于 deep-dive 之后 / 页面存在重复 id（2026-09-24 已修）** | `discriminate_check.pageDefaults` 按 `<!-- TOOLBOX-DEEP-DIVE -->` 截断，而全站 **72 页**的表单控件在该标记**之后**（如 `engineering/heat-transfer` 的 input 在第 235 行、标记在第 178 行）⇒ 取不到任何默认值 ⇒ 所有键都无法回退 ⇒ 整例静默判「跳过」，而这些用例其实带真实注入。多页签页还普遍存在**重复 id**（同 id、不同 value），旧版循环覆盖取到**最后一个**，而浏览器 `getElementById` 取**第一个** ⇒ 默认值失真、`usable` 误判 false 又跳过。已修正为「截断后无控件则回退全文」+「首次出现优先」（input/select/textarea 三处同步），据此暴露 5 个被掩盖的真逃生项 |
| **只改「与当前页签无关」的输入键不算去默认化** | 多页签页里 `v1`（属「稀释」页签）、`r`（属「电位器」页签）之类改了也白改 —— 默认页签的输出纹丝不动，用例仍是 `all_default`、仍被跳过。**必须改真正影响当前页签结果的键**（如 mixture-ratio 改 `ca/ma/cb/mb`、voltage-divider 改 `vin/r1/r2`） |
| **材料 / 形状类页靠 `getElementsByName('material')` 单选组 + innerHTML 模板生成控件** | 不注入 `radios:{material:N}` 时 `calc()` 直接抛错（reading `dens` / `E`）⇒ 看不到任何结果，极易误判为「页面真缺陷」，**实为桩盲区**（`engineering/material-calculator`、`engineering/stress-calculator`）。注入 radios 后计算正常，且 radios 使 `usable=true`，判别器即可正常校验 |
| **无 value 的 input 已被判别器覆盖（2026-09-24 起）；textarea / 动态 id 仍需自建探针** | 旧版 `discriminate_check.pageDefaults()` 对无 `value` 属性的 input 直接丢弃 ⇒ 该键无法回退 ⇒ 整例判「跳过」而漏检；现按真机口径登记为**空串**（与 `runCase` 的 `defaults/sel` 一致），据此暴露并修掉 5 个存量逃生项（另 1 个 `legal/court-fee` 为 checkbox 假阳性，已按 type 跳过）。`<textarea>` 与动态 id（`q0..qN`）仍不解析，须自建同口径探针补验 |
| **零参 `setXxx()` 兜底会「改写状态后重算」，产出的串与注入无关**（原缺陷 B 的实操面） | `pets/kennel-space` 的 `selectSize()` 无参被调用时 `currentSize=undefined` → `\|\| sizes[0]` 落回**小型犬**，于是「小型犬值」16.0/36.0 恰好与兜底输出重合 = 逃生项（本例首版即踩坑）。**定 expect 前必须想清：零参调用该页所有 `set*`/`select*`/`setType` 后最终态会算出哪一组值，expect 必须避开它** —— 首选页面**默认选择项**（本题中型犬 24.0/61.5）派生的值。`DESTRUCTIVE` 正则已补 `^set[A-Z]`，但**仍覆盖不了** `selectSize` 这类「名含 set 却不以 `set[A-Z]` 开头」的设值函数 |
| **`inputs` 为空 / 缺失的用例，判别器一律「跳过」** | 即使 `checkIds`/`radios` 也全空也一样跳过 ⇒ **`no_inputs` 弱用例的逃生项判别器兜不住**，只能靠 `selfcheck` 的数量棘轮 + 人工核查。`music/sheet-music` 即此类：页面无任何 input/select/checkbox（调号条是 `innerHTML` 生成的 `span+onclick`，属 §7.1 保留项），**结构性不可注入**，只能断言初始化渲染串并继续留在 `no_inputs` 基线内 |
| **判定发生在 `blob1`（注入后立即收集），不是 `fullBlob`** | 用 `expect:["@@NOMATCH@@"]` 取输出「看结果」是错的。定位逃生项只看 `blob1` |
| **页面源码字面量 + 静态参考表 + 恒定文案都进 blob** | 凡页面含「参考表/换算表」容器且带 id、深度解析示例、图例文案，其数值/词汇均不可作 expect。定 expect 前先 `grep -c "该串" tools/<slug>.html` |
| **「暂无…记录」等占位串是常量型逃生项（命中率最高）** | 凡页面含 `saveHistory/renderHistory/historyBox`（写 localStorage，harness 无实现 → 恒显占位），该串一律不得作 expect |
| **长数字的后缀会吞掉短 expect** | 光「加长」不够，还要防默认态存在以它为后缀的更长数字（`5000.0 g` 被 `15000.0 g` 包含）。修法：合并为跨格连续串 |
| **等级词/分类词须「跨档」** | 定等级类 expect 前必须先算一遍默认态的同档位，不跨档就换锚点数值 |
| **控件带 id ≠ 可注入：class 选择器读取的勾选态 harness 注入不了（2026-09-24）** | 页面若用 `document.querySelectorAll('.'+g.cls)` / `document.querySelectorAll('.s8')` 遍历复选框（`rheumatology/bvas` 43 个、`rheumatology/sledai` 24 个），桩的 `querySelectorAll` 仅对**选择器串含 `checked`** 的调用返回 `c.checks`，纯 class 选择器恒返回 `[]` ⇒ 复选框虽在静态 HTML 里也注入不了。**判据**：`grep -cE '<input[^>]*id='` 为 0 且驱动句是 class 选择器 ⇒ 结构性不可注入，保留 `no_inputs`（改页面补 id 属改动线上已验证内容，不做） |
| **无参 `loadXxx()` 预设函数会覆盖注入值 ⇒ 占位 expect 的 dump 可能是「兜底后」状态（2026-09-24）** | 页面含无参预设函数（`loadNormal`/`loadMS`/`loadDM`/`loadGDM`/`loadPCOS` 等）时，`runCase` 的兜底阶段会调用它们**重写输入并重算** ⇒ 用 `expect:["@@NOMATCH@@"]` 取到的 `fullBlob` 可能只是预设覆盖后的输出，**与注入值无关**；endocrinology 批曾据此误判整批「结构性不可注入」。**正确判据**：看 `runCase` 返回的 `via === "input event"`（注入态即时命中）为真，并让 expect 避开各 `loadXxx` 的预设值 |
| **卡片标签名 / 页脚提示词是最易误用的 expect（2026-09-24）** | `data-card` 的 `label`（「跨中弯曲应力」「输出转矩」「角速度」「转动动能」「校验功率」「阻力」…）与页脚 `tip` 的静态文案（「推荐带速 5~25 m/s」「普通滚子链」）都**与输入无关、默认态必然出现**。mechanical 分类 8 例旧 expect **全部**栽在这两类上。**必须前缀具体数值**，形如 `18.75 最大弯矩 M (kN·m)` 才有判别力 |
| **「双 dump 对比法」定 expect（2026-09-24 起强制）** | 改完先 dump **新注入态**、再 dump **默认态**，逐串比对，**只有真正随输入变化的串才能进 expect**。一批「换值也不变」的输出串靠单看注入态发现不了：gas 批次一次性剔出 7 处 —— `DN20 推荐管径`、`DN25 调压器`、`电流密度 20 mA/m²`、`过保护`、`压降很小`、`流量系数 C=0.6`、`β 比（d/D）=0.50`（后者是 design 批 `focal-length-equivalent` 全画幅→全画幅的同源形态）。另发现 `gas/current-2` 的 `resistivity` 是**无效键**（换值不影响电流密度），与 design 批 `checker` 的 `bgColor` 同源 ⇒ 定 expect 前须实测「换值是否引起输出变化」 |
| **等级词落在静态「参考标准表」表头里（2026-09-24）** | `sports/estimate-tester` 页面含 `VO2max参考标准` 表，表头行就是「优秀 良好 一般 较差」⇒ 等级词「优秀」在**默认态也必然出现**，单独作 expect 必成逃生项 | 等级词必须与指标标签绑成连续串（`优秀 体能等级`，默认态是「一般 体能等级」才不撞）。**凡页面含等级/评级参考表的，等级词一律先 `grep -c` 静态出现次数** |
| **兜底生成场景 / 明细大表会让裸数值 expect 变逃生项（2026-09-24）** | `finance/break-even-calculator`：① harness 兜底调 `addScenario()` 会在默认态额外渲染一组**模板场景**，其「单位边际贡献」恰为 30.00 ⇒ expect `30.00 单位边际贡献` 默认态也命中（实测 3/3）；② 明细表里销量 6000 行的「450,000.00」会命中裸 expect `450,000` | **数值必须与其标签绑成连续串**（`450,000 盈亏平衡收入`），且改完要把每条 expect **单独跑默认态 3 次**（兜底函数顺序随机，跑 1 次可能漏）逐项二分验证 |
| **三类结构性不可注入形态（2026-09-24 归纳）** | ① **需点按钮写 localStorage 的页**（`cleaning/appliance-cycle`「记录今日」、`cleaning/cycle-20`「添加地毯」）：harness 无 `clicks` 字段，且 `setLastClean` 之类被 `DESTRUCTIVE` 的 `^set[A-Z]` 排除 ⇒ 注入对输出零影响（实测 appliance-cycle 换 checkDate 2024-06-15↔2020-01-01 输出完全一致），只能维持 `no_inputs`；② **id 由 JS 模板拼接的页**（`checker-10` 的 `a{区}_{项}`、`checker-9` 的 `m{模块}_{项}`）：注入有效，但 HTML 源码无字面 id ⇒ `discriminate_check` 取不到默认值、判「跳过」，须用同口径双态 dump 人工确认；③ **输入值回显型断言**（`cycle-20` 的 expect 锚 select 的 value）：计算结果根本不变，属已知弱断言，须在 `ref` 里写明、不得计入判别力 |
| **select 在两道校验里取值口径不同** | `selfcheck._pageDefaults` 读全文（取 JS 设定的真实默认），`discriminate_check.pageDefaults` 取**首个 option**。凡页面对 select 值做三元兜底，非预期值会与另一选项同分支 → 这类词不可作 expect |
| **兜底函数的「随机态」会命中等级词** | 凡页面存在 `randomXxx()`/`shuffle` 类兜底函数，等级词一律不用，改断言只由注入值派生的量 |
| **含 `<` 的输出会被标签剥离吞掉** | 如 `< 0.001`，不可作 expect；改锚 Z 统计量 / 置信区间 / 结论文案 |
| **检索/过滤型图鉴页的结果是全量列表的「子集」** | 任何「单卡片内文本」在默认全量态同样存在，作 expect 必为逃生项 |
| **兜底阶段会调用 `swapValues()`（`DESTRUCTIVE` 的 `swap\b` 对它无效）** | 该函数把两个输入**互换后重算** → **二值判读词**（偏高/正常、力度偏大/适中、A 优于 B…）在交换态必命中其中一档 → 判定词一律**不得作 expect**，只锚依赖被测输入的数值项 |
| **`blob.includes(want)` 是子串匹配**（`collectStrings` 返回拼接后的单字符串） | expect 会被默认输出包含：`达标` ⊂ `未达标`、`5.00%` ⊂ `25.00%`。定 expect 前须做「默认态 + 交换态」**双侧子串**检查，必要时给 expect 加标签前缀 |
| **expect 与「默认态输出」字符串一致 → 逃生项**（即便注入的是另一组输入） | 只看 `x/x 全过` 会漏判。**新增用例后必须跑 `discriminate_check`（或先手算默认态输出）**，并换一组能跨分支/跨档的数据 |
| **`select` 的 `selected` 属性在 harness 里不生效**（桩取**首个 option**） | 页面「默认选中项」类改动无法用默认态用例验证 —— 必须**显式注入该 select 的值**；判断真实浏览器行为只认 HTML 标准 |
| **页面自带的 `fmt()` 常走 `toLocaleString()`（默认截 3 位小数）** | `0.0025` 会显示成 `0.003`，使「分步计算」文案无法自校验、也易被误判为算术错。凡步骤/卡片要展示小数量，改用带参 `toFixed(n)`；定 expect 时避开被截断的位置 |
| **控件写在 deep-dive 标记**之后**时，`pageDefaults` 仍取不到 ⇒ 该键在判别器里「无法回退」（2026-09-24）** | 2026-09-24 的「截断后无控件则回退全文」只修了**整页**无控件的情形；`mining/excavation-volume` 这类**前面有静态控件（swell/price）、形状参数（L/W/D）却由 `renderParams` 模板写在标记之后（第 244 行起）** 的页，截断段里已有控件 ⇒ 不触发回退 ⇒ `defs` 只有 swell/price。模拟注入失败时 L/W/D 保持注入值不变 ⇒ **断言「原状方量 1080.0 m³」是逃生项**（已实测并被判别器抓出）。**定 expect 前先 `grep -n 'id="L"' tools/<slug>.html` 看行号是否 > deep-dive 行号**；是则 expect 只能锚**同时依赖可回退键**的量（松方量 ×swell、总造价 ×price） |
| **比例型页面改输入必须「打破比例」（2026-09-24）** | `chemical/solution-concentration` 默认 58.5/58.5/1 得 C=1.0000 mol/L、质量浓度 58.50 g/L；首版改成 117/58.5/2（mass 与 vol 同倍放大）后 **C 与质量浓度与默认完全重合**，只有「物质的量 2.0000」变了 ⇒ 仍近乎无判别力。改 90/45/0.5 才得到 4.0000 mol/L 与 180.00 g/L。**凡输出是比值/密度/单价这类「齐次」量，换值前先确认新输入不是默认输入的等比缩放** |
| **多页签页的 harness 末次调用决定 res 内容（2026-09-24）** | `chemical/detector-39` 默认页签是「酸碱滴定」，但 harness 依次调用 `calc → calcT → calcG`，**最终 res 是 `calcG`（重量法）的输出** ⇒ 改滴定页签的 conc/vol/mass/molar 对 blob 毫无影响，用例仍是 all_default。多页签页定 expect 前必须**先 dump 默认态看实际落到哪个页签**，再改对应页签的键 |
| **按钮驱动的交互页在静态 HTML 里 0 控件 ⇒ 结构性不可注入（2026-09-24 dermatology 批）** | `dermatology/contact-dermatitis-patch`（14 个过敏原卡片由 `renderGrid()` 拼 HTML、反应强度靠卡片内 `<button onclick="setReact(...)">` 写 `selections`）、`miliaria-classification`（`selectType(btn,idx)`）、`wood-lamp`（`selectFluor(btn,i)`）三页的 `input/select/textarea` 计数**均为 0** ⇒ harness 既无可注入控件、按钮又不在 `elements` 表内（且无 clicks 注入）⇒ 只能渲染默认串。**选批前先预筛**：`grep -cE '<input|<select|<textarea' tools/<ind>/<slug>.html` 为 0 即结构性不可注入，保留在 `no_inputs` 基线并在 `ref` 写明理由 |
| **`grade` 由 `selectGrade(btn,g)` 点击改写 ⇒ harness 里恒为默认档（2026-09-24）** | `dermatology/chilblain-grading`（`var grade=1`）与 `hdss-hyperhidrosis`（`grade=2`）的严重度分支只能点按钮改，而 `selectGrade()` 无参调用会在 `btn.classList` 抛错 ⇒ **grade 派生文案（I 级建议、20% 氯化铝建议）在注入前后完全一致**，以其为 expect 即默认命中（逃生项）。可注入点只剩 checkbox 派生的「受累部位 / 分型提示 / 警示」三串。**定 expect 前先确认目标量能否被 input/checkIds 触达**：不能则换锚点 |
| **`render()` 用 `.length` 判空但入参是对象 ⇒ 整页功能恒空（P0 真缺陷，2026-09-24 travel 批）** | `travel/travel-adapter-guide` 的 `render(list)` 写 `if(!list.length)`，而 `plugs` 是**对象**、`filter()` 也传对象 ⇒ `undefined` 恒真 ⇒ 修前无论搜索什么都只显示「未找到」，默认态亦然（原 expect 正是这个「未找到」＝ 缺陷与逃生项双重命中）。改 `if(!list||!Object.keys(list).length)` 后搜索生效。**启示**：`Object.entries(list)` 遍历 + `list.length` 判空混用是高频真缺陷；遇「整页功能恒定不工作」的弱用例，先怀疑判空/类型错，别急着归类为「不可注入」 |
| **有 id 的控件注入后输出逐字不变 ⇒ 仍属结构性不可注入（2026-09-24 travel 批）** | `travel/packing-list` 有 `input#tripName`/`input#tripDate`（判别器不会判「跳过」），但渲染主体 `renderList()` 只读 `currentData.categories`，`tripName` 仅在 `saveList()` 写 localStorage 时使用，而 `saveList` 不在 harness 兜底调用序列内 ⇒ 注入 tripName=测试行程A 后 blob 与默认态逐字一致。**判据**：控件的处理函数是否在 harness 实际调用链上；不在 ⇒ 输出无关，保留 `no_inputs` 并在 `ref` 写明（与 estimate-reserve / contact-dermatitis-patch 同类） |
| **selfcheck 全站 `--exec` 会崩（历史现象，勿误判为本批引入，2026-09-24）** | 结尾抛 `TypeError: process.exit is not a function`（某页脚本污染全局 process），且顺带打印数百条 `default-hit`。**取基线请用结构模式** `node scripts/selfcheck_false_pass.js scripts`（与门禁第 216 项同口径，risk=0），只看 no_inputs/all_default 计数行；`--exec` 仅供单文件调试。已用 `git show HEAD:<file>` 对照复现，确认与当批改动无关 |
| **无参 `loadXxx()` 兜底预设会把「可注入页」伪装成「不可注入」（2026-09-24 endocrinology 批）** | `runCase` 顺序是：① 注入 inputs + 触发 input/change/keyup → **立即**检查 expect（命中即 `via="input event"`）；② 未命中才兜底**遍历无参调用各函数**（跳过 DESTRUCTIVE）。而 `endocrinology/*` 这类页普遍带 `loadNormal()/loadMS()/loadDM()/loadPCOS()` 预设函数，会把输入**全部改回预设值**并重算 ⇒ **用占位 expect 做 blob dump 看到的是兜底后状态**（与注入无关），极易误判为「注入无效 ⇒ 结构性不可注入」 | 判据必须看 **`r.via === "input event"`**（本批 7 例全部如此）；标准流程：读页面 `calc()` 渲染模板构造 expect（如 `arr.toFixed(1)` + 标签）→ 测注入态（期望 ok 且 via=input event）→ 测默认态（期望 not ok）→ 最后避开 `loadXxx` 预设值（`metabolic-syndrome` 的「满足 5 / 5 项标准」、`ogtt-interpretation` 的「1h： 11.5」「2h： 9.2」都是预设产出，作 expect 即逃生项） |

### 10.6 方向1：公式-脚本一致性精查（**全量闭环** · 老板选定）

- **目标**：逐页独立复算计算类页 `calc()` 输出的数学/物理正确性（与标准公式/权威向量比），找"用户拿到错钱数/错物理量"的真缺陷（§4.5 红线第一条最高频事故）。
- **覆盖（已全量闭环）**：10 高热度行业（science / math / geometry / photo / ai / sports / agriculture / finance）+ 金融周边集群（banking/investment/tax/realestate/accounting/insurance/economics/statistics/forex/futures ~334 页）+ 中低热度 113 个行业（页≥15）+ **96 个小行业（<15 页，687 页）**默认态与 ZERO/EMPTY 边界态。边界 NaN 守卫已铺开（4 个待办分类 86 页 + 7 个物理工程行业 194 页）。
- **工具（均在本地，`_*.js` 按 `.gitignore` 不入库）**：
  - `scripts/_audit_iso_small.js` —— 批量隔离器。`node 脚本 <industry,ind2,...>`；`DUMP=1` 另写 `/tmp/iso_small.json`。**不要用「函数名必须含 calc」的窄口径过滤入口**（会漏掉 `compare()`/`update()` 类页，687 页里因此漏审 168 页）；桩需覆盖 `MutationObserver`/`getElementsByName`/`style.setProperty`/`cloneNode`/`insertAdjacentHTML`/`toBlob`/`ctx.*`/`window.X=` 透传 globalThis/`innerHTML` 里 `<select>`+`<option>` 注册。
  - `/tmp/jsdom_probe.cjs` —— **jsdom 真实 DOM 复核探针**（里程碑：不再靠"猜桩盲区"）。对候选页跑 DEF/ZERO/EMPTY 三态，读 `result|grid|card|state|total|detail` 类容器文本，判 `NaN|Infinity`。**判据：隔离器报的 `err` 一律先过 jsdom 复核；jsdom 三态无 NaN/Infinity ⇒ 桩盲区，立排除，不改页。**
- **SOP**：① 隔离器扫 DEF 态 → 筛 `NaN`/`Infinity`/越界值/`err`；② 每条 `err` 过 jsdom 三态复核，区分「桩盲区」与「真缺陷」；③ 确凿缺陷才改页，改完补/改用例。
- **纪律**：确凿真缺陷前不改页面；找到即立项闭环（修 calc + 修/注册 verify 用例 + run_gates + 提交推送）。

