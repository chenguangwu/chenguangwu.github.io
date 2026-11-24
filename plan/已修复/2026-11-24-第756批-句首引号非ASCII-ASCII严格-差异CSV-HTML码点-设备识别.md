# 第756批：句首引号/非 ASCII、ASCII 严格、差异 CSV、HTML 码点、iPhone 识别

本批处理 `plan/it/` 五项扫描任务，均已修复并回归。

## 1. 大小写转换：句首引号与非 ASCII
- `tools/it/case-converter.html`：`toSentenceCase` 句子边界扩展为 `. ! ?`（后接空白）、`。！？`、换行；边界后允许先出现引号/括号，再将第一个 Unicode 字母大写。
- `"hello world"` ⇒ `"Hello world"`；`école est belle` ⇒ `École est belle`；中文句号后的中文正文保持原样。公式说明同步。

## 2. 文本转二进制 / 十六进制：ASCII 模式截断
- 两页 `textToBytes` ASCII 分支改为按码点遍历，>127 直接抛出「第 N 个字符、码点」并建议 UTF-8；编码主流程捕获错误并清空输出、在可视化区显示原因。
- `bytesToText` ASCII 解码遇到 >127 字节报「第 N 字节」；UTF-16BE 补齐偶数字节、代理项配对校验；UTF-8 改 `fatal:true` 严格解码。
- 解码失败清空输出并把原因写入 placeholder（中英双语）；成功后恢复 placeholder。

## 3. 文本对比：CSV 丢行首尾空白
- `tools/it/text-diff.html`：不再通过 `TBKit.util.exportTable('#tdHidden')` 读 DOM，直接从 `currentDiff` 生成 CSV；字段全程带引号、双引号转义、保留行首尾空格/制表符/换行。
- 以 `= + - @` 开头的单元格前置单引号，降低电子表格公式注入风险；CRLF 行分隔，`downloadText` 自动补 UTF-8 BOM。

## 4. 文本转十进制：HTML 实体按字节
- `tools/it/text-to-decimal.html`：`&#` 模式独立为 Unicode 码点转换：`中` ⇒ `&#20013;`、`😀` ⇒ `&#128512;`，逐字符视图显示 `U+... = &#...;`，与 UTF-8/UTF-16 字节脱钩。
- 反向只接受 `&#数字;`（可含空白），按码点解析并拒绝代理项与 >U+10FFFF；普通字节十进制模式不变。
- 说明/FAQ/选项补齐中英与字面实体转义，避免 HTML 解析把 `&#20013;` 变成「中」而看不出字符引用。

## 5. 设备信息：iPhone 系统与浏览器识别
- `tools/it/device-info.html`：先判 iPhone/iPod、iPad，再判桌面模式 iPad（Mac OS X + 触摸点 >1），最后才判 macOS；iOS/Android 版本一并显示。
- 浏览器识别新增 `EdgiOS/`、`EdgA/`、`CriOS/`、`FxiOS/`，再匹配桌面 `Edg/`、`Chrome/`、`Firefox/`、`Safari`。
- 新增 UA 限制说明：UA 冻结/缩减、桌面模式、伪装与自定义 UA 会导致偏差，iPad 桌面模式只能按触摸点推断，不能唯一识别设备或用户。

## 验证
- `python3 _build.py` exit 0；六页手改 `grep` 复查存活。
- 定向 `verify_it_calc.js` 六 slug：43/43；全量 IT **2049/2049**。
- 真机 Puppeteer `/tmp/test756.js`：13/13（引号/重音句首、二进制与十六进制 ASCII 编码/解码拒绝、CSV 保留空格、HTML 实体中文/emoji/代理项、iPhone Safari/CriOS、iPad 桌面模式）。
- 英文探针：`text-diff` 14 条残留与改动前基线一致，其余 5 页 0 残留。
- `audit_inline_marker_placement.js` exit 0；`_audit_assets.py --check` 0 死链 / 0 lang 缺失 / 0 重复 id。
