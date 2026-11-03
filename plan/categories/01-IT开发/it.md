# IT 开发 · tools/it（340 页，全站第一大分类）

## 已知问题
### I1. hash/编码类页深度参差
- ⚠ 核实（2026-10-26）：pbkdf2 已完整参数化（迭代/盐/密钥长度/格式）、bcrypt 已有 rounds 成本因子——「参数化」部分条目过时。
- ✅ 耗时实测已落地（2026-10-26）：bcrypt 生成成功消息加「实测耗时 X ms（成本因子每 +1 耗时约翻倍）」、校验加实测耗时+恒定时间比较说明；pbkdf2 派生输出加「实测耗时」行（迭代次数为主要耗时来源）。均 performance.now 本地实测（fallback Date.now）。harness 不可达路径（CDN bcrypt 库/crypto.subtle 分支），老锚零漂移：verify it 764/764、判别器 0、门禁 218/218。

### I2. 正则/格式化器错误提示原始
- ✅ 已核实并收口（2026-10-26）：json-formatter 既有行列定位、yaml-validator 既有行号+列号+上下文片段（条目过时）。真缺口在 toml 系：toml-formatter 的 parseToml 是宽松解析器（无效行静默跳过），「验证」几乎永远通过且无定位。已落地：新增 validateTomlStrict 严格逐行校验（表头格式/缺少 =/空键名/空值，带行号定位；值侧三引号多行字符串跳过内容行不误报、表头行内注释 strip），validateToml 通过时输出输入相关统计「（共 N 个键值对，M 个表）」；format/转换仍走宽松 parseToml 零漂移。verify +2 强用例（缺 = 行号锚 / 合法多行字符串统计锚——后者修复「两态同值」逃生，判别器抓到后以统计输出收敛）；verify it 766/766、判别器 0、EN 分支手写 ASCII 无 CJK。

### I3. barcode/QR 系列仅静态生成
- ✅ barcode 导出已落地（2026-10-26）：7 个 barcode 页（codabar/code128/code39/ean/itf/msi/upc）统一加「下载 PNG」按钮（downloadBarcodePNG：canvas.toDataURL、无 canvas 空态提示、文件名带 slug+时间戳）；qrcode.html 已有 downloadQR（核实既有）。verify it 764/764、判别器 0、门禁 218/218。
- ✅ QR 中心 logo 已落地（2026-10-26）：qr-beautify logo 上传 + 按容错级别限宽嵌入（详见进度区）。纠错级别可视化对比核实：qrcode.html 既有「各纠错级别最小版本对比图 + 容量表高亮当前级别列」（__qrT 双语）——条目后半过时，销案。

## 功能缺陷
- ✅ 时间戳毫秒/秒自动识别已落地（2026-10-26）：timestamp-converter 加「智能粘贴识别」smartInput（纯数字 ≥1e12 判毫秒否则判秒、日期串走 parseDate，同步填秒/毫秒/日期三框 + 识别文案进 #smartHint 可断言；expect 锚 ISO toISOString UTC 确定串免时区漂移）+「当前时间」常驻表 #nowBar（**matchMedia 守卫**：harness 会注入 rAF/setInterval 定时器桩守不住，node/真机差分用 matchMedia；stub 不采集 ⇒ 零 blob 影响，真机 setInterval 每秒刷新）。verify it 768/768、判别器 0。
- ✅ IP 计算器 CIDR 批量已落地（2026-10-26）：ip-calculator v4 tab 加「批量 CIDR 解析」（textarea 每行一条，支持 ip/前缀、ip 点分掩码、裸 IP=/32 三形态；错误行 ❌ 标注不中断；统计串「共 N 条：有效 X，无效 Y」+ 六列汇总表）。⚠ 锚只能用统计串——主机数/掩码值撞「掩码对照表」（harness 兜底直调 buildMaskTable 进 blob），判别器抓到 2 逃生后收紧。verify it 775/775、判别器 0。

## 优化点（G06 联动）
- S6 输入智能化：※ cron「人类语翻译」双向（2026-10-26 落地）+ regex-common「原文高亮+命中偏移明细」（2026-10-26 落地：matchAll 逐段 <mark> + `#i [s-e] 文本` 位置表；⚠ 默认态样例也产高亮标题，标题不可单独作锚）。「正则速查输入联想」核实销案（2026-10-26）：regex-cheatsheet 既有实时搜索过滤（searchInput input → renderCommands 全量重渲染），「输入即响应」已实现，增量价值不足，不再单列。
- S3 位运算可视化已落地（2026-10-26）：bitwise-calculator 结果位区升级 A/B/R 三行 8 位分组对齐（NOT 显示 A/R 两行、SHL/SHR 显示移位前后+移位数）+ 差异统计（AND/OR/XOR「与 A 不同 N 位」、NOT「1→0 共 X 位，0→1 共 Y 位」逐位方向计数）。曾出 bug：NOT 方向计数误用总差异数取补恒得 0/32。verify it 778/778、判别器 0。
- S3 分步：base64/进制约 30 页加「逐步位运算」可视化。
- 高流量页优先做 S4 分享卡（uuid/password/hash）。

## 受影响范围
- tools/it/（340 页，全站第一大分类）

## 进度
- ✅ QR 中心 logo 已落地（2026-10-26）：qr-beautify 加 logo 上传（FileReader→Image→drawLogoOverlay 白底圆角块 contain 居中嵌入），宽度按容错级别限幅 L≤10%/M≤15%/Q≤20%/H≤25%（可遮挡比例口径），状态行显示实际占比；clearLogo 可移除；Boot 挂 initLogoInput（__qrLogoBound 防重复绑定）。⚠ logo 路径 harness 不可达（FileAPI 缺口），闭环 = 默认态零漂移 778/778 + 代码审阅 + 真机验证待老板抽查。修复「简介承诺 add logos 但功能未实现」的名不副实。
- 🟢 批次 2026-10-26：I1 耗时实测、I2 toml-formatter 严格校验、I3 barcode PNG 导出均已落地。
- 🔴 待开发：QR 中心 logo/纠错级别对比；S6 输入智能化试点（正则速查输入联想）；S4 分享卡。

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

### IT-N3 大小写不敏感替换损坏未匹配文本（高，确认源码缺陷）
- 问题与证据：`tools/it/text-replace.html:629-632` 全局且不区分大小写时将整段文本转小写；`Hello WORLD hello` 将 `hello` 替换为 `X` 得 `X world X`，未匹配的 WORLD 也被改变。
- 影响：`tools/it/text-replace.html`；复制或下载可能静默破坏原文。
- 方案：在原文中查找匹配并仅替换命中段，增加混合大小写与 Unicode 用例；保留未匹配片段原样，展示替换次数和差异预览。

### IT-N4 删除空行示例输出反斜杠字符（中，确认源码缺陷）
- 证据：`tools/it/text-replace.html:619-626,797-801` 示例的替换值是两个字符 `\\n`，直接交给 `String.replace`，不是换行符；示例结果会出现字面量 `\\n`。
- 影响：`tools/it/text-replace.html`；一键试用得到错误文本。
- 方案：预设使用真实换行符，或明确支持转义语法并测试；说明正则与普通替换的差异。

### IT-N5 配置导出忽略密钥编码及 Shell 引用不安全（高，确认源码缺陷）
- 证据：`tools/it/env-generator.html:671-679,739-746,759-772` TOML 分支调用 `formatValue` 后仍读取原始 `v.value`，勾选密钥 Base64 后 TOML 依然输出原值；Shell 分支直接拼接变量值，`hello world` 无引号会改变 shell 解析，双引号中的 `$` 等也会展开。
- 影响：`tools/it/env-generator.html`；生成的配置与选项不符，复制执行的 Shell 值可能变化或触发展开。Base64 不是加密，不能将该选项描述为保密措施。
- 方案：各格式共用转换后的值，分别按目标格式安全序列化和转义；覆盖特殊字符及复制下载一致性，明确 Base64 非加密。

