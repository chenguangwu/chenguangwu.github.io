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

## 八、分类推进记录

> ✅ **`ai` (64) 已收口**（2026-09-13 开工并完成）。**范围**：`tools/ai/` 全部 64 个工具页。
> **八项基线审计（2026-09-13）**：deep-dive **已达 §4.5**（64/64，3 场景 / 2 FAQ / 1 示例，192/64/128，无套话）；UI 零缺项；cat 0 错标；**英文 p 占位 63**；**formula 口径完全反了**（8 个文本/图像 demo 反而有框，56 个真计算器全无框）；计算验证 0；**指南 0**；英文态（intro 占位 64、真代号 3 `Ai 8/9/12`、ed 不达标 1）。中文态无缺口。
> **批次计划（全部完成）**：A 英文态数据源根治 → B 英文占位正文注入 → C formula 补框（口径纠正后 56 页）→ D 计算验证（第 13 道门禁）→ E 指南 0→64 → 收口归档。
> **收口结果（2026-09-13）**：① 英文态八维全清零（64 条真实英文名 + 英文描述三端同步；消除 `Ai 8/9/12` 代号）② 63 页英文占位正文改真实英文 + data-zh 中文保留（沿用已验证流程：临时改 `_prerender_tool_body` → build → 只保留 ai 落盘 → 回退 `_build.py` 与其它行业改动）③ **纠正 formula 判定口径**：`math/dev/reference/calculator` 四类 cat 与「是否计算工具」无对应关系，改用客观口径（`type="number"` 输入 ≥2 判计算类）；据此为 **56 个真计算器全部补框**（公式逐条对照页面 `function calc()` 实现撰写），计算类覆盖 56/56，8 个交互 demo（OCR/语音/情感/图像分类等）豁免 ④ 新增第 13 道门禁 `verify_ai_calc.js` **9/9** 通过 ⑤ 指南 0→64（数据驱动生成器，内容取自 ai.json 中文 title/intro + formula MAP + deep-dive 场景/示例/FAQ + 页面 input 标签，非套话）。十三道质量门禁全过。

> ✅ **`fun` (64) 已收口**（2026-09-12 开工并完成）。**范围**：`tools/fun/` 全部 64 个工具页。
> **八项基线审计（2026-09-12）**：deep-dive **已达 §4.5**（64/64，(3 场景 / 2 FAQ / 2 示例)，192/128/128，无套话）；UI 零缺项；cat 0 错标；**英文 p 占位 55**；formula 缺 25（其中计算类仅 4 个，21 个为 game/generate 豁免）；计算验证 0；**指南 64/64 已全覆盖**；英文态（body intro 占位 82、title 代号 7、en_override 代号 7、ed 不达标 3、**孤儿键 26**）。
> **批次计划（全部完成）**：A 英文态数据源根治（含三端孤儿键清理 + 中文 title/intro 补齐）→ B 英文占位正文注入 → C formula 补框 → D 计算验证（第 12 道门禁）→ 收口归档。
> **收口结果（2026-09-12）**：① 英文态八维全清零（64 条真实英文名 + 英文描述三端同步；清 26 个 body 孤儿键 + 24 个 `_en_override` 孤儿键 + 9 个 `fun.json` 孤儿键，其中含彩票/老虎机/轮盘/牌力/地址生成等不合规类别残留，清理后线上无入口）② 补 6 个工具缺失的中文 title/intro（bbq-portion / gomoku-ai / hotpot-portion / meditation-timer / random-name-gen / wedding-banquet），修复 `<title>` 退化为英文 slug ③ 55 页英文占位正文改为真实英文 + data-zh 中文保留（沿用 sports 验证流程：临时改 `_prerender_tool_body` → build → 只保留 fun 落盘 → 回退 `_build.py` 与其它行业改动）④ formula 计算类覆盖 11/11（4 页补框：烧烤/火锅分量、冥想计时、婚宴桌数）⑤ 新增第 12 道门禁 `verify_fun_calc.js` 5/5 通过 ⑥ 修复 3 个空 `<select>`（meditation-timer style、wedding-banquet type/backup，无 option 且无 JS 填充 → 用户看到空下拉框、计算恒走默认值）。十二道质量门禁全过。

