# DEV-PLAN.md — 待处理任务清单

> **本文件为当前主线开发任务清单**：英文态「内容区全量英文化」专项（`en-dev-plan.md`）已全量收口并删除，主线回归本文件。本文件只放「待处理任务」与「干活必须遵守的规则」；已完成项、批次成果、历史操作流水一律不写入（归档走 `.workbuddy/memory/YYYY-MM-DD.md`）。

> **本文件只放「待处理任务」与「干活必须遵守的规则」。已完成项、批次成果、历史操作流水一律不写入** —— 归档走 `.workbuddy/memory/YYYY-MM-DD.md`；历史全量快照另存 `.workbuddy/memory/archive-devplan-full-2026-09-23.md`。
> **⚠️ 体积红线（硬约束）**：`wc -c DEV-PLAN.md` **> 60 KB 即说明有批次流水混入，先清理再干活**。每批收尾**只允许**更新 ① §10.2 的计数行 ② §10.3 的存量数与不可注入清单 ③ §九/§7.1 的**待办增删**；**禁止把「本批处理了哪些例、逐例打法、验证过程」写进本文件**（这些一律进 memory 与 skill）。清理时先把全文快照存入 `.workbuddy/memory/archive-devplan-full-YYYY-MM-DD.md` 再删。
> **收尾口径（老板 2026-09-21 明确）**：闭环 = 本地 build / 门禁通过 + GitHub 部署成功（Actions run success）。**不做线上产物 MD5 落盘比对、不 sleep、不轮询 API**；纯文档类改动（`*.md`、memory）不等部署。
> **状态（2026-09-23）**：全站 209 分类 §4.1 已收口；A 级率 **99.2%**；SEO 与术语内链（1591 页 / 2268 条）已治理；小行业精查已闭环。**当前无进行中批次，待办见 §九。**

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
- **术语内链唯一源 = `_build.py::linkify_terms()`**（§4.1.7）：把 deep-dive 正文里的专业名词链到站内工具页/指南页。术语 = 工具中文名 + 剥通用后缀的核心词（`_TERM_LINK_SUFFIXES`）+ 指南标题去「使用指南」；**目标必须存在且非 `TOOLBOX-REDIRECT` 存根**。细则：逐字符最长匹配、`TERM_LINK_MIN_LEN=3`（「公式」曾命中 844 次）、每目标页每页只链一次、上限 `TERM_LINK_MAX_PER_PAGE=6`、不链自身、ASCII 术语要求词边界（防 `CSS` 命中 `CSS3`）。**禁在页面手改内链**。
- **繁体 `zh-tw/` 是构建产物**：勿手动改（被 `.gitignore` 忽略）；其子树不含 `js/`，引用站内 JS 必须绝对路径 `/js/x.js`。
- **i18n 八件套**：标题/简介走 `_en_override.json` + `slug-en.json`；行业 i18n 走 `i18n/tools/<ind>.json`；凡引 `common.js` 的静态页须引 `i18n.js`。
- **计算函数名不统一**：`calcTool()` / `calc()` / `calcBelt()` 等。抽取时在整个 html 里多候选 `function <name>(` + 花括号配平，勿用 `max(scripts, key=count('calcTool'))`（会选中 stub）。依赖 select 与常量表的工具须先抽 `<select id=...>` 默认项与 `const X = {` 常量表。
- **英文 p 三种机制（改法不同）**：① `data-zh` —— 英文写在源 HTML，改源文件；② 裸 `<p>中文</p>` —— build 用 `<ind>-body.json` 覆盖，**必须改数据源**；③ `data-i18n` —— 由 build 注入，同样改数据源。
- **英文态数据源三处（最易漏）**：`i18n/tools/<ind>-body.json`（title/h1/intro）、`i18n/tools/<ind>.json` 的 `en-US`（同时是 industry JSON 的 `ed` 最高优先级源）、`_en_override.json`（en/ed）。
- **build 预渲染陷阱（最高频事故）**：`_prerender_tool_body` 用 `count=1` 命中文档**首个 `<p>`**，任何插在首个 `<p>` 前的中文 `<p>` 都会被 intro 覆盖。修法：改成 `<div>` 或补 `data-zh`。该函数**幂等**，故改数据源后必须先把页面「还原」再 build。
- **`slug_to_intro` 默认模板恰是审计判定短语**：新增默认文案须避开 `is a free online (tool|...)` / `is available directly in your browser` / `check and validate online` / `Generate results online for free` / `VERB online` 五类指纹（否则审计会把默认文案误判为套话）。
- **英文副标题 p 已英文不重渲染**：`_prerender_tool_body` 对**已是英文**的副标题 `<p>` 不重渲染，故清副标题必须**直接改写 HTML p 内文**（或扩展重渲染逻辑），不能只改数据源。
- **指南页模板化识别**：审计判据——核心功能 ≠ 适用场景、使用步骤 ≠ 示例标题且 ≥5 条、实用技巧 ≥4 条。跨分类重名用 `--prefix`。
- **跨分类重名 slug 的指南必须走 `--prefix`**：`guides.json` 按 basename 去重，重名会互覆。`_build.py` 靠指南页正文的**绝对 URL** 反查行业，相对路径不会建立精确映射。
- **计算验证 DOM stub 框架六条踩坑**：① 页面多用 DOMContentLoaded，stub 须收集并执行；② 大量工具用内联 `oninput=`，须解析 HTML 属性；③ 内联 handler 在全局作用域执行，window 须指向 globalThis 且把 `new Function` 顶层函数导出到全局；④ 顶层函数枚举须含 `async function` 且 await 结果；⑤ 结果可能写 textContent 或 appendChild，采集须覆盖 value/innerHTML/textContent；⑥ 用例间须清理挂到 globalThis 的页面函数。**依赖「今天」的日期类用例不可纳入**。
- **Python `a = b = []` 多变量共享同一 list**：写审计脚本时多列表必须逐个独立赋值；计数异常一致时先怀疑脚本。
- **仓库体积（`.git`）维护**：`du -sh .git` > **800M** 即跑 `git repack -a -d` + `git prune-packed`（合并全 pack、**不 prune 任何不可达对象**，零工作区影响、可随时重跑）—— 参考实测 860M（29 pack）→ 662M（1 pack）。另注：仓库另有约 103M **不可达对象**（经查全是 `git stash` 残留），清理须 `git prune`（**不可恢复 → 须老板拍板**，Agent 只报数据不做）。
- **同一逻辑在多个分类重复实现时，抽通用脚本而非复制**：新分类开工前先 `ls scripts/` 查是否有可加 `--industry` 的现成脚本（老板明确偏好复用而非复制）。

