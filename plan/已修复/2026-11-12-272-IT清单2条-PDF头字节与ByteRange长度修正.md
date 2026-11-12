# 2026-11-12 · 第272批 · IT 清单 2 条（攒批第 2 批）

分类：`01-IT开发/it.md`
条目：IT-N315（高）、IT-N316（高，含假工具候选口径纠偏）

## 处理结果

### IT-N315 PDF 头版本号取错字节（高）— 真改

- 旧实现 `head='%PDF-'+(buf[5]||'')+'.'+(buf[6]||'')` 把**字节码**当字符拼，合法 `%PDF-1.7` 得到 `%PDF-49.46`，且正则 `/^%PDF-\d$/` 只认一位数字 ⇒ 合法 PDF 恒判红。
- 修复：直接取前 8 字节原文 `String.fromCharCode.apply(null,Array.from(buf.slice(0,8)))`，严格匹配 `/^%PDF-\d\.\d$/`，完整显示 `%PDF-1.7` 并判绿；PDF 2.0 同样通过。

### IT-N316 签名区域字节数算成负数（高）— 真改

- 旧实现用 `br[4]-br[3]`（len2−offset2），`/ByteRange [0 8000 9000 1200]` 得 `-7800 bytes`。
- 修复：按 PDF ByteRange `[offset1 len1 offset2 len2]` 口径改成 `BigInt(br[2])+BigInt(br[4])`，输出 `9200 bytes`；BigInt 避免大文件偏移溢出。公式区同步改为“两段长度之和（第 2 参数 + 第 4 参数）”。

### 假工具候选口径纠偏（随 N316 一并处理）

- 清单标注该页“只做 ByteRange/Contents 存在性匹配，却宣称校验 PKCS#7 与证书链”。本批把深度解析场景、示例、FAQ、结果含义、用途五处改为结构检查口径：明确不计算摘要、不解析 PKCS#7、不验证证书链、不给“有效/无效”结论。
- 权威源同步：`i18n/tools/content_deepdive.json` 对应条目、`i18n/tools/en/it/pdf-signature-checker.json` 的 map 键与英文值。英文值 CJK 数 0。

## 验证证据

- JSDOM 新旧差分 `scripts/_verify_it_batch272.mjs`（FileReader 桩注入含标准头/ByteRange/Contents 的 PDF 字节）：
  - 新源码 **11/11**：头 `%PDF-1.7`、判绿、原样 ByteRange、`9200 bytes`、BigInt 求和、签名结构回归锚、公式与五处口径。
  - 旧源码（`/tmp/bk272`）**2/11**：精确复现 `%PDF-49.46` + danger、`-7800 bytes`，且旧虚假承诺文案全部命中。
  - 判别点 9 个；2 个回归锚新旧都绿，如实记录。
- verify 新增 1 条强锁 `PDFH`（FileReader 桩 + check() 探针读 d_head/d_bytes）：单页 1/1、全站 **1672/1672**；旧源码换入后 0/1、输出 `PDFH BAD`；单用例判别力 1/1、零逃生。
- `audit_verify_input_ids.js`：207 文件 / 10468 用例 / 31039 注入键，缺页 0、僵尸 0；`node --check` 两脚本通过。
- JSON 解析通过，英文 map 值 CJK 0；build 两次 `git diff` SHA-256 均为 `530fd5185419…`，构建幂等；构建后 JSDOM 11/11、单页 verify 1/1 复验通过。

## 待复核要点

- 真机：上传 `%PDF-1.7` 与 `%PDF-2.0` 样本，「PDF 头」都应显示完整版本号且判绿；非 PDF 仍判红。
- 真机：`/ByteRange [0 8000 9000 1200]` 显示 `9200 bytes`；构造大偏移样本确认 BigInt 不溢出。
- 真机：中英文态深度解析/结果含义/用途均不再出现“验签通过 / 证书链可信 / 有效无效”结论，只描述结构检查与覆盖范围。

## 攒批节奏

- 上批（第270批）已跑完整 258/258 gates + 全站 discriminate 双绿；本批为攒批第 2 批，按约定只跑轻量项，常规批次只本地提交、不 push。