> ✅ **`sports` (75) 已收口**（2026-09-12 开工并完成）。**范围**：`tools/sports/` 全部 75 个工具页。
> **八项基线审计（2026-09-12）**：deep-dive 原 75/75 条目存在但条数不达标（scenarios 恒为 1、faqs 恒为 1，同 science 第三种缺口形态）；UI 零缺项；cat 0 错标；英文 p 占位 47；formula 缺 24；计算验证 0；指南 0；英文态七维（body intro 占位 47、title 代号 3、en_override 代号 22、en-US 缺 0、ed 不达标 2、industry ed 不达标 2、HTML 可见英文占位串未注入）。
> **批次计划（全部完成）**：A 英文态数据源根治 → B formula 框补齐 → C 计算验证（第 11 道门禁）→ D 指南精选 → E deep-dive 条数补齐（§4.5）→ 收口归档。
> **收口结果（2026-09-12）**：① deep-dive 75/75 补齐至 §4.5 标准（场景≥2 且 示例≥1 且 FAQ≥2 且 无套话，fill_sports_deepdive，150 场景/75 示例/150 FAQ，达标率 100%）② 英文态七维全清零 + 修复 build 非 CJK 占位页英文未注入根因（sports 75 页 h2/首个 p 由英文占位串改写为真实英文、data-zh 中文保留；_build.py 改动因波及全站已回退，sports 页修正落盘保留，全站缺陷记入 §9.3）③ formula 覆盖 24 页补框（fix_sports_formula_map，TITLE_CALC='📐 计算公式 / 原理'）④ 计算验证第 11 道门禁 verify_sports_calc.js 8/8 通过 ⑤ 指南 0→8（gen_sports_guides，estimate-tester/tester-1/calc-heart-rate-1/calculator-calc-time/swimming-stroke-efficiency/calculator-calc-9/estimate-35/xuerusuanyuzhiceding）⑥ 清 6 孤儿键。十一道质量门禁全过，部署 run 34688676392 success（线上 MD5 逐字节一致）。

