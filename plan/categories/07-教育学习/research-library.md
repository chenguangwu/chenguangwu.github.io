# 科研/图书馆 · tools/{research,library,archive}（~20 页）

## 功能缺陷
- 缺「样本量计算器」统一入口（alpha/效力/效应量三参数，各学科预设）。
- 缺「期刊分区速查」（静态 CAS/JCR 数据模块）。

## 优化点
- S7 引据：统计页标方法出处（Cohen 1988 等）。

## 受影响范围
- tools/research/、tools/library/、tools/archive/

## 进度
- 🔴 待开发

## 2026-11-03 第一轮抽样补充

### 逾期罚款封顶与倒序日期（中，确认函数缺陷）
- 证据：`tools/library/overdue-fine.html:265-302` 已启用封顶但 cap=0 时 `cap>0` 不成立，原函数 10 天、每本每日 0.5 元仍收费 5 元；归还早于借阅时输出负借阅天数而未拒绝。
- 影响：`tools/library/overdue-fine.html`，封顶语义和日期状态不可靠。
- 方案：明确零元封顶是支持还是非法并对应处理；校验日期先后，不输出正常罚单。

### 专著页码标点与页面示例不一致（中，确认源码冲突）
- 证据：`tools/library/citation-format.html:201-204,358-364` 出版年后拼接 `.100-150.`，同页示例用 `:100-150.`。
- 影响：`tools/library/citation-format.html`，引用复制结果与页面示例不一致；未独立审核全部著录标准。
- 方案：核对所用标准版本并统一示例与生成逻辑，增加页码有无及版本的用例。可加入用户主动维护的本地文献草稿与逐条编辑、批量复制。

### 覆盖与目录冲突
- 本次仅抽查上述 4 页；前三项使用内存 DOM 桩，未验证真实浏览器、专业规范、线上及其余页面。旧范围列 `tools/archive/`，当前目录不存在，须核对分类映射，不应算已覆盖。

## 2026-11-03 续查（并行批 H）

> 编号说明：首轮 4 条结论无编号，保留原文不动；本批新增 `RL-H` 系列，不与其重号。以下结论均为源码阅读 + node 内存复算，未做真实浏览器、英文态、移动端、门禁或线上验证。本批覆盖 8 页：`analysis-50/51/52/54`、`assessor-50`、`tester-17`、`clc-classifier`、`shelf-capacity`。

### RL-H8 定性路径：深度解析整段是「频次描述统计」另一工具模板（中，确认）
- 描述：正文计算编码覆盖率/主题密度/饱和度，但深度解析的场景、算例与 FAQ 讲的是「把各编码类目的出现频次粘进来算均值、中位数、极差、标准差」，与页面输入格式和输出完全不同。
- 证据：`tools/research/analysis-54.html:144-154`（场景与算例，含 `:149` 的「均值 6.25、中位数 5.50、标准差 3.15」），对照 `:199-235` 的实际计算。node 按深度解析示例输入 `12,9,8,6,5,5,3,2` → 条目 1、主题 7 个（`9/8/6/5/5/3/2`）、覆盖率 100%、平均主题 7.00，与文中「样本量 8、总和 50」不符。
- 影响：`tools/research/analysis-54.html`。用户按深度解析操作必然对不上结果，削弱 E-E-A-T。
- 方案：把深度解析改写为本页的编码/覆盖率/饱和度示例；若确需频次描述统计，另建工具页承接，勿混在同一页。

### RL-H20 中图法：R76 标为「眼科学」且 R77 缺失（中，待验证）
- 描述：R 大类中 `R76` 写成「眼科学」，全表无 `R77`，也没有耳鼻咽喉科学。按通行《中国图书馆分类法》分类表，R76 为耳鼻咽喉科学、R77 为眼科学。
- 证据：`tools/library/clc-classifier.html:387-401`（R 子类数据）。node 复算 `search('眼科学')` → 1 条 `R76 眼科学`，`search('R77')` → 0 条。仓库内无权威原表可比对，故列为待验证。
- 影响：`tools/library/clc-classifier.html`。按此表编目会把眼科学书籍错分到耳鼻咽喉类号。
- 方案：对照《中图法》第五版 R 类原表逐条校核，修正 R76 并补 R77；同时补一条类号唯一性/连续性测试。

