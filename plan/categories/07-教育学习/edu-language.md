# 教育/语言 · tools/{edu,edu2,language,chinese}（~60 页）

## 已知问题
### E2. 遗留：GPA 页「加权平均权重和≠1」未系统扫（列入：输入学分权重后校验 Σw 提示）。
- 受影响：tools/edu/gpa-calculator.html、grade-weight-calculator 等

## 功能缺陷
- 中文页（chinese-culture/lunar）静态，缺「生辰八字/节气」交互深挖。

## 优化点
- S4 分享卡：倒计时打卡卡。

## 受影响范围
- tools/edu/（47）、tools/edu2/、tools/language/、tools/chinese/

## 进度
- 🟡 续批中（剩余：生辰八字节气深挖 / S4 打卡分享卡）

## 2026-11-06 语言工具静态复核

### 润色输入修改后仍可复制旧输出（中，代码确认）
- `tools/language/text-polisher.html:153,174-176,287-294,361-362,422` 输入事件只更新统计，不清除或标记之前的润色结果，复制按钮直接取旧输出。输入改动后立即复制会拿到前一次结果；应标记过期或清空并提示重新润色。未运行页面。
- 历史关于同义词完全未实现的描述已过时：`:429-459` 已提供选词推荐和替换首次出现的按钮；仍需运行回归，不能正式销账。另阅读短语搜索、分类与语音路径，未验证音频播放。

## 2026-11-03 审计补充

### 空答案提交残留上一题反馈（低，确认缺陷）
- 问题：答错后清空输入再提交，仍显示上次错误及正确答案。
- 证据：`tools/edu/multiplication-table.html:192-195,341-358`：空值 `parseInt` 为 NaN 后直接返回，`pFeedback` 不清；错误分支写入答案。浏览器未实测。
- 影响：`tools/edu/multiplication-table.html`；练习反馈与当前输入状态不一致。
- 方案：空值时清除旧反馈并提示填写，增加错误→清空→提交的交互测试。

### 留存优化：根据错误题型练习（低，建议）
- 证据：同页 `:330-338,348-368` 随机抽题并累计对错，但给出的统计仅为次数与正确率。
- 影响：同页；方案：在本地维护本次会话的易错乘数对，提供「再练错题」和家长可复制的练习摘要，不记录个人身份。

### 阅读估算清空后保留旧结果（中，确认函数缺陷）
- 证据：`tools/edu/reading-speed-calculator.html:389-397` 仅在两个输入均正数时写结果，无效分支不清空；原函数内存执行速度 500、字数 10000 得 20 分钟，清空速度后仍显示旧值。
- 影响：`tools/edu/reading-speed-calculator.html`；方案：无效时清除估算并提示。

### 当日错题不计入到期统计（中，确认函数缺陷）
- 证据：`tools/edu2/wrong-book.html:342-360,389-403` UTC 日期与本地午夜比较；Node 模拟上海时区，2026-11-03 到期的未掌握题显示“今日复习”，统计却为 0。
- 影响：`tools/edu2/wrong-book.html`，提醒漏计；方案：统一本地日历日期比较并测试不同时区和夏令时。可加今日及逾期筛选和一键重练，支持用户主动导出可恢复的本地备份。

### 法语变位生成错误及内置词无时态（高，确认函数缺陷）
- 证据：`tools/language/french-verb-conjugator.html:539-555,574-620,628-650` 规则复合过去时将原词直接拼 é/i 而无助动词，parler 输出 parleré；manger 数据仅含词干、分词等而没有时态数组，时态按钮被禁用。
- 影响：`tools/language/french-verb-conjugator.html`，误导学习；方案：按正确助动词和过去分词构造，补内置词时态或明示不支持，规则和特殊词均加回归。准确后可对当前词与时态做遮答案自测、本地错项重练。

### 韩语终声名称及罗马字错误（高，确认函数缺陷）
- 证据：`tools/language/korean-hangul-decomposer.html:289-298,305-335,346-378` 终声 8 的 ᆯ 却对应 디귿；原函数 `갈` 显示该错名，`각` 转写还混入斜杠和韩文终声字符。
- 影响：`tools/language/korean-hangul-decomposer.html`；方案：逐项校对 Unicode 索引并区分音值提示与规范罗马字，注明跨音节音变限制。

### 部首字表基本资料错误（高，确认源码缺陷）
- 证据：`tools/chinese/chinese-radical-lookup.html:213-234,250-254` 数据把“你”的总笔画设为 2（实际 7），把“听”部首设为讠（实际口）。
- 影响：`tools/chinese/chinese-radical-lookup.html`；方案：据可靠字表核对每条部首、名称和总笔画并标注版本，增加数据回归。核实后可提供本地最近查询和已收录的同部首练习，明确覆盖范围。

### 留存建议（低，建议）
- `tools/edu/flashcards.html:1307-1327,1379-1398` 已支持认识/不认识和复习错词；可在此基础上增加用户可选本地复习间隔与一键开始今日复习，避免重复建设。

### 覆盖
- 本轮共核查 7 页：原 `tools/edu/multiplication-table.html`，以及 `tools/edu/reading-speed-calculator.html`、`tools/edu/flashcards.html`、`tools/edu2/wrong-book.html`、`tools/language/french-verb-conjugator.html`、`tools/language/korean-hangul-decomposer.html`、`tools/chinese/chinese-radical-lookup.html`。本次新增 5 个问题、4 项建议；真实浏览器、移动端、线上和其他页面未复核。

## 2026-11-03 续查（并行批 F）

> 方法：逐页读源码 + Node 内存复算（抽取页面内函数/字典求值），未做浏览器、英文态、移动端、门禁或线上验证。编号 `EL-F*` 为本批新增，未与既有 E2 / S2 / S4 重号。

### EL-F1 拼音字典重复键静默覆盖，多音字整词读错（高，确认缺陷）
- 问题：`pinyinData` 以重复对象键逐个录入，JS 对象字面量后者覆盖前者且无提示，同一字的最终读音由「最后一次出现」决定，与词语语境无关。
- 证据：`tools/edu/pinyin-converter.html:326-412`（字典）、`:559-581`（转换循环）。源码共 765 条键值、实际对象只剩 543 个键；冲突字 `了→le/liǎo`、`发→fā/fà/fā`、`行→xíng/háng/xíng`、`子→zǐ/zi×…`、`白→bái/bai`、`乐→yuè/lè`。内存复算（带声调模式）：`好了 → hǎo liǎo`、`头发 → tóu fā`、`银行 → yín xíng`、`音乐 → yīn lè`、`白发 → bai fā`。
- 影响：`tools/edu/pinyin-converter.html`；核心「汉字转拼音」对最常用多音字给出错误读音，注音教学场景直接误导。
- 方案：改用「单字默认音 + 词语级多音词表（如 银行/音乐/头发/好了 整词匹配）」的分层结构，禁止重复键；为每条多音词建立回归用例（内存求值即可），并在 UI 标注「按词消歧」。落地前先用脚本扫描全字典重复键，逐条人工定音。

### EL-F2 拼音字典缺常用字，整句出现「不转换」的汉字（中，确认缺陷）
- 问题：字表只覆盖 543 字且遗漏大量高频字，未收录字符原样保留，与同句已转换的拼音混排。
- 证据：`tools/edu/pinyin-converter.html:326-412`、`:575-577`（未命中分支直接回填汉字）。抽 50 个常用字，缺失 `男女空车觉立飞父母儿女` 共 12 个；复算 `子女 → zi 女`、`空中 → 空 zhōng`。另 `空` 仅存在于 `:520-523` 的多音字表，未进主字典。
- 影响：`tools/edu/pinyin-converter.html`；页面宣称「汉字转拼音」，实际覆盖率显式显示但用户仍拿到半中半拼的结果。
- 方案：以《通用规范汉字表》一级字（约 3500 字）为下限补字典，缺字时输出可辨识占位（如 `?`）并在结果区提示覆盖率；把「常用 500 字全覆盖」做成用例断言。

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
### EL-J67 字数页数换算：双倍行距每页字数三处口径不一致，英文论文 6000 词少算 5–8 页（中，确认缺陷）
- 问题：格式表/代码用 350 字/页；公式引据又写「双倍行距约 500 汉字/页」和「英文双倍 250–280 词/页」。同一「双倍行距」在页面内有三套数值，「双倍行距（英文论文）」选项仍按 350 计。
- 证据：`tools/edu/word-count-pages.html:364`（`double:350`）、`:250`（参考表「双倍行距约350字」）、`:303-304`（公式引据 500 汉字 / 250–280 词）。
- 复现：手动输入 6000 词、排版选「双倍行距（英文论文）」、图表 25% → `effectiveW=7500`，按 350 得 `ceil(7500/350)=22 页`；按 APA/MLA 250–280 词应为 27–30 页；中文按 500 汉字则为 15 页。三种口径差 7–15 页。
- 影响：`tools/edu/word-count-pages.html`；英文论文页数系统性偏少，直接影响投稿篇幅判断。
- 方案：拆分「中文汉字/页」与「英文词/页」两套系数，英文预设使用 250–280；参考表、公式引据、代码三处同步；或明示 350 为「中文双倍行距」专用。
- 留存建议：同上。