> ✅ **`science` (99) 已收口**（2026-09-12 开工并完成）。**范围**：`tools/science/` 全部 99 个工具页。
> **八项基线审计（2026-09-12）**：deep-dive 99/99 **条目存在且内容真实**，但**条数不达标**（scenarios 恒为 1、faqs 恒为 1 —— 与 finance 的「套话」、design 的「达标」均不同，是第三种缺口形态）；UI（common.js/i18n.js/viewport/lang/toolbox）零缺项；cat 0 错标；无输入项 2（`calculator` / `logic-gate-simulator`，待核实）。**缺口**：① deep-dive 条数 99 ② 英文 p 占位 93 ③ formula 缺 25 ④ 计算验证 0 ⑤ 指南 15/99。
> **数据源现状**：`science-body.json` 103 条（孤儿 4：`convert-5` / `calculator-calc` / `simulator-circuit` / `simulator-3`）、intro 占位 94、title 代号 5（cycle / fibonacci / pHCalculator / prime-number / xianxingfangchengzuqiujie-2yuan-3yuan）；`science.json` 98 条、缺 1（`significant-figures`）、en-US 套话 83；`_en_override` en 代号 5、ed 不达标 93；`industry-science` ed 不达标 3。
> **批次计划（全部完成）**：A 英文态数据源根治 → B deep-dive 条数补齐 + formula → C 计算验证（第 10 道门禁）→ D 指南精选 → 收口归档。
> **收口结果（2026-09-12）**：① deep-dive 99/99 各补 1 scenario+1 faq（fix_science_deepdive）② 英文态七维全清零（fix_science_body_i18n + 全站 `fix_h2_entities` 修复 32 页 h2 实体多重转义损坏）③ formula 覆盖 99/99 + 修正 calc-1 错公式、移除 cycle 重复工具、根因修复 script 内 formula-box 误注入（fix_formula/fix_science_formula_map）④ 计算验证第 10 道门禁 verify_science_calc.js 8/8 通过 ⑤ 指南 15→23（新增 8 篇旗舰计算器指南，gen_science_guides）⑥ cycle 重复工具移除、4 个孤儿键记入 §9.3。十道质量门禁全过，部署 run 34684543764 success。
>
> ✅ **`design` (103) 已收口**（2026-09-12，八项目标全达标，部署 run 34674667024 success）。历史 `it` (345) / `general` (180) / `finance` (112) 归档见 §9.1 白名单（跨分类经验已沉淀至 §4.5 / §6）。
> **`design` 批次明细（已完成，留存备查）：**
> - **八项基线审计（2026-09-12）**：deep-dive **103/103 条数达标且套话≈0**（仅 `font-pairing` examples 1 处）；UI（common.js/i18n.js/viewport/lang/toolbox）零缺项；cat 0 错标；无输入项仅 `bpm-tapper`（按钮驱动节拍器，合理）。缺口：① 英文 p 占位 92 ② formula 缺 49 ③ 计算验证 0 ④ 指南 7/103。数据源（混合半成品）：`design-body.json` 缺 9 + 孤儿 3（generator-5 / color-scheme-generator / simulator-2）、intro 占位 94、title 代号 6；`design.json` 缺 9、en-US 套话 52；`_en_override` en 代号 6、ed 不达标 96；`industry-design` ed 不达标 3。
> - **① 英文态数据源根治（批次 A）**：新建 `fix_design_body_i18n.py` 为 103 工具写真实英文名 + 描述，同步 `_en_override.json`（en/ed）、`design-body.json`（title/h1/intro + en 嵌套）、`design.json`（en-US）三端，并补 9 + 9 条缺失条目与 9 条缺失 zh-CN。复用已泛化脚本：`fix_formula_intro_p.py --industry design`（30 个公式页的 formula-desc 是首个 `<p>`，改 `<div>` 并在框后补中文 intro `<p>` —— 否则首个 `<p>` 会落到 `<script>` 内 JS 模板串，41 页）、`fix_prerender_reset.py --industry design --intro-p`（还原已预渲染 h2 92 处 + 首个 `<p>` 61 处让 build 重注入）。
> - **② formula 全量补齐（批次 B）**：把 `fix_finance_formula.py` 的插入/更新逻辑**抽为通用** `scripts/fix_formula.py`（`--industry` + `--map module:VAR`，锚点 input-row → input-row2 → h2 后首个 `<p>`），数据单放 `fix_design_formula_map.py`。共 91 处：49 无框插入完整框（单位换算 px/rem/vw/vh、DPI、冲印尺寸；色度学 WCAG 相对亮度、色温近似式；摄影光学 景深/超焦距、等效焦距与视角；版式 间距/字阶等比数列）、24 有框无 desc 补依据、16 套话换真实说明；纯生成器类按 §4.1.2 给「参数参考表/核心算法说明」，不编造公式。识别修正：`vh-vw` 原有空壳框（仅 title）遗漏在首轮统计外，补入 MAP 后修复。→ **103/103 均有真实 formula**。
> - **③ 计算验证 12 用例（批次 C，第 9 道门禁）**：新建 `scripts/verify_design_calc.js`（复用 DOM stub 框架）：单位换算 7（px↔rem、px→vw、像素↔英寸 DPI、冲印尺寸 cm、间距/字阶等比数列）+ 色度学 3（WCAG 对比度 ×2：`#1F2937`/白 = 14.68:1、`#333`/白 = 12.63:1；Tanner Helland 色温近似式 5500K → `#FFEDDE`）+ 摄影光学 2（景深/超焦距 f=50 N=1.8 c=0.03mm → H 46.3m、近点 1.92m；等效焦距视角 50mm 全画幅 → 39.6°×27.0°）。期望值全部标准公式独立复算并显式注入；依赖 canvas / WebAudio / 点击 / 「今天」的工具不纳入。刻意排除 `color-shade-generator`（亮色梯度经 `mix()` 退化为纯灰度、与基色无关，属工具自身实现缺陷，不可为其背书，另记 §9.3）。`run_gates.py` 由 8 项扩为 9 项。
> - **④ 指南精选 15 篇 + deep-dive 复检（批次 D）**：deep-dive 103/103 条数达标，scenarios/faqs 与 examples 套话均为 0（无 finance 那类模板）；入库初判的「英文名嵌中文 5 处」经逐字段核查为**误报**（命中的是 `title` 字段本身的英文名，属预期）。已有指南 7 篇（5 篇真实 + `image-to-ascii` 为「原理/参数/FAQ」内容集群版式）内容真实、仅条数 3–4 条非模板，保留不改。新增 15 篇（单位换算 7 / 色度学 1 / 摄影光学 4 / 存储配色 3），新建 `fix_design_guide_fields.py` 补真实 features(4)/steps(5)/tips(4) 后跑 `gen_guide_pages.py --industry design`；跨分类重名 slug（audio-recorder / image-compress / image-mosaic / image-to-base64 / image-watermark）不纳入，避免与既有 `guides/<slug>-guide.html` 互覆。
> - **最终结果**：deep-dive 达标 103/103（套话 0）、UI 零缺项、cat 0 错标、formula 覆盖 103/103、**英文态七维全清零**（页面残留 0 / script 内误注入 0 / h2 代号 0 / body.intro 0 / body.title 0 / `design.json` en-US 0 / ov.en 0 / ov.ed 0 / industry-design ed 0）、计算验证 12、指南 22（7→22）、指南链接注入 15/15；**八项目标全达标**。9 道门禁全过（design 12/12、finance 20/20、general 19/19、it 28/28），Actions `2a57f8ab4` / `5273b8cda` / `7c4fbb699`（run `34674667024`）全 success。
> - **遗留（非 design 缺口，记入 §9.3）**：① `design-body.json` 3 个孤儿键（generator-5 / color-scheme-generator / simulator-2）全站无页面；② `color-shade-generator` 亮色梯度实现缺陷（`mix()` 退化为纯灰度）；③ `contrast-checker` 与 `color-contrast-check` / `checker` 主题重复，分类去重待老板确认；④ 5 个跨分类重名 slug 的指南缺口。

