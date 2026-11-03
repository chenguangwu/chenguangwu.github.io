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

## 2026-11-03 续查（并行批 J）

> 方法：逐页读源码 + Node 内存复算（抽取页面内函数/字典求值、按页面判定逻辑模拟输入），未做浏览器、英文态、移动端、门禁或线上验证。编号 `EL-J*` 为本批新增，未与既有 E2 / S2 / S4 / EL-F* 重号。

### EL-J1 拼音打字练习实为汉字照抄，拼音输入必然全错（高，确认缺陷）
- 问题：页面标题、英文副标题、深挖示例均宣称「拼音打字 / Practice pinyin typing / 显示「中国」输入 zhongguo 判对」，但判定逻辑是把用户输入的**最后一个字符**与当前汉字逐字比对，页面没有任何拼音/音节数据。
- 证据：`tools/edu/pinyin-typing-practice.html:243`（深挖示例「输入 zhongguo 判对」）、`:368`（按 `ch === inputValues[i]` 着色）、`:391-397`（`newChar = val[val.length-1]`，`if (newChar !== currentText[currentIndex]) errors++`）。Node 按该逻辑模拟样例「床前明月光，疑是地上霜。…」：逐键输入 `zhongguo` 8 个字母 → `currentIndex=8`、`errors=8`、正确率 0%。
- 影响：`tools/edu/pinyin-typing-practice.html`；拼音用户按页面宣称的方式输入永远得 0 分，核心「打字速度/正确率」统计对目标用户不可用。IME 组合态期间 `input` 事件也会把拼音字母计入错误（需真机 IME 验证，标为待验证）。
- 方案：二选一——① 为每条样例逐字标注拼音，按音节比对（接受无声调/同音变体），并加 `compositionstart/compositionend` 守卫，组合态不计错；② 明确改名为「汉字照抄练习」，删除「拼音打字 / zhongguo 判对」等宣称及英文 `Practice pinyin typing` 文案。落地后用内存用例断言 `zhongguo → 100%` 或断言页面无拼音宣称。

### EL-J2 错误数只增不减，退格后准确率与速度可为负（中，确认缺陷）
- 问题：退格只回退 `currentIndex`，不回退 `errors`；`updateStats`/`finishTyping` 仍用累计错误数计算正确率与速度。
- 证据：`tools/edu/pinyin-typing-practice.html:402-404`（`else if (val.length < currentIndex) currentIndex = val.length;`，无 `errors--`）、`:412-414`（`currentIndex - errors`）、`:431-434`（完成 toast 未做 `Math.max`，直接输出负值）。Node 模拟两字文本「你好」：输 `x`（错 1）→ 退格 → 输 `y`（错 2）→ 输 `z`（错 3）完成，得 `(2-3)/2 = -50%`，速度同为负。
- 影响：同页统计与完成提示；中间打错再改对的用户会被持续扣分，甚至看到负正确率/负速度，数据不可信。
- 方案：记录每个位置的首次错误标记（数组 `errorFlags[i]`），退格时按标记回退；或在 `currentIndex` 减小时同步修正 `errors`。显示前统一 `Math.max(0, …)` 并补「打错→退格→改对」用例。

### EL-J3 一次 input 事件只记 1 字，粘贴/长输入进度失真（中，确认缺陷）
- 问题：输入处理只取 `val` 末字符并 `currentIndex++`，不按新增长度逐字推进；粘贴整句或语音/输入法一次上屏多字时，进度只前进 1。
- 证据：`tools/edu/pinyin-typing-practice.html:389-397`（`if (val.length > currentIndex) { … currentIndex++ }`，没有循环）。Node 复算：把 12 字「床前明月光，疑是地上霜。」一次性粘贴，得 `currentIndex=1、errors=1`（应推进 12）。
- 影响：同页；粘贴/批量输入后进度条、速度、正确率全部失真，且比对只覆盖最后一个字。
- 方案：保存上一次输入值，按 `val` 与旧值的差异逐字处理（或对所有新增字符循环比对）；屏蔽粘贴（`paste` 事件提示逐字输入），并明确说明不支持整段粘贴。

