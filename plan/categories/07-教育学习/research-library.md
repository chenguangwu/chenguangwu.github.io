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

- 本轮实读 8 页：`tools/library/archive-label.html`、`tools/library/generator-label.html`、`tools/library/stats-report.html`、`tools/cognition/digit-span-test.html`、`tools/cognition/schulte-table.html`、`tools/cognition/stroop-test.html`、`tools/museum/lighting-lux.html`、`tools/museum/era-comparator.html`；新增 21 条（高 3 / 中 11 / 低 7）。
- 与既有条目无重号、无重复页面：首轮已覆盖 `analysis-49`、`calc-97`、`overdue-fine`、`citation-format`，H 批已覆盖 `analysis-50/51/52/54`、`assessor-50`、`tester-17`、`clc-classifier`、`shelf-capacity`；本批 8 页均为首次阅读。
- 未覆盖：`tools/library/index.html`、`tools/cognition/index.html`、`tools/museum/index.html`、`tools/research/index.html`（分类索引页）；`tools/cognition/cognitive-assessment.html`、`corsi-block-test.html`、`human-benchmark.html`、`nback-training.html`、`time-perception.html`；`tools/museum/audio-guide-timer.html`、`exhibit-spacing.html`、`historical-calendar.html`、`showcase-monitor.html`、`timeline-viewer.html`、`visitor-route.html`；`tools/library/stats-report.html` 的导出/历史面板未单独审查。

## 2026-11-04 续查（并行批 M）

> 范围：本轮阅读 8 页（`tools/cognition/cognitive-assessment.html`、`tools/cognition/corsi-block-test.html`、`tools/cognition/nback-training.html`、`tools/cognition/time-perception.html`、`tools/museum/audio-guide-timer.html`、`tools/museum/exhibit-spacing.html`、`tools/museum/historical-calendar.html`、`tools/museum/showcase-monitor.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。
> 编号说明：文件实际最大编号为 K 批末尾 RL-K21（非提示中的 K16），为避免重号，本轮从 **RL-K22** 起续编。

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