## 九、未完成任务清单

> **推进方式**：恢复「按分类逐行优化」。分类按**热度（分类下工具页数量，覆盖用户面代理）降序**排列于 §9.2，从最热的 `it`(345) 起逐分类推进。**历史已完整优化的分类见 §9.1 白名单，不列入本清单**。§9.3 为跨分类 / 独立的孤立未完成任务，可穿插推进但不替代逐分类收口。硬约束唯一权威见 §4.3。

### 9.1 历史已优化分类白名单（开工前先审计，满足则跳过）

> 以下分类此前已完整走完 §4.1 八项目标（git 实测），**不重新从零做**；开工首批即先按 §4.1 八项目标审计，满足则标记完成移出待办，不满足仅补缺项后移出。

- ✅ automotive (53)：45 死壳重建、C 级清零、八项目标全覆盖（git 实测）
- ✅ fire-rescue (40)：已收口分类（§4.4 明示）
- ✅ psychology (20)：已优化过一遍（§4 开头「先验证后跳过」指令）
- ✅ it (345)：八项目标全覆盖（deep-dive 345/345、套话/占位/公式 0、指南 40、计算验证 28/28、英文描述 297 真实化、页面 UI 100%；部署 run 34632953856 success），git 实测
- ✅ general (180)：八项目标全覆盖（deep-dive 180/180、p 占位/套话/formula 缺失 0、ed 与 desc-en 套话 0、指南 31、计算验证 19、英文态数据源根治；部署 run 34672625411 success），git 实测
- ✅ finance (112)：八项目标全覆盖（deep-dive 达标 112/112、scenarios/faqs 与 examples 套话 0、formula 全覆盖、英文态三端套话 0、计算验证 20、指南 26、指南链接注入 20/20；部署 run 34673915217 success），git 实测
- ✅ design (103)：八项目标全覆盖（deep-dive 103/103 达标且套话≈0、formula 覆盖 103/103、英文态七维全清零、计算验证 12、指南 22、指南链接注入 15/15；部署 run 34674667024 success），git 实测
- ✅ science (99)：八项目标全覆盖（deep-dive 99/99 条数补齐、英文态七维全清零含全站 h2 实体修复 32 页、formula 覆盖 99/99 + calc-1 错公式修正、计算验证 8/8（第 10 道门禁 verify_science_calc.js）、指南 23（精选新增 8 篇旗舰指南）、cycle 重复工具移除、script 内 formula-box 误注入根因修复；部署 run 34684543764 success），git 实测
- ✅ sports (75)：八项目标全覆盖（deep-dive 75/75 达 §4.5 标准、英文态七维全清零、formula 覆盖 24/24 补框、计算验证 8/8（第 11 道门禁 verify_sports_calc.js）、指南 8、6 孤儿键清理；部署 run 34688676392 success（线上 MD5 逐字节一致）），git 实测
- ✅ fun (64)：八项目标全覆盖（deep-dive 64/64 已达 §4.5、英文态八维全清零含三端 59 个孤儿键清理、中文 title/intro 补齐 6、formula 计算类覆盖 11/11、计算验证 5/5（第 12 道门禁 verify_fun_calc.js）、指南 64/64、修复 3 个空 select；部署 run 34703760306 success（线上 MD5 逐字节一致）），git 实测
- ✅ ai (64)：八项目标全覆盖（deep-dive 64/64 达 §4.5、英文态八维全清零、formula 口径纠正后计算类覆盖 56/56、计算验证 9/9（第 13 道门禁 verify_ai_calc.js）、指南 0→64；部署 run 见发布核验回填），git 实测