### IT-N6 空或非数组 JSON 保留旧 CSV（高，确认源码缺陷）
- 证据：`tools/it/json-to-csv.html:266-277,291-304` 先转换 `[{"a":1}]`，再转换 `[]`；错误分支未清空 `output`，复制、下载仍读取上一份 CSV。与 G10 为同类问题，修复按页面计，避免全站重复计数。
- 影响：`tools/it/json-to-csv.html`；旧数据易被误作当前结果导出。
- 方案：所有失败分支清空结果并禁用复制下载，展示当前输入状态；回归测试有效→无效→有效。

### IT-N7 JSON 嵌套展开承诺与输出不符，历史回填触发下载（中，确认源码缺陷）
- 证据：`tools/it/json-to-csv.html:121-123,278-285,345-356` 文案说嵌套对象展开，但实际仅收集顶层字段并将对象 JSON 字符串化；历史回填调用 `downloadCSV()` 而非转换，可能下载旧输出，浏览器交互待测。
- 影响：`tools/it/json-to-csv.html`；用户预期列不存在，恢复历史可触发非预期下载。
- 方案：实现并说明嵌套展开规则或改正说明；历史恢复后只重算，下载必须由用户主动触发；提供列预览与可复制 CSV。

### IT-N8 负数和自定义进制未正确处理（中，确认源码缺陷）
- 证据：`tools/it/number-base-converter.html:433-445,448-497` 十进制 `-10` 经 `BigInt` 接受，但非十进制转换只在 `n>0` 时循环，返回空串；自定义进制未校验 2–36，37 仍参与计算；回填自定义进制直接把数值赋给不存在该选项的下拉框。
- 影响：`tools/it/number-base-converter.html`；结果缺失或采用超范围基数，历史状态可能无法恢复。
- 方案：明确支持带符号整数或拒绝负数；严格检查基数并正确恢复自定义选项，提供位宽可选的补码解释；浏览器核验历史回填。

### IT-N9 Nginx 场景预设生成无效或误导性配置（高，确认源码缺陷）
- 证据：`tools/it/nginx-config-generator.html:224-235,345-348` 反向代理预设的 root 为空，被回退成 `/var/www/html`，生成 `proxy_pass /var/www/html;`；「HTTPS 静态站」仅设置 `listen 443`，不包含 TLS 监听及证书；端口也未校验 1–65535。
- 影响：`tools/it/nginx-config-generator.html`；配置可能无法加载或误让用户认为已启用 HTTPS。
- 方案：按模式校验上游 URL 和路径；HTTPS 明确要求证书并生成 TLS 配置，端口严格限制范围；提供完整配置复制或下载，并区别历史 CSV 导出。

### 续查覆盖
- 新抽查 `tools/it/env-generator.html`、`tools/it/json-to-csv.html`、`tools/it/number-base-converter.html`、`tools/it/text-replace.html`、`tools/it/nginx-config-generator.html` 共 5 页，新增 7 条问题；未做浏览器、部署或门禁验证。历史回填的实际交互需真机复核。

## 2026-11-03 续查（并行批 G）

### IT-N10 .properties 含空格的赋值被整体当成键（高，确认源码缺陷）
- 问题：`parseProps` 扫描键时遇到普通空格就 `break` 退出，`sep` 保持 -1，随后把整行 trim 后当键、值置空；标准 `key = value` 写法全部失效。
- 证据：`tools/it/properties-parser.html:268-275`。Node 内存执行原函数：`parseProps("app.name = toolbox")` → `{"app.name = toolbox":""}`；页面默认 `SAMPLE`（255）经 Boot（435）→`loadSample`（319）→`doBeautify`（293-300）→`toProps(parseProps())`，实际首行输出为 `app.name \= toolbox = `（键里还带被二次转义的 `=`）。无空格写法 `a=b`、`c:d` 正常。
- 影响：`tools/it/properties-parser.html`；页面一打开示例就是错误结果，JSON 转换/美化/压缩三条路径同时失真。
- 方案：按 Java Properties 规范实现键扫描——行首空白跳过、键在首个未转义的 `=`/`:` 或空白处结束、空白分隔后可选再吃一个 `=`/`:`，再做值 trim；补 `key = value`、`key: value`、制表符分隔与行首缩进用例。

### IT-N11 properties-parser 重复定义覆盖后错误态样式反转（低，确认源码缺陷）
- 问题：同一段脚本里 `setOut/setErr/clearAll/loadSample` 各定义两次，后者覆盖前者；覆盖版 `setErr` 的条件写成 `'err'+(s?'':' ok')`，有消息时反而没有成功态、空消息时反而带 `ok`。
- 证据：`tools/it/properties-parser.html:312-319`（对比 286-311）。`loadSample` 被 319 覆盖后不再只做解析，而是走 `doBeautify`，与 IT-N10 叠加；`clearAll` 的占位文案也由“等待解析...”变为“等待输入...”。
- 影响：`tools/it/properties-parser.html`；解析成功提示按红色错误样式显示，状态反馈不可信。
- 方案：删除重复定义只保留一套；错误/成功态用独立 class 或直接按 `s` 是否以 ✅ 开头判断，并让 `loadSample` 只调用 `propsToJson`。

### IT-N12 URL 解析结果未转义直插 innerHTML，重复参数被覆盖（高，确认源码缺陷）
- 问题：`url.searchParams.forEach` 把重复键写入同一对象（后者覆盖前者）；随后字段值与参数值未经转义拼进 `innerHTML`，历史记录（localStorage）回显同样原样拼接。查询值经 `URLSearchParams` 已解码，`<img onerror>` 会作为标签生效；值内的单引号还会截断复制按钮的 `onclick` 属性。
- 证据：`tools/it/url-parser.html:377-379,389-403,477`。Node `new URL("https://x.com/p?q=<img src=x onerror=alert(1)>&a=1&a=2&tag=%3Cb%3E")` → `searchParams` 得 `{"q":"<img src=x onerror=alert(1)>","a":"2","tag":"<b>"}`：重复 `a` 只剩 `2`，且值含可执行标签。路径侧 `<` 被 URL 序列化为 `%3C`，注入面主要是查询值与历史记录。
- 影响：`tools/it/url-parser.html`；解析含 HTML 的链接时页面可被注入（自输入/历史持久化），参数表只显示最后一个同名参数，复制按钮可能失效。浏览器实际执行未验证。
- 方案：所有输出统一走文本转义或 `textContent`/`createElement` 构建；重复参数保留数组并按 `getAll` 逐行展示；`onclick` 改为事件委托，不把数据拼进属性。

### IT-N13 CSV 校验不识别引号内换行（中，确认源码缺陷）
- 问题：校验按 `\n` 切行后逐行解析，RFC 4180 允许双引号字段跨行，跨行字段会被误报为“引号未闭合”，后续行也被连带误报。
- 证据：`tools/it/csv-validator.html:233-243`。Node 复算（提取 `parseLine` 后按原循环执行）：输入 `id,note\n1,"line1\nline2"\n` → `lines:3, expect:2, issues:["第 2 行：引号未闭合","第 3 行：引号未闭合"]`；同一逻辑对 `"x,y",z` 单行引号逗号判定正常。
- 影响：`tools/it/csv-validator.html`；合法的多行字段（备注、地址）一律判错，用户会去“修”本来正确的数据。
- 方案：改为按字符流状态机解析整份 CSV（引号内换行不切行），记录逻辑行号；补充多行字段、转义双引号、CRLF 用例。

