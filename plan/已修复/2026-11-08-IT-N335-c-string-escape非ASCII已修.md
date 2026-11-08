# IT-N335 c-string-escape 非 ASCII 转义（已修复 · 申请复核 · 仅清理）

- **分类**：it / 编码转换
- **原缺陷**：`esc()` 对 `cp > 0x7E` 一律输出 `\x` + 2 位十六进制，C 的 `\x` 无长度上限、超 `unsigned char` 即非法；反转义只读 2 位致 `中`→`\x4e2d`→反解成 `N2d`，中文/emoji 损坏且 C 源码不可编译。
- **现状（实测确认已修复）**：当前 `tools/it/c-string-escape.html` `esc()`（:268-309）对非 ASCII 已走 `cp > 0xFFFF`→`\U`8 位、`cp > 0x7E`→`\u`4 位（:299-302），不再产生非法 `\x`。
  - 实证：`runCase({slug:"it/c-string-escape", inputs:{input:"中"}, clicks:["esc()"], expect:["\\u4e2d"]})` → ok=true。
- **本次动作**：经逐行核对源码 + harness 实测确认既往批次已修复，分类清单条目属「已修未删」陈旧项；本批**不改源码**，仅整条删除 it.md 条目并落此移交档。
- **判别力**：既有 c-string-escape verify 用例均 PASS（新行为已覆盖），无回归、无新增逃生项。