---

## 七、未完成任务清单

### 7.1 孤立未完成任务（按优先级）

> 跨分类 / 独立的系统性问题，可穿插推进。

**P1 — 待办**

- **harness 输入桩能力现状（2026-09-24 定型，勿再重估）**：可注入手段共 **6 种** —— `inputs`、`checkIds`、`radios`、`checks`（**仅在「无 inputs」分支计入弱用例判定**）、`clicks`（页面作用域 direct eval + 动态 DOM 登记）、`dynDom`。**「纯 checkbox 量表页不可注入」的旧结论已失效**。逐例打法见 `.workbuddy/memory/` 与 skill `toolbox-weakcase-hardening`。
- **仍未闭环的残留（转 P3 顺带，不单独成批）**：
- **`metalwork/tester-19` ≤1kV 耐压分支无法构造判别用例**：该分支输出恒为 `3.5 kV`（与 `ratedV` 无关），任何 `expect` 都会在**默认态**命中 → 必被判逃生项，故**刻意不补用例**；该修复只能靠隔离器人工跑 + 代码评审保真。
- **「多页签（mode）」页面的非默认页签分支无法被 harness 覆盖**：切页签必须带参 `setMode(1)`，而 harness 只无参调用候选函数 ⇒ 第二种模式分支永不执行。**复核口径**：复制页面到 `tools/<ind>/_tmp-xxx.html`，把 `let currentMode=0;` 改成 `1` → 隔离器单跑 → **立即删除副本**。
- **永久排除（不下架）**：同名异功能 `finance/salary-after-tax` ↔ `payroll-calculator`、`ophthalmology/self-assess-2` ↔ `osdi-scale`；跨行业同名编号页（`calc-N`/`rater-N` 等 17 个 basename）经内容哈希取证均为不同工具，非重复。


**P2 — 低优先级**

- **指南英文副本（`guides/*.en.html` 100 篇）软隔离已办**：已配为孤儿文件（sitemap 排除 + hreflang/入口移除 + 索引 state 清理）。**文件保留至约 2026-10-21 再物理删除**（到期前勿动）。

