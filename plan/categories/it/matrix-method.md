# IT 分类「同族可逆性矩阵」审计方法

> 适用：编码 / 转义 / 校验器 / 时间 / 进制 / 字符集等「有标准答案」的族。
> 核心：**不读代码自证，用独立标准实现回解并逐字节比对。**

## 一、判据句式

> **正向编码 → 用独立标准实现解码 → 与原文逐字节比对。**

三条补充口径：

1. **逐字节，不逐字符**：多字节编码（UTF-8、Base32、Base85）只有按字节比对才能发现「末组丢字节」「填充位非零」这类静默错误。
2. **同族同输入**：同一族用同一组向量（空串 / 纯 ASCII / 中文 / emoji / 混合 / 超长 / 边界），保证结论可横向对比。
3. **边界必测**：URL-safe 变体（`-_` vs `+/`）、有无填充位（`=`）、BOM、前导零、负号、超 2⁵³ 大数、DST 跳变日、代理对与孤立代理。

## 二、三类结论

| 结论 | 含义 | 页面动作 |
|---|---|---|
| **可逆且精确** | 与独立实现逐字节一致 | 无需改动，记录进矩阵 |
| **可逆但需口径说明** | 结果正确，但受选项/实现语义影响（如 URL-safe、裸 Punycode 不可逆、JS 本地时区解析） | 页面明示口径，不改算法 |
| **不可逆（须页面明示）** | 输出丢失信息或静默误判（如 `parseInt('1g',16)`→1、`BigInt('0x10')` 在十进制模式算成 16、`\x` 贪婪吞 hex） | 修实现；确实无法修的（命名实体表有限）在页面写明边界 |

判定纪律：

- **静默错误优先于报错**：会给出错答案的路径（静默误解码、静默截断）比直接报错的路径危险一个等级。
- **同族口径必须一致**：两个同族页面（`number-base-converter` / `integer-base-converter`、`timestamp-converter` / `time-format-converter`）对同一输入必须给同一结论；不一致就统一或双页明示。
- **校验器不强行统一算法**：只统一「措辞模板」，各页保留自己的真实上限。

## 三、外部参照清单（可直接复用）

| 参照 | 覆盖能力 | 用法 |
|---|---|---|
| Python `base64` / `binascii` | Base16/32/64 | `b32encode`、`bytes.hex()` |
| Python `base64.a85encode(adobe=True)` | Ascii85 | 含 `z` 缩写与末组截断 |
| Python `quopri` | Quoted-Printable | `encode`/`decode` 往返 |
| Python `codecs` + `TextDecoder` | UTF-8 / GB18030 / Big5 / UTF-16 | 严格模式（fatal）确认「能否解」 |
| Python `datetime` / `zoneinfo` | 时区偏移、DST 边界、ISO 周 | 每个时区至少 2 个 DST 边界日 |
| Python `int(s, base)` | 任意进制大数 | 2⁵³ 以上逐位比对 |
| Python `ast.literal_eval` | Python 字面量转义 | 3 引号 × escape/raw |
| Node `Buffer` / `encodeURIComponent` / `punycode` | Base64、URL 编码、Punycode | 与页面输出逐字节比对 |
| Node `vm.runInNewContext`（严格模式） | JS 转义 | 只做解码验证，不执行业务代码 |
| `javac` + 运行 | Java 转义 | 2 模式 × 10 向量 |
| `cc -std=c11 -fexec-charset=UTF-8` | C 转义 | 逐字节 `printf("%02x")` |
| 独立手写参考实现 | Base58 / Z85 | 三套字母表 / 两种变体 |

无本地工具链时（Go / PHP / Rust）：按语言规范静态核对，并在矩阵里标注「规范核对（未编译）」。

## 四、各族速查要点