### IT-N14 curl 转代码漏判 POST 与方法/选项值误认作 URL（高，确认源码缺陷）
- 问题：未处理“带 `-d` 时 curl 默认改 POST”，输出固定 GET；除 `-X/-H/-d/--data/--data-raw` 外的选项（如 `-F`、`--data-binary`、`-u`、`-o`）的值不以 `-` 开头，会被当成 URL；头部值原样进 `innerHTML`。
- 证据：`tools/it/curl-parser.html:243,250-265,267-272`。Node 桩执行 `parse()`：`curl -d '{"a":1}' https://api.example.com/x` → `方法：GET`（curl 实际以 POST 发送）；`curl -F 'file=@a.txt' --data-binary @b.json https://x.com` → `URL：file=@a.txt`（真实 URL 丢失）；`-H 'X-Test: <img src=x onerror=alert(1)>'` 原样输出 `<p>X-Test: <img src=x onerror=alert(1)></p>`。
- 影响：`tools/it/curl-parser.html`；复制出的请求方法/URL/表单体与真实 curl 行为不符，常见上传命令直接解析错。
- 方案：建立“选项是否带值”的映射表，成对消费参数；无 `-X` 而有 `-d/--data*/--form` 时默认 POST；未知选项跳过其值并提示；输出统一转义，必要时以结构化 JSON 展示。

### IT-N15 文本截断按 UTF-16 码元切割并忽略省略号预算（中，确认源码缺陷）
- 问题：`chars` 模式用 `length/substring` 按码元截断，emoji 等代理对会被切成半个字符；省略号直接追加、不占长度预算；`bytes` 模式仅把 CJK/全角计 2 字节，emoji 仍按 1 个码元计；非法 limit 被 `||0` 吞成 0 后只输出省略号。
- 证据：`tools/it/text-truncate.html:314,323-335,348-363`。Node 桩执行 `truncate()`：输入 `😀😀😀`、chars、limit=3 → `"😀\ud83d…"`（残留孤立代理项 U+D83D）；`abcdef`、limit=3、省略号 `...` → `"abc..."` 长 6；limit 非法/0 → `"…"`；`😀😀`、bytes、limit=4 → 两个 emoji 全保留（实际 8 字节）。页面公式表（255-268）自称“按码点截断、省略号计入上限”，实现与之相反。
- 影响：`tools/it/text-truncate.html`；复制结果可能含非法字符，长度上限不可用于严格字段校验。
- 方案：用 `Array.from`/`Intl.Segmenter` 按码点或字素簇截断，省略号从 limit 中扣除；bytes 模式按 UTF-8 实际编码长度累计；limit 非正整数时明确报错而非静默 0。

### IT-N16 slugify 的 Unicode 模式在默认选项下被剥掉百分号（中，确认源码缺陷）
- 问题：`unicode` 模式先 `encodeURIComponent` 生成 `%HH`，默认勾选的“移除特殊符号”正则 `[^\w\s\u4e00-\u9fa5-]` 会把 `%` 换成空格，随后小写化并按分隔符切分，转义三元组被拆成普通十六进制片段。
- 证据：`tools/it/slugify.html:350-357,196-200`。Node 复算：`slugify("中文", {mode:"unicode",separator:"-",lowercase:true,stripSymbols:true,stripStopWords:false})` → `e4-b8-ad-e6-96-87`；关闭剥离符号才得到 `%e4%b8%ad%e6%96%87`。另：分隔符选点号时“下划线”预览（379）仍只把 `-` 换成 `_`，显示 `hello.world` 却标为下划线。
- 影响：`tools/it/slugify.html`；默认配置下“Unicode 转义”输出不是可解码的百分号编码，预览标签也会误导。
- 方案：剥离符号发生在编码之后时跳过 `%` 与十六进制字符，或先剥离再编码；预览按实际分隔符替换；补中文/emoji 的转义往返用例。

### IT-N17 Title Case 把撇号后的字母再大写并压平驼峰（中，确认源码缺陷）
- 问题：`toTitleCase` 用 `\b\w` 大写、`\B\w` 小写，撇号是非单词字符，`'t` 被当作新词首字母大写；同样的 `\B\w` 会把驼峰内部大写压成小写。
- 证据：`tools/it/case-converter.html:377-380`。Node 复算：`"don't stop now"` → `Don'T Stop Now`；`"myVar"` → `Myvar`。页面 FAQ（301）声称“只按空格切词、对每个词首字母大写”，与实际结果不符。
- 影响：`tools/it/case-converter.html`；英文标题/人名带撇号时出现 `Don'T`，驼峰输入的首字母大写结果被意外压平。
- 方案：按空白分词后仅把每词首字符大写、保留词内其余字符，或使用带 Unicode 属性转义的正则并显式排除撇号；补 `don't`、`O'Reilly`、`myVar`、`iPhone` 用例。

### 留存优化
- `properties-parser.html:280` 的 `unescapeVal` 不解码 `\uXXXX`：`greet=\u4f60\u597d` 原样保留（Node 已复算），与页面 FAQ 对转义的说明不一致，可随 IT-N10 一并修。
- `properties-parser.html:265` 行尾 `\\`（字面反斜杠）也被当作续行：`path=C:\\` + 下一行 → `{"path":"C:\next=1"}`，需区分“单个反斜杠续行 / 双反斜杠字面量”。
- `url-parser.html:442-459` 构造器不校验 host/port，host 为空会生成 `https:///path`，端口可写入任意非数字内容。
- `slugify.html:315` 拼音表 `'音频':'yinpinyin'` 拼写有误；297 的 15 字长键因贪心上限 8（324）永远匹配不到，属冗余数据。
- `text-truncate.html:330` `fromEnd` 分支完全忽略 `wordBoundary`，与正向行为不对称。
- `case-converter.html:384` `toSentenceCase` 先整体小写，专有名词与缩写（NASA、iOS）会被降格，如需保留应改为逐句首字母处理。

### 续查覆盖
- 本轮人工查看 `tools/it/properties-parser.html`、`url-parser.html`、`csv-validator.html`、`curl-parser.html`、`text-truncate.html`、`slugify.html`、`case-converter.html` 共 7 页，新增 8 条（高 3、中 4、低 1），编号续 IT-N10～N17，与既有 IT-N1～N9 无重复。
- 取证方式仅为源码静态阅读 + Node 内存提取原函数/最小 DOM 桩执行复算；未做真实浏览器交互、英文态、移动端、门禁或部署验证。

## 2026-11-03 续查（并行批 J）

### IT-N18 Markdown 链接目标未转义，可注入 HTML 属性（高，确认源码缺陷）
- 描述：`inline()` 只转义 `&<>`，不处理双引号；链接正则把 URL 原样塞进 `href`，最终经 `ToolBox.setResult` 以 `innerHTML` 写入预览区。
- 证据：`tools/it/markdown-to-html.html:289-296`（294 为链接替换）；`js/common.js:2047-2050`（`setResult` 直接赋值 `innerHTML`）。Node 复算 `inline('[x](https://a/" onmouseover="alert(1))')` → `<a href="https://a/" onmouseover="alert(1" target="_blank" rel="noopener">x</a>`；`[x](javascript:alert(1))` 的 `href` 被 `[^)]+` 截成 `javascript:alert(1`。
- 影响：`tools/it/markdown-to-html.html`；粘贴带引号的链接即可在预览区制造事件属性（自输入型 XSS），转载他人 Markdown 时同样成立。
- 方案：URL 走白名单（http/https/mailto）并做属性转义，或改用 `createElement`/`setAttribute` 构建链接；预览与“HTML 代码”面板统一输出净化后的结果。