### 7.2 分类收口待办清单（按 §4.1 维度）

> 完成一个分类从本节删一个。判定标准见 §4.1 / §4.5。
>
> **当前为空** —— 全站 209 分类已全部收口（2026-09-19 收官）。


### 7.4 verify 用例覆盖缺口（新线）

**全站真实零用例 = 616 页 / 86 行业**（2026-10-07 重建扫描）。扫描口径：覆盖集合 slug 为 **`行业/slug`** 形式；过滤 `TOOLBOX-REDIRECT` 存根；**用例块键名常不带引号，正则须写 `"?slug"?\s*:\s*"([^"]+)"`** 否则大量误报「无用例」（已踩两次）。checkbox 页 353 个，162 个有用例的均带注入通道、弱用例 0。

**分批补强进度（确定性计算器 + radio 量表，已收口）**：B1=encode/calc-2·homa-ir·earth-curvature(3)、B2=neurology/dhi·dn4·phq9-stroke·rls-severity(4)、B3=encode/calc-1·it/calc-8(2) + **harness atob/btoa 始终宽松覆盖补丁**（修 Node24 原生严格 atob 对 URL-safe 多余 `=` 误抛 Invalid character，对齐浏览器宽松语义）。判别力 7758/0、弱用例基线 no_inputs=10/all_default=4 零新增；atob 改动零回归。**放弃候选**：it/html-to-markdown（convert() 依赖 `new DOMParser()`，harness 未建模，需完整 HTML 解析器桩，超范围）。剩余确定性计算器候选待 B4+ 续推。

**⚠ 判别器口径（踩过才确认）**：`discriminate_check.js` 是**一次性把 inputs 全部换回页面 HTML 默认**（非逐键）**且保留 clicks**（⇒ 仅靠 clicks 所设状态的输出恒命中，不可作锚）；harness 判定是「expect **任一**子串命中即通过」。⇒ 凡不在静态 HTML 中的输入（如 JS 动态渲染的 `sus0..sus9`）**无法回退**，失败态 = 其余键默认 + 该键保持注入；此时必须按**该失败态**实测选锚。**`fun` 53 页已坐实：50/53 为游戏或随机生成器（RAND=True），整行业结构性排除。**

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
- **修完页面必回头查 verify 用例**：① 用例 `expect` 可能锚在旧错误输出上；② 该页可能**根本没有用例**（缺陷漏网的直接原因，补一条）；③ 新用例的 `expect` 若在**页面默认输出**里也命中，会被判别器（`scripts/discriminate_check.js`）判为**逃生项** —— 非默认输入必须使「默认态」不命中。
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

### 8.12 浮点 expect 的「跨平台 1 ULP」翻车 + CI 诊断盲区