### EL-J70 字数页数换算：32 开系数 0.48 与面积比 0.38 偏差约 25%，5000 字少算 3 页（低，确认缺陷）
- 问题：`paperFactor['32k']=0.48`，但 32 开纸面积约 23920 mm²、A4 约 62370 mm²，面积比约 0.384；按面积口径每页字数应更少、页数更多。
- 证据：`tools/edu/word-count-pages.html:368`（`'32k':0.48`）、`:389`（直接相乘）。
- 复现：5000 字/标准文档/小四/32 开 → 每页 432 字，`ceil(5000/432)=12 页`；按面积比 0.384 每页约 346 字，`ceil(5000/346)=15 页`（差 3 页）。
- 影响：`tools/edu/word-count-pages.html`；小纸张页数被低估，打印/装订估算偏差。
- 方案：按实际纸张面积比校准（B5≈0.71、16开≈0.77、32开≈0.38），或至少把 32 开改为 0.38 并在参考表注明近似。
- 留存建议：同上。

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

### EL-J121 「数字记忆」训练记录只在答错时写入，"挑战次数"实为失败次数、平均可高于最高记录（中，确认缺陷）
- 问题：`submitAnswer` 的成功分支只更新 `bestRecord`，不写 `history`；失败分支才 `unshift({level})`。因此"挑战次数"=失败次数，"最近10次平均"=失败层级均值，且失败层级可高于 `bestRecord`，出现"平均 5.0 > 最高 4"的矛盾。
- 证据：`tools/edu/number-memory.html:393-404`（成功仅更新 best）、`:405-415`（失败才写 history）、`:435`（`avg = history.slice(0,10)...`）、`:442-443`（标签"挑战次数"）。
- 复现：答对 3 位、4 位（best=4）→ 挑战 5 位失败 → `history=[{level:5}]`；页面显示"挑战次数 1（实际 2 次）""最近10次平均 5.0""最高记录 4"。
- 影响：`tools/edu/number-memory.html`；训练量与成绩曲线系统性偏低/偏高，无法用于进步追踪。
- 方案：成功也写入 `{level, passed:true}`，失败写 `{level, passed:false, correct}`；"挑战次数"取全部记录，"平均"按通过的最高位数或分通过/失败两列。

### EL-J122 「数字记忆」清空记录 toast 无文案参数，记录时间硬编码中文区域（低，确认缺陷）
- 问题：`clearHistory()` 调 `ToolBox.showToast(i18nText())` 未传 key，提示为空/`undefined`；`history` 的日期用 `toLocaleString('zh-CN')`，英文态仍输出中文格式。
- 证据：`tools/edu/number-memory.html:469`（空参 `i18nText()`）、`:412`（`toLocaleString('zh-CN')`）。
- 复现：点"清空记录" → 出现空白 toast（真实文案待浏览器确认）；切 `?lang=en-US` 后记录时间仍为"2026/11/4 下午3:20:00"式中文。
- 影响：`tools/edu/number-memory.html`；交互反馈缺失，英文态残留中文日期。
- 方案：传真实 toast key；日期改用 `toLocaleString(undefined)` 或按当前语言选择 locale。

### 留存建议（tools/edu/number-memory.html）
- 成功/失败都写入历史并记录是否通过，"挑战次数/平均"改全量口径。
- 修复空 toast 与日期本地化；`showTime` 前加"准备/倒计时"避免数字闪现。
- 增加"错题回顾"（记录失败的数字串）以支撑宣称的记忆训练闭环。

### EL-J123 「时区转换」勾选"考虑夏令时"后恒用 `dstOffset`，不看日期，1 月纽约被按 EDT 计算（高，确认缺陷）
- 问题：`getOffset(tz,useDST)` 只要 `useDST` 为真且该城有 `dstOffset` 就直接返回夏令时偏移；`dstMonths` 与 `isLikelyDST()` 定义了却从未被调用。结果 1 月转换纽约也按 UTC−4，产生 1 小时错误。
- 证据：`tools/edu/timezone-converter.html:673-676`（`if(useDST && dstOffset!==null) return dstOffset`）、`:666-671`（`isLikelyDST` 定义后全文无调用）、`:832-833`（`doConvert` 直接传入）、`:843-848`（无条件展示"使用夏令时偏移"）、`:434`（公式称"按各地区夏令时规则取偏移量"）。
- 复现：node 复刻 `convertTime`：源北京 480、目标纽约 −240（勾 DST），日期 2026-01-15 12:00 → 结果 `2026-01-15 00:00`；未勾选（−300）→ `2026-01-14 23:00`。1 月纽约实际为 EST（−300），勾选后早 1 小时。
- 影响：`tools/edu/timezone-converter.html`；冬季跨时区会议/航班时间整体偏移 1 小时，属核心计算错误。
- 方案：按所选日期判断 DST（`dstMonths` 起止日 + 实际切换规则），无日期时用当前日期；`isLikelyDST` 接入 `getOffset`，并在结果中显示"该日是否处于 DST"。

### EL-J124 「时区转换」世界时钟恒用标准偏移，DST 徽标却常显，"可能夏令时"说明与实现不符（中，确认缺陷）
- 问题：`updateWorldClock` 调 `getOffset(tz,false)`，永远按标准偏移算当前时刻；`renderWorldClock` 对所有有 `dstOffset` 的城市无条件渲染"☀️ 夏令时 UTC±X"徽标。提示框却说徽标表示"在特定月份可能使用夏令时"。
- 证据：`tools/edu/timezone-converter.html:781`（`getOffset(tz,false)`）、`:796-797`（`if(tz.dstOffset!==null) dstNote=...` 无月份判断）、`:442`（"标有'可能夏令时'…"）、`:434`。
- 复现：8 月查看纽约世界时钟 → 按 −300 显示，比实际 EDT（−240）慢 1 小时；1 月查看仍显示"夏令时 UTC−4"徽标。期望按当前日期取 −240 并只在 DST 期显示徽标。
- 影响：`tools/edu/timezone-converter.html`；世界时钟与真实当地时间不符，徽标误导。
- 方案：`updateWorldClock` 改用 `getOffset(tz, isLikelyDST(tz))`；徽标按当前月份显隐，文案统一为"夏令时期间 UTC±X"。

### 留存建议（tools/edu/timezone-converter.html）
- DST 按具体日期/规则判断，`isLikelyDST` 接入主流程，世界时钟同步。
- 校验时/分/秒范围（`:818-820` 目前 25 点会静默进位到次日），下拉标签随 DST 勾选更新。

### EL-J126 「国家测验」宣称"国旗、首都或地理位置"且"限时作答"，实际仅国旗题、无计时器、无错题库（高，承诺未实现）
- 问题：meta 与 og 描述写"随机考查国旗、首都或地理位置对应的国家，限时作答并判分"，页面只有国旗 emoji 一种题型，`next()` 固定问"这面国旗属于哪个国家？"，全程无倒计时/超时；deep-dive 的"错题库：强化易错项"也无任何实现。
- 证据：`tools/edu/country-quiz.html:10`（宣称）、`:254-261`（仅 `{name,flag}`）、`:287`（唯一题干）、`:265-318`（`start/next/choose` 无计时）、`:202`（"错题库"）。
- 复现：开始答题 10 题 → 题面全部是国旗，无首都/位置题；页面找不到计时条，超时不判错；答错后仅高亮正确项，无错题收集/复盘入口。
- 影响：`tools/edu/country-quiz.html`；简介承诺的三种题型与限时均落空，SEO 描述与功能不符。
- 方案：二选一 —— ① 补首都/位置题型（题库加 `capital/region` 字段）与倒计时；② 把 meta/deep-dive 改为"国旗专项"，并删除"首都/位置/限时/错题库"表述。

### EL-J127 「国家测验」题库仅 20 国，国旗以 emoji 渲染，部分平台可能显示字母代码（中，待验证）
- 问题：`countries` 只有 20 个条目，覆盖"全球主要国家"偏少；国旗用 Unicode emoji（`🇨🇳`）直接 `textContent` 上屏，Windows Chrome/部分 Linux 无彩色国旗字形，会回退为 "CN" 等区域指示符字母，题目退化为"猜国家代码"。
- 证据：`tools/edu/country-quiz.html:254-261`（20 条 emoji 数据）、`:288`（`flag.textContent=cur.flag`）；同批 `flag-quiz.html:252-261` 为 24 国。
- 复现：在无 emoji 国旗字形的平台打开 → 国旗位显示"CN/JP"字母而非旗帜；题库抽 10 题仅来自 20 国，重复练习很快穷尽。
- 影响：`tools/edu/country-quiz.html`；跨平台可用性与题量不足（平台渲染需真机确认）。
- 方案：国旗改用 SVG/PNG 资源（本地或内联）并按 `flagcdn` 映射；题库扩到 50+ 并标注洲别/难度。

