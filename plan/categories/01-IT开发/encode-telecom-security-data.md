# 编码/通信/安全/数据 · tools/{encode,telecom,security,data}（合计 ~100 页）

> 2026-11-16（692 批已修并核销）：Base32 含/无填充长度与换行口径、CSV→JSON 重复表头/超列/未闭合引号/大整数与前导零、历史恢复模式与清空输入缓存。
> 2026-11-16（693 批已修并核销）：数据透视表合计语义/引号 CSV/HTML 转义/重复表头、CSV 分析多行字段与错列提示。

## 2026-11-06 交互复核：数据清洗格式化承诺未实现（中，确认）

- 基线 `0781ef7e61`；`tools/data/data-cleaner.html:138` 称支持全角转半角、日期归一到 `YYYY-MM-DD`、指定列去重与删除空白单元格；第 259–268、285–303 行实际仅实现整行 trim、去空行、去重、大小写、去特殊字符、排序、打乱、限长，没有分列或上述格式规则。
- 独立 Chrome 输入 `ＡＢＣ` 和 `2026/1/2` 两行并点击“清洗”，输出保持原样；应实现所承诺规则或更正文案。此前关于条数和截断的记录另见本文件旧条目。
- 分桶补证：修改文本后输出仍是原姓名列表，点击“清洗”后才出现新内容，支持该页探针 A；操作开关可单独触发清洗，不代表文本输入实时刷新。

## 优化点
- S1 首屏即答案：编码类页默认给「Hello World」示例的完整编码链。
  - 🟢 S1 全部收口：编码类空输入页已全部具备首屏即答案（qr-decoder 需传图不做）。

## 受影响范围
- tools/encode/、tools/telecom/、tools/security/、tools/data/（合计 ~100 页）

## 2026-11-03 审计补充

### 留存优化：字符转换增加码点解释（低，建议）
- 证据：`tools/encode/convert-4.html:124-126,395-398` 已有字符、码点预设以及复制和 CSV 导出。
- 影响：`tools/encode/convert-4.html`；方案：在现有转换结果旁说明 Unicode 码点与 UTF-8 字节的区别，并为 emoji 场景展示编码字节，避免用户把码点当文件字节；保留现有单击试用与导出。

### 覆盖
- 本轮人工核查编码 1 页 `tools/encode/convert-4.html`；通信 2 页 `tools/telecom/subnet-planner.html`、`tools/telecom/bandwidth-calculator.html`；安全 2 页 `tools/security/virtual-safe.html`、`tools/security/passphrase-generator.html`；数据 2 页 `tools/data/csv-analyzer.html`、`tools/data/csv-to-markdown.html`。仅抽样 7 页，未逐页覆盖其余页面；旧「全部收口」属于历史报告，未独立复验。

### 通信：零地址被拒及输出可带走（中，确认缺陷 + 优化）
- 问题：`tools/telecom/subnet-planner.html:238-255` 将解析结果 0 判为无效，使合法网络地址 `0.0.0.0` 无法按 `/0` 划分；错误地址的空段及非整数也未严格拒绝。
- 方案：严格校验四段十进制整数并区分 `null` 和 0；添加 `0.0.0.0/0`、空段、浮点数测试。
- 留存优化：该页 `:297-312` 已显示最多 1024 条子网但复制仅带摘要；增加带截断标记的完整清单导出和 `/31`、`/32` 用途说明。移动端表格可用性尚未实测。

### 安全：保险箱文本往返损坏（高，确认缺陷）
- 问题：`tools/security/virtual-safe.html:430-465,579,645` 对部分字符先编码再统一 `decodeURIComponent`，改变明文；代理对源码提取的原函数做内存 Node 执行，`%41` 加解密变 `A`，`😀` 加密抛 `URIError`。用户保存或读取文本时可能损坏或无法保存；尚未做页面交互验证。
- 方案：使用标准 UTF-8 编码和可靠的加密/解密实现，保证 `%`、中日韩和 emoji 原样往返；对于现存加密记录先提供明确可验证的读取和迁移路径，防止升级后旧数据不可读取。该工具本身声明教学级简化加密，不把该声明等同专业安全保证。
- 留存优化：该页 `:228-250` 已有加密备份与明文 CSV 导出；增加显式的明文风险提示和备份恢复验证，避免用户误导出敏感内容。