### EL-J4 英语单词测试题量输入负数得到 95 题（中，确认缺陷）
- 问题：题量只做了 `Math.min(parseInt(...)||20, vocab.length)`，没有下限与整数校验；输入负数时 `slice(0, 负数)` 表示「去掉末尾 N 条」，反而生成接近全量的题目。
- 证据：`tools/edu/english-vocabulary.html:193`（`min="5" max="100"` 仅是 HTML 属性，手输不受约束）、`:451-453`（`const count = Math.min(parseInt(...)||20, vocab.length); questions = shuffle(vocab).slice(0, count)`）。Node 复算 cet4（100 词）输入 `-5` → `count=-5` → `slice(0,-5).length=95`；输入 `0`/空 → 20；输入 `200` → 静默截为当前词库长度（cet4 为 100）。
- 影响：同页；用户输入 `-5` 后界面显示「95 题」且无提示，与「5–100 题」预期不符，也拉长测试时长。
- 方案：入口校验 `Number.isInteger(n) && n>=5 && n<=vocab.length`，非法时提示并回填默认值；把题目数量显示在开始面板。

### EL-J5 选项判对用 endsWith，多个选项被同时标绿（中，确认缺陷）
- 问题：答错后通过 `button.textContent.endsWith(q.answer)` 反查正确选项；选项文本形如「A. 容纳；适应」，只要某个错误选项的释义以正确答案结尾，就会与正确项一起被标绿。题库还存在同一测试内两条同释义词条，形成两个完全相同的选项。
- 证据：`tools/edu/english-vocabulary.html:503`（`buttons.forEach(b => { if (b.textContent.endsWith(q.answer)) … })`）；toefl 块 `:414`（`accommodate` → `容纳；适应`）与 `:420`（`adapt` → `适应`）同处一词库，Node 复算 `'B. 容纳；适应'.endsWith('适应') === true`，抽到 `adapt` 时 A、B 两项同时判对。另 cet6 块 `:398` 与 `:404` 均为 `{m:'极度痛苦'}`（agony / anguish），同一题可出现两个文本相同的选项。
- 影响：`tools/edu/english-vocabulary.html`；错题反馈会同时点亮两个「正确答案」，学习者无法判断哪个才对；同释义题本身也是歧义题。
- 方案：判分改为按选项索引（`answer(index, correctIndex)`），不比对文本；抽题时对同义释义去重（同一 `m` 只保留一词），或从选项中剔除与正确答案释义相同的干扰项。补「adapt vs accommodate」与「agony vs anguish」两条用例。

### EL-J6 生词本只展示不可复习，历史记录无任何入口（中，确认缺陷）
- 问题：文案承诺「生词可存入生词本循环复习」，实际生词本只有列表与清空，不能从生词本出题；`vocab-history` 每局写入却没有任何展示组件。公式框还宣称「未作答记入 skip 并汇总未作答数」，但页面没有跳过按钮，`skip` 只可能为 0。
- 证据：`tools/edu/english-vocabulary.html:171-172`（skip/循环复习文案）、`:544-546`（`vocab-history` 只写不读）、`:607-617`（加入生词本）、`:619-637`（只渲染列表 + 清空）、`:199`（唯一入口「查看生词本」）。全文件搜索 `vocab-history` 仅出现在写入处。
- 影响：同页；「生词本循环复习」与「历史」两个学习闭环均落空，用户只能反复查看静态列表。
- 方案：增加「用生词本出题」模式（复用 `startQuiz`，词源改为 wordbook）与历史面板（读 `vocab-history`）；或者在文案中删除循环复习与未作答统计，只保留「生词本查看」。

### EL-J7 单词学习「认识」自动塞进收藏，收藏无法移除（中，确认缺陷）
- 问题：标记「认识」时无条件把当前词 push 进 `vocab_fav`；「⭐收藏」分类直接读该数组，且页面没有任何取消收藏入口。收藏从「用户主动标记」退化为「所有点过认识的词」。
- 证据：`tools/language/vocabulary-builder.html:399-403`（`if (status === 'known') { … favs.push(state.current.w); setFav(favs); }`）、`:355-362`（fav 分类按 `favs.includes(w.w)` 组池）。全文件无 `removeFav`/`unfav`/取消收藏逻辑。
- 影响：同页；收藏列表随学习进度无限增长、无法清理，⭐分类失去筛选意义；误点「认识」也无法纠正。
- 方案：解耦两个状态——收藏改为卡片上的显式星标开关（可增可删），`known` 只写 `vocab_progress`；⭐分类提供「移出收藏」按钮，并在统计里区分「已掌握」与「已收藏」。

