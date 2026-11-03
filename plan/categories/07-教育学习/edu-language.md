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