### 留存优化
- `analysis-50` 的「预设」为空实现（`tools/research/analysis-50.html:409-411`，`analysis-51` 同名区域同样为空），可各补 3 组行业示例；两页解析逻辑近乎同构，建议抽公共解析器，避免同名分隔符缺陷各自复制。
- `analysis-52` / `analysis-54` 建议输出「坏行清单」（行号 + 原文），而不是只给条数，便于研究者修数据。
- `assessor-50` 结果卡建议并列「每触达人次成本」与「CPM(元/千次)」，并在卡片上直接标注单位，避免再次混淆。
- `tester-17` 可增加「四价单调性提示/曲线顺序图」，让倒序输入在提交前即可见；`clc-classifier` 建议提供「复制索书号」而非仅分类号，并在搜索无结果时给出相近类目。
- `shelf-capacity` 建议把单面/双面并排成一表，并输出 80%/85%/90% 三档填充率敏感度，替代单一估算。

### 续查覆盖
- 本批覆盖 8 页：`tools/research/analysis-50.html`、`tools/research/analysis-51.html`、`tools/research/analysis-52.html`、`tools/research/analysis-54.html`、`tools/research/assessor-50.html`、`tools/research/tester-17.html`、`tools/library/clc-classifier.html`、`tools/library/shelf-capacity.html`。
- 首轮已覆盖 4 页（`analysis-49`、`calc-97`、`overdue-fine`、`citation-format`），本批不重复。
- 未覆盖：`tools/library/archive-label.html`、`generator-label.html`、`stats-report.html` 及 `tools/research/index.html`、`tools/library/index.html`；`tools/archive/` 仍不存在，首轮目录疑问保留。
- 方法边界：全部结论基于静态源码 + node 内存复算，未做真实浏览器、英文态、移动端、门禁与线上验证；`RL-H20` 需按专业类表复核后方可定级。

## 2026-11-03 续查（并行批 K）

