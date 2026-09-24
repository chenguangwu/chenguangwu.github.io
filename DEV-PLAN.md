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
  - ✅ **`innerHTML=` 动态生成的控件已可注入**（BATCH91 闭环，2026-09-24）：harness 新增 `clicks: ["pick(0,3)", …]` 字段（在 inputs 注入之后、兜底之前按序于页面作用域执行，命中即 `via="click"`）＋ 用例级「动态 DOM 登记」（`innerHTML` setter 按容器 id 分桶解析 `{tag,id,class}`，`querySelectorAll` 从登记表回填 —— 供 `pick()` 内 `its[i].querySelectorAll('.q-opt')` 与 `classList.toggle` 不抛错）。**以 `DYN.on` 开关隔离**：仅当用例声明 `clicks`/`dynDom` 时启用，其余用例行为逐字节不变 —— 由此绕开 2026-09-23 全站无差别 `id` 注册误伤 `psychology/calc-12` 的坑。`psychiatry` 18 例已全部去默认化（`no_inputs` 170→152）。**BATCH92（同日晚）把 `clicks` 升级为「页面作用域求值」**：编译期保留 `__pageEval`，作答代码由「全局 `new Function`」改为「页面作用域 direct eval」——因各页可变状态（`selLoc`/`ausData`/`checked`/`selected`/`answers`…）是顶层 `var`，只导出 `function` 的旧机制够不到；页面作用域是全局的**严格超集**，故 pick 型用例行为不变。据此 `tcm-diagnosis` 13 例去默认化、1 例（`etiology-tree`，纯浏览无输出容器）结构性保留（`no_inputs` 152→139）。
  - ✅ **`checks`（已选中项）已纳入弱用例判定**（BATCH93 闭环，2026-09-24）：`c.checks` 是 harness 里 `querySelector('input[name=x]:checked')` 的返回值，即「哪一项被选中」——对 `berg-balance-scale`/`flacc-scale`/`mmse-scoring`/`mmt-grading` 这类**题目与选项全由 `render()` 拼 `innerHTML` 生成、静态 HTML 无任何表单控件**的量表页，它是唯一的真实注入方式。此前 `selfcheck_false_pass.weakKind` 与 `discriminate_check` 只认 `checkIds`/`radios`/`clicks`，这 4 例被误判 `no_inputs` 并计入判别器 `skip`。**已按「仅在『无 inputs』分支计入、不参与 `all_default` 判定」的最小口径补齐**（全站仅这 4 例为 checks-only，改动零副作用）。据此 `dentistry` 4 例 + `rehabilitation` 8 例去默认化（`no_inputs` 139→127，判别器已检 2898→2906 / 跳过 263→255）。剩余 `fim-scale`（同批已改，仅判别器取不到默认值）/`womac`/`load-curve` 等按 P3 顺带推进。
  - ✅ **expect 锚在 else（最高严重度）分支会被「零参兜底算坏状态」的破坏态复现 ⇒ 逃生项**（BATCH97 闭环，2026-09-24）：`clinical-nursing` 8 例去默认化（`barthel-index`/`braden-score`/`morse-score`/`pain-nrs`/`fall-emergency-flow`/`surgical-position-risk` 走 `clicks`，`cycle-7`/`suction-pressure` 走 `inputs`）。其中 3 例首版 expect 锚在「极度风险 / 高度跌倒风险 / 重度疼痛」＝**条件分支的 else 兜底路**，而 harness 兜底阶段无参调用 `selectScore(undefined,undefined)` 会先写坏状态（`scores[undefined]=undefined` ⇒ `total=NaN` ⇒ 所有阈值比较为 false ⇒ 落 else），`getLevel(undefined)` 亦因 `undefined<=各 max` 均 false 返回 `labels[last]` ⇒ **「清空注入」的破坏态反而命中 expect**，判别器虽正确变红但该 expect 已零判别力。修法 = 锚**非兜底分支的 desc 独有串**（`每2小时翻身一次` / `保持病区环境安全` / `可考虑非药物干预`，逐串 grep 静态 HTML 确认零出现），改后默认态 8/8 全 FAIL。文件判别力「已检 **26** / 全变红 / 跳过 **0**」（`no_inputs` 107→100、`all_default` 91→90）。
  - ✅ **「FAIL 的 blob 是兜底后视图」——判 clicks 是否生效不能用 FAIL 的 blob（BATCH99 闭环，2026-09-24）**：`admin` 5 例 + `archaeology` 2 例去默认化，并修复坏用例 `baking/mold-volume`（`all_default` 78→74、`no_inputs` 100→98；判别器已检 2948→**2955** / 跳过 213→**206**）。**最关键的 harness 认知**：`clicks` 执行后若 expect 未命中，程序会继续进入阶段 3（无参遍历调用候选函数），`render()` / `calc()` 会把结果区**重写回默认值** ⇒ **FAIL 时 `fullBlob` 呈现的是「兜底后」的视图**，与默认态逐字相同，据此判断「clicks 未生效」必犯错（本批 `meeting-conflict` / `checker-manager-training-hr` 曾因此白查一小时、还误判为「页面不可注入」）。**正向判据**：把 expect 换成**标记串**（`clicks:["document.getElementById('stats').value='MARK_V'"]` + `expect:["MARK_V"]`）跑一次，命中即证明写入路径通；本次三路对照（`value` / `innerHTML` / `ToolBox.setResult`）**全部 OK**，证明写入无碍、问题只在 expect 锚点。**另一坑**：`archaeology/site-grid` 首版误锚越界提示「部分探方超出遗址范围，请核对尺寸」—— 默认态 nL=12 ⇒ `siteLen = 12×5+11×1 = 71 > 遗址长 60` ⇒ **默认本身就越界**、同样落该分支 ⇒ 零判别力（默认态 `via=calc` 逃逸）；**判据**：「范围/越界/警告」类提示语务必先算默认态是否也触发。`admin/detector-time` 判**结构性不可注入**（`addRow` 用 `createElement + #rows.appendChild` 建行、`detect()` 靠 `querySelectorAll('#rows .input-row')` 遍历；桩的 `dynRecord` 只登记 `innerHTML` 解析出的标签、不含容器 div 自身 ⇒ 选择器恒空），按 `tcm-diagnosis/etiology-tree` 先例保留 `no_inputs` 并写明 `ref`。
  - ✅ **dump 探针：`clicks` 内把结果回写到独立元素，绕开「FAIL 的 blob 被兜底覆盖」盲区（BATCH100 闭环，2026-09-24）**：`chemistry` 3 例 + `chess` 4 例去默认化（`all_default` 74→**67**、`no_inputs` 98 不变；判别器已检 2955→**2961** / 跳过 206→**200**）。BATCH99 查明「FAIL 时 `fullBlob` 是兜底后的视图」后，本批改用`clicks:["calc();document.getElementById('__p').value=document.getElementById('result').innerHTML"]` —— **兜底阶段只会重写 `result`、不碰 `__p`**，故 FAIL 时仍能在 blob 里读到真实注入输出，7 例一次拿全真实值（省去逐个试 expect 的来回）。要点：① `chess/gomoku-forbidden` 等级词「长连禁手」在静态规则表里出现 6 次 ⇒ 只能锚子分支专属句「黑棋形成6连（超过五连）…」；原 expect「结合实际棋盘分析」是页脚常驻免责文案；② `chess/xiangqi-endgame` 结构性不可注入（常量 `ENDGAMES` + `renderEndgames()` 一次性渲染三 tab，交互仅 `classList.toggle` 不入 blob）保留 `no_inputs` 并写明 `ref`；③ **工具**：`chemistry` 是**无引号键风格**（`quoted=0`）⇒ 必须用 `patch4.py`（`patch3.py` 只认带引号风格、会静默不命中并吃掉注释缩进）；改完须逐块 JSON 比对确认非目标块 0 变动、注释零 diff。
  - ✅ **只锚「可注入字段派生的量」＋ 避开零参兜底函数产出（BATCH98 闭环，2026-09-24）**：`agriculture` / `baking` / `hvac` 三分类 12 例全部去默认化（`all_default` 90→78、`no_inputs` 100 不变；判别器已检 2936→**2948** / 跳过 225→**213**）。`hvac/duct-calculator` 是关键标本：`diaD` 位于默认隐藏的圆形面板，**注入值与 `calc()` 读取不是同一份 DOM 实例 ⇒ diaD 注入完全无效**（实测 `inputs{diaD:"600"}` 与 `clicks` 内赋值都改不动，输出恒 `Φ 500 mm`），且形状判定 `$('btnRect').classList.contains('active')` 在桩里恒 false ⇒ 恒走圆形分支 ⇒ 只能锚**仅由 Q/v 决定**的「所需截面积 F」（0.1389）。另两处实证：① **零参兜底函数会污染「分支文案」型锚点** —— `suggestSize()`（duct）/ `calc()`（pump）被无参调用后照样渲染「建议调整风管尺寸」；② **锚点若在默认态也命中即零判别力** —— `pump-calculator` 原第二锚点写截面积 0.00785，但默认管径同为 100mm ⇒ 已换为随输入变化的「2.69 管内流速 v (m/s)」。三文件判别力：agriculture 17/0、baking 7/1（`baking/mold-volume` 的 `inputs` 键是生成器模板串残留 ⇒ 双双漏判，**记为待修**）、hvac 9/0。
  - ✅ **「控件运行期渲染」页面改用 `clicks` 内 `document.getElementById` 赋值（BATCH96 闭环，2026-09-24）**：`beauty/checker-14`/`checker-assessor-1`/`checker-assessor-2`/`assessor-risk-12` 的 `<select>` id 全由 `buildList()` 运行期拼 `innerHTML` 生成（`d{di}i{ii}`、`stage+i`、`key+i`、`c{i}`）。**不要写 `inputs`**（判别器 `pageDefaults` 在静态 HTML 里找不到这些 id ⇒ `usable=false` ⇒ 整例静默 `skip`），改用 `clicks: ["…document.getElementById('c'+i).value='2'…;calc()"]` —— `clicks` 属「无 inputs 分支」的真实注入，判别器清空后必然变红，`checked` 直接提升。`beauty` 8 例（另含 4 个纯 onclick 卡片页）已全部去默认化，文件判别力「已检 **21** / 全变红 / 跳过 **0**」（此前 13/8），`no_inputs` 114→107、`all_default` 92→91。
  - ✅ **「inputs 与默认值逐字相同」的用例判别器会静默跳过（BATCH95 闭环，2026-09-24）**：`ophthalmology/visual-fatigue-vas` 原用例 `inputs{vasSlider:"5"}` 与页面 `value="5"` **完全相同** ⇒ 判别器 `usable=false` 直接 `skipped++`，该例虽在 `all_default` 基线上却**从未被判别力校验**；其 `expect「从不(0)」` 又是问卷选项标签文案（与输出无关）。改法：`inputs{vasSlider:"8"}` + `checks:["3"]`（12 项症状全选 3）+ `clicks:["calc()"]` —— 该页 `calc()` **只由按钮 onclick 触发**（`range` 的 `oninput` 只调 `updateVAS`），必须 clicks 驱动 ⇒ total = 8×5 + 36 = 76 > 50 ⇒「重度」。判别器在 inputs 分支会**同时清空 checks/clicks** ⇒ 回退默认后 `answered=0` ⇒ 输出「请至少作答部分症状问卷」⇒ 正确变红，本例由 `skipped` 转入 `checked`。**判据**：`selfcheck` 的 `all_default` 只按「inputs 值 == 页面默认值」判定，凡 `all_default` 例一律视为零判别力、须重写。
  - ✅ **「按钮驱动 + 顶层 `var` 状态」整类页面已可注入**（BATCH94 闭环，2026-09-24）：`ent` 的 7 个量表页（`facial-nerve-hb`/`gag-reflex`/`grbas-scale`/`lund-kennedy-score`/`lund-mackay-score`/`vocal-cord-assessment`/`eustachian-tube`）题面与选项全是 `<button onclick="selectGrade/selectOpt(this,…)">`、**无任何 input/select**，但状态就存在页面顶层 `var`（`grade`/`scores`/`sel`/`selections`+`symptomSelected`）。`clicks` 在页面作用域直接写这些 `var` 再调 `calc()` 即可（**比模拟点按钮更稳**：无需构造 `btn.classList`/`dataset`）。`ent` 8 例（含 `calc-1` 的 4 个 select）已全部去默认化（`no_inputs` 127→119，判别力「已检 23 / 全数变红」）。
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

