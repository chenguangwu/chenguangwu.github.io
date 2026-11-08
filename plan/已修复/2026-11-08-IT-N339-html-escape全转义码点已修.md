# IT-N339 html-escape 全转义 emoji 码点（已修复 · 申请复核 · 仅清理）

- **分类**：it / 编码转换
- **原缺陷**：`doEscape` 的 `escAll` 分支用 `charCodeAt(0)` 取 UTF-16 单元，emoji（双单元码点）低位代理被丢弃；`😀`→`&#55357;`（仅高位代理 0xD83D），再反转义得孤立代理、浏览器乱码。
- **现状（实测确认已修复）**：当前 `tools/it/html-escape.html` `doEscape`（:447-510）`escAll` 分支改用 `Array.from(text).map(c => ...c.codePointAt(0)...)`（:451-453 / :464 / :473），按码点输出。
  - 实证：`runCase({slug:"it/html-escape", inputs:{input:"😀"}, clicks:[直接调用 doEscape(input,'html-dec',false,false,true)], expect:["&#128512;"]})` → ok=true（U+1F600=128512 正确）。
- **本次动作**：经逐行核对源码 + harness 实测确认既往批次已修复，分类清单条目属「已修未删」陈旧项；本批**不改源码**，仅整条删除 it.md 条目并落此移交档。
- **判别力**：既有 html-escape verify 用例均 PASS，无回归、无新增逃生项。