> 跳过规则：上述分类**不列入 §9.2 待办**；其余分类按 §9.2 热度顺序从零推进。

### 9.2 分类优化清单（257 分类，按热度降序，完成一个删一个）

> 清单由脚本按 `tools/` 目录工具数生成；每行 = 分类名 + 工具数。当前进行中的分类在 §8 同步登记。

- [ ] biz (62)
- [ ] life (62)
- [ ] agriculture (60)
- [ ] hydraulic (55)
- [ ] statistics (55)
- [ ] legal (54)
- [ ] realestate (54)
- [ ] energy (46)
- [ ] health (46)
- [ ] edu (44)
- [ ] marketing (44)
- [ ] meteorology (42)
- [ ] optical (41)
- [ ] surveying (40)
- [ ] fishery (38)
- [ ] securities (38)
- [ ] aerospace (37)
- [ ] geology (37)
- [ ] machinery (37)
- [ ] math (36)
- [ ] accounting (35)
- [ ] fitness (35)
- [ ] eco (34)
- [ ] cosmetic-derm (33)
- [ ] healthcare (33)
- [ ] insurance (33)
- [ ] obstetrics (32)
- [ ] ophthalmology (32)
- [ ] encode (29)
- [ ] metalwork (29)
- [ ] photo (29)
- [ ] tax (29)
- [ ] acoustics (28)
- [ ] chemistry (28)
- [ ] dynamics (28)
- [ ] economics (28)
- [ ] electromagnetism (28)
- [ ] fluid (28)
- [ ] geometry (28)
- [ ] investment (28)
- [ ] kinematics (28)
- [ ] materials (28)
- [ ] metrology (28)
- [ ] nuclear (28)
- [ ] optics (28)
- [ ] quantum (28)
- [ ] reproductive-medicine (28)
- [ ] robotics (28)
- [ ] signal (28)
- [ ] structural (28)
- [ ] thermodynamics (28)
- [ ] banking (27)
- [ ] hematology (27)
- [ ] livestock (27)
- [ ] neurology (27)
- [ ] clinical-nursing (26)
- [ ] construction (26)
- [ ] dentistry (26)
- [ ] pulmonology (26)
- [ ] astronomy (25)
- [ ] cardiology (25)
- [ ] clinical-lab (25)
- [ ] pediatrics (25)
- [ ] psychiatry (25)
- [ ] rheumatology (25)
- [ ] urology (25)
- [ ] ballistics (24)
- [ ] dermatology (24)
- [ ] electronics (24)
- [ ] food (24)
- [ ] food-testing (24)
- [ ] nephrology (24)
- [ ] rehabilitation (24)
- [ ] tcm-pharmacy (24)
- [ ] acupuncture (23)
- [ ] ent (23)
- [ ] gastroenterology (23)
- [ ] tcm-chemistry (23)
- [ ] endocrinology (22)
- [ ] forensic-medicine (22)
- [ ] beauty (21)
- [ ] civil (21)
- [ ] ecommerce (21)
- [ ] food-processing (21)
- [ ] hr (21)
- [ ] property (21)
- [ ] tcm-diagnosis (21)
- [ ] textile (21)
- [ ] travel (21)
- [ ] blasting (20)
- [ ] data (20)
- [ ] forestry (20)
- [ ] electrical (19)
- [ ] music (19)
- [ ] language (18)
- [ ] nutrition (18)
- [ ] advertising (16)
- [ ] metallurgy (16)
- [ ] niche (16)
- [ ] safety (16)
- [ ] leather (15)
- [ ] transport (15)
- [ ] welding (15)
- [ ] engineering (14)
- [ ] image (14)
- [ ] mechanical (14)
- [ ] medical (14)
- [ ] mining (14)
- [ ] process (14)
- [ ] dyeing (13)
- [ ] pr (13)
- [ ] chemical (12)
- [ ] gardening (12)
- [ ] misc (12)
- [ ] paper (12)
- [ ] elderly (11)
- [ ] fire (11)
- [ ] gas (11)
- [ ] security (11)
- [ ] text (11)
- [ ] usedcar (11)
- [ ] hvac (10)
- [ ] misc2 (10)
- [ ] pet (10)
- [ ] procurement (10)
- [ ] baking (9)
- [ ] sales (9)
- [ ] admin (8)
- [ ] cleaning (8)
- [ ] cognition (8)
- [ ] decor (8)
- [ ] logistics (8)
- [ ] quality (8)
- [ ] rental (8)
- [ ] research (8)
- [ ] restaurant (8)
- [ ] telecom (8)
- [ ] wedding (8)
- [ ] audio (7)
- [ ] dance (7)
- [ ] hotel (7)
- [ ] office (7)
- [ ] parenting (7)
- [ ] printing (7)
- [ ] archaeology (6)
- [ ] chinese-cook (6)
- [ ] exhibition (6)
- [ ] film (6)
- [ ] floral (6)
- [ ] funeral (6)
- [ ] home (6)
- [ ] jewelry (6)
- [ ] media (6)
- [ ] packaging (6)
- [ ] road (6)
- [ ] startup (6)
- [ ] urban (6)
- [ ] video (6)
- [ ] accessibility (5)
- [ ] antiques (5)
- [ ] aquaculture (5)
- [ ] audit (5)
- [ ] bonding (5)
- [ ] bridge (5)
- [ ] ceramics (5)
- [ ] chess (5)
- [ ] chinese (5)
- [ ] edu2 (5)
- [ ] fengshui (5)
- [ ] forex (5)
- [ ] futures (5)
- [ ] gardening2 (5)
- [ ] glass (5)
- [ ] kids (5)
- [ ] legal2 (5)
- [ ] library (5)
- [ ] logistics2 (5)
- [ ] manufacturing (5)
- [ ] maritime (5)
- [ ] martial (5)
- [ ] medical2 (5)
- [ ] museum (5)
- [ ] pet-training (5)
- [ ] petrochem (5)
- [ ] pets (5)
- [ ] photo2 (5)
- [ ] plastic (5)
- [ ] project (5)
- [ ] railway (5)
- [ ] rubber (5)
- [ ] seismology (5)
- [ ] service (5)
- [ ] shipping (5)
- [ ] stage (5)
- [ ] stats (5)
- [ ] tunnel (5)
- [ ] woodworking (5)
- [ ] yi (5)
- [ ] colorvision (4)
- [ ] content (4)
- [ ] convenience (4)
- [ ] discipline (4)
- [ ] domestic (4)
- [ ] environment (4)
- [ ] exam (4)
- [ ] gis (4)
- [ ] network (4)
- [ ] pneumatic (4)
- [ ] textile2 (4)
- [ ] uiux (4)
- [ ] archive (3)
- [ ] beekeeping (3)
- [ ] cable (3)
- [ ] community (3)
- [ ] consulting (3)
- [ ] customer-service (3)
- [ ] food-safety (3)
- [ ] fresh (3)
- [ ] history (3)
- [ ] mold (3)
- [ ] municipal (3)
- [ ] photography (3)
- [ ] steel (3)
- [ ] unitedfront (3)
- [ ] woodwork (3)
- [ ] auto-beauty (2)
- [ ] building-material (2)
- [ ] casting (2)
- [ ] defense (2)
- [ ] furniture (2)
- [ ] heattreat (2)
- [ ] landscape (2)
- [ ] livestream (2)
- [ ] martial-arts (2)
- [ ] pharmacy (2)
- [ ] security-guard (2)
- [ ] sports-event (2)
- [ ] surface (2)
- [ ] timber (2)
- [ ] warehouse (2)
- [ ] water (2)
- [ ] yoga (2)
- [ ] beneficiation (1)
- [ ] brand (1)
- [ ] cnc (1)
- [ ] cosmetics (1)
- [ ] daily-goods (1)
- [ ] embedded (1)
- [ ] event (1)
- [ ] express (1)
- [ ] interior (1)
- [ ] knowledge (1)
- [ ] outdoor (1)
- [ ] paint (1)
- [ ] stone (1)
- [ ] supplychain (1)
- [ ] writing (1)