### 留存建议（tools/edu/country-quiz.html）
- 实现首都/位置题型与倒计时，或统一改宣称；补错题本（记录答错国家，复练）。
- 国旗改图片资源，避免 emoji 平台差异；题库扩量并按难度分层。
- 与 `flag-quiz.html` 明确分工（本页做首都/位置，另页做国旗），消除近重复。

### EL-J128 「国旗测验」英文简介称"timed multiple-choice quiz"但无计时器，错题库未实现（中，承诺未实现）
- 问题：`formula-desc` 英文写"timed multiple-choice quiz"，中文 meta 写"即时判分并累计成绩"；实际 `choose()` 只判分后 900ms 进下一题，全程无倒计时/超时判负；deep-dive 的"错题库：强化易错"也无实现。
- 证据：`tools/edu/flag-quiz.html:158`（timed）、`:303-315`（`choose` 无计时）、`:200`（"错题库"）。
- 复现：答 10 题 → 无计时显示，停留任意久也不判错；答错后无错题清单，重开 `start()` 只重新随机抽题。
- 影响：`tools/edu/flag-quiz.html`；英文态描述与功能不符，错题强化承诺落空。
- 方案：加每题倒计时（超时记错）并显示剩余秒数，或在文案删"timed"；补错题本并在下一轮优先抽错题。

### EL-J129 「国旗测验」与「国家测验」逻辑与题库近重复，仅多 4 国且少一行题干（中，确认缺陷）
- 问题：两页 `data/countries` 前 20 条完全相同，`start/reset/next/choose/finish` 与 `__tbq` 历史（localStorage key 仅前缀不同）几乎逐行一致；国旗页多 4 国（挪威/希腊/土耳其/泰国），国家页多一行 `question` 文本。两页对搜索引擎与用户都是近重复内容。
- 证据：`tools/edu/flag-quiz.html:252-261`（24 国）与 `tools/edu/country-quiz.html:254-261`（20 国，前 20 条同）；`flag-quiz.html:264-320` 对比 `country-quiz.html:265-319`；历史 `flag-quiz.html:342-371` 对比 `country-quiz.html:346-371`。
- 复现：同一轮 10 题，两页题干除国旗页无"Q1."前缀外一致；答错高亮、得分口径、完成文案、历史 CSV 全部相同。
- 影响：`tools/edu/flag-quiz.html`、`tools/edu/country-quiz.html`；关键词自相竞争，用户无差异化理由。
- 方案：按题型拆分（国旗页只考国旗+限时；国家页考首都/位置+错题本），题库与文案各自独立；或合并为一页并 301/存根处理另一 URL（须按 §4.6 提死链）。

### 留存建议（tools/edu/flag-quiz.html）
- 与 country-quiz 分工，避免同题库同逻辑；题库扩量并加难度分级。
- 历史记录同时存题量/用时，CSV 增加这两列，支撑"成绩累计"。

### EL-J130 「高考/考研倒计时」大字天数与"剩余总天数"统计差 1，考试前一天统计为 0（中，确认缺陷）
- 问题：hero 用 `diff = round(target-now)`（今天到考试日，含今天为第 0 天）；`countDays` 从"明天"开始 `while(cur<target)`，不含今天也不含考试当天。两者口径不同，导致同屏两个"剩余天数"相差 1；考试前一天 `countDays` 返回 0，而大字显示"1 天后开考"。
- 证据：`tools/edu/countdown-5.html:267-278`（`cur.setDate(+1)` 后循环到 `<target`）、`:299`（`diff`）、`:304`（hero 大字）、`:308`（`statTotal=d.total`）、`:312-313`（"距考试还有 d.total 天"）、`:158-159`（公式称"剩余天数 = round(目标−今日)"与"区间统计"并存）。
- 复现：node 复算 today=2026-11-04，target=2026-11-10 → `diff=6`、`countDays={total:5,work:3,weekend:2}`；target=2026-11-05 → `diff=1`、`total:0`。页面同时显示"1 天后开考"和"剩余总天数 0"。
- 影响：`tools/edu/countdown-5.html`；首屏主数字与统计卡自相矛盾，考前最后一天显示 0 天。
- 方案：统一口径（推荐"含今天、不含考试日"：`total = diff`，工作日从今天起算），或 hero 也用 `d.total` 并改文案；公式说明同步为同一口径。

### EL-J131 「高考/考研倒计时」重复两组"相关工具"与两个公式框，三处空 toast（低，确认缺陷）
- 问题：同一页连续输出两份 `related-tools`（第二份工具卡描述更长），`formula-box` 也重复两次；`saveExam/addLog/clearLog` 的错误/信息分支多处调用 `i18nText()` 不传 key。
- 证据：`tools/edu/countdown-5.html:157-164`（两个公式框）、`:438-466` 与 `:467-496`（两组相同 6 卡相关工具）、`:241`、`:261`、`:263`（空参 `i18nText()`）。
- 复现：页面"相关工具"出现两遍；点"清空记录"（无记录时）或输入非法时长 → toast 文案为空/undefined（真实文案待浏览器确认）。
- 影响：`tools/edu/countdown-5.html`；DOM 重复、页面冗长，错误提示缺失。
- 方案：删除后一组 `related-tools`（保留描述更完整的一份）与一个公式框；所有 toast 传真实 key。

### 留存建议（tools/edu/countdown-5.html）
- 统一剩余天数口径，hero 与统计卡使用同一 `countDays` 结果。
- 删重复 related-tools/formula-box；补 toast key 与日期区间校验（当前可给任意未来日期打卡）。
- 打卡按日期区间校验并支持"今日投入 vs 剩余所需日均"提示，增强备考闭环。

### EL-J132 「学习进度仪表」说明称"预计完成日按工作日计"，代码按日历天累加（中，确认缺陷）
- 问题：进度说明明确"预计完成日 = 今日 + 剩余工时 ÷ 每日学习时长（按工作日计）"，但 `estDate` 直接用 `today + needDays*86400000`，把周末也计入；"进度滞后"建议的 `needDaily` 也按日历天摊平。
- 证据：`tools/edu/study-progress.html:161`（按工作日计）、`:310-316`（`estDate.setTime(today+needDays*86400000)`）、`:366-368`（`needDaily=totalRemainHours/daysToTarget`）。
- 复现：剩余 17h、日投入 4h → `needDays=5`，从周五 2026-11-06 起算 → 预计 11-11（周三）；按工作日口径应为 11-13（跳过周末）。页面显示 11-11，与说明不符。
- 影响：`tools/edu/study-progress.html`；预计完成日偏早，目标评估（onTrack）偏乐观。
- 方案：按工作日推进（逐日跳过周六/日，可选法定节假日），或把说明改为"按日历天、含周末"。

### EL-J133 「学习进度仪表」每任务耗时非数字未校验，NaN 传播后整块结果变成"—"（中，确认缺陷）
- 问题：`parseSubjects` 只校验 name/done/total，第 4 段 `hours` 直接 `parseFloat`，`NaN` 会进入 `remainHours` → `totalRemainHours` → `needDays` → `estDate`；渲染时 `String(html).replace(/Infinity|NaN/g,'—')` 把错误伪装成占位符，用户看不到原因。`dailyHours` 为 0/负数也仅用 `||4` 兜底 0，负数不拦。
- 证据：`tools/edu/study-progress.html:271`（`hours=p[3]?parseFloat(p[3]):1`，无 `isNaN`）、`:303`（`s.remainHours=s.remain*s.hours`）、`:312-316`（`needDays/estDate`）、`:334-336`（展示 `toFixed`）、`:377`（`replace(/Infinity|NaN/g,'—')`）、`:296`（`||4`）、`:310`（`dailyHours` 负数未校验）。
- 复现：输入 `数学,45,80,abc` → node 复算 `hours=NaN`；页面"剩余工时 — h""预计还需 — 天""预计完成日 —-aN-aN"（`fmtDate` 对 Invalid Date 拼出 `NaN-aN-aN`，再被 `:377` 部分替换），且无任何错误提示。
- 影响：`tools/edu/study-progress.html`；一行格式错误即让全部统计失效，且被静默显示为破折号。
- 方案：`hours` 校验 `isFinite && >0`，非法行给出明确提示并跳过；`dailyHours` 用 `Number.isFinite(v)&&v>0?v:4`，负数/0 拒绝。

### EL-J134 「学习进度仪表」目标日期已过仍给中性提示，"距目标天数"负值被钳成 0（中，确认缺陷）
- 问题：`daysToTarget` 为负时，统计卡显示 `0`（`daysToTarget>=0?…:0`）；滞后分支要求 `daysToTarget>0`，`onTrack` 又为 false，于是逾期直接落入最后的 else，输出"按每日 N 小时计算，预计…完成全部任务。设置目标日期可评估是否按期完成"，完全不提"目标已过期"。
- 证据：`tools/edu/study-progress.html:322-326`（`daysToTarget/onTrack`）、`:341`（负值→0）、`:366-374`（三分支条件）。
- 复现：目标日期设为 2026-11-03、今天 2026-11-04、剩余 17h/日 4h → node 复算 `daysToTarget=-1`、`onTrack=false`、`shownDays=0`；页面显示"距目标 0 天"和中性提示，不提示已逾期。
- 影响：`tools/edu/study-progress.html`；逾期被掩盖，目标评估失效。
- 方案：`daysToTarget<0` 单独分支显示"已逾期 N 天"；统计卡显示负值或"已逾期"；`onTrack` 在目标已过时恒 false 并高亮。

