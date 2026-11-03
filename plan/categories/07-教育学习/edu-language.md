# 教育/语言 · tools/{edu,edu2,language,chinese}（~60 页）

## 已知问题
### E2. 遗留：GPA 页「加权平均权重和≠1」未系统扫（列入：输入学分权重后校验 Σw 提示）。
- 受影响：tools/edu/gpa-calculator.html、grade-weight-calculator 等

## 功能缺陷
- ✅ 目标分反推（2026-10-26）：exam-score-calculator 加「🎯 目标分反推」card（calcTarget：给定目标分反推还需做对多少题，含已达标/超满分/剩余题不足三分支，__T 双语）；verify edu 73→74、判别器 0 逃生。
- 中文页（chinese-culture/lunar）静态，缺「生辰八字/节气」交互深挖。

## 优化点
- ✅ S2 场景（2026-10-26）：exam-score-calculator 加 3 分制预设「四级 710 分制」（456 题对 → 456.0 分 vs 及格线 425）「高考 750 分制」「考研 500 分制」，labelEn 双语；verify edu 70→73、判别器 0 逃生；顺带修该页 #result EN 存量泄漏（成绩/等级/对比全 __T 化）→ OK_EN。倒计时类因铁律④（测试禁依赖当前时间）不纳入测试，未做。
- S4 分享卡：倒计时打卡卡。

## 受影响范围
- tools/edu/（47）、tools/edu2/、tools/language/、tools/chinese/

## 进度
- 🟡 续批中（S2 分制场景、目标分反推已落地；剩余：生辰八字节气深挖 / S4 打卡分享卡）

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

### EL-F3 拼音历史随每次键入落库，50 条被输入过程占满（中，确认缺陷）
- 问题：`oninput` 每敲一个字符就 `convert()`，`convert()` 末尾无条件 `saveHistory()`，输入过程产生的中间串全部成为历史记录。
- 证据：`tools/edu/pinyin-converter.html:182`（textarea `oninput="convert()"`）、`:611`（`saveHistory(input, result)`）、`:626-633`（去重后 `unshift`、上限 50）。
- 影响：同页「历史」标签；输入「中华人民共和国」一次即可能写入 7 条半截记录，把真正有用的整句记录挤出 50 条上限。
- 方案：仅在显式「转换」按钮、失焦（`change`/`blur`）或停顿 500ms 防抖后写历史；同时把去重键改为整串精确匹配并保留时间戳。

### EL-F4 无声调模式仍保留 ǹ 声调符（低，确认缺陷）
- 问题：`removeTone` 的替换表覆盖 āáǎà/ēéěè/īíǐì/ōóǒò/ūúǔù/ǖǘǚǜü，未含 `ǹ`，`嗯` 的 `ǹg` 在「无声调」「首字母」模式下去不掉声调。
- 证据：`tools/edu/pinyin-converter.html:526-528`；内存执行 `removeTone('ǹg') → 'ǹg'`，首字母模式 `charAt(0) → 'ǹ'`。
- 影响：同页；个别字在无声调/首字母输出中仍带调号，与其他字不一致。
- 方案：按 Unicode 组合符统一去调（NFD 后删除 U+0300–U+036F），或用完整拼音声调字符表覆盖 `ǹńň` 等鼻音音节。

### EL-F5 西语分音节不切分「元音+单辅音+元音」，几乎整词算一音节（高，确认缺陷）
- 问题：`splitSyllables` 在元音后遇到单个辅音时，把该辅音继续拼进当前音节，而不是「辅音归下一音节」；只有双辅音或强+强元音才触发切分，导致 `ca-sa`、`me-ses` 等全部粘连。
- 证据：`tools/language/spanish-accent-rules.html:277-356`，关键分支 `:313-317`（`current += ch` 后继续，不 push）。内存复算：`casa → casa`（1 音节）、`meses → meses`、`ciudad → ciudad`、`lápiz → lápiz`、`jamás → jamás`；仅 `perro → pe-rro`、`cantar → can-tar`、`real → re-al` 等含双辅音/ hiatus 的词偶然正确。
- 影响：`tools/language/spanish-accent-rules.html`；核心「音节划分 + 重音位置」结论对绝大多数单词错误，页面规则示例 `casa → CA-sa` 与实际输出自相矛盾。
- 方案：按西语音节规则重写：元音间单辅音归后一音节；辅音连缀按合法 onset（pr/br/tr/bl/cl/fl/pl/gl/fr/dr/cr/gr + ch/ll/rr）整体归后；其余在两个辅音间切分；补 `casa/papel/meses/ciudad/lápiz/están/jamás/espárrago` 回归用例。