### 数据：CSV 多行字段解析错误（已修，693 批）
- 现状：`tools/data/csv-analyzer.html:235-264` 改为整段引号状态机，支持引号内换行、`""` 转义与 CRLF；`:312-322` 预览对表头/单元格做 HTML 转义，并在字段数与表头不一致时给出「N 行字段数不一致」提示。门禁用例 `data/csv-analyzer` 覆盖多行字段/转义引号/错列三条。

## 2026-11-03 续查：编码、通信、安全与数据

### 紧急联系人用户内容拼入 HTML 与内联脚本（高，确认源码注入路径；浏览器待验证）
- 证据：`tools/security/emergency-contacts.html:453-468,520-530,544-566` 将联系人电话经 `ToolBox.escHtml` 后拼进单引号包围的内联事件，`js/common.js:2022-2025` 的转义是 HTML 文本转义而非 JS 字符串转义；CSV 导出把姓名、电话和备注原样拼进 `innerHTML` 后插入文档。
- 影响：`tools/security/emergency-contacts.html`；恶意联系人内容可能在站点同源上下文执行，触发及浏览器实际表现待验证，不能断言已发生数据外传。
- 方案：用 DOM 节点 `textContent` 和事件监听器生成列表及导出表，不拼 HTML 或事件代码；限制电话格式并分别测试引号、标签、导出及拨打路径。

### 紧急联系人清除后字段可能残留（中，确认源码路径；浏览器待验证）
- 证据：`tools/security/emergency-contacts.html:453-481` 添加和删除仅清空 DOM 或联系人记录；`js/tool-ux.js:24-30,205-245` 对非密码输入和 textarea 的 input/change 单独持久化。程序直接赋值不触发 input；删除后字段缓存可能留在本地。
- 影响：`tools/security/emergency-contacts.html`；姓名、电话和备注可能在共享设备残留，不代表上传。
- 方案：敏感字段默认排除通用缓存；添加、删除和清空时同步清除相关缓存，注明本地留存并测试刷新。

### Base32 长度与填充、换行计算不符（已修，692 批）
- 现状：`tools/encode/base32.html:248-284` 已按「是否含填充」分别输出 ⌈n/5⌉×8 与 ⌈n×8/5⌉，换行只计行间 LF 并分列 CRLF 开销；负字节数/非 0-1 填充/负行宽均拦截且不输出长度。门禁用例 `encode/base32` ×5 覆盖。

### 无线接收功率显示为零（中，确认源码缺陷）
- 证据：`tools/telecom/path-loss.html:253-264` 默认 2400 MHz、1 km、20 dBm、两端各 2 dBi 时约 -76.04 dBm，即约 2.49×10⁻⁸ mW；固定四位小数显示 `0.0000 mW`。
- 影响：`tools/telecom/path-loss.html`；非零功率被读作零。
- 方案：按量级采用科学计数法或自动切换 µW/nW/pW，保留有效数字和 dBm，支持对比不同距离。

### CSV 转 JSON 静默丢列和大整数精度（已修，692 批）
- 现状：`tools/data/csv-json.html:345-450` 重复表头、行内超列、未闭合引号均明确提示并停止转换；前导零与超出 Number.MAX_SAFE_INTEGER 的整数保留字符串。门禁用例 `data/csv-json` 覆盖重复/超列/大整数/未闭合四条。

### CSV/JSON 历史恢复及清空状态不可靠（已修，692 批）
- 现状：`tools/data/csv-json.html:570-583,613-651` 历史记录新增 `__mode` 并在恢复时切回对应模式、更新标签后再 `convert()`（旧实现无参 `setMode()` 抛错被吞）；`clearAll()` 派发 input 事件把通用缓存写成空串。历史表/CSV 导出过滤 `__` 前缀字段。
- 剩余：未在浏览器实测历史恢复与清空后的 localStorage 具体键值。