### EL-J135 「学习进度仪表」只持久化科目文本，目标日期/每日时长每次重置；"导出明细"实为历史表（中，确认缺陷）
- 问题：`saveInput` 仅把 `#subjectInput` 写入 localStorage；`targetDate` 在每次加载被强制设为"今天+45 天"，`dailyHours` 完全不保存。"导出明细 CSV"绑定 `#study_progressTable`，该表是 TBKit 历史记录表（输入快照+结果摘要），不是当前各科明细；无历史时导出为空。
- 证据：`tools/edu/study-progress.html:256-258`（仅存 subjectInput）、`:386-390`（加载即覆盖 targetDate）、`:150`（"导出明细 CSV"）、`:545-548`（导出 `#study_progressTable`）、`:479-490`（该表由 `TBKit.history` 渲染）。
- 复现：设目标 2026-12-31、日投入 3h → 刷新页面 → 目标变回"今天+45 天"、日投入回 4h；点导出 → 得到历史快照表（列含"时间/各输入/结果"），不是"科目/完成/总数/耗时"明细。
- 影响：`tools/edu/study-progress.html`；用户设置丢失，导出内容与按钮文案不符。
- 方案：把 `targetDate/dailyHours` 一并存入 `toolbox_study_progress`（改 JSON 结构并兼容旧纯文本）；导出改用当前 `list` 生成科目明细 CSV，或把按钮改为"导出历史记录"。

### 留存建议（tools/edu/study-progress.html）
- 预计完成日与 `needDaily` 统一口径（工作日或日历天），说明与代码一致。
- 校验第 4 段耗时与每日时长，非法输入明确提示，不要用"—"掩盖 NaN。
- 持久化目标日期/每日时长；补逾期分支；导出当前科目明细而非历史表。

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

### EL-J136 「知识成熟度自评」缺口用固定 <6 阈值，与公式「最低分维度即缺口」不符（中，确认缺陷）
- 问题：公式框写明「最低分维度即知识缺口优先改进项」，代码却只收集 `<6` 的维度；六个维度全打 6 分时最低分仍存在，页面却输出「知识管理各维度均达标」，缺口卡片完全不出现。
- 证据：`tools/edu/assessor-27.html:120`（公式定义最低分维度为缺口）、`:220`（`d.v<6` 过滤）、`:223-224`（else 分支判全达标）。
- 复现：六项均填 6 → node 复算均分 `6.00`、`gaps<6=[]`；页面显示「综合评分 6.00/10、3级-规范级」+「各维度均达标」，没有任何缺口项。
- 影响：`tools/edu/assessor-27.html`；只要各维度都 ≥6，工具就宣称"无缺口"，与自评模型「短板优先」的核心承诺相反。
- 方案：按 `min(d.v)` 找出最低维度并始终列为优先缺口（可再叠加 `<6` 阈值作为"严重缺口"），文案区分"最低项/未达标项"。

### EL-J137 「知识成熟度自评」评分无范围校验，15 分计入并判为最高等级（高，确认缺陷）
- 问题：六个 number 输入只声明 `min=1 max=10`，`calc()` 用 `+value||0` 直接取值，既不做 0–10 钳制也不提示越界；空值被静默当 0 参与平均，仍输出完整等级。
- 证据：`tools/edu/assessor-27.html:124-129`（仅 HTML min/max）、`:212`（`+document.getElementById('d1').value||0`）、`:213-214`（直接平均与分档）。
- 复现：把六项全填 15 → node 复算 `avg=15.00`，页面输出 `15.00/10` +「5级-优化级」；六项全清空 → `0.00/10` +「1级-初始级」，无任何"请输入"提示。
- 影响：`tools/edu/assessor-27.html`；评分口径失真，越界值直接抬高成熟度结论。
- 方案：`calc()` 内对每维做 `Number.isFinite` 与 `0–10` 校验，越界标红并中止；空值提示而不是按 0 计。

### EL-J138 「知识成熟度自评」缺口建议只覆盖三项，仅缺"存储/安全"时输出空「建议：」（中，确认缺陷）
- 问题：缺口提示的拼接只包含知识共享、知识创新、知识捕获三种，`知识存储`、`知识安全` 落入缺口列表却没有对应建议；极端情况下整段只剩「建议：」后无内容。
- 证据：`tools/edu/assessor-27.html:220`（缺口可为六项中任意项）、`:222`（仅三个 `indexOf` 分支拼接）。
- 复现：输入 7、7、7、7、5、5（仅存储与安全不达标）→ 缺口为「知识存储、知识安全」，建议串为空，页面显示「知识缺口：知识存储、知识安全 建议：」。
- 影响：`tools/edu/assessor-27.html`；用户看到断句，得不到可执行改进项。
- 方案：为六维各配一条建议（存储→统一文档库/备份策略，安全→权限分级与脱敏），并按缺口顺序全部输出；无建议时省略「建议：」。

### 留存建议（tools/edu/assessor-27.html）
- 评分统一走 `0–10` 校验与钳制，空值与越界分别提示，禁止用 `||0` 兜底。
- 缺口改为「最低分维度 + 未达标维度」双口径，保证永远有优先改进项。
- 六维建议表补全，提示块按实际缺口动态拼接，不留空标签。

### EL-J139 「标准分Z分数」选「分数越低越好」后，等级与百分位文案互相矛盾（高，确认缺陷）
- 问题：`direction=lower` 只把等级判定的 Z 取反，百分位仍按原始 Z 计算并固定写「该分数约高于 X% 的参照群体」。低分被标为「良好」，同一结果区却称它高于极少数人。
- 证据：`tools/edu/calc-2.html:149-152`（比较方向）、`:325-332`（`score = -z` 后分档）、`:346-349`（`pct=percentile(z)`、`effectiveZ=-z`）、`:358`（固定「高于 ${pct}%」）。
- 复现：原始分 45、均值 60、标准差 8、方向「越低越好」→ node 复算 `z=-1.875`、`pct=3.04%`、`effectiveZ=1.875`；页面显示「有效 Z 1.8750／等级 良好」，同时写「该分数约高于 3.04% 的参照群体」。
- 影响：`tools/edu/calc-2.html`；反向指标场景下等级与解释完全相反，用户无法判断成绩好坏。
- 方案：lower 时百分位改用 `1-Φ(z)`（或输出「优于 96.96% 的参照群体」），文案按方向切换；不要只翻转等级。

### EL-J140 「标准分Z分数」负 Z 仍称「高于参照群体」，百分位方向词写反（中，确认缺陷）
- 问题：百分位是标准正态 CDF（低于该值的比例），但结果区对任意 Z 都写「约高于 X% 的参照群体」；Z 为负时实际是"低于"多数人，句子与数值相反。
- 证据：`tools/edu/calc-2.html:321-322`（`percentile = normalCDF(z)*100`）、`:358`（固定「高于 …%」）。
- 复现：原始分 62.2、均值 75、标准差 10 → node 复算 `z=-1.28`、`pct=10.03%`；页面显示「该分数约高于 10.03% 的参照群体」，实际应表述为低于约 90% 的群体。
- 影响：`tools/edu/calc-2.html`；低于均值的学生被描述成"高于一成"，统计解释错误。
- 方案：按 `z>=0` 输出「高于/处于第 pct 百分位」，`z<0` 输出「低于 …%」；或统一改用"百分位排名"措辞。

### EL-J141 「标准分Z分数」公式承诺的 T 分数无输出，FAQ/指南仍是通用套话（低，确认缺陷）
- 问题：公式框写「T 分数 = 50 + 10Z 便于成绩解释」，结果区只输出 Z、百分位、有效 Z，没有 T 分数；页尾 `opt-guide`/`opt-faq` 与 FAQPage JSON-LD 仍是"点击「计算」或「生成」"模板。
- 证据：`tools/edu/calc-2.html:128`（T 分数公式）、`:351-358`（结果卡仅三项）、`:494`（可见套话）、`:77`（FAQ JSON-LD 套话）。
- 复现：任意输入计算 → 结果区无 T 字段；页面尾部出现「在对应的输入框或选项中填写…点击「计算」或「生成」按钮运行」。
- 影响：`tools/edu/calc-2.html`；公式展示与输出不一致，SEO 段落与工具实际交互不符。
- 方案：结果卡补 T 分数（`50+10*effectiveZ`）；删除/替换 opt-guide 与 opt-faq，FAQPage 同步改写。

