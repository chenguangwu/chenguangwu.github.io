# IT 开发 · tools/it（340 页，全站第一大分类）

## 已知问题
### I1. hash/编码类页深度参差
- ⚠ 核实（2026-10-26）：pbkdf2 已完整参数化（迭代/盐/密钥长度/格式）、bcrypt 已有 rounds 成本因子——「参数化」部分条目过时。
- ✅ 耗时实测已落地（2026-10-26）：bcrypt 生成成功消息加「实测耗时 X ms（成本因子每 +1 耗时约翻倍）」、校验加实测耗时+恒定时间比较说明；pbkdf2 派生输出加「实测耗时」行（迭代次数为主要耗时来源）。均 performance.now 本地实测（fallback Date.now）。harness 不可达路径（CDN bcrypt 库/crypto.subtle 分支），老锚零漂移：verify it 764/764、判别器 0、门禁 218/218。

### I2. 正则/格式化器错误提示原始
- ✅ 已核实并收口（2026-10-26）：json-formatter 既有行列定位、yaml-validator 既有行号+列号+上下文片段（条目过时）。真缺口在 toml 系：toml-formatter 的 parseToml 是宽松解析器（无效行静默跳过），「验证」几乎永远通过且无定位。已落地：新增 validateTomlStrict 严格逐行校验（表头格式/缺少 =/空键名/空值，带行号定位；值侧三引号多行字符串跳过内容行不误报、表头行内注释 strip），validateToml 通过时输出输入相关统计「（共 N 个键值对，M 个表）」；format/转换仍走宽松 parseToml 零漂移。verify +2 强用例（缺 = 行号锚 / 合法多行字符串统计锚——后者修复「两态同值」逃生，判别器抓到后以统计输出收敛）；verify it 766/766、判别器 0、EN 分支手写 ASCII 无 CJK。

### I3. barcode/QR 系列仅静态生成
- ✅ barcode 导出已落地（2026-10-26）：7 个 barcode 页（codabar/code128/code39/ean/itf/msi/upc）统一加「下载 PNG」按钮（downloadBarcodePNG：canvas.toDataURL、无 canvas 空态提示、文件名带 slug+时间戳）；qrcode.html 已有 downloadQR（核实既有）。verify it 764/764、判别器 0、门禁 218/218。
- 🔴 待续：QR 中心 logo 与纠错级别可视化对比（量级较大，视批次续接）。

## 功能缺陷
- ✅ 时间戳毫秒/秒自动识别已落地（2026-10-26）：timestamp-converter 加「智能粘贴识别」smartInput（纯数字 ≥1e12 判毫秒否则判秒、日期串走 parseDate，同步填秒/毫秒/日期三框 + 识别文案进 #smartHint 可断言；expect 锚 ISO toISOString UTC 确定串免时区漂移）+「当前时间」常驻表 #nowBar（**matchMedia 守卫**：harness 会注入 rAF/setInterval 定时器桩守不住，node/真机差分用 matchMedia；stub 不采集 ⇒ 零 blob 影响，真机 setInterval 每秒刷新）。verify it 768/768、判别器 0。
- ✅ IP 计算器 CIDR 批量已落地（2026-10-26）：ip-calculator v4 tab 加「批量 CIDR 解析」（textarea 每行一条，支持 ip/前缀、ip 点分掩码、裸 IP=/32 三形态；错误行 ❌ 标注不中断；统计串「共 N 条：有效 X，无效 Y」+ 六列汇总表）。⚠ 锚只能用统计串——主机数/掩码值撞「掩码对照表」（harness 兜底直调 buildMaskTable 进 blob），判别器抓到 2 逃生后收紧。verify it 775/775、判别器 0。

## 优化点（G06 联动）
- S6 输入智能化：※ cron「人类语翻译」双向（2026-10-26 落地）+ regex-common「原文高亮+命中偏移明细」（2026-10-26 落地：matchAll 逐段 <mark> + `#i [s-e] 文本` 位置表；⚠ 默认态样例也产高亮标题，标题不可单独作锚）。剩余试点：正则速查页输入联想。
- S3 分步：base64/进制约 30 页加「逐步位运算」可视化。
- 高流量页优先做 S4 分享卡（uuid/password/hash）。

## 受影响范围
- tools/it/（340 页，全站第一大分类）

## 进度
- 🟢 批次 2026-10-26：I1 耗时实测、I2 toml-formatter 严格校验、I3 barcode PNG 导出均已落地。
- 🔴 待开发：QR 中心 logo/纠错级别对比；S6 输入智能化试点（正则速查输入联想）；S3 位运算可视化；S4 分享卡。
