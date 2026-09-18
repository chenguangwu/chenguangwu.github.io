# DEV-PLAN.md — 全站工具优化总计划（超大规模工程）

> 状态：按分类逐行优化中。**一个分类必须把 §4.1 八项目标全部干完才进行下一项**（硬约束唯一权威见 §4.3）。完成一个分类从 §9.2 删一个，不做完不收手。
> 本文件为权威分批计划载体；所有改动落盘后按"批量多文件合并提交"原则分批 commit / push master 触发发布。

---

## 一、总体目标

目前线上大部分工具都不合格，需优化成**成熟、可直接线上使用**的工具，且要比竞品工具更强、有一定优势（功能更全、内容更专业、UI 更现代、结果更可信）。

---

## 二、未完成的主要问题（逐条对照验收，已完成项已移除）

> 以下为 git 实测后**仍未全站收口**的问题（已完成深度真实化与 i18n 修复的项已移出本清单）。

1. **UI 太丑**：没有一点现代化网站的设计 → 统一现代化视觉（遵循 `ui/设计规范.md` + 参考 MBTI `tester-2.html` 风格）。（对应 §4.1.3）
2. **内容不够丰富**：补真实使用场景、示例、参考表、可视化（明细表 / 图表 / 日历等）。（对应 §4.1.2）
3. **逻辑错误误导用户**：工具内部存在计算 / 计分 / 判定错误 → 必须验证结果正确，不误导。（对应 §4.1.1）
4. **缺使用指南**：重要的专业工具没加使用指南 → 补「📖 使用指南」+ 深度解析（FAQ）。（对应 §4.1.4）
5. **SEO 描述不合适不完善**：名称 / 标题重复已清零，但 Description 仍有 69 组重复未修复；让人一眼看懂用途，完善 Description / H1。（对应 §4.1.7）
6. **下拉选项只是占位或不合理**：选项要真实、合理、有业务意义。（对应 §4.1.3 页面下拉项）
7. **结果正确性未验证**：需验证工具使用结果正确（最好专业可验证）。（对应 §4.1.1）
8. **专业名称缺外链**：部分专业名称可加百度百科外链跳转。（对应 §4.1.7）

---

## 三、注意事项

1. 工具都必须是**纯前端**的；实在不适合本项目的工具（需后端 / 实时数据 / 登录认证等）直接删。
2. 所有**答题类工具**参考样式：`/tools/psychology/tester-2.html`（逐题作答引擎：进度条 + 单题卡片 + 题号速览 + 键盘操作 + 本机存进度 + 真实计分 + 深度解读）。
3. 有好建议也可补充，只要能提升用户体验和效率的都能加。
4. 之前项目里不合理的约束可以去掉，按最好的方式开发。

---

## 四、开发规则（强制）

- **恢复逐分类完整优化清单（按热度排序）**：全站 268/268 分类虽已完成 deep-dive 六型占位真实化（git 实测 285 commit / `content_deepdive.json` 提交 316 次，键数守恒 5022），但 **§4.1 八项目标的其余维度（UI / 指南 / 下拉 / 外链 / 逻辑验证 / SEO 描述等）仍全站未收口**。故恢复「按分类逐行优化」模式：所有分类按**热度（分类下工具页数量，覆盖用户面代理）降序**列入 §9.2 待办，从最热的分类开始。历史已完整优化的分类见 §9.1 白名单，不列入 §9.2。
- **进行中的分类**：在「当前进行中分类」登记（分类名 + 工具数 + 当前进度），列全部分类下工具。
- 分类状态按状态机推进（权威定义见 §4.3）：待办分类保留在「§9.2 分类优化清单」；开始后写入「当前进行中分类」；完成即同时从「当前进行中分类」和「§9.2」删除该分类条目。状态须在同一次任务中同步更新。
- **psychology 已优化过一遍**：先按上面 10 条标准**验证**是否满足，全满足则直接跳过该分类；否则先优化该分类里不满足的工具。
- 每完成一批（或一个工具）跑 `python3 _build.py` + `python3 _test_static.py`，确保门禁通过、繁体 `zh-tw/` 同步。
- **提交发布节奏**：最好**一个分类提交发布一次**；分类下工具多的（如 `it` 345 / `general` 180 / `finance` 112），可分批提交，**每批至少 10 个工具**，避免单工具频繁发布。
- **发布前必须跑质量门禁、发布后必须查部署结果**：每次 `git push` 前，先本地跑 `python3 scripts/run_gates.py`（五项门禁：build→静态→死链→资产→公式）**全部通过**；`git push` 触发 GitHub Actions 后，**必须查 Actions 运行结果确认部署成功**（公开仓库 `curl -s https://api.github.com/repos/<owner>/<repo>/actions/runs` 看最新 run 的 status/conclusion），**禁止 push 完就发总结结束回合**。CI 会重跑门禁，本地没跑过的 CI 照样挂、照样不发布。
- **新建页面防死链**：从范本 copy 的指南/工具页，必须删掉英文版 `hreflang` 链接与 "🌐 English" 按钮（本项目英文走 `?lang=en-US`，不生成独立 `.en.html`）；不引用任何不存在的文件（拼写错的 slug、未生成的附属页），否则 dead-link 门禁必挂。
- **改 deep-dive / 使用指南等被构建重建的区块，必须改数据源 `i18n/tools/content_deepdive.json`**（直接改源 html 会被 `_build.py` 覆盖，见下方踩坑备忘）。

### 4.1 每个分类的强制任务目标

每个分类必须覆盖该分类下的全部工具，不能只挑页面清理文案。开始分类前，先在「当前进行中分类」登记完整工具清单；每完成一个工具就从清单中删除，并保留可追溯的改动证据。

每个工具必须同时完成以下目标，缺一项都不能结束分类：

1. **功能**：输入、处理逻辑、输出和异常提示真实可用；专业计算用已知样例、独立公式或 `node` 纯函数验证。
2. **内容**：补真实场景、真实示例、边界说明、参考表或可视化；禁止复制“常见场景：XXX”“先统一输入单位与口径”等套话。
3. **页面**：检查 UI、移动端布局、输入项、下拉选项、默认值、按钮和结果区；不能因为 SEO 文案变化就视为页面完成。
4. **深度内容**：专业工具必须在 `i18n/tools/content_deepdive.json` 有真实条目，含场景、示例和至少 2 条针对性 FAQ；需要指南的工具必须补指南入口和指南数据。
5. **i18n**：同步中文页、行业 JSON、`slug-en.json`、`_en_override.json`、页面英文元信息、英文可见内容和繁体构建结果；英文描述必须说明实际用途，不能只是“free online tool”。
6. **分类**：核对 `<meta name="toolbox">` 的 `industry` 与 `cat`，发现错标必须在源 HTML 修正，不能只手改构建产物。
7. **SEO 与专业性**：Title、Description、H1、JSON-LD 和面包屑用途一致；关键专业名词按需补权威外链，并确保不制造死链。
8. **发布证据**：分类全部工具完成后，必须有构建、五项门禁、远端 Actions 成功和提交 SHA；只证明“套话不存在”不能作为完成证据。

若本批只改了 `desc-en`、`slug-en`、meta 或其他文案，不得标记分类完成，必须继续补齐该分类在 §4.1 八项目标下的其余内容（UI / 指南 / 外链 / 逻辑验证等）。完成一个分类后，必须从「当前进行中分类」和「§9.2 分类优化清单」中删除该分类条目，不得改成 `[x]` 后长期保留（硬约束与严禁项见 §4.3）。

### 4.2 提交与发布文件边界

- 修改前和准备提交前都必须执行 `git status --short`，建立本批文件清单；发现不是本任务产生的改动，立即停止并确认，不得覆盖、暂存或提交。
- 禁止使用 `git add -A` 或 `git add .` 兜底提交；必须按已确认的文件清单显式 `git add`。
- `json/*.json`、`sitemap.xml`、`sw.js` 等构建产物只能由 `_build.py` 生成；若状态中出现其他脚本、配置或业务文件，必须排除并向用户说明。
- 最终汇报必须列出 commit SHA、实际提交文件范围、五项门禁结果和 Actions run URL，不能只说“已发布”。

### 4.3 分类收口顺序与状态同步

每个分类只能按以下顺序收口，不得跳步：

1. **建立范围**：读取该分类实际目录，登记全部工具页（含工具数，须与 §9.2 热度计数一致）；分类下每个工具都必须走完 §4.1 八项目标。
2. **逐工具处理**：逐个完成功能、内容、页面、deep-dive、i18n、cat、SEO 和验证目标；工具完成一项就从进行中清单删除。
3. **完成前审计**：确认进行中清单为空，且分类下**没有**：占位套话、缺失 deep-dive、英文通用描述、cat 错标、未验证的关键逻辑、缺使用指南（专业工具）、缺专业外链、UI 未现代化、Description 重复。**八项目标缺任一项即视为未收口**。
4. **同步状态**：从「当前进行中分类」和「§9.2 分类优化清单」删除该分类条目，确认本分类完整收口。
5. **发布收口**：状态同步后才能跑门禁、提交和推送；归档未更新、清单未删除或文件范围未核对时，禁止宣称分类完成。

> **硬约束（老板 2026-09-11 明确，违反即违规）**：**一个分类必须把 §4.1 八项目标在该分类下全部工具上完全干完，才能开始下一个分类**；**禁止只挑简单任务**（如只清占位 / 只补 deep-dive 内容）就标记分类完成、跳过 UI / 指南 / 外链 / 逻辑验证等难项。清单未清空（本分类仍有工具未完成或八项目标有缺项）**不得开始下一个分类**。

严禁以下不完整状态：只把待办改成 `[x]` 不删除、当前进行中标题与清单分类不一致、清单未空就开始下一个分类、本分类八项目标有缺项却标记完成。

### 4.4 使用指南增强规则（老板 2026-09-08 明确授权）

每个分类除按 §4.1 完成基础优化外，**须主动识别「专业度高且热门」的工具并补充独立使用指南页**，使其同时具备深度解析（deep-dive FAQPage）与系统化「📖 使用指南」独立页。

- **判定标准（agent 自主判断，老板授权）**：
  - *专业度高*：计算 / 判定 / 法规 / 工程 / 医疗 / 金融 / 养殖等技术类工具，结果影响用户决策或有行业依据（如池塘容载量、投饵率、溶解氧、用药休药期、收益测算等）。
  - *热门*：用户常用、搜索量大的高频工具（各类计算器、收益测算、单位 / 密度换算等）。
  - 满足其一且非纯娱乐 / 纯展示的简单工具即应补指南；纯娱乐（骰子、抛硬币）、纯文本格式转换等低专业度工具可不加。
- **落地动作**：用通用脚本 `scripts/gen_guide_pages.py` 批量生成 `guides/<slug>-guide.html`，自动合并 `json/guides.json` 并追加 `guides/index.html`；模板须去除英文版 `.en.html` 链接与独立英文 `hreflang`（英文走 `?lang=en-US`，遵循 §4.48）。
- **内容要求**：指南页须含适用场景、操作步骤、注意事项、针对性 FAQ，内容真实专业，禁止「常见场景：XXX」等套话；可基于该工具 deep-dive 的真实场景 / 算例 / FAQ 扩展，但须系统化、可读性强。
- **已收口分类**（如 fire-rescue）若属专业度高的工具集中，后续批次可择要补指南，不强制回退已发布版本。
- **⚠️ 指南页克制原则（老板 2026-09-08 补充）**：指南页只给「有必要的工具」加，**不要全分类铺量**。判定「必要」= 专业度高且易被误用/需说明步骤/有法规或计算依据的工具（如金融、医疗、法规、工程计算、养殖投饵/用药、收益测算等）；纯娱乐（骰子/抛硬币/猜数字）、纯文本格式转换、纯展示查询类工具**不生成**指南页。每个分类优先把精力放在 deep-dive 真实化与套话清零，指南页按需精选，避免数量过多稀释质量。

### 4.5 通用修复清单（质量红线，每个分类必做，老板 2026-09-08 起固化）

优化过程中反复出现的几类问题，必须作为**每个分类处理时的标准步骤**固化，避免回退：

1. **公式数字必须与工具 JS 一致（最高频事故）**：写 deep-dive 算例后，必须用 `node` / `python` 按工具默认输入**独立复算**一遍，结果一致才落盘；禁止凭记忆/估算写数字。已发生事故：manning-velocity 误写 1.94（实 1.53）、weber-number 误写 1374（实 13736，差 10 倍）、terminal-velocity/venturi 缺算例（后补）。任何「差 10 倍 / 数量级不符」都是危险信号。
2. **opt-guide / opt-faq 套话块清零**：每个分类处理前先 `grep 'class="opt-guide"\|class="opt-faq"'` 全分类，命中即用正则 `re.sub(r'<section class="opt-guide">.*?</section>\s*','',t,flags=re.S)` 配对清理，目标**前 N 后 0**（非构建范围，须手改源 HTML）。
3. **数据源孤儿条目自动新增**：`tools/` 有页但 `content_deepdive.json` 无条目时（如 food-processing/tester-5），写入脚本须**自动新增**而非 `assert` 中断；避免整批丢失。
4. **缺数字断言防误伤**：算例含中文数字（四/五/十/百）也视为「有数字」，不得因无 ASCII 数字触发缺数失败；写入脚本改用**增量落盘 + 软警告**，单条异常不丢整批。
5. **线上落盘核验（发布证据）**：push 后必须 `curl` 落盘校验——真实算例文本已注入、套话（占位指纹：①快速复核 ②统一口径(建模·演示) ③统一复核 ④高频复用模板 ⑤在X业务中先把Y标准化后再执行对比 + 复用模板示例 + 保留复用模板 + 结构性泛化短语「减少重复确认成本/标准化再批量/可复核输出/沿用模板逐项核对/形成标准复核清单/边界样本建议单独标注/降低上手门槛」）为 0、opt-guide/opt-faq 为 0；不能只靠五项门禁通过就宣称完成（§4.1.8）。
6. **指南页克制**：见 §4.4 末条，不铺量。
7. **套话指纹持续扩充（老板 2026-09-11，it 分类实测）**：上条清单之外，已确认还有这些变体，审计时必须一并 grep：
   - `本生成器依据指定格式规范…`（生成器/条码类，曾一次性命中 23 个）
   - `本速查内容依据权威标准…`、`本计算基于标准数学定义…`（速查表/计算器类）
   - **数量达标 ≠ 内容达标**：barcode/http-* 等曾出现「场景 2 条」但内容是「生成/识别 XX 码用于仓储、零售或资产标签」这类无信息量的结构泛化，必须逐条看内容而非只数条数。
   - **指纹会误伤正常措辞**：`统一口径` 在「先约定统计口径」这类正常语境下也会命中，写内容时避开该词组，命中后先判断是否真套话再改。
