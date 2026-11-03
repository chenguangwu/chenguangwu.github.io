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
