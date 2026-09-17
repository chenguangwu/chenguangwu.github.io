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

- [x] **D 项 假门禁恢复（851 用例 / 128 分类）—— 2026-09-15 已完成**：含 683 道 `_selfcheck` 假门禁（不验证计算）+ 168 道裸空输入用例（未标 `_selfcheck` 但同样不验证）。须逐分类还原为 `inputs`+`expect` 真 runCase 用例；分布极广（medical/industrial/life/legal 等 128 个分类均有，最大 neurology 23 / psychiatry 24 / tcm-pharmacy 19 / tcm-diagnosis 21 / dermatology 21 / ophthalmology 16 / pulmonology 16 / rheumatology 16）。完整清单见 `/tmp/fake_gates.json`。→ §9.3 P0-1（**已完成**：全 206 道 verify 实跑 FAIL 0，`selfcheck_false_pass.js` risk=0）。
- [x] **E 项 指南补齐（99 分类）—— 2026-09-15 已完成**：（原记「103 分类」有误，磁盘实测 99，`ceramic` 目录不存在）robotics / signal / thermodynamics / structural / banking / neurology / hematology / construction / pulmonology / astronomy / clinical-nursing / dentistry / cardiology / livestock / accessibility / acupuncture / admin / advertising / antiques / aquaculture / archaeology / audio / audit / bridge / ceramic / chemical / chess / chinese / chinese-cook / cleaning / clinical-lab / dance / decor / dyeing / ecommerce / edu2 / elderly / electronics / endocrinology / engineering / exhibition / fire / gardening2 / home / hotel / hr / hvac / jewelry / kids / leather / legal2 / library / logistics2 / manufacturing / maritime / martial / media / medical / medical2 / museum / music / niche / office / paper / parenting / pet / pet-training / petrochem / pets / photo2 / plastic / pr / printing / process / procurement / project / property / quality / railway / rental / research / restaurant / road / rubber / safety / sales / seismology / service / shipping / stage / stats / telecom / textile / tunnel / urban / usedcar / wedding / woodworking / yi（完整列表见审计脚本 `audit_all_closed.py` 输出）。
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
- [x] **B 项 enmap 英文态（16 分类缺 enmap JSON）—— 2026-09-16 已完成**：agriculture / ai / banking / biz / design / finance / fun / general / hydraulic / it / legal / life / realestate / science / sports / statistics。**关键发现：这 16 分类英文并非从零缺失，而是"有英文、无 enmap 数据源"**——`industry-<cat>.json` 的 `en`/`ed` 本已 100% 覆盖，仅 `i18n en-US` 缺 51 条、85 页缺 body 键。故 enmap 采用**无损反推**生成（不编造英文）：`name`/`intro` 依次取自 `i18n/tools/<cat>-body.json` 的 en 字段 → `_en_override` 的 en/ed → `industry-<cat>.json`，并用已收口分类 eco 做闭环校验（body→enmap 38/38 完全等价）；label 取自 `i18n/industry-en.json`。成果：16 份 enmap 新增，1496 页全覆盖（中文名 0 / 中文简介 0 / 空简介 0），i18n en-US 1360→**1496（100%）**，补齐 85 条 body 键，h2 对齐规范英文名 196 处（修复线上 `title-en` 与 h2 不一致，如 `agriculture/calc-36` 的 `(ET / Evapotranspiration)` vs `(ET)`），占位 `<p>` 替换 12 处。**零破坏性**：cat 修正 0（enmap 不含 cat 字段，不改页面 meta cat）、孤儿键清理 0。**遗留**：140 个真孤儿键（general 110 / it 18 / finance 5 / science 4 / design 3）仅报告未删，需老板确认后再清理。全 214 道门禁通过，提交 `bd9a1b1da`。

### 9.3 孤立未完成任务（按优先级）

> 跨分类 / 独立的系统性问题，可穿插推进但不替代后续验证质量深挖。

**P0 — 必须修复（本轮新发现，09-15 批次造成）**