### EL-F6 西语「重音符号判断」对所有无符号词一律判「不需要」，错拼词被放行（中，确认缺陷）
- 问题：无书写重音时只按词尾推导默认重音，不做「该重音是否与默认位置一致」的比对，两个分支都固定输出「不需要重音符号 ✓」。
- 证据：`tools/language/spanish-accent-rules.html:396-413`（`needsAccent=false` 两分支写死）、`:441-457`（渲染绿字结论）。复算：`cafe`（应为 café）音节切分后判「不需要重音符号」；`camion`（应为 camión）同理。
- 影响：同页；拼写检查场景会把漏标重音的词判为正确，学习者得到反向反馈。
- 方案：把「无符号词的实际重音位置」与「规则默认位置」显式比较；若用户输入形态无法判定，改为中性提示「按规则重音在第 N 音节；若实际重音不同需补符号」，不输出绿色「✓ 不需要」。

### EL-F7 西语清空输入不清旧结果（低，确认缺陷）
- 问题：`analyze()` 在 `word` 为空时直接 `return`，结果区保留上一次分析。
- 证据：`tools/language/spanish-accent-rules.html:366-369`；对比同批 `reading-speed-calculator` 同类缺陷（本文件前文已记）。
- 影响：同页；用户删空输入后仍看到旧单词的音节与重音结论，误以为是空输入的结果。
- 方案：空输入时清空 `#result` 并给出「请输入单词」提示，并加「输入→清空」交互用例。

### EL-F8 艾宾浩斯「今天」状态永不命中，当日复习点显示「待复习」（中，确认缺陷）
- 问题：`startDate` 读自 `<input type=date>`，`new Date('YYYY-MM-DD')` 按 UTC 零点解析，本地（UTC+8）得到当日 08:00；与 `today`（本地零点）比较既非「小于」也非「相等」，永远落入 else。
- 证据：`tools/edu/ebbinghaus-curve.html:351-354`（读日期）、`:363`（today 置零）、`:373-375`（三分支）。Asia/Shanghai 内存复算：start=`2026-11-03` → `date=2026-11-03 08:00`，`date.getTime()!==today.getTime()`，状态输出「待复习」而非「📌 今天」。
- 影响：`tools/edu/ebbinghaus-curve.html`；学习当天生成的计划，首个复习点永远不标「今天」。在 UTC 负偏移时区还会整体前移一天。
- 方案：统一用「本地日历日」比较（`getFullYear/getMonth/getDate` 组装或 `setHours(0,0,0,0)` 后比较），不要依赖 `new Date('YYYY-MM-DD')` 的 UTC 解析；补 UTC+8 / UTC-5 两个时区用例。

### EL-F9 艾宾浩斯保持率与间隔天数错配（中，确认缺陷）
- 问题：「记忆保持率」按数组下标取值，而数组取自艾宾浩斯「20 分钟/1 小时/1 天/6 天」实验值；下标对应的是自定义复习序号，不是经过天数。
- 证据：`tools/edu/ebbinghaus-curve.html:337-341`（间隔表）、`:364`（`retention=[100,58,44,36,33,28,25,23,22,21]`）、`:377`（`ret=retention[i]`）。标准模式输出 `0天→100%, 1天→58%, 2天→44%, 4天→36%, 7天→33%, 15天→28%, 30天→25%`；而页内引据 `:281` 明写「1 天后 ≈34%、6 天后 ≈25%」，1 天列与引据相差 24 个百分点。
- 影响：同页；复习日程的「保持率」列不可信，与同页标准引据自相矛盾。
- 方案：按 `R=e^(−t/S)` 或按经过天数查表（20min/1h/1d/6d/30d），不要用序号下标；表头改为「预计保持率（示意）」并给出取数依据。

