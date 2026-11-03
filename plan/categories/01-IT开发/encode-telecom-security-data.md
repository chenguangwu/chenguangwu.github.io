# 编码/通信/安全/数据 · tools/{encode,telecom,security,data}（合计 ~100 页）

## 已知问题
### E1. encode 系结果仅文本
- ✅ 已落地（2026-10-26 · 落点 it/char-encoder 多格式字符编码器）：加「🔬 字节视图」卡（#byteViewBox：字符 ↔ 码点 ↔ UTF-8 字节 hex/binary 逐字符对照表，空格␣/换行⏎/制表⇥符号化、截前 64 字符、TBKit EN 守卫双语；空输入清空零渲染）。verify 强用例（Hi中 → U+4E2D e4 b8 ad 11100100…）；EN probe 全英文（输入回显除外）。verify it 763/763、判别器 0 逃生、门禁 218/218。

### E2. telecom 换算页口径混杂
- ✅ 已落地（2026-10-26）：bandwidth-calculator KB 选项 0.001→1/1024（byte 系统一 1024，GB/TB 原本已 1024）+ 「bit 系 1000 / byte 系 1024」口径标注（data-zh 双语）；quick-calc-time-bandwidth formula-eq 80 秒（1000 进制）与案例 91 秒（1024 进制）矛盾消除标注。verify 强用例（2048 KB=2.00 MB，clicks 直调）；verify telecom 11/11、判别器 0、门禁 218/218。

### E3. security 模拟器类内容单薄
- ✅ 已落地（2026-10-26 · data-erase-simulator）：加「📚 标准依据」徽标（#standardBadge 随选中算法切换：零填充→NIST 800-88 Clear 级 / 随机→Clear/Purge 过渡 / DoD→NIST 已不推荐说明 / Gutmann→1996 论文局限+建议加密擦除），对比表与 CSV 导出加「标准依据」列，页脚 NIST 800-88 Rev.1 三级别说明（data-zh 双语 + GEN_UI_MAP 映射）。⚠ 同批修两条弱锚：老用例锚「24」是 byteGrid 随机字节概率性回显（撞值即逃生）→ 收紧为 startSim 同步渲染的确定性步骤锚；新用例锚须带「标准依据」badge 专属前缀（compareTable 全算法列会把引据文本带进默认态）。verify security 11/11、判别器 0 逃生、门禁 218/218。
- ✅ 已落地（2026-10-26 · smoke-alarm-test / virtual-safe）：smoke-alarm 加 #alarmStdBadge 随报警器位置切换引据（GB 20517-2009 产品标准 + GB 50016 设置场所 + NFPA 72 每月测试，8 位置各配专属安装/选型文案，select onchange + 预设按钮联动，TBKit helper 双语）；verify +2 强位置锚（厨房附近「距烹饪区至少 3 米」/地下室「烟气易积聚」——badge 通用引据渲染不依赖输入，不可作 expect）。virtual-safe 加静态 NIST 800-63B/OWASP 标准徽标（data-zh，无 id 不进 blob 零用例影响）+ updateStrength 追加 NIST 长度建议动态行（masterPwd addEventListener input 在 stub 可触发）；verify +1 强锚。verify security 14/14、判别器 0、门禁 218/218。

## 功能缺陷
- ✅ 自定义多项式已落地（2026-10-26）：`it/crc-calculator` 加「自定义 CRC 模型」块（checkbox 默认关 ⇒ 零渲染；width 8–64/poly·init·xorout hex/refin·refout 勾选，复用 crcGeneric 在 8 标准算法后追加一行）；__gv 防御 harness stub 对静态 input .value 不解析 attribute 的坑。verify 自洽用例（CRC-8 参数+abc → 0x5f 与内置一致）；GEN_UI_MAP 补 7 条 label。verify it 764/764、判别器 0 逃生、门禁 218/218。（既往疑点已定性 2026-10-26：blob 中「undefined 0xundefined」×2 卡是 harness 兜底步骤无参直调 `renderResult()` 的伪影，真实浏览器无此调用路径，页面 8 张标准卡计算全对，无需改动。）

## 优化点
- S1 首屏即答案：编码类页默认给「Hello World」示例的完整编码链。
  - ✅ 试点落地（2026-10-26 · it/url-encode）：textarea 默认样例 `https://toolbox.example.com/search?q=你好 世界` + `__url_encodeFirstRender()` boot 静默首渲染（encodeURIComponent、output 空才写、不写历史不弹 toast）。同批修 1 条 B 类快照用例漂移（blob 段序变化 → 隔离 fullBlob 实测重写，判别力保持）。verify it 766/766、判别器 0、门禁 218/218。⚠ 首屏渲染串不依赖注入（A===B 盲区）→ 不配 expect，以既有用例零漂移为闭环标准。
  - ✅ 续批落地（2026-10-26 · 3 页）：html-entities-encode（样例 `Tom & Jerry © 你好`，避开 `&lt;` 短锚）/ url-encoder-advanced（样例 URL）/ uuencode（样例 `Hello ToolBox 你好`，编码体不含 `2&D` 连续串）各加默认样例 + boot 静默首渲染（output 空才写、不弹 alert 不写历史）。html-entity-encoder 核实已有默认样例（前次扫描按 id="input" 误报）。同批修 1 条 B 类漂移（uuencode 惰性登记段序 → 改锚 begin 644 abc123测试 确定性产物锚，判别力增强）。verify it 766/766、判别器 0、门禁 218/218。
  - 🟢 S1 全部收口：编码类空输入页已全部具备首屏即答案（qr-decoder 需传图不做）。

