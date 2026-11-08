# IT-N336 c-string-escape 反转义八进制分支（已修复 · 申请复核 · 仅清理）

- **分类**：it / 编码转换
- **原缺陷**：`unesc()` 的 `switch(n)` 用 `case /[0-7]/:`（正则对象作 case）与字符串严格比较恒为 false，八进制转义全部落入 `default`；`\101`→`101`、`\012`→NUL+`12`，C 合法八进制转义解错。
- **现状（实测确认已修复）**：当前 `tools/it/c-string-escape.html` `unesc()`（:311-378）八进制改用前置 `if(/[0-7]/.test(n))` 判断并最多读 3 位（:324-332），不再依赖正则 case。
  - 实证：`runCase({slug:"it/c-string-escape", inputs:{input:"\\101"}, clicks:["unesc()"], expect:["A"]})` → ok=true（`\101`=0o101=65='A'）。
- **本次动作**：经逐行核对源码 + harness 实测确认既往批次已修复，分类清单条目属「已修未删」陈旧项；本批**不改源码**，仅整条删除 it.md 条目并落此移交档。
- **判别力**：既有 c-string-escape verify 用例均 PASS，无回归、无新增逃生项。