- [x] **P0-1 恢复 851 道假门禁（683 `_selfcheck` + 168 裸空输入）为真实 runCase 用例**：**2026-09-15 完成全量还原**。`/tmp/fake_gates.json` 全清单 + 09-15 批次残留的占位/空输入用例已逐分类还原为 `inputs`+`expect` 真 runCase；全 206 道 `verify_*` 门禁脚本实跑 **FAIL 0**、`verify_calc`/`verify_it_calc` 两道 meta 全过。`selfcheck_false_pass.js` 静态判定 **risk=0**（无 `_selfcheck` 标记、无占位 expect）。其中 **115 个不可派生/随机/二进制/答题页**（45 分类，如 `psychology/*`×14、`forestry/*`×6、`data/random-*`、各 `generator-*` 随机生成器、`image/gif-split` GIF-LZW 解码等）无法构造稳定 expect，已从门禁**排除**（非降级保留）并登记于 `scripts/_unverifiable.json`（按约定 `_` 前缀不入 git），后续需逐页补真实 expect。
- [x] **P0-2 把 `selfcheck_false_pass.js` 接入 `run_gates.py` 作为第 6 道门禁**：已于 09-15 批次（提交 f2da3d2fe）接入 `run_gates.py` 第 6 道（`node scripts/selfcheck_false_pass.js scripts`）；RISK>0 即 FAIL，已堵死假门禁与默认态假通过。
- [ ] **P0-3 回退 §9 原"208 全收口"虚假声明**：09-15 批次将本 §9 改写为"208 全部完成基础收口 / 208/208 已收口 / §9.2 清空"，与实测（103 分类 0 指南、117 深解 0 达标、16 缺 enmap、683 假门禁）严重不符，已于本轮（2026-09-15）重新核定（见本 §9 头部与各小节）。
- [x] **原「非 CJK 占位页英文未注入」—— 2026-09-17 全站复核：作为全站级缺陷已不成立，真实残留仅 10 页且已修**。用**浏览器渲染实测**逐层证伪（不靠静态推演）：① **`<h1>`**：323 页为英文，其中 311 页是公式/符号（有意 UI 设计），另 12 页是 `<h1 class="sr-only">`（屏幕阅读器专用、**视觉不可见**，且同页已有 `data-i18n-fb` 中文通道），均非缺陷；② **`<h2>`**：187 页纯英文无 `data-zh`，绝大多数为公式型，抽验 13 页里 12 页正常（走 `data-i18n` 通道还原中文），唯一 `meteorology/humidex` 的中文数据源 `zh-CN.title` 本身就是 `Humidex`（专有名词），亦有据；③ **intro `<p>`**：这才是真病灶 —— **10 页**（`energy` 5 / `health` 4 / `optical` 1）的 intro 是英文自然语言句，却既无 `data-zh` 也无 `data-i18n`，中文态被钉死英文。修法见 `scripts/fix_intro_i18n.py`（幂等）：补 `data-i18n="<ind>.<slug>.intro"` + `data-i18n-fb="<中文简介>"`，与已正常的手工页（`design/color-picker`）**写法对齐**；其中 `health/milk-tea-calories`、`pregnancy-weight-gain`、`safe-period-calculator` 三页因 `health.json` 缺 `zh-CN.intro`（数据源缺口）一并无中文可补，按英文 intro 译写补齐。** `_build.py` 未改** —— 判据显示缺陷不具全站性，不应为此承担 5000 页回归风险。
    - **踩坑（防复发）**：这套渲染验证**不能用 `file://` 测英文态** —— 行业字典/`-body.json` 靠 `fetch` 加载，`file://` 下被 CORS 拦截，`I18n.apply` 找不到 en-US 词典就回落到 `data-i18n-fb`，导致「英文态也显示中文」的**假回归**。原生页（`energy/battery-capacity-wh`）同样如此，是环境限制而非代码问题。**正确做法**：起 `python3 -m http.server`（同源）后再渲染对比中英双语。
    - **踩坑（防复发）**：渲染 DOM 里 intro 段落**不能靠样式正则定位**（header/footer 运行时注入后节点顺序变化，会抓到别的 `<p>`）。应按 `data-i18n="<ind>.<slug>.intro"` **属性精确定位**目标节点。
- [ ] **`upload-pages-artifact@v4` 移除 `include-hidden-files`**：本轮已降级 v4→v3 临时修复（Run 931）。长期方案：等 v4 加回该参数后升级，或改 workflow 不用该参数。

**P1 — 建议修复**