8. **审计要查「达标率」而不只是「覆盖率」（老板 2026-09-11，it 分类审计缺口的教训）**：`content_deepdive.json` 有条目 ≠ 满足 §4.1.4。收口审计必须按「场景 ≥2 且 示例 ≥1 且 FAQ ≥2 且无套话」逐条算达标率——it 分类首次审计时覆盖率 100% 但达标率仅 8/345，差点漏掉整个 §4.1.4 缺口。

---

## 五、验收标准

> 验收 = §4.1 八项目标的**可勾选版**，须与 §4.1 逐条同步更新（避免三套清单各自漂移）。每个分类收口前，逐项确认 §4.1 八项目标全部达标，即视为验收通过。

- [ ] 1. 功能：真实可用 + 独立验证（对应 §4.1.1）
- [ ] 2. 内容：真实场景 / 示例 / 参考表 / 可视化（对应 §4.1.2）
- [ ] 3. 页面：UI / 移动端 / 下拉 / 按钮（对应 §4.1.3）
- [ ] 4. 深度内容：deep-dive 真实条目 + 指南（对应 §4.1.4）
- [ ] 5. i18n：中 / 英 / 繁完整（对应 §4.1.5）
- [ ] 6. 分类：industry / cat 无误标（对应 §4.1.6）
- [ ] 7. SEO 与专业性：Title / Description / H1 / 外链（对应 §4.1.7）
- [ ] 8. 发布证据：构建 + 门禁 + Actions + SHA（对应 §4.1.8）

---

## 六、踩坑 / 约束备忘

> 质量红线类约束（套话清零 / 占位六型 / 算例复算）已固化于 §4.5，本节仅保留**环境级 / 工程级**约束，不重复。

- **deep-dive 由 `_build.py` 按 `i18n/tools/content_deepdive.json` 重建**：直接改源 html 的 deep-dive 区块会被构建覆盖。改 deep-dive / 场景 / 示例 / FAQ → 改 JSON 数据源。
- **FAQPage 结构化数据不被 `_build.py` 重建**：手动加的合法 JSON-LD 会保留，但注入坏 JSON 不会被自动修复，须自测解析合法。
- **繁体 `zh-tw/` 是构建产物**：改源文件 + 跑 `_build.py` 后自动同步；勿手动改 `zh-tw/`（被 `.gitignore` 忽略）。
- **i18n 八件套**：标题/简介走 `_en_override.json` + `slug-en.json`；行业 i18n 走 `i18n/tools/<ind>.json`；凡引 `common.js` 的静态页须引 `i18n.js`。
- **门禁**：`python3 _test_static.py` 须 0 失败 0 告警；死链 `_audit_links --check` 与资产 `_audit_assets --check` 须 exit 0。
- **提交**：批量多文件改动合并提交，commit + push master 触发 GitHub Pages 发布；不可逆操作前先核验。
- **计算函数名不统一**：`calcTool()` / `calc()` / `calcBelt()` / `calcChain()` 等。抽取时在**整个 html** 里多候选 `function <name>(` + 花括号配平，勿用 `max(scripts, key=count('calcTool'))`（会选中 stub）。依赖 select 与常量表的工具（GRADE_DATA / MAT_SPEED / stressArea / torqueCoef）须先抽 `<select id=...>(.*?)</select>` 默认项与 `const X = {` 常量表。
- **deep-dive JSON 格式**：`content_deepdive.json` 仓库规范 `indent=1`（`_build.py` 只读不写、不归一化），apply 脚本须 `json.dump(indent=1)`，否则全 ~12.7 万行重排成噪音 diff。
- **英文 p 三种机制（改法不同）**：① `data-zh` 机制 —— 英文写在源 HTML 里，改源文件即可；② 裸 `<p>中文</p>` —— `_prerender_tool_body` 会用 `<ind>-body.json` 覆盖，**必须改数据源**；③ `data-i18n` 机制 —— 由 build 从 i18n 注入，同样改数据源。页面 grep 到占位串只是表象，根治必须同步数据源（it base64/json-minify、general 全部实测同一坑）。
- **英文态数据源三处（最易漏）**：除页面可见英文（p / `desc-en` meta / `ed`）外，`?lang=en-US` 与 industry JSON 还取决于：`i18n/tools/<ind>-body.json`（title/h1/intro）、`i18n/tools/<ind>.json` 的 `en-US`（**同时是 industry JSON 的 `ed` 最高优先级源**）、`_en_override.json`（en/ed）。只改页面 → 英文态仍显示占位串与工具代号（general 实测：body intro 140/180 占位、title 96 条代号）。
- **build 预渲染陷阱（最高频事故）**：`_prerender_tool_body` 用 `count=1` 命中文档**首个 `<p>`**；任何插在首个 `<p>` 之前的中文 `<p>`（如 formula-desc）都会被 intro 覆盖。修法：改成 `<div>`（不匹配 `<p>`）或补 `data-zh`。该函数**幂等**（检测到已英文即跳过），故改数据源后必须先把页面「还原」（去英文与 `data-zh`）再 build，新值才会注入（it ⑥ / general 均踩）。
- **`desc-en` meta 权威源是 build**：`_build.py` 用硬截断重写 `desc-en` meta，脚本写的「词边界截断」版会被 build 覆盖——无需手改 meta，改 EN_MAP / 数据源即可。
- **指南页模板化识别**：`gen_guide_pages.py` 在缺 `features/steps` 时用「适用场景」派生「核心功能」、用「示例标题」派生「使用步骤」。审计判据：核心功能 ≠ 适用场景、使用步骤 ≠ 示例标题且 ≥5 条、实用技巧 ≥4 条；不达标先在 `content_deepdive.json` 补真实字段（indent=1）再重跑 `--industry <ind> --slugs ...`。跨分类重名用 `--prefix`。
- **计算验证 DOM stub 框架（复用 `scripts/verify_<ind>_calc.js`）六条踩坑**：① 页面多用 DOMContentLoaded，stub 须收集并执行；② 大量工具用内联 `oninput=`，须解析 HTML 属性；③ 内联 handler 在全局作用域执行，window 须指向 globalThis 且把 `new Function` 顶层函数导出到全局（否则恒报 `xxx is not defined`）；④ 顶层函数枚举须含 `async function` 且 await 结果；⑤ 结果可能写 textContent 或 appendChild 到父节点，采集须覆盖 value/innerHTML/textContent 并在 appendChild 时回写父节点；⑥ 用例间须清理挂到 globalThis 的页面函数。**依赖「今天」的日期类用例不可纳入**（门禁会随运行日期失败，general/calc-14 实测）。
- **静态审计两处已知误报（勿报）**：页面无 `id="result"`（结果区用各自命名 grid/detail/astTree…）、无 `data-theme`（主题由 `js/common.js` 运行时写到 documentElement）均为**非缺陷**。

- **deep-dive「覆盖率 ≠ 达标率」有三层套话（finance 收口教训）**：`content_deepdive.json` 有条目 / 条数够 ≠ 达标。逐条比对须分三处独立查：① `scenarios` / `faqs` 模板（如「输入完整的Xxx Validator…」「先清理空格、连字符和分组符号」「工具会上传文本吗」）② `examples` 模板（「{Xxx}的反例复核」「{Xxx}基准复核」+ 通用描述、无真实算例）③ 英文名嵌入中文（`[A-Z][a-z]+ Validator` 出现在中文句里 = 代号型套话）。finance 覆盖率 100% 但三项分别命中 74 / 90 / 若干 —— 只查条数会整体漏掉。
- **跨分类重名 slug 的指南必须走 `--prefix`**：`guides.json` 按 `tool` basename 去重、指南页落盘为 `guides/<slug>-guide.html`，故同名 slug（如 `calc-2` 存在于 22 个分类）新增指南会被去重跳过或直接互覆。处理顺序：先 grep 目标指南页正文的 `/tools/<ind>/<slug>.html` 判断现有归属，重名的用 `--prefix <ind>-` 生成 `guides/<ind>-<slug>-guide.html`；`_build.py` 靠指南页正文的**绝对 URL** 反查行业建 `GUIDE_MAP_IND`，命中则不回退 `GUIDE_MAP`，故相对路径 `/tools/...` 的指南页不会建立精确映射（会误挂同 basename 的其他分类）。
- **审计脚本自身的坑 —— Python `a = b = []` 多变量共享同一 list**：`no_title=no_h1=no_jsonld=no_bread=[]` 会让四个变量指向**同一个**列表对象，任一 append 都会进同一个 list，导致四项计数完全相同（finance 审计时误报「缺 JSON-LD 6 / 缺面包屑 6」，实为 title 的 6 处且判据过严——中文 4 字标题 `<title>[^<]{5,}</title>` 被判为「缺」）。写审计脚本时多列表必须**逐个独立赋值**，或显式 `a, b = [], []`；计数异常一致时应先怀疑脚本而非项目。
- **同一逻辑在多个分类重复实现时，抽通用脚本而非复制**：`fix_finance_formula.py` → `scripts/fix_formula.py`（`--industry` + `--map module:VAR`，数据单放 `fix_<ind>_formula_map.py`，锚点 input-row → input-row2 → h2 后首个 `<p>`）；`fix_general_prerender_reset.py` → `fix_prerender_reset.py`（`--industry` + `--intro-p`）；`fix_formula_intro_p.py` 本身即通用。收益：① 逻辑修复一次即全分类生效（如 `vh-vw` 空壳框识别、script 内误注入防护）② 脚本数量不随分类数线性膨胀。老板明确偏好「直接复用而非复制」，新分类开工前先 `ls scripts/` 查是否有可加 `--industry` 的现成脚本。

---

## 九、未完成任务清单

> **真实状态（2026-09-15 重新核定）**：全站 208 个分类已注册 `verify` 门禁脚本，但**绝非"已全部收口"**。09-15 接手批次把"门禁注册数量"误当"收口完成"，造成三类虚假进度，已在本 §9 重排：① **683 道门禁降级为 `_selfcheck` 假门禁**（占 3121 用例 21.9%），不验证计算，其中 576 道（84.3%）连默认态假通过自检都过不了；② **`run_gates.py` 从未调用 `selfcheck_false_pass.js`**，假通过自检安全网形同虚设；③ **内容维度大量未达标**：实测 103/208 分类 0 指南、117/208 深解 0 达标（sc≥3/ex≥2/fa≥2）、16 分类缺 enmap JSON。以下为真实待办。

### 9.1 门禁真实状态（注册 ≠ 收口）

> ⚠️ **重要**：有 `verify` 门禁脚本 ≠ 分类收口完成。门禁只是 §4.1 八项目标之一；即便已注册门禁的分类，仍可能缺指南 / 深解达标 / 英文闭环。本小节仅描述门禁注册的**真实状态**，收口待办见 §9.2。

**真公式校验（runCase 模式，105 分类）**

以下分类的 verify CASES 包含真实 `expect` + `ref` 字段，main 函数调用 `runCase(c)` 注入 inputs 到页面 DOM 并断言输出子串匹配——计算结果**真实跑页面函数验证**。

accounting、acoustics、admin、advertising、aerospace、agriculture、ai、antiques、aquaculture、archaeology、baking、beauty、biz、bonding、bridge、ceramics、chemical、chemistry、chess、civil、cleaning、clinical-lab、cosmetic-derm、design、dyeing、dynamics、eco、ecommerce、economics、edu、edu2、electrical、electromagnetism、encode、energy、engineering、exhibition、fengshui、finance、fire、fishery、fitness、floral、fluid、food-processing、fun、gardening、gardening2、gas、general、geology、geometry、glass、health、healthcare、home、hotel、hr、hydraulic、insurance、investment、it、kids、kinematics、legal、life、logistics2、machinery、manufacturing、maritime、marketing、martial、materials、math、media、medical2、metallurgy、metalwork、meteorology、metrology、mining、misc2、nuclear、obstetrics、optical、optics、pediatrics、photo、psychiatry、pulmonology、quantum、realestate、reproductive-medicine、rheumatology、robotics、science、securities、signal、sports、statistics、structural、surveying、tax、tcm-pharmacy、urology

**self-check 占位 + 真 expect 待深挖（103 分类，其中 49 个有真 expect 但降级）**

以下分类的 verify CASES 被降级为 `_selfcheck` 假门禁：要么占位 `expect: ["OK"]`，要么曾有真 `expect` 但 runCase 实跑失败后被清空 inputs 降级（**未修复计算逻辑，只是不再验证**）。这些用例不验证计算正确性，且其中 576/683 连默认态假通过自检（selfcheck_false_pass）都过不了。须逐分类恢复为真实 runCase 用例，详见 §9.3 P0-1。**（已于 2026-09-15 全量还原：所有占位/空输入用例已转为真实 `inputs`+`expect` 或排除，全 206 道门禁 FAIL 0、`selfcheck_false_pass` risk=0。）**