- **时间族**：位数分档必须同族一致（≤10 秒 / 11–13 毫秒 / 14–16 微秒 / 17–19 纳秒），纯数字串**不得回落给 `new Date()`**（会被当 ISO 年份）；年积日按 `Date.UTC` 归一计算，禁止毫秒差整除（DST 后少一天）；无偏移本地时间落在 DST 缺口时浏览器会顺延，须页面明示。
- **进制族**：全程 BigInt；十进制分支必须 `^[0-9]+$`（`BigInt('0x10')` 会算成 16）；正负号、前导零、`0x/0b/0o` 前缀口径同族一致。
- **字符集族**：区分「字节串识别」与「双重编码还原」；GBK 与 GB18030 同一解码器、不可区分；GB18030 与 Big5 区间重叠，短文本只能给并列结论；含 U+FFFD 即信息已丢失。
- **编码族**：Base85 的 `z` 仅限完整 4 字节全零组；Base32 末组符号数 %8 ∈ {1,3,6} 即不完整。
- **转义族**：C 的 `\x` 贪婪；C 的 UCN `\u0080` 非法；Rust 字节串禁止 `\u{...}` 与非 ASCII；Python raw 串禁止 NUL 与跨行；`\0` 后接数字会变遗留八进制。
- **校验器族**：行列号统一 1-based，措辞统一为「行列号从 1 开始；本页深度上限 X；输入上限 Y」，深度/体积的真实差异照实写。

## 五、收尾

改页面同批改 `scripts/verify_it_calc.js`（每个缺陷至少一条可判别用例，`ref` 写独立参照来源）；提交用带路径 `git commit -- <路径>`，单笔 ≤30 文件；构建与推送由集成线统一执行。

## 六、结构化文本族矩阵（2026-11-05）

> 范围：`tools/it/**` 中 JSON / XML / YAML / CSV / HTML 转义与清洗 / 文本 diff / 正则 七族，共 46 页。
> 外部参照：Python `json` / `tomllib` / `xml.etree.ElementTree` / `csv` / `html.escape`、Ruby Psych（libyaml，YAML 1.1 与 1.2 core 双口径）、Node `JSON` / `RegExp`（含 `vm` 验证 JS 转义）、`CSS.escape` 语义。
> 回解向量：空串 / 纯 ASCII / 中文 / emoji / 混合 / 嵌套对象与数组 / null / 前导零 / `0x` `0b` / 指数大数 / 含 `: ` `#` `- ` `? ` / 空键 / 键含空格冒号换行 / CRLF / BOM / 引号内逗号与换行 / 未闭合引号。

| 族 | 页数 | 真缺陷 | 声明超出 | 一致 |
|---|---|---|---|---|
| JSON | 13 | 2 | 1 | 10 |
| XML | 5 | 0 | 3 | 2 |
| YAML | 5 | 0 | 4 | 1 |
| CSV | 5 | 3 | 1 | 1 |
| HTML 转义与清洗 | 8 | 0 | 1 | 7 |
| 文本 diff/清洗 | 5 | 1 | 0 | 4 |
| 正则 | 5 | 1 | 0 | 4 |
| **合计** | **46** | **7** | **10** | **29** |

### 6.1 真缺陷（已修，同批补 verify 用例）

| 页面 | 根因（外部参照回解结论） | 修法 | 用例 |
|---|---|---|---|
| `json-to-yaml` | 空串裸写被 YAML 解析成 `null`；`- item` / `? key` 被当序列项与复杂键；`.inf`、日期形态被解析成非字符串；键为空或含 `:` 时产出非法 YAML；`1e+21` 在 YAML 1.1 解析器（PyYAML/Psych）下退化为字符串 | 新增 `yamlPlainSafe` / `yamlScalar` / `yamlNum`：键与字符串按需双引号，空串输出 `""`，指数补 `.0` | IT-N22 |
| `json-to-toml` | TOML 无 null，原实现静默输出 `""`（类型被改写）；对象与标量混排的数组退回 `JSON.stringify` 产出 `[{...}, 2]`（非合法 TOML） | 两条路径改为显式报错，不静默改写 | IT-N23（2 条） |
| `csv-to-html-table` | 字段中间的 `"` 被当成引用段起点，吞掉后续逗号（`x"y,2` 变成单格 `xy,2`） | 仅字段起始位置的双引号开启引用段 | IT-N25 |
| `csv-to-yaml` | 先按行切分再解析，引号内换行被拆成两条记录；表头裸写（含空格/冒号时 YAML 非法） | 改为整段 RFC 4180 扫描（引号内允许逗号/换行），表头键按需双引号 | IT-N26 |
| `csv-validator` | 末尾空行被当成单列记录，误报「列数 1（应为 2）」；字段中间 `"` 同样误开引用段 | 跳过空白行（行号仍按物理行推进）；引号仅字段起始生效 | IT-N24 |
| `regex-escape` | 非法 `\x` / `\u` 走 `String.fromCodePoint(NaN)` 抛 RangeError，按钮无输出；ES2015 `\u{...}` 未支持 | 先校验十六进制与码点上限，非法转义原样保留；支持 `\u{...}` | IT-N21（2 条） |
| `text-dedupe-sort` | 用普通 `{}` 做集合，`__proto__` / `constructor` 行从 `Object.prototype` 继承后恒为真值，首行即被静默丢弃 | 集合改为 `Object.create(null)` | IT-N20 |