- [x] **「工具 ↔ 使用指南」配对链路修复（2026-09-17 已处理，脚本 `scripts/fix_guides_pairing.py`）**：`_build.py`（行 ~3040）只按 `json/guides.json` 注入工具页「📖 查看使用指南」入口，靠 `GUIDE_MAP[tool basename]` + `GUIDE_MAP_IND['<industry>/<basename>']` 两本字典；只要**缺条目或 `tool` 字段写错，这篇指南就永不出现在工具页上**。全站体检 3434 篇指南，修三类：
  - **① 缺登记 376 条**（指南页在磁盘、`guides.json` 无条目）→ 补登记后 376 个工具页长出 📖 入口。配对判据（唯一才认，歧义跳过）：同名 basename → 行业前缀消歧 `<ind>-<base>` → 指南页 `.back` 主链接 → 正文唯一工具引用。
  - **② `tool` 字段错位 6 条**（basename 全站不存在，工具改名遗留）：`base64.html→base64-converter.html`、`calorie-calculator→food-calorie-counter`、`gradient-generator→gradient`、`color-blindness-sim→colorblind-simulator`、`budget-planner→funeral-budget-planner`、`roi-calculator→investment-roi`；另把真孤儿 `tnss-guide` 正确挂到 `ent/calc-1.html`（TNSS 鼻炎评分）。这 7 篇首次在工具页可见。
  - **③ 孤儿指南下架 11 篇 + 清 stale 登记 16 条**：工具页已不存在的指南页（`dice-roller` / `spinner-wheel` / `blackjack-simulator` / `roulette-simulator` / `poker-hand-evaluator` / `dice-statistics` / `slot-machine` / `chinese-address-generator` / `gunshot-wound` / `blast-injury` —— **均为合规整改下架工具的残留，主 CTA「→ 打开工具」指向 404，且内容命中老板红线（赌博博彩 / 枪爆法医 / 个人信息伪造）**；`regex-tester-guide` 为 `regex-guide` 的重复旧页（工具改名 `it/regex-tester.html→it/regex.html`）。一并清掉 5 条指南文件早已消失的旧登记（`bip39-generator` / `id-card-generator` / `lottery-odds-calculator` / `lottery-quick-pick` / `calc-21`，同属敏感类）。删除前已逐一确认无外部页面互链（仅 `guides/index.html` + 构建产物引用）。
  - **验证三轮**：① 脚本幂等复跑 → 3423 篇指南 **100% 可唯一定位**、缺登记 0 / 错位 0 / stale 0；② 构建后全站工具页带 📖 入口 **3419 个，异常 0**（逐页校验「注入的指南文件存在」且「该指南正文回引本工具页」，无跨行业串味）；③ 全 214 道门禁（含构建）+ 死链/资产门禁 + 反伪自检 risk=0。
  - **踩坑（防复发）**：① 判断「指南指向哪个工具」**不能取正文首个 tools 链接** —— 指南页含「相关工具」chip 区（2758 篇有多个工具链接），首链接多数是相关推荐。权威来源是 `<div class="back">` 里的「→ 打开xxx工具」；老批次该 div 指向 `guides/index.html`，此时退回到全正文中**唯一存活**的工具引用，仍歧义则用人工核实表 `MANUAL_TOOL_FIX`。② `json/guides.json` 落盘格式是 **`json.dumps(indent=1)` 且无尾换行**（与 `content_deepdive.json` 的「+ 尾换行」不同），写前必须校验否则整文件 diff 爆炸。③ stale 判定必须在删除文件**之后**再算一遍（首版本先算后删，导致 11 条刚删页的登记残留成孤儿）。