- **有真 expect 待恢复 runCase（49）**：['accessibility', 'acupuncture', 'astronomy', 'audio', 'audit', 'automotive', 'cardiology', 'chinese-cook', 'chinese', 'clinical-nursing', 'cognition', 'construction', 'dance', 'data', 'decor', 'dentistry', 'dermatology', 'elderly', 'electronics', 'endocrinology', 'ent', 'film', 'fire-rescue', 'food-testing', 'food', 'forensic-medicine', 'forestry', 'forex', 'funeral', 'futures', 'gastroenterology', 'hematology', 'hvac', 'jewelry', 'language', 'leather', 'legal2', 'library', 'livestock', 'logistics', 'mechanical', 'medical', 'misc', 'nephrology', 'neurology', 'ophthalmology', 'rehabilitation', 'tcm-chemistry', 'tcm-diagnosis']
- **纯占位 self-check**：['banking', 'image', 'museum', 'music', 'niche', 'nutrition', 'office', 'packaging', 'paper', 'parenting', 'pet', 'pet-training', 'petrochem', 'pets', 'photo2', 'plastic', 'pr', 'printing', 'process', 'procurement', 'project', 'property', 'psychology', 'quality', 'railway', 'rental', 'research', 'restaurant', 'road', 'rubber', 'safety', 'sales', 'security', 'seismology', 'service', 'shipping', 'stage', 'startup', 'stats', 'telecom', 'text', 'textile', 'thermodynamics', 'transport', 'travel', 'tunnel', 'urban', 'usedcar', 'video', 'wedding', 'welding', 'woodwork', 'woodworking', 'yi']

### 9.2 分类收口真实待办清单（按 §4.1 维度）

> 以下为按八项目标仍有缺口的分类，**绝非"已清空"**。逐维度补齐后才算收口（判定标准见 §4.1 / §4.5）。

- **A 项 深解达标（117 分类 / 1917 页）—— 批 1 已完成，结构达标 1912/1917（99.7%）**：accounting / accessibility / acupuncture / admin / advertising / aerospace / agriculture / ai / antiques / aquaculture / archaeology / astronomy / audio / audit / automotive / baking / banking / beauty / bonding / bridge / cardiology / ceramics / chemical / chemistry / chess / chinese / chinese-cook / civil / cleaning / clinical-lab / clinical-nursing / cognition / construction / dance / data / decor / dentistry / dermatology / design / dyeing / dynamics / eco / ecommerce / economics / edu / edu2 / electrical / electromagnetism / electronics / endocrinology / energy / engineering / ent / exhibition / fengshui / fire-rescue / fishery / fitness / floral / gardening2 / home / hotel / image / insurance / jewelry / kids / legal2 / library / logistics / logistics2 / manufacturing / maritime / martial / media / medical2 / misc2 / museum / office / packaging / parenting / pet / pet-training / petrochem / pets / photo2 / plastic / procurement / project / psychology / quality / railway / rehabilitation / rental / research / restaurant / road / rubber / sales / science / security / seismology / service / shipping / sports / stage / startup / stats / tcm-pharmacy / telecom / text / tunnel / usedcar / video / wedding / woodwork / woodworking / yi（口径见下）。

> **A 项权威口径与批 1 成果（2026-09-16）**
> - **达标标准以 §4.1.4 / 第 116 行为准：scenarios ≥2 / examples ≥1 / faqs ≥2 / 无套话**（本条目原文写的 sc≥3/ex≥2/fa≥2 与该口径不一致；已收口分类 energy `(3,1,2)`、insurance `(2,1,2)` 均按第 116 行判定，可反证）。
> - **深度解析键 = `tools.json` 的 industry + basename（`_build._slug_of`），不是目录名**。按目录名扫描会把 44 条已迁移页面误判为「缺键」（如 `design/analysis-64` 的键实为 `uiux/analysis-64`）——**踩过，勿复**。
> - 批 1 成果：补 **59 条真实领域 FAQ**（jewelry 6 / kids 5 / rehabilitation 24 / tcm-pharmacy 24）；修 **39 条键名 hygiene**（用旧键内容无损复制到当前分类键，0 编造）。结构达标 **1873 → 1912/1917**。
> - **遗留**：① 5 条无源键（页面有深度块但 JSON 无源）；② 质量类缺口（不计入结构达标）：**664 页 examples 无真实算例**、184 页 examples 标题套话、9 页英文名嵌入中文。提交 `61d0516d8`。
>
> **A 项批 2 成果（2026-09-16）—— 全站结构达标 5124/5124（100%）**
> - **① 无源键回填 30 条**（`scripts/backfill_orphan_deepdive.py`）：全站扫描发现 **30 个页面有「📚 深度解析」块但 `content_deepdive.json` 无源**（不只是批 1 记的 5 条，另有 textile×4 / general×3 / metallurgy×4 / it×5 / food-testing×3 等）。这些页面下次构建会被 `_DEEP_DIVE_BLOCK_RE` 清掉旧块、因无数据不再注入 → **内容永久丢失**。已按页面 HTML 反解析为 `title`/`scenarios`/`examples`/`faqs` 无损写回，纯新增 761 行、0 删除，30/30 结构达标。**教训：批 1 只按 A 项 117 分类扫描，漏掉了其它分类的同类问题——以后先全站扫再按分类推进。**
> - **② 套话改写 77 条**（`scripts/fix_deepdive_boilerplate_{logistics,quality,rental,research,restaurant,telecom,wedding,misc}.py`）：这批深解由「一体化标准化使用示例」模板批量生成——场景全是「在XX场景里，先统一 Xxx 的输入口径…」、示例是「先准备一组典型样本并固定单位与格式…」、FAQ 是「这个 XX 工具适合什么阶段使用」。已按各页面真实输入项与 `calc()` 实现逐条重写，**所有算例数值独立复算**。对纯随机组合型生成器（`rental/generator-32`、`rental/recommender-5`）与通用描述统计页（`research/analysis-49~54`、`ecommerce/analysis-70/71`、`sports/stats-11`、`woodwork/analysis-cost-price`）**如实说明能力边界，不虚构"按人数精确推荐""自动情感分析"等不存在的功能**（老板反对伪功能的红线）。
> - **③ 补第 2 条 FAQ 26 条**（`scripts/add_missing_faq_2nd.py`）：urology 24 条 + finance 3 条，只追加 FAQ 不动其它字段。
> - **④ 清孤儿键 23 条**（`scripts/clean_orphan_deepdive_keys.py`）：逐条核对迁移后的新键已持有等同或更全内容才删（脚本自动校验，内容更少则跳过）；含 **2 条合规红线残留**：`finance/lottery-odds-calculator`（博彩）、`it/sn-generator`（序列号生成器）。
> - **成果**：全站 examples 标题硬套话 **92→0**、scenarios/faqs 套话 **57→0**、英文名嵌入中文 **14→0**；结构达标（sc≥2 且 ex≥1 且 fa≥2）**5098→5124/5124（100%）**。构建 4825 工具全 A 级，214 道门禁全过，提交 `9c9bd4162`。
> - **遗留**：`content_deepdive.json` 仍有 **299 个孤儿键**（页面已迁移到其它分类，键未同步清理）。不影响达标（孤儿键不渲染），但属数据卫生问题；**按老板"禁止擅自批量删除"原则仅报告，未删**，需确认后再清理。

> **⚠️ 门禁系统性隐患（2026-09-16 暴露）：日期型 / 随机型用例随真实日期或 Math.random 偶发挂**
> - **现象**：部署 CI 在 `fire calc`（10/11）、`livestock calc`（24/26）、`cleaning calc`（7/8）、`pediatrics calc`（24/25）、`travel calc`（18/20）五道门禁随机/漂移失败。**根因**：这些用例期望页面输出**绝对日期**（如 `2026-09-15`、`2025-09-15`），但页面用 `new Date()` 取"今天"相对推算，真实日期每推进一天，期望就过期一天（`fire/response-drill` 则是 `Math.random()` 随机选场景，6 个场景仅 5 个含"拨打119报警"，约 1/6 概率失败）。
> - **修复（均改门禁期望为与今天无关、由输入确定的子串，不动页面功能）**：`verify_fire_calc.js` 的 `response-drill` 期望 `拨打119报警`→`火灾`（6 个场景名全含）；`verify_livestock_calc.js` 的 `fattening-pig-timeline`→`预计饲养天数 38`、`withdrawal-period`→`休药期 28 天`；`verify_cleaning_calc.js` 的 `appliance-cycle`→`已到清洁周期`；`verify_pediatrics_calc.js` 的 `vaccine-schedule`→`乙肝疫苗(第1剂)`；`verify_travel_calc.js` 的 `travel-days-counter`→`8 天 (7晚)`、`world-timezone-converter`→`北京/上海`。
> - **教训**：以后新增"今天/随机"相关用例，**绝不可断言绝对日期或随机命中串**，必须断言由输入确定、与运行时刻无关的结果（如时长、计数、静态名称、状态标题）。已全量扫描 7 个含日期期望的门禁（automotive/data/elderly/hr 的日期期望为固定参考值/种子，不随今天变，无需改），剩余 date-expect 一律改为确定性断言。修复后全 214 道门禁稳定通过（各门禁多轮复跑 0 失败）。
> - **已根治（2026-09-16 收口）**：本（页面用真实 `Date`/`Math.random`）已彻底修复——`verify_it_calc.js` 的 harness 注入 **FrozenDate**（冻结基准日 `2024-06-15`，无参构造返回固定日、带参透传）**并**把 `Math.random` 替换为**确定性种子 PRNG（mulberry32，每用例前重置）**。两类漂移/随机飘（日期型 + 随机型）现对 CI/本地/任意 Node 版本完全一致、构造性确定。本次 `niche calc` 在 CI 偶发 14/15（`recommender-temp-pottery` 等随机推荐页断言随机命中串落空）即为此类，根因修复后全 214 道门禁连跑稳定通过。
> - **验证纪律（本次教训）**：之前只跑一次 `run_gates.py` 即报全绿、且未确认部署实际生效，导致 `471da89f6`(statistics)、`81c356e6b`(color-shade) 两次推送均未成功部署（前者被 `cancel-in-progress` 并发取消、后者在 niche 门禁挂掉）。**正确流程**：本地全量门禁多轮复跑稳定 → 提交 → 推送 → 必须查 Actions run 结论 + 线上落盘 MD5 比对，二者齐备才算完成，禁止"跑过即宣称成功"。
### 9.3 孤立未完成任务（按优先级）

> 跨分类 / 独立的系统性问题，可穿插推进但不替代后续验证质量深挖。

**P0 — 必须修复（本轮新发现，09-15 批次造成）**

- [ ] **P0-3 回退 §9 原"208 全收口"虚假声明**：09-15 批次将本 §9 改写为"208 全部完成基础收口 / 208/208 已收口 / §9.2 清空"，与实测（103 分类 0 指南、117 深解 0 达标、16 缺 enmap、683 假门禁）严重不符，已于本轮（2026-09-15）重新核定（见本 §9 头部与各小节）。
- [ ] **`upload-pages-artifact@v4` 移除 `include-hidden-files`**：本轮已降级 v4→v3 临时修复（Run 931）。长期方案：等 v4 加回该参数后升级，或改 workflow 不用该参数。

**P1 — 建议修复**

- [ ] **SEO Description 重复（2026-09-16 复核）**：工具页 meta description 已**零重复**（5026 页全唯一，原"69 组"已消解）。全站扫描另见 **4690 个重复组 / 9380 页**集中在非工具页（guides / industry / index / sitemap），其中大量为同类页共享模板描述（如某行业 6 篇指南同描述），属预期近似重复，**非工具页"69 组"范畴**。是否对这部分做唯一化（按页标题/核心词区分）需老板定夺，避免无价值 churn —— 暂未动。
- [ ] **`science/calc-1` 错公式已修**：原写 pH 公式（张冠李戴），实为自由落体工具，已改为 `s=½gt²`。
- [ ] **`legal/traffic-accident-compensation` 伤残赔偿系数倒置已修**：公式改为 `(11 - injuryLevel)/10`（一级=1.0、十级=0.1），verify_legal_calc.js 已补 2 防回归用例，提交 `f07e5ff0d`。

**P2 — 低优先级**