- `all_default 67 / no_inputs 98 / escape 0`；`checked=3161`；门禁 `run_gates.py` **217 项全过**、逃生项 0（判别器已检 **2961** 例 / 跳过 200）。
- A 级率 **99.2%**（A 4693 / B 32 / C 4，共 4729）；deep-dive 术语内链 **1591 页 / 2268 条 / 唯一目标 630**（零死链、零自链、单页 ≤6 条）。**注：内链不影响质量分级**（`own_len` 只统计 `<script>` 内容）。
- 存量弱用例 **165 例**（`no_inputs=98` / `all_default=67`），**转 P3 顺带**，不单独成批。
  - **注意：弱用例整体处于判别器盲区** —— `discriminate_check` 对「注入值本就等于默认值」的用例判 `usable=false` ⇒ **直接跳过**（§10.5）。故 `escape=0` 只说明「强用例无逃生项」，弱用例的逃生项从未被检查；每批改造弱用例后必须重跑判别器确认其由「跳过」转为「已检且变红」。

### 10.3 弱用例去默认化（仅在 P0/P1 顺带时执行）

**存量 165 例**（`no_inputs=98` / `all_default=67`，selfcheck 口径；含 textarea/动态 id/结构性不可注入的「skip」类全站 200）。

**选批预筛清单（2026-09-24 实测 · 弱例数 / 其中可注入数）** —— 按「可注入数」降序挑批次，**不可注入的不要选**（页面静态 HTML 里 `grep 'id='` 为 0，控件由 innerHTML 动态生成，属 §7.1 保留项）：

**（§10.3 选批清单已空 —— 全部 209 分类的弱用例批次处理完毕）**。