## 受影响范围
- tools/encode/、tools/telecom/、tools/security/、tools/data/（合计 ~100 页）

## 进度
- 🟢 批次 2026-10-26：E1 字节视图（char-encoder）+ E2 进制统一（bandwidth-calculator/quick-calc）+ E3 引据徽标（data-erase-simulator）+ crc 自定义多项式均已落地。
- 🟢 销案（2026-10-26 复核）：S1 编码链默认示例已收口（上方进度「S1 全部收口」+ 编码类空输入页全部具备首屏即答案），本条为过期残留。

## 2026-11-03 审计补充

### 编码预设英文标签混入汉字（高，确认缺陷；归口 G05-A/G08-1）
- 问题：英文按钮标签包含中文字符，英文态显示中英混排。
- 证据：`tools/encode/convert-4.html:395-398` 中 `labelEn` 为 `Char 中 to code point`。
- 影响：`tools/encode/convert-4.html` 英文态；此条与 G05-A/G08-1 为同一问题，不重复计数。
- 方案：更改为纯英文场景名；修后检查英文态实际按钮及构建版本。

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

### 数据：CSV 多行字段解析错误（高，确认缺陷）
- 问题：`tools/data/csv-analyzer.html:246-262,289-304` 先按换行拆分后再逐行处理引号；源码原函数内存执行 `name,note\nAlice,"first\nsecond"` 得到两条数据行而非一条，统计行数和各列数据随之失真。
- 方案：按完整 CSV 输入跟踪引号状态，正确解析引号内换行、转义双引号及 CRLF；增加上述示例与字段错列测试，错误格式提示而非静默统计。
- 留存优化：该页 `:146-160` 已有样例及明细导出，增加一键多行/缺失值示例、解析后的异常行定位及含分析口径的概要导出，帮助复核统计结果。

## 2026-11-03 续查：编码、通信、安全与数据

### 紧急联系人用户内容拼入 HTML 与内联脚本（高，确认源码注入路径；浏览器待验证）
- 证据：`tools/security/emergency-contacts.html:453-468,520-530,544-566` 将联系人电话经 `ToolBox.escHtml` 后拼进单引号包围的内联事件，`js/common.js:2022-2025` 的转义是 HTML 文本转义而非 JS 字符串转义；CSV 导出把姓名、电话和备注原样拼进 `innerHTML` 后插入文档。
- 影响：`tools/security/emergency-contacts.html`；恶意联系人内容可能在站点同源上下文执行，触发及浏览器实际表现待验证，不能断言已发生数据外传。
- 方案：用 DOM 节点 `textContent` 和事件监听器生成列表及导出表，不拼 HTML 或事件代码；限制电话格式并分别测试引号、标签、导出及拨打路径。

### 紧急联系人清除后字段可能残留（中，确认源码路径；浏览器待验证）
- 证据：`tools/security/emergency-contacts.html:453-481` 添加和删除仅清空 DOM 或联系人记录；`js/tool-ux.js:24-30,205-245` 对非密码输入和 textarea 的 input/change 单独持久化。程序直接赋值不触发 input；删除后字段缓存可能留在本地。
- 影响：`tools/security/emergency-contacts.html`；姓名、电话和备注可能在共享设备残留，不代表上传。
- 方案：敏感字段默认排除通用缓存；添加、删除和清空时同步清除相关缓存，注明本地留存并测试刷新。

### Base32 长度与填充、换行计算不符（高，确认源码缺陷）
- 证据：`tools/encode/base32.html:258-267` 读取 `pad` 却不参与公式，1 字节、不填充时输出无填充长度 8，按 `ceil(8/5)` 应为 2；按 80 字符换行，160 字符加 2 个换行，若只在行间插入则应加 1 个。
- 影响：`tools/encode/base32.html`；长度估算可能导致存储或传输容量规划错误。
- 方案：分别计算有/无填充长度，标明 LF/CRLF 和末尾换行口径；覆盖 0–6 字节及整行边界，增加编码长度对照表。