### EL-F10 艾宾浩斯清空开始日期输出 NaN 表格（低，确认缺陷）
- 问题：`generate()` 不校验日期有效性，`new Date('')` 为 Invalid Date，后续 `getFullYear()` 全为 NaN，状态比较恒 false。
- 证据：`tools/edu/ebbinghaus-curve.html:353-378`。内存复算 `new Date('')` → `dateStr='NaN-NaN-NaN'`，状态「待复习」。
- 影响：同页；清空日期后表格出现 `NaN-NaN-NaN`，且仍显示绿色「待复习」。
- 方案：`isNaN(date.getTime())` 时清空结果并提示选择日期；`savePlan` 的空日期分支同样应给出可见提示（`:391` 目前 `i18nText()` 无 key，toast 为静默）。

### EL-F11 笔画统计「平均笔画」分母含未收录字（中，确认缺陷）
- 问题：`showMultipleChars` 平均笔画用 `chars.length` 作分母，而 `total` 只累加已收录字；未收录字越多，平均值被拉得越低。
- 证据：`tools/edu/chinese-stroke-counter.html:442-470`，平均式在 `:470`。内存复算输入「一二郁郁」：总字数 4、总笔画 3、已收录 2，页面平均 `0.8`，仅按已收录应为 `1.5`。预设「张伟」（`:666`）两字均未收录（`strokeMap` 无「张」「伟」），输出总笔画 0 / 平均 0。
- 影响：`tools/edu/chinese-stroke-counter.html`；批量统计的均值失真，且官方预设示例直接落在未收录区。
- 方案：平均按 `found` 计并标注「按已收录 N 字计算」，未收录字单列清单；预设换成字表内词（如「学习」「国家」），或补「张/伟」等姓名高频字。

### EL-F12 笔画「按笔画查找」上限 10 画，11–16 画已收录字不可达（中，确认缺陷）
- 问题：下拉框只生成 1–10 画，`strokeMap` 实际收录到 16 画，11 画以上字符无法通过筛选器检索，只能靠手动输入。
- 证据：`tools/edu/chinese-stroke-counter.html:172-182`（option 1–10）、`:358-389`（字典）、`:482-484`（按值筛选）。内存统计：203 字、最大 16 画；11 画以上共 23 字（`猫11 短12 新13 瘦14 黄11 蓝13 绿11 黑12 紫12 橙16 唱11 跑12 跳13 喝12 雪11 雷13 森12 想13 慢14 善12 假11 错11 道12`）。
- 影响：同页「笔画知识」检索功能与数据范围不一致，用户选 10 画后无法理解为何看不到「短/新/橙」。
- 方案：按字典最大笔画动态生成 option（或补 11–16 画），并在列表为空时提示「当前仅收录 1–N 画」。

### EL-F13 笔画页深度解析宣称「笔顺拆解」，实现只有总笔画（中，确认缺陷）
- 问题：页内标题/首屏文案承诺「按笔顺拆解、展示笔画组成顺序」，代码只有总笔画数与按画筛选，无任何笔顺序列数据或渲染。
- 证据：`tools/edu/chinese-stroke-counter.html:299`（`深度解析：统计汉字的总笔画数并按笔顺拆解`）、`:303`（`笔顺拆解：展示笔画组成顺序`）、`:309-310`（数据来源宣称「笔顺规范」）；`strokeMap` 为 `字→数字`（`:358-389`），无笔顺字段，`showSingleChar`（`:421-440`）只渲染 `N 画`。
- 影响：同页；搜索摘要/深度解析与真实能力不符，用户按「笔顺」预期进入后拿不到结果。
- 方案：二选一——补笔顺数据（每字笔画序列）并渲染，或把深度解析文案改为「总笔画统计与按画筛选」，删除「笔顺拆解/笔顺组成顺序」表述。