- [ ] **指南英文副本（`guides/*.en.html` 约 100 篇）清理 —— 2026-09-17 老板明确：英文指南优先级低，延后处理，后续专门开任务**：项目早改 `?lang=en-US` 单页 runtime 模式，这 ~100 篇 `*-guide.en.html` 是早期独立英文副本（git 跟踪 + sitemap 收录），属死重复页。**暂不处理**——删/改属 SEO 不可逆动作（直接影响约 100 个线上 URL 的索引与权重，处理不当会 404 掉索引）。后续专门任务须评估：① 是否下架并 301 指向 `?lang=en-US` 等效页；② 清理后须同步 sitemap.xml / `json/guides.json` / 构建产物，避免死链门禁挂；③ 须先出全量 301 规划再动，禁止直接删。记录于此，待老板指定时机单独推进（不与其它优化混批）。
- [ ] **跨分类真重复工具去重（D 全站审计，2026-09-17 启动，进行中）**：
  - **第一批**（h1 完全同名）已下架 5 个（commit `9bffc3229`，总数 4821→4816）。
  - **第二批**（h1 模糊近似 + 系统双命名）已下架 19 个「模板短名 vs 描述性专名」冗余：全站 h1 归一化模糊聚类（≥0.82）得 387 相似对 → 108 对同目录且差异仅在于「器/计/算」后缀+全半角括号，呈**机器模板命名（calc-N/rater-N/assessor-N/analysis-N/convert-N/拼音/date-diff 等）vs 描述性专名**双命名；逐对比对 calc 真实输入集，仅删「专名版为模板版输入超集（不丢功能）且无全局复用歧义」的 19 对（如 `rater-25`→留`bishop-score`、`due-date-1`→留`due-date`、`rater-3`→留`ipss-score`）；另 2 对（`calc-2`/`calc-3`）因 basename 全局 30+ 行业复用移出单列专项。commit `5057f5744`，214 门禁全过、线上删除页 404、tools.json 残留 0、总数 4816→4797。脚本 `scripts/retire_template_dupes.py`（幂等，字符级括号匹配兼容内联 `{ slug:`）。
  - **第三批**（跨目录/同目录确凿真重复，2026-09-17 晚）已下架 3 个：对全站 h1 strict 归一化聚类得 11 对同名候选，逐页比对 calc 输入集+公式系数取证实为 3 处确凿真重复（输入集相等或冗余方⊆权威方，删冗余方零功能丢失）：`materials/density-basic`（ρ=m/V 与 `science/density-physics` 输入集完全相同）→ 留 science 版；`science/z-score-calculator`（Z=(x-μ)/σ 与 `statistics/z` 输入集相同）→ 留 statistics 版；`fitness/calculator-calc-metabolism`（Mifflin+Harris 双公式 BMR ⊆ 全局复用页 `fitness/calc-2`）→ 留 calc-2。commit `00af9e70f`，214 门禁全过、线上删除页 404、tools.json 残留 0、总数 4797→4794。脚本 `scripts/retire_redundant_crossind.py`（幂等；清理逻辑修复：① chip 抓取改为精确路径+通用 `<a>` 链接含相对路径 `related-tool-card` 与跨行闭合 ② 遍历递归 `tools/**/*.html` 二级子目录）。
  - **剩余（基本完成，建议暂停/专项）**：经三批（5+19+3=27 个）下架后，全站 strict 同名仅余 11 对候选，已逐对取证——`hematology/mpn-scoring`vs`rater-5`（DIPSS 含细胞遗传学 vs MPN-10 症状问卷，异算法）、`quality/process-capability`vs`calc-cpk`（双组规格 vs 原始数据录入，实现差异大）、`edu/gpa-calculator`vs`exam-gpa-calculator`（累计 GPA vs 考试 GPA，语义微差）、`safety/accident-stats`vs`stats-report-frequency`（标准 KPI vs 通用报表）、`marketing/marketing-roi`vs`investment/roi-calc`（营销多口径 vs 投资简单 ROI，跨目录异语义）、`it/csharp-cheatsheet`vs`cpp-cheatsheet`（C# vs C++，明显异功能）均**非简单重复不下架**；其余 ~84 对为全局复用编号页（calc-N/rater-N 跨行业同名，牵连系统性命名，需单列专项）与描述性短名对（多已证为同名异功能）。继续硬删风险高，建议暂停 D 项或后续开专项。
  - **已排除（不下架，仅记录）**：同名异功能 `finance/salary-after-tax`(累计预扣)vs`payroll-calculator`(含年终奖比例)、`ophthalmology/self-assess-2`vs`osdi-scale`(OSDI 两算法)。
- [ ] **`fun` 行业图标 🎮 语义一致性（2026-09-17 复核：原条目举例不准确，降级为设计决策项）**：原记"含计算类工具（烧烤分量计算器）图标与语义不符"经实测**不成立**——`bbq-portion`/`hotpot-portion`（烧烤/火锅分量计算器）命中 TOOL_ICON_RULES 的"计算器/分量"规则，实际图标为 `🧮`（正确），并非 🎮；`convert-speed-stride`/`step-stride` 为 `🏎️`。真实情况：`INDUSTRY_DEFS['fun']=('🎮','娱乐游戏')`（行 1056）是**行业默认兜底图标**，与 `CAT_DEFS['fun']=('🎉',…)`（行 993）不一致；`tool_icon_candidates` 优先用 TOOL_ICON_RULES，仅**无专属规则的非游戏 fun 工具**（如 `fingerprint-types` 指纹演示）回退到 🎮。23 个得 🎮 的工具绝大多数是真游戏（tetris/number-guess/各记忆游戏等），命中游戏规则，属正确。**结论**：当前态可接受；若要消除非游戏 fun 工具的 🎮 兜底，需把 `INDUSTRY_DEFS['fun']` 改为 `🎉`（中性），但该改动同时改变 fun 行业页头图标与所有无规则兜底工具，**属可见设计变更，须老板拍板，未擅自改**。
- [ ] **data-zh「中文原文」容器属性损坏 —— 2026-09-16 已修 197 页（本轮新增）**：`js/tool-i18n.js` 运行时用 `getAttribute('data-zh')` 覆盖 `h2`/intro `p` 的 `textContent` 作为中文态文案，故 data-zh 里任何脏字符都**直接显示给中文用户**。无头 Chrome 取证：`design/checker` intro 显示「`>输入前景色和背景色…`」（对照正常页 `edu/exam-timer` 为「倒计时、正计时、休息提醒一体化」）。两类损坏：① **194 页 intro `<p>` 的 data-zh 前导多余 `&gt;`**（science 74/design 57/finance 57/audio 1 等，根因=mardown 引用行 `> 描述` 的引导符被带入）；② **4 页 `<h2>` 的 data-zh 被塞入转义 `<span>`**（base64-converter/jwt-parser/stock-profit-calculator/dehumidifier），英文正文另多一个 `&lt;`。修法见 `scripts/fix_data_zh.py`（幂等，`pre-commit` 可复跑）：剥前导 `&gt;`（**仅剥离开头一个**，正文中间如 `TDS&gt;5.45` 属合法内容不动）+ 4 页 h2 按「页面 `<title>` / i18n `zh-CN.title`」权威源重写、图标沿用页面原有（不取 meta icon，后者只是占位）。**未处理 46 条 B 类**：data-zh 内含真实 HTML 标签 / JS 模板（`<strong>…${map.size}` 等），属运行时动态文案模板，非损坏。
- [ ] **`psychiatry.json` 并行进程未提交改动**（mtime 2026-09-13）：需老板确认归属。

---

## 十、反模式与防复发（血泪教训 · 2026-09-17 复盘固化）

> 本章记录**主 agent 自己挖过的坑**。共性根因只有一句：**动手前拿"我以为的结构"当依据，而不是先验证；且对"爆炸半径"验证不足。**
> 铁律：**任何"完成"结论 = 门禁真跑 + 产物落盘比对双证据。口头打包票一律视为未做。**

### 10.1 假门禁 / 虚假"全收口"声明（最严重 · 09-15）
- **犯错**：把"门禁注册了 + 跑绿"当成"已验证收口"，683 道门禁用占位 expect / 缺 `_selfcheck` 标记空跑通过，还对外声明"208 全部收口"。
- **根因**：**"跑了"≠"过了"** —— 没验证用例是否真正触发页面计算逻辑就报通过。
- **防复发**：报绿灯前必须确认 ① 用例有真实 inputs；② expect **独立复算**（严禁取页面自身输出当期望，那是自证循环 = 假门禁）；③ 随机/二进制不可派生页须登记 `_unverifiable.json` 排除，不得凑数。

### 10.2 门禁随机飘（CI 偶红 · 09-16）
- **犯错**：写新用例时用 `Math.random` / `Date.now` 当输入、未种子化，本地绿、CI 随机红。
- **防复发**：非确定性输入一律种子化（`mulberry32` 每用例重置 / `FrozenDate` 冻结基准日），门禁**可重现**才准提交。

### 10.3 批量改页面的正则炸雷（09-17 · retire 系列）
- **犯错**：清理脚本 link 正则 ① 错写成 `tools/<slug>/<slug>.html`（真实是 `tools/<ind>/<slug>.html`，ind≠slug）② 只扫 `tools/` 顶层，漏掉 `tools/<ind>/` 子目录 ③ 贪婪 `[\s\S]*?</a>` 跨行匹配差点吞掉 JS 多行字符串 → **险些误改 `tools/psychology/*` 10 个文件**（靠 `git diff` 在提交前逮到并 `checkout` 回退）。
- **防复发**：批量改前必 **dry-run + 逐文件 diff 预览**；改完必做 `grep -rIl` 全仓"残留引用复核"；遍历一律递归 `**/*.html`，路径一律按 `ind+slug` 精确构造（禁子串 glob，防 `rater-3` 误伤 `rater-30`）。

### 10.4 清理文档漏删"已完成"标记（09-17）
- **犯错**：第一遍只删了 `✅ 已收口` 归档章，漏掉待办区里打成**删除线**的 `- [x]` 完成项（老板当场指出）。
- **防复发**：清理"已完成"须**同时 grep 全部标记变体**：`✅` 归档块 + `- [x]` 勾选 + `~~` 删除线，只认一种必漏。

### 10.5 反伪工具自身的假绿（2026-09-17 深审发现 · 本节最重要）
- **发现**：`selfcheck_false_pass.js`（已接入 `run_gates.py:271` anti-regression 门禁）报 `risk=0`，但它有**两个盲区**：
  - 盲区1：文件头注释第 15–16 行声明"用例无有效 inputs 判 RISK"，但 `isFakeStruct()` **从未调用 `hasRealInputs()`** —— 该判定实际从未生效。
  - 盲区2："用例注入值 == 页面默认值"未检测 —— 框架编译期已跑过一次默认态 `calc()`，注入失败时默认结果恰好命中期望 → 假通过（项目记忆中的头号机制）。
- **实测**：3031 用例中 **783 例（26%）无判别力** —— `no_inputs=230`（根本没注入）、`all_default=553`（注入值＝页面默认值）。抽查 4 例（含作为范例的 `science/newtons-second` m=10/a=3）均证实撞默认值。
- **已修**：`selfcheck` 补上两项检测 + 建基线 `scripts/falsepass_baseline.json`（230/553/3031）—— **存量入基线只准降不准增，新增弱用例立即让门禁红**；反向验证（压低基线至 229）确认退出码 1，是真门禁。
- **存量分批专项（进行中）**：改 expect 若取自页面自身输出即"自证循环"，正是 10.1 的假门禁老路；正确修法须**逐例按标准公式独立复算**，故分批推进。
  - **第一批 statistics（2026-09-17，39 例全部清零）**：39 例全为 `all_default`。做法——用 Python 按标准公式**独立复算**新 expect（换成非默认输入）；p 值类（单样本 t / F 检验）用**数值积分独立实现**，并先用两个已知 p 值做精度校验（t: 0.327287 vs 已知 0.3273；F: 0.359728 vs 已知 0.3597），校验通过才投入复算；落盘后实跑 `verify_statistics_calc` **39/39 通过**（页面实现与独立复算互证）。statistics 弱用例 **39 → 0**，全站 **783 → 744**，基线棘轮下调 `all_default` 553→**514**。
  - **第二批 energy（2026-09-17，29 例全部清零）**：29 例全为 `all_default`，均为标准物理/工程公式（P=UI、卡诺效率、导热 Q̇=kAΔT/d、LCOE、P=½ρAv³、阶梯电价、碳足迹因子表等）。做法同第一批：Python 独立复算 + 换非默认输入；**新增一条强断言**——因 verify 框架是「expect 任一命中即通过」，故逐例断言「新 expect ∩ 默认输出 = ∅」，从机制上杜绝残留假通过。落盘后实跑 `verify_energy_calc` **30/30 通过**。energy 弱用例 **29 → 0**，全站 **744 → 715**，基线棘轮下调 `all_default` 514→**485**。
  - **本批改造顺带查出 2 个真实缺陷（未擅自改页面，待定夺）**：① `energy/air-purifier-area` 的 `recArea = cadr × 0.1` **硬编码**，用户可调的 `factorInput`（0.05–0.15）**完全未参与计算**，仅用于展示——用户输入 0.08 仍按 0.10 出结果；② verify 框架兜底调用的 `DESTRUCTIVE` 正则未拦 `set*` 类函数，`setCadr()` 被无参调用把输入置为 `undefined`→0。二者已记入 §10.6。
  - **剩余 489 例**（`no_inputs=213` / `all_default=276`）待后续批次，按"公式可可靠独立复算 + 页面存在可注入控件"两条同时满足的分类依次推进。**选批前必做可注入性预筛**（第十四批教训：psychiatry 22 例里 18 例是纯点击答题页，无可注入控件，白跑一半）。截至第十六批的可注入性实测（弱用例数 / 页面含静态表单控件数）：pulmonology 14/14、advertising 12/12、dyeing 12/12、dermatology 14/11、engineering 14/11、signal 11/11、design 10/10、rheumatology 14/9、endocrinology 10/9、mining 10/9、gas 9/9、mechanical 9/9、travel 9/7、gardening 8/7、finance 7/7、sports 7/7、fire 7/6、chemical 9/5、cleaning 7/5 —— 下批建议取 **pulmonology 14**（`ecommerce 17` 已于第十六批收口；实测 ecommerce 收口 23 例：14 all_default + 8 回显型 + 1 阈值回显）。

### 10.6 弱用例改造顺带查出的真实缺陷（2026-09-17 · 改造即体检）

弱用例改造的价值不止于"让门禁有判别力"——**把用例输入改成非默认值后，长期被默认值掩盖的页面缺陷会立刻暴露**（此前这些页面"看起来正常"，只因没人真正改过输入）。本批 energy 29 例即查出 2 个：

- **缺陷 A（页面功能 bug）`energy/air-purifier-area`**：`recArea = cadr × 0.1` 为**硬编码**，用户可调的 `factorInput`（0.05–0.15）**完全未参与计算**，仅在展示文案里回显。后果：用户输入系数 0.08，结果仍按 0.10 输出 —— 输入无效、结果误导。
  - **状态（2026-09-17 已修）**：老板授权后已修复，采用**零回归**方案 —— `min = cadr×(factor−0.03)`、`rec = cadr×factor`、`max = cadr×(factor+0.02)`，并钳制 `factor ∈ [0.02, 0.30]`；默认 `factor=0.10` 时结果与修复前**逐位一致**（28/40/48/4.2/96）。展示文案的硬编码系数同步改为动态；条形图 `maxRef` 由固定 96 改为 `max(96, maxArea×1.05)`。另加 `setCadr()` 无参保护（`typeof val !== "number" || !isFinite(val)` 时直接 return），作为缺陷 B 的页面侧低风险加固。
  - **验证**：用例改为取**非默认系数 0.12**（`cadr=550` → 66.0 / 49.5 / 3.5 次），并做了**反向验证** —— 临时把 `recArea` 改回硬编码 0.1，用例立刻由 30/30 变为 29/30（退出码 1），恢复后回到 30/30。