- [ ] **SEO Description 重复（2026-09-16 复核）**：工具页 meta description 已**零重复**（5026 页全唯一，原"69 组"已消解）。全站扫描另见 **4690 个重复组 / 9380 页**集中在非工具页（guides / industry / index / sitemap），其中大量为同类页共享模板描述（如某行业 6 篇指南同描述），属预期近似重复，**非工具页"69 组"范畴**。是否对这部分做唯一化（按页标题/核心词区分）需老板定夺，避免无价值 churn —— 暂未动。
- [x] **门禁 id 错配伪门禁根治（全站审计，2026-09-16 已修复）**：原记「49 个降级分类 inputs id 按结构推断不匹配」经**全量审计（208 脚本 / 3059 用例）推翻**——49 分类 784 用例 inputs id **全部真实存在于页面**（早已正确还原，ref 标注 auto-restore）。真正 id 错配伪门禁集中在 **signal 17/24 + science 1/8 + sports 1/8 = 19 用例**：用例 key 与页面真实 id 大小写/缩写不一致（如 `q`→页面`Q`、`fupper/flower`→`fu/fl`、`a`→`vout/vin`、`amp`→`Vpk`），导致输入未注入、calc 跑默认值、expect 因恒定子串命中而**假通过**。已逐页读 calc 对齐真实 id 并重算 expect；其中 **4 处 expect 数值/符号本身也错**（bandwidth-q 应 40.000 而非 200.000、group-delay 符号应 +0.001571、damping-ratio 取非默认 0.2、pwm-average 按 D 百分比 2.5）。三道门禁现 24/24、8/8、8/8 真通过；全 213 道门禁 + 反伪自检 risk=0。
- [x] **deep-dive 缺 `title` 导致「📚 深度解析：」空标题（全站扫描，2026-09-17 已修复）**：原记「edu 段 44 条 `summary`/`example` 旧键」经**全站 5124 键复核修正**——`summary` 键虽仍有 **819 条**（纯冗余、`_build.py` 不渲染，非缺陷），**真正影响渲染的是缺 `title`**：`_build_deep_dive_html()` 只认 `title`/`scenarios`/`examples[].body`/`faqs[].a`，缺 `title` 就渲染成 `<h2>📚 深度解析：</h2>`。定量：**119 条缺 title → 其中 95 条对应在线页**（dentistry 26 / construction 25 / data 17 / health 15 / decor 8 / design 4；余 24 条为孤儿键，无页面不渲染）。另发现 **1 条 example 键名写错**：`materials/brinell-hardness` 的示例写成 `{title, a}`，`body` 缺失 → 示例正文空白。
  - **修法**（`scripts/fix_deepdive_title.py`，幂等，dry-run 默认）：按权威源回填中文标题 —— ① `i18n/tools/<industry>.json` → `<slug>` → `zh-CN.title` → `zh-CN.h1`（**98 条**，与 MEMORY「i18n 是页面 title 权威源」同口径）；② 页面首个含 CJK 的 `<h2>` 文本（**7 条**，去前置图标）——仅用于 i18n 缺该 slug 的页。同时把 `{title, a}` 归一为 `{title, body}`。**约束**：落盘前先校验 `json.dumps(indent=1)+'\n'` 与磁盘原文恒等（不满足直接 FATAL 退出，不冒全量重写 JSON 的风险）；`title` 插为首个键，diff 极简（+106/-1，其余 4825 页零改动）。
  - **验证三轮（硬要求）**：① 数据源 4825 条全部非空 title；② 构建产物 HTML 逐页比对渲染标题 **4825/4825 == 数据源、0 不一致**，全站 `深度解析：</h2>` 残留 **0**；③ 全 214 道门禁（含构建）+ 反伪自检 risk=0。改动面 96 页（95 标题 + 1 示例）。
  - **遗留**：14 条孤儿键无中文名来源（`content/*`×4 / `consulting/*`×3 / `dentistry/*`×4 / `construction/*`×2 / `health/tdee-calculator`），页面已不存在、不渲染，未编造；819 条 `summary` 冗余键属历史数据卫生问题，**按"禁止擅自批量删除"原则仅报告未删**。
- [x] **`classify_quality()` A 级率 100% 失真 —— 2026-09-16 已修复（收紧 rich 判据）**：原实现 `rich = 'formula-box' in content or '<canvas' in content or 'data-viz' in content`，且 A 级条件为 `rich or ...`，即**只要 HTML 里出现 formula-box 类名就判 A**，导致全站 A 级率报 100%（README 实测是 100.0%）。
  - **量化证据**（只读审计 5033 页）：A=4825（95.9%），其中**伪 A=2822（58.5%）**，2817 例仅靠 formula-box 撑起；其中 **759 页的 formula-box 是空壳**——`0 字 46 页 + 5~9 字 713 页`（剥标签/图标后只剩标题「工作原理与说明」7 字），**978 页 own_len<800（大量 own_len=0，自研逻辑为零）**。铁证：`tools/accounting/analysis-46.html`（formula-box 无正文、own_len=0、inputs=1）旧判 A。
  - **修法**：① 新增 `formula_box_text_len()`——按 div 嵌套配平取出 formula-box 块真实正文（剥标签/图标/空白），要求 `>= FORMULA_BOX_MIN_TEXT(20)` 才算真实公式说明（20 落在 10~19 仅 124 页的分布谷底，分界有据）；② canvas/data-viz 保留为真实可视化信号；③ A 级条件 `(rich and own_len>=800) or own_len>=6000 or (own_len>=3000 and inputs>=3)`——rich 须搭配自研代码量，单薄占位页不再混进 A。
  - **结果**：README 对外数字 **A 100.0% → A 66.6% / B 20.6% / C 12.8%**（全站 5033 页口径：A 63.9%/B 19.7%/C 16.4%）。`tools.json` 条目数 4825 不变、`industry-*.json` 总和 4837 守恒、归属变动 0/消失 0/新增 0——diff 里的"删除"是 `_build.py:241` 排序 key 含 `QUALITY_RANK` 导致的**同分重排**，非数据丢失。副作用良性：索引页按 (hot,质量,名) 取名额，B/C 工具不再抢占前列（`js/industry-info.js` hot 微降即此因）。全 214 道门禁（含构建）通过。