### 续查覆盖
- 新抽查 `tools/security/emergency-contacts.html`、`tools/encode/base32.html`、`tools/telecom/path-loss.html`、`tools/data/csv-json.html` 4 页，新增 6 条（其中 3 条高优）；源码及局部内存计算证据，未做浏览器、网络或线上验证。

## 2026-11-03 续查（并行批 I）

### I-1 UTF-8 字节数允许负数与小数，产生负字节和误导性膨胀率（中，确认）
- 描述：三个计数输入没有 `min`/整数约束，`calc()` 直接按 `+value` 参与 1/3/4 字节加权；输入负数时分量为负，平均值与“较 ASCII 膨胀”失去物理意义。
- 证据：`tools/encode/utf-8.html:122-124,313-323`；输入 ascii=-100、cjk=20、emoji=5 → 总字节 -20、平均字节/字符 0.27、较 ASCII 膨胀 -73.33%（node 复算，平均分母 -75）。
- 影响：容量估算可被无提示写成负值或错误比例，用于存储/传输预算时会反向低估。
- 方案：给三项加 `min="0"` 与整数校验（或改为粘贴文本自动统计字符类别），负值/小数给出明确提示；补 -1、0.5 用例。

### I-2 Base64 编码长度页“含填充”开关未参与计算，且小数字节产生非整数填充（中，确认）
- 描述：`padding` 被读取后未进入任何公式或输出，页面始终按含填充口径显示；`bytes` 为 `step="any"`，填充数用取模计算，小数输入得到小数个填充字符。
- 证据：`tools/encode/base64-length.html:122-124,259-270`；bytes=100 时 padding=1 与 0 输出完全相同（136 字符 / 2 个填充 / 1 行）；bytes=1.5 → 填充字符数 1.5（node 复算）。
- 影响：用户以为可切换是否含填充，实际结果不随控件变化；小数字节输出无意义的 1.5 个填充字符。
- 方案：padding=0 时改为去填充长度（`4*floor(n/3)+(n%3===1?2:3)`），或在文案明确该开关仅为标记；bytes 改 `step="1"`、强制整数并拒绝负值。

### I-3 JWT 长度按含填充 Base64 计算，且预设把签名“字符数”当“字节数”（中，确认）
- 描述：公式与引据表写明 base64url 去掉尾部 `=`，代码却按 `4*ceil(n/3)` 含填充累加；“简单登录 JWT”预设把 HS256 的 43 字符签名直接填进“签名长度字节”框，被再编码一次。
- 证据：`tools/encode/jwt-size.html:122-124,192-194,318-321,434-437`；header=50/payload=200/sig=32 → 输出 382 字符，去填充应为 379；预设 36/120/43 → 输出 270，而 43 字符签名对应令牌 253（node 复算）。
- 影响：请求头/Cookie 体积预算每段偏大 1–2 字符，预设场景偏大约 17 字符，且与页面自述口径矛盾。
- 方案：按每段 `n%3===0?4n/3:4*floor(n/3)+(n%3===1?2:3)` 去填充计算；签名输入明确为“字节数”，预设填 32/64，或增加“签名已是 base64url 字符数”选项。

### I-4 BER→Eb/N0 反解被 0 dB 下界截断，低信噪比目标给出错误 0.00 dB（中，确认）
- 描述：二分区间固定 lo=0，而 BER 输入允许 (0,1)；当目标 BER 高于 0 dB 对应的 BER（BPSK/QPSK 约 7.87×10⁻²）时，解应落在负 dB，算法只能返回 0 dB，且“校验”行仍写“与目标一致”。
- 证据：`tools/telecom/ber-snr.html:261-269,295-310`；BPSK、BER=0.1 → 输出 `所需 Eb/N0 ≈ 0.00 dB`，反算 BER=7.865e-2（实际约 -0.86 dB）；BER=0.5 同样返回 0.00 dB（node 复算）。
- 影响：极高误码率场景的所需 Eb/N0 被高估（可达约 1 dB），校验文案掩盖偏差。
- 方案：二分下界改为 -20（或按各调制 BER→0.5 的极限取负值），超出可解范围时明确提示；校验行按实际反算值比对，不一致时提示。