门禁：`verify_it_calc.js` 944/944 通过；legacy discriminate 943 已检 / 0 逃生；`TB_STUB_FIDELITY=1` 940 已检 / 0 逃生；`selfcheck_false_pass` 的 `all_default=0`（不高于基线）。

### 6.2 声明超出实现（登记，不因好看改口径）

| 页面 | 超出的声明 | 实测边界 |
|---|---|---|
| `json-to-xml` | 「JSON 转 XML」 | 顶层数组按「同名标签重复」输出多个同级根元素 ⇒ 是 XML 片段而非单一良构文档；页面未写明这一点 |
| `xml-to-json` / `xml-to-yaml` / `xml-to-toml` | 共用 `parseEl` 的 XML→结构转换 | 混排内容（`<p>Hello <b>world</b>!</p>`）只取子元素、丢弃同级文本；叶节点 `trim()` 丢首尾空白 |
| `yaml-to-json` / `yaml-to-toml` / `yaml-to-xml` / `yaml-formatter` | 共用行式 `parseYaml`，文案称 YAML 转 JSON/TOML/XML | 不支持流式集合（`a: [1,2]` → 字符串 `"[1, 2]"`）、引号键（`"a:b": 1` → 键被拆坏）、块标量（`\|` 后内容全丢）；属静默类型/内容变化，需整解析器才能修 |
| `csv-to-json` | CSV 转 JSON 对象 | 数据行字段多于表头时，多余列被静默丢弃（仅按表头映射） |
| `html-entities-encode` | 「反向解码还原」 | 解码仅覆盖内置常用命名实体表，表外命名实体原样保留 |

### 6.3 一致（含口径说明）

- **JSON（10）**：`json-formatter` / `json-minify` 走 `JSON.parse`+`JSON.stringify`，与 Node `JSON` 一致；`json-to-csv` 全字段双引号 + `""` 转义，Python `csv` 可回读；`json-to-tsv` 按选项把制表符/换行替换为空格（已声明）；`json-diff` / `json-path` / `json-repair` / `json-schema-generator` / `json-schema-validator` / `json-to-code` 为自定义子集/启发式，结论与页面声明一致。
- **XML（2）**：`xml-formatter`（缩进/压缩）、`xml-validator`（结构校验）。
- **YAML（1）**：`yaml-validator` 用内置 js-yaml（`loadAll` 支持多文档），与标准解析器一致。
- **CSV（1）**：`list-converter` 按行/分隔符转换，属文本列表语义而非 RFC 4180，口径自洽。
- **HTML（7）**：`html-escape`（转义 + textarea 反解，与浏览器实体解码一致）、`html-entity-encoder`（编码 + 浏览器反解）、`html-entities`（速查表 + 编码，解码仅 6 个命名实体但文案未承诺完整解码）、`html-minifier`（保护 `pre/textarea/script/style` 与属性值）、`html-nesting-checker`、`html-tags`（速查表）、`html-to-markdown`（自定义降级，已声明）。
- **文本（4）**：`text-diff`（行级 LCS + 修改配对）、`text-similarity`（按码点 Levenshtein，空输入已守卫）、`text-cleaner`、`whitespace`（末尾换行的空片段计入「空行数」属统计口径，不影响输出）。
- **正则（4）**：`regex`（Worker 内直接跑原生 `RegExp`，与 Node 语义一致，含零长匹配保护）、`regex-cheatsheet` / `regex-common`（速查表）、`regex-visualizer`（基于正则源的可视化，口径自洽）。