- [x] **`realestate` 三页 `calc-93`/`pv`/`depreciation-2` 非错放（2026-09-17 澄清，移出分类治理）**：原记"268 行业复用模板"经核实不成立——grep 全站无跨行业引用，三页（`calc-93` 比较法估价 / `pv` 收益现值 / `depreciation-2` 房屋折旧）实为 realestate 专属工具。可选补 verify 覆盖门禁缺口，不属分类错放治理。
- [x] **`energy` 分类重复工具下架 —— 2026-09-17 已完成（低影响，老板免 301）**：逐页比对 calc 公式+输入输出确认真重复，按"保留最全权威页、下架冗余"处置（**影响范围小、不纠结 SEO、未做 301**）：① 热泵×3 保留 `heat-pump-cop`（最全含 EER+电费），下架 `cop-heatpump`+`calculator-calc-5`；② 光伏保留 `solar-panel-power`（有指南），下架 `solar-output-physics`（近重复 P=A·G·η），`solar-calculator` 不同层级保留；③ 比能量保留 `energy-density`，下架 `specific-energy`（E/m 同义）。**每个被下架工具均有配套指南**，连同指南一并下架，并清理全数据源（guides.json/energy.json/_en_override/slug-en/_en_desc/content_deepdive/energy-body/enmap/energy/locale-zh-TW）+ 移除其它指南里 15 处 chip 硬链接（防断链）+ 移除 verify_energy_calc.js 4 用例。214 门禁含链接审计全过；线上核验删除页 404、权威页 200、tools.json 残留 0、Actions success。脚本 `scripts/retire_energy_dupes.py`（幂等）。
- [x] **`finance` 分类混入非金融工具 —— 2026-09-17 已完成（零 301）**：核实 11 个嫌疑工具，仅 8 个确为非金融混入（word-scramble / wifi-password-show 在 finance 目录不存在已剔除；currency-converter 货币换算确属金融剔除）。**修法：仅改页面 meta `industry=`（分类页按 industry 分组、URL 按目录，故零 301）**，目标行业均核存在于 INDUSTRY_DEFS（注意 `dev` 不存在，密码/二维码改归 security/general）：driver-license-validator→life、mirror-text→text、word-wrap→text、word-search→fun、dns-record-info→network、password→security、password-generator-advanced→security、vcard-qr→general。构建重建触发 141 个相关卡 rt-icon + 分类索引/industry-json/sitemap/tools.json 结构性更新（无内容破坏，214 门禁含链接/资产审计全过已证）。脚本 `scripts/fix_finance_misclass.py`（幂等）。已提交 `fa3fc30de` + 推送 + 线上 MD5/404 双证据。
- [ ] **`science/calc-1` 错公式已修**：原写 pH 公式（张冠李戴），实为自由落体工具，已改为 `s=½gt²`。
- [x] **`statistics-4/5`（置信区间 / 样本量）逆正态 z 反解公式 —— 2026-09-16 已修复**：原实现用错误常数 `a=0.147` 的近似，cl=95 反解出 z≈0.0008 → CI 退化为样本均值、样本量恒为 1。现改用 Acklam probit `normalInv`（cl=95→z≈1.96、cl=99→z≈2.576），两页 JS 已改 + 门禁补 2 道回归断言（verify_statistics_calc 37→39/39）。
- [ ] **`legal/traffic-accident-compensation` 伤残赔偿系数倒置已修**：公式改为 `(11 - injuryLevel)/10`（一级=1.0、十级=0.1），verify_legal_calc.js 已补 2 防回归用例，提交 `f07e5ff0d`。

**P2 — 低优先级**