- **缺陷 B（验证框架隐患）`scripts/verify_it_calc.js`**：第 3 步"兜底调用所有函数"用 `DESTRUCTIVE` 正则排除破坏性函数，但该正则只拦 `reset|clear|restore|save|swap|history`，**未拦 `set*` 类设值函数**。`air-purifier-area` 的 `setCadr()` 因此被**无参调用**，把 `cadrInput.value` 置为 `undefined` → `parseFloat → NaN → 0`，直接破坏已注入的输入。
  - **影响面**：只要页面存在 `setXxx()` 且无参调用会写输入，同类破坏就会发生；当前因第 2 步命中即 return，多数用例未受影响，属**潜伏隐患**。
  - **状态**：未改框架（改它会影响 200+ 脚本的兜底判定，风险面大）。
  - **待定夺**：是否在 `DESTRUCTIVE` 中补充 `set*` 模式（需先评估对全量 214 门禁的影响，属专项）。
- **缺陷 C（页面交互失效，第十批查出）`food-processing/sterilization-f-value`**：输入区由 `renderParams()` 动态 `innerHTML` 生成（`#T/#Tref/#Z/#t` 等），但这些 `<input>` **均未绑定 `oninput`**（同页 `renderModes()` 的模式按钮有 `onclick=...calc()`，故切模式会重算，掩盖了问题）。后果：**用户修改杀菌温度/时间后结果不更新**，除非再切换一次模式——典型「看起来正常、实则输入无效」缺陷。
  - **判定依据**：verify 用例注入 `T=110/t=40` 后 `via=calc`（走框架兜底调用）而非 `via=input event`——`input/change/keyup` 三事件均无监听者，直接证实输入未绑定重算。
  - **状态**：未改页面（本批为脚本批，不擅自改线上）。同类页面（`blanching-conditions`/`filling-volume`）的动态输入**有** `oninput="calc()"`，可作修复参照。
  - **待定夺**：是否给该页 3 个模式分支的动态 input 补 `oninput="calc()"`。
- **缺陷 D（页面无效输入 / 占位功能，第十一批查出）`hr/tracking-hours` 与四例「通用双输入」页**：
  - ① `hr/tracking-hours`：`deadline`（培训截止日期）与 `dept`（部门）两个输入框**完全未参与计算**——`calc()` 只读取 `required`（要求学时）；`dept` 取值后从未使用，`deadline` 根本没被读取。后果：**用户填写部门/截止日期对结果零影响**，属装饰性伪输入。
  - ② `hr/bandwidth-1`（标题「薪酬（带宽/分位/公平性）设计」）、`hr/calc-81`（「内推（激励/流程/效果）计算」）、`hr/eap-xinli-zixun-weiji-ziyuan`（「EAP（心理/咨询/危机）资源」）、`hr/hris-zizhuyuaiduibijisuanqi`（「数字化（HRIS/自助/AI）设想」）四页共用一套「按 `h1` 正则选择计算模式」的模板，但标题**均未命中模板内任一模式正则** → 全部落入兜底分支，只输出「总和 / 差值 / 比值 / 较大者」等**通用双数运算**，与标题宣称的业务功能无关（占位现象）。同模板、标题含「得分」的 `hr/performance-ranking` 命中评分分支，但输出仅「总分/平均分」，与「归一化与排名」亦名不符。
  - **状态**：涉及页面内容重做（超出脚本批范围），本批未动线上 HTML，仅登记待定夺。
- **缺陷 E（页面核心计算失效 / 结果与输入无关，第十二批查出）`metallurgy/hardness-conversion`**：`interp(x, xs, ys)` 的实现假设 `xs` **递增**（先判 `x<=xs[0]` 取首值、`x>=xs[last]` 取末值，再线性插值），但 `buildAxis()` 传入的 `xs` 取自 `DATA` 表**首列**（HRC 列，按硬度由高到低排列）→ **递减**。后果：对**任意落在轴范围内的输入**，`x<=xs[0]` 恒真 → 恒返回首行 `ys[0]`，即 `inVal=45` 与 `inVal=60` 输出完全相同的 `68.0 / 760 / 940 / 2820`；仅当 `inVal` 大于首轴值（68）时绕开该分支、又因区间判断 `x>=xs[i] && x<=xs[i+1]` 在递减序列下永不成立而返回 `null`，卡片显示 `-`。
  - **影响**：硬度换算表的核心功能（按输入插值换算）**实际未生效**——用户输入 20~68 之间任意值都得到 68 HRC 的同一结果；`refTable` 全表展示正常，掩盖了交互失效。
  - **状态**：未改页面（本批为脚本批）。修法：`buildAxis()` 返回前把 `xs` 及其伴随列统一按升序重排（或在 `interp()` 内先判方向），属页面侧改动，待定夺。
- **缺陷 F（页面名不符实 / 三页同一占位实现，第十三批查出）`clinical-lab/analysis-8`、`clinical-lab/analysis-9`、`clinical-lab/analysis-density-2`**：三页标题分别为「血气分析（pH/PaO2/PaCO2）代偿判断」「电泳图谱（血清蛋白）区带分析」「精液分析（密度/活力）参考」，但三页**共用同一段与标题毫无关系的通用描述统计实现**——单个 `<textarea id="data">` 输入一串数字，输出「数据量/总和/平均值/中位数/最小值/最大值/极差/方差/标准差」九项。既没有血气代偿公式（Winter 公式等），也没有电泳区带百分比换算，更没有精液密度/活力判读；即用户按标题来用，得到的是与临床检验无关的通用统计。同类现象另见 §10.6 缺陷 D 的 hr 四页「通用双输入模板」。
  - **判定依据**：三页 HTML 体量均约 14KB（同目录其它工具页 18–25KB），`calc()` 逐字相同（仅 `<title>`/`<h1>` 不同）；且本批 origin 用例的 expect 为 textarea 回显 `80_X`，即原用例根本没验证过任何计算结果。
  - **状态**：未改页面（本批为脚本批，仅将 expect 改为均值/方差独立复算值使门禁具备判别力）。修法：按标题重做三页内容（复用同目录 `blood-gas-analysis`/`electrophoresis-analysis`/`semen-analysis` 的已有实现），或下架三页并清理 `json/tools.json` + i18n 双键，属页面/内容侧改动，待定夺。
- **缺陷 G（页面无可注入控件 → 门禁无法验证，第十四批查出）`psychiatry/` 18 个量表页**：`aq-autism`、`asrs-adhd`、`bis11-impulse`、`cage-substance`、`cdrisc-resilience`、`cssrs-suicide`、`eat26-eating`、`gad7-anxiety`、`isi-insomnia`、`les-stress`、`lsas-social`、`mdq-bipolar`、`panss-schizophrenia`、`pcl5-ptsd`、`pdss-panic`、`phq15-somatization`、`phq9-depression`、`ybocs-ocd`。
  - **现象**：这些页一律采用「选项即 `<span class="q-opt" onclick="pick(i,j)">` + 答案存**内存数组** `A`（`les-stress` 为对象 `sel`）」的纯点击答题交互，**整页没有任何 `<input>`/`<select>`/`<textarea>`**，`calc()` 只读内存数组、不读 DOM。后果：**门禁无法注入任何输入**（`getEl` 只能按 id 即席造元素，而页面从不按 id 取答案）——只能断言默认态「已作答 0/N 项，请继续完成剩余题目」这类**页面自身默认输出**，属结构性弱用例（本批 18 例保留 `no_inputs`）。
  - **影响**：① 验证维度缺失（18 个工具的计算逻辑全站无自动化覆盖）；② 该交互对**键盘/无障碍**不友好（`span` 不可 Tab 聚焦、无 `role`/`aria`、无法用系统级表单自动填充）；③ 无 `form` 语义，答案不进 DOM，任何"填表/批量测评"类扩展都做不了。
  - **状态**：未改页面（本批为脚本批）。修法（页面侧）：把选项渲染为 `<input type="radio" name="q{i}" value="{j}" onchange="calc()">`（或 `<select id="q{i}">`），`calc()` 改读 DOM——**一处小改同时解锁「可验证 + 可键盘操作 + 可自动填表」三项收益**；改造后本批 18 例可一次性转为「非默认输入 + 独立复算 expect」。待定夺。

**方法论沉淀**：弱用例改造 = 给全站工具做一次"真实输入体检"。每批改造都会顺带产出缺陷清单，应逐条记录、交由老板定夺，而非由 agent 顺手改线上页面。

### 10.7 「逃生项」——比撞默认值更隐蔽的假通过（2026-09-17 · 第三层假门禁）

**机制**：verify 框架判定为「`expect` 任一命中即通过」（`verify_it_calc.js`）。此前已防住「撞默认值」（§10.5），但那不够——
**只要 `expect` 里混入一个「不依赖被测输入」的项，输入注入即使完全失败，用例照样 PASS。这样的项叫「逃生项」。**

**为什么「零交集断言」防不住它**：零交集只保证「新 expect 不在默认输出里」。但页面常常**部分使用输入、部分硬编码**——
此时被注入的那部分输出确实不在默认输出中（零交集通过），而**被测点本身没变**，用例却无从察觉。

**实测（本批）**：statistics+energy 共 68 例改造，全部通过零交集断言，但判别力验证器跑出 **6 例在注入失败时仍 PASS**：

| 用例 | 逃生项 | 为什么它是逃生项 |
|---|---|---|
| `statistics/statistics-11` | `1.0000`（权重和） | 默认权重和也是 1.0，与输入无关 |
| `statistics/iqr` | `35.0000`（中位数） | 默认态的 **IQR** 恰好也是 35 —— 同一数字、不同含义 |
| `statistics/relative-risk` | `2.0000`（RR） | 默认 RR 恰好也是 2.0 |
| `statistics/one-sample-t-test` | `24`（df） | n 未变 ⇒ df 不变，与被测的 t 值无关 |
| `statistics/chi-square-test` | `2`（df） | 同上，且 `"2"` 是极易误命中的超短串 |
| `statistics/statistics-13` | `18.6667`/`4.3205`（方差/标准差） | **等差数列的离差平方和只与步长有关** —— 换了整组数值但步长不变，方差纹丝不动 |

**铁律（写死，后续每批必须执行）**：
1. **`expect` 的每一项都必须依赖被测点。** 不得混入只依赖其它输入、或与被测点无关的中间量（df、样本量、求和系数、固定换算常数等）。
2. **避免超短 expect 串**（如 `"2"`、`"24"`），子串 `includes` 极易误命中。
3. **改造后必须跑判别力验证器**：`node scripts/discriminate_check.js [脚本名]`（模拟注入失败，用例应全部变红）。全站仅约 1 秒。
4. **关键用例必须做反向验证**：临时把被测逻辑改回错误实现，确认用例**真的会红**（本批 `air-purifier-area` 正是靠这一步发现 expect 有逃生项 —— 首轮反向验证时它 30/30 仍绿）。

**已固化为门禁**：`scripts/discriminate_check.js` 已接入 `run_gates.py`（anti-regression 项），配 `scripts/discriminate_baseline.json`（`escape=78` / `checked=1872`）——
**只准降不准增**，且**下降时也必须同步下调基线**（强制棘轮，防止悄悄回涨）。已做三向反向验证：78=78→exit 0 / 基线 77（新增）→exit 1 / 基线 79（下降未更新）→exit 1。

**存量与分批清理**：全站 1872 例已检，1794 例判别力有效，初始 **78 例含逃生项**。

**第二批（2026-09-17，78 → 48）**：先用「逐项二分」精确定位逃生项——对每个用例把 `inputs` 换回页面默认值，再对 `expect` **逐项单独**跑 `runCase`，仍 `ok` 的即逃生项（注意：不能用单一 `fullBlob` 判定，框架 `ok` 可能来自第 2 步的 `blob1` 而 `fullBlob` 是最后一步的 blob，元素集合不同，会全判为"无逃生"）。
  - 分类结果：**45 例 expect 全为逃生项**（须改 inputs 让输出真正变化，等同弱用例改造工作量，留专项）+ **33 例部分逃生**（删项即可）。
  - 本批处理 33 例，删掉逃生项后**暴露 5 例原 expect 本身写错**（此前全靠逃生项蒙混过关），已按独立复算修正：
    `ai/softmax` 12.71→**12.70**（e^0.5/Σ=1.6487/12.977=12.703%）；
    `hydraulic/calc-26` 5.158→**5.159**（Q=A·V=6.375×0.80918=5.15853，第4位为5须进位）；
    `legal/child-support` `624000`/`4000`→**`624,000`/`4,000`**（漏千分位逗号，页面输出带逗号）；
    `marketing-roas-calculator` `75.00`/`30000`→**`75.0%`/`30,000.00`**；
    `marketing/calc-price-elasticity` -1.73→**-1.727**（中点法 18.18%/−10.53%）。
    五例均已独立复算确认**页面公式正确、是 expect 写错**，非改页面。
  - 基线棘轮下调 `escape` 78→**48**。剩余 48 例多为 nutrition 5 / machinery 5 / legal 4 / signal 3，    其中约 45 例属「expect 全为逃生项」，须改 inputs + 按公式独立复算，留专项。

**第三批（2026-09-18，48 → 0 · 逃生项清零）**：剩余 48 例全部分类处理，逐例读页面公式/模板 → 改非默认输入 → 按公式独立复算 → `discriminate_check.js` 验证变红。