### 留存建议（tools/edu/calc-2.html）
- 方向切换时同时调整百分位、文案与等级，三者用同一 `effectiveZ` 口径。
- 负 Z 用"低于/百分位"表述，避免"高于"造成误读。
- 补 T 分数输出，清理通用指南与 FAQ 套话（含 JSON-LD）。

### EL-J142 「错题本」第 3 轮复习点「已掌握」弹出 `undefined天后再复习`（高，确认缺陷）
- 问题：`nextInfo` 用 `REVIEW_INTERVALS[Math.min(stage+1,4)]`，而数组只有 4 项（索引 0–3）；stage=3 时取索引 4 得 `undefined`，直接拼进提示文案。
- 证据：`tools/edu/reminder-1.html:316`（`[1,3,7,14]`）、`:426`（stage 名称到 4）、`:435-437`（`stage<4` 时计算 `Math.min(stage+1,4)`）。
- 复现：某题连续 3 次「已掌握」推进到 stage=3 → 打开复习弹窗 → node 复算 `REVIEW_INTERVALS[4]=undefined`，页面显示「选择"已掌握"→undefined天后再复习」。
- 影响：`tools/edu/reminder-1.html`；最后一轮复习的排期说明失效，用户不知道点"已掌握"后是否还需复习。
- 方案：stage=3 单独文案「已掌握→标记为已掌握，不再排期」；或把数组补一项并统一 stage→interval 映射。

### EL-J143 「错题本」只按学科归类，"按错误类型自动归类"未实现（中，确认缺陷）
- 问题：描述与简介称「自动按学科和错误类型归类」，实际只有学科筛选 chip 与学科分布条；错误类型仅作为卡片上的文字标签，没有分组、筛选或错因统计。
- 证据：`tools/edu/reminder-1.html:10`（meta description 宣称双维归类）、`:173`（正文简介同述）、`:539-543`（仅生成学科 chip）、`:620-637`（仅学科分布）、`:567`/`:594`（错误类型只作 `q-type` 文本）。
- 复现：添加 5 道"计算错误"、3 道"审题失误" → 筛选区只有学科选项，无法按错误类型查看，也无错因占比统计。
- 影响：`tools/edu/reminder-1.html`；错因分析这一核心卖点不可用，用户仍要人工翻卡片。
- 方案：补错误类型 chip 筛选与"错因分布"统计块，或把文案降级为"按学科归类，错误类型仅标签"。

### EL-J144 「错题本」删除/清空时 `i18nText()` 无参，toast 显示 `undefined`（低，确认缺陷）
- 问题：`delQuestion` 与 `clearAll` 调用 `ToolBox.showToast(i18nText())`，`i18nText` 收到 `undefined` 会原样返回该值，toast 文案变成 `undefined`。
- 证据：`tools/edu/reminder-1.html:417`（删除）、`:649`（清空）；`js/common.js:1510-1522`（无 key 时返回 `key` 本身）。
- 复现：删除任意错题或确认清空 → toast 文本为 `undefined`（node 复刻 `normalizeI18nKey(undefined)` 返回 `undefined`）。
- 影响：`tools/edu/reminder-1.html`；操作反馈变成乱码，且与同页其它已配 key 的 toast 不一致。
- 方案：改用具体 key（如 `toast.deleted` / `toast.cleared`）或直接传中文兜底字符串。

### 留存建议（tools/edu/reminder-1.html）
- 修正 stage=3 的排期文案，补齐 `REVIEW_INTERVALS` 与 stage 的边界映射，并加单测式 node 复算。
- 实现错误类型筛选/统计，或把"双维归类"改写为"按学科归类"。
- 所有 `showToast` 必须显式传 key 或文案，禁止空参调用。

### EL-J145 「考试成绩目标计算」深挖算例 91.7 与页面实际口径 25.00 冲突（高，确认缺陷）

> **订正（2026-11-05）**：本条结论已过时。`edu/calc-4` 及 `dermatology/vasi-vitiligo`、`obstetrics/fetal-weight-hadlock`、`fishery/feed-protein-fat` 四页经 `calc()` 实跑复核：HEAD 值与实现吻合（95.0 / 16.75 / 2892 g / 11.45 kJ/g）；早先「确认错值」结论有误，存档值（91.7 / 28 / 3100 / 1.14）才无算式来源。现页面 `calc()` 为 `earned=当前成绩×当前权重/100`、`需平均=(目标−earned)/剩余权重`，70/40/85 → 95.0，与深挖示例一致；本条下述「页面得 25.00」为改版前旧实现，已不适用。台账见 `plan/tools-audit-84-ledger.md`。

- 问题：输入标签把当前成绩定义为"加权后"的贡献，页面按 `(目标 − 当前)/剩余权重` 计算；深挖算例却用 `(85 − 70×0.4)/0.6 = 91.7`，即把当前成绩当成未加权原始分。同输入 70/40/85 在页面得 25，在文档示例得 91.7。
- 证据：`tools/edu/calc-4.html:138`（"当前已得成绩（加权后）"）、`:311-312`（`(target-current)/remainingWeight*100`）、`:229`（`(85−70×0.4)/0.6=91.7`）。
- 复现：当前 70、权重 40、目标 85 → node 实算页面公式 `(85−70)/60×100=25.00`；按页面输出「剩余考核平均分 25.00%」，而深挖示例写 91.7%。
- 影响：`tools/edu/calc-4.html`；用户按示例核对会得到相差 66.7 分的结果，无法信任倒推值。
- 方案：统一口径——若输入是加权贡献，示例改为 `(85−70)/60×100=25`；若想收原始分，则页面先算 `current×weight/100` 再倒推，并改标签。

### EL-J146 「考试成绩目标计算」剩余考核项数不参与计算，"每项平均分"恒等于总平均分（中，确认缺陷）
- 问题：`remainingParts` 只做 `>=1` 校验与重置，计算完全不用；`perPart = neededAvg`，于是"每项考核平均分"和"剩余考核平均分"永远同一个数，1 项与 5 项输出完全相同。
- 证据：`tools/edu/calc-4.html:297`（读取）、`:300`（仅校验）、`:313-314`（`perPart=neededAvg`）、`:333-334`（两张同值卡片）。
- 复现：其余输入固定，剩余项数 1 → 2 → 5，结果区三项数值完全不变；node 复算默认参数均为 17.50。
- 影响：`tools/edu/calc-4.html`；一个显式输入参数是死参数，误导用户以为会按项拆分。
- 方案：要么按项数输出「每项需 N 分」并说明均分相同（当前逻辑本就如此，可保留但文案改"每项均需"）；要么真正支持各项权重/分值差异并移除该输入。

### EL-J147 「考试成绩目标计算」当前成绩无 0–100 校验，150 分算出 -162.50% 仍判"目标可行"（高，确认缺陷）
- 问题：校验只覆盖 `currentWeight`、`targetScore`，漏掉 `currentScore` 的上下界；超满分输入会得到负数所需平均分，可行性分支落入最后的 else，输出绿色"目标可行，保持状态即可"。
- 证据：`tools/edu/calc-4.html:129`（公式声明成绩 ∈[0,100]）、`:300`（校验条件不含 `currentScore`）、`:311-312`（无钳制计算）、`:317-328`（`neededAvg>100` 才不可行）。
- 复现：当前 150、权重 60、目标 85 → node 复算 `neededAvg=-162.50`；页面显示「剩余考核平均分 -162.50%／每项考核平均分 -162.50%／剩余权重 40.0%」+「目标可行，保持状态即可」。
- 影响：`tools/edu/calc-4.html`；越界输入产出负分且被判定为可行，结论与数值自相矛盾。
- 方案：校验 `currentScore ∈ [0,100]`，越界提示并中止；`neededAvg<0` 时输出"当前已超过目标，无需追加"。

### 留存建议（tools/edu/calc-4.html）
- 明确"当前成绩"是加权贡献还是原始分，并让示例、标签、公式、校验四处一致。
- 让 `remainingParts` 产生可见作用，或删除该输入避免死参数。
- 补 `currentScore` 范围校验，负数/超满分的结论单独分支。

### EL-J148 「记忆宫殿位置编码」公式描述的三层编码与实现不符，无家具序号（中，确认缺陷）
- 问题：公式称编码为「房间号 + 家具位 + 序号」，可写作 `房间×100 + 家具×10 + 序号` 或 `A1-01`；代码输出的是 `房间-A1-对象名`（如 `客厅-A1-沙发`），既没有家具位编号，也没有序号位，序号只出现在联想口诀末尾。
- 证据：`tools/edu/generator-26.html:120`（三层编码说明）、`:221`（`${room}-${gridX}${gridY}-${object}`）、`:223-225`（位置编码/坐标/口诀展示）。
- 复现：生成 5 条 → 编码形如 `客厅-A1-沙发`、`卧室-B1-电视`…`阳台-A2-花盆`，只有"房间+坐标"，无法从编码还原公式宣称的"家具位"或"序号"，也得不到 `客厅×100+家具×10+序号` 的数值编码。
- 影响：`tools/edu/generator-26.html`；编码方案与说明不一致，用户按公式手算对不上页面。
- 方案：输出同时给"数值编码"（`roomIdx*100+furnitureIdx*10+seq`）与字符编码；或改写公式为实际的"房间-坐标-锚点"三段式。