> 范围：本轮阅读 8 页（`tools/library/archive-label.html`、`tools/library/generator-label.html`、`tools/library/stats-report.html`、`tools/cognition/digit-span-test.html`、`tools/cognition/schulte-table.html`、`tools/cognition/stroop-test.html`、`tools/museum/lighting-lux.html`、`tools/museum/era-comparator.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

### RL-K1 档案盒脊背标签：整页是「随机抽 10 条示例」模板，与标题/简介承诺的字段化排版完全不符（高，确认）
- 描述：页面 h2/description/公式说明/深度解析均承诺「按全宗号、年度、机构、起止件号、盒号生成盒脊标签，字号随 30/40/50mm 盒型自动收缩」；实际全页只有「生成数量」一个输入，`gen()` 只是从内置 10 条 `ARCHIVES` 里洗牌取 n 条渲染，既不读任何表单字段，也没有盒型/字号逻辑。
- 证据：`tools/library/generator-label.html:10`（description）、`:126`（formula-desc）、`:160`（深度解析示例「全宗号 A032…盒号 012」）、`:129`（唯一输入）、`:206-217`（10 条常量池）、`:219-231`（渲染逻辑）。
- 复现：打开页面 → 不填任何字段即显示一条「行政综合 / 2024年度 / 永久 / XZ-2024-001」；按说明想生成「A032 / 2024 / 办公室 / 0001-0150 / 012」→ 无法输入，实际输出与该示例无关。
- 影响：工具无法完成页面宣称的唯一功能，属于模板占位页；用户按深度解析操作必然对不上结果。
- 方案：补齐全宗号/年度/机构/起止件号/盒号/脊厚输入并做竖排排版与字号计算；若暂不做，应删除夸大的 description/深度解析示例，避免 E-E-A-T 损害。

### RL-K2 档案盒脊背标签：数量上限 50 但池仅 10 条，n>10 静默截断（低，确认）
- 描述：输入框 `max=50`、公式框写「n 限幅 1–50，池不足取全部」，实际常量池只有 10 条，填 50 只出 10 条且无任何提示；`pick()` 用 `sort(()=>Math.random()-0.5)` 洗牌，分布有偏。
- 证据：`tools/library/generator-label.html:129`、`:177`、`:206-217`、`:218-221`。
- 复现：生成数量填 50 → 实际 10 条（期望 50 条或明确提示「示例池仅 10 条」）。
- 影响：批量打印/清点数量被悄悄截断，用户会以为已生成 50 枚。
- 方案：扩充示例池至 ≥50 或把上限改为 10 并提示；洗牌改用 Fisher-Yates。

### RL-K5 统计报表：深度解析的场景与算例是「台账明细+类型汇总」另一工具模板（中，确认）
- 描述：深度解析要求「输入台账明细自动汇总总件数、各类型数量与占比、按年度/类型交叉汇总」，算例给出「总件数 1200、文书 800 利用 300、业务 400 利用 60」；页面实际只有馆藏/借阅/读者/到馆/新增 5 个全局数字，无明细录入、无类型维度。
- 证据：`tools/library/stats-report.html:160-165`（场景与算例）对照 `:130-134`（实际输入）、`:218-225`（实际输出）。
- 复现：按深度解析输入「文书类 800 件、利用 300 件次」→ 页面无对应字段，只能算全馆利用率；`360÷1200=30%` 的示例无法复现。
- 影响：示例与实现脱节，用户照做必然对不上。
- 方案：把深度解析改写为本页真实口径（`借阅册次 ÷ 馆藏册数`），或补明细表输入与分组汇总。

### RL-K11 Stroop：一致条件 40 试次（含 24 前置纯块）对不一致 16 试次，干扰量基线受练习/块序污染（中，疑似）
- 描述：一致块 24 次先于混合块 48 次（内部分为一致/不一致/中性各 16），因此 `cong` 汇总 40 次且主要来自前置纯块，`incong` 仅 16 次；`interference = incong.m - cong.m` 把「块序 + 练习效应」混入 Stroop 效应。
- 证据：`tools/cognition/stroop-test.html:327-337`（块结构）、`:409-418`（按条件汇总）、`:431-433`（干扰量差值）。
- 复现：完成一轮默认测试后，一致 n=40、不一致 n=16、中性 n=16；若把一致块也改成混合块内 16 次，干扰量通常会明显变化（当前实现无法分离块序效应）。
- 影响：干扰量/干扰率的可比性与研究用途受影响。
- 方案：三条件在混合块内等量随机化（或明确把纯块作为练习不计分），保证 n 与块序平衡。

### RL-K19 历史朝代对比：「时间跨度相差」实为起始年差；现代中国止年写死 2025（低，确认）
- 描述：`timeDiff=|e1.s-e2.s|` 只比较起始年，却标为「时间跨度相差」；同页另有「持续时长差」。且「现代中国」固定 `e=2025`、`dur=76`，当前 2026 年已过期。
- 证据：`tools/museum/era-comparator.html:303`、`:321-322`、`:271`。
- 复现：夏朝(-2070) vs 清朝(1644) → 显示「时间跨度相差 3714 年」，实际是建立时间相差；持续时长差另显示 202 年（期望文案改为「起始相差」或直接比较时长）。
- 影响：对比文案误导；现代中国时长逐年失真。
- 方案：改名为「起始年相差」，或直接输出两朝时长差；现代中国止年改为动态当前年。

### RL-K20 档案盒标签：批量「每盒件数」与单盒「起止件号」互不校验，首盒区间可越过当前标签（低，确认）
- 描述：单盒标签用 `range` 原样显示，批量的首盒件号却从 `range` 的首个数字起、按 `perBox` 重算，不检查 `perBox` 是否等于/小于 range 跨度，也不检查是否越过 range 末号。
- 证据：`tools/library/archive-label.html:177`（range 默认 `1-50`）、`:214`（每盒件数默认 50）、`:371-386`（`firstFrom + i*per`、`fromNo+per-1`）。
- 复现：把起止件号改成 `1-30`、其余默认（每盒 50、盒数 5）→ 单盒标签显示「件号 1-30」，批量清单首盒却为 `0001 / 01-50`，第二盒 `0002 / 51-100`（期望首盒 1-30，或提示 perBox 与 range 不一致）。
- 影响：同一页面两处件号口径冲突，打印后与实际盒内文件数对不上。
- 方案：以 range 跨度为默认 perBox 并校验 `perBox <= range 结束-开始+1`，超界给警告。

### RL-K21 档案盒标签：盒号前缀在批量中被丢弃；批量参数非法时静默无反馈（低，确认）
- 描述：`boxLen = boxNo.length`、批量盒号用 `pad(from+i, boxLen)` 重新生成纯数字，用户填 `A0001`（长度 5）时批量输出 `00001`，前缀 `A` 丢失，与单盒标签 `A0001` 不一致；`__alBatch` 参数不合法时直接 `return`，界面无任何提示。
- 证据：`tools/library/archive-label.html:372`（静默 return）、`:375`（取长度）、`:382-383`（重新 pad 生成盒号）。
- 复现：盒号填 `A0001`、起始盒号 1、盒数 2 → 批量「00001 / 00002」，而单盒标签为「A0001」（期望保留前缀或明确提示仅支持纯数字盒号）。
- 影响：带前缀/分类码的盒号批量打印后会错号。
- 方案：解析盒号中的数字段与其前后缀，批量时保留前缀；非法参数弹 toast。

- 本轮实读 8 页：`tools/library/archive-label.html`、`tools/library/generator-label.html`、`tools/library/stats-report.html`、`tools/cognition/digit-span-test.html`、`tools/cognition/schulte-table.html`、`tools/cognition/stroop-test.html`、`tools/museum/lighting-lux.html`、`tools/museum/era-comparator.html`；新增 21 条（高 3 / 中 11 / 低 7）。
- 与既有条目无重号、无重复页面：首轮已覆盖 `analysis-49`、`calc-97`、`overdue-fine`、`citation-format`，H 批已覆盖 `analysis-50/51/52/54`、`assessor-50`、`tester-17`、`clc-classifier`、`shelf-capacity`；本批 8 页均为首次阅读。
- 未覆盖：`tools/library/index.html`、`tools/cognition/index.html`、`tools/museum/index.html`、`tools/research/index.html`（分类索引页）；`tools/cognition/cognitive-assessment.html`、`corsi-block-test.html`、`human-benchmark.html`、`nback-training.html`、`time-perception.html`；`tools/museum/audio-guide-timer.html`、`exhibit-spacing.html`、`historical-calendar.html`、`showcase-monitor.html`、`timeline-viewer.html`、`visitor-route.html`；`tools/library/stats-report.html` 的导出/历史面板未单独审查。

## 2026-11-04 续查（并行批 M）

> 范围：本轮阅读 8 页（`tools/cognition/cognitive-assessment.html`、`tools/cognition/corsi-block-test.html`、`tools/cognition/nback-training.html`、`tools/cognition/time-perception.html`、`tools/museum/audio-guide-timer.html`、`tools/museum/exhibit-spacing.html`、`tools/museum/historical-calendar.html`、`tools/museum/showcase-monitor.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。
> 编号说明：文件实际最大编号为 K 批末尾 RL-K21（非提示中的 K16），为避免重号，本轮从 **RL-K22** 起续编。