| 类型 | 数量 | 处理口径 | 代表 |
|---|---|---|---|
| 随机生成器（只有 `cnt` 一个输入、原 expect 是静态标题） | 13 | 断言**条数或末条**：`"8. "`（带序号模板）/ `"共 8 组"` / `"共 8 张"` / `"#8"` / `"8 00:"` | nutrition×5、acupuncture、advertising、beauty、data、food-testing、image、library、music、niche、psychology、rental、seismology、travel |
| 输入与默认**数值巧合**（比值/乘积相同） | 6 | 换一组不成比例的输入 | `signal/carrier-freq`(1200/800 中点=默认 1010/990)、`snr-db`(100/1 比值=默认 10/0.1)、`structural/radius-of-gyration`(2e-6/2e-3 比值=默认)、`chemistry/boiling-point-elevation`(0.512×0.5×**2** = 默认 0.512×1×1)、`marketing-roas`(10000/40000 比值=默认)、`chemistry/empirical-formula`(2,4,2 与默认 3.33,6.65,3.33 **同为 1:2:1**) |
| 输入**只喂给了不被读取的通道** | 4 | 改到真正参与计算的输入 | `machinery/estimate-gravity`（`density` 是 number input，页面实际读 `material` select）、`machinery/temp-hardness`（`maxHrc` 仅 `grade=custom` 时生效）、`machinery/calc-64`（最大间隙 `(ES−ei)/1000` 与 `basic` 无关 → 改断言孔最大极限 `D+ES/1000`）、`machinery/strength-15`（节距只依赖 `n1`，与 `P` 无关） |
| expect 是**输入回显/静态串** | 3 | 删回显项，改断言计算结果 | `ai/sigmoid`（`"正类"`/`"2.0000"`）、`biz/checker-8`（`"88"` 是 csat 回显）、`legal/*`（`"100%"`/`"10%"` 只依赖伤残等级） |
| select 无默认值 → 注入失败时**仍留在用例值** | 4 | 改到有默认值的输入上 | `obstetrics/heart-rate`(decel)、`reproductive-medicine/endometrial-receptivity`(pattern)、`testicular-volume`(leftP/rightP Prader 通道) |
| 页面**源码字面量**导致假命中 | 2 | 断言改为「计算值 + 单位/上下文」的完整串 | 见 §10.8 |

顺带修正的页面/用例真错：`legal/calc-interest` 原 expect 写的是默认 `rate=12` 的结果（`¥112,000`/`¥12,000`），与它自己的 ref（10% → 110000）**自相矛盾**，已按 150000×10%×1 复算改为 `¥165,000`/`¥15,000`。

### 10.8 两个新增易踩坑（2026-09-18 · 第三批实测）

1. **页面 JS 源码里的字面量也会被计进 blob。**
   `collectStrings` 收集的是元素 `value`/`innerHTML`，其中含**脚本片段**。所以「页面源码里出现过的字符串」不能拿来当 expect：
   - `stage/power-load`：expect `"30.4"` 恒命中——深度解析示例里有「总功率 **30.40** kW」（`30.4` 是 `30.40` 的子串），与计算毫无关系。改成完整串 `"总电流： 30.4 A"` 才真判别。
   - `library/generator-label`：数据池 `code:'CW-2023-018'` 是源码字面量，单独断言档号恒命中；须断言**组合后的输出串**（含年度/保管期限/档号）。
   - 判据：改完 expect 先 `grep -c "该串" tools/<slug>.html`，命中就换更长的上下文串。

2. **判定发生在 `blob1`（注入后立即收集），不是最终的 `fullBlob`。**
   随机生成器页面在**编译期**就跑过一次 `gen()`（用默认 `cnt`），注入后又跑一次——两次共用同一条确定性 PRNG 序列。
   因此「断言第 N 条」时，注入失败态的 blob1 里会有**序列后段**的条目：
   `library` 断言第 8 条（`cnt=8`）时，注入 `cnt=5` 的 blob1 恰好包含序列第 6–10 条，其中就有第 8 条 → 仍 PASS。
   解法：把 `cnt` 拉大到 **20** 并断言**末条**（序列第 20 项，绝不在前 10 项内）。
   - 推论：用 `runCase(..., expect:["@@NOMATCH@@"]).fullBlob` 观察到的输出**不等于**判定用的 blob1；定位逃生项时不要只信 `fullBlob`。

3. **同文件并行 Edit 会互相覆盖。** 本批对 `verify_signal_calc.js` 一次并发发 3 条 Edit，结果只落了 1 条（另 2 条静默丢失），`discriminate` 复检才暴露。
   **同一个文件的多处修改必须串行 Edit，或改用单条脚本一次性改写。**

### 10.9 弱用例改造口径与新增坑（2026-09-18 · 第四批）

**第四批成果**：health 23 + civil 21 + electrical 16 = **60 例** all_default 弱用例清零（基线 485 → 425）。

**第五批成果（2026-09-18）**：hydraulic **16 例** all_default 弱用例清零（含 calc-26 / calc-1 两例本已含一个非默认键、18 例全部 `via=input event` 通过），基线 425 → **409**；判别力 0 逃生项。修正一处逃生项：`calc-protection` 的 expect 含恒定文案「间接水锤」（默认/非默认同值，回退默认仍命中）→ 改为随输入变化的 ΔH(`61.16`)/ΔP(`600.0`)。`ratio-24` 液压伺服公式页内自洽（F/A/D/Q 互验一致），expect 取页面输出、ref 标注逐项独立复算 F=m·a、D=√(4A/π) 一致。

**第六批成果（2026-09-18）**：general **15 例** all_default 弱用例清零（含 calculator-calc-10 / calc-13 两例本就非全默认、17 例全部 `via=input event` 通过），基线 409 → **394**；判别力 0 逃生项。修正一处逃生项：`voltage` 的 expect 含「600.0 线能量 E」，但 E=P/v 在默认(6000/10)与改后(12000/20)下巧合同为 600 → 假命中，改为随输入变化的「12000 束功率 P」与「2.39e+4 功率密度」。

**第七批成果（2026-09-18）**：pediatrics **16 例** all_default 弱用例清零（`verify_pediatrics_calc.js` **24/24** 通过、`via=input event`；基线 394 → **378**）；判别力 0 逃生项。本批同时**修复 `discriminate_check.js` 漏读 `<select>` 默认值**的根因（旧 `pageDefaults()` 只抓 `<input>`，导致 hirschberg-test 的 fixing/reflex 永远无法"换回默认"而被误报逃生项——实为校验器盲区，探针实测默认「正位」/非默认「明显眼位偏斜」真实有效），并**连带收紧 11 例存量逃生项**（ost/ingredient-sorter/recipe/wedding/gfr/nbc/legal/pr/assessor-38/assessor-39/stats），含两处新踩坑：① `vaccine-schedule` 的 expect「已接种」命中页面**恒定图例**「绿色=已接种…」（恒存在）→ 改随输入变化的行串「预防：乙型肝炎 已接种」；② `stats` 的 alpha=0.05 是 select **默认 selected 值**且会撞 IQR「0.057」子串 → 改用非默认的 0.1 并避撞 `2 桌`⊂`12 桌`、`140.00`贷款额与利率无关。全站 escape 保持 **0**。

**第八批成果（2026-09-16）**：urology **14 例** all_default 弱用例清零（`verify_urology_calc.js` **24/24** 通过、`via=input event`；基线 378 → **364**）；判别力 0 逃生项（19 例注入失败均变红）。本批同时修 5 例破损/退化/失效：`calc-1` / `iief5-score` 模板字符串破损（数字在 `<strong>` 内须用空格感知串 `21 分（0-35 分）`、`IIEF-5 总分：15 / 25`）、`hematuria-differential` / `hydrocele-assessment` expect 退化匹配自身输入值（改 `肾小球性血尿` / `60 mm`）、`stone-composition` `no_inputs` 失效（注入 `search:"zzz"`→`未找到匹配的结石成分`）。三例判别力逃生项收紧：`urine-flow-rate` 原 `8.0 mL/s`⊂`18.0 mL/s`→`梗阻可能`；`turp-parameters` 原 `TURP(单极电切)` 仅依赖 method 默认不换回→`48 分钟`（依赖 vol）；`stone-size-assessment` 原 `2%`⊂`42%`→`自发排石率低`（prob<30 策略文本，回退 42%/75% 输出均无此串）。**新踩坑（防复发）**：`discriminate_check.js` 的 `pageDefaults()` 抓 `<select>` 默认值时，正则 `<option[^>]*\bselected\b[^>]*value=` 只认「selected 在 value 之前」，对 `value="distal" selected`（value 在前）fallback 到首个 option 误取 `renal` → 该校验器对「注入首个 option」的 select 用例永不回退、会误报/漏判；本批用 expect 收敛规避，未动校验器（避免波及全站基线）。**门禁棘轮补刀**：`selfcheck_false_pass.js` 复核发现 `penile-rigidity`（`ehs:1` 误等于校验器误取的首 option）与 `uti-diagnosis`（`count:"high"` 即 select 真实默认）两例重写后仍判 `all_default`，已改 `ehs:2`+NPT(2/8/60) 与 `count:"mid"` 真正去默认化；全站 `all_default` 终回落至 364 = 基线（24/24 + 判别力 0 逃生项保持）。

**第九批成果（2026-09-18）**：realestate **14 例** all_default 弱用例清零（`verify_realestate_calc.js` **24/24** 通过、`via=input event`；基线 364 → **350**）；判别力 **24/24 变红、0 逃生项**。范围：`calc-1`×2（80万/5.0%/20年 → 总利息 467,115.02 / 401,666.67）、`calc-2`×3（180万/6500/9000 → 年租金 78,000.00 / 毛 4.33% / 净 3.83%）、`down-payment`×3（250万/35%/25年/4.8% → 首付 875,000 / 贷款 1,625,000 / 月供 9,311.2）、`fund-loan`×2（6万/25倍/2000/8年 → 按余额 ¥1,500,000 / 建议可贷 ¥192,000）、`calc-70`×2（8000㎡/6000万/3.0 → 楼面地价 2,500 / 溢价率 50.00%）、`calc-return`×2（NAV12/9.8/DPU0.55 → 股息率 5.61% / 资本化率 4.58%）。全部 expect 由 Python `Decimal` 高精度独立复算，并逐串核验**不与页面「深度解析」源码字面量 / 静态参考值碰撞**（`calc-70` 深解含 `2000`、`calc-2` 深解含 `3.0%`/`2.6%`/`3.26%`、`calc-return` 深解含 `5.26%`/`4.76%`，均已避开）；未发现页面真缺陷。**口径提示**：本批 `pageDefaults()` 对 `calc-2`（summary 网格）与 `down-payment`/`fund-loan`（data-grid）的实参与判决均取「输入注入后立即收集的 `blob1`」，数字与标签分处不同 `<div>`、以单空格分隔，断言取纯数值（`78,000.00`）或带 `¥` 前缀（`¥1,500,000`）均可稳定命中。

**第十批成果（2026-09-18）**：food-processing **14 例** all_default 弱用例清零 + **1 例** `no_inputs` 转真输入（`verify_food-processing_calc.js` **21/21** 通过；基线 all_default 350 → **336**、no_inputs 230 → **228**，与 selfcheck 实测一致）；判别力 **15/15 变红、0 逃生项**。范围：`dough-absorption`（吸水率 68.8%）、`emulsion-stability`（ESI 75.0%）、`fermentation-brix`（ABV 9.33%）、`filtration-rate`（滤液 1687.09 L）、`freeze-thaw-loss`（失水率 10.00%）、`homogenization-pressure`（粒径 1.205 μm）、`oil-absorption-rate`（吸油率 28.5%）、`ph-adjustment`（柠檬酸 0.039 g）、`quick-freeze-time`（冻结 153.5 min）、`residual-oxygen`（终氧 10.00%）、`shelf-life-aslt`（701.5 天）、`smoking-concentration`（1458.33 mg/m³）、`spray-drying`（实际出粉 352.6 kg/h），全部由 Python 高精度独立复算并核验不与深解算例字面量碰撞。**同时修 5 例破损/回显/依赖兜底副作用的用例**：① `blanching-conditions` inputs 是从 HTML 模板误抓的注入残骸（`"' + e.Dref + '"`）→ 改真值（n=2/T=90 → 12.56 min）；② `filling-volume` expect 为恒定文案「灌装量」→ 改数值（dia=80/h=150 → 754.0 mL）；③ `sterilization-f-value` expect 为恒定文案「安全基准」→ 改 F 值（T=110/t=40 → 3.105，**该页 `renderParams` 动态生成的 input 未绑 `oninput`，用户改数值不重算 = 真交互缺陷，见 §10.6 待定夺**）；④ `material-balance`（inputs 为空 → 判定走兜底，`delIn/delOut` 被无参调用会删行，`87.50%` 是**删行后破坏态**而非默认态）→ 改默认态真值 `88.89%`（180/160 得率），**该页输入为动态行内 input 无 id、不可按 id 注入，故保留 `no_inputs`**；⑤ `recipe-cost-calculator`（`via=delRow`，`0.0060` 同为兜底 `delRow` 删行后破坏态）→ 改真值 `0.0081`（总成本 ¥12.1559 ÷ 1500 g）。**新踩坑（防复发）**：① 无 id 的动态行内 input（material-balance/recipe-cost-calculator 的行填写区）**只能由兜底阶段驱动**，而兜底会无参调用 `delIn/delOut/delRow` 等**未被 `DESTRUCTIVE` 正则拦截的删除函数**（正则只拦 `reset|clear|restore|save|swap|history`），使输出落到「删行后的破坏态」——此类用例若 expect 命中破坏态值即假通过，须改为「默认态真值」并让 `blob1` 命中（`via=input event`）；② 文案型 expect 必须先查**默认态 advice 是否含该串**：`water-activity` 的「需防霉」在默认 aw=0.85 的 advice「部分酵母霉菌可生长，需防霉」中同样出现 → 恒命中逃生项，改用稳定性等级独有串「较稳定」（aw=0.62）；③ **`selfcheck_false_pass.js` 的 `_pageDefaults` 读全文（含 `<script>` 内的 `renderParams` 模板字符串）**，故「输入区由 JS 动态渲染」的页面（`filling-volume`/`sterilization-f-value`）其模板默认值同样参与 `all_default` 判定——这与「截断 `<!-- TOOLBOX-DEEP-DIVE -->`」的扫描口径**不一致**（本批用后者漏判了 `filling-volume` 1 例，导致基线一度误设 337，经全量 selfcheck 实测 336 后修正）。凡自建诊断脚本，须与 selfcheck 保持同口径（全文、逐键、支持 textarea），否则会漏判。