### EL-J149 「记忆宫殿位置编码」只有生成数量一个参数，房间/家具/序号规模不可配（中，确认缺陷）
- 问题：页面的唯一输入是 `cnt`；公式给出 `总挂钩点 = 房间数 × 家具数 × 序号数`，但没有任何入口调整 R/F/N，房间固定 10 个、锚点固定 18 个、坐标由 `i` 推导，生成结果只随条数变化。
- 证据：`tools/edu/generator-26.html:120`（R×F×N 公式）、`:124`（唯一 `cnt` 输入）、`:209-221`（房间/物品/坐标全部硬编码或按 `i` 取模）。
- 复现：`cnt=5` 与 `cnt=25` 均只改变条数；房间循环固定 10、对象固定 18，无法生成"3 房间 × 4 家具 × 5 序号"的定制宫殿。
- 影响：`tools/edu/generator-26.html`；生成器与记忆宫殿规模参数不联动，无法按实际空间定制。
- 方案：增加房间数、每房间家具数、每家具序号数三个输入，输出 `R×F×N` 个唯一编码并展示总数。

### EL-J150 「记忆宫殿位置编码」输入 0 生成 5 条，且存在未使用的随机函数（低，确认缺陷）
- 问题：`parseInt(value)||5` 把 `0` 当假值回退成 5，违背 1–50 的提示；`randInt` 定义后从未调用。
- 证据：`tools/edu/generator-26.html:124`（min=1 提示）、`:209`（`||5` 兜底）、`:205-207`（`randInt` 无调用）。
- 复现：生成数量填 0 → node 复算 `Math.min(Math.max(parseInt('0')||5,1),50)=5`，页面输出 5 条而非 1 条或报错。
- 影响：`tools/edu/generator-26.html`；边界输入被静默改写，提示与行为不符。
- 方案：用 `Number.isFinite` 判断后再钳制，0/空值提示；删除死函数。

### 留存建议（tools/edu/generator-26.html）
- 统一编码口径：字符编码与数值编码同屏输出，说明与 `gen()` 逐项对齐。
- 补 R/F/N 三个参数并校验总数上限，避免只改条数的伪联动。
- 修正 0 值兜底，清理未使用的 `randInt`。

### 留存建议（tools/edu/convert-3.html）
- 逐位合法性校验替代 `parseInt` 的宽松解析，非法字符定位到位置并报错。
- 决定单值或批量：若保留批量文案就实现分隔解析与结果表。
- 统一负数与大数口径，修正 FAQ 与"精确无近似"表述。

### EL-J154 「摘要生成器」没有文本输入，永远摘要同一段硬编码示例（高，确认缺陷）
- 问题：页面唯一输入是"生成数量"，`gen()` 始终对常量 `sampleText` 分词打分；用户无法粘贴自己的文章，调整数量只是在同一段 8 句样例里换选句。
- 证据：`tools/edu/generator-4.html:124`（唯一 `cnt` 输入）、`:205`（`const sampleText=` 硬编码）、`:214`（`tokenizeSentences(sampleText)`）。
- 复现：任意修改"生成数量"→ 结果始终来自同一段 AI 介绍文字；页面没有 textarea，无法输入自定义文本。
- 影响：`tools/edu/generator-4.html`；工具退化为固定示例演示，"Summarize a passage"的能力不存在。
- 方案：增加 textarea（预填示例）并让 `gen()` 读取用户文本；空输入时提示，示例仅作占位。

### EL-J155 「摘要生成器」公式承诺的位置加权/标题词加权/长度惩罚/压缩率均未实现（中，确认缺陷）
- 问题：公式框写「句子得分 = Σ词频 + 首段×1.5 + 含标题词×1.2 − 长度惩罚；压缩率 = 摘要字数/原文字数」，代码只算"该句实词词频的平均值"，无位置、标题词、长度项，也不输出压缩率。
- 证据：`tools/edu/generator-4.html:120`（完整公式）、`:221-224`（仅 `词频和/词数`）、`:228-235`（结果只有句子与权重）。
- 复现：同一段文本下首句与末句权重只由词频决定；结果区无"压缩率"字段，node 复算 `score` 仅等于平均词频。
- 影响：`tools/edu/generator-4.html`；公式展示与实际算法不符，用户无法按说明理解排序依据。
- 方案：实现三项加权并在结果标注各分项，或把公式改写为"平均词频打分"；补压缩率输出。

### EL-J156 「摘要生成器」生成数量大于句数时静默截断，无任何提示（低，确认缺陷）
- 问题：`cnt` 允许 1–50，但样例只有 8 句，`slice(0,n)` 超过句数时只返回全部 8 句，界面不说明"已达上限"。
- 证据：`tools/edu/generator-4.html:124`（max=50）、`:227`（`scored.slice(0,n)`）、`:205`（样例仅 8 句）。
- 复现：生成数量填 20 → 页面仍只输出 8 句，标题仍写"生成结果"，无"文本仅 8 句"提示；node 统计 `tokenizeSentences(sampleText).length=8`。
- 影响：`tools/edu/generator-4.html`；用户以为参数未生效。
- 方案：`n=min(n, sentences.length)` 后在结果区注明"原文共 8 句，已全部选取"，并给出上限提示。

### 留存建议（tools/edu/generator-4.html）
- 增加可编辑 textarea，示例文本仅作默认值，`gen()` 必须读用户输入。
- 按公式实现位置/标题词/长度加权与压缩率，或同步改写公式。
- 句数上限与提示对齐，避免"数量调大但结果不变"。

### 留存建议（tools/edu/convert-2.html）
- 四种格式各自加严格正则 + 范围校验，非法输入一律报错，禁止 NaN 落成 0 或破折号。
- 输出前钳制通道值，保证 HEX/RGB 永远合法。
- 精度口径与实现二选一，缺参单独提示。

### 留存建议（tools/edu2/exam-countdown.html）
- 删除或真正实现"统计周末"，让开关与统计口径一致。
- 进度条改用可解释基准（起始日→考试日），无起始日就不显示。
- 节假日数据按年份维护并标注覆盖范围，缺年份时提示不扣减。

### EL-J163 「考试成绩分析」及格线调到 >75% 后，等级与及格率互相矛盾（中，确认缺陷）
- 问题：等级判定顺序是"优秀线 → 满分 75% → 及格线"，75% 分支优先于及格线；当及格线设成 90% 时，78 分学生被标"良好"，却因 `<90` 不计入及格人数，及格率把它算作未及格。
- 证据：`tools/edu2/exam-analysis.html:331`（`passCount` 以 `passScore` 计）、`:389-390`（`score>=full*0.75` 先于 `score>=passScore`）、`:128`（公式也写"≥满分75% 良好"）。
- 复现：满分 100、及格线 90%、优秀线 95%，录入 78 分 → node 复算 `pass? false`，等级函数输出「良好」；结果区同一人「良好」但及格率不含他。
- 影响：`tools/edu2/exam-analysis.html`；自定义及格线后名单与统计口径冲突，教师无法解释。
- 方案：等级改为按 `excellentScore → passScore → 其他` 顺序，或把"良好"阈值也改成动态（如 `max(passScore, 75%×full)`），并同步公式说明。

### EL-J164 「考试成绩分析」打开即载入 15 人示例并自动写历史，预设按钮还会覆盖用户输入（中，确认缺陷）
- 问题：`__exam_analysisBoot` 在加载时调用 `loadSample()`，`calc()` 被包装后会把示例结果写入 TBKit 历史；预设回调用 `__exam_analysisScaleSample` 直接把 `scoreInput` 改成样例，用户已录入的成绩被清空。
- 证据：`tools/edu2/exam-analysis.html:580`（boot 调 `loadSample`）、`:555`（`TBKit.history.record`）、`:570-573`（预设回调覆盖 `scoreInput`）。
- 复现：打开页面 → 历史表出现一条含 15 人示例的记录；先录入自己班级成绩，再点"小规模"预设 → 输入框被替换成缩放后的示例，原数据丢失。
- 影响：`tools/edu2/exam-analysis.html`；真实成绩与示例混淆，且预设造成不可撤销的数据覆盖。
- 方案：首屏不自动载入示例（改为空态+按钮），或载入但不写历史；预设只改满分/分数线，保留用户文本，必要时弹确认。

### EL-J165 「考试成绩分析」并列分数按输入顺序给不同名次，未处理并列（低，确认缺陷）
- 问题：排名直接对排序后的数组 `idx+1`，相同分数会得到连续且不同的名次，先输入者靠前，名次不代表同一水平。
- 证据：`tools/edu2/exam-analysis.html:354-355`（`sort` 后 `s.rank=idx+1`）。
- 复现：两名学生同为 92 分（张三在前、李四在后）→ 页面显示张三第 1、李四第 2；node 复刻排序与赋号一致。
- 影响：`tools/edu2/exam-analysis.html`；并列名次失真，家长/教师看到的排名不公平。
- 方案：按分数做 dense/competition ranking（同分同名次，下一名跳号），或加"并列"标记。

