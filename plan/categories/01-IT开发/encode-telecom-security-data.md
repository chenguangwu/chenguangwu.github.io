# 编码/通信/安全/数据 · tools/{encode,telecom,security,data}（合计 ~100 页）

> **2026-11-21 全量收口核验**：本文件所列问题已处理完毕，仅作历史档案；当前代码由 210 个 verify 全绿、4,426 页构建、12,102 段内联脚本 0 语法错误及全量门禁覆盖。

> 2026-11-16（694 批已修并核销）：YAML→JSON 列表项多键/行尾注释/块标量/引号内冒号、JSON→YAML 键与引号转义、方向切换到高亮；紧急联系人列表与导出转义；虚拟保险箱 UTF-8 往返（v2 前缀，兼容旧记录）。另核实 path-loss 功率单位、subnet-planner 零地址、data-no-persist 三项早已修复。
> 2026-11-16（692 批已修并核销）：Base32 含/无填充长度与换行口径、CSV→JSON 重复表头/超列/未闭合引号/大整数与前导零、历史恢复模式与清空输入缓存。
> 2026-11-16（693 批已修并核销）：数据透视表合计语义/引号 CSV/HTML 转义/重复表头、CSV 分析多行字段与错列提示。

## 优化点
- S1 首屏即答案：编码类页默认给「Hello World」示例的完整编码链。
  - 🟢 S1 全部收口：编码类空输入页已全部具备首屏即答案（qr-decoder 需传图不做）。

## 受影响范围
- tools/encode/、tools/telecom/、tools/security/、tools/data/（合计 ~100 页）

## 2026-11-03 审计补充

### 覆盖
- 本轮人工核查编码 1 页 `tools/encode/convert-4.html`；通信 2 页 `tools/telecom/subnet-planner.html`、`tools/telecom/bandwidth-calculator.html`；安全 2 页 `tools/security/virtual-safe.html`、`tools/security/passphrase-generator.html`；数据 2 页 `tools/data/csv-analyzer.html`、`tools/data/csv-to-markdown.html`。仅抽样 7 页，未逐页覆盖其余页面；旧「全部收口」属于历史报告，未独立复验。

## 2026-11-03 续查：编码、通信、安全与数据

### 续查覆盖
- 新抽查 `tools/security/emergency-contacts.html`、`tools/encode/base32.html`、`tools/telecom/path-loss.html`、`tools/data/csv-json.html` 4 页，新增 6 条（其中 3 条高优）；源码及局部内存计算证据，未做浏览器、网络或线上验证。

## 2026-11-03 续查（并行批 I）

### 留存优化
- `tools/encode/utf-8.html:131-135` 公式列了 4 档（含 2 字节拉丁/希腊），但只有 3 个输入，无 2 字节与组合 emoji 入口；可增加“2 字节字符数”或直接粘贴文本自动分档，并在结果旁对比字符数/字节数/码点数。
- `tools/encode/base64-length.html:164-169` 深度解析提到 MIME 每 76 字符折行，但结果只给行数不含 CRLF 开销；可并列“纯字符数 / 含 CRLF 实际传输字节”，并同时展示有/无填充两种口径。
- `tools/telecom/ber-snr.html:155-165` 只给 BPSK 与 M-QAM 近似式，未说明适用 SNR 区间与 Gray 映射假设；可在结果旁标注“理论值/高 SNR 近似”，并给出 BER=0.5 与负 Eb/N0 的边界示例。
- `tools/telecom/ap-coverage.html:266` 覆盖评级只看半径绝对值，未区分室内/室外与频段；建议按环境给不同阈值，或展示“留 30% 余量”的保守半径并提示需现场勘测。

### 续查覆盖
- 本轮新抽查 8 页：`tools/encode/utf-8.html`、`tools/encode/base64-length.html`、`tools/encode/jwt-size.html`、`tools/telecom/ber-snr.html`、`tools/telecom/ap-coverage.html`、`tools/data/yaml-json.html`、`tools/data/pivot-table.html`、`tools/data/data-cleaner.html`；与前两批已覆盖的 convert-4、subnet-planner、bandwidth-calculator、virtual-safe、passphrase-generator、csv-analyzer、csv-to-markdown、emergency-contacts、base32、path-loss、csv-json 不重复。