- [ ] **指南英文副本（`guides/*.en.html` 约 100 篇）清理 —— 2026-09-17 老板明确：英文指南优先级低，延后处理，后续专门开任务**：项目早改 `?lang=en-US` 单页 runtime 模式，这 ~100 篇 `*-guide.en.html` 是早期独立英文副本（git 跟踪 + sitemap 收录），属死重复页。**暂不处理**——删/改属 SEO 不可逆动作（直接影响约 100 个线上 URL 的索引与权重，处理不当会 404 掉索引）。后续专门任务须评估：① 是否下架并 301 指向 `?lang=en-US` 等效页；② 清理后须同步 sitemap.xml / `json/guides.json` / 构建产物，避免死链门禁挂；③ 须先出全量 301 规划再动，禁止直接删。记录于此，待老板指定时机单独推进（不与其它优化混批）。
- [ ] **跨分类真重复工具去重（D 全站审计，2026-09-17 启动，进行中）**：
  - **第一批**（h1 完全同名）已下架 5 个（commit `9bffc3229`，总数 4821→4816）。
  - **第二批**（h1 模糊近似 + 系统双命名）已下架 19 个「模板短名 vs 描述性专名」冗余：全站 h1 归一化模糊聚类（≥0.82）得 387 相似对 → 108 对同目录且差异仅在于「器/计/算」后缀+全半角括号，呈**机器模板命名（calc-N/rater-N/assessor-N/analysis-N/convert-N/拼音/date-diff 等）vs 描述性专名**双命名；逐对比对 calc 真实输入集，仅删「专名版为模板版输入超集（不丢功能）且无全局复用歧义」的 19 对（如 `rater-25`→留`bishop-score`、`due-date-1`→留`due-date`、`rater-3`→留`ipss-score`）；另 2 对（`calc-2`/`calc-3`）因 basename 全局 30+ 行业复用移出单列专项。commit `5057f5744`，214 门禁全过、线上删除页 404、tools.json 残留 0、总数 4816→4797。脚本 `scripts/retire_template_dupes.py`（幂等，字符级括号匹配兼容内联 `{ slug:`）。
  - **第三批**（跨目录/同目录确凿真重复，2026-09-17 晚）已下架 3 个：对全站 h1 strict 归一化聚类得 11 对同名候选，逐页比对 calc 输入集+公式系数取证实为 3 处确凿真重复（输入集相等或冗余方⊆权威方，删冗余方零功能丢失）：`materials/density-basic`（ρ=m/V 与 `science/density-physics` 输入集完全相同）→ 留 science 版；`science/z-score-calculator`（Z=(x-μ)/σ 与 `statistics/z` 输入集相同）→ 留 statistics 版；`fitness/calculator-calc-metabolism`（Mifflin+Harris 双公式 BMR ⊆ 全局复用页 `fitness/calc-2`）→ 留 calc-2。commit `00af9e70f`，214 门禁全过、线上删除页 404、tools.json 残留 0、总数 4797→4794。脚本 `scripts/retire_redundant_crossind.py`（幂等；清理逻辑修复：① chip 抓取改为精确路径+通用 `<a>` 链接含相对路径 `related-tool-card` 与跨行闭合 ② 遍历递归 `tools/**/*.html` 二级子目录）。
  - **剩余（基本完成，建议暂停/专项）**：经三批（5+19+3=27 个）下架后，全站 strict 同名仅余 11 对候选，已逐对取证——`hematology/mpn-scoring`vs`rater-5`（DIPSS 含细胞遗传学 vs MPN-10 症状问卷，异算法）、`quality/process-capability`vs`calc-cpk`（双组规格 vs 原始数据录入，实现差异大）、`edu/gpa-calculator`vs`exam-gpa-calculator`（累计 GPA vs 考试 GPA，语义微差）、`safety/accident-stats`vs`stats-report-frequency`（标准 KPI vs 通用报表）、`marketing/marketing-roi`vs`investment/roi-calc`（营销多口径 vs 投资简单 ROI，跨目录异语义）、`it/csharp-cheatsheet`vs`cpp-cheatsheet`（C# vs C++，明显异功能）均**非简单重复不下架**；其余 ~84 对为全局复用编号页（calc-N/rater-N 跨行业同名，牵连系统性命名，需单列专项）与描述性短名对（多已证为同名异功能）。继续硬删风险高，建议暂停 D 项或后续开专项。
  - **已排除（不下架，仅记录）**：同名异功能 `finance/salary-after-tax`(累计预扣)vs`payroll-calculator`(含年终奖比例)、`ophthalmology/self-assess-2`vs`osdi-scale`(OSDI 两算法)。