### 留存建议（tools/edu2/exam-analysis.html）
- 等级顺序改为 `优秀线 → 及格线 → 75%`，与及格率共用同一阈值链。
- 首屏不自动填示例、不自动写历史；预设保留用户已录入的成绩。
- 排名按并列规则赋号，并说明并列策略。

### 承诺 vs 实际（R 批专项）
- `tools/edu/assessor-27.html:120`「最低分维度即知识缺口优先改进项」→ 实际按固定 `<6` 过滤（`:220`），全 ≥6 即宣称无缺口。
- `tools/edu/calc-2.html:128`「T 分数 = 50 + 10Z」→ 结果区无 T 分数（`:351-358`）；`:77`/`:494` 仍是"点击计算或生成"套话。
- `tools/edu/reminder-1.html:10`/`:173`「自动按学科和错误类型归类」→ 只有学科筛选与分布（`:539-543`、`:620-637`），错误类型仅作文本标签。
- `tools/edu/calc-4.html:229`「(85−70×0.4)/0.6=91.7」→ **订正（2026-11-05）**：现 `calc()` 为加权口径 `earned=当前×权重/100`，同输入 70/40/85 → 95.0，示例 91.7 无算式来源；早先「页面口径 25」为旧实现，不适用。`:152` 的"剩余考核项数"仍不参与计算（`:313`）。
- `tools/edu/generator-26.html:120`「房间×100+家具×10+序号 / A1-01」→ 实际 `${room}-A1-${object}`（`:221`），无家具位与序号位。
- `tools/edu/convert-3.html:204`「批量转换：一次处理多个数」→ 仅单值输入（`:124`、`:169`）；`:180`「精确无近似」→ 大数受双精度限制。
- `tools/edu/generator-4.html:117`「Summarize a passage」→ 无文本输入，固定 `sampleText`（`:205`、`:214`）。
- `tools/edu/convert-2.html:214`/`:221`「保留输入精度」→ HSL 全程取整（`:171`），缺参输出 `rgb(—, —, —)`（`:178`）。
- `tools/edu2/exam-countdown.html:140`「统计周末」→ 读取后未使用（`:285` 为唯一引用），勾选不影响结果。
- `tools/edu2/exam-countdown.html:247` 注释「2025-2027 主要节假日」→ 仅 2026 年数据（`:248-255`）。
- `tools/edu2/exam-analysis.html` 宣称的批量粘贴（逗号/换行）、满分百分比换算、总体标准差均已实现；仅等级顺序在非默认及格线下与及格率冲突（EL-J163），不属虚标。

### 覆盖
- 实读 10 页（`tools/edu/assessor-27.html`、`calc-2.html`、`reminder-1.html`、`calc-4.html`、`generator-26.html`、`convert-3.html`、`generator-4.html`、`convert-2.html`，`tools/edu2/exam-countdown.html`、`exam-analysis.html`），10/10 全覆盖。
- 新增 30 条（EL-J136～EL-J165）：高 10 条（EL-J137、J139、J142、J145、J147、J151、J154、J157、J158、J160），中 12 条，低 8 条（EL-J141、J144、J150、J152、J153、J156、J159、J165），另附 10 组留存建议与 1 节"承诺 vs 实际"。
- 累计覆盖：07 教育 `tools/edu` 45 页 + `tools/edu2` 6 页共 51 页；本文件已覆盖 48 页，仍余 3 页（`tools/edu/convert-area-volume.html`、`tools/edu2/index.html`、`tools/edu2/schedule-conflict.html`），`plan/categories/07-教育学习/research-library.md` 负责的另一批不计入。
- 路径校正：上一批写的 `tools/edu/exam-analysis.html`、`tools/edu/study-progress.html` 实际不存在，真实地址为 `tools/edu2/exam-analysis.html`、`tools/edu2/study-progress.html`；本批按真实 URL 审计。
- 验证边界：仅静态读源码 + `node` 复刻（成熟度均分/缺口阈值、Z 与 CDF、错题 stage 边界、目标倒推与越界、位置编码、`parseInt` 截断、颜色 HEX/RGB 越界、倒计时进度与复选框、等级/及格率冲突、并列排名）；**未**做真实浏览器、移动端、英文态/繁体态、门禁、构建与线上验证。

### EL-J166 「长度/重量/温度/面积/体积单位换算」选“温度”后原/目标单位下拉为空，输出恒等于输入（高，确认缺陷）
- 问题：类别下拉有「温度」选项，但换算系数表 `U` 与名称表 `N` 都没有 `temp` 键；`fillSel()` 用 `for(const k in U[cat])` 遍历 `undefined` 得到空列表（不抛错），把两个 select 清空后不追加任何 option。随后 `calc()` 温度分支拿到 `f===""`、`t===""`，先走 `c=val-273.15` 再 `r=c+273.15`，结果永远等于原值。
- 证据：`tools/edu/convert-area-volume.html:124`（类别含 temp）、`:207-208`（U/N 无 temp）、`:209`（`for(const k in u)`）、`:211`（温度分支）、`:214`（初始 `fillSel();calc()`）。
- 复现：node 复刻 `for(const k in undefined)` → `[]`；cat=temp、f=t="" 时 `calc(100)` → 「结果 = 100.00」、`calc(1)` → 「结果 = 1.00」；按页面公式 100°F 应为 37.78、1K 应为 −272.15。
- 影响：`tools/edu/convert-area-volume.html`；五类换算中的温度整类不可用，界面无任何报错，用户会把 100°F 当成 100°C。
- 方案：给 `U`/`N` 增加 `temp:{C,F,K}` 并单独实现仿射换算（不要复用比例系数）；或显式拦截温度类别并提示“暂不可用”，同时移除该 option。

### EL-J167 结果趋势图读取带“结果 = ”前缀的展示文本，`parseFloat` 恒 NaN，图表永不出现（中，确认缺陷）
- 问题：历史记录里的“结果”字段存的是整段展示文案（`结果 = 100.0000`），图表却对该字段做 `parseFloat`，首字符为“结”即 NaN，`nums` 永远为空，`nums.length>=2` 分支不成立。
- 证据：`:213`（结果文案带前缀）、`:344-365`（`rec[rk]=res`，res 来自 `__convert_area_volumeResText`）、`:331-335`（`parseFloat(arr[j].d[rk])`）。
- 复现：node `parseFloat('结果 = 100.0000')` → NaN；连续换算 3 次后切到“结果”tab，`#convert_area_volumeChart` 仍为空。
- 影响：同页；图表 tab 形同装饰，无法查看多次换算的趋势。
- 方案：历史中单独存数值字段（如 `resultNum`），图表读数值；或先 `replace(/^结果\s*=\s*/, '')` 再 parse。

### EL-J168 工具简介只重复标题，深挖要点为空泛短句，未说明量纲覆盖与精度口径（低，确认缺陷）
- 问题：`tool-intro` 正文为“长度/重量/温度/面积/体积单位换算（内置公式）。”；深度解析三条要点均为“多类换算/公式内置/精度保留”式短语，没有列出支持的单位与四/两位小数规则，也未提示温度类别不可用（见 EL-J166）。
- 证据：`:260`（简介正文）、`:153-156`（三条短要点）、`:120`（精度与温度说明）。
- 复现：通读页面可见文本：无任何单位清单；简介与公式中的温度说明和实际功能不符。
- 影响：同页；介绍无法帮助用户判断适用量纲，SEO 正文偏薄。
- 方案：简介补“长度 7 种、重量 5 种、面积 5 种、体积 5 种、温度 3 种（暂不可用）”与精度规则；深挖换成具体算例（1 mi=1609.344 m、1 acre=4046.8564224 m²）。

### EL-J169 课程表冲突检测宣称“可视化课表”与“无冲突排课率”，页面均未实现（高，确认缺陷）
- 问题：meta/og/正文简介与公式框都承诺“输出冲突清单与可视化课表”“无冲突排课率 = 无冲突时段数 ÷ 总时段数 × 100%”，但结果区只输出 4 个统计卡与两张冲突明细表，没有任何“周次 × 节次”网格，也没有排课率数值。
- 证据：`tools/edu2/schedule-conflict.html:13`/`:16`（描述承诺可视化课表）、`:118`（正文 `data-zh` 再次承诺）、`:121`（公式含排课率与网格）、`:299-329`（结果 HTML 仅 stat-grid + 两张 table）。
- 复现：录入任意课程点“检测冲突” → 页面只出现“课程总数/教师冲突/教室冲突/冲突状态”与冲突表；全页无 canvas/svg 课表，结果区无“排课率”字段。
- 影响：同页；核心卖点缺失，用户仍需自己画课表，搜索结果描述与页面不符。
- 方案：按 day 1–7 × 节次 1–N 渲染网格，冲突格加 class 高亮；排课率按“无冲突时间片数/总时间片数”算出并放进 stat-grid；否则删掉两处承诺文案。