- **🔴 expect 禁含浮点全展开（≥15 位有效数字）**：`Math.pow/exp/log` 在 macOS ARM 与 Linux x86 间常差 **1 ULP** ⇒ `toString()` 最短表示位数不同 ⇒ **本地全绿、CI 必红且不可复现**。处置：只留 **≤10 位有效数字**（实证差 1000 ULP 仍命中）。`toFixed(6)` 短尾数属低危。
- **expect 是连续子串，多数值时须「切成多条」而非各自截断**：逐点截断会跳过中间字符致不命中。正解：在数值处切开（expect 为 **OR 语义**，每条各自连续）；<8 字符碎片丢弃，改后必过 `discriminate_check`。
- **日期/时区依赖（同法排查）**：harness 冻结 `now` 保证确定性（故每天恒定），但 `new Date('<日期串>')` 按 UTC 解析、用本地分量格式化 ⇒ 输出随时区偏移 1 天；`toLocaleString()` 的 **AM/PM** 同理。**判定：同一用例在 UTC-12 与 UTC+14 下结果不一致即脆弱。**
- **锚点须由「注入」决定、不由「时钟」决定**：改 expect 优先选 inputs 直接推出的串。**补强输入须合页面语义**（`γ<1` 别灌 42）；**哨兵串禁灌日期/数值字段**（`new Date('abc123测试')` ⇒ Invalid，页面崩且只剩回显，全站约 51 处）。
- **行业 `main()` 必须打印失败身份**（`❌ slug / why / errs / got`）：否则 CI 只显示 `117/118`，是抓不到真凶的诊断债。已统一补齐。
- **🔴 复验必须用 CI 的同款运行时**：CI 用 `node-version: lts/*`（现为 **Node 24**），本地 managed 是 22 ⇒ `Math.pow/exp/log` 结果差 1 ULP，`toString()` 位数随之不同（`42*Math.pow(42,42)`：Node22/23 = `6.3054993769024**56**e+69`，Node24 = `6.30549937690245**555**e+69`）。**已装 `/Users/cgw/.workbuddy/binaries/node/versions/24.11.1/bin/node`，改动 verify 用例后必须 Node22+Node24+`TZ=UTC` 三重复验。** 教训：不可凭「测了两个版本相同」推断全版本相同。
- **🔴 天文数字用例一律换温和输入**：`42^42` / `p=42` 这类违反语义的输入产出的巨型值，**不是 1 ULP 而是整体随 Node 版本变**（`binomial-cdf` 实测 Node22 `5.075681950731849e+63` vs Node24 `5.48713341525903e+63`，差 8%）⇒ 截到 10 位也救不了。判据：expect 含 `e+2x` 及以上的天文数字，就该换输入而非调 expect。
- **「本地过、CI 挂」排查次序**：① 纯净树复跑 ② 多时区 ③ 多 Node 版本 ④ 比对纯净树 build 产物与工作树 `tools/` ⑤ 余者即 CPU/OS 架构级 1 ULP。
- **已知脆弱 2 条已收口（2026-10-11 批次）**：`legal/patent-term-calculator`、`life/date-difference-calculator` 此前 `new Date('<日期串>')` 按 UTC 解析、用本地 `getFullYear/getMonth/getDate/getDay` 格式化 ⇒ UTC 之后时区（如 America/New_York）偏移 1 天。**处置=只重锚 verify expect（不修页面）**：`legal` 改锚稳定「2035年3月」(剔「20日」)、`life` 正常用例锚「从…到…/1周0天」(剔「0年1月/7天」)、B类哨兵用例锚 diff 面板连续三行「NaN 天/从…到…/⚠告警」(剔「暂无历史记录」默认文案与「周五/共NNNNN天」本地分量)。**不修页面理由**：内联脚本被 `_build.py` 静默覆盖、受众 China/UTC 本就正确、任务范畴是「让 verify 套件跨时区稳健」非改页面逻辑。复验：UTC/Asia/Shanghai/America/New_York 三时区 legal 101/101、life 235/235 全过；判别力 0 逃生；`run_gates --skip-build` 216/216。改动仅 verify 脚本（非构建产物）⇒ 本地 commit 不 push。

### 8.13 i18n 键「前缀错配」会静默把键名弹给用户

- **症状（真浏览器取证）**：中文态点「复制结果」→ toast 显示字面量 `toast.copy_success`（**不是 `undefined`**）。**根因是前缀错配、不是键缺失**：页面里写 `i18nText('toast.msgNNN')`（1033 处）而 `I18N_MSG` 存**裸 `msgNNN`**（624 条）⇒ `resolve()` 回退链末端 `return key`，把**调用方的键字符串**渲染出来。**逐个补键是错方向**（755 键两套字典皆无、语义未知）⇒ 走**前缀归一化回退**（剥前缀再查，页面与字典零改动），配套 `js/i18n.js` 导出 `I18n.has()`；**英文态须单独兜底**（`en-US PACKS` 未收录 msgNNN，否则回落中文给英文页面）。
- **三个坑（各返工一轮才定位）**：① 兜底**必须放 `i18nText` 内**，不能放 `normalizeI18nKey` 末尾——后者在 `while` 剥前缀时已 `return k` 提前退出，末尾分支永不执行；② `js/common.js` **整体在 IIFE 内**，`I18N_MSG` 在 `evaluate` 里 `typeof==='undefined'` 属正常，**不可据此判"修复未生效"**；③ 语言判定用 `I18n.get()`，别用未挂 window 的 `isEnglishMode()`。**验证口径**：改 i18n 必须**真浏览器点一次真实按钮**看 toast 的 `textContent`。排查用 `grep -roh "i18nText('[a-z][a-zA-Z0-9_.]*'" tools/ js/` 取全键与两套字典求差集。

### 8.14「卡死」判定必须用心跳，不能用 evaluate 往返超时

