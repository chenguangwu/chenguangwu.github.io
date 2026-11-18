# 教育/语言 · tools/{edu,edu2,language,chinese}（~60 页）

## 已知问题
## 功能缺陷
- 中文页（chinese-culture/lunar）静态，缺「生辰八字/节气」交互深挖。

## 优化点
- S4 分享卡：倒计时打卡卡。

## 受影响范围
- tools/edu/（47）、tools/edu2/、tools/language/、tools/chinese/

## 进度
- 🟡 续批中（剩余：生辰八字节气深挖 / S4 打卡分享卡）

## 2026-11-03 审计补充

### 留存优化：根据错误题型练习（低，建议）
- 证据：同页 `:330-338,348-368` 随机抽题并累计对错，但给出的统计仅为次数与正确率。
- 影响：同页；方案：在本地维护本次会话的易错乘数对，提供「再练错题」和家长可复制的练习摘要，不记录个人身份。

### 留存建议（低，建议）
- `tools/edu/flashcards.html:1307-1327,1379-1398` 已支持认识/不认识和复习错词；可在此基础上增加用户可选本地复习间隔与一键开始今日复习，避免重复建设。

### 覆盖
- 本轮共核查 7 页：原 `tools/edu/multiplication-table.html`，以及 `tools/edu/reading-speed-calculator.html`、`tools/edu/flashcards.html`、`tools/edu2/wrong-book.html`、`tools/language/french-verb-conjugator.html`、`tools/language/korean-hangul-decomposer.html`、`tools/chinese/chinese-radical-lookup.html`。本次新增 5 个问题、4 项建议；真实浏览器、移动端、线上和其他页面未复核。

## 2026-11-03 续查（并行批 F）

> 方法：逐页读源码 + Node 内存复算（抽取页面内函数/字典求值），未做浏览器、英文态、移动端、门禁或线上验证。编号 `EL-F*` 为本批新增，未与既有 E2 / S2 / S4 重号。

### 留存优化
- `tools/edu/pinyin-converter.html`（低，建议）：把「多音字提示」升级为可点击选择读音的卡片，用户选定后即时重算整句，并把该词加入本地「我的读法」表，避免只提示不解决。
- `tools/edu/ebbinghaus-curve.html`（低，建议）：在修好日期比较后，提供「复制日程 / 导出 .ics」纯前端文本，方便用户带入系统日历；不新增后端与通知权限。
- `tools/language/language-toolkit.html`（低，建议）：五十音练习增加「本次易错假名」本地清单与一键重练，配合可接受答案集合，直接复用现有 `getAllKana` 数据，不重复建设。
- `tools/edu/chinese-stroke-counter.html`（低，建议）：补「最近查询」与收藏字卡（现有 `saveHistory` 已存 20 条，只差展示入口），并在未收录字处提供「反馈缺字」的本地复制文案。

### 续查覆盖
- 本批共核查 8 页：`tools/edu/pinyin-converter.html`、`tools/edu/ebbinghaus-curve.html`、`tools/edu/chinese-zodiac.html`、`tools/edu/chinese-stroke-counter.html`、`tools/language/spanish-accent-rules.html`、`tools/language/german-gender-quiz.html`、`tools/language/ipa-practice.html`、`tools/language/language-toolkit.html`。
- 新增 20 条问题（高 3 条：EL-F1 / EL-F5 / EL-F14；中 13 条；低 4 条）与 4 项留存建议。全部证据来自源码阅读与 Node 内存复算；真实浏览器、英文态、移动端、门禁与线上页面均未验证。

## 2026-11-03 续查（并行批 J）

> 方法：逐页读源码 + Node 内存复算（抽取页面内函数/字典求值、按页面判定逻辑模拟输入），未做浏览器、英文态、移动端、门禁或线上验证。编号 `EL-J*` 为本批新增，未与既有 E2 / S2 / S4 / EL-F* 重号。

### 留存优化
- `tools/edu/pinyin-typing-practice.html`（低，建议）：修好判定后，把本次打错的字符位置写入现有 `typing-history`，提供「只练错字」与本会话正确率趋势，复用现有统计卡，不新增数据源。
- `tools/language/idiom-solitaire.html`（低，建议）：现有 `chain` 与得分已落历史，可增加「本局接龙导出/重练」和拼音模式下的「末字不会读」提示（展示该字拼音与可选接龙），降低提前断局的挫败感。
- `tools/language/vocabulary-builder.html`（低，建议）：修好日期与收藏解耦后，用 `vocab_progress` 的 `unknown/fuzzy` 生成「今日待复习」队列；间隔信息只存本地，不引入后端与通知。
- `tools/chinese/chinese-character.html`（低，建议）：`lookup()` 已写历史，可补「最近查询」入口与同部首字卡；未收录时提供可复制的「反馈缺字」文案，明确当前覆盖的 20 字范围。
- `tools/language/grammar-checker.html`（低，建议）：问题修到可信后，按规则类型分组筛选并支持「复制修改建议 / 导出 CSV」，复用现有结果卡片与 `__grammar_checkerExport`，不重复建设。