### 9.3 独立未完成任务（跨分类 / 孤立项，可穿插推进）

- [ ] `science-body.json` 4 个孤儿键（`convert-5` / `calculator-calc` / `simulator-circuit` / `simulator-3`）全站无对应页面（science 收口时发现），清理前先确认无页面 / 分类页引用
- [ ] `science/calc-1` 错公式已修正：原写 pH 公式（张冠李戴），实为自由落体工具，已改为 s=½gt²（fix_science_formula_map + fix_formula 支持替换错误 eq）
- [ ] `science/cycle` 重复工具（与 `periodic-table` 功能完全重叠的「交互式元素周期表」）已从 `science-body.json` / `science.json` / MAP 移除并 `git checkout` 回退污染页；属分类错放，已在 science 收口时处理
- [ ] `fire-rescue/calc-3` 脏页（英文 h2 / formula-desc 与控件错位）
- [ ] 内容翻译三类：指南 441 篇 / 工具页正文 48 处 / embed 25 处（英文内容层）
- [ ] Analytics-C 扩面（缺 Bing / Clarity 周期数据）
- [ ] SEO 描述：Description 重复 69 组未清零（全站级，可并入逐分类时顺手修）
- [ ] `i18n/tools/general-body.json` 中 107 条非 general 的占位 intro —— 全站无对应页面的**孤儿条目**（general 收口时发现），清理前先确认无页面 / 分类页引用
- [ ] `finance` 分类混入 10+ 个非金融工具（currency-converter / driver-license-validator / mirror-text / word-scramble / word-search / word-wrap / dns-record-info / password / password-generator-advanced / vcard-qr / wifi-password-show 等），属分类错放，**动分类前须先与老板确认**（涉及 URL 归属与 SEO）
- [ ] 跨分类重名 slug 的指南缺口（finance/calc-2~5 属 fitness、finance/simple-interest 属 banking、finance/word-scramble 属 fun 等）：因 `guides.json` 按 basename 去重、`guides/<slug>-guide.html` 会互覆，需 `--prefix <ind>-` 方案，暂缓
- [ ] `design-body.json` 3 个孤儿键（generator-5 / color-scheme-generator / simulator-2）全站无对应页面（design 收口时发现），清理前先确认无页面 / 分类页引用
- [ ] `ai` 收口遗留：① 行业 cat 字段（math/dev/reference/calculator）与「是否计算工具」无对应关系——8 个文本/图像 demo 被标 calculator、56 个真计算器被标 math/dev，`audit_ai.py`【5】已改用客观口径（数值输入 ≥2 判计算类），后续分类若照抄 fun 的 cat 豁免口径会重蹈覆辙 ② `_build.py` 非 CJK 占位页英文未注入缺陷**第三次遇到**（sports 75 + fun 55 + ai 63），仍按「临时改 → build → 只保留本行业 → 回退」处理
- [ ] `psychiatry.json` 存在并行进程的未提交改动（合规去敏类改名，mtime 2026-09-13 00:22），非本轮 ai 批次产物，未提交也未回退，需老板确认归属后再处理
- [ ] `fun` 收口遗留：① 21 个 game/generate 类工具无 formula-box（游戏与生成器无计算公式，按 §4.1.2 属合理豁免，`audit_fun.py`【5】已按 cat 区分判定）② `convert-speed-stride` 单位换算 select 选项值为 1/0/1000，选 0 会除零且语义不清，实现薄弱待重构 ③ fun 行业 h2 图标被语义重分配为 🎮（含计算类工具如烧烤分量计算器），图标与工具语义不符，待确认是否按 cat 细分图标规则
- [ ] `_build.py` `_prerender_tool_body` 非 CJK 占位页英文未注入缺陷（全站级，第二次遇到）：sports 75 页 + fun 55 页已分别落盘修正（h2/首个 p 由英文占位串改真实英文 + 保留 data-zh），但修复改动因波及数百非本行业页已两次回退 `_build.py`；建议单独开一轮由老板确认后统一修复（否则每个同形态分类都要重复一次「临时改 → build → 只保留本行业 → 回退」流程）
- [ ] `sports` 收口遗留：① 6 孤儿键（compare-temp / simulator-composition / tool-005-47 / tool-011-27 / tool-011-29 / zhuanxiang-pao-tiao-tou-jishufenjie）全站无页面，已从 `sports-body.json` 删除 ② `yoga-pose-generator`（cat=generate）无 formula-box 属合理例外（生成器非计算工具），不计入 formula 缺口 ③ `sports-calculator` / `swimming-stroke-efficiency` 公式框在 `<script>` 内（innerHTML 动态渲染，功能完好），非死串 bug，保留 ④ `audit_sports.py`【1】判定口径已对齐 §4.5（场景≥2 且 示例≥1 且 FAQ≥2 且 无套话），避免“数量达标≠内容达标”假阳性
- [ ] `design/color-shade-generator` 亮色梯度实现缺陷：`mix()` 退化为 `Math.round(t)`，浅色档位与基色无关（结果近似纯灰度），属工具自身算法 bug，需重写混色逻辑后再决定是否纳入门禁
- [ ] `design` 分类主题重复工具：`contrast-checker` 与 `color-contrast-check`（已有指南）/ `checker`（已有指南）功能重叠，**去重前须先与老板确认**（涉及 URL 归属与 SEO）
- [ ] `design` 跨分类重名 slug 的指南缺口（audio-recorder / image-compress / image-mosaic / image-to-base64 / image-watermark）：同 finance 情况，需 `--prefix design-` 方案，暂缓