### IT-N19 输入修改后仍处理旧快照（高，确认源码缺陷）
- 描述：`applyOp` 只在 `!hasOriginal` 时快照输入，之后所有操作都基于 `currentLines`；用户再改输入框，按钮仍处理首轮快照。
- 证据：`tools/it/text-dedupe-sort.html:515-525`（552-558 渲染、562-584 复制/下载同样读 `currentLines`）。Node 模拟：对 `a\na\nb` 执行去重 → `a\nb`；把输入改为 `y\nx` 再点升序 → 仍输出 `a\nb`。`380-385` 的“原始项数”却读当前输入 `parseInput()`，与结果不同源。
- 影响：`tools/it/text-dedupe-sort.html`；首次操作后输出、复制、下载都与当前输入无关，统计数量也对不上。
- 方案：监听 `input` 或在每次 `applyOp` 前比对输入与快照，变化即重建快照；统计统一按同一数据源计算。

### IT-N20 历史/数据表/图表恒空，历史回填会清空全部选项（中，确认源码缺陷）
- 描述：`__text_cleanerResText` 读取 `#output-text` 的 `textContent`，而它是 `textarea`——当前 `value` 不写入子节点，`textContent` 恒为空，extras 直接提前返回；且 extras 只包装了 `applyPreset`，点“执行清理”与预设条回调（`executeClean`）都不会记录。历史回填调用 `applyPreset()` 不带参数。
- 证据：`tools/it/text-cleaner.html:756-763`（textarea 取 textContent）、`846-849`（仅包装 applyPreset）、`839-845`（预设条回调为 `executeClean`）、`781-793`（回填 `applyPreset()`）、`491-505`（`presets[undefined]` → `[]` → `deselectAll()`）、`472-474`。jsdom 复算：`#output-text` 初始与 `value='清理结果内容'` 之后 `textContent` 均为 `""`，ResText 等价结果为 `""`；`{…}[undefined]` → `undefined`，`list=[]` 会走 `deselectAll()`。
- 影响：`tools/it/text-cleaner.html`；数据表/图表/历史三个页签永远为空；若将来有历史记录，恢复后默认勾选被清空，输出与记录不符。
- 方案：改读 `output-text.value`；包装 `executeClean` 记录历史；回填时逐字段恢复后直接 `executeClean()`，不要用无参 `applyPreset`。

### IT-N21 空输入回退示例文本，复制结果与输入无关（中，确认源码缺陷）
- 描述：`calcTool` 在输入为空时把局部变量 `raw` 替换成三行示例，但输入框仍为空；输出框、统计与“复制结果”都显示/复制示例。
- 证据：`tools/it/line-ending-converter.html:320-327`（`if(!raw){raw='line1\nline2\nline3';}`）、`340-343`（`copyLe` 复制 `leOutput`）。Node 复算 `raw=''`、目标 `' \n'` → `"line1 \nline2 \nline3"`。
- 影响：`tools/it/line-ending-converter.html`；清空后点“转换/复制结果”得到与当前输入无关的文本，易被误当作自己的数据。
- 方案：空输入时清空输出与统计并提示；示例仅由显式的“示例”按钮注入（页面当前无该按钮）。

### IT-N22 历史只保存前 1000 字符，恢复后静默截断（中，确认源码缺陷）
- 描述：`addToHistory` 对两份文本各做 `substring(0,1000)`；`loadHistory` 直接回填并重新 `doDiff()`，无任何截断提示。
- 证据：`tools/it/text-diff.html:697-703`、`733-739`。Node 复算：1500 个 `A` + `TAIL` 经 `substring(0,1000)` 后长度为 1000 且不含 `TAIL`。
- 影响：`tools/it/text-diff.html`；长文本从历史恢复后 diff 结果看似正常但内容已被砍掉。
- 方案：保存完整文本；确需限长时存全文摘要并提示“已截断，不可恢复对比”，或对超限记录禁用回填。

### IT-N23 重复节静默丢键，解析成功提示掩盖数据丢失（中，确认源码缺陷）
- 描述：`parseIni` 遇到同名 `[section]` 直接 `result[section] = {}` 重建空对象，先前同名节里的键全部丢失；页面说明虽写了“新建该节的空对象”，但未提示会覆盖旧键，FAQ 也只说明重复键（后值覆盖），用户无从察觉。
- 证据：`tools/it/ini-parser.html:259-278`（265-267 覆盖）、`160`（说明文案）、`208`（FAQ 只提重复键）、`292-297`（始终返回“✅ 解析成功”）。Node 复算：`parseIni('[a]\nx=1\n[a]\ny=2')` → `{"a":{"y":"2"}}`（`x` 丢失）。
- 影响：`tools/it/ini-parser.html`；含重复节（分片配置、拼接文件）的合法 INI 被静默截断，成功提示让用户以为解析完整。
- 方案：同名节合并已有键（或重复键显式报错并列出冲突键），至少在被覆盖时给出警告；`:` 等常见分隔写法可作为兼容性增强另行评估（页面当前只声明 `=`）。

### IT-N24 “压缩”等同“美化”，重复定义导致成功态变红（中，确认源码缺陷）
- 描述：`doMinify` 直接调用 `doBeautify`；脚本后段重复定义 `setOut/setErr/clearAll/loadSample`，覆盖版 `setErr` 的条件写成 `'err'+(s?'':' ok')`——有消息反而只有 `err`，空消息反而带 `ok`；`loadSample` 也被改成走美化。
- 证据：`tools/it/ini-parser.html:307-316`（316 `doMinify(){ doBeautify(); }`）、`317-325`（重复定义）。Node 复算覆盖版 `setErr('✅ 解析成功')` → className `err`；`setErr('')` → `err ok`。`441` 的 Boot 先 `loadSample()` 再 `iniToJson()`，示例按钮（325）则只做美化。
- 影响：`tools/it/ini-parser.html`；“压缩”按钮无任何压缩效果，成功提示显示为红色错误样式，示例按钮输出语义也被改。
- 方案：实现真正的 INI 压缩或移除该按钮；删除后一组重复定义，成功/失败用独立 class 判断。

### IT-N25 美化把 JSON 数组当 INI 节名（中，确认源码缺陷）
- 描述：`doBeautify` 仅以 `startsWith('{')` 判定 JSON，`[...]` 走 INI 解析；`toIni` 对数组用 `for...in` 输出 `0 = a` 形式。
- 证据：`tools/it/ini-parser.html:307-314`、`279-291`、`299-306`。Node 复算：`parseIni('["a","b"]')` → `{"\"a\",\"b\"":{}}`；`JSON→INI` 对 `["a","b"]` 产出 `0 = a` / `1 = b`。
- 影响：`tools/it/ini-parser.html`；对合法 JSON 数组执行“美化”得到空节，用户难以判断是输入错误还是工具问题。
- 方案：用 `JSON.parse` 试解析判型（含 `[`），数组显式支持（如 `[list]` 节）或明确报“INI 不支持数组”；`toIni` 对数组单独处理。

### IT-N26 两个下拉框没有任何选项，代码面板与压缩模式不可用（中，确认源码缺陷）
- 描述：`#showcode`、`#compact` 两个 `<select>` 在源码中为空，代码却按值 `'1'`/`'compact'` 判断；`resetForm` 的 `selectedIndex=0` 也无实际效果。压缩结果 `outHtml` 只在“显示 HTML 代码”分支被使用。
- 证据：`tools/it/markdown-to-html.html:136,140`（空 select）、`330-337`（取值判断与 `outHtml` 用法）、`342-343`。jsdom 复算：`#showcode` 与 `#compact` 的 `options.length` 均为 0；再按 330-337 逻辑模拟“显示代码关闭 + 压缩开启”：可见区 `<p>a</p>\n<ul><li>b</li></ul>` 不变，仅 `code` 变量被压缩。
- 影响：`tools/it/markdown-to-html.html`；两个标注功能实际不可选，HTML 代码面板永不出现；“压缩”即使可选项生效也只影响代码面板，不影响预览。
- 方案：补上 `option`（`0/1`、`pretty/compact`），并让压缩模式同时作用于预览与代码输出。