### EL-J8 单词学习宣称按遗忘曲线排下次复习，实际仅随机抽卡（中，确认缺陷）
- 问题：深度解析明确「新词第 1/2/4/7/15 天复习」「工具按正确率动态推下次复习日」，公式表也列「复习间隔按遗忘曲线递增」；实现只有随机抽词 + 60% 偏向 unknown，没有时间戳、间隔、到期队列。
- 证据：`tools/language/vocabulary-builder.html:227`、`:231`、`:250`（宣称）；`:353-386`（`pickWord` 仅 `Math.random()` 抽池，`progress` 只存 `known/fuzzy/unknown`，无 `nextReview`/`due`/`interval` 字段）。全文件搜索 `nextReview|interval|due|复习日|遗忘曲线` 仅命中宣本文案。
- 影响：同页；学习者按「今日该复习哪些」的预期使用，得到的却是随机抽词，教学承诺与行为不符。
- 方案：在 `vocab_progress` 中记录 `lastSeen/interval/ease`，按 1/2/4/7/15 天计算 due，增加「今日待复习 N」入口；若不做，删除遗忘曲线/动态排程表述，改为「随机抽卡 + 自评」。

### EL-J9 连续天数按 UTC 日期，本地日界前后各错一次（中，确认缺陷）
- 问题：`today` 取 `toISOString().slice(0,10)`（UTC 日历日），而用户感知的「一天」是本地日历日。在 UTC+8，凌晨 0–8 点的打卡会落到前一 UTC 日；同一本地日上午 8 点前后又会落到不同 UTC 日，导致连续天数同日 +1、跨日不 +1。
- 证据：`tools/language/vocabulary-builder.html:426-441`（`:427` UTC 日期、`:431-434` 用 `new Date(last)` 求差）。Asia/Shanghai Node 复算：本地 `11-02 07:30` → UTC `11-01`，本地 `11-02 08:30` → UTC `11-02`，`diff===1` → 同一天 `days` 从 1 变 2；本地 `11-02 23:30` → UTC `11-02`，本地 `11-03 00:30` → UTC `11-02`，`streak.last===today` 直接 return，跨日不增。
- 影响：同页「连续学习天数」；时区偏移下统计既可能虚高也可能断签，长期激励数据不可信（与 EL-F8 同类，但此处是本地日界而非日期解析）。
- 方案：统一用本地日历日（`getFullYear/getMonth/getDate` 拼 `YYYY-MM-DD`，或 `toLocaleDateString('sv-SE')`），差值按本地零点计算；补 UTC+8 两个边界用例（07:30/08:30、23:30/00:30）。

### EL-J10 成语接龙拼音模式用 undefined===undefined 放行，且缺拼音即断局（高，确认缺陷）
- 问题：拼音模式把「首字拼音」与「当前字拼音」直接做 `===` 比较；当两字都不在 `PINYIN_MAP` 时得到 `undefined === undefined` 为真，任意无拼音字都能冒充正确读音。用户答完后，若**答案末字**没有拼音，候选词直接置空并结束游戏，即使库中存在该字开头的成语。
- 证据：`tools/language/idiom-solitaire.html:631-633`（`inputPy === targetPy`）、`:645-657`（`nextPy ? getIdiomsByStartPinyin(nextPy) : []` → `candidates.length===0` 即 `endGame`）、`:581`（缺拼音显示「拼音: ?」）、`:292`（IDIOM_DB）、`:425`（PINYIN_MAP）。Node 统计：903 条成语、552 个不同末字，其中 261 个（47.3%）无拼音；15 条成语首字无拼音。可复现例：当前字「力」（无拼音，提示 ?）→ 提交「刻骨铭心」（首字「刻」也无拼音）被判定正确；用户答「自食其力」（首字 zi 匹配）后，末字「力」无拼音 → 候选为空 → 提示「没有可接的成语」并结束，但库中「力不从心」实际存在（同类可复现 11 例）。
- 影响：`tools/language/idiom-solitaire.html` 拼音模式；既可被无拼音字「蒙对」，也会在仍有合法接龙时提前判负，模式基本不可玩。
- 方案：比较前先判双方拼音都存在，任一缺失则回退为**汉字精确匹配**；候选改为「拼音候选 ∪ 同字候选」，`nextPy` 缺失时仍按 `nextChar` 取词，不得直接结束；最彻底是为全部入库字补齐拼音并加「末字有候选」的数据断言。