### 6.4 未纳入本族

哈希 / 编码 / 进制 / 时间 / 字符集族已在前几批收口；TOML/INI/properties/plist 独立格式页未在本族枚举范围内，留待后续批次（`json-to-toml` 作为 JSON 源页已审）。

## 七、网络与协议族矩阵（2026-11-05）

> 范围：`tools/it/**` 中 URL 解析/编解码、HTTP 头与状态码、Cookie、CIDR/子网、MIME、JWT、UA、端口/协议速查、Referer/redirect 九族，共 20 页（`it/ip-calculator` 按任务约定排除，归交互异常线）。
> 外部参照：Node `URL` / `URLSearchParams` / `punycode`、Python `urllib.parse` / `http.cookies` / `ipaddress`（`ip_network` 严格模式 + `/31` `/32` 特例）/ `mimetypes`、RFC 7230/9110（HTTP）、RFC 6265（Cookie）、RFC 3021（/31）、RFC 4291/5952（IPv6）、RFC 7519（JWT）、RFC 7617（Basic Auth）。
> 回解向量：空串 / 纯 ASCII / 中文 / emoji / 空格与 `+` / 畸形百分号 `%` / 前导零八位组 / `/31` `/32` `/0` / 内嵌 IPv4 / `__proto__` 与 `constructor` 键 / `exp=0` / 真实 iOS 与三星 UA 串。

| 族 | 页数 | 真缺陷 | 声明超出 | 一致 |
|---|---|---|---|---|
| URL 解析/编解码（含 Punycode） | 5 | 2 | 1 | 2 |
| HTTP 头与状态码 | 5 | 0 | 1 | 4 |
| Cookie | 1 | 0 | 1 | 0 |
| CIDR/子网 | 4 | 3 | 0 | 1 |
| MIME/Content-Type | 1 | 0 | 0 | 1 |
| JWT | 2 | 2 | 0 | 0 |
| UA 解析 | 1 | 1 | 0 | 0 |
| 端口/协议速查 | 1 | 0 | 0 | 1 |
| Referer/redirect | 0 | 0 | 0 | 0 |
| **合计** | **20** | **8** | **3** | **9** |

### 7.1 真缺陷（已修，同批补 verify 用例）

| 页面 | 根因（外部参照回解结论） | 修法 | 用例 |
|---|---|---|---|
| `url-params` | `decodeURIComponent` 遇畸形 `%` 抛 URIError，整段解析中断、结果停在默认示例；Python `parse_qs` / `URLSearchParams` 均把非法转义按字面 `%` 保留 | 逐段 `try/catch`，失败回退字面值；`collectPairs` 改用 `Object.create(null)` | IT-N28 |
| `url-parser` | `params` 用普通 `{}`，`?__proto__=x&constructor=y` 走原型 setter，JSON 导出丢键（表格行仍在） | `Object.create(null)` | IT-N27 |
| `ipv4-range-expander` | ① `/31` 报 0 个可用主机（RFC 3021 为 2，且与 `it/calc-subnet` 自相矛盾）；② `/32` 报 0 且不输出范围（Python `ipaddress` hosts=1）；③ `+octet` 接受空段、前导零、`0x1`、浮点形态，静默误解析 | `/31=2`、`/32=1` 分支；八位组改 `^\d{1,3}$` + 禁前导零 | IT-N29（3 条） |
| `calc-subnet` | `/32` 硬编码可用主机 0，与 Python 3.8+ `hosts()` 返回该地址本身不符 | `/32` 可用数改 1 | IT-N30 |
| `ipv6-converter` | 内嵌 IPv4 的八位组用 `Number('001')=1`，接受前导零（RFC 3986 / `ipaddress` 均拒绝） | 八位组校验加前导零拒绝 | IT-N31 |
| `user-agent-parser` | iOS 上 Chrome/Firefox/Edge/Opera 的 `CriOS`/`FxiOS`/`EdgiOS`/`OPiOS` 无 `Chrome/` 或 `Version/`，落入「未知浏览器」；三星浏览器含 `Chrome/` 被误报为 Google Chrome | 新增 5 条 UA 分支与对应版本号提取；SamsungBrowser 先于 Chrome | IT-N32（2 条） |
| `jwt-parser` / `jwt-debugger` | `if(payload.exp)` 把合法的 NumericDate `exp=0` 当 false，漏报「已过期」并漏 `exp_human`（RFC 7519） | 改 `typeof payload.exp === 'number'`，`iat`/`nbf` 同口径 | IT-N33（2 条） |

