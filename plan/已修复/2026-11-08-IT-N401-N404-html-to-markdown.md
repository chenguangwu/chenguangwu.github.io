# 第 15 批 · IT-N401 ~ IT-N404 · html-to-markdown 行内格式/转义/换行/脚本丢弃

- 日期：2026-11-08
- 页面：`tools/it/html-to-markdown.html`
- 条目：IT-N401（高）、IT-N402、IT-N403、IT-N404（均中）
- 提交：见本批 commit（工具 + verify + 判别器透传 + 移交档同一提交）

## 一、修复内容

### IT-N401 strong/em 完全不处理（高，承诺未实现）
**根因**：`nodeToMarkdown` 没有 `STRONG/EM` 分支（落到默认 `innerMarkdown`），且 `P/H*` 用 `innerText` 取纯文本 —— `innerText` 抹掉所有行内标签，加粗/斜体在转换前就已丢失。

**修复**（`nodeToMarkdown` 重写，原 `:231-310` 整段替换）：
- `P` / `H1..H6` 改用 `innerMarkdown(node, depth)` 递归取内容，不再 `innerText`；
- 新增分支：`STRONG|B → '**' + innerMarkdown + '**'`、`EM|I → '_' + ... + '_'`、`DEL|S|STRIKE → '~~' + ... + '~~'`；
- `TD/TH` 单元格改为 `innerMarkdown(c)` 递归后压平换行、转义 `|`。

### IT-N402 `escapeMarkdown` 定义后从未调用（中，承诺未实现）
**根因**：`:223` 定义、全文零调用；正文 `*` `_` 原样输出会被 Markdown 渲染成斜体/强调。

**修复**：
- `escapeMarkdown` 补 `[` / `]` 两项（`\\[`、`\\]`）；
- 文本节点输出统一走 `escapeMarkdown(折叠空白后的 textContent)`；
- 表格单元格内容走 `escapeMarkdown`（`|` 单独转 `\|`）。

### IT-N403 `<br>` 与嵌套列表被折叠（中，确认缺陷）
**根因**：① `BR` 两个分支顺序错误（先 `return '\n'`，后一个返回 `'  \n'` 的永远不可达），且 `P` 用 `innerText` 把 `a<br>b` 的换行折叠成空格；② 列表项 `body.replace(/\n+/g, ' ')` 把子列表换行压平。

**修复**：
- `BR` 统一返回 `'  \n'`（两个空格硬换行）；
- 列表项（`LI`）保留内部换行，续行按 `' '.repeat(prefix.length)` 缩进（保持子列表对齐父项文本起点）；
- 列表整体输出改为 `return '\n' + out + '\n'` —— 前置换行修复「`- a` `- b`」两兄弟项在无父缩进时粘连成 `- a- b`。

### IT-N404 `<script>`/`<style>` 文本未丢弃（中，承诺未实现）
**根因**：`SCRIPT/STYLE` 落到默认 `return innerMarkdown(...)`，子文本节点被原样写进 Markdown；注意事项却承诺「脚本等表现层信息会被丢弃」。

**修复**：`SCRIPT` / `STYLE` / `NOSCRIPT` 三类直接 `return ''`。

## 二、证据（jsdom 真机执行页面脚本）

| 输入 | 修复前 | 修复后 |
|---|---|---|
| `<p>支持 <strong>HTML 转 Markdown</strong>，保留标题、列表与链接。</p>` | `支持 HTML 转 Markdown，保留标题、列表与链接。` | `支持 **HTML 转 Markdown**，保留标题、列表与链接。` |
| `<p><em>斜体</em> 与 <b>粗</b> 与 <i>他</i></p>` | `斜体 与 粗 与 他` | `_斜体_ 与 **粗** 与 _他_` |
| `<p>2 * 3 * 4 与 a_b</p>` | `2 * 3 * 4 与 a_b` | `2 \* 3 \* 4 与 a\_b` |
| `<p>a<br>b</p>` | `a b` | `a␠␠\nb` |
| `<ul><li>a<ul><li>b</li><li>c</li></ul></li><li>d</li></ul>` | `- a - b - c - d` | `- a\n  - b\n  - c\n- d` |
| `<p>正文</p><script>alert("zzz9")</script>` | `正文\n\nalert("zzz9")` | `正文` |
| 表格含 `<td><strong>粗</strong></td>` | `| 粗 |` | `| **粗** |` |