### 续查覆盖
- 本批共核查 8 页：`tools/edu/pinyin-typing-practice.html`、`tools/edu/english-vocabulary.html`、`tools/language/vocabulary-builder.html`、`tools/language/idiom-solitaire.html`、`tools/language/grammar-checker.html`、`tools/chinese/chinese-character.html`、`tools/chinese/stroke-order-viewer.html`、`tools/language/phrase-translator.html`。
- 新增 21 条问题（高 6 条：EL-J1 / EL-J10 / EL-J12 / EL-J15 / EL-J16 / EL-J17；中 12 条；低 3 条）与 5 项留存建议。全部证据来自源码阅读与 Node 内存复算；真实浏览器、英文态、移动端、门禁与线上页面均未验证。

## 2026-11-04 续查（并行批 L）

> 范围：本轮阅读 8 页（`tools/language/calc-1.html`、`calc-2.html`、`generator-19.html`、`stats-2.html`、`riyuwushiyintulianxi-dianjifayin.html`、`text-polisher.html`、`translator.html`、`tools/edu/quiz-score-percentage.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

### 续查覆盖
- 本轮实读 8 页：`tools/language/calc-1.html`、`tools/language/calc-2.html`、`tools/language/generator-19.html`、`tools/language/stats-2.html`、`tools/language/riyuwushiyintulianxi-dianjifayin.html`、`tools/language/text-polisher.html`、`tools/language/translator.html`、`tools/edu/quiz-score-percentage.html`。
- 新增 13 条（高 3 条：EL-J23 / EL-J28 / EL-J29；中 6 条：EL-J22 / EL-J24 / EL-J25 / EL-J26 / EL-J30 / EL-J31；低 4 条：EL-J27 / EL-J32 / EL-J33 / EL-J34）。
- 未覆盖：`tools/language/index.html`（目录页）、`tools/edu/` 其余 44 页、`tools/edu2/` 6 页、`tools/chinese/` 6 页；方法边界同前，未做真实浏览器、英文态、移动端、门禁与线上验证。

## 2026-11-04 续查（并行批 O）

本批实读 `tools/edu/` 下 8 页：`grade-calculator.html`、`exam-gpa-calculator.html`、`grade-weight-calculator.html`、`exam-score-calculator.html`、`study-planner.html`、`edu-unit-converter.html`、`word-count-pages.html`、`essay-word-counter.html`；编号接续 EL-J35。

### 留存建议（tools/edu/grade-calculator.html）
① 支持批量粘贴「科目,分数,学分」导入；② 目标倒推与主成绩表联动，补「已达标 / 无论期末考多少都不够」分支；③ 导出 CSV 与打印成绩单。
### 留存建议（tools/edu/exam-gpa-calculator.html）
① 提供百分制 ↔ 4.0/5.0 的 GPA 对照表；② 支持整张成绩单批量粘贴；③ 学期 GPA 对比与目标 GPA 反推。
### 留存建议（tools/edu/grade-weight-calculator.html）
① 多套权重方案并列对比；② 用进度条展示「已得/缺口/剩余需考」；③ 导出 CSV 与打印测算表。
### 留存建议（tools/edu/exam-score-calculator.html）
① 多次考试历史趋势图；② 按题型/知识点记录错题；③ 目标倒推与主成绩联动并提供打印成绩单。
### 留存建议（tools/edu/study-planner.html）
① 一键打印周计划；② 导出 ICS 日历/CSV；③ 本地数据备份与恢复 JSON。
### 留存建议（tools/edu/edu-unit-converter.html）
① 常用单位收藏/自定义单位；② 批量一行一值换算；③ 复制结果时带单位并可设精度。
### 留存建议（tools/edu/word-count-pages.html）
### 覆盖小结（2026-11-04 并行批 O）
- 实读 8 页（清单内 8/8 全覆盖），新增 43 条：高 6 条（EL-J35、EL-J39、EL-J40、EL-J47、EL-J64、EL-J71），中 27 条，低 10 条（EL-J38、EL-J45、EL-J46、EL-J53、EL-J59、EL-J60、EL-J63、EL-J70、EL-J76、EL-J77）。
- 本批高优集中在：成绩目标倒推未归一（EL-J35）、GPA 百分制三套口径（EL-J39）、GPA 控件切换后崩溃（EL-J40）、历史保存忽略每题分值（EL-J47）、页数历史忽略纸张/字号（EL-J64）、单换行段落被算 1 段（EL-J71）。
- 未覆盖：`tools/edu/index.html`（目录页）、`tools/edu/` 本批清单外其余页面、`tools/edu2/`、`tools/chinese/` 与 `tools/language/index.html`；本次为静态源码审计 + `node -e` 内存复算，未做真实浏览器、英文态、繁体态、移动端、门禁与线上验证。

## 2026-11-04 续查（并行批 P）

范围：静态实读 9 页（`tools/edu/` 8 页 + `tools/edu2/` 1 页），完整核对 HTML、内联 JS、deep-dive、FAQ 与 JSON-LD；关键数值缺陷用 `node -e` 内存复刻。只读审计，未改代码、未跑构建、未做 git 写。

### 覆盖小结（2026-11-04 并行批 P）
- 实读 9 页（清单 9/9 全覆盖），新增 35 条：高 9 条（EL-J78、EL-J79、EL-J82、EL-J85、EL-J89、EL-J96、EL-J100、EL-J104、EL-J108），中 22 条，低 4 条（EL-J92、EL-J99、EL-J107、EL-J112）。
- 本批高优集中在：24 点求解器 head 裸文本上屏与解表达式残缺、首都测验"限时"无计时器、证书查询假"编号核验"、时区转换无 DST、考试计时正计时永久停在 00:00:00、数学测验"限时/难度/题量"三项皆无、打字游戏按键数重复累计使 WPM 放大约 10 倍、考试成绩分析逗号粘贴丢 3/4 数据。
- 复算方式：`node -e` 内存复刻 24 点 DFS、正计时逐 tick、打字按键累计、成绩解析/均值/标准差/分段，未依赖页面运行时。
- 未覆盖：`plan/categories/07-教育学习/` 内其余工具页、`tools/edu/index.html` 目录页、`tools/edu2/` 除本页外其余页、`tools/language/` 与 `tools/chinese/`；未做真实浏览器、英文态、繁体态、移动端、门禁、构建与线上验证。

### 留存建议（tools/edu/calc-3.html）
- 首屏只保留 4 个默认科目（或改为 3 个并显式标注），删掉 Boot 的隐式追加，避免权重稀释。
- 分配算法改为"整数分钟 + 最大余数"分配，保证各科合计严格等于总时长、无 60 分钟显示。
- 补"每日/每周"维度或改宣称；清空按钮同时清历史，删除重复公式框。

### 留存建议（tools/edu/color-quiz.html）
- 题面改为"只显示色块"或改问"文字颜色是？"，让答案不能靠读字获得。
- 增加 HEX/RGB 题型并扩充色库（至少覆盖常见 24 色），删除未实现的"限时"宣称。
- 正确项高亮改用数据属性/索引判定（`:315` 现依赖 `textContent.includes` + 长度 ≤3，脆弱）。

### 留存建议（tools/edu/word-memory.html）
- 统计改为四档独立计数，"认识"不再硬编码 0。
- 落地艾宾浩斯队列：`lastReview + 1/3/7/15/30 天`，首页展示"今日待复习"。
- 空词库时同步重置进度条；掌握词退出轮转或只在复习模式出现。

### 留存建议（tools/edu/number-memory.html）
- 成功/失败都写入历史并记录是否通过，"挑战次数/平均"改全量口径。
- 修复空 toast 与日期本地化；`showTime` 前加"准备/倒计时"避免数字闪现。
- 增加"错题回顾"（记录失败的数字串）以支撑宣称的记忆训练闭环。

### 留存建议（tools/edu/timezone-converter.html）
- 校验时/分/秒范围（`:818-820` 目前 25 点会静默进位到次日），下拉标签随 DST 勾选更新。

### 留存建议（tools/edu/country-quiz.html）
- 与 `flag-quiz.html` 明确分工（本页做首都/位置，另页做国旗），消除近重复。

### 留存建议（tools/edu/flag-quiz.html）
- 历史记录同时存题量/用时，CSV 增加这两列，支撑"成绩累计"。

### 留存建议（tools/edu/countdown-5.html）
- 打卡按日期区间校验并支持"今日投入 vs 剩余所需日均"提示，增强备考闭环。

### 承诺 vs 实际（Q 批专项）
- `tools/edu/color-quiz.html:10`「选出名称或 HEX 代码」→ 实际仅 12 个中文色名，无 HEX 题；`:159`「timed quiz」→ 无计时器；`:201`「由 HEX/RGB 反推颜色」→ 未实现。
- `tools/edu/country-quiz.html:10`「国旗、首都或地理位置」「限时作答」→ 仅国旗题、无计时；`:202`「错题库：强化易错项」→ 无错题本。
- `tools/edu/flag-quiz.html:158`「timed multiple-choice quiz」→ 无计时；`:200`「错题库：强化易错」→ 无错题本。
- `tools/edu/word-memory.html:10`、`:283-287`「艾宾浩斯遗忘曲线/1·3·7·15·30 天复习」→ 只写 `lastReview` 不读取，无到期复习队列；`:314`「错词反复练」→ `nextWord` 仅顺序轮转，无错词优先。
- `tools/edu/calc-3.html:10`、`:126`「分配每日或每周学习时长」→ 只有单一"总可用时长（分钟）"，无日/周切换。
- `tools/edu/timezone-converter.html:434`「按各地区夏令时规则取偏移量」→ 勾选后恒用固定 `dstOffset`，不看日期（`:673-676`）；`:442`「可能夏令时」徽标 → 常显（`:796-797`）。
- `tools/edu/countdown-5.html:10`「统计剩余总天数」→ 与 hero 天数差 1（`:267-278` vs `:299`），但"工作日/周末"能力本身已实现，无其他虚标。
- `tools/edu/study-progress.html:161`「预计完成日…按工作日计」→ 实际按日历天（`:310-316`）；`:150`「导出明细 CSV」→ 导出历史快照表（`:545-548`）。
- `tools/edu/number-memory.html` 宣称的"成绩记录/最高长度"已实现，未发现明显虚标；本轮 9 页其余宣称（音标/释义卡片、多词库、学习打卡、进度条）均有对应代码。

### 覆盖
- 实读 9 页（`tools/edu/calc-3.html`、`color-quiz.html`、`word-memory.html`、`timezone-converter.html`、`country-quiz.html`、`number-memory.html`、`flag-quiz.html`、`countdown-5.html`、`tools/edu2/study-progress.html`），9/9 全覆盖。
- 新增 23 条（EL-J113～EL-J135）：高 4 条（EL-J118、EL-J119、EL-J123、EL-J126），中 16 条，低 3 条（EL-J115、EL-J122、EL-J131），另附 9 组留存建议与 1 节"承诺 vs 实际"。
- 未覆盖：`plan/categories/07-教育学习/` 内其余教育页、`tools/edu/index.html` 目录页、`tools/edu2/` 其余页、`tools/language/` 与 `tools/chinese/` 均未在本批审计。
- 验证边界：仅静态读源码 + `node` 内存复刻（countdown 日差/工作日、calc-3 分配与取整、study-progress NaN 与逾期、时区 DST 偏移、数字记忆历史口径）；**未**做真实浏览器、英文态/繁体态、移动端、门禁、构建与线上验证；`i18nText()` 空参的真实 toast 表现待浏览器确认。

### 留存建议（tools/edu/convert-3.html）
- 逐位合法性校验替代 `parseInt` 的宽松解析，非法字符定位到位置并报错。
- 决定单值或批量：若保留批量文案就实现分隔解析与结果表。
- 统一负数与大数口径，修正 FAQ 与"精确无近似"表述。

### 留存建议（tools/edu/convert-2.html）
- 四种格式各自加严格正则 + 范围校验，非法输入一律报错，禁止 NaN 落成 0 或破折号。
- 输出前钳制通道值，保证 HEX/RGB 永远合法。
- 精度口径与实现二选一，缺参单独提示。

### 留存建议（tools/edu2/exam-countdown.html）
- 删除或真正实现"统计周末"，让开关与统计口径一致。
- 进度条改用可解释基准（起始日→考试日），无起始日就不显示。
- 节假日数据按年份维护并标注覆盖范围，缺年份时提示不扣减。

### 承诺 vs 实际（R 批专项）
- `tools/edu/assessor-27.html:120`「最低分维度即知识缺口优先改进项」→ 实际按固定 `<6` 过滤（`:220`），全 ≥6 即宣称无缺口。
- `tools/edu/calc-2.html:128`「T 分数 = 50 + 10Z」→ 结果区无 T 分数（`:351-358`）；`:77`/`:494` 仍是"点击计算或生成"套话。
- `tools/edu/reminder-1.html:10`/`:173`「自动按学科和错误类型归类」→ 只有学科筛选与分布（`:539-543`、`:620-637`），错误类型仅作文本标签。
- `tools/edu/calc-4.html:229`「(85−70×0.4)/0.6=91.7」→ **订正（2026-11-05）**：现 `calc()` 为加权口径 `earned=当前×权重/100`，同输入 70/40/85 → 95.0，示例 91.7 无算式来源；早先「页面口径 25」为旧实现，不适用。`:152` 的"剩余考核项数"仍不参与计算（`:313`）。
- `tools/edu/generator-26.html:120`「房间×100+家具×10+序号 / A1-01」→ 实际 `${room}-A1-${object}`（`:221`），无家具位与序号位。
- `tools/edu/convert-3.html:204`「批量转换：一次处理多个数」→ 仅单值输入（`:124`、`:169`）；`:180`「精确无近似」→ 大数受双精度限制。
- `tools/edu/generator-4.html:117`「Summarize a passage」→ 无文本输入，固定 `sampleText`（`:205`、`:214`）。
- `tools/edu/convert-2.html:214`/`:221`「保留输入精度」→ HSL 全程取整（`:171`），缺参输出 `rgb(—, —, —)`（`:178`）。
- `tools/edu2/exam-countdown.html:247` 注释「2025-2027 主要节假日」→ 仅 2026 年数据（`:248-255`）。
- `tools/edu2/exam-analysis.html` 宣称的批量粘贴（逗号/换行）、满分百分比换算、总体标准差均已实现；仅等级顺序在非默认及格线下与及格率冲突（EL-J163），不属虚标。

### 覆盖
- 实读 10 页（`tools/edu/assessor-27.html`、`calc-2.html`、`reminder-1.html`、`calc-4.html`、`generator-26.html`、`convert-3.html`、`generator-4.html`、`convert-2.html`，`tools/edu2/exam-countdown.html`、`exam-analysis.html`），10/10 全覆盖。
- 新增 30 条（EL-J136～EL-J165）：高 10 条（EL-J137、J139、J142、J145、J147、J151、J154、J157、J158、J160），中 12 条，低 8 条（EL-J141、J144、J150、J152、J153、J156、J159、J165），另附 10 组留存建议与 1 节"承诺 vs 实际"。
- 累计覆盖：07 教育 `tools/edu` 45 页 + `tools/edu2` 6 页共 51 页；本文件已覆盖 48 页，仍余 3 页（`tools/edu/convert-area-volume.html`、`tools/edu2/index.html`、`tools/edu2/schedule-conflict.html`），`plan/categories/07-教育学习/research-library.md` 负责的另一批不计入。
- 路径校正：上一批写的 `tools/edu/exam-analysis.html`、`tools/edu/study-progress.html` 实际不存在，真实地址为 `tools/edu2/exam-analysis.html`、`tools/edu2/study-progress.html`；本批按真实 URL 审计。
- 验证边界：仅静态读源码 + `node` 复刻（成熟度均分/缺口阈值、Z 与 CDF、错题 stage 边界、目标倒推与越界、位置编码、`parseInt` 截断、颜色 HEX/RGB 越界、倒计时进度与复选框、等级/及格率冲突、并列排名）；**未**做真实浏览器、移动端、英文态/繁体态、门禁、构建与线上验证。

### 承诺 vs 实际（S 批专项）
- `tools/edu/countdown-5.html:316-321`「累计时长 = Σ记录；学习天数 = 记录条数」→ 已实现，复核通过。
- `tools/edu2/schedule-conflict.html:227-230`「载入示例」→ 示例 8 门课冲突数为 0（教师 0/教室 0），无法演示冲突检测。

### 覆盖
- 实读 3 页：`tools/edu/convert-area-volume.html`、`tools/edu2/schedule-conflict.html`、`tools/edu/countdown-5.html`，3/3 全覆盖。
- 新增 6 条（EL-J166～EL-J171）：高 2（EL-J166、EL-J169），中 3（EL-J167、EL-J170、EL-J171），低 1（EL-J168），另附 3 组留存建议与 1 节“承诺 vs 实际（S 批专项）”。
- 07 教育/edu2 已无未提及页：`tools/edu` 45 个工具页 + `tools/edu2` 5 个工具页均已在 `edu-language.md` 或 `research-library.md` 覆盖；`tools/edu/index.html`、`tools/edu2/index.html` 为分类目录页（无 `<meta name="toolbox">`、无工具交互），不计入工具页审计。
- 验证边界：仅静态读源码 + `node -e` 复刻（`for…in undefined`、温度空选项恒等、`parseFloat('结果 = …')`、倒计时 hero 与 countDays 差值、示例冲突对数、半开/闭区间判定）；未做真实浏览器、移动端、英文态/繁体态、门禁、构建与线上验证；`showToast(undefined)` 的最终显示形态待浏览器确认。