**不可注入（结构性，勿选）**：`psychiatry` 24 例里 **18 例**页面只有 `id="quiz"` + innerHTML 渲染（`gad7`/`phq9`/`pcl5`/`mdq`/`asrs`/`cage`/`isi`/`ybocs`/`bis11`/`cdrisc`/`lsas`/`panss`/`pdss`/`phq15`/`eat26`/`cssrs`/`aq`/`les`）—— **已于 BATCH91（2026-09-24）以 `clicks` + 用例级动态 DOM 登记机制全部去默认化，不再属 `no_inputs`**（判别力「已检 18 / 全数变红 / 跳过 6」）；`tcm-diagnosis` 14 例同类 —— **已于 BATCH92（2026-09-24）13 例去默认化、1 例保留**（`etiology-tree` 结构性不可注入：仅 `treeContainer` 一个容器、交互只有 `classList.toggle`（不进 blob）/`copyTree()` 写剪贴板（桩无实现）；13 例判别力「已检 18 / 全数变红 / 跳过 1」）；`chemical` 6 例、`mining` 9 例已于 2026-09-24 清零（chemical 判别力「已检 10 / 全数变红」，`checker-15` 因 id 由 JS 模板拼接被判跳过、已自建探针补验；mining 判别力「已检 11 / 全数变红」，`estimate-reserve` 属结构性不可注入 —— 块段由 `addBlock()` 按钮 + class 选择器动态生成，静态 HTML 无带 id 控件）；`engineering`、`signal`、`design`、`gas`、`mechanical` 已于 2026-09-24 清零（判别力分别由「已检 0 / 跳过 14」→「已检 14」、「已检 13 / 跳过 11」→「已检 24」、「已检 5 / 跳过 9」→「已检 14」、「已检 2 / 跳过 9」→「已检 11」、「已检 5 / 跳过 8」→「已检 12」，均为全数变红）；`cleaning` 同日改掉 6 例（判别力「已检 5 / 全数变红」），**残留 1 例** `appliance-cycle` 属结构性不可注入（见 §10.5 三类形态）；`finance` 同日 7 例清零（判别力「已检 21 / 全数变红」）；`sports` 同日 7 例清零（判别力「已检 29 / 全数变红」）；`dermatology` 同日 12 例改掉 9 例（判别力「已检 20 / 全数变红」），**残留 3 例** `contact-dermatitis-patch`/`miliaria-classification`/`wood-lamp` 属结构性不可注入（三页 `input/select/textarea` 计数为 0，交互全靠 JS 模板生成的按钮 onclick，见 §10.5）；`travel` 同日 9 例改掉 6 例（判别力「已检 17 / 全数变红」）并**顺带修掉 1 个 P0 页面缺陷**（`travel-adapter-guide` 的 `render()` 对对象用 `.length` 判空 ⇒ 整页搜索恒显示「未找到」，见 §10.5），**残留 3 例** `aim-trainer`/`emergency-phrasebook`/`packing-list` 属结构性不可注入；`endocrinology` 同日 21 例里改掉 7 例（判别力「已检 19 / 全数变红」），**残留 1 例** `ti-rads`（0 表单控件）；`fire` 同日 11 例里改掉 6 例（判别力「已检 10 / 全数变红」），**残留 1 例** `response-drill`（场景随机、按钮驱动）；`rheumatology` 同日 25 例里改掉 5 例（判别力「已检 20 / 全数变红」），**残留 2 例** `bvas`/`sledai` 属结构性不可注入（按 class 选择器 `.g1/.g2`、`.s8/.s4/.s2/.s1` 读取无 id 复选框，harness 的 `querySelectorAll` 仅对含 `checked` 的选择器返回注入项，纯 class 选择器恒返回空数组）；`language` 同日 12 例里改掉 5 例（判别力「已检 11 / 全数变红」），**残留 1 例** `vocabulary-builder` 属结构性不可注入（0 表单控件，词表由 JS 模板生成）；`aquaculture` 同日 5 例全部改掉（判别力「已检 5 / 全数变红」，无残留）—— 5 例原 expect 均为「暂无计算记录」常量型逃生项；`bridge` 同日 5 例全部改掉（判别力「已检 5 / 全数变红」，无残留）—— 原 expect 为标签/单位/判定片段，其中「满足要求」属二值判读词；`glass` 同日 5 例全部改掉（判别力「已检 5 / 全数变红」，无残留）—— 5 例原 expect 全为标签片段且 inputs 恰等于页面默认值（全员 all_default），其中 `snell-refraction` 由默认「空气→水 30°」折射分支**跨到「玻璃→空气 45°」全反射分支**（临界角 41.15°）；`life` 同日 5 例全部改掉（判别力「已检 16 / 全数变红」，无残留）—— 5 例属「有真实 inputs 但恰等于页面默认值」型 `all_default`，原 expect 为单值/判读词；其中 `leap-year-checker` 原断言「闰年（366 天）」是**纯判读词**（与 year 取值无关，改 2000 仍命中），改锚「1900 - 1911 年附近的闰年：」+ 列表「1904、1908」；`manufacturing` 同日 5 例全部改掉（判别力「已检 5 / 全数变红」，无残留）—— 原 expect 全是**页面常驻文案/表格词**（「当前」「建议加强质量控制」「最小总库存成本」「世界级标准」「能力过剩」）＝常量型逃生项；5 页**只有「计算」按钮 onclick、无 input 绑定** ⇒ 命中通道为兜底无参 `calc()`（`via=calc`）；`maritime` 同日 5 例全部改掉（判别力「已检 5 / 全数变红」，无残留）—— 5 例原 expect 全是单串标签/单位/判读词（「出链长度合理」「罗航向」「小时」「舱容受限」「分钟」），其中 `stowage-factor` 由默认 sf 模式**跨到 capacity 模式**（4,800 m³ / 53.3% / 7,000 t）。**本批观察**：本 5 页 `<select>` 选项**均无 `selected` 属性** ⇒ harness 首项 == 真机首项（与 `bridge/span-calc` 的 selected 不一致情形不同），但跨分支取值仍必须显式注入；`medical2` 同日 5 例中 4 例改掉（判别力「已检 5 / 变红 4」，无残留）—— 硬化的 4 例含 `surgery-duration`（注入 `procedure` select 触发 `onchange=addProcedure()`，把术式加入 `selected`，属可注入）、`medical-abbrev`（静态词表搜索页，**只锚计数**）、`bed-occupancy`、`iv-drip-speed`；第 5 例 `drug-expiry` **结构性不可注入**（数据源 localStorage 桩 `getItem` 恒 null ⇒ `data` 恒空；唯一写数据函数 `saveForm()` 命中兜底 `^save` 被跳过），保留 `all_default` 并在 `ref` 写明原因。**本批新坑**：静态词表页首版锚了行内容（`qd quaque die 每日一次 医嘱`）——该行在**默认全表渲染**时同样出现，因「expect 任一命中即 PASS」立刻退化成逃生项；**只可锚随搜索词变化的计数**；`dentistry` 4 例 + `rehabilitation` 8 例已于 BATCH93（2026-09-24）去默认化（判别力「已检 reh 16 / den 21、全数变红」；其中 reh `asia-impairment-scale`/`fim-scale`、den `gingival-index`/`rater-risk-2` 因控件运行期渲染、判别器取不到默认值仍计 skip，已用注入态/默认态双跑手工核验「12 例默认态全 FAIL」）——**本批顺带修掉 1 个 P0 页面缺陷**：`rehabilitation/asia-impairment-scale` 感觉总评分分母 `/112` 系量纲错（28 皮节×4 位点×2 分=224），真机默认态原显示 `224/112`（率>100%），已修为 `/224`；`ent` 8 例已于 BATCH94（2026-09-24）去默认化（判别力「已检 23 / 全数变红」，无残留）—— 打法 = `clicks` 在页面作用域直接给顶层 `var`（`grade`/`scores`/`sel`/`selections`）赋值再调 `calc()`；**本批顺带修掉 1 个 P0 页面缺陷**：`ent/eustachian-tube` 的 `adjustedScore = total − symptomCount` 未截断 ⇒ 客观 0 分 + 9 症状会渲染「评分 -9 / 18」「开放程度 (-50%)」，已修为 `Math.max(0, …)`（`calc`/`copyResult` 两处）；`ophthalmology` 6 例已于 BATCH95（2026-09-24）去默认化（判别力「已检 27 / 全数变红 / 跳过 0」，无残留）—— 5 例走 `checks`（`fluorescein-staining`/`meibomian-grading`/`osdi-scale` 的选项由 `buildZones()`/`buildQ()` 运行期拼 `innerHTML` 生成）+ 2 例走 `inputs`（`calc-1`/`rater-7`）+ 1 例 `visual-fatigue-vas` 属「inputs 恰等于页面默认值」型 `all_default`（判别器 `usable=false` 静默跳过）须改用 `inputs`+`checks`+`clicks[calc()]`；**本批顺带修掉 1 个 P0 页面缺陷**：`ophthalmology/calc-1` 的 CCT 校正符号写反（原 `iop + ((cct−544)/10)*0.7`，厚角膜反而把校正值上抬），与本页文案「厚角膜实测被高估」及姊妹页 `iop-correction` 的 Ehlers(520−cct)/Doughty(542−cct)/Feltgen(550−cct) 三种标准式符号相反，已改为减号并同步生成器 `scripts/apply_ophthalmology.py`、`i18n/tools/content_deepdive.json`、指南页 `guides/ophthalmology-calc-1-guide.html`（顺带把「Doughty 线性法」正名为「线性校正法」，因 544μm/0.7 并非 Doughty 原始参数 542μm/0.020）；`beauty` 8 例已于 BATCH96（2026-09-24）全部去默认化（判别力「已检 21 / 全变红 / 跳过 0」，无残留）—— 前三例与 `assessor-risk-12`（共 4 例）的 `<select>` id 由 `buildList()` 运行期生成，**改用 `clicks` 内 `document.getElementById` 赋值而非 `inputs`**（写 `inputs` 会被判别器判 skip），另 4 例（`face-hair-match`/`makeup-shade`/`nail-color-harmony`/`skin-tewl`）静态控件数为 0、交互全是 onclick 卡片/按钮，`clicks` 直接写顶层 `let` 状态再调渲染函数。`clinical-nursing` 8 例已于 BATCH97（2026-09-24）全部去默认化（判别力「已检 26 / 全变红 / 跳过 0」，无残留）—— 6 例页面 `input/select/textarea` 计数为 0、选项全是 `<button onclick>`、分数存顶层 `scores` 对象或点选函数（`barthel-index`/`braden-score`/`morse-score`/`pain-nrs`/`fall-emergency-flow`/`surgical-position-risk`）走 `clicks`；2 例走 `inputs`（`cycle-7` 的 `ptInput`/`startInput` 静态空默认、`suction-pressure` 的 90mmHg + `clicks` 切 `currentAge`）。**本批关键坑**：3 例首版 expect 锚在 else（最高严重度）分支，被 harness 零参兜底的破坏态复现成逃生项（详见 §10.5 / §7.1）。

**BATCH98 已处理（2026-09-24）**：`agriculture` 4 例（`estimate-fuel-engine-oil` / `estimate-area-density` / `ratio-10` / `calculator-calc-ratio-1`）、`baking` 4 例（`convert-28` / `convert-temp` / `dough-hydration` / `fermentation-time`）、`hvac` 4 例（`cooling-tower` / `duct-calculator` / `pump-calculator` / `supply-air`）全部去默认化（均为「inputs 逐字等于页面默认值」型 `all_default`）。**遗留待修**：`baking/mold-volume` 的 `inputs` 键写成生成器模板串（`"'+side+'D"` 等），页面无此 id ⇒ `pageDefaults` 找不到、整例被判 `skip`（判别器漏检）；修法须用 `clicks` 驱动其运行期渲染的输入（比照 BATCH96）。另：`agriculture/estimate-area-density` 在文件里**有两份同名用例**（历史累积），本批一次改掉两份、内容已一致。