### EL-J11 成语库含重复条目与非成语短语，计分权重失真（低，确认缺陷）
- 问题：词库直接以数组存放，存在完全重复的成语（同一随机池中被抽中两次，权重翻倍），也混入 3–5 字非四字短语，用户提交这些短语会被当作「成语」判对。
- 证据：`tools/language/idiom-solitaire.html:292-424`（`IDIOM_DB`）。Node 复算：共 903 条、去重后 888 条（15 条重复，如「神出鬼没」「水落石出」「暗度陈仓」「一针见血」各 ×2）；5 条非四字：`试金石`、`露马脚`、`工欲善其事`、`欲速则不达`、`治标不治本`；`pickRandomIdiom`/`candidates[random]`（`:543-545`、`:659`）按数组下标抽取，重复条目被等概率放大。
- 影响：同页；出题分布与「常用成语库」定位不符，接受非成语答案削弱判对可信度。
- 方案：加载时按 `Set` 去重或直接清理数据；把词库限定为四字成语，或明确标注「含常用熟语」并在 UI 分开；加数据断言「长度=去重长度、每条 4 字」。

### EL-J12 语法检查 `做?坐?` 空匹配，任意文本刷出 N+1 条「字词」问题（高，确认缺陷）
- 问题：规则 `做?坐?` 两个字符都可选，正则可在任意位置匹配空串；`matchAll` 对零长度匹配逐位置推进，于是文本每个字符位置都产出一条「注意做/坐区分」，问题列表被空 `<mark>` 卡片淹没。
- 证据：`tools/language/grammar-checker.html:279`（`{ p: /做?坐?/g, … }`）、`:304-318`（`for (const m of text.matchAll(r.p))` 收集 `m[0]`）、`:330`（`i.ctx.replace(i.match, '<mark…>…</mark>')`，`i.match=''` 时只在卡片开头插空标记）。Node 复算：页面自带 73 字默认文本 → **74 条**问题、`match` 全为空串（index 0…73）；输入「你好」→ 3 条。
- 影响：`tools/language/grammar-checker.html`；`s-issues` 永远为「字符数+1」，任何干净文本都被判有几十处问题，核心检查结论不可用。
- 方案：删除该规则或改为明确的误用词表（如「做/坐 + 具体搭配」）；在收集循环加 `if (!m[0]) continue;` 作为兜底。补「干净文本 → 0 问题」与「你好 → 0 问题」断言。

### EL-J13 语法检查宣称的密度分级/最小编辑距离未实现，「的地得」「在再」规则按字面串匹配（中，确认缺陷）
- 问题：公式框写明「问题密度 = 问题数 ÷ 总句数」「<0.5 良好 / 0.5–1.5 局部修订 / >1.5 整体润色」「改写建议按最小编辑距离优选」，`check()` 只统计条数，从不计算密度、无分级、无编辑距离。中文规则 `/的地得(?=[一-龥])/`、`/在再/g` 匹配的是三个字连续出现或「在再」相邻，正常用法（单独一个「的/地/得」或「在/再」）永远不触发。
- 证据：`tools/language/grammar-checker.html:166`（宣称）、`:278`（`的地得` 需三字连写且后接汉字）、`:280`（`在再` 需两字相邻）、`:296-320`（只有 `chars/words/sentences/issues` 四个统计，无密度）、`:298`（句数按标点串计数，无句末标点时偏少）。Node 复算「他很开心地笑了。」「她跑得很快。」「这是我的书。」均无对应规则命中（只剩 EL-J12 的空匹配噪声）。
- 影响：同页；分级结论、改写建议均无实现支撑，「的地得/在再」这两条最常用的中文检查形同虚设，用户以为工具能查而实际查不出。
- 方案：实现并展示 `issues/sentences` 密度与三档结论（或删除该段宣称）；把中文规则改成上下文匹配（「的+名词」「地+动词」「得+补语」至少做词性近似/搭配表），做不到就明确标为「关键词提示，不判断对错」；句数改为按句末标点计数并处理无句末标点。