**第十一批成果（2026-09-18）**：hr **13 例** all_default 弱用例清零 + **8 例**「expect 命中注入值回声 / 兜底破坏态」的无效用例改进（`verify_hr_calc.js` **21/21** 通过；基线 all_default 336 → **323**，no_inputs 228 不变）；判别力 **17/17 变红、0 逃生项**（另 4 例 textarea 用例被 `discriminate_check.js` 计入「跳过」——其 `pageDefaults()` **不解析 `<textarea>`**，属校验器盲区，已用同口径自建脚本补验变红）。13 例 all_default：`annual-leave-calc`（工龄 3 年/在职 6 月 → 2.5 天）、`assessor-training-hr`（90+92+66.667÷3 → 82.9/100）、`attendance-stats`（扣款合计 525 元）、`bandwidth-1`/`calc-81`/`eap-xinli-zixun-weiji-ziyuan`/`hris-zizhuyuaiduibijisuanqi`（通用双输入页兜底分支总和 480.00/325.00/280.00/175.00）、`comp-time-calculator`（休息日 6h×2÷8 → 1.5 天）、`gross-up-calculator`（税后 12000/社保率 0.20 → 二分迭代 15680.56）、`overtime-pay-calc`（30×(1.5×10+2×8+3×4) → 1290.00 元）、`performance-ranking`（评分分支总分 164.0）、`performance-score`（优秀比例 50% → 张三由「良好」升「优秀」）、`social-insurance`（基数 12000 → 合计 7,212 元），全部由 Python 高精度独立复算。**同时修 8 例无效用例**：① 四例统计页 `analysis-29`/`analysis-conversion-recruit`/`stats-funnel-recruit`/`stats-report-attendance` 的 expect `"80_X"` 实为 **textarea.value 回显**（并非任何计算结果，calc 完全失效也会通过）→ 改 `2,4,6,8,10` → 断言标准差 `2.83`；② `annual-leave-prorate` 的 `"2026-03-15_X"` 同为 date input 回显 → 改 `2026-02-01`/工龄 12 年 → 折算 `9.15 天`；③ `recruitment-funnel` 的 `"tech"` 为 select.value 回显 → 改 `preset=campus` → 整体转化率 `1.50%`；④ `generator-36` 的 `"6."` 依赖随机打乱后的条目编号 → 改 `cnt=12` → 断言 `"12. "`；⑤ `tracking-hours` 原 `via=delEmp`（兜底阶段 `delEmp()` 被无参调用删行后的**破坏态** 37%）→ 改 `required=50` → 平均完成率 `62%`。**新踩坑（防复发）**：① **`discriminate_check.js` 的 `pageDefaults()` 不解析 `<textarea>`**（只解析 `<input>`/`<select>`），textarea 类用例一律落「跳过」→ 判别力未被覆盖，须用支持 textarea 的自建脚本补验（注意与 `selfcheck_false_pass.js` 的 `_pageDefaults` 口径**不同**，后者**支持** textarea）；② **等级词类 expect 易被兜底副作用命中**：`performance-score` 原拟用「不合格」，但兜底会无参调用未被 `DESTRUCTIVE` 正则拦截的 `addEmp()` → 员工数 4→5 → `failCount=Math.round(5×10%)=1`，默认参数下同样出现「不合格」→ 逃生项；改用只依赖「优秀比例」的联合串 `88.1 88.1 优秀`；③ **「通用双输入计算器」模板页的 h1 分支**：`bandwidth-1`/`calc-81`/`eap-*`/`hris-*` 共用一套「按 h1 正则选计算模式」的模板，h1 未命中任一模式正则时落**兜底分支**，输出「总和/差值/比值/较大者」等通用双数指标——此类页可断言的只有兜底输出，须避开与默认态（150.00）的子串关系。

**第十二批成果（2026-09-18）**：metallurgy **13 例** all_default 弱用例清零 + **6 例**「expect 命中注入值回声 / 静态参考表」的无效用例改进（`verify_metallurgy_calc.js` **20/20** 通过；基线 all_default 323 → **310**，no_inputs 228 不变）；判别力 **15/15 变红、0 逃生项**（另 5 例 textarea 分析页被 `discriminate_check.js` 计入「跳过」——其 `pageDefaults()` **不解析 `<textarea>`**，属校验器盲区，已用同口径自建脚本补验变红）。13 例 all_default：`alloy-ratio`（8t/初始 1% → 总原料加入量 3.046 t）、`calc-1`（2000kg / 92+8 / 97% / 45% → 有效成分总占比 89.264%）、`calc-88`（目标 2.2/3.5/1.5、烧损 8/10/25 → C 偏差 +0.04%）、`calc-temp-1`/`estimate-temp-time-1`（通用双输入页落「温度」分支 → A 开尔文 473.15 / 523.15 K）、`energy-1`/`power-6`（落「功率/能耗」分支 → 6.0000 / 7.5000 kW）、`convert-hardness`（250×2.5 → 625.000000）、`decarburization`（1150°C/10h/ratio 0.8 → xMm≈0.865 落「脱碳较明显」档）、`heat-treatment`（80mm/900°C/系数 2.0 → 792 分钟）、`solidification-time`（板件 300×250×40、K=3.0 → 7.17 分钟）、`steel-calc-1`（角焊缝复合应力 82.46 → 应力比 41.2%，避「满足」⊂「不满足」）、`steel-profile-weight`（槽钢 100×50×8 / 12m → 106.03 kg），全部由 Python 高精度独立复算。**同时修 6 例无效用例**：① 五例统计页 `analysis-34`/`analysis-grade`/`analysis-heatmap`/`analysis-price-1`/`stats-10` 的 expect `"80_X"` 实为 **textarea.value 回显**（calc 全坏亦通过）→ 各换独立数据集分别断言标准差/方差（2.83 / 14.14 / 81.65 / 151.25 / 291.67，刻意错开避免五页 expect 撞车）；② `hardness-conversion` 的 `"hb"` 为 **select.value 回显** → 改 `inVal=100`（超轴值触发空插值分支）断言 `- 布氏 HBW`。**新踩坑（防复发）**：① **静态参考表只要有 id，整表就进 blob**：`hardness-conversion` 的 `#refTable` 由 JS 填入 DATA 全表（含「抗拉强度 σb(MPa)」列，首行 2820），故 `2820 MPa` 恒命中、不可作判别串——凡页面有「参考表/换算表」容器且带 id，其全表数值均须回避；② 同页 `interp()` 的 `xs` **递减**而实现假设递增 → 任意范围内输入**恒取首行**（68/760/940），结果与输入无关（见 §10.6 缺陷 E）；③ 通用双输入模板页的分支由 h1 正则**首个命中**决定：`calc-temp-1`/`estimate-temp-time-1` 标题同时含「温度」与「深度」，实测落**先声明的「温度」分支**——不可按标题语义臆测分支，须跑一次确认。

**第十三批成果（2026-09-18）**：clinical-lab **12 例** all_default 弱用例清零 + **3 例** `no_inputs` 转真输入 + **4 例**「expect 命中注入值回声 / 恒定文案 / JS 模板残骸」的无效用例改进（`verify_clinical-lab_calc.js` **25/25** 通过；基线 all_default 310 → **298**、no_inputs 228 → **225**，与 selfcheck 实测一致）；判别力 **18/18 变红、0 逃生项**（另 7 例被 `discriminate_check.js` 计入「跳过」——textarea 3 例 + 无 `value` 属性 input 3 例 + 动态 id select 1 例，均属校验器盲区，已用同口径自建脚本补验：注入态 PASS、换回默认态 FAIL）。12 例 all_default：`biochemistry-ratio`（alt60/ggt200 → De Ritis 0.50 偏低 + GGT/ALT 3.33>3）、`blood-gas-analysis`（pH7.25/PaCO2 28/HCO3 12 → AG 28 增高型代酸 + 矫正 HCO3 28 合并代碱）、`convert-39`（45/12、ISI1.0 → INR 3.750）、`convert-glucose-1`（7.5×2.5 → 18.750000）、`csf-analysis`（脓性/压力300/WBC2000 → 化脓 16.5/20.5 = 80%）、`electrophoresis-analysis`（白蛋白 50%/α2 13%/γ 23% → 慢性肝病图谱）、`flow-cytometry-ratio`（WBC2.0×20% → CD4 绝对值 60/μL → AIDS C3 + CD4/CD8 0.33 倒置）、`hba1c-converter`（9.4% → eAG 223 mg/dL = 12.4 mmol/L）、`pcr-ct-interpretation`（Ct32 → 阳性低拷贝；未知样本 30 → 10^((30−38.56)/−3.37)=346.8 → 3.468e+2）、`semen-analysis`（1.0×5×35% → TMSC 1.75 → 生育力受损）、`thyroid-function-model`（TSH0.02/FT3 12/FT4 35/TPO 120 → 原发甲亢 + TPOAb 阳性）、`cardiac-marker-curve`（上限 2.0 → 峰值 8.5 落 NSTEMI 分支），全部由 Python 高精度独立复算。**同时修 7 例无效用例**：① `analysis-8`/`analysis-9`/`analysis-density-2`（三页同构）expect `"80_X"` 实为 **textarea.value 回显**（calc 全坏亦通过）→ 改数据集 `3,7,11,19,23` → 断言均值 `12.60`/总体方差 `55.04`；② `coagulation-inr` expect `"范围"` 取自 `#targetInfo` 的**恒定文案**「目标INR范围」（真逃生项）→ 改锚 `pt=45` 派生的「INR 3.5-5.0：暂停华法林1-2次」与 PTA `38%`；③ `autoantibody-interpretation` expect `"40"` 为 `1:40` 回显 → 改 `1:320` + 均质型 + dsDNA 阳性 → 断言 `系统性红斑狼疮(SLE)`/`高滴度阳性(临床意义大)`；④ `stool-occult-blood` expect `"75"` 为 age 回显 → 改 `immunoResult=weak` + age75 → 断言「年龄≥45岁，弱阳性也有临床意义」；⑤ `urinalysis-interpretation` inputs 是 **JS 模板残骸**（`"ua_'+it.key+'"`，全页 select 由 `buildForm()` 动态生成）→ 改注入真实动态键 `ua_leu=500`/`ua_nit=pos` → 断言 `提示泌尿系感染`（`via=interpret` 兜底，注入值经 `buildForm()` 后仍存活）；⑥ `blood-routine-reference` 由 `no_inputs` 转真输入（`metricSel=0`/`testVal=17.25` → 断言 `↑ 偏高` 与 `17.3`=17.25.toFixed(1)，刻意避开 17.25 的回显）；⑦ `vaginal-discharge-grading` 与 `mic-breakpoint`、`tumor-marker-doubling` 核验为真实有效用例，保持不动。**新踩坑（防复发）**：① **「检索过滤」型图鉴页（`parasite-egg-id`/`urine-sediment-atlas`）不存在单卡片判别串**——过滤结果是全量结果的**子集**，任何卡片内文本（名称/大小/形态/参考值/临床意义）在默认全量态同样存在，用它作 expect 必为逃生项；唯一可行解是断言**仅在过滤态成立的「跨卡片相邻串」**（如 search=吸虫 时「卵盖小不明显。 肝片形吸虫卵」、「肾移植排斥反应 草酸钙结晶」，两卡在全量列表中并不相邻），标签剥离后以**单空格**连接、须逐字含该空格；② **无 `value` 属性的 `<input>` 是判别力校验的盲区**：`pageDefaults()`（discriminate）与 `_pageDefaults`（selfcheck）口径不同——前者对无 value 的 input 返回 `undefined` → 该键**不回退默认**、整个用例被跳过（`coagulation-inr` 的 `inrIn`、`tumor-marker-doubling` 的 `days`、两个图鉴页的 `search` 皆属此列）→ 真逃生项可能被漏判，必须补验；本批 `coagulation-inr` 的 `范围` 正是这样漏网的，且第一次改写（断 `由INR反算：对应PT = 30.0 秒`）因 `inrIn` 不回退仍被判逃生项，最终改锚 `pt` 派生量才收口；③ **动态 id 的 input/select 可注入**（`ua_leu` 等由 JS 生成、静态 HTML 无此 id）——`getEl` 按 `c.inputs` 的键即席建元素，但**不会注册内联事件**（HTML 里没有该标签）→ 只能靠兜底函数（`via=interpret`）驱动，属可接受路径。

**第十四批成果（2026-09-18）**：psychiatry **4 例** `no_inputs` 转真输入 + **2 例**「inputs 为 JS 模板残骸」的无效用例修正（`verify_psychiatry_calc.js` **24/24** 通过；基线 no_inputs 225 → **221**，all_default 298 不变，与 selfcheck 实测一致）；判别力 **24/24 全部计入「跳过」**——22 例 `no_inputs` 本就不适用，另 6 例虽已注入真值，但键是 **JS 模板生成的动态 id**（`f0`/`a0`/`q0`/`sc0`/`ide0`…），静态 HTML 里只有 `id="f'+i+'"` 这类模板字面量 → `discriminate_check.pageDefaults()` 与 `selfcheck._pageDefaults()` 均取不到默认值（判 `null`），**判别力根本没被检查**，故已由自建同口径探针逐例补验：**注入态 PASS + 回退默认态 FAIL（6/6）**，并用**浏览器真实默认值**（rater-23/24 的 `<option value="2" selected>`）做反向验证，同样变红 —— 确认非 `all_default` 伪装。**4 例转真输入**（均为 `calc()` 直接读 DOM 的动态 id `select`）：① `calc-1`（PHQ-9 九项 3,3,2,2,1,2,2,1,2 → 总分 18 落「中重度抑郁」+ `q8=2>0` 触发第 9 项自伤念头警示）；② `rater-23`（LSAS 24 项 · 表演型 13 + 社交互动型 11，`f_i`/`a_i` 全取 3 → 恐惧 72 + 回避 72 = **144/144**，落 total≥105 分支「重度社交焦虑」+ 表演型 **78/78**）；③ `rater-24`（CD-RISC 25 项全 4 → **100/100** 落「高心理韧性」+ 条目均分 **4.00/4.0**）；④ `assessor-risk-5`（C-SSRS `ide2=1` 其余否 → `maxIdeation=2` → 风险「**中风险**」+ 表格「**3级（0=无）**」+ 该分支处置文案）。**2 例残骸修正**：`mmpi2-personality`（原键 `sc'+i+'` → 改真键 `sc0=75`/`sc1=68` → 升高量表数 2 → 触发「多个临床量表达到临床显著升高(T≥65)」+ `75 临床显著`）、`self-assess-4`（原键 `q'+i+'` → 改真键 `q0..q5=4,3,2,2,3,3` → 阳性项 6/6 → 「高度疑似成人ADHD」+「混合型表现」）。**18 例保留 `no_inputs`**（见 §10.6 缺陷 G）。**新踩坑（防复发）**：① **动态 id 用例会同时骗过两道静态校验**——`discriminate_check` 因「键不在 `pageDefaults`」判 `usable=false` 落「跳过」（不计入 `checked`），`selfcheck` 因 `defs[k]===null` 直接 `return null`（不计入 `no_inputs`/`all_default`）→ **基线数字会「虚降」而判别力其实没被验证**；凡注入键含动态 id 者，必须自建同口径探针（缺失默认按 `""`）跑「注入 PASS + 回退默认 FAIL」，并另用**浏览器真实默认值**再跑一遍反向验证（本批 `selected=2` 与 `""` 两种默认态都变红）。② 这类页的顶层 `render();calc();` 在 `new Function` **编译期即执行**，而 `getEl` 会按 `c.inputs` **即席建元素** → 注入值在顶层 `calc()` 里就已生效，`blob1` 直接命中，`via` 报 `input event`（**不是**真实事件驱动，是「顶层即读数」）——不要因此误判为「有内联事件绑定」。