**BATCH99 已处理（2026-09-24）**：`admin` 5 例（`supplies-forecast` / `travel-subsidy` / `meeting-conflict` / `checker-manager-training-hr` / `detector-time`）、`archaeology` 2 例（`artifact-measurement` / `site-grid`）+ **修复坏用例 `baking/mold-volume`**（原 `inputs` 键为生成器模板串残留、`expect` 只有静态标签词「高度」⇒ 判别器与 selfcheck 双双漏判，改用 `clicks` 给运行期生成的 `fromD/fromH/toD/toH` 赋值后 `calc()`，锚 707 / 3142 / ×4.44 / 2042；baking 判别力由 7 检 1 跳 → **8 检 0 跳**）。**逐例打法**：`supplies-forecast`（window=2/safetyFactor=1.5 ⇒ 151.5 / 227.3）、`travel-subsidy`（mealStd=150/transStd=120 ⇒ 4,890 / 1,050）、`artifact-measurement`（20/10/4/800/12/6 ⇒ 800.0 / 0.40 / 2.00）、`site-grid`（100/60/10/2 ⇒ 60 探方 / 2260.0 m²）四例走 `inputs`；`meeting-conflict`（重写顶层 `events` 为三条自定日程 ⇒ 冲突：甲 与 乙 / 重叠 30 分钟 / 270分钟）、`checker-manager-training-hr`（12 个运行期 select 全置 2 分 ⇒ 100% / 8/8）两例走 `clicks`；`detector-time` 保持 `no_inputs`（结构性不可注入，见 §10.5）。**注意**：`supplies-forecast` 的「月均 138.0 / 最高 155.0 / 波动范围」、`travel-subsidy` 的「出差天数 7 / 住宿限额 3,000」只由页面顶层常量决定、与注入字段无关 ⇒ 默认态同样命中，一律不锚。