### IT-N27 图片语法未实现，`![alt](url)` 输出字面 `!` 加链接（中，确认源码缺陷）
- 描述：行内规则只有标题/粗斜/链接/行内代码，没有图片规则；`![alt](url)` 中的 `[alt](url)` 被链接规则匹配，感叹号留在文本里。
- 证据：`tools/it/markdown-to-html.html:289-296`、FAQ JSON-LD `347` 声称覆盖“图片”。Node 复算 `![alt](https://x/y.png)` → `!<a href="https://x/y.png" target="_blank" rel="noopener">alt</a>`。
- 影响：`tools/it/markdown-to-html.html`；粘贴含图片的 Markdown 得到错误 HTML，与页面承诺不符。
- 方案：增加图片规则（必须先于链接匹配），输出 `<img src alt>`，并对 `src`/`alt` 做属性转义与 URL 白名单。

### IT-N28 字符级对比按 UTF-16 码元切分（低，确认源码缺陷）
- 描述：`charDiffLine` 用 `split('')` 与按码元的 LCS，emoji 等代理对被拆成两半分别着色。
- 证据：`tools/it/text-diff.html:459-463`。Node 复算 `charDiffLine('😀😀😀','😀😀')` → oldHtml 含 `[-\ud83d-][-\ude00-]`（两个高亮块分别包住一对代理项的一半）。
- 影响：`tools/it/text-diff.html`；emoji/扩展字符差异展示破碎，导出文本可能含孤立代理项。
- 方案：改用 `Array.from` 或 `Intl.Segmenter` 按码点/字素簇切分后再做 LCS。

### IT-N29 逐行对照预览按索引配对，删行后错位；FAQ 承诺的“全压成一行”未实现（中，确认源码缺陷）
- 描述：`top_blank` 本身按 `trim()===''` 判空行（行为正确），但预览直接拿 `rawLines[pi]` 与 `lines[pi]` 并列；一旦删除过空行（默认预设即会删），两列的第 N 行就不再对应同一段文本。另 FAQ 称“可选保留段落或全压成一行”，页面只有 4 个勾选项，没有折叠换行能力。
- 证据：`tools/it/whitespace.html:219-229`（225 空行过滤）、`250-257`（253-256 同索引配对）、`407-408`（FAQ）。Node 复算 `a\n   \nb` 勾 `top_blank` → 输出 `a\nb`；按 253-256 配对得到：第 2 行原始 `"   "` / 处理后 `"b"`，第 3 行原始 `"b"` / 处理后 `""`。
- 影响：`tools/it/whitespace.html`；预览把“被删的空白行”和“下一行内容”放在同一行展示，误导用户核对；文档承诺的“全压成一行”无法实际执行。
- 方案：预览携带原始行号映射（被删行明确标注“已删除”），左右列不再假装同源同一行；删除该 FAQ 承诺或补“折叠为单行”选项。

### IT-N30 裸 CR 不切分、强制 trim 静默丢空项与缩进（低，确认源码缺陷）
- 描述：输入只按 `/\r?\n/` 切分，旧 Mac 的单独 `\r` 不识别；随后统一 `trim()` 并 `filter(Boolean)`，缩进、空字段被静默去掉。
- 证据：`tools/it/list-converter.html:272-290`（273 切分/清洗、280 quote、283 csv）。Node 复算：`a\rb`、comma 模式 → 单条 `a\rb`（未按 CR 切分）；`"  a  \n\nb "` → `["a","b"]`，结果 `a, b`。
- 影响：`tools/it/list-converter.html`；混合换行文件被当成一项；需要空字段或缩进的列表无法原样转换。
- 方案：改用 `/\r\n|\r|\n/`；提供“保留首尾空白/保留空项”开关，至少在结果中提示删除了多少项。

### IT-N31 视图切换依赖全局 `event`（中，待验证：Firefox）
- 描述：`switchView` 通过 `event.target` 找当前页签，`event` 未作为参数传入；Chrome/Safari 有 `window.event`，Firefox 没有全局 `event`，内联 `onclick` 调用时会取不到。
- 证据：`tools/it/text-diff.html:405-410`、`252-253`（内联 `onclick="switchView('unified')"`）。本轮按源码推断为 Firefox 下 ReferenceError，未做浏览器验证。
- 影响：`tools/it/text-diff.html`；Firefox 用户可能无法切换合并/并排视图。
- 方案：改为 `switchView(view, evt)` 显式传参，或用事件委托绑定 `.view-tab`，不依赖全局 `event`。

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
- 本轮人工查看 `tools/it/text-diff.html`、`whitespace.html`、`text-cleaner.html`、`text-dedupe-sort.html`、`line-ending-converter.html`、`list-converter.html`、`markdown-to-html.html`、`ini-parser.html` 共 8 页，新增 14 条（高 2、中 10、低 2），编号续 IT-N18～N31，与既有 IT-N1～N17 无重复；其中 IT-N31 为待验证项。
- 取证方式为源码静态阅读 + Node 内存提取原函数/最小逻辑复算（含 `markdown inline`、`parseIni`、`removeLineNum`、`leViz`、`list convert`、`calcTool` 等价实现），并用本地已装 jsdom 复核 `textarea.textContent` 与空 `<select>` 的 `options.length`；未开浏览器，未做英文态、移动端、门禁或部署验证。

## 2026-11-03 续查（并行批 K）

> 范围：本轮阅读 8 页（`tools/it/xml-formatter.html`、`tools/it/html-entities.html`、`tools/it/text-statistics.html`、`tools/text/stats-1.html`、`tools/text/analysis-density.html`、`tools/text/reading-time-estimator.html`、`tools/text/sensitive-word-filter.html`、`tools/text/text-extract-phones.html`）。仅源码 + Node/jsdom 复算，未开浏览器/未做 EN/移动端/门禁验证。

### IT-N32 XML 格式化与压缩丢失根元素、CDATA 和文本内换行（高，确认源码缺陷）
- 描述：`formatXml` 把 `doc.documentElement` 传给 `serializeNode`，而后者只遍历 `childNodes`，根元素自身的开闭标签永远不输出；子节点收集只认元素与文本（`nodeType 1/3`），CDATA（`nodeType 4`）被当作空内容输出为自闭合标签，内容整体丢失；`doMinify` 又对序列化结果全局删除 `\n`，文本节点与 CDATA 内部的合法换行一并被删。XML 声明、DOCTYPE、根外注释同样不会保留。
- 证据：`tools/it/xml-formatter.html:262,264-296,272,284-285,306-312`
- 复现：用 jsdom 加载页面原有函数执行。默认 `SAMPLE` 经 `formatXml(SAMPLE,true)` → 输出以 `<to from="Alice">Bob</to>` 开头、`<raw/>`，根 `<note>` 与 `<![CDATA[<unparsed>text</unparsed>]]>` 全部消失；`<root><a>1</a><b>2</b></root>` → `<a>1</a>\n<b>2</b>`（期望保留 `<root>`）；`<a>line1\nline2</a>` 压缩 → `<a>line1line2</a>`（期望保留文本换行）。
- 影响：页面 Boot 直接 `doBeautify()`，首屏示例即为多根、非法 XML；用户复制格式化/压缩结果会解析失败或丢失整段 CDATA 内容。
- 方案：在 `formatXml` 中单独输出根元素本身；按 `nodeType` 分发并保留 CDATA、注释、处理指令与 XML 声明；压缩只删除元素之间的缩进换行，文本与 CDATA 原样保留；补根元素、CDATA、mixed content 往返用例。