### EL-J14 语法检查结果用 innerHTML 拼接原文，输入 HTML 会被执行或吞掉（中，确认缺陷）
- 问题：问题卡片把用户原文 `ctx` 直接插入 `innerHTML`，并只对 `match` 做字符串 `replace`；输入含 HTML 标签时会被浏览器解析执行（自注入），且 `replace` 只替换首个出现、空匹配时插入空标记。
- 证据：`tools/language/grammar-checker.html:327-332`（`` `${i.ctx.replace(i.match, `<mark …>${i.match}</mark>`)}` `` 写入 `el.innerHTML`）、`:309-317`（`ctx/match` 直接来自 textarea）。示例输入 `<img src=x onerror="alert(1)">` 会生成真实 `img` 节点；`i.match=''` 时每个卡片开头多一个空 `<mark>`。
- 影响：同页；纯本地工具虽无第三方数据，仍属自 XSS/渲染破坏——原文中的 `<div>`、`<script>` 等会被吞掉或改写，用户看不到真实文本。
- 方案：结果区改用 DOM 构建：文本节点 `textContent` 渲染原文，命中区间用 `document.createElement('mark')` 拼接；禁止把用户输入拼进 `innerHTML`；`match` 为空时跳过高亮。

### EL-J15 汉字查询字库仅 20 字，深挖示例「曦」查不到，多音字/Unicode 宣称均未实现（高，确认缺陷）
- 问题：字库注释与文案自称「精选 200+ 汉字」，实际只有 20 个字；深挖示例查询「曦」、FAQ 举例「行」均不在库中，直接返回「未收录」。介绍还宣称输出「字形结构」「Unicode / 郑码」，实际结果卡只有拼音/部首/总笔画/五笔，且 `pinyin` 是单一字符串，无法表示多音字。
- 证据：`tools/chinese/chinese-character.html:283-345`（`charDB`，Node 复算键为 `汉字中国学生日月年人爱家好心意你我他她时`，共 20 个）、`:235`（FAQ/深挖示例「曦」xī、20 画、U+66E6）、`:238`（「行」多音字说明）、`:363-366`（输出字段仅四项）、`:551-553`（介绍宣称字形结构与 Unicode）、`:166`（formula-desc 同样宣称 Unicode/输入法编码）。Node 复算 `'曦' in charDB === false`、`'行' in charDB === false`。
- 影响：`tools/chinese/chinese-character.html`；搜索摘要引导的示例一查即空，多音字与编码能力不存在，用户按「查字典」预期使用会反复碰壁。
- 方案：扩充到常用字（至少一级字表 3500，或明确保留示例并改文案）；`pinyin` 改为数组 `[{py, sense}]` 支持多音；输出补 `codePointAt().toString(16)`（Unicode）与结构字段，或删除相关宣称。补「曦/行」两条回归。

### EL-J16 汉字查询笔画/部首数据错误：「汉」13 画、「爱」13 画、「国」部首标「玉」（高，确认缺陷）
- 问题：字库把简体「汉」录成 13 画并配 13 步笔顺，「爱」录成 13 画（接近繁体「愛」的笔画数）；「国」部首写成「玉」。空白输入默认查询「汉」，所以首屏展示即为错误数据。
- 证据：`tools/chinese/chinese-character.html:285`（`'汉': strokes:13`，`strokesOrder` 却是 13 项「点、点、提、竖、横折钩…」，与简体「汉」的 5 画「点、点、提、横撇、捺」不符）、`:315`（`'爱': strokes:13`，简体规范 10 画）、`:294`（`'国': radical:'玉'`，规范部首「囗」）、`:354`（空值 `|| '汉'`）。Node 复算：汉 13/部首氵、爱 13、国 8/部首玉。
- 影响：同页；查字/识字/书法核对的核心数据错误，且默认字与笔顺序列一起错，教学误导。
- 方案：按《通用规范汉字表》修正笔画（汉 5、爱 10），「国」部首改「囗」；对 `strokesOrder` 与 `strokes` 做一致性断言（`split('、').length === strokes`），不一致即视为待补，不要展示错误序列；补常用字数据回归。

