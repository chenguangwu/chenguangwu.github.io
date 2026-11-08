# IT-N364 hash-identifier `$5$`/`$6$` 前缀漏判 —— 已修复，申请复核

- 分类：01-IT开发 / it
- 工具：`tools/it/hash-identifier.html`
- 移交批次：2026-11-08 批次（真缺陷修复）

## 状态拆分（原条目含两部分）

1. **长度映射错位（12 位标成 CRC32、8 位判未知）—— 已在既往批次修复**，本次核对确认：
   - `map` 现为 `{8:['CRC-32','32 位校验'], 32:MD5, 40:SHA-1, 56:SHA-224, 64:SHA-256, 96:SHA-384, 128:SHA-512}`，12 位已从表中删除（落「未知」）；
   - 既有门禁用例 `1a2b3c4d`→CRC-32、`1a2b3c4d5e6f`→未知 均 PASS，可作佐证。
2. **`$5$`/`$6$` 前缀未实现 —— 本次修复**（页面说明与引据表早已承诺 `$6$` = SHA-512-crypt，代码只识别 `$2a$/$2y$/$2b$/$1$/$argon2`）。

## 修复

```js
if(v.indexOf('$5$')===0)cands.push(['SHA-256-Crypt','前缀 $5$（SHA-256 crypt）']);
if(v.indexOf('$6$')===0)cands.push(['SHA-512-Crypt','前缀 $6$（SHA-512 crypt）']);
```

## 判别力实测

```
$6$rounds=5000$abc$xyz → 识别结果 SHA-512-Crypt 前缀 $6$（SHA-512 crypt）
$5$rounds=5000$abc$xyz → 识别结果 SHA-256-Crypt 前缀 $5$（SHA-256 crypt）
$1$abc$xyz             → 识别结果 MD5-Crypt 前缀 $1$          （原有行为不变）
```

新增门禁用例：

```
slug:   it/hash-identifier
inputs: { h: "$6$rounds=5000$abc$xyz" }
clicks: ["calcTool()"]
expect: ["SHA-512-Crypt 前缀 $6$（SHA-512 crypt）"]
```

修复前该输入恒判「未知」⇒ 不命中；默认值是 64 位十六进制、不含 `$` 前缀 ⇒ 默认态不命中，非逃生项。

`node scripts/verify_it_calc.js` → **1082/1082 通过**；`discriminate_check.js verify_it_calc.js` → **已检 1081 / 正确变红 1081 / 逃生 0**。