### RL-K22 综合认知评估：深度解析称「百分制/非标准常模」，实现却是年龄常模标准分（中，确认）
- 描述：深度解析与 FAQ 两处写「各域 82/74/88/79 为相对百分制」「分数仅站内自评、非标准化常模换算」，但同页公式框与代码使用四层年龄常模、`SS=100+15Z`、`PR=Φ(Z)`，报告直接输出标准分（可低于 40 或高于 160），并非 0–100 百分制。
- 证据：`tools/cognition/cognitive-assessment.html:179-180`（公式）、`:299`、`:302`（文案）；`js/tools/cognitive-assessment.js:831`（综合分取各指标 SS 均值）。
- 复现：选 30–49 岁、仅测简单反应时，原始 300 ms → 页面显示 SS≈94.5、PR≈35.6；若原始 250 ms → SS≈114（期望文案按 SS 常模解释，而不是「百分制 94 分」）。
- 影响：同一分数被两种口径解释；用户会把 SS 94 当作「94 分及格」，与 PR 35.6 的实际常模位置相差一倍。
- 方案：全页统一为「标准分 SS（M=100，SD=15，基于年龄常模）+ 百分位 PR」；删除「百分制/非标准化常模」表述，示例改列 SS 与 PR 双值。

### RL-K23 综合认知评估：仅测单项时仍称「综合标准分」，强弱项重复同一项（低，确认）
- 描述：`comp` 对全部已测指标 SS 取均值；仅测 1 项时仍输出「综合标准分/综合百分位」，强弱项用 `slice(0,2)` 与 `slice(-2)` 在同一项上重复展示。
- 证据：`js/tools/cognitive-assessment.js:831`、`:891-897`；`tools/cognition/cognitive-assessment.html:202-211`（仅测选项）。
- 复现：仅测「简单反应时」得 SS 94.5 → 报告「综合标准分 94」，同时「强项：简单反应时」「相对弱项：简单反应时」（期望单项模式显示「单项标准分」且不展示强弱项）。
- 影响：单项结果被包装成综合能力，强弱项自相矛盾。
- 方案：单项模式改标题为「单项标准分」并隐藏强弱项；强弱项先去重，且指标数 <3 时不展示。