### EL-J17 笔顺表演示 8 字多处错误，列表条数与「合计笔画」自相矛盾（高，确认缺陷）
- 问题：内置 8 个字的笔顺/笔画几乎逐条可疑：把「永」列成 8 画 8 步（规范 5 画），「我」列 5 步（规范 7 画），「学」列 10 步却写「（11画）」（规范 8 画），「生」列 6 步却写「（5画）」（规范 5 画），「想」只列 6 步却写「（13画）」，「爱」写 9 画（规范 10 画）；「中」用「一/丨/人字」当笔画名，「好」的起笔顺序也与规范不符。
- 证据：`tools/chinese/stroke-order-viewer.html:222-231`（`STROKES` 全部数据）、`:233-249`（`render()` 逐项输出并显示条数）、`:267-270`（`__soCount` 从「（N画）」尾项取合计）。Node 复算每字「条目数 vs 自称笔画」：永 8/8、我 5/5、好 6/6、学 **10/11**、生 **6/5**、中 4/4、爱 9/9、想 **6/13**；对照规范：永 5、我 7、学 8、爱 10、中 4（竖、横折、横、竖）、好 6（撇点、撇、横、横钩、竖钩、提）。
- 影响：`tools/chinese/stroke-order-viewer.html`；核心「笔顺演示」对 8 个字全部不可信，导出的 CSV 与页面合计也会出现「行数≠总笔画」的自相矛盾。
- 方案：按 GF 3002-1999 重新录入 8 字（或缩减为已验证字），统一用结构化数组 + 单独的 `total` 字段，启动断言 `strokes.length === total`；无法核实的字直接返回「未收录」，不要用猜测数据填充。

### EL-J18 笔顺页宣称逐笔动画/暂停重播，实际仅静态文字列表；深挖示例「火/水/万/及」不在库（中，确认缺陷）
- 问题：`formula-desc`、meta description、FAQ 均宣称「逐笔动画」「支持逐笔演示与暂停/重播」，`render()` 只把笔画名称拼成 `<div>` 文本，没有任何 canvas/SVG/定时器或播放控件。深挖场景给出的「火」「水」「万」「及」示例全部不在 `STROKES` 中，输入即「未收录」。
- 证据：`tools/chinese/stroke-order-viewer.html:122`（formula-desc 逐笔动画）、`:45`（meta description 同宣称）、`:391`（FAQ 暂停/重播）、`:233-249`（仅文本列表）、`:383-384`（场景示例「火」「水」「万」「及」）、`:222-231`（库键仅 `永我好学生中爱想`）。Node 复算 `Object.keys(STROKES).length === 8`。
- 影响：同页；用户按动画/临摹预期进入，只得到静态名单；搜索摘要与 FAQ 承诺超出真实能力。
- 方案：二选一——实现 CSS/SVG 逐笔显现 + 播放/暂停/重播控件（复用现有笔画顺序数组），或把文案统一改为「静态笔顺列表」并删除动画/暂停表述；示例改成库内字（永/学/想），或补齐示例字数据。

### EL-J19 笔顺页「相关工具」整块重复渲染两次（低，确认缺陷）
- 问题：同一页面出现两个 `data-related-tools="1"` 区块，内容几乎完全相同（中文文化工具箱、偏旁部首查询、农历转换、汉字查询各一次），页面会渲染两遍「🔗 相关工具」。
- 证据：`tools/chinese/stroke-order-viewer.html:178-198` 与 `:200-220`（两块 `related-tools`，仅「农历转换」描述不同）。
- 影响：同页；版式重复、视觉噪声，也让后续维护改一处漏一处。
- 方案：删除重复块保留一份；在页面结构检查中加「同名 `data-related-tools` 唯一」断言。

