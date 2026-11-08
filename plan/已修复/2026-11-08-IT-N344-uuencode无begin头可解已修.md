# IT-N344 uuencode 反转义强制要求 begin 头 —— 已修复，申请复核

- 分类：01-IT开发 / it
- 工具：`tools/it/uuencode.html`
- 移交批次：2026-11-08 批次（真缺陷修复）

## 缺陷

`decodeUu()` 以 `started = false` 起步，只有匹配 `begin <权限> <文件名>` 才置真；RFC 未强制该头行，从邮件/工具截取的纯数据段因此全部被跳过，输出空串且无任何提示。

## 修复

`tools/it/uuencode.html` `decodeUu()`：

```js
let started = !lines.some((l) => /^begin\s+\d+\s+\S*/.test(l.trim()));
```

- 含 `begin` 行 ⇒ 与原先一致，只解析头行之后的内容；
- 不含头行 ⇒ 整段按数据行解析（与 xxencode 页既有行为一致）。

## 判别力实测

新增回归用例（`scripts/verify_it_calc.js`，紧随 uuencode 编码用例）：

```
slug: it/uuencode
inputs: { input: "&6F%P<&5R\n`\nend" }
clicks: ["dec()"]
expect: ["Zapper"]
```

向量手算可复算：Zapper = 5A 61 70 70 65 72；
- 长度字节 6 → chr(38) = `&`
- 组1 90/97/112 → 22/38/5/48 → `6F%P`
- 组2 112/101/114 → 28/6/21/50 → `<&5R`

修复前 `started` 恒 false ⇒ 输出空串，"Zapper" 不出现；默认样例是编码后的文本（非合法数据段）⇒ 默认态不命中，非逃生项。

`node scripts/verify_it_calc.js` → **1076/1076 通过**；`discriminate_check.js verify_it_calc.js` → **已检 1075 / 正确变红 1075 / 逃生 0**。