### RL-K35 历史日历：节气用固定月-日表，2024 冬至等年份错位/漏标（中，确认）
- 描述：`TERM_DATES` 是固定「月-日」表（如冬至 12-22），不随年份变化；节气实际每年漂移 1–2 天。
- 证据：`tools/museum/historical-calendar.html:300`、`:379-393`。
- 复现：选 2024-12-21（2024 年冬至，北京时间 12-21）→ 节气行缺失（期望「冬至」）；选 2024-12-22 → 显示「冬至」（错误）。另 2024 处暑为 08-22，表给 08-23。
- 影响：节气标注在多数年份错位或漏标，历史日期解读失真。
- 方案：内置 1900–2100 逐年节气表，或用太阳黄经近似公式按年份计算。

- 本轮实读 8 页：`tools/cognition/cognitive-assessment.html`、`tools/cognition/corsi-block-test.html`、`tools/cognition/nback-training.html`、`tools/cognition/time-perception.html`、`tools/museum/audio-guide-timer.html`、`tools/museum/exhibit-spacing.html`、`tools/museum/historical-calendar.html`、`tools/museum/showcase-monitor.html`；新增 18 条（高 4 / 中 10 / 低 4）。
- 与既有条目无重复页面：research 非索引页（`analysis-49/50/51/52/54`、`assessor-50`、`calc-97`、`tester-17`）与 library 非索引页（`archive-label`、`citation-format`、`clc-classifier`、`generator-label`、`overdue-fine`、`shelf-capacity`、`stats-report`）已由前序批次全覆盖，本轮无剩余可读页，故转向 cognition/museum 未覆盖页。
- 未覆盖：`tools/research/index.html`、`tools/library/index.html`、`tools/cognition/index.html`、`tools/museum/index.html`（分类索引页，无工具逻辑）；`tools/cognition/human-benchmark.html`；`tools/museum/timeline-viewer.html`、`tools/museum/visitor-route.html`。