- **踩坑**：`Promise.race([page.evaluate(click), timeout(1500)])` 判卡死，全站报 5 页，用「主线程心跳 + 8 次采样」复核**全部心跳每秒 +10 无阻滞** ⇒ **零真死循环**（原报警是通信延迟的假阳性）。**正确判据**：点击前装 `setInterval(()=>window.__hb++,100)`，点击后每 1s 采样连续 8s：停摆 = 真死循环。**单次超时不能定罪。**
- **两条静态伪线索（勿采信）**：① 正则扫 `while` 报 338 处可疑，复核全是正常写法（欧几里得 `[a,b]=[b,a%b]`、日期 `hh=(hh+1)%24`、`push`）—— 死循环只能靠真浏览器 + 心跳二次确认；② 数据表「列数不一致」实为**对象字面量**按属性名取值、无下标 —— 字段错位只能靠页面语义判断（如 `chinese-radical-lookup` 的 `d[3]`/`d[4]`）。
- **harness 盲区页无法静态识别**：**注入 → 跑该行业 verify → 失败页写入 `--skip` → 带 `--skip` 重跑 → 直到全绿**（v8）。**dry-run 命中 ≠ 存在缺陷**，须过「jsdom 真机 + 源码兜核」；**jsdom 桩会把 `:checked`/`dataset`/动态 `innerHTML` 控件页误报成除零 ⇒ 判真缺陷只能用真浏览器**。**v8 守卫只是遮羞布，治本用 `_inject_input_guard_v9.py`**（calc 入口插 `__tbInputGuard()`、公式不改；必填判据=`type=number` 且有非空 `value`，顺序＝分母→全零，判存在用 `indexOf` 非 `in`）。

### 8.15 动态扫「异常/死功能」：探针自身准确率是第一位

- **两条最易踩**：① 必须走 **HTTP**（用 `ThreadingHTTPServer`，单线程 `http.server` 会被并发压垮产生假超时）而非 `file://` —— 后者 `fetch` 必被 CORS 拦，每页误报 2 条 console error；② **收敛标尺：60 页样本上 flagged 必须为 0 才允许跑全站**（本类探针曾 59/60 全误报、返工 4 次才到 0，探针不过关跑全站等于白跑）。
- 另四条（结果区 id 不能硬编码、排除页面 chrome、乘性扰动、排除广告分享区输入）见 memory `2026-10-07.md`。

### 8.16 两种「函数存在但不可见」的真缺陷（各修 1 页）

- **形态一：被未闭合的函数体吞掉**。`calcTool(){…`（数组型工具生成函数）行尾只有 `{` 没有 `}`，函数体延伸到块末尾，把紧随的 `copyEmoji`/`copyLatex` 变成内部代码 ⇒ 从未注册全局。**表象极具迷惑性**：同块其他函数正常、加载期**零 pageerror**、script 语法校验**通过**（整体合法、语义错位）。`emoji-picker`（195 emoji 全渲染不出）与 `latex`（183 符号全渲染不出）**整页核心功能不可用却无任何报错**。**判据**：逐个 `function` 做花括号平衡，**体长异常（>4000）且其后还有 function 声明**即候选，再用 `typeof window.X` 复核。**修法**：在真正该闭合处补 `}`，被吞的函数定义**移回顶层**（会留重复定义，须删内部那份，且别误删相邻函数的函数头）。
- **形态二：IIFE 包裹 + 内联 onclick**。`(function(){…})()` 内的 `function` 声明不挂全局，而 `onclick="executeSQL()"` 需要全局 ⇒ 报 `X is not defined`。同页其他函数已按 `window.X = function…` 挂载时，**只有漏掉的那几个**是真缺陷。照该页既有风格补一行挂载，**不要用 `eval`**。
- **形态三：`onclick` 属性被 `JSON.stringify` 的双引号提前闭合**。`onclick="applyPreset(${JSON.stringify(p.colors)})"` 中 JSON 对数组/对象产出的值**本身含双引号** ⇒ 解析器在第一个 `"` 处闭合属性，`onclick` 变成 `applyPreset([` ⇒ 点任何预设抛 `SyntaxError: Unexpected end of input`。**修法：属性改用单引号包裹**。全站 17 页内联 `JSON.stringify`，但**只有传数组/对象的 5 页会出问题** ⇒ **必须真浏览器逐页编译验证**（遍历 `[onclick]` 用 `new Function` 编译，失败即坏 handler），实测 16/12/12/12 个 → 全归零。
- **Canvas 负半径**：`radius=Math.min(cw,ch)/2-30` 而 `cv.width=ct.clientWidth`，容器未布局时 `cw` 为负 ⇒ `ctx.arc` 抛 `The radius provided (-70) is negative`。修法 `Math.max(5, …)`，已修 construction 三页。
- **两条静态假阳性（勿采信）**：「IIFE 未挂 window」报 **293 页** —— 抽样 8 页仅 3 页真有问题；「函数体超长吞并后续」报 **530 处** —— 复核**全是正常调用**（长 `calc()` 里调 `copyResult()`）。**「函数不可见」只能用真浏览器 `typeof window.X` 定罪。**

