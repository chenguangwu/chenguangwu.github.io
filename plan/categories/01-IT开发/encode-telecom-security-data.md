# 编码/通信/安全/数据 · tools/{encode,telecom,security,data}（合计 ~100 页）

> 2026-11-16（694 批已修并核销）：YAML→JSON 列表项多键/行尾注释/块标量/引号内冒号、JSON→YAML 键与引号转义、方向切换到高亮；紧急联系人列表与导出转义；虚拟保险箱 UTF-8 往返（v2 前缀，兼容旧记录）。另核实 path-loss 功率单位、subnet-planner 零地址、data-no-persist 三项早已修复。
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

## 2026-11-03 续查：编码、通信、安全与数据

### 续查覆盖
- 新抽查 `tools/security/emergency-contacts.html`、`tools/encode/base32.html`、`tools/telecom/path-loss.html`、`tools/data/csv-json.html` 4 页，新增 6 条（其中 3 条高优）；源码及局部内存计算证据，未做浏览器、网络或线上验证。

## 2026-11-03 续查（并行批 I）

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
