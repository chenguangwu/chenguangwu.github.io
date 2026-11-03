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