### IT-N33 HTML 实体全字符编码按 UTF-16 码元取码，代理对被截断（中，确认源码缺陷）
- 描述：`encodeAll` 用 `for...of` 按码点迭代，却只取 `ch.charCodeAt(0)`（UTF-16 高位），非 BMP 字符只生成高位代理项的数字实体，低位代理被丢弃；`decodeText` 用 `innerHTML` 解析输入，裸 `<` 后接字母会被当成标签吞掉。
- 证据：`tools/it/html-entities.html:573-587`（`576-577` 编码、`585-586` 解码）
- 复现：`encodeAll('😀')` → `&#55357;`（期望 `&#128512;`）；`encodeAll('𠮷')` → `&#55362;`（期望 `&#134071;`）；`decodeText('a<b')` → `a`（期望 `a<b`）；`decodeText('<div>Hello</div>')` → `Hello`（期望保留标签文本）。
- 影响：emoji、生僻字经“全字符编码”后变成孤立代理项实体，复制出去无法还原；解码含未转义尖括号的文本会静默丢内容。
- 方案：编码改用 `codePointAt(0)` 生成 `&#十进制;`；解码避免 `innerHTML`，改用 `textarea` 的 `textContent` 往返或只替换已知实体；补 emoji、扩展汉字、裸 `<` 用例。

### IT-N34 敏感词高亮与计数使用两套文本源，清空后复制仍取旧结果（中，确认源码缺陷）
- 描述：`count`/`clean` 在原始文本上做替换，而 `marked` 在转义后的 HTML 上再跑同一正则：词表含 `lt`/`amp` 会命中 `&lt;`/`&amp;` 实体名并破坏实体，词表含 `<` 时 clean 能命中却因原文已被转成 `&lt;` 而无法高亮。另 `!raw || words.length===0` 分支只更新 `preview.innerHTML`，不更新 `preview.dataset.clean`，复制按钮继续读上一次的清洗结果；词表为空时该分支还把未转义原文直接写入 `innerHTML`。
- 证据：`tools/it/sensitive-word-filter.html:202-210,216-221,224-235,239-245`
- 复现：输入 `a < b`、词表 `lt` → 计数 0，预览却输出 `a &<mark>lt</mark>; b`（实体被切断）；词表 `<` → 计数 1，预览 `a &lt; b` 无高亮；先清洗 `违法内容`（词表 `违法`）再清空内容 → `copyResult` 仍复制 `**内容`；清空词表后粘贴 `<img src=x onerror=...>` 会作为 HTML 写入预览（自输入型注入）。
- 影响：高亮与命中数对不上，实体/标签类词条误报；清空后复制到旧数据，易被误当作当前清洗结果。
- 方案：高亮改为在原文上按匹配区间插入标记后再统一转义（或分段构建 DOM）；清空/无词条时同时清空 `dataset.clean` 并禁用复制；空词表分支用 `textContent` 输出。

### IT-N35 关键词按无边界子串计数，密度可超 100%，纯数字文本被判无内容（中，确认源码缺陷）
- 描述：含字母的关键词用 `new RegExp(...,'gi')` 全文子串匹配，无词边界；中文分支用 `indexOf` 累加，同样按子串计数。分母却只算“汉字数 + 英文单词数”，因此关键词命中次数可大于总词数，密度超过 100%。此外纯数字/纯符号文本的 `total=0`，在关键词统计前直接返回“请输入文本”。
- 证据：`tools/text/analysis-density.html:202-206,211-219`
- 复现：文本 `banana`、关键词 `a` → 出现 3 次、总词数 1、密度 `300.00%`（期望按独立词 0 次或明确说明按子串）；文本 `the the`、关键词 `he` → 密度 `100.00%`（实际 `he` 作为独立词 0 次）；文本 `2026 11 03`、关键词 `2026` → 输出“请输入文本”（期望照常统计并提示密度不适用）。
- 影响：英文短词/词根会把密度算成虚高，SEO 判断被误导；纯数字或编号文本无法分析。
- 方案：英文关键词加非字母数字边界并按词计数，或明确标注“子串出现次数”；分母纳入数字组或单独给出“不适用”；纯数字文本不提前返回。

### IT-N36 号码正则无边界，长数字串被截断并重复提取国际号（中，确认源码缺陷）
- 描述：手机号 `/1[3-9]\d{9}/g` 与座机 `/0\d{2,3}[-\s]?\d{7,8}/g` 均无前后边界，会在更长数字串中截取前 11/12 位；国际号与手机号规则并行，`+8613812345678` 同时抽出带国家码与裸手机号两份，去重因字符串不同而无效。
- 证据：`tools/text/text-extract-phones.html:281-284,286-298`
- 复现：`138123456789` → `["13812345678"]`（期望不匹配或提示疑似非法长度）；`+8613812345678` → `["13812345678","+8613812345678"]`（同一号码重复）；`0101234567890` → `["010123456789"]`（截断）。
- 影响：从日志/通讯录批量抽取时复制出被截断号码与重复号码，后续外呼或导入会失败/重号。
- 方案：号码规则加 `(?!\d)`/前后非数字边界并校验总长度；国际号优先匹配并抑制其内部手机号；规范化后统一去重；补超长数字串与 `+86` 连续写法用例。

### IT-N37 阅读速度清空/非法被当成 1，空文本恒报 1 分钟且取整与说明相反（中，确认源码缺陷）
- 描述：`Math.max(1,num(id))` 把空值、0、负数统一抬成 1，清空“中文速度”后长文被算成数百分钟；空文本 `Math.max(1,Math.round(0))` 仍显示 1 分钟；公式说明写“结果向上取整至分钟”，实现却是 `Math.round`，1.4 分钟显示 1。
- 证据：`tools/text/reading-time-estimator.html:106,214,218-224`
- 复现：300 个汉字 + 中文速度留空 + 英文 200 → 300 分钟（期望提示速度无效/拒绝计算）；280 个汉字 + 速度 200 → 1 分钟（期望向上取整为 2）；空文本 → 1 分钟（期望 0 或提示无可估算内容）。
- 影响：默认参数误删后结果相差两个数量级；空输入也给出“1 分钟”的伪结论。
- 方案：速度校验为正整数，非法/空明确报错，不 clamp 为 1；空文本返回 0；按文档使用 `Math.ceil` 或修正说明。

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

### IT-N40 时间格式转换：微秒预设与 14 位以上时间戳必然报错（中，确认源码缺陷）
- 描述：`parseInput` 只认 `^\d{10,13}$`，其余交给 `new Date()`；16 位微秒串既不被当作时间戳、也无法被 Date 解析，返回 null 后直接走"无法解析时间"分支。而页面预设条自身就提供"微秒时间戳"按钮。
- 证据：`tools/it/time-format-converter.html:234-241`（正则 235、回退 239）、`379`（微秒预设 `1700000000000000`）、`252`（错误分支）
- 复现：点"微秒时间戳"预设或输入 `1700000000000000` → 输出"无法解析时间，请输入合法值"（期望按 1.7e15 µs = 2023-11-14T22:13:20Z 换算，或明确不支持并移除该预设）；`17000000000000`（14 位）同样报错
- 影响：页面唯一的"微秒"入口不可用；14 位时间戳（部分日志/数据库）无法转换。
- 方案：按位数识别 16 位微秒（除以 1000 转毫秒）、19 位纳秒（除以 1e6）；无法识别时提示支持范围并移除不可用预设；补 10/13/16/19 位用例。