### 8.17 已知重复工具组：`pets/` 与 `pet/` 同功能双实现（✅ 已收口 · 2026-10-10 commit 87fb49549c）

- **处置（已落地）**：保留 `pet/`（10 工具），`pets/` 5 个同义页全部转 `TOOLBOX-REDIRECT` 存根（保留 URL）：`pet-age-convert`→`pet-age-converter`、`feeding-amount`→`pet-feeding-calc`、`vaccine-reminder`→`reminder-vaccine-deworming`、`grooming-guide`、`kennel-space`。`json/industry-*.json` 已移除 pets 行业（207 行业）；`guides/`、`json/` 无 `tools/pets/` 硬引用；`sitemap.xml` 中 pets/ 出现 0 次；`verify_pets_calc.js` 已无 pets 用例。`tools/pets/index.html` 工具链接已正确指向 `../pet/*`（无断链）。
- **残留（已收口 · 2026-10-11）**：`tools/pets/index.html` 已转 `TOOLBOX-REDIRECT` 存根指向 `tools/pet/index.html`（保留 URL、`noindex,follow`、沿用 §8.17 同款 TTZZ 分析脚本与 meta refresh 模板）。pets 行业至此彻底消除（5 同义子页 + index 全部存根化，json 行业清单已移除 pets）。

---

## 九、发现但未修的真实缺陷（待老板定夺）

> **缺陷 A–U 已闭环**（根因进 §八，明细见 memory 2026-09-2*.md）。本节只留**未处理**项。

- **未处理（疑似口径）**：`legal/calc-8`（年终奖计税）把「社保/专项附加」按**年度值**扣除、未 ×12；若语义是「月缴」则应税所得高估、税额偏低。等老板确认语义。
- **未处理（非缺陷）**：`ai/ocr`、`ai/image-classification` 等 5 个 `<script type="module">` 页的 `own_len` 度量盲区（结论：不改）。

## 十、优先级与当前主线

> **主线 = 优化 `tools/**` 页面本身**。`scripts/` 验证脚本除门禁必需外不单独投入，只在优化分类时顺手改，不单独立批。

### 10.1 优先级总纲

| 级别 | 内容 | 状态 |
|---|---|---|
| **P0** | 页面级真实缺陷修复（§九 清单） | A–U 已闭环；**当前无进行中批次**，§九 仅余 `ai/*` 度量盲区（评估为不改） |
| **P1** | 按热度逐分类 §4.1 八项目标收口 | **全站 209 分类已收口**（§7.2 为空） |
| **P2** | ✅ 工具质量分级提升（C→A） | **已达成：A 级率 70.0% → 99.43%**；名不符实占位换算器全量 30 页已重做收口（§九 已处置） |
| **P3** | `scripts/` 用例与基线维护 | **仅随 P0/P1 顺带**；门禁必需项（`run_gates.py` 链路）除外 |

### 10.2 现状（实测基线）

- `all_default 4 / no_inputs 10 / escape 0`；门禁 `run_gates.py` **216 项全过**（含新增首道 `expect anti-pattern` 静态门禁：秒级、源码文本层扫描 207 脚本/7775 个 expect 数组，禁浮点全展开 / 时区 AM-PM / 冻结日期，置于 build 之前以便快速失败）、逃生项 0（判别器已检 **7758** 例 / 跳过 52）。
- A 级率 **99.5%**（A 4701 / B 20 / C 5）；术语内链 **1591 页 / 2268 条**（零死链、零自链）。占位换算器重做批次见 §九。
- 弱用例口径与选批规则见 §10.3。**注意：弱用例整体处于判别器盲区** —— 「注入值等于默认值」的用例被判 `usable=false` 直接跳过（§10.5）⇒ `escape=0` 只说明强用例无逃生项；每批改造后须重跑判别器确认其由「跳过」转为「已检且变红」。