## 2026-11-04 续查（并行批 N）

> 范围：本轮阅读 7 页（`tools/cognition/human-benchmark.html`、`tools/museum/visitor-route.html`、`tools/museum/timeline-viewer.html`、`tools/research/index.html`、`tools/library/index.html`、`tools/cognition/index.html`、`tools/museum/index.html`）。**说明：四目录仅剩这 7 个未覆盖页（3 个工具页 + 4 个索引页），不足以凑满 8 页；未跨目录外扩，以免与 edu-language 批重复。** 仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

### RL-K43 Human Benchmark：只做 1 项也生成完整报告，未测维度按 P0 计入综合指数（中，确认）
- 描述：`computeAbilities()` 对未测能力返回 0；报告照常显示四维 P 值与「0–100 综合脑力指数」，`computeIndex()` 仍按 0.30/0.25/0.25/0.20 全权重求和，未测项被当作「0 百分位」。
- 证据：`tools/cognition/human-benchmark.html:854-880`、`:936-953`、`:330`。
- 复现：只完成反应速度 250ms（P69）→ 报告「记忆 P0 / 注意 P0 / 加工速度 P69 / 执行 P0」，指数 17、「击败了约 17% 的人」（期望隐藏未测维度，或按已测权重归一化，指数应≈69）。
- 影响：单项用户得到严重低估且自相矛盾的报告。
- 方案：报告中未测维度显示「未测」并排除出雷达；综合指数按已测能力权重重新归一；仅 8 项齐全时提示完整指数。

### RL-K47 参观流线：改名展厅后通道下拉无匹配项，显示错位且计算静默丢弃通道（中，确认）
- 描述：`renderEdges()` 仅对 `e[0]===n` 加 `selected`；旧端点不存在时浏览器默认选第一项，但 `edges` 数据仍保留旧名；`compute()` 对不在 `nodes` 的端点直接跳过，无提示。
- 证据：`tools/museum/visitor-route.html:274-275`、`:354-360`、`:245-255`。
- 复现：把展厅列表的「出口」改为「东门」→ 原来「玉器馆—出口」行第二个下拉显示「入口」，但内部仍是「出口」；规划显示「没有可达路径」。期望自动同步/标红失效通道并提示。
- 影响：界面显示与实际图数据不一致，用户误删或漏连通道。
- 方案：节点变更时按索引/映射迁移端点，映射不到的边标红并要求确认删除；不要依赖 `<select>` 默认项。

### RL-K48 历史时间轴：无任何筛选/搜索控件，深度解析却称「支持中西对照筛选」且算例事件不在数据中（中，确认）
- 描述：页面只有 4 个主题按钮，无 `input/select`；`renderTimeline()` 仅按主题整表渲染。深度解析称可按「公元前 3 世纪 / 15 世纪 / 19 世纪」筛选，并称有 1405 郑和、1861 洋务、1894 甲午，但数据中均不存在。
- 证据：`tools/museum/timeline-viewer.html:206-207`、`:362-376`、`:344-360`；数据仅到 `:273`（1840）与 `:287`（1453），无 1405/1861/1894。
- 复现：找筛选入口 → 无；选「中国历史」→ 看不到 1405/1861/1894。期望实现世纪/关键词筛选，或删掉「筛选」表述并改写算例。
- 影响：深度解析示例无法复现，工具核心「查找」承诺落空。
- 方案：增加年份区间/关键词输入并过滤 `TIMELINES[currentTheme]`；补齐或改写示例事件。

