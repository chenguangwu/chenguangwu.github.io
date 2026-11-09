# 金融 F-N207 重做移交：MEID 缺校验位不再判有效，补齐 hex/dec 互证与算法降级说明

- 失败点：14 位 hex / 18 位 dec 缺校验位时一律 `valid=true`，把「长度格式」包装成「校验通过」；页面宣称验证 hex/dec 自洽但源码无换算；算法注释自称 `Luhn-like`/`Luhn-style` 却无权威出处。
- 根因：只有 15 hex / 19 dec 带校验位分支做比对，缺位分支直接放行；两种表示未做 BigInt 换算与范围约束；算法来源无法核实。

## 修复位点

- `tools/finance/meid-validator.html`
  - 新增 `meidHexToDec14()` / `meidDecToHex18()`，后者以 `0xFFFFFFFFFFFFFFn` 约束 MEID 56 位范围；
  - hex 输入展示「十进制表示（同一 MEID）」与「十进制参考校验位」；dec 输入展示「十六进制表示（同一 MEID）」与「十六进制参考校验位」；
  - 14 hex / 18 dec 缺校验位不再判 ✅，改为第三态「⚠ 仅格式通过，未提供校验位，无法完成校验」，并保留参考建议值；
  - 算法文案统一降级为「参考 Luhn Base16/Base10（非标准，仅供格式自检）」，注释不再暗示 3GPP2 官方校验位；
  - `__meid_validatorScore()` 失败词表补 `未提供校验位|无法完成校验`，避免部分态被历史记录误记为通过。
- `scripts/verify_finance_calc.js`
  - `MEIDFIX A0000012345679 OK`：同时要求部分态结论、十进制等价 `045035996579124857`、非标准算法标注；
  - `MEIDDEC 045035996579124856 OK`：要求十进制→十六进制互证得到 `A0000012345678`。

## 证据

- 新源码：`node scripts/verify_finance_calc.js` **446/446**；
- 判别力：**446/446 全部变红，逃生项 0**；僵尸 id **0**；
- 旧源码替换实测：单跑 `meid-validator` **5/7**，两条新增用例分别输出 `MEIDFIX … BAD` / `MEIDDEC … BAD`，旧结论均为 `✅ MEID 号码有效`；恢复新源码 **7/7**。