### EL-J170 数据表/历史/图表只在“载入示例”时写入，自建课表检测不落记录且首屏自动灌示例（中，确认缺陷）
- 问题：TBKit 包装只替换了 `loadSample`（`:497-500`），`detect()` 未被包装；用户改 textarea 后点“检测冲突”不会调用 `__schedule_conflictExtras`，数据表/历史/图表保持旧值。boot 又在 `DOMContentLoaded` 调 `loadSample()`，首屏覆盖输入并写一条示例历史；脚本尾部先跑一次空输入 `detect()`（`:336`），会排入一条“请输入…”错误 toast。
- 证据：`:497-503`（仅包装 loadSample、boot 自动载入）、`:336`（解析期空 detect）、`:270-273`（空列表错误 toast）、`:434-435`（table/diff 渲染）、`:490-493`（CSV 导出读历史表）。
- 复现：打开页 → 弹一次错误 toast，随后输入框被示例填满、历史新增 1 条；把 textarea 改成自己的 3 门课并点“检测冲突”，结果区更新但数据表/历史不动；此时导出 CSV 得到的是示例快照。node 复算示例 8 门课冲突 0（教师 0、教室 0），导出记录也是“无冲突”。
- 影响：同页；用户数据无法沉淀，“导出明细 CSV”名不副实，示例与真实数据混淆。
- 方案：把包装挂到 `detect`（或统一在 detect 末尾记录）；boot 不自动 `loadSample`（改空态 + 按钮）；首屏不要调用空输入 detect；导出改为导出当前冲突表。

### EL-J171 FAQ/引据表的重叠判据写作半开区间，与“含起止节”的实现相反（中，确认缺陷）
- 问题：FAQ 写“a.start<b.end 且 b.start<a.end”、引据表写 `[start,end)`，都是半开区间；实现 `overlap()` 用 `!(a.end<b.start || b.end<a.start)` 为闭区间，“检测规则”正文也写“起始节至结束节（含）”。同一节次（1-1）重叠时两套判据结论相反。
- 证据：`:181`（FAQ 半开公式）、`:201`（引据表 `[start,end)`）、`:145`（检测规则“含”）、`:262-265`（实现闭区间）。
- 复现：两门课同教师、星期 1、起始 1、结束 1 → 实现判冲突（`!(1<1||1<1)` 为 true）；按 FAQ 公式 `1<1` 为 false → 判无冲突。node 复算两式分别 true/false。
- 影响：同页；按 FAQ 自查排课会漏判/误判单节冲突，文档与行为不一致。
- 方案：统一为闭区间并同步 FAQ 与引据表（写成 `a.start<=b.end && b.start<=a.end`）；若采用半开区间则改实现与“检测规则”文案。

### 留存建议（tools/edu/convert-area-volume.html）
- 补齐温度三单位的仿射换算，或在 UI 明确禁用并删掉承诺文案。
- 历史/图表改为存数值字段，展示层再拼“结果 = ”前缀。
- 简介与深挖补单位清单、精度口径与真实算例。

### 留存建议（tools/edu2/schedule-conflict.html）
- 实现 week×period 网格与冲突高亮，并输出排课率。
- 把历史/表格/导出挂到 detect，取消首屏自动示例与空输入 detect。
- 统一区间为闭区间，三处文档一起改。

### 留存建议（tools/edu/countdown-5.html）
- 统计卡与 hero 统一口径（建议都含考试当天，或都在文案里注明“不含考试当天”）。
- 删除重复的公式框与第二组相关工具，补全三处空 toast 文案。

### EL-V1 「高考/考研倒计时」hero 天数与“剩余总天数”统计仍差 1，考试前一天统计为 0（中，确认缺陷，复核仍成立）
- 问题：复核 R 批 EL-J130。hero 用 `diff=Math.round((target-now)/86400000)`（含考试当天），统计用 `countDays()` 从明天起 `while(cur<target)`（不含考试当天），两者恒差 1。
- 证据：`:299`（diff）、`:304`（hero 输出 diff）、`:152`（统计卡“剩余总天数”）、`:267-278`（从明天起、`cur<target`）、`:312`（提示语用 `d.total`）。
- 复现：node 实算（今天 2026-11-04）：考试明天 → hero 1、statTotal 0、motto“距考试还有 0 天”；2 天后 → hero 2、total 1；30 天后 → hero 30、total 29（工作日 21、周末 8）；100 天后 → hero 100、total 99。
- 影响：`tools/edu/countdown-5.html`；同一屏两个“剩余天数”不一致，临近考试时统计卡显示 0 天，误导考生。
- 方案：统计改为 `total=diff`（含考试日），或让 hero 与统计共用同一计数函数，并在标签注明“不含考试当天”。

### EL-V2 「高考/考研倒计时」重复公式框/重复相关工具与三处空 toast 仍存在（低，确认缺陷，复核仍成立）
- 问题：复核 R 批 EL-J131。`statsCard` 内连续两个“📐 计算方式”卡片，第二个只重复一句话；页面尾部两组“🔗 相关工具”；`addLog`/`clearLog`/清空成功三处 `i18nText()` 无参数。
- 证据：`:157-160` 与 `:161-164`（两个 formula-box）、`:438-466` 与 `:468-496`（两组 related-tools）、`:241`、`:261`、`:263`（空 `i18nText()`）。
- 复现：grep 计数“📐 计算方式”=2、`class="related-tools"`=2；日期留空点“记录”→ `i18nText()` 返回 `undefined`，toast 文本随之变成 `undefined`。
- 影响：同页；页面冗长、toast 出现字面量 undefined。
- 方案：删掉第二个公式框与第二组相关工具；三处改为真实键（如 `i18nText('toast.需要日期')`）或直接传中文兜底。

### 承诺 vs 实际（S 批专项）
- `tools/edu/convert-area-volume.html:120`/`:121`「温度按 (值−32)÷1.8、K−273.15 换算」→ 温度类别无单位可选项，输出恒等于输入（`:207-211`）。
- `tools/edu/convert-area-volume.html:157`「示例 100°F ≈ 37.78°C」→ 页面输出 100.00（`:211`）。
- `tools/edu/convert-area-volume.html:344-350`「结果趋势图」→ 对 `结果 = …` 文本 `parseFloat` 得 NaN，图永不渲染（`:331-335`）。
- `tools/edu2/schedule-conflict.html:13`/`:16`/`:118`「输出冲突清单与可视化课表」→ 只有统计卡与冲突表，无周×节网格（`:299-329`）。
- `tools/edu2/schedule-conflict.html:121`「无冲突排课率 = 无冲突时段数 ÷ 总时段数 × 100%」→ 结果区无该数值（`:299-329`）。
- `tools/edu2/schedule-conflict.html:181`/`:201`「半开区间 a.start<b.end」→ 实现为闭区间（`:262-265`），同节次判定相反。
- `tools/edu/countdown-5.html:158`「剩余天数 = round((目标−今日)/86400000)」→ 统计卡用“不含考试当天”的 `countDays`，与 hero 差 1（`:267-278`、`:299`、`:304`）。
- `tools/edu/countdown-5.html:316-321`「累计时长 = Σ记录；学习天数 = 记录条数」→ 已实现，复核通过。
- `tools/edu2/schedule-conflict.html:227-230`「载入示例」→ 示例 8 门课冲突数为 0（教师 0/教室 0），无法演示冲突检测。

### 覆盖
- 实读 3 页：`tools/edu/convert-area-volume.html`、`tools/edu2/schedule-conflict.html`、`tools/edu/countdown-5.html`，3/3 全覆盖。
- 新增 8 条（EL-J166～EL-J171、EL-V1～EL-V2）：高 2（EL-J166、EL-J169），中 4（EL-J167、EL-J170、EL-J171、EL-V1），低 2（EL-J168、EL-V2），另附 3 组留存建议与 1 节“承诺 vs 实际（S 批专项）”。
- 07 教育/edu2 已无未提及页：`tools/edu` 45 个工具页 + `tools/edu2` 5 个工具页均已在 `edu-language.md` 或 `research-library.md` 覆盖；`tools/edu/index.html`、`tools/edu2/index.html` 为分类目录页（无 `<meta name="toolbox">`、无工具交互），不计入工具页审计。
- 复核结论：EL-J130（hero 与统计差 1）仍成立 → EL-V1；EL-J131（重复公式框/相关工具、空 toast）仍成立 → EL-V2。
- 验证边界：仅静态读源码 + `node -e` 复刻（`for…in undefined`、温度空选项恒等、`parseFloat('结果 = …')`、倒计时 hero 与 countDays 差值、示例冲突对数、半开/闭区间判定）；未做真实浏览器、移动端、英文态/繁体态、门禁、构建与线上验证；`showToast(undefined)` 的最终显示形态待浏览器确认。