### I-5 AP 覆盖页深度解析的“室内密集”半径与页内公式不符（中，确认）
- 描述：算例先用 office(+8 dB) 得 125 m，再称改“室内密集(+15 dB)”降至约 76 m；同参数按页内 FSPL 反解应为 55.9 m。
- 证据：`tools/telecom/ap-coverage.html:189,245-252`；Pt20/Gt3/Gr2/Pr_min−75/f2400/extra0/fade10 → office MAPL 82.00、125.3 m；dense MAPL 75.00、55.9 m（node 复算），页面写 76 m。
- 影响：布点密度参考值偏差约 36%，与同页公式自相矛盾。
- 方案：把 76 m 更正为 55.9 m（同步直径），或补充 76 m 采用的额外假设；增加“按公式复核算例”的校验。

### I-6 YAML→JSON 对“列表项多键对象”静默丢键（高，确认）
- 描述：解析 `- key: value` 后只前进一步，随后遇到更深缩进的同级键即 `break`，导致 `- name: Tom` 后面的 `age: 3` 被丢弃且不报错。
- 证据：`tools/data/yaml-json.html:329-390`（343 行 `lineIndent !== indent && !startsWith('-')` 直接 break）；输入 `list:\n  - name: Tom\n    age: 3` → `{"list":[{"name":"Tom"}]}`（node 抽取源码执行）。
- 影响：K8s/CI 常见的“列表内多键对象”转换后缺字段，下游直接消费会丢配置。
- 方案：列表项命中 `key:` 后以该项缩进为基准继续收集同级键，直到缩进回退；增加“列表项含 2+ 键”和嵌套列表用例，丢键时显式报错。

### I-7 YAML→JSON 的行尾注释、块标量与带引号键值被误解析（中，确认）
- 描述：只跳过整行注释，行尾 `# …` 并入标量；`|`/`>` 走嵌套对象分支，正文行无冒号被跳过，块内容变 `null`；数组项按第一个 `:` 切分，引号内冒号被当作键值分隔。
- 证据：`tools/data/yaml-json.html:339,375-379,346-361`；`host: localhost # note` → `"localhost # note"`；`msg: |\n  hello` → `{"msg":null}`；`- "a:b"` → `{"\"a":"b\""}`（node 抽取源码执行）。
- 影响：含注释、多行脚本、URL/时间的 YAML 会被静默改值或丢段。
- 方案：按 YAML 1.2 处理引号外的行尾注释、实现 `|`/`>` 块标量、先识别引号再找分隔冒号；无法支持时提示“不支持该语法”而非静默转换。

### I-8 JSON→YAML 不转义特殊字符键，混合引号时生成非法 YAML（中，确认）
- 描述：对象键原样输出；值同时含 `'` 与 `"` 时走单引号包裹但未把内部 `'` 翻倍。
- 证据：`tools/data/yaml-json.html:301-312,316-322`；`{"a: b":1}` → `a: b: 1`；`{"k":"it's \"x\""}` → `k: 'it's "x"'`（node 复算），两者均非合法 YAML。
- 影响：从 JSON 生成的 YAML 交给解析器会报错，用户难以定位是键还是引号问题。
- 方案：键也走 `yamlString()`；单引号风格时把内部 `'` 替换为 `''`，或统一双引号并转义；补特殊键与混合引号用例。

### I-9 YAML/JSON 方向切换高亮错按钮（低，确认）
- 描述：`setDir()` 用 `.dir-tabs button` 的下标判断，但该容器第 2 个按钮是“导出明细 CSV”，因此切到 YAML→JSON 时高亮的是导出按钮，“YAML → JSON”永不高亮。
- 证据：`tools/data/yaml-json.html:156-159,269-275`（`(d === 'y2j' && i === 1)`）。
- 影响：用户无法从高亮判断当前方向，易在错误方向粘贴数据。
- 方案：给两个方向按钮加独立 id 或 `data-dir`，按属性切换 `active`，不要用下标。

### I-10 数据透视表把单元格内容直接拼入 innerHTML（已修，693 批）
- 现状：`tools/data/pivot-table.html:295-299,353-375` 新增 `escPivot()`，表头、行/列分组值与聚合名统一转义后再拼入表格；门禁用例注入 `<img onerror>` 断言输出为实体。

