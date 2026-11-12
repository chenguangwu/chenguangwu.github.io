# 2026-11-12 · 第281批 · IT 清单 2 条（攒批第 11 批）

分类：`01-IT开发/it.md`
条目：IT-N334（高）、IT-N349（高，假实现转正）

## 处理结果

### IT-N334 Baudot 数字 8 被静默丢弃（高）— 真改

- 旧 ITA2 FIGS 表缺 key 6，标准 `8` 无对应码，`enc()` 未命中即跳过且不提示。
- 修复：
  - FIGS 补 `6:'8'`（标准 ITA2 数字档 code 6）。
  - `enc()` 收集所有未映射字符到 `dropped`，编码结束后 `alert` 明确列出（中英双语），不再静默改写。
- 效果：输入 `8` → `11011 00110`；输入 `H8I` → `10100 11011 00110 11111 00110`（含 FIGS/LTRS 自动切换）。

### IT-N349 JWT 假 HMAC 签名（高）— 真改（假工具转正）

- 旧 `simpleHmac()` 只是 32 位滚动哈希并返回十进制字符串，第三段是该串的 base64url，任何 JWT 库验签必失败。
- 修复：
  - 新增 `bytesToBase64Url(buf)`：签名字节按二进制转 base64url，不再把字节当字符串 btoa（避免非 ASCII 失真）。
  - 新增 `async hmacSign(alg, sigInput, secret)`：`crypto.subtle.importKey('raw', enc.encode(secret), {name:'HMAC',hash})` + `subtle.sign`，按 HS256/384/512 映射 SHA-256/384/512；无 WebCrypto 明确报错。
  - `generateJwt()` 改为 `async`，签名改 `await hmacSign(alg, sigInput, secret)`；`alg==='none'` 保持空签名。
- 标准值实证（node crypto 对照）：HS256 / secret `your-secret-key` / payload `{"sub":"123"}` → 第三段 `w5SAnahm4DxLK3xCsxkPJdDeDMWFXKxnNfKjwNUnQs0`，与 `crypto.createHmac('sha256',...).digest('base64url')` 完全一致（旧为 `LTkxMzgwOTQyMQ`）。

## 验证证据

- JSDOM 新旧差分 `scripts/_verify_it_batch281.mjs`：新源码 **4/4**，旧源码（`/tmp/bk281`）**1/4**，3 个判别点；旧态精确复现 `H8I`→`10100 00110`（8 消失）与假签名 `LTkxMzgwOTQyMQ`。
- verify 新增 2 条强锁：Baudot `8`→`11011 00110` 输出判别；JWT 用探针断言 `hmacSign` 含 `importKey`/`subtle.sign`、`generateJwt` 不再含 `simpleHmac` 且 `await hmacSign`、字节版 base64url 存在。
  - 目标页 new 3/3 + 4/4；换入旧源码 2/3 + 3/4（新用例均正确变红）；恢复后 3/3 + 4/4；全站 **1687/1687**。
  - 单批判别力：已检 **2** / 正确变红 **2** / 逃生 **0** / 跳过 **0**。
- `audit_verify_input_ids.js`：207 文件 / 10483 用例 / 31051 注入键 / 缺页 0 / 僵尸 0。
- build 两次 `git diff` SHA-256 均为 `842d8570d3325b043461e0de31b6fafdd609e73b19bb149ee8177f3d369ee156`，构建幂等。
- 本批前完成攒批 5 批（276–280）完整门禁：全站 discriminate 已检 **10688** / 正确变红 **10669** / 逃生 **19=基线** / 跳过 **7=基线**；`run_gates.py` **258/258 全过**（`All 258 quality gates passed.`）。

## 待复核要点

- 真机：Baudot 输入含 `8` 与码表外字符（如 emoji），前者正确编码、后者弹出明确提示；解码方向仍可还原。
- 真机：JWT HS256/384/512 三种 alg 生成的 token，用 jwt.io 或服务端 `jsonwebtoken` 库验签通过；`alg=none` 空签名仍按预期；不支持 WebCrypto 环境给出明确错误而非假签名。