### EL-F14 五十音练习只认单一罗马音，常见拼写被判错（高，确认缺陷）
- 问题：`checkPractice()` 用 `ans === currentPracticeKana.romaji` 精确相等，题库每假名只存一种拼写，且混用平文/训令式（し=shi、ち=chi、つ=tsu 用 Hepburn，ぢ=di、づ=du 用训令）。
- 证据：`tools/language/language-toolkit.html:707-759`（题库）、`:831-849`（判定，`:837` 精确相等）。内存复算 106 个假名：`し` 仅 `shi`（输入 `si` 判错）、`ち` 仅 `chi`（`ti` 判错）、`つ` 仅 `tsu`（`tu` 判错）、`ふ` 仅 `fu`（`hu` 判错）、`じ` 仅 `ji`（`zi` 判错）、`ぢ` 仅 `di`（`ji` 判错）、`づ` 仅 `du`（`zu` 判错）、`を` 仅 `wo`（`o` 判错）、`ゐ` 仅 `wi`。
- 影响：`tools/language/language-toolkit.html`「日语五十音图-练习」；按词典常见拼写输入会被判错，入门练习的挫败感直接来自判分错误。
- 方案：每题维护可接受答案集合（`shi|si`、`chi|ti`、`tsu|tu`、`fu|hu`、`ji|zi`、`ji|di`、`zu|du`、`wo|o`），统一标注采用 Hepburn；`ゐ/ゑ` 明确标为历史假名或移出练习题库。

### EL-F15 五十音练习无「已答」锁，1.2 秒内重复回车重复计分（中，确认缺陷）
- 问题：答完题后输入框未立即清空，`currentPracticeKana` 在 `setTimeout(nextPractice,1200)` 前仍有效，`checkPractice()` 没有 answered 守卫，连按回车会把同一题重复计入总数与正确数。
- 证据：`tools/language/language-toolkit.html:831-849`（无守卫、`:848` 延时换题）、`:823-830`（换题时才清空输入）。对照同项目 `ipa-practice.html:460-462` 有 `quizAnswered` 守卫。
- 影响：同页；正确率统计被按键噪声污染，练习结果不可用。
- 方案：加 `answered` 标志并在答题瞬间清空/禁用输入，1.2 秒后再解锁换题；或改为「答完立即进入下一题，仅保留反馈 1.2 秒」。

### EL-F16 首字母缩写对中文只取整段首字（中，确认缺陷）
- 问题：中文分支按空白分词后只取 `w.charAt(0)`，没有逐字取拼音首字母；输入框与标签却宣称「中英文均可」，占位示例还给出「中华人民共和国」。
- 证据：`tools/language/language-toolkit.html:858-884`（中文分支 `:876-882`，注释自述「简化为取字本身/取第一个字」）、`:320`（占位「或：中华人民共和国」）。复算「中华人民共和国」→ 输出「中」，明细「中华人民共和国 → 中」。
- 影响：同页「首字母缩写生成器」；中文用户得到 1 个字而非缩写，功能与占位示例完全不符。
- 方案：中文按字取拼音首字母（复用页面已有拼音能力或内置常用字表），过滤「的/了/和」等虚词；若暂不做，则把输入标签与占位改为「仅支持英文/拉丁字母」。

### EL-F17 生肖年份越界取模为负，结果区抛 TypeError 不更新（中，确认缺陷）
- 问题：`getZodiac(y)` / `getGanZhi(y)` 直接用 `(y-4)%12`、`(y-4)%10`，y<4 时负数取模得到负下标，数组返回 `undefined`，`calc()` 取 `z.a` 抛错；输入框只有 `min/max` 属性，`calc()` 没有 JS 校验。
- 证据：`tools/edu/chinese-zodiac.html:155`（`min=1900 max=2100` 仅属性）、`:350-351`（取模）、`:355-356`（`z.a` / 干支拼接）。Node 复算：`getZodiac(3)`、`getZodiac(0)`、`getZodiac(-1)` 均为 `undefined`；输入 1/2/3 时 `z.a` 抛 TypeError，`:380` 的结果写入不会执行。
- 影响：`tools/edu/chinese-zodiac.html`；清空后逐位键入（先入「1」）或输入 1900 以前年份时页面报错、结果区停留在旧内容。
- 方案：入口统一 clamp 到 1900–2100 并对非法值提示；取模改用 `((y-4)%12+12)%12` 防御；`calc()` 增加 `Number.isInteger` 与范围校验。

### EL-F18 生肖只按公历年换算，未实现页内宣称的春节边界（中，确认缺陷）
- 问题：深度解析与 FAQ 均称「以农历正月初一为界，年初出生可能属上一年生肖」，但 `calc()` 只接收四位年份，没有农历/春节日期表，任何 1 月 1 日–除夕出生者都会得到当年生肖。
- 证据：`tools/edu/chinese-zodiac.html:276`（FAQ 边界说明）、`:350`（仅按年份取生肖）、`:353-358`（`y=parseInt(year)`，无月日）。示例：2024-01-15 出生按本工具为「龙」，按春节边界应为「兔」（2024 春节 2 月 10 日）。
- 影响：同页；民俗/年龄属相查询在年初人群上结论错误，且与自身说明不一致。
- 方案：增加「出生日期（可选）」输入并内置 1900–2100 春节日期表（纯前端静态数据），按日期定生肖；无日期时结果区显著标注「按公历年粗算，年初出生请补日期」。

