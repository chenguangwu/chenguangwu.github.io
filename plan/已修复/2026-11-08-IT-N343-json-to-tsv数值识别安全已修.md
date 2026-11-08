# IT-N343 json-to-tsv「自动识别数字」改写长 ID / 前导零 —— 已修复，申请复核

- 分类：01-IT开发 / it
- 工具：`tools/it/json-to-tsv.html`
- 移交批次：2026-11-08 批次（真缺陷修复）

## 缺陷

`tsvToJson()` 在 `autoNumber` 开启时用 `parseFloat` 无条件转数值：

- `12345678901234567890` → `12345678901234567000`（超出 IEEE-754 安全整数被舍入）
- `00123` → `123`（前导零丢失）

订单号 / 身份证 / 手机号 / 带前导零编码在默认配置下被静默改坏，且不可逆。

## 修复

```js
// 旧：if (autoNumber && val !== '' && !isNaN(val) && !isNaN(parseFloat(val))) val = parseFloat(val);
if (autoNumber && val !== '' && /^-?(0|[1-9]\d*)(\.\d+)?$/.test(val) && String(Number(val)) === val) {
  val = Number(val);
}
```

两道关卡：

1. 正则限制「无前导零、无千分位、无指数形式」——`00123`、`1,234`、`1e5` 一律保留字符串；
2. `String(Number(val)) === val` 做往返校验——超出安全整数的 20 位数、`3.10` 这类会被改写字面量的值一律保留字符串。

`autoNumber` 仍默认开启（修好后不再有数据风险），`30`、`3.14` 等正常数值照旧转成数值。

## 判别力实测

新增回归用例（含三态断言，缺一即红）：

```
slug:    it/json-to-tsv
inputs:  { tsvInput: "id\tcode\tamount\n12345678901234567890\t00123\t30", t2jFormat: "compact" }
clicks:  ["document.getElementById('t2jNumber').checked=true; tsvToJson()"]
dumpIds: ["jsonOutput"]
expect:  ["[{\"id\":\"12345678901234567890\",\"code\":\"00123\",\"amount\":30}]"]
```

- 长 ID 保字符串、前导零保字符串、普通 `30` 转数值——三者同时成立才命中；
- 修复前输出 `[{"id":12345678901234567000,"code":123,"amount":30}]` ⇒ 不命中；
- 默认态 `jsonOutput` 是示例数据 ⇒ 不命中，非逃生项。
- 注：harness 的 checkbox 在桩内默认未勾（页面 `checked` 属性不生效），故必须在 clicks 里显式置 `checked=true`。

`node scripts/verify_it_calc.js` → **1078/1078 通过**；`discriminate_check.js verify_it_calc.js` → **已检 1077 / 正确变红 1077 / 逃生 0**。