门禁：`verify_it_calc.js` 971/971 通过；legacy discriminate 970 已检 / 0 逃生 / 1 跳过；`TB_STUB_FIDELITY=1` 967 已检 / 0 逃生 / 4 跳过；`selfcheck_false_pass` 的 `all_default=0`（与基线持平，预存 risk 3 未触碰）。

### 7.2 声明超出实现（登记，不因好看改口径）

| 页面 | 超出的声明 | 实测边界 |
|---|---|---|
| `punycode` | 「IDN 国际化域名编码（RFC 3492）」 | 只做 RFC 3492 裸 Punycode：不做 IDNA nameprep/大小写折叠。`Bücher` → `Bcher-kva`，而浏览器/`domainToASCII` 得 `bcher-kva`；全角字符也不会先做 NFC 归一 |
| `http-methods` | TRACE「已废弃」 | RFC 9110 §9.3.8 仍定义 TRACE，仅因 XST 风险常被服务器禁用；状态应为「诊断用途、通常禁用」而非「废弃」 |
| `http-cookies` | 英文简介称 “Parse and build HTTP Cookie…” | 实际是 Cookie/Set-Cookie 属性速查表 + JS 操作说明，没有输入框、不解析也不构造任何头 |

### 7.3 一致（含口径说明）

- **URL（2）**：`url-encode` 直接调用原生 `encodeURIComponent` / `encodeURI`（与浏览器逐字节一致，空格→`%20` 或按开关 `+`）；`url-encoder-advanced` 同样走原生函数，仅按选项切换函数，口径自洽。
- **HTTP（4）**：`http-headers` / `http-response-headers` / `http-status` / `http-cache` 为速查表，抽样核对 RFC 7230/9110 与 RFC 9111（`immutable` 的边界描述正确：「max-age 期间连条件请求也不发」）；`http-status` 的 422 保留 WebDAV 旧名 “Unprocessable Entity”，语义与 RFC 9110 新名 “Unprocessable Content” 相同，属命名沿革，不构成错误。
- **CIDR（1）**：`ipv6-ula` 按 RFC 4193 生成 `fd` + 40-bit Global ID（12 个十六进制位拼成 3 段）；用 `Math.random` 而非 CSPRNG，统计随机性满足 ULA 用途（未承诺密码学安全）。
- **MIME（1）**：`mime-type` 表逐项对照 IANA 注册表，均取现行注册名；与 Python `mimetypes` 的差异集中在平台历史别名（如 `image/x-icon`），页面值更贴近 IANA。
- **端口（1）**：`random-port-generator` 在 1024–65535 内取值、可选跳过常用保留端口，逻辑与声明一致。
- **Referer/redirect（0）**：本目录没有 Referer/重定向解析页；`short-link-generator` 只是本地短链生成器，未解析 301/302，故不纳入本族。

### 7.4 未纳入本族

`it/ip-calculator` 按任务约定排除；Basic Auth 生成器（RFC 7617）与 curl 命令解析器做了抽样核对（UTF-8 凭据 / 引号与 `-H`/`-d` 合并），未发现与声明不符的静默错误，故未单列族行。