### EL-F19 IPA 音标示例把「茶 chá」挂到 /i:/（低，确认缺陷）
- 问题：`/i:/` 的示例列表混入中文「茶」，且标注 `chá (类似)`；茶韵母为 /a/，与闭前不圆唇长元音 /i:/ 无对应关系，其余示例均为英语词。
- 证据：`tools/language/ipa-practice.html:279`（`'i:'` 条目 `examples` 第 4 项 `{w:'茶',tr:'chá (类似)'}`）；同页 `:281` 对 `/e/` 描述为「半开前不圆唇」，而 /e/ 为半闭（close-mid），术语亦偏差。
- 影响：同页「IPA 音标练习」；音标卡与发音示例错配，中文学习者会被误导。
- 方案：删除非对应语言的示例，只保留同音位英语词（see/machine/he）；`/e/` 描述改为「半闭前不圆唇」，并按 IPA 官方表校对全部 `desc`。

### EL-F20 德语题库「Augen(复数)」与「Auge(单数)」同义并存，答题判定歧义（中，确认缺陷）
- 问题：题库把复数 `Augen` 作为独立词条（die/眼睛），同时又收 `Auge`（das/眼睛）；测验抽到 `Augen` 时正确答案为 die，但学习者按「眼睛=das Auge」作答会被判错。另有重复词条 `Haus`（先 der 后 das，靠「保留最后一条」掩盖）与错误注释「der Haus (dialect)」。
- 证据：`tools/language/german-gender-quiz.html:403`（`Augen/die/眼睛`）、`:470`（`Auge/das/眼睛`）、`:428-429`（`Haus` der + das 两条）、`:498-503`（按小写词保留最后一条）。内存复算：原始 187 条、去重后 184 条；重复词 `mädchen×2 haus×2 buch×2`；去重后同时存在 `Augen/die/眼睛` 与 `Auge/das/眼睛`。
- 影响：`tools/language/german-gender-quiz.html`；测验答案歧义，且重复/错误条目依赖去重顺序，后续改序即出错。
- 方案：题库只收单数名词（复数统一在详情里展示 `die Augen`），删除 der Haus 伪条目与完全重复条目；加载时校验「同词同义不同性」并报警，补单测。

### 留存优化
- `tools/edu/pinyin-converter.html`（低，建议）：把「多音字提示」升级为可点击选择读音的卡片，用户选定后即时重算整句，并把该词加入本地「我的读法」表，避免只提示不解决。
- `tools/edu/ebbinghaus-curve.html`（低，建议）：在修好日期比较后，提供「复制日程 / 导出 .ics」纯前端文本，方便用户带入系统日历；不新增后端与通知权限。
- `tools/language/language-toolkit.html`（低，建议）：五十音练习增加「本次易错假名」本地清单与一键重练，配合可接受答案集合，直接复用现有 `getAllKana` 数据，不重复建设。
- `tools/edu/chinese-stroke-counter.html`（低，建议）：补「最近查询」与收藏字卡（现有 `saveHistory` 已存 20 条，只差展示入口），并在未收录字处提供「反馈缺字」的本地复制文案。

### 续查覆盖
- 本批共核查 8 页：`tools/edu/pinyin-converter.html`、`tools/edu/ebbinghaus-curve.html`、`tools/edu/chinese-zodiac.html`、`tools/edu/chinese-stroke-counter.html`、`tools/language/spanish-accent-rules.html`、`tools/language/german-gender-quiz.html`、`tools/language/ipa-practice.html`、`tools/language/language-toolkit.html`。
- 新增 20 条问题（高 3 条：EL-F1 / EL-F5 / EL-F14；中 13 条；低 4 条）与 4 项留存建议。全部证据来自源码阅读与 Node 内存复算；真实浏览器、英文态、移动端、门禁与线上页面均未验证。