**第十五批成果（2026-09-18）**：tcm-pharmacy **8 例** all_default 弱用例清零 + **8 例** `no_inputs` 转真输入 + **5 例**「expect 为注入值回显 / JS 模板残骸」的无效用例改进 + **1 例**结构性 `no_inputs` 保留（`verify_tcm-pharmacy_calc.js` 全量重写 **22/22** 通过；基线 all_default 298 → **290**、no_inputs 221 → **213**，与 selfcheck 实测一致）；判别力自建同口径探针实测 **注入 PASS 22/22 + 回退默认 FAIL 21/22**（余 1 例 `five-flavors` 为结构性 `no_inputs`）。**8 例 all_default**：`calc-time-concentration`（herb150/vol800/abv60/target0.15 → `目标生药浓度 0.150 g/mL：当前已达标。` + `1:5 药酒比` + `33.8`）、`decoction-time`（石膏/附子/薄荷/三七粉 6 味/均 12g/三煎 → `总量约 519ml` + `步骤4 - 三煎` + `分3次温服`）、`medicinal-wine`（红花酒 100g/800ml/45% → `药酒比例(1:8.0)` + `12.50%`）、`tcm-dosage`（成人 9g/6 岁/20kg/有毒 → `推荐儿童剂量：1.64g` + `2.97g ~ 4.16g`）、`tcm-pharmacoeconomics`（补中益气丸 36 元/200 丸/8 丸×3/14 天 → `日治疗费用仅 4.32 元，疗程费用 60.48 元。` + `0.180`）、`formula-song`（银翘散/十味/辛凉透表 → `银翘方中用银花` + `辛凉透表功独擅`）、`granule-equivalent`（石膏 45g → `45g ÷ 10 = 4.50g` + `4.50g`）、`incompatibility-check`（硫黄/朴硝/甘草/海藻 → `发现 2 项配伍禁忌` + `甘草 与 海藻 不可同用` + `共 4 味药`）。**8 例 `no_inputs` 转真输入**（其中 5 例为过滤型图鉴检索页，见下坑①）：`herb-properties`（化痰）、`four-qi-nature`（葶苈子 → `大寒性` + `清热泻火力强。适用于实热重证。不宜久服。`）、`herb-processing`（炭）、`herb-storage`（参）、`patent-medicine`（失眠）、`pregnancy-contraindication`（攻毒杀虫药）、`jun-chen-zuo-shi`（四物汤 → `君:2.0 臣:1.5 佐:1.5 使:1.0` + `君药剂量占比 33.3%，符合`）、`tcm-adr-assessment`（雷公藤多苷片 + 肝功能异常 + `checks=["2"]` → `该不良反应与药物存在明确的因果关系，建议立即停药并上报` + `可疑药品：雷公藤多苷片`）。**5 例无效用例改进**：`analysis-ratio-prescription`（`"80_X"` 为 **textarea value 回显** → 改数据集 `5,8,12,17,21,30` → `方差： 70.25`/`标准差： 8.38`）、`herb-quality`（inputs 键为脚本模板字面量 `score_'+i+'` 残骸、expect 为该幻影元素 value 回显 → 改真键 `score_0…score_7` → `84.5 分`）、`medicated-diet`（`"qi"` 为 select value 回显 → `药食比例(1:0.4)` + `气虚质：补气药量增加30%`）、`medication-timing`（`"supplement"` 回显 → `饭后服（调整建议）`）、`medicinal-guide`（`"child"` 回显 → `儿童用药引减半` + `8.5g`）。全部数值期望由 Python `Decimal`（prec=60、ROUND_HALF_UP，模拟 JS `toFixed`）高精度独立复算。**新踩坑（防复发）**：① **检索/过滤型图鉴页的结果是全量列表的「子集」**——任何「单卡片内文本」在默认全量态同样存在，作 expect 必为逃生项（本批 3 处实测命中：`decoction-time` 的「步骤1 - 先煎（石膏、附子）」被兜底 `loadExample` 的石膏/附子命中、`pregnancy-contraindication` 的「🤰 硫黄 忌用」在全量列表本就存在、另 5 检索页原 expect 均为 `countText` 默认全量数）；唯一解 = 断言「**仅过滤态成立的跨卡片相邻串**」（如 `消痞散结 🌿 冬虫夏草`、`止血止泻 🔬 地黄 · 生地炭`、`大毒，蚀疮去腐 🤰 硫黄`），因过滤后卡片相邻关系改变；② **动态 id（`score_0…score_7`）、`<textarea>`、无 `value` 属性 `<input>` 三类用例同时骗过 `selfcheck`（`defs[k]===null` → 直接 `return null`，不计入弱用例）与 `discriminate_check`（`pageDefaults()` 取不到 → 落「跳过」，不计入 `checked`）** → **基线数字「虚降」而判别力根本没被验证**，必须自建同口径探针补验（本批 `herb-quality` 的 8 个动态 id 即属此类）；③ **量表类 `:checked` 桩须补 `parentElement`**：`tcm-adr-assessment` 的 `assess()` 读选中项后会读 `checked.parentElement.textContent` 取选项标签，`verify_it_calc.js` 的两处 `:checked` 桩（`querySelector` 单元素 + `querySelectorAll` 数组）已各补 `parentElement: { textContent: "" }`，否则抛 "Cannot read properties of undefined"；④ `assess()` 末尾调 `#resultCard.scrollIntoView()`（未桩化会抛错），但 `#result.innerHTML` 已在抛错前写入 → 结果确由 `checks` 计算，断言在下一候选 `copyReport` 处命中，不受影响；⑤ `five-flavors` 为**结构性 `no_inputs`**（纯 `tab`+`onclick` 切换、整页无注入控件，同 §10.6 缺陷 G）→ 保留。

**第十六批成果（2026-09-18）**：ecommerce **13 例** all_default 弱用例清零（13 例 v0/v1 双变量计算器换 217/83 → 217.00/134.00）+ **8 例**「expect 为注入值回显 / 静态 data 含 `_X`」的无效用例升级真实统计 + **1 例**阈值回显（`verify_ecommerce_calc.js` 全量重写 **23/23** 通过；基线 all_default 290 → **276**、no_inputs 213 不变，与 selfcheck 实测一致）；判别力单文件 `discriminate_check.js verify_ecommerce_calc.js` **已检 15 / 正确变红 15 / 仍 PASS 0 / 跳过 8**（8 个 textarea 分析页被 `pageDefaults()` 不解析 textarea 计入「跳过」——属校验器盲区，已由自建同口径探针 `probe_analysis.js` 补验 **注入 PASS 8/8 + 回退默认 FAIL 8/8**，判别力真实有效）。**13 例 all_default**（页面公式 `a=v0,b=v1`；`a.toFixed(2)=217.00`、差值 `a-b=134.00`，默认 100/50 输出 100.00/50.00/50.00 不重叠）：`calc-79`/`calc-commission-2`/`conversion-4`/`discount`/`erp-dingdan-caigou-duijie`/`estimate-ranking`/`inventory-1`/`kaidian-yunyingyuguizeduibijisuanqi`/`kedan-jiandanjia-liandailv`/`pingjia-chaping-tuihuo-lv`/`response-2`/`wuliu-fahuo-cangchu-gongyinglian-zhenghe`/`wuliu-lanshou-qianshou-shixiao`。**8 例 textarea 统计分析页升级**（inputs `data:"7,14,21,28,35,42,49,56"` → 断言 `31.50`/`252.00`/`257.25`，对应 n/sum/mean/var；默认空 data 输出「请输入数据」→ 不命中）：`analysis-25`/`analysis-70`/`analysis-71`/`analysis-conversion-funnel`/`analysis-cost-8`/`report`/`stats-flow-conversion`/`stats-profit`。**1 例 groupon-filler**（`inputs:{target:"520",cut:"70",cur:"400",cands:"22,44,66,88,110"}` → `差 120.00 元`/`462.00`/`86.84%`；need=max(0,520-400)=120.00、双指针最优凑单 {22,110} 合计 132、finalPay=max(0,400+132-70)=462.00、effective=462/532×100=86.84%）。**1 例 cycle-15 保留**（churnDays=135，非默认 90；页面客户数据来自 `localStorage` harness 恒 null → 空 → 仅显「暂无客户记录」，135 仅作输入值回显，重置默认 90 后消失 → 可判别、非 all_default/非 no_inputs，selfcheck 不计入弱用例）。**新踩坑（防复发）**：① **两类校验对 textarea / 无 value input / 动态 id 用例的双盲**：`discriminate_check.pageDefaults()` 与 `selfcheck._pageDefaults()` 口径不同（前者截断 DEEP-DIVE 只解析 `<input>`/`<select>` 且不含 textarea、无 value 属性的 input 返回 undefined → 整例跳过；后者读全文含 `<script>` 模板、支持 textarea），但**共同盲区**是 textarea 与无 value input 在判别器里必落「跳过」——凡此类用例必须自建同口径探针（支持 textarea、缺失值按 undefined→整例 FAIL 反向）补验「注入 PASS + 回退默认 FAIL」；② 全站 `discriminate_baseline.json` 的 `skipped` 由 722 → **699**（14 个 all_default 改非默认后从「跳过」转「已检且正确变红」），`checked` 2326 → **2340**，escape 仍 **0**；`falsepass_baseline.json` 的 `all_default` 290 → **276**、no_inputs 213、`total_cases` 3030 不变。

每例流程固定四步：**读页面公式 → 选一组与默认不同的输入 → Python 独立复算 → `runCase` 验证 `via=input event`**。

| 环节 | 口径 |
|---|---|
| 选输入 | 至少一项数值 ≠ 页面默认；**避免与默认成比例**（opamp 1k/10k 与 1.5k/33k 的比值巧合会让判别失效） |
| 复算 | 一律用 Python 高精度算（`math`），不手算尾位；`toFixed` 边界（1867.89 → "1867.9"）以 Python `format(x,'.1f')` 为准 |
| 验证 | `runCase` 必须 `ok=true` **且 `via=input event`**；`via` 为空说明该串只在兜底阶段出现，等于没验证 |
| 收尾 | `discriminate_check.js <脚本>` 必须 0 逃生项 |

**新增坑（三条，均已实测）**：

1. **`fullBlob` 不可信，判定只看 `blob1`。**
   框架在兜底阶段会**无参调用所有导出函数**，`setGender()` / `calc()` 之类会把模块级变量污染成 `undefined`：
   - `health/calorie-needs`：默认 `gender='male'`，被无参 `setGender()` 改成 `undefined` → 走 female 分支，输出 1810（真实应为 2009），还连带刷出 `undefined BMR` / `NaN kcal`。
   - `health/child-height-predictor`：男童 179.0 被算成女童 166.0，同一机理。
   - 推论：**用 `expect:["@@NOMATCH@@"]` 取输出来"看结果"是错的**，那是 fullBlob。正确做法是拿复算值去 `runCase` 探测，看 `via` 是否为 `input event`。

2. **expect 会撞上页面可见的静态参考表（§10.8 源码字面量的"表亲"）。**
   - `electrical/wire-gauge-selector`：断言 `"10 mm²"` 恒命中 —— 页面「常见家用电器电流参考表」里有 `6–10 mm²`。
   - `electrical/transformer-sizing`：断言 `"500 kVA"` 恒命中 —— 页面把所有 ≥0.85·S_t 的标准容量都列为候选标签，500 总在列表里。
   - 解法同 §10.8：**断言要带上下文**，`"10 mm² 推荐截面"` / `"推荐容量：500 kVA"`。

3. **select 的"默认值"是第一个 `<option>`，顺序未必符合直觉。**
   `electrical/calc-1` 的敷设方式第一个 option 是 `conduit`（系数 0.8）而不是 `free`（1.0），芯数第一个是 `2` 而不是 `3`。复算载流量前必须 `grep` option 顺序，否则 Iz 差 20%。

**本批修出的真缺陷**：`tools/electrical/voltage-drop.html` 电压降公式多除 1000 ——
`ΔU = √3·I·r·cosφ·L/1000`，而 `r = ρ/S` 已是 Ω/m（`ρ=0.0184 Ω·mm²/m`），再除 1000 使压降小 1000 倍（25 kW/120 m/16 mm² 得 0.0157 V，物理值应为 15.73 V）。
连带**反算截面** `S_min` 同样多除 1000（默认参数反算出 0.005 mm²，正确应为 5.3 mm²）。
已修 6 处（含分步计算与推导文案），并做反向验证：改回 `/1000` 后用例立刻变红。