首屏默认样例同样生效：`## ToolBox 在线工具…` 起头，全文含 `**HTML 转 Markdown**`。

## 三、测试同步（同批，`scripts/verify_it_calc.js` 新增 7 条）

新增用例全部声明 `"htmlDom": true`（页面 `convert()` 走 `new DOMParser().parseFromString(html,'text/html')`）；harness 为此新增 `makeHtmlDomParserStub()`（jsdom 实现），**只在用例显式声明 `htmlDom` 时注入**，不动 globalThis 默认态（`domParser` 的 XML 桩保持原样，`it/rich-text-editor`、`it/xml-formatter`、`it/xml-to-json` 的既有行为逐字节不变）。

| # | 锚定条目 | expect | 防逃生设计 |
|---|---|---|---|
| 1 | N401 | `支持 **HTML 转 Markdown**，保留标题、列表与链接。` | 输入 HTML 不含 `**`，断言串只能来自转换结果 |
| 2 | N401 | `_斜体_ 与 **粗** 与 _他_` | 同上，且同时覆盖 b/i 别名标签 |
| 3 | N402 | `2 \* 3 \* 4 与 a\_b` | 反斜杠只在转义路径产生 |
| 4 | N403 | `BR hard=1 flat=0 q=1`（clicks 在页面内判 `a␠␠\nb` 形态） | blob 会折叠空白 ⇒ 不能在 expect 写换行；`q=1` 绑注入值 |
| 5 | N403 | `UL nested=1 flat=0 q=1` | 同上，判 `- a\n  - b` 相邻形态 |
| 6 | N401 | `\| **粗** \|` | 表格单元格路径单独覆盖 |
| 7 | N404 | `N404 js=0 t=1` | `t=1` 绑注入值（「正文」），注入失败即 FAIL |

**为何第 4/5 条用 clicks 而不用 expect 直判**：harness `collectStrings` 对 `el.value` 也做 `replace(/\s+/g,' ')`，换行/连续空格在 blob 里不可区分，任何「空格数/换行」断言都会恒真（零判别力）。改由页面内 `indexOf` 判形态，把布尔结果写回输出区再断言，判别力真实存在。

## 四、判别力实测

**负向对照**（`git checkout HEAD -- tools/it/html-to-markdown.html` 回退到修复前，重跑这 7 条）：**7/7 全部变红**。
正向：`node scripts/verify_it_calc.js` → **1163/1163 通过**；`node scripts/audit_verify_input_ids.js` → 僵尸 id ①0。

**判别器本身同步修**（`scripts/discriminate_check.js`）：`snapshotOf()` 原先把用例裁剪成 `{slug, afterLoad, dynDom, dynInputs, snapshotOnly}` 再取默认态快照，**漏传 `htmlDom`/`domParser`** ⇒ 依赖 DOMParser 的页面在快照阶段直接抛 `DOMParser is not defined`，7 条用例被判 `no-snapshot` 静默跳过（跳过数 1 → 8）。
本次把两个环境装配开关原样透传、并纳入 `snapCache` key（同一 slug 可同时存在需要/不需要 DOM 桩的用例）。结果：**已检 1155 → 1162，跳过 8 → 1，逃生 0 不变**（7 条全部正确变红），判别力真实覆盖到本批用例而不是"看着绿"。

## 五、遗留说明（不凑用例）

- 「已删除的控件」（如本批未涉及）无行为契约可断言：harness `getElementById` 对任意 id 会自动造桩元素，`getElementById('x') === null` 恒 false。此类只靠 jsdom 真机复核 + 僵尸 id 审计，不硬塞用例。
- 存量 `escapeMarkdown` 不转义行内代码块内部原文：行内代码（`` ` ``）内容按浏览器语义本就原样输出，本轮不处理，避免与「转义集合」承诺冲突。