### RL-K49 历史时间轴：固定 24px 间距与「比例 = 像素宽度 ÷ 总跨度」公式不符（中，确认）
- 描述：每条 `.tl-item` 固定 `margin-bottom:24px`，圆点绝对定位 `left:75px`，与年份数值无关；公式表却声称时间轴按像素/跨度比例缩放。
- 证据：`tools/museum/timeline-viewer.html:34-36`、`:230-231`、`:163`；渲染见 `:362-376`。
- 复现：同类目下前 221 与前 202 的垂直间距，与 1840 与 1911 完全相同（均 24px）；期望按年份差缩放，或删掉比例公式。
- 影响：时间轴视觉误导「等距即等时」，与公式自相矛盾。
- 方案：按 `(y-minY)/(maxY-minY)` 计算位置/高度；若坚持列表式，删除比例行并注明「等距排列」。

### RL-K50 历史时间轴：遗留中医模板「辨证记录历史」与 `tcm-history.csv`（中，确认）
- 描述：历史记录面板文案、英文 `Diagnosis Records`、localStorage 键 `__tbm_tcm_timeline`、导出文件名均沿用中医模板。
- 证据：`tools/museum/timeline-viewer.html:467-469`、`:481-487`。
- 复现：切换两次主题 → 页面出现「辨证记录历史 / 序号 / 条目 / 查看次数」，点导出得到 `tcm-history.csv`。期望「浏览记录 / 主题 / 浏览次数 / timeline-history.csv」。
- 影响：明显串味，削弱专业可信度；英文态同样错误。
- 方案：替换 `T` 字典、KEY 与文件名（含新 KEY 迁移或直接重置）。

### RL-K51 科研索引页：三张卡片承诺未实现的功能（KMO/Bartlett、三角验证、主持人提纲）（中，确认）
- 描述：索引卡与工具页 title/meta 均超出实现——analysis-49 只算 Cronbach α，无 KMO/Bartlett 输出；analysis-54 FAQ 明确「不能三角验证」；analysis-52 FAQ 明确「不能质性编码/主题提炼」，卡片却写「主持人提纲与编码归类」。
- 证据：`tools/research/index.html:88-89`、`:93`；`tools/research/analysis-49.html:217-252`（仅 α）；`tools/research/analysis-54.html:152`；`tools/research/analysis-52.html:166`。
- 复现：从索引点 analysis-49，输入任意矩阵 → 结果只有被试数/条目数/α/判读，无 KMO、Bartlett χ²、p（期望卡片承诺的四项）；analysis-54/52 同理无三角验证/提纲。
- 影响：搜索摘要与首屏承诺落空，用户按缺失功能评估工具。
- 方案：补实现 KMO/Bartlett（相关矩阵求逆+行列式）；或把卡片与 title/meta 改为「Cronbach α 信度分析」等真实能力。

### RL-K52 Human Benchmark：反应时用算术均值，深度解析却称「去掉极端后中位值」（低，确认）
- 描述：`finish()` 对 5 次全部取平均；深度解析称「取多次中位值」「去掉极端后中位约 251ms」。
- 证据：`tools/cognition/human-benchmark.html:392-398`、`:1152`、`:1156`。
- 复现：5 次 268/251/243/259/247 → 页面「平均 254 ms」；深度解析示例写 251ms（期望同一统计口径，或页面改用中位值）。
- 影响：说明与实现不一致，用户对成绩口径产生疑问。
- 方案：二选一——改代码为中位值（并说明不去极值），或把深度解析改为「5 次算术平均 254ms」。

### RL-K53 参观流线：历史快照只存有 id 的控件，通道距离/端点无法回放（低，确认）
- 描述：`__visitor_routeSnap()` 只采集带 `id` 的 `input/select/textarea`；通道行只有 `data-i/data-k` 没有 `id`，因此历史记录不含任何边数据；回放只恢复展厅、起终点。
- 证据：`tools/museum/visitor-route.html:508`、`:543-554`；边控件 `:276-279`。
- 复现：把某通道改为 100m 并规划（记录）；再改为 20m 后点历史记录回放 → 展厅/起终点恢复，但通道仍是 20m，总距离与当初记录不同。期望快照包含通道端点与权值并整体恢复。
- 影响：历史「回放/对比」失真，记录无法复现。
- 方案：给边控件加 `id`（如 `edge-<i>-0/1/2`），或快照序列化 `edges` 数组并在回放时重建。