- [x] **全站非法 cat 排查与 `daily` 补注册 —— 2026-09-16 已修复**：原记「4 处（baking/biz/daily/automotive）标签回退裸 slug」经核查不准确——`baking/biz/automotive` 均在 `INDUSTRY_DEFS`，搜索卡走 `INDUSTRY_INFO`、构建走 `INDUSTRY_DEFS` 回退，中文标签正常（`🧁烘焙甜点`/`💼商业办公`/`🚗汽车交通`）；**唯一真正两处字典都缺（且不在 `INDUSTRY_DEFS`）的是 `daily`**（`tools/life/parking-fee.html`，cat=daily、industry=life），其分类筛选页标题（`js/app.js` `CAT_INFO['daily']` 缺失）会显示裸 "daily"。已补注册：`_build.py` `CAT_DEFS` 加 `daily:('🗓️','#e1f5fe','日常工具')` + `js/app.js` `CAT_INFO` 加同名条目（两处均为分类名权威源）。`reproductive-medicine`（28 工具）虽不在 `CAT_DEFS` 但在 `INDUSTRY_DEFS`，渲染正常，未动。全 214 道门禁通过。
- [x] **`design/color-shade-generator` 亮色梯度实现缺陷 —— 2026-09-16 已修复**：`mix(c,t)` 实为 `Math.round(t)`，tint 侧退化为纯灰度（`#d5d5d5` 档）、与基色无关。改为三参 `mix(c,t,r)=round(c+(t−c)·r)`（对齐页面公式 `tint=C·(1−t)+255·t`），tint 侧 `mix(rgb,255,f)`、shade 侧 `mix(rgb,0,f2)` 均按混合比例插值；基色 #6366F1/steps=5 现得最浅 tint `#e5e6fd`、最深 shade `#111128`。门禁补 1 道判别性回归用例（`expect:["#e5e6fd"]`，仅正确 tint 命中；灰度/NaN 态均不含此串）—— 踩到并行改同文件导致 142 行被覆盖的坑，已逐行复核落盘。
- [x] **`hydraulic/calc-1`（达西-魏斯巴赫 + Blasius）纳入真实门禁 —— 2026-09-16 已修复**：原记"未纳入门禁"准确；已补一道 runCase（slug=`hydraulic/calc-1`）：取绝对粗糙度=0 走确定性 Blasius 摩阻（`λ=0.3164/Re^0.25`，避免 Colebrook 迭代浮点歧义），独立复算 v=1.273m/s、Re≈1.27e5 紊流、hf=1.386m、ΔP=16.43kPa 并断言。hydraulic 门禁 17→18/18，全 213 道门禁 + 反伪自检 risk=0。
- [x] **`fun/convert-speed-stride` 单位换算 select 值 —— 2026-09-16 核查非 bug**：原记"选 0 除零"不准确，当前代码 `from`/`to` 的 option 值为 `1 / 0.001 / 1000`，**无字面 0**，不会出现除零；公式为 `v*rate*f/t`，属通用乘算器。语义偏"步幅↔速度"标签不严谨（维度不同），但非计算错误，未改（避免伪功能改动）。
- [ ] **`fun` 行业图标 🎮 语义一致性（2026-09-17 复核：原条目举例不准确，降级为设计决策项）**：原记"含计算类工具（烧烤分量计算器）图标与语义不符"经实测**不成立**——`bbq-portion`/`hotpot-portion`（烧烤/火锅分量计算器）命中 TOOL_ICON_RULES 的"计算器/分量"规则，实际图标为 `🧮`（正确），并非 🎮；`convert-speed-stride`/`step-stride` 为 `🏎️`。真实情况：`INDUSTRY_DEFS['fun']=('🎮','娱乐游戏')`（行 1056）是**行业默认兜底图标**，与 `CAT_DEFS['fun']=('🎉',…)`（行 993）不一致；`tool_icon_candidates` 优先用 TOOL_ICON_RULES，仅**无专属规则的非游戏 fun 工具**（如 `fingerprint-types` 指纹演示）回退到 🎮。23 个得 🎮 的工具绝大多数是真游戏（tetris/number-guess/各记忆游戏等），命中游戏规则，属正确。**结论**：当前态可接受；若要消除非游戏 fun 工具的 🎮 兜底，需把 `INDUSTRY_DEFS['fun']` 改为 `🎉`（中性），但该改动同时改变 fun 行业页头图标与所有无规则兜底工具，**属可见设计变更，须老板拍板，未擅自改**。
- [x] **`_build.py` desc 图标剥离正则漏 `\u2300-\u23FF` —— 2026-09-16 核实：可见影响为零，不改**：原记「74 页受影响」不准确——实为 **34 条** desc（tools.json 34/4825，industry-*.json 合计 34/4837；h2 层 33 页），图标为 ⏱×46/⌨×8/⏰×8/⏲×4/⌥×2。**关键：desc 用户不可见**，已逐链路取证：① `tools.json` 4825 条**全部有 `d`**（中文），`industry-*.json` 工具条目亦 4825/4837 全有 `d`（缺的 12 条是 `industry-groups.json` 的行业分组，非工具页、无 desc 展示）；② 前端一律走 `(t.d || t.desc)` 兜底链（`js/app.js:49`/`682`、`js/common.js:2337`），`desc` 永不抵达用户；③ `_build.py:232` 热度评分同为 `d or desc`；④ `generate_tools_js()` 产物**是死代码**——其输出传给 `update_index_html(INDEX_FILE, tools_js, …)` 但该函数从不使用此参数，首页 index.html 内亦无 `const tools`。另：`tools.json` 有 4760/4825 desc 为英文，但 h2 **预渲染英文是设计意图**（`js/tool-i18n.js:410` 注释明示「预渲染英文到静态 HTML」，中文由 `data-zh` 回写），并非缺陷。**结论：不动判据、不动提取源**，仅记录。`_build.py` 全站无 `\uFE0F` 处理（emoji 变体选择符）亦为既有行为，未改。
- [ ] **data-zh「中文原文」容器属性损坏 —— 2026-09-16 已修 197 页（本轮新增）**：`js/tool-i18n.js` 运行时用 `getAttribute('data-zh')` 覆盖 `h2`/intro `p` 的 `textContent` 作为中文态文案，故 data-zh 里任何脏字符都**直接显示给中文用户**。无头 Chrome 取证：`design/checker` intro 显示「`>输入前景色和背景色…`」（对照正常页 `edu/exam-timer` 为「倒计时、正计时、休息提醒一体化」）。两类损坏：① **194 页 intro `<p>` 的 data-zh 前导多余 `&gt;`**（science 74/design 57/finance 57/audio 1 等，根因=mardown 引用行 `> 描述` 的引导符被带入）；② **4 页 `<h2>` 的 data-zh 被塞入转义 `<span>`**（base64-converter/jwt-parser/stock-profit-calculator/dehumidifier），英文正文另多一个 `&lt;`。修法见 `scripts/fix_data_zh.py`（幂等，`pre-commit` 可复跑）：剥前导 `&gt;`（**仅剥离开头一个**，正文中间如 `TDS&gt;5.45` 属合法内容不动）+ 4 页 h2 按「页面 `<title>` / i18n `zh-CN.title`」权威源重写、图标沿用页面原有（不取 meta icon，后者只是占位）。**未处理 46 条 B 类**：data-zh 内含真实 HTML 标签 / JS 模板（`<strong>…${map.size}` 等），属运行时动态文案模板，非损坏。
- [x] **多卡片页 intro 段落漏翻译 —— 2026-09-17 已修（第 497 条转此）**：`js/tool-i18n.js:400` 的选取器是 `card.querySelector('p')`，而 **多卡片布局页的主工具卡（`.tool-card-accent`）内可能完全没有 `<p>`**，此时 introP 为 null，全页唯一的 `<p data-zh>` 落在次级卡片里、永不被写回，中文用户看到静态英文。**定量**：全站精确模拟选取语义后用**注入式浏览器探针**（向页面注入脚本读回运行时 `$0` 命中结果并写入 `<title>`）复核，确认为 **4 页**（`design/glassmorphism-generator` / `design/shadow-generator` / `finance/discount-calculator` / `it/jwt-parser`）。另外定性到一个**更深的双重错配**：这 4 个段落是次级卡片的小节说明（中文 data-zh 为「选择背景图案」「点击应用预设阴影」「点击可将该折扣填入正向计算…」「填写 Payload 与密钥…」），英文正文却被灌成了 `<meta name="desc-en">` 的**主介绍**，中英语义完全不搭。**修法两处缺一不可**：① `js/tool-i18n.js` 加保守回退 —— 仅当 `introP === null` 时取首个 `p[data-zh]` 作为 `fbP`，且**只在非英文态写回 `data-zh`**；英文态刻意**不套** `body.intro`（那是主介绍，套上会把错配固化）；该分支全站仅 4 页触发，其余 5029 页走原路径不变。② 4 页静态英文改为与小节中文语义对应的英文。**验证**：双语渲染（含 `?lang=en-US`）4 页中文态/英文态全部正确；另抽样 40 页确认零回归。
    - **踩坑（防复发）**：判定「intro p 是否落在某容器内」**不可用自研 `HTMLParser` 的起止偏移** —— 本项目大量页面的首个 `<div class="card">` 标签未闭合，Python 解析器拿到 `end=None`，会把本在容器内的段落误判为「容器外」（psychology 三页即为此假阳性，实际运行时正常）。可靠做法是向页面注入探针脚本、用真实浏览器 DOM 读回选取结果。
    - **踩坑（防复发）**：放宽运行时选取器前**必须先读 `applyToolBody` 的英文分支**（`introP.textContent = body.intro`，行 ~447）。若盲目放宽，英文态会把主介绍灌回小节说明，等于把错配写死。故回退分支要独立成键（`ORIG[slug].fbIntro`），不与主 intro 共用。
- [ ] **`psychiatry.json` 并行进程未提交改动**（mtime 2026-09-13）：需老板确认归属。
- [x] **`funeral` 和 `dance` verify 跑超时 —— 2026-09-16 核查非问题**：原记"60s 内没返回"不准确，当前 `verify_funeral_calc.js`（5/5）、`verify_dance_calc.js`（7/7）均 **0.1s 完成**，无超时。疑似早期批次已修复或记录有误，未再处理。
