# IT-N340 html/js 反转义顺序（已修复 · 申请复核 · 仅清理）

- **分类**：it / 编码转换
- **原缺陷**：`doUnescape('js')` 用固定顺序链式 `replace`，`\\n`/`\\uXXXX`/`\\0` 在 `\\\\` 之前被替换，把「转义反斜杠」误当真实转义；`C:\\new` 被解成 `C:\`+换行+`ew`、`\\u0041`→`A`、`\\0`→NUL。
- **现状（实测确认已修复）**：当前 `tools/it/html-escape.html` `doUnescape` js case（:521-543）改为单遍状态机，遇 `\` 先成对消费 `\\`（:522 注释明确「先成对消费 \\，避免 \n 先于 \\ 替换」），再处理 `\u`/`\x`/`SIMPLE`。
  - 实证：`runCase({slug:"it/html-escape", inputs:{input:"C:\\new"}, clicks:[setFormat js + setMode unescape + convert], expect:["C:\\new"]})` → ok=true（双反斜杠输入正确还原为单反斜杠+new）。
- **本次动作**：经逐行核对源码 + harness 实测确认既往批次已修复，分类清单条目属「已修未删」陈旧项；本批**不改源码**，仅整条删除 it.md 条目并落此移交档。
- **判别力**：既有 html-escape verify 用例均 PASS，无回归、无新增逃生项。