### RL-K54 参观流线：公式框的「通行时间/拥挤度」与「必看节点」均未实现（低，确认）
- 描述：公式表列出 `T = L/v + Σ停留` 与拥挤度 `人数/通行能力`，页面只算距离；深度解析称「设定起终点与必看节点」，实际无必经节点输入。
- 证据：`tools/museum/visitor-route.html:208`、`:212-213`、`:183`、`:189`。
- 复现：页面仅有距离输入与起终点下拉，无速度/停留/人数/容量/必经节点控件（期望按公式给出时长与拥挤度，或删除公式行）。
- 影响：公式与标准引据区展示未实现能力，误导专业用户。
- 方案：删除未实现公式，或补「步行速度+停留时间」输入输出 T；必经节点可后续实现多点分段。

### RL-K55 参观流线：SEO 介绍区残留「商业办公/批量操作/团队协作」模板（低，确认）
- 描述：工具简介写「免费在线博物馆工具。。商业办公工具」，功能写「支持批量操作」，场景写「日常办公文档处理/会议与项目管理/团队协作」，与本工具无关。
- 证据：`tools/museum/visitor-route.html:475`、`:478-489`。
- 复现：展开「关于参观流线规划」→ 可见上述文案（期望展馆导览、限流、动线优化场景）。
- 影响：首屏下方内容明显跑题，影响 E-E-A-T。
- 方案：改写为博物馆动线场景，删除「批量操作」等模板项与重复句号。

### RL-K57 四个分类索引页：meta 均称覆盖「单位转换」，目录内并无换算类工具（低，确认）
- 描述：research/library/cognition/museum 四个 `index.html` 的 description/og/twitter 使用同一套模板句「常见计算、换算、单位转换与查询需求」，但四目录工具均为统计、档案、测评、展陈类，无单位换算器。
- 证据：`tools/research/index.html:6`、`tools/library/index.html:6`、`tools/cognition/index.html:6`、`tools/museum/index.html:6`（`:11`/`:21` 同样）。
- 复现：浏览四页工具卡 → 无任何单位转换工具（期望删去「单位转换」或按类目定制摘要）。
- 影响：搜索摘要与页面内容不符，易致高跳出；四页摘要高度同质。
- 方案：构建模板按行业生成差异化描述，移除未覆盖的能力词。

### RL-K58 文博索引页：时代对比/历史日历/时间轴三张卡片共用同一段「查询历史文化知识」套话（低，确认）
- 描述：三张卡描述几乎逐字相同，未说明各自独有能力（朝代重叠/节气农历/主题时间轴），与同页其他卡（照度、导览、间距）的信息密度明显不一致。
- 证据：`tools/museum/index.html:88`、`:90`、`:93`。
- 复现：对比三卡文案 → 除工具名外一致，均无具体功能与输入输出说明（期望分别写明「朝代区间重叠/人口对比」「农历节气/干支」「按主题浏览/按年份排序/CSV 导出」）。
- 影响：类目页无法帮助用户选择工具，SEO 内容重复。
- 方案：按各工具实际能力重写三张卡描述。

- 本轮实读 7 页：`tools/cognition/human-benchmark.html`、`tools/museum/visitor-route.html`、`tools/museum/timeline-viewer.html`、`tools/research/index.html`、`tools/library/index.html`、`tools/cognition/index.html`、`tools/museum/index.html`；新增 19 条（高 2 / 中 10 / 低 7）。
- 重复说明：本批无重读页面；RL-K51 是索引页文案问题（analysis-49/52/54 页面本身由前序批次覆盖，但该三处「卡片承诺未实现」此前未记录），RL-K57 为四个索引页共有模板问题。
- 四目录 35 个 HTML（31 个工具页 + 4 个索引页）至此全部覆盖；未覆盖：无。**本批范围内只剩上述 7 个未覆盖页，无法凑满 8 页，特此说明。**
