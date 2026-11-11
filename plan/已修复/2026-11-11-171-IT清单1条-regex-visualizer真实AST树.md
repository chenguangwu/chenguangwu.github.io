# 第171批 · IT 清单 1 条 · regex-visualizer 承诺树状图但只有线性状态链

- 来源：`plan/categories/01-IT开发/it.md` → IT-D28（问题表格行 + 族矩阵 + 逐页结论已同步更新）
- 修复日期：2026-11-11
- 类型：功能承诺与实现不符（页面宣称 AST 树/铁路图/层级，实际仅 token 直线），纯前端结构解析

## 失败点
`tools/it/regex-visualizer.html` 的 `buildStates()` 对每个 token 建 1 个状态并首尾串联，默认 `^a[0-9]+b$` 得到 10 token / 12 状态的直线；页面 title、meta description、工作原理与 FAQ 均宣称「彩色的树状可视化图」「解析为语法树（AST）」「直观展示分组、量词与字符类层级」，实际完全无层级结构。

## 根因
实现阶段只做了 tokenize + 线性状态链，未实现承诺的递归下降解析与树渲染。

## 修复位点
1. 新增 `parseRegexAst(p)`：递归下降解析，支持分支 `|`、序列、捕获/非捕获/命名分组、正负向先行后行、字符类（含取反与转义）、量词（`* + ? {n,m}` 及惰性后缀）、锚点 `^ $ \b \B`、转义序列与 `.`；返回带 `type/label/detail/children` 的 AST 节点数组。
2. 新增 `renderAstTree(nodes)`：输出嵌套 `<ul class=ast-tree/ast-children>`，每个节点带类型 class 与中文/英文标签；所有用户内容经既有 `escapeHtml()` 转义。
3. `render()` 在原有线性状态链之前插入 AST 树视图（英文态标题走既有 `__en` 分支）；线性状态链完整保留，兼容既有导出和 4 条历史 verify 用例。
4. 新增主题变量驱动的树样式（亮/暗主题均可读），未引入硬编码颜色。

## 证据
1. **verify 强锁**：`scripts/verify_it_calc.js` 新增 2 条——`a(b|c)*` 断言 `ast-alt` / `2 路择一` / `ast-group`；`(?:ab)+` 断言 `非捕获分组`。regex-visualizer 6/6（含 4 条历史用例全部保持绿）、it 全量 **1501/1501**。
2. **旧源码差分**：换回 `HEAD` 旧 HTML → regex-visualizer 4/6 红（两条新锁失败）；恢复修好版 → 6/6 绿。
3. **JSDOM 真机**（`scripts/_verify_it_batch171.mjs`）：**16/16 PASS**，覆盖默认态 AST+状态链并存、分支/捕获分组/量词嵌套、非捕获/命名分组、正反向先行后行、字符类取反、惰性花括号量词、AST 路径 XSS 转义、非法正则安全早退。
4. **判别力**：单文件 1500 已检 / 1499 正确变红 / 逃生 1（既有 `it/vector-magnitude`，无新增）/ 跳过 1。
5. **门禁辅助**：audit 10295 用例 / 僵尸 id 0 / 缺页 0；`_en_i18n_probe --check/--roundtrip it/regex-visualizer` 均 0。

## 备注
- 本批只改源码 + verify + 清单 + 真机脚本 + 本移交档；攒批后统一跑全站门禁。
- 文案中「铁路图（railroad diagram）」的完整图形化布局仍未实现，本批交付的是等价层级树视图（AST 节点可展开层级、类型可读）。铁路图样式升级留待后续单独批次，不在此伪称收口。
- 本批同时提交 `sw.js`：为第166–170批后全量门禁构建脚本自动注入的 BUILD hash 变更（非手改）。