### IT-N41 时间格式转换：纯日期按 UTC 解析，UTC+8 下时间偏移 8 小时（中，确认源码缺陷）
- 描述：`YYYY-MM-DD` 未命中前面的本地解析规则，落入 `new Date(v)` 回退路径；ECMAScript 规定 date-only 形式按 UTC 解释，页面却把结果当本地时间格式化，导致输入日期后"本地时间"变成同日 08:00。另：FAQ/深度解析要求"确认所选时区"，页面没有任何时区选择控件。
- 证据：`tools/it/time-format-converter.html:234-241`（239）、`260`（本地时间输出）、`419-420`（FAQ 时区表述）
- 复现：输入 `2023-07-22` → 本地时间 `2023-07-22 08:00:00`、Unix 秒 `1689984000`（期望本地 `2023-07-22 00:00:00`、`1689955200`，或显式说明按 UTC 解析）
- 影响：只填日期的用户会得到整体偏移 8 小时的"本地时间"与时间戳。
- 方案：date-only 显式拼 `T00:00:00` 按本地解析（或增加时区下拉），并在页面标注解析口径。

### IT-N42 时间格式转换：裸数字 "0"/"1" 被当成年份 2000/2001（低，确认源码缺陷）
- 描述：非 10–13 位纯数字落入 `new Date(v)`；V8 把 `"0"`、`"1"` 解释为年份 2000/2001，而不是 Unix 秒。
- 证据：`tools/it/time-format-converter.html:235-240`
- 复现：输入 `0` → `2000-01-01 00:00:00`；`1` → `2001-01-01 00:00:00`（期望 `1970-01-01 08:00:00` 或提示"位数不足"）
- 影响：粘贴被截断的时间戳会被静默当成 2000/2001 年，排查日志时误判。
- 方案：纯数字统一走时间戳分支（按位数或阈值判定秒/毫秒），不足 10 位给出明确提示。

### IT-N43 时间戳转换：12 位毫秒戳被 smartConvert 判成秒，输出 31969 年（高，确认源码缺陷）
- 描述：智能识别只用 `n >= 1e12` 区分毫秒；2001-09-09 之前的毫秒戳（12 位）低于阈值，被当成秒再乘 1000，Date 仍可表示，于是静默给出 3 万年后的日期，并提示"识别成功"。
- 证据：`tools/it/timestamp-converter.html:577-596`（579 阈值、580 构造日期）
- 复现：`946684800000`（2000-01-01T00:00:00Z）→ 识别为"秒时间戳（12 位）"，日期 `31969-04-01 08:00:00`（ISO 为 `+031969-04-01T00:00:00Z`；期望 2000-01-01）；`1700000000000` 才会正确判为毫秒
- 影响：2000–2001 年的历史数据整体算错，且提示文案让用户以为识别正确。
- 方案：按位数（≤10 位秒、13 位毫秒、16 位微秒）或结合合理年份区间判定；毫秒数 <1e12 时仍判毫秒；无法判定时让用户显式选单位。

### IT-N44 时间戳转换：时区表写死固定偏移，忽略夏令时（中，确认源码缺陷）
- 描述：`TIMEZONES` 为纽约 -5、伦敦 0、巴黎 +1、悉尼 +11 等固定值；这些地区夏季使用 DST（-4/+1/+2/+10），固定偏移在半年内整体差 1 小时。
- 证据：`tools/it/timestamp-converter.html:416-427`、`546-562`（553-554 固定偏移计算）
- 复现：`2026-07-01T12:00:00Z` → "纽约 (GMT-5)" 显示 `07:00`（期望 08:00，EDT -4）；"伦敦 (GMT+0)" 显示 `12:00`（期望 13:00，BST +1）
- 影响：跨时区排障时纽约/伦敦/巴黎/悉尼结果偏差 1 小时；北京/东京/夏威夷不受影响。
- 方案：改用 `Intl.DateTimeFormat` 的 IANA 时区（America/New_York 等）格式化，或明确标注"标准时（不含 DST）"。

### IT-N45 时间戳转换：相差年/月按日历字段相减，1 天可显示 1 年/1 月（中，确认源码缺陷）
- 描述：`diffYear/diffMonth` 只比较年份与月份字段，不看日/时；结果与"相差天数"自相矛盾，文案虽带"约"仍是错误结论。
- 证据：`tools/it/timestamp-converter.html:713-714`（输出 719-720）
- 复现：`2025-12-31` → `2026-01-01`：相差天数 1，相差年数"约 1 年"；`2026-01-31` → `2026-02-01`：相差月数"约 1 个月"
- 影响：日期对比结论被夸大，跨年/跨月仅 1 天的场景误判。
- 方案：改为整月/整年口径（按月历逐段推进或计算完整周期数），或移除这两项只保留天/周/时/分/秒。

### IT-N46 颜色转换：rgb/rgba 数值不校验范围，生成非法 HEX 与 alpha（中，确认源码缺陷）
- 描述：`rgbMatch` 只接受 `\d+`，不限制 0–255；`rgbToHex` 直接 `toString(16)`，三位通道值输出 3 位十六进制，拼出 7 位 HEX；alpha 也不限制 0–1。
- 证据：`tools/it/color-converter.html:443-446`（解析）、`457-459`（转 HEX）、`554-566`（格式输出）
- 复现：`rgb(300, 0, 0)` → `#12c0000`（期望 `#ff0000` 或提示越界）；`rgba(0, 0, 0, 1.5)` → `rgba(0, 0, 0, 1.5)`（期望拒绝或 clamp 到 1）
- 影响：复制出的 HEX/RGBA 不是合法 CSS，预览色与实际输入不一致。
- 方案：解析时校验 0–255 与 alpha 0–1，越界 clamp 或报错；`rgbToHex` 对越界值先 clamp。

### IT-N47 颜色转换：对比度忽略 alpha 且非法输入保留旧结果（中，确认源码缺陷）
- 描述：`calcContrast` 只用 r/g/b 计算亮度，RGBA 前景半透明时未与背景合成；`if (!fg || !bg) return;` 直接返回，上一次的比值与 WCAG 结论原样留在页面。
- 证据：`tools/it/color-converter.html:644-685`（651 早退、653-658 亮度计算）
- 复现：前景 `rgba(0, 0, 0, 0.5)`、背景 `#ffffff` → 显示 `21.00:1`、AAA（按白底合成应约 `3.95:1`、不通过）；把前景清空 → 仍显示上一组比值
- 影响：半透明配色的可读性结论严重偏乐观；无效输入时旧结论被误当作当前结果。
- 方案：按背景合成前景 alpha 后再算亮度；非法输入清空比值与等级并提示。

### IT-N48 进制转换：非法输入只改主结果，其余进制仍显示上次值；基数静默 clamp（中，确认源码缺陷）
- 描述：catch 分支只把 `mainOut` 设为 ❌，`r2/r8/r10/r16/r32/r36` 保持旧值；`fromBase/toBase` 超出 2–36 时静默改成 2/36 并写回输入框，无提示。
- 证据：`tools/it/integer-base-converter.html:294-295`（clamp 与写回）、`298-308`（308 catch）
- 复现：先输入 `ff`（16→10）得到各进制结果，再输入 `1g`（16 进制非法）→ 主结果显示 ❌，但二/八/十/十六/32/36 进制卡片仍是 `ff` 的旧值；源进制填 `99` → 被改成 `36` 且无提示
- 影响：错误输入下旧数据仍可被复制；基数被悄悄替换，用户不知转换口径已变。
- 方案：catch 时清空全部结果卡片；基数越界时保留输入并明确报错，不写回。