## 八、全站「对象当 Set/Map」排查（2026-11-05）

> 触发：`it/text-dedupe-sort` 的 `__proto__` 被 `Object.prototype` 误判。口径：只有「键来自用户可控输入（文本行、标签、字段名）」才算风险；页面内固定枚举键 / DOM id / 数值键不算。

| 指标 | 数量 |
|---|---|
| 初筛命中（`obj[k]=` / `obj[k]=true` / `seen[k]` / `if(obj[k])` 写法） | 约 3,600 处，涉及 200+ 文件 |
| 真风险页（键来自用户文本/键名） | 19 |
| 已修（含前批 `text-dedupe-sort`） | 16 |
| 登记待修 | 3 |

已修（本批 15 页 + 前批 1 页）：`it/url-parser`、`it/url-params`、`it/ini-parser`、`it/properties-parser`、`it/toml-formatter`、`it/xml-to-json`、`it/xml-to-yaml`、`it/xml-to-toml`、`it/yaml-to-json`、`it/yaml-to-toml`、`it/yaml-to-xml`、`it/yaml-formatter`、`it/csv-to-json`、`it/json-schema-generator`、`it/toml-to-yaml`、`it/text-dedupe-sort`（前批）。统一改为 `Object.create(null)`（或保留键仍走自有属性），并补 `__proto__` / `constructor` 输入用例（IT-N27 / IT-N34 系列）。

登记待修（3 页，未纳入 Top 10 扩展批次）：

| 页面 | 写法 | 触发键 |
|---|---|---|
| `biz/text-remove-duplicates-lines` | `seen[key]` | 整行文本可以是 `__proto__` / `constructor` |
| `biz/text-extract-english` | `seen[key]` | 英文单词 `constructor` 是合法命中词 |
| `research/analysis-54` | `freq[t]` / `seen[t]` | 分词后 token 可为 `constructor`（代码类文本） |

不算风险（固定键 / 数值键 / 不可产出魔法名）：`it/ipv6-ula`、`it/mime-type`（表为数组 filter）、`it/jwt-*`（固定字段）、`it/curl-parser`（固定字段）、`tools/quality/control-chart`（数值键）、`biz/text-extract-dates`（日期形态键）、`biz/text-extract-urls`（URL 形态键，不会恰为 `__proto__`）。


## 九、「`x || 默认值` 吞 0」与输入事件缺失（2026-11-05）

> 口径：只有空串 / NaN 才回退默认值；0 是合法值必须原样进入计算；定义域确实排除 0 的（数量、长度）显式拒绝并给原因，不静默改成默认值。

| 页面 | 原缺陷 | 注入 0 后的输出（修复后） |
|---|---|---|
| `it/random` | `max \|\| 100` 把上限 0 当假值回退 100 | min=-5 / max=0 / count=1 → `-4`（落在 [-5,0]）；count=0 → 「生成数量须为不小于 1 的整数」 |
| `it/vector-magnitude` | 6 处 `m \|\| 1` 把零向量分母改成 1 | (0,0,0) → 「零向量无方向余弦与方向角」；2D 零向量 → 「零向量无方向角」；非零 (3,4,0) 仍为 cos α=0.6 / β=0.8 / γ=0 |
| `it/random-string` | `parseInt(value\|\|'5')\|\|5` 双段兜底 | cnt=0 → 「生成数量至少为 1 个」；len=0 → 「长度至少为 1 位」 |
| `it/json-to-tsv` | 根因 **① 事件没绑**：仅在页面加载末调用一次 `jsonToTsv()`，textarea 无 `input` 监听 | 改成合法 JSON 数组即自动重算（静默模式不写历史/不弹 toast），表头、数据行与行列统计同步刷新 |

门禁：`verify_it_calc.js` 977/977；legacy 判别 976 已检 / 0 逃生 / 1 跳过；fidelity 973 已检 / 0 逃生 / 4 跳过；`all_default=0`（risk 3 为既有 `calc-2`、`vector-dot-product`、`vector-magnitude`，未新增）。