**BATCH100 已处理（2026-09-24）**：`chemistry` 3 例（`mass-fraction` 35/140 ⇒ 25.00 / 105.00 / 0.25000；`mass-to-moles` 36/18.015 ⇒ 1.9983 / 0.5004 / 1.2034e+24；`poh-to-ph` 2.5e-5 ⇒ 4.602 / 9.398 / 4.000e-10）、`chess` 4 例（`bridge-scoring` level=5/tricks=11 ⇒ 定约分 100 / 奖金 300 / 总分 +400；`elo-rating` 2000/1800/K=40/5局 ⇒ +48.1 / 9.61 / 76.0% / 2048；`go-territory` komi=0.5 且黑白对调 ⇒ 65.0 / 42.5 / +22.5 / 领先 22.5 目；`gomoku-forbidden` overline+6 连 ⇒ 专属句「黑棋形成6连（超过五连）…」）。`chess/xiangqi-endgame` 保留 `no_inputs`（结构性不可注入，见 §10.5）。**遗留**：`chemistry/mass-to-moles` 原 `inputs{m:18,M:18}` 里 `M=18` 本就 ≠ 页面默认 18.015 ⇒ 判别器原本已检，本批一并改成显式非默认并补全复算。

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
| **复选框 / 单选组 / 点击注入字段（2026-09-24 起）** | `checkIds: ["c","u"]` → `getElementById(id).checked`（纯复选框量表页）；`radios: { htn: "1" }` → `getElementsByName(name)`；`c.checks` → `querySelector(':checked')`/`querySelectorAll('…checked')`（声明「已选中项」的 value，即页面 `input[name=x]:checked` 的返回值）；`clicks: ["pick(0,3)", …]` → 页面作用域执行（BATCH91，命中即 `via="click"`，配套动态 DOM 登记）。四者均已获 `selfcheck`（算有效注入）与 `discriminate`（清空注入即模拟失败）识别 —— **注意 `checks` 的识别口径较窄（BATCH93 起）：仅在「无 inputs」分支计入 `no_inputs` 判定，不参与 `all_default` 判定**（它可能只是 inputs 的修饰项），保持既有口径逐字节不变 ⇒ 纯 checkbox 量表页 / `innerHTML` 点击型页面**不再判结构性 `no_inputs`**。**被 checkbox 门控的页面仍可改判「门控前的派生量」** |
| **HTML 默认选中态已生效（2026-09-24）** | `querySelector(':checked')` / `querySelectorAll('…checked')` / `getElementsByName` 在用例未声明 `c.checks`/`c.radios` 时**回落页面 `checked` 属性** ⇒ 默认输出与真机一致（曾使 `optical/progressive-corridor` 抛 TypeError）。**选批注意**：① 新用例优先**显式声明** `checkIds`/`radios`，勿依赖默认态；② 旧 expect 若曾建立于「默认未选中」的失真输出上会失配（本次全量扫描仅 `cardiology/aortic-dissection` 一例，已重写） |
| **动态 id（`q0..qN`）会同时骗过两道静态校验** | `discriminate_check` 判「跳过」、`selfcheck` 判 `null` 不计入 → **基线会「虚降」**。须自建探针补验「注入 PASS + 回退默认 FAIL」，并另用浏览器真实默认值再跑一遍 |
| **表单控件位于 deep-dive 之后 / 页面存在重复 id（2026-09-24 已修）** | `discriminate_check.pageDefaults` 按 `<!-- TOOLBOX-DEEP-DIVE -->` 截断，而全站 **72 页**的表单控件在该标记**之后**（如 `engineering/heat-transfer` 的 input 在第 235 行、标记在第 178 行）⇒ 取不到任何默认值 ⇒ 所有键都无法回退 ⇒ 整例静默判「跳过」，而这些用例其实带真实注入。多页签页还普遍存在**重复 id**（同 id、不同 value），旧版循环覆盖取到**最后一个**，而浏览器 `getElementById` 取**第一个** ⇒ 默认值失真、`usable` 误判 false 又跳过。已修正为「截断后无控件则回退全文」+「首次出现优先」（input/select/textarea 三处同步），据此暴露 5 个被掩盖的真逃生项 |
| **只改「与当前页签无关」的输入键不算去默认化** | 多页签页里 `v1`（属「稀释」页签）、`r`（属「电位器」页签）之类改了也白改 —— 默认页签的输出纹丝不动，用例仍是 `all_default`、仍被跳过。**必须改真正影响当前页签结果的键**（如 mixture-ratio 改 `ca/ma/cb/mb`、voltage-divider 改 `vin/r1/r2`） |
| **材料 / 形状类页靠 `getElementsByName('material')` 单选组 + innerHTML 模板生成控件** | 不注入 `radios:{material:N}` 时 `calc()` 直接抛错（reading `dens` / `E`）⇒ 看不到任何结果，极易误判为「页面真缺陷」，**实为桩盲区**（`engineering/material-calculator`、`engineering/stress-calculator`）。注入 radios 后计算正常，且 radios 使 `usable=true`，判别器即可正常校验 |
| **无 value 的 input 已被判别器覆盖（2026-09-24 起）；textarea / 动态 id 仍需自建探针** | 旧版 `discriminate_check.pageDefaults()` 对无 `value` 属性的 input 直接丢弃 ⇒ 该键无法回退 ⇒ 整例判「跳过」而漏检；现按真机口径登记为**空串**（与 `runCase` 的 `defaults/sel` 一致），据此暴露并修掉 5 个存量逃生项（另 1 个 `legal/court-fee` 为 checkbox 假阳性，已按 type 跳过）。`<textarea>` 与动态 id（`q0..qN`）仍不解析，须自建同口径探针补验 |
| **零参 `setXxx()` 兜底会「改写状态后重算」，产出的串与注入无关**（原缺陷 B 的实操面） | `pets/kennel-space` 的 `selectSize()` 无参被调用时 `currentSize=undefined` → `\|\| sizes[0]` 落回**小型犬**，于是「小型犬值」16.0/36.0 恰好与兜底输出重合 = 逃生项（本例首版即踩坑）。**定 expect 前必须想清：零参调用该页所有 `set*`/`select*`/`setType` 后最终态会算出哪一组值，expect 必须避开它** —— 首选页面**默认选择项**（本题中型犬 24.0/61.5）派生的值。`DESTRUCTIVE` 正则已补 `^set[A-Z]`，但**仍覆盖不了** `selectSize` 这类「名含 set 却不以 `set[A-Z]` 开头」的设值函数 |
| **`inputs` 为空 / 缺失的用例，判别器一律「跳过」（`checks`-only 已于 BATCH93 开闸）** | 即使 `checkIds`/`radios`/`checks` 也全空也一样跳过 ⇒ **`no_inputs` 弱用例的逃生项判别器兜不住**，只能靠 `selfcheck` 的数量棘轮 + 人工核查。**BATCH93 起 `checks`-only 已并入适用性判定**（`berg-balance-scale`/`flacc-scale`/`mmse-scoring`/`mmt-grading` 四例已能送检并变红）。`music/sheet-music` 即此类：页面无任何 input/select/checkbox（调号条是 `innerHTML` 生成的 `span+onclick`，属 §7.1 保留项），**结构性不可注入**，只能断言初始化渲染串并继续留在 `no_inputs` 基线内 |
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
| **三类结构性不可注入形态（2026-09-24 归纳；① 已按 BATCH91 修订）** | ① **需点按钮写 localStorage 的页**（`cleaning/appliance-cycle`「记录今日」、`cleaning/cycle-20`「添加地毯」）：harness **现已有 `clicks` 字段**（BATCH91），但点击只写 localStorage（harness 无实现）、且 `setLastClean` 之类被 `DESTRUCTIVE` 的 `^set[A-Z]` 排除 ⇒ 注入/点击对**渲染输出**仍零影响（实测 appliance-cycle 换 checkDate 2024-06-15↔2020-01-01 输出完全一致），只能维持 `no_inputs`；② **id 由 JS 模板拼接的页**（`checker-10` 的 `a{区}_{项}`、`checker-9` 的 `m{模块}_{项}`）：注入有效，但 HTML 源码无字面 id ⇒ `discriminate_check` 取不到默认值、判「跳过」，须用同口径双态 dump 人工确认；③ **输入值回显型断言**（`cycle-20` 的 expect 锚 select 的 value）：计算结果根本不变，属已知弱断言，须在 `ref` 里写明、不得计入判别力 |
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
| **按钮驱动的交互页在静态 HTML 里 0 控件 ⇒ 结构性不可注入（2026-09-24 dermatology 批；BATCH91 起有解）** | `dermatology/contact-dermatitis-patch`（14 个过敏原卡片由 `renderGrid()` 拼 HTML、反应强度靠卡片内 `<button onclick="setReact(...)">` 写 `selections`）、`miliaria-classification`（`selectType(btn,idx)`）、`wood-lamp`（`selectFluor(btn,i)`）三页的 `input/select/textarea` 计数**均为 0** ⇒ harness 既无可注入控件、按钮又不在 `elements` 表内 ⇒ 只能渲染默认串。**选批前先预筛**：`grep -cE '<input|<select|<textarea' tools/<ind>/<slug>.html` 为 0 即结构性不可注入，保留在 `no_inputs` 基线并在 `ref` 写明理由。**BATCH91 起有了出路**：这些按钮由 `clicks` 传入登记元素即可驱动（如 `clicks:["selectType(document.querySelectorAll('.type-btn')[0],0)"]`，动态 DOM 登记提供 `querySelectorAll`），归 P3 顺带处理 |
| **`grade` 由 `selectGrade(btn,g)` 点击改写 ⇒ harness 里恒为默认档（2026-09-24）** | `dermatology/chilblain-grading`（`var grade=1`）与 `hdss-hyperhidrosis`（`grade=2`）的严重度分支只能点按钮改，而 `selectGrade()` 无参调用会在 `btn.classList` 抛错 ⇒ **grade 派生文案（I 级建议、20% 氯化铝建议）在注入前后完全一致**，以其为 expect 即默认命中（逃生项）。可注入点只剩 checkbox 派生的「受累部位 / 分型提示 / 警示」三串。**定 expect 前先确认目标量能否被 input/checkIds 触达**：不能则换锚点 |
| **`render()` 用 `.length` 判空但入参是对象 ⇒ 整页功能恒空（P0 真缺陷，2026-09-24 travel 批）** | `travel/travel-adapter-guide` 的 `render(list)` 写 `if(!list.length)`，而 `plugs` 是**对象**、`filter()` 也传对象 ⇒ `undefined` 恒真 ⇒ 修前无论搜索什么都只显示「未找到」，默认态亦然（原 expect 正是这个「未找到」＝ 缺陷与逃生项双重命中）。改 `if(!list||!Object.keys(list).length)` 后搜索生效。**启示**：`Object.entries(list)` 遍历 + `list.length` 判空混用是高频真缺陷；遇「整页功能恒定不工作」的弱用例，先怀疑判空/类型错，别急着归类为「不可注入」 |
| **有 id 的控件注入后输出逐字不变 ⇒ 仍属结构性不可注入（2026-09-24 travel 批）** | `travel/packing-list` 有 `input#tripName`/`input#tripDate`（判别器不会判「跳过」），但渲染主体 `renderList()` 只读 `currentData.categories`，`tripName` 仅在 `saveList()` 写 localStorage 时使用，而 `saveList` 不在 harness 兜底调用序列内 ⇒ 注入 tripName=测试行程A 后 blob 与默认态逐字一致。**判据**：控件的处理函数是否在 harness 实际调用链上；不在 ⇒ 输出无关，保留 `no_inputs` 并在 `ref` 写明（与 estimate-reserve / contact-dermatitis-patch 同类） |
| **selfcheck 全站 `--exec` 会崩（历史现象，勿误判为本批引入，2026-09-24）** | 结尾抛 `TypeError: process.exit is not a function`（某页脚本污染全局 process），且顺带打印数百条 `default-hit`。**取基线请用结构模式** `node scripts/selfcheck_false_pass.js scripts`（与门禁第 216 项同口径，risk=0），只看 no_inputs/all_default 计数行；`--exec` 仅供单文件调试。已用 `git show HEAD:<file>` 对照复现，确认与当批改动无关 |
| **无参 `loadXxx()` 兜底预设会把「可注入页」伪装成「不可注入」（2026-09-24 endocrinology 批）** | `runCase` 顺序是：① 注入 inputs + 触发 input/change/keyup → **立即**检查 expect（命中即 `via="input event"`）；② 未命中才兜底**遍历无参调用各函数**（跳过 DESTRUCTIVE）。而 `endocrinology/*` 这类页普遍带 `loadNormal()/loadMS()/loadDM()/loadPCOS()` 预设函数，会把输入**全部改回预设值**并重算 ⇒ **用占位 expect 做 blob dump 看到的是兜底后状态**（与注入无关），极易误判为「注入无效 ⇒ 结构性不可注入」 | 判据必须看 **`r.via === "input event"`**（本批 7 例全部如此）；标准流程：读页面 `calc()` 渲染模板构造 expect（如 `arr.toFixed(1)` + 标签）→ 测注入态（期望 ok 且 via=input event）→ 测默认态（期望 not ok）→ 最后避开 `loadXxx` 预设值（`metabolic-syndrome` 的「满足 5 / 5 项标准」、`ogtt-interpretation` 的「1h： 11.5」「2h： 9.2」都是预设产出，作 expect 即逃生项） |
| **兜底无参「联动函数」会把注入值回写覆盖（`onMediumChange` 型，2026-09-24 glass 批）** | 与 `loadXxx()` 同源但更隐蔽：页面把 select 联动写成长度可控的无参函数（`glass/snell-refraction` 的 `onMediumChange()` / `onMediumChange2()` —— 从 `m1`/`m2` 的 value 回写 `n1`/`n2` 后 `calc()`），函数名不匹配 `DESTRUCTIVE` ⇒ 落入第 ② 步兜底调用序列，**在注入判定之后**把 n1/n2 覆盖回 select 首选项（1.0003 / 1.0003）。⇒ 用占位 expect 做的 blob dump 会显示「注入值未生效」，极易误判为「结构性不可注入」。**判据同上行**：只看 `r.via === "input event"`；expect 只要在注入阶段命中即成立。选值优先锚「联动函数不会产生的」数值（本批 `41.15°` 全反射临界角即默认态不可达） |
| **「数值巧合型」逃生项：默认态与注入态算得同一个百分比（2026-09-24 manufacturing 批）** | `manufacturing/production-efficiency` 首版 expect 写了「合格率 (Quality) 95.0%」—— 默认 475/500 = 95.0%、注入 570/600 **也** = 95.0% ⇒ 该串在两态都在 blob 里，`discriminate_check` 直接报「仍 PASS 1 例」。| **凡 expect 是百分比/比率/均值类同量纲指标，必须先逐项算「默认态 vs 注入态」是否同值**；同值即零判别力（与「等级词同档」同源，只是从等级词扩展到数值）。改锚 OEE 56.5%（默认 49.5%）后 5/5 全红 |
| **静态词表页：锚「行内容」必成逃生项（2026-09-24 medical2 批）** | `medical2/medical-abbrev` 首版 expect 写了 `qd quaque die 每日一次 医嘱`（搜索 qd 的唯一命中行）—— 但该页**默认空关键词即渲染全部 96 条**，该行在默认态同样在 blob 里 ⇒ 「expect 任一命中即 PASS」立刻判逃生（discriminate 报「已检 4 / 变红 3 / 仍 PASS 1」）。| **凡是「默认渲染全表、搜索/筛选才缩小」的页面，绝不可锚任何行内容**（全表必含所有行）；只可锚**随检索词变化的计数**（本批改锚「1 匹配结果」，默认态为「96 匹配结果」）。同理 `selfcheck --exec` 也会用「页面默认值」跑一遍，提前暴露该类问题 |
| **click 驱动型量表页（`innerHTML` 渲染 + `pick(i,j)`）已可注入（BATCH91，2026-09-24）** | 这类页（`psychiatry` 24 例里 18 例、`tcm-diagnosis` 同类）静态 HTML 里 `input/select/textarea` 计数为 **0**，题目与选项由 `render()` 拼 HTML 写进 `#quiz`（`<span class="q-opt" onclick="pick(i,j)">`），答题态只存在于页面内存数组（`var A=new Array(QS.length).fill(-1)`）。harness 新增 **`clicks: ["pick(0,3)","pick(1,2)",…]`**（在 inputs 注入之后、兜底之前按序执行，命中即 `via="click"`；**BATCH92 起改为「页面作用域 direct eval」`__pageEval`，见本表后续行**）＋ 用例级「**动态 DOM 登记**」（`innerHTML` setter 按容器 id 分桶解析 `{tag,id,class}`，同容器以**最后一次渲染为准**；`querySelectorAll` 从登记表回填 ⇒ `pick()` 内 `its[i].querySelectorAll('.q-opt')` 与 `classList.toggle` 不再抛错）。**以 `DYN.on` 开关隔离**：仅当用例声明 `clicks`/`dynDom` 时启用，其余 3143 例行为逐字节不变 —— 由此绕开 2026-09-23 全站无差别 `id` 注册误伤 `psychology/calc-12` 的坑。**判据**：`r.via === "click"`；`selfcheck`（`weakKind` 的 `hasInjection`）与 `discriminate_check`（`hasInj`/`clearInject`）均已识别 `clicks`（否则被误判 `no_inputs` 推高基线致门禁红） |
| **兜底零参调用「作答函数」会把点击态覆盖成未作答 ⇒ expect 必须点击后立即判（`via=click`）（2026-09-24 BATCH91）** | `psychiatry/mdq-bipolar` 的 `pickP2()`/`pickP3()` 名不匹配 `DESTRUCTIVE` ⇒ 落入兜底零参调用序列，把 `P2`/`P3` 写成 `undefined`，使**最终 blob 显示「未满足」态**（覆盖点击注入）。⇒ 与 `loadXxx()`/`onMediumChange` 同源：**expect 只在 `clicks` 执行后立即判定（命中即 `via="click"` 返回），不看最终 dump**；判据只看返回的 `via` |
| **`"不满足"` 含 `"满足"` 子串 ⇒ 子串匹配型 expect 不可锚「正向判定词」（2026-09-24 BATCH91）** | `blob.includes(want)` 是**子串**匹配：`mdq` 若锚 `"满足 标准N"`，则显示「**不**满足」时也命中（`不满足` ⊃ `满足`），零判别力。**凡结论词有「否定式包含肯定式」的（满足/不满足、达标/未达标、符合/不符合、有效/无效…），一律锚完整结论串**（本批改锚 `"三条标准同时满足"`），或锚派生数值/计数 |
| **`clicks` 已升级为「页面作用域 direct eval」（BATCH92，2026-09-24）** | BATCH91 的 `clicks` 走全局 `new Function`，只能调到**已导出到 globalThis 的函数**；而 harness 的 `expose` 只导出 `function` 声明 —— 页面顶层 `var`（`selLoc`/`selNat`/`ausData`/`checked`/`selected`/`sel`/`answers`/`currentNature`/`userAnswers`…）**够不到**，故 `tcm-diagnosis` 这类「状态在 var 里」的页无法驱动。BATCH92 在编译期追加 `__f["__pageEval"]=function(c){return eval(String(c));}`，`clicks` 改走它 ⇒ 作答代码在**页面作用域**执行（页面作用域是全局的**严格超集**，`pick(0,3)` 型用例行为不变，已回归 psychiatry 24/24）。**判据仍是 `r.via === "click"`**；`selfcheck`（`hasInjection`）与 `discriminate`（`hasInj`/`clearInject`）均已识别 `clicks` |
| **「列表默认全渲染 + `#result` 仅交互后填充」页面的 expect 唯一可取源（BATCH92，2026-09-24）** | `tcm-diagnosis` 13 页均为「初始化渲染整张卡片/网格，点击或分析后把详情写进 `#result`」⇒ **默认 blob = 列表本体**，任何「卡片内文本」（name/desc/brief/area/nature）作 expect 必为**常量型逃生项**（旧 14 例 expect 全栽在此：`auscultation` 的「说话声音低沉断续」是列表 `desc`、`zang-fu` 的「心脉痹阻」是卡片名、`san-jiao` 的「温邪犯肺或逆传心包」是 `brief`、`meridian` 的「肩臂内侧前缘」是卡片 `area`、`formula-matching` 的「全部」是分类 chip 文案）。**唯一安全源 = 只由 `showXxx()`/`analyze()`/`derive()`/`simulate()`/`showSyndrome()` 写入 `#result` 的字段**：`symp`/`nature`/`detail`/`effect`/`usage`/`formula`/`treat`/`points`/`route`。校验法同「双 dump 对比法」：注入态含、默认态不含 |
| **`confirm` 未实现 ⇒ 未答满的 `calcScore()` 静默早退（BATCH92 `constitution-test`）** | 页面 `calcScore` 在 `unanswered>0` 时 `if(!confirm(...))return;`，而 harness 未提供 `confirm` 桩（`alert` 有、`confirm` 无）⇒ 抛 `confirm is not defined` 被兜底 catch ⇒ 结果区恒空。**对策**：`clicks` 先把全部题目填满（`constitutions.forEach(...answers[...]=5...)`）使 `unanswered===0` 走主路径。**通用提醒**：页面若用 `confirm`/`prompt` 做闸门，harness 下必须绕开该闸门（填满/预置状态），不要指望弹窗桩 |
| **量表页控件运行期渲染 ⇒ 判别器取不到默认值、仍计 `skip`（BATCH93，2026-09-24）** | `rehabilitation/asia-impairment-scale`（`renderSensory()/renderMotor()` 拼 `<select id="sens_C2_lt_l">`）、`fim-scale`（`'fim_'+idx`）、`dentistry/gingival-index`/`rater-risk-2` 的控件与 id **全在运行期 `innerHTML` 里生成**，静态源码 grep 不到 ⇒ `discriminate_check.pageDefaults` 拿不到「默认值」⇒ 无法模拟「换回默认 ⇒ 失配」⇒ 用例被判 `skip`（**不是**用例弱，而是判别器盲区）。**对策**：这类用例必须用「注入态 PASS / 默认态 FAIL」**双跑手工核验**（清空 `inputs/checks/clicks` 后 expect 必须失配），并在 `ref` 写明；本批 12 例默认态**全数 FAIL**。**勿**为它们改页面加静态控件（属改动线上已验证内容） |
| **旧 expect 锚在「桩假象 NaN」上（BATCH93 `asia-impairment-scale`）** | 该页原 expect 是 `「NaN/112」`：`sel` 映射只扫**静态源码**的 `<select>`，而本页下拉是运行期生成 ⇒ `getEl(id)` 回落空串 ⇒ `parseInt('')=NaN` ⇒ 桩下默认态恒为「感觉总评分 NaN/…」。**这是桩的产物、不是用户可见值**（真机默认 option「2-正常」带 `selected` ⇒ 显示 224/112）。⇒ **凡 expect 含 `NaN`/`Infinity`/空串提示者，先判「真机是否也会这样」**；多用「隔离器 dump 真机默认态」交叉验证。**本批由此顺带发现并修掉 1 个 P0 量纲错**：感觉总评分分母 `/112` 应为 `/224`（28 皮节×4 位点×2 分），真机默认态原显示 224/112（率>100%） |
| **按钮驱动 + 顶层 `var` 状态：`clicks` 直接写状态比模拟点按钮更稳**（BATCH94 `ent` 7 页） | 该批页面题面/选项全是 `<button onclick="selectGrade(this,g)">`，驱动函数第一步就 `btn.classList.add('active')` ⇒ `clicks` 若传 `null`/伪元素会抛错；而**真正被 `calc()` 读取的只是页面顶层 `var`**（`grade`/`scores`/`sel`/`selections`）。`clicks: ["grade=5;calc()"]`、`["scores.G=3;scores.R=3;…;calc()"]`、`["sel.mobility='固定';sel.position='中间位';calc()"]` 一行驱动到底且不受 DOM 桩限制 | **判据**：先看 `calc()` 读的是「DOM 选中态」还是「顶层 var」；是 var ⇒ `clicks` 直接赋值（**无需**动态 DOM 登记，`dynRecord` 只是给 `querySelectorAll` 兜底不抛错）。`expect` 仍锚**非默认分支**的 advice/特征串（原 expect 全是默认态常量：`0-12`/`(89%)`/`2级`/`总评(0-3)`/`24`/`声带运动功能正常`） |
| **扣分型评分未做下限截断 ⇒ 可渲染负分与负百分比**（BATCH94 `ent/eustachian-tube`） | 该页 `adjustedScore = total - symptomCount`：客观检查最小 0 分（B型 + 4 项「0」），症状按钮 9 个各扣 1 ⇒ 全选时 `adjustedScore = -9`，页面渲染出「评分 **-9** / 18」与「咽鼓管开放程度 (**-50%**)」——**有界量越界**（分数/百分比不得为负）。`copyResult()` 里同一算式也需同步改 | 改 `Math.max(0, total - symptomCount)`（`calc` 与 `copyResult` 两处）。**通用**：凡「基础分 − 扣分」式页面，先算**最小值**是否越界；百分比类一律核 `[0,100]`；越界即公式/守卫缺陷，按 P0 修页面 |
| **校正型公式的「加/减」必须与本页文案方向一致（BATCH95 `ophthalmology/calc-1`）** | 该页 `corrected = iop + ((cct−544)/10)*0.7`：角膜越厚校正值**越高**，但同页第 181 行与第 111 行 formula-eq 都写「CCT 越厚，实测眼压往往被**高估**」（即真值应**低于**实测）、深度解析示例也标「厚角膜略高估」——**代码与自家文案自相矛盾**；姊妹页 `tools/ophthalmology/iop-correction.html` 的 Ehlers(520−cct)/Doughty(542−cct)/Feltgen(550−cct) 三种标准式**一律是减号**（厚角膜下调）。 | 改为 `iop − ((cct−544)/10)*0.7`（示例随之由 19.12/14.92 变为 16.88/21.08）。**通用判据**：凡「校正/补偿/折算」型页面，先问「物理方向对不对」，再**拿同站姊妹页或权威公式交叉验证符号**；改页面后必须同步 **①生成器脚本 ②`content_deepdive.json` ③`guides/*-guide.html`**（本页三处都有同一算式，只改页面会被下次构建覆盖）。另：命名须与真实参数相符——544μm/0.7 并非 Doughty 原始参数（542μm/0.020），已由「Doughty 线性法」正名为「线性校正法」 |
| **`inputs` 与页面默认值逐字相同 = 零判别力，判别器静默跳过**（BATCH95 `ophthalmology/visual-fatigue-vas`） | 该例 `inputs{vasSlider:"5"}`、页面 `value="5"`，`all_default`（selfcheck 已计）却**从未被判别力校验**：`discriminate_check` 换回默认时发现「注入值本就等于默认值」⇒ `usable=false` ⇒ **直接 `skipped++`**。其 `expect「从不(0)」` 是问卷选项标签文案，纯常量型逃生项，`escape` 棘轮完全看不到 | 改 `inputs{vasSlider:"8"}` + `checks:["3"]` + `clicks:["calc()"]` ⇒ 76/110「重度」。**通用**：①改弱用例前先看 `all_default` 名单（不是只有 `no_inputs` 才是弱用例）；②`calc()` **只由按钮 onclick 触发**的页面（`range`/`select` 的 `oninput/onchange` 只更新显示值）必须 `clicks` 驱动，否则结果区永不刷新、expect 只能落在静态 DOM 上；③判别器 inputs 分支**同时清空 checks/clicks** ⇒ 这类混合注入例仍能正确变红（本例由 `skipped` 转入 `checked`） |
| **运行期渲染的 `<select>` 用 `clicks` 赋值，不要写 `inputs`（BATCH96 `beauty` 4 例）** | `checker-14`/`checker-assessor-1`/`checker-assessor-2`/`assessor-risk-12` 的 select id（`d{di}i{ii}` / `stage+i` / `key+i` / `c{i}`）由 `buildList()` 拼 `innerHTML` 生成，静态源码 grep 不到 ⇒ 若写 `inputs`：`discriminate_check.pageDefaults` 找不到这些 id，「换回默认」无从谈起 ⇒ `usable=false` ⇒ **整例静默 `skip`**（用例其实有真实注入，只是判别器看不见）；`selfcheck.weakKind` 也因 `defs[k]===null` 直接返回 null（不计入基线）。 | 改用 `clicks: ["…document.getElementById('c'+i).value='2'…;calc()"]` —— `clicks` 在页面作用域执行，`getElementById` 按需造出带注入值的元素并记忆化，`calc()` 读到的正是这些值；判别器清空 `clicks` 后各控件回落空串 ⇒ 必然变红。**判据**：静态 `<select>` 计数为 0 但页面用 `getElementById(动态 id).value` 读值 ⇒ 走 `clicks`。`beauty` 文件判别力由此从「已检 13 / 跳过 8」变为「已检 **21** / 跳过 **0**」 |
| **expect 锚在 else 兜底分支 ⇒ 被零参兜底破坏态复现（逃生项）**（BATCH97 `clinical-nursing` 3 例） | `barthel-index`/`braden-score`/`morse-score`/`pain-nrs` 这类「分数存顶层对象 + 阈值 `if/else`」页，**兜底阶段的零参调用会先把状态算坏**：`selectScore(undefined,undefined)` 使 `scores[undefined]=undefined` ⇒ `total=NaN` ⇒ `NaN>=19` / `NaN<25` 等比较**全 false** ⇒ 落入最后的 `else`（最高严重度）；`getLevel(undefined)` 因 `undefined<=各 max` 均 false ⇒ 返回 `labels[last]`（重度）。故「清空注入」的破坏态与 else 分支文案**逐字相同**。 | 去默认化时**目标必须落在非兜底的那一路**：braden 取 total=13 走「中度风险」的 `每2小时翻身一次`、morse 取 35 走「低度跌倒风险」的 `保持病区环境安全`、pain 取 `selectPain(2)` 走「轻度疼痛」的 `可考虑非药物干预`；三条锚点均先 `grep` 静态 HTML 确认零出现。**判据**：expect 若在「默认态 + 零参兜底态」任一态也会命中 ⇒ 无判别力（改后默认态 8/8 FAIL 才算过）。另：`selectPosition(pos, btn)` 第二参需带 `classList`，`clicks` 里传哑对象 `{classList:{add:function(){}}}` 即可 |
| **纯浏览页无输出容器 ⇒ 结构性不可注入（BATCH92 `etiology-tree`）** | `tcm-diagnosis/etiology-tree` 只有 `treeContainer` 一个容器、无 `#result`；节点由 `buildNode()` 渲染（初始化即全部进 blob），交互只有 `classList.toggle('expanded')`（class 变化**不进 blob**）与 `copyTree()` 写剪贴板（`ToolBox.copyText` 桩无实现）⇒ **不存在任何随输入变化的输出**。⇒ 维持 `no_inputs` 并在 `ref` 写明（与 `music/sheet-music`、`cleaning/appliance-cycle` 同类） |
| **`createElement + appendChild` 建行 ⇒ `querySelectorAll` 遍历型页面结构性不可注入（BATCH99 `admin/detector-time`，2026-09-24）** | 日程行由 `addRow()` 用 `document.createElement('div') + #rows.appendChild(div)` 建立，`detect()` 靠 `document.querySelectorAll('#rows .input-row')` 取值。桩的 `dynRecord` 只把 **innerHTML 字符串里解析出的标签**登记进 DYN（`<input>`/`<select>`…），**不含容器 div 自身** ⇒ 该选择器恒返回空。实测 `clicks:[addRow({name:'甲',…});addRow({name:'乙',…})]` 后仍是「共 0 个有效日程」。#rows 的 innerHTML 因 `appendChild` 拼接而含全部表单标签（blob 里能看到 6 行「会议名称 日期或星期…」），**极易误判为「行已建好」**。 | **判据**：驱动语句是 `querySelectorAll('#容器 .行类名')` 且行由 `createElement`（而非 innerHTML 拼串）生成 ⇒ 结构性不可注入，保留 `no_inputs` 并在 `ref` 写明（比照 `tcm-diagnosis/etiology-tree`）。 |
| **FAIL 的 `fullBlob` 是「兜底后」视图 —— 不能用来判断 clicks 是否生效（BATCH99，2026-09-24）** | `clicks` 执行完若 expect 未命中，程序继续进入阶段 3（无参遍历调用候选函数），`render()`/`calc()` 会把结果区**重写回默认值** ⇒ FAIL 打印的 blob 与默认态逐字相同。本批 `admin/meeting-conflict`（clicks 里重写 events + `renderList();render()`）与 `checker-manager-training-hr` 都因此被误判为「clicks 未执行 / 页面不可注入」，白查近一小时。 | **正向判据**：临时把 expect 换成**标记串**跑一次 —— `clicks:["document.getElementById('stats').value='MARK_V'"]` + `expect:["MARK_V"]`，命中即证明写入路径通（本次对 `value`/`innerHTML`/`ToolBox.setResult` 三路均 OK）。**推论**：clicks 型用例的 expect **必须在阶段 2.5 内命中**，否则结果区被兜底覆盖、永远 FAIL —— 这既是坑也是保护（判别器正靠它变红）。 |
| **「范围 / 越界 / 警告」类提示语先算默认态是否也触发（BATCH99 `archaeology/site-grid`）** | 首版把越界提示「部分探方超出遗址范围，请核对尺寸」当专属锚点，但默认 `len=60` 时 `nL=12` ⇒ `siteLen = 12×5+11×1 = 71 > 60` ⇒ **默认本身就越界**、同样落该分支 ⇒ 默认态 `via=calc` 逃逸（判别器正确变红但 expect 已零判别力）。同源坑还有 `supplies-forecast` 的「月均/最高/波动范围」（只由顶层常量 `data` 决定）、`travel-subsidy` 的「出差天数 / 住宿限额」（只由常量 `trips` 与城市档位决定）—— 都**与注入字段无关**。 | **判据**：锚分支提示语前，先按**默认参数**手算一遍是否落同一分支；凡只由页面顶层常量派生的量一律不锚（BATCH98「锚点在默认态命中即零判别力」的延伸）。改后 `site-grid` 只锚「60 探方总数 / 2260.0 隔梁面积 m²」，默认态正确 FAIL。 |
| **dump 探针：`clicks` 内把结果回写到独立元素（BATCH100，2026-09-24）** | 承接 BATCH99「FAIL 的 blob 是兜底后视图」：要拿某页在**注入态**下的真实输出，最省事的做法是在 `clicks` 末尾加一句回写 —— `clicks:["calc();document.getElementById('__p').value=document.getElementById('result').innerHTML"]`（多容器就 `+'|'+` 拼接）。兜底阶段只重写 `result`/`dataGrid`，**不碰 `__p`** ⇒ 即便用例 FAIL，`fullBlob` 里仍含真实注入输出。 | **用法**：定新 expect 前先跑一次 dump 探针（expect 写 `__PROBE__`），一次拿全所有结果区文本；`__p` 的写入走 `value` 通道（`collectStrings` 读 `el.value`）。比「逐个试 expect + 看 OK/FAIL」快一个数量级（BATCH100 的 7 例一次到手）。 |
| **等级词/规则名常被静态说明表命中，须改锚分支专属句（BATCH100 `chess/gomoku-forbidden`）** | 该页等级词「长连禁手」在**静态规则说明表**里出现 **6 次** ⇒ 无论注入什么都会命中，零判别力；原 expect「结合实际棋盘分析」更是**页脚常驻免责文案**（`* 本工具提供基础禁手判断参考…`）＝常量型逃生项。 | 改锚子分支专属句「黑棋形成6连（超过五连），违反长连禁手规则。黑方判负。」（`grep` 确认 static=0）。**通用**：定锚前把候选串逐个 `grep -c` 静态 HTML（去掉 `<script>`），凡是「等级词 / 规则名 / 单位 / 免责声明 / 参考标准表头」一律先验静态出现次数（BATCH99 的 `sports/estimate-tester` 与 `medical2/medical-abbrev` 同源）。 |
| **隐藏面板内的控件注入无效（BATCH98 `hvac/duct-calculator`，2026-09-24）** | 页面把圆形风管的 `diaD` 放在默认 `display:none` 的 `circleInputs` 面板里。实测 `inputs{diaD:"600"}` 与 `clicks:["document.getElementById('diaD').value='600';calc()"]` **都改不动** `calc()` 读到的值（输出恒 `Φ 500 mm`），而同一批注入的 Q/v/rho/L/xi 全部生效 ⇒ **注入阶段与 calc 阶段不是同一份 DOM 实例**，静态 HTML 里的 `value` 才是 calc 实际读到的。 | **判据**：改了某控件的值、对应输出量却纹丝不动（尤其该控件位于 hidden/tab 面板内）⇒ 改锚**只由已验证可注入字段派生**的量（本页 F_req = Q÷(3600×v)）。`clicks` 不是万能解 —— 只在「赋值与读取同一份 DOM」时有效。 |
| **expect 必须避开「任何无参函数调用」能产出的串（BATCH98，2026-09-24）** | harness 兜底阶段会**无参遍历调用**页面候选函数（`DESTRUCTIVE` 正则跳过 reset/clear/save/swap）。`hvac/duct-calculator` 的 `suggestSize()` 与 `hvac/pump-calculator` 的 `calc()` 被无参调用后照样渲染出完整结果区，其中「建议调整风管尺寸」与目标锚点同形 ⇒ 默认态（清空注入）仍 PASS。 | 去默认化必须**实跑默认态核验**（本例首版两条 expect 均被兜底命中）。**判据**：用「仅含 expect 的 JSON」跑清空注入态，**必须全 FAIL**；锚点优先选「零参调用会先写坏状态而落其它分支」的量（BATCH97 的非 else 分支文案）或只由输入直接派生、兜底无法复现的量。 |
| **verify 用例文件存在「同 slug 多份」历史残留（2026-09-24 全站实测）** | 全站 **16 个** `verify_*_calc.js` 共 **62 条多余条目**（`realestate` 12、`math` 14、`science` 5、`ai` 4、`agriculture` 3…），其中 **61 条两份内容不同**（早期「收口」批建例、后来「精查/缺陷修复」批又为同一 slug 追加新例，写入前未查重，`git log -S <slug>` 可逐条定位）。影响：① 门禁 verify 会把同一页面跑两遍（`checked=3161` 内含 62 条重复）；② `selfcheck`/`discriminate` 计数虚高；③ **批量替换器按 slug 定位时会同时改掉两份**（BATCH98 agriculture 即如此）。 | 暂不清理（删条目会同时改动 `total_cases`/`checked`/`skipped` 三个基线数，属独立批次）。**工具侧**：`patch3.py` 的 slug 正则只认带引号的 `"slug":`，遇无引号 `slug:` 风格的文件会**静默不命中**并吃掉块前导注释的空格与横线填充（BATCH98 agriculture 曾误伤 5 条注释 + 10 处缩进，已用 HEAD 原文整行修复）—— 换文件前先 `grep -c '"slug":'` 探格式。 |