### 无线接收功率显示为零（中，确认源码缺陷）
- 证据：`tools/telecom/path-loss.html:253-264` 默认 2400 MHz、1 km、20 dBm、两端各 2 dBi 时约 -76.04 dBm，即约 2.49×10⁻⁸ mW；固定四位小数显示 `0.0000 mW`。
- 影响：`tools/telecom/path-loss.html`；非零功率被读作零。
- 方案：按量级采用科学计数法或自动切换 µW/nW/pW，保留有效数字和 dBm，支持对比不同距离。

### CSV 转 JSON 静默丢列和大整数精度（高，确认源码缺陷）
- 证据：`tools/data/csv-json.html:356-381,384-427` 对重复表头直接写同一对象键、仅遍历表头列且默认数字转换调用 `Number`；`id,id\n00123,9007199254740993` 输出键覆盖且大整数变为 9007199254740992；`a,b\n1,2,3` 丢第三列。未闭合引号也未报错。
- 影响：`tools/data/csv-json.html`；转换后编号、数据精度及列可能丢失。
- 方案：显式拒绝或交互处理重复表头、额外列和未闭合引号，保留前导零及超安全整数为字符串；展示列差异和受影响行，提供边界样例。

### CSV/JSON 历史恢复及清空状态不可靠（中，确认源码路径；浏览器待验证）
- 证据：`tools/data/csv-json.html:517-522,562-586` 恢复记录时无参调用要求标签参数的 `setMode()`，异常被吞；清空仅改 DOM，不删除 `js/tool-ux.js:205-245` 保存的输入缓存。
- 影响：`tools/data/csv-json.html`；历史可能无法刷新结果，清空后敏感 CSV 仍可能在本地缓存中残留。
- 方案：完整记录并恢复模式及选项后重新转换；清空同步删除缓存和历史，区分转换结果与历史表导出并提示无数据。

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

### I-10 数据透视表把单元格内容直接拼入 innerHTML（高，确认源码注入路径；浏览器待验证）
- 描述：表头、行/列分组值与合计均原样插入模板字符串后赋给 `result.innerHTML`，CSV 中的 `<img onerror=…>`、`<svg onload=…>` 可在同源页面执行，注入也会破坏表格 DOM。
- 证据：`tools/data/pivot-table.html:288-294,331-359`（334–343 行 `${rowField}`、`${c}`、`${r}` 未转义）。
- 影响：粘贴来源不可信的 CSV 即可触发同源脚本，可能读写本工具 localStorage/页面数据；未做浏览器实测，不能断言已发生数据外传。
- 方案：用 `textContent`/DOM 节点构建表格，或至少统一 HTML 转义后再拼接；对表头与分组值走安全渲染并补注入用例。

### I-11 数据透视表 avg/min/max 的“合计”列与总计行算错（高，确认）
- 描述：avg 的行合计是“各列均值的和”，列合计是“各行均值的平均”，右下总计又是“行合计再求和”；min/max 的合计同样做求和，均不符合对应聚合语义。
- 证据：`tools/data/pivot-table.html:313-328,338-357,364-368`；数据 A/X=10、A/Y=20、B/X=100、B/Y=200、B/X=300 → 总计显示 430，正确均值应为 126（列 X 均值 136.67、Y 110）；min/max 合计为各列极值之和（node 复算）。
- 影响：报表“合计”不可用于汇报，avg 误差可达数倍。
- 方案：合计按“合并原始行后重新聚合”计算（avg 用总分子/总分母，min/max 取全局极值），或明确标注合计为“各行结果之和”并分别展示正确统计。

### I-12 数据透视表 CSV 按逗号切分，忽略引号与重复表头（中，确认）
- 描述：表头与数据行都直接 `split(',')`，带逗号的引号字段错列；重复表头写同一对象键，后者覆盖前者。
- 证据：`tools/data/pivot-table.html:288-294`；`地区,备注\n华北,"北京,朝阳"` → 备注列变成 `"北京`，第 3 段被丢弃；表头 `id,id` 时两列数据互相覆盖，仅剩 `{"id":"9007199254740993"}`（node 复算）。
- 影响：真实 CSV 的分组/计数结果错位，用户难以察觉。
- 方案：复用 CSV 状态机处理引号、转义双引号与 CRLF；重复表头显式报错或自动加后缀；补带逗号字段用例。

### I-13 数据清洗“原始条数”含尾部空行，限长按 UTF-16 截断 emoji（中，确认）
- 描述：`beforeCount` 用 `text.split('\n').length`，末尾换行后的空串也算一条；`maxLen` 用 `l.length`/`slice` 按 UTF-16 码元切，emoji 会被截成孤立代理项。
- 证据：`tools/data/data-cleaner.html:286-288,300-301`；`abc\n` → 原始条数 2（应为 1）；`😀ABC`、maxLen=1 → `\ud83d`（半个 emoji），node 复算 `"😀ABC".length===5`。
- 影响：条数统计偏大；截断可产出乱码并随复制/导出保留。
- 方案：计数前去掉末尾空行（或按非空行计），截断用 `Array.from(str)`/码点计数并避免截断代理对与组合序列；补尾换行与 emoji 用例。

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