### I-11 数据透视表 avg/min/max 的“合计”列与总计行算错（已修，693 批）
- 现状：同页 `:332-351` 每格保存原始数值与计数，行/列/总计都用 `aggregate()` 合并原始值后按同一语义重算（avg 加权、min/max 取极值、count 计数、sum 求和）。用例锁定 avg=126.00、min 行/列/总计。

### I-12 数据透视表 CSV 按逗号切分，忽略引号与重复表头（已修，693 批）
- 现状：同页 `:273-316` 新增 `parsePivotLine()` 支持引号包裹与 `""` 转义，行分隔兼容 CRLF；重复表头给出提示并停止透视。用例覆盖带逗号字段（北京,朝阳）与重复列名。

### I-13 数据清洗“原始条数”含尾部空行，限长按 UTF-16 截断 emoji（已修，693 批）
- 现状：`tools/data/data-cleaner.html:274-308` 先统一 CRLF 并弹出末尾空行再计原始条数；限长改为按字形簇（Intl.Segmenter，缺失时退化为码点）截断，不再切出孤立代理项。门禁用例 `data/data-cleaner` 锁定 `abc\n\n → 1` 与 `😀ABC 限长 1 → 😀`。


### 留存优化
- `tools/encode/utf-8.html:131-135` 公式列了 4 档（含 2 字节拉丁/希腊），但只有 3 个输入，无 2 字节与组合 emoji 入口；可增加“2 字节字符数”或直接粘贴文本自动分档，并在结果旁对比字符数/字节数/码点数。
- `tools/encode/base64-length.html:164-169` 深度解析提到 MIME 每 76 字符折行，但结果只给行数不含 CRLF 开销；可并列“纯字符数 / 含 CRLF 实际传输字节”，并同时展示有/无填充两种口径。
- `tools/encode/jwt-size.html:164-165` 算例写“header+payload 各 120 字节、签名 32 → 约 250 字节”，按页内公式实为 366（去填充 365）；建议用真实 HS256/RS256 示例重算，并提示输入是 JSON 字节而非字符。
- `tools/telecom/ber-snr.html:155-165` 只给 BPSK 与 M-QAM 近似式，未说明适用 SNR 区间与 Gray 映射假设；可在结果旁标注“理论值/高 SNR 近似”，并给出 BER=0.5 与负 Eb/N0 的边界示例。
- `tools/telecom/ap-coverage.html:266` 覆盖评级只看半径绝对值，未区分室内/室外与频段；建议按环境给不同阈值，或展示“留 30% 余量”的保守半径并提示需现场勘测。
- `tools/data/yaml-json.html:153,578` 简介仍为“单位与格式换算/SI 单位制”套话，与工具无关；`__yaml_jsonPresets` 为空却保留“预设”页签。建议改写简介、移除空页签或补 K8s/CI 示例预设。
- `tools/data/pivot-table.html:241` FAQ 称空值“通常忽略”，但 count 按匹配行计数、sum/avg 过滤非数值，口径不一致；建议在结果区固定展示每组“有效值/空值/非数值”数量。
- `tools/data/data-cleaner.html:259-268,296` “去非字母”实际保留数字与汉字，文案与行为不符；建议改名“去特殊字符”，或提供“仅字母/字母数字/含汉字”选项。

### 续查覆盖
- 本轮新抽查 8 页：`tools/encode/utf-8.html`、`tools/encode/base64-length.html`、`tools/encode/jwt-size.html`、`tools/telecom/ber-snr.html`、`tools/telecom/ap-coverage.html`、`tools/data/yaml-json.html`、`tools/data/pivot-table.html`、`tools/data/data-cleaner.html`；与前两批已覆盖的 convert-4、subnet-planner、bandwidth-calculator、virtual-safe、passphrase-generator、csv-analyzer、csv-to-markdown、emergency-contacts、base32、path-loss、csv-json 不重复。
- 新增 13 条（高 3 条 I-6/I-10/I-11、中 9 条、低 1 条）。证据为源码行号与 node 内存执行页面函数复算；未开浏览器，未做英文态/移动端/门禁或线上验证。