### 10.6 方向1：公式-脚本一致性精查（**全量闭环** · 老板选定）

- **目标**：逐页独立复算计算类页 `calc()` 输出的数学/物理正确性（与标准公式/权威向量比），找"用户拿到错钱数/错物理量"的真缺陷（§4.5 红线第一条最高频事故）。
- **覆盖（已全量闭环）**：10 高热度行业（science / math / geometry / photo / ai / sports / agriculture / finance）+ 金融周边集群（banking/investment/tax/realestate/accounting/insurance/economics/statistics/forex/futures ~334 页）+ 中低热度 113 个行业（页≥15）+ **96 个小行业（<15 页，687 页）**默认态与 ZERO/EMPTY 边界态。边界 NaN 守卫已铺开（4 个待办分类 86 页 + 7 个物理工程行业 194 页）。
- **工具（均在本地，`_*.js` 按 `.gitignore` 不入库）**：
  - `scripts/_audit_iso_small.js` —— 批量隔离器。`node 脚本 <industry,ind2,...>`；`DUMP=1` 另写 `/tmp/iso_small.json`。**不要用「函数名必须含 calc」的窄口径过滤入口**（会漏掉 `compare()`/`update()` 类页，687 页里因此漏审 168 页）；桩需覆盖 `MutationObserver`/`getElementsByName`/`style.setProperty`/`cloneNode`/`insertAdjacentHTML`/`toBlob`/`ctx.*`/`window.X=` 透传 globalThis/`innerHTML` 里 `<select>`+`<option>` 注册。
  - `/tmp/jsdom_probe.cjs` —— **jsdom 真实 DOM 复核探针**（里程碑：不再靠"猜桩盲区"）。对候选页跑 DEF/ZERO/EMPTY 三态，读 `result|grid|card|state|total|detail` 类容器文本，判 `NaN|Infinity`。**判据：隔离器报的 `err` 一律先过 jsdom 复核；jsdom 三态无 NaN/Infinity ⇒ 桩盲区，立排除，不改页。**
- **SOP**：① 隔离器扫 DEF 态 → 筛 `NaN`/`Infinity`/越界值/`err`；② 每条 `err` 过 jsdom 三态复核，区分「桩盲区」与「真缺陷」；③ 确凿缺陷才改页，改完补/改用例。
- **纪律**：确凿真缺陷前不改页面；找到即立项闭环（修 calc + 修/注册 verify 用例 + run_gates + 提交推送）。