### EL-J20 常用语翻译仅 48 条中→英，深挖示例西语/法语查无结果，介绍宣称多语言互转（中，确认缺陷）
- 问题：页面实际是「中文 → 英文」静态短语本（48 条，字段只有 zh/en/py/cat/ex），搜索只在 `zh+en+cat` 中匹配。深挖示例给出西语 `¿Cuánto cuesta?`、法语 `Je ne comprends pas`，搜索这些字符串必然 0 命中；介绍还宣称「支持多种语言互转」。
- 证据：`tools/language/phrase-translator.html:247-296`（`PHRASES`，Node 复算 48 条、8 个分类、字段 `zh,en,py,cat,ex`）、`:325-334`（`hay = p.zh + ' ' + p.en + ' ' + p.cat`）、`:199`（西语/法语示例）、`:509`（「支持多种语言互转」）、`:517`（「多语言内容处理」）。Node 复算含「cuánto」「comprends」的记录均为 0。
- 影响：同页；示例与介绍把工具描述成多语翻译器，实际只有中英对照，用户按示例搜索直接落空。
- 方案：补齐 `es`/`fr` 字段并加语言选择器（纯前端静态数据），或改文案为「中英常用语对照」、删除西语/法语示例与「多语言互转」表述；补「示例短语可命中」用例。

### EL-J21 常用语搜索每次停顿键入即写历史，历史被半截词占满（低，确认缺陷）
- 问题：搜索框 `oninput` 直接调用 `doSearch()`，包装层在 1 秒节流后把当前搜索词与结果写入历史；逐字输入并稍作停顿时，`多`、`多少`、`多少钱` 都会成为独立历史记录，把完整查询挤出上限。
- 证据：`tools/language/phrase-translator.html:166`（`oninput="doSearch()"`）、`:436-450`（`now-last<1000` 节流后 `TBKit.history.record(rec)`，`rec` 含 `search-input` 快照）、`:431`（`res` 取结果区文本前 80 字）。Node 复算连续三次输入「多」「多少」「多少钱」（间隔 >1s）会写 3 条不同记录。
- 影响：同页「历史」标签；用户检索的真实意图被输入过程切碎，历史回放也会恢复半截关键词（与 EL-F3 同类，本页为 1s 节流版）。
- 方案：仅在回车、点击搜索或 `blur` 时记录，且 `q.trim().length >= 2`；或在 `doSearch` 的去抖回调中合并同一输入框的连续变化，只保留最终串。

### 留存优化
- `tools/edu/pinyin-typing-practice.html`（低，建议）：修好判定后，把本次打错的字符位置写入现有 `typing-history`，提供「只练错字」与本会话正确率趋势，复用现有统计卡，不新增数据源。
- `tools/language/idiom-solitaire.html`（低，建议）：现有 `chain` 与得分已落历史，可增加「本局接龙导出/重练」和拼音模式下的「末字不会读」提示（展示该字拼音与可选接龙），降低提前断局的挫败感。
- `tools/language/vocabulary-builder.html`（低，建议）：修好日期与收藏解耦后，用 `vocab_progress` 的 `unknown/fuzzy` 生成「今日待复习」队列；间隔信息只存本地，不引入后端与通知。
- `tools/chinese/chinese-character.html`（低，建议）：`lookup()` 已写历史，可补「最近查询」入口与同部首字卡；未收录时提供可复制的「反馈缺字」文案，明确当前覆盖的 20 字范围。
- `tools/language/grammar-checker.html`（低，建议）：问题修到可信后，按规则类型分组筛选并支持「复制修改建议 / 导出 CSV」，复用现有结果卡片与 `__grammar_checkerExport`，不重复建设。

### 续查覆盖
- 本批共核查 8 页：`tools/edu/pinyin-typing-practice.html`、`tools/edu/english-vocabulary.html`、`tools/language/vocabulary-builder.html`、`tools/language/idiom-solitaire.html`、`tools/language/grammar-checker.html`、`tools/chinese/chinese-character.html`、`tools/chinese/stroke-order-viewer.html`、`tools/language/phrase-translator.html`。
- 新增 21 条问题（高 6 条：EL-J1 / EL-J10 / EL-J12 / EL-J15 / EL-J16 / EL-J17；中 12 条；低 3 条）与 5 项留存建议。全部证据来自源码阅读与 Node 内存复算；真实浏览器、英文态、移动端、门禁与线上页面均未验证。