### 10.3 弱用例去默认化（仅在 P0/P1 顺带时执行）

**存量 14 例**（`no_inputs=10` / `all_default=4`）**已全部收口（2026-10-10 补完最后 2 个 `auto-restore(default)` 漏评项 `ceramics/glaze-temp`、`image/nine-grid-cutter`，均判死保留 `no_inputs`；14 例 `ref` 齐备）**。两处「顺序保持型筛选」翻案（`office/excel-formula-reference`、`gardening2/pruning-time`）均锚**过滤后跨条目相邻串**（§10.5 C.7④）。**转 P3 顺带，不单独成批**；逐批成果与逐例打法归档在 `.workbuddy/memory/` 与 skill `toolbox-weakcase-hardening`，**本文件不再记录批次流水**。

**选批口径**：① 按「可注入数」降序挑批次；② **结构性不可注入的不要选**（判据 §10.5 B 组）—— 保留 `no_inputs` 并在 `ref` 写明理由；③ 每批 8–11 例，走 §10.4 六步。**结构判死的唯一依据是各用例 `ref`**。

### 10.4 每批收口流程（六步，缺一不可）

1. 改写 `scripts/verify_<cat>_calc.js`（非默认输入 + Python 独立复算 expect）
2. 单跑 100% 通过 → `node scripts/discriminate_check.js verify_<cat>_calc.js` **0 逃生项**
3. 被「跳过」的用例（textarea / 动态 id `q0..qN`）必须**自建同口径探针**补验「注入 PASS + 回退默认 FAIL」
4. 更新 `falsepass_baseline.json` 与 `discriminate_baseline.json`（**只准降不准增**，按实测值同步）
5. `python3 scripts/run_gates.py` 全过 → `git commit` + push、**单次**确认部署
6. 归档 memory（**批次玩法只写 memory 与 skill，禁止写进本文件**），清理 `/tmp` 临时脚本

### 10.5 harness 已知限制（选批与定 expect 前必读）

> harness = `scripts/verify_it_calc.js`。**三阶段**：① 覆盖 `inputs` + 触发 `input/change/keyup` 立刻查 expect → ② 执行 `clicks` → ③ 未命中才**无参遍历调用候选函数**兜底。`collectStrings` 收每元素 `value`/`innerHTML`/`textContent`，剥标签压成**单串** ⇒ `blob.includes(want)` 是**子串**匹配。

- **定 expect 五条铁律**：① 锚点只依赖被测点，禁混表头/按钮/页脚/option value 等常量（`达标` ⊂ `未达标`）；数值须与标签绑成连续串。② **双态核验**：注入态 PASS + 默认态 FAIL 双跑，`inputs` 等于默认值 ⇒ 判 `usable=false` 静默 skip（零判别力）。③ 兜底会改状态重算 ⇒ 避开无参函数能产出的串；`expect` 含 `undefined`/`NaN` 几乎必是兜底产物。④ 日期/随机一律不锚；`clicks` 改进程级全局**用完即恢复**。⑤ **判别器是清空 clicks 后跑** ⇒ 锚「恒产全量」输出（`checkAll()` 的 `36/36`）必判逃生项，改锚具体输入态。
- **不可注入的静态判据**（B1–B9 全分支与 `clicks`/`radios`/`checkIds`/`dynDom` 六种手段用法见 **skill `toolbox-weakcase-hardening` → `references/harness-limits.md`**）：控件由运行期 `innerHTML` 生成（id 形如 `c{i}`）、驱动走纯 class 选择器、`createElement+appendChild` 建的行、控件在 `display:none` 面板内（`inputs` 与 `clicks` 都改不动）。
- **P0 真缺陷信号**：控件 id 不存在（加载即 `Cannot read properties of null`、整页无输出）；`.length` 判空却传对象（`!list.length` 恒真 ⇒ 整页功能恒定不工作）。别急着归类为「不可注入」。
- **工具**：常驻 runner `~/.workbuddy/skills/toolbox-weakcase-hardening/assets/weakcase_runner.js`（cwd 为仓库根，每批直接调用、不要重建）；FAIL 定位用 `runCase` 逐项二分，**禁用 `fullBlob.includes()`**。