### IT-N49 Chmod 计算器：文档承诺特殊位，界面无法输入/输出四位数（低，确认源码缺陷）
- 描述：公式说明与 FAQ 都写 setuid/setgid/sticky 置于首位（如 4755），但页面只有 9 个 r/w/x 复选框，`calc` 恒拼接 3 位数字，复制命令也永远是 3 位。
- 证据：`tools/it/chmod-calculator.html:122`（公式列表）、`200`（FAQ）、`305-311`（calc）、`327-331`（copyPerm）
- 复现：勾选全部 rwx → `chmod 777 <file>`；没有任何控件能得到 `4755`（期望提供 setuid/setgid/sticky 三个开关并输出 4 位）
- 影响：需要 setuid/sticky 的场景无法使用，文档与功能不一致。
- 方案：增加三个特殊位复选框（4/2/1 置千位），或在说明中注明"本工具仅支持 3 位权限"。

### IT-N50 Crontab 生成器：校验函数忽略 min/max，越界值被当作合法表达式（高，确认源码缺陷）
- 描述：`valid(s,min,max)` 的三个参数中 min/max 完全未使用，正则只检查形状；`99` 分钟、`1-99` 小时、`*/0` 步长都能通过，生成的 crontab 会被 cron 拒绝或语义异常。
- 证据：`tools/it/crontab-generator.html:283`（正则）、`296-302`（调用处传入范围）
- 复现：分钟填 `99` → ✅ 表达式 `99 9 * * *`；分钟填 `*/0` → ✅；小时填 `1-99` → ✅（期望标红"分钟 0-59 / 小时 0-23"）
- 影响：复制出的 crontab 无法加载（cron 报 bad minute/hour），或 `*/0` 行为不可预期。
- 方案：解析每个枚举/区间/步长并逐项校验边界（步长 >0 且不超过范围），越界给出字段级提示。

### IT-N51 Crontab 生成器：默认表达式的中文说明重复"每月"且语序不通（低，确认源码缺陷）
- 描述：`f[2]==='*' && f[4]==='*'` 分支固定以"每月 "开头，再拼接本身已是"每月"的 `parts[3]`，造成重复量词与错误语序。
- 证据：`tools/it/crontab-generator.html:313-317`、`284-290`
- 复现：默认值 `0 9 * * *` → "中文说明：每月 每月 每天 小时 9 分钟 0"（期望"每天 9:00"）
- 影响：默认打开的页面即展示病句，用户难以据此核对表达式。
- 方案：按"分/时/日/月/周"重组自然语言并去重量词；补 `* * * * *`、`0 9 * * *`、`0 18 * * 1-5` 快照用例。

### IT-N52 IPv6 转换：IPv4 映射预设必然报非法，`/前缀` 也不支持（高，确认源码缺陷）
- 描述：`expand` 对 8 段做 `^[0-9a-f]{1,4}$` 校验，点分十进制段必然失败；页面预设条提供 `::ffff:192.0.2.1`，FAQ 也专门介绍 IPv4 映射。含 `/64` 的地址同样被拒。
- 证据：`tools/it/ipv6-converter.html:213-232`（230 正则）、`346`（IPv4 映射预设）、`385`（FAQ）、`151`（前缀说明）
- 复现：点"IPv4 映射"或输入 `::ffff:192.0.2.1` → "⚠️ 不是合法的 IPv6 地址。"（期望 `0000:...:ffff:c000:0201`）；`2001:db8::1/64` → 同样报错（期望拆出前缀长度并校验 0–128）
- 影响：工具自带的 4 个预设之一不可用；双栈/映射地址与带前缀地址都无法转换。
- 方案：识别末尾 IPv4 段并转成两组十六进制；剥离 `/len` 单独展示与校验；补 `::ffff:192.0.2.1`、`64:ff9b::192.0.2.1`、`/64` 用例。

### IT-N53 IPv6 转换：多个 `::` 的非法地址被当作合法并展开（中，确认源码缺陷）
- 描述：`parts.indexOf('')` 只取第一个空段，后续空段被 `filter(p=>p!=='')` 丢掉，只补一次零段，于是出现两个 `::` 的地址也能凑够 8 段。
- 证据：`tools/it/ipv6-converter.html:215-231`
- 复现：`2001::db8::1` → `2001:0000:0000:0000:0000:0000:0db8:0001`（期望报非法，RFC 4291 规定 `::` 每地址最多一次）
- 影响：非法地址被"修正"成合法地址，核对防火墙规则时可能放行错误目标。
- 方案：先统计 `::` 出现次数，>1 直接判非法；再处理零段补齐。

### IT-N54 CRC 计算器：`CRC-8/CCITT` 参数组合非标准，校验值错误（中，确认源码缺陷）
- 描述：`ALGOS` 中该项用 poly 0x07 / init 0xFF / 不反射 / xorout 0x00；标准 CRC-8/ITU（即 CCITT）为 init 0x00 + xorout 0x55（校验值 0xA1），ROHC 为反射 + init 0xFF（0xD0），本组合得 0xFB 不属于任何标准模型。
- 证据：`tools/it/crc-calculator.html:330`（算法参数）、`300-326`（实现）、`377-387`（输出）
- 复现：输入 ASCII `123456789`（未勾选 hex 模式）→ "CRC-8/CCITT: 0xfb"（期望 0xa1；若实现 ROHC 则 0xd0）
- 影响：按名称取值的用户会得到无法与标准实现对齐的校验值。
- 方案：更正为 CRC-8/ITU 参数（poly 0x07, init 0x00, xorout 0x55），另列 CRC-8/ROHC 作为独立项，并用 check 值 0xA1/0xD0 做回归。

### IT-N55 CRC 计算器：十六进制模式不校验奇偶与非法字符，静默丢半字节/归零（中，确认源码缺陷）
- 描述：`getInputBytes` 去掉分隔符后直接按 `s.length/2` 建数组，奇数长度丢掉最后一个半字节；`parseInt` 失败得 NaN，写入 `Uint8Array` 变 0，仍输出"正常"CRC。
- 证据：`tools/it/crc-calculator.html:339-349`（344-346）
- 复现：hex 勾选后输入 `ABC` → 仅按 `AB` 计 1 字节（期望报"半字节数不足"或补 0）；输入 `zz` → 按 `0x00` 计（期望报非法十六进制）
- 影响：用户以为校验的是完整报文，实际少算了尾部或整段被当成 0。
- 方案：先校验仅含十六进制字符与分隔符，且去分隔后长度为偶数；非法/奇数时明确报错并停止计算。

- 备注：`tools/it/timestamp-converter.html:429-435`、`tools/it/color-converter.html:414-423` 的 `switchTab` 依赖全局 `event`（与 IT-N31 同模式，Firefox 可能失效），不重复计数，未单列为新条目。
- 本轮实读 8 页：`tools/it/time-format-converter.html`、`tools/it/timestamp-converter.html`、`tools/it/color-converter.html`、`tools/it/integer-base-converter.html`、`tools/it/chmod-calculator.html`、`tools/it/crontab-generator.html`、`tools/it/ipv6-converter.html`、`tools/it/crc-calculator.html`；新增 16 条（高 3 / 中 10 / 低 3）；未覆盖：`tools/it` 其余非文本页（如 `regex-escape`、`css-minifier`、`html-minifier`、`date-duration`、`ipv4-range-expander`、`punycode`、`user-agent-parser` 等）与全部速查表页；未做浏览器、EN、移动端、门禁或部署验证。
