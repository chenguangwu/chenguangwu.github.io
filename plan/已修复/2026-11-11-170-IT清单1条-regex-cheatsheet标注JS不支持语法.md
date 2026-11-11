# 第170批 · IT 清单 1 条 · regex-cheatsheet 未标注 JS 不支持语法

- 来源：`plan/categories/01-IT开发/it.md` → IT-D30（问题表格行 + 族矩阵 + 逐页结论 + 待复核提示已同步更新）
- 修复日期：2026-11-11
- 类型：内容正确性（跨引擎速查表未区分 JS 支持性），纯静态数据标注

## 失败点
`tools/it/regex-cheatsheet.html` 的 COMMANDS 数据中：
1. `\A \Z` 标为「锚点 / 字符串首/末」且无任何引擎说明；node 复核 `/\AHello/.test('AHello')===true`、`/\AHello/.test('Hello')===false` —— JS 中 `\A` 是字面 A，不是字符串首锚点，JS 用户照抄会得到错误结果。
2. `[:alpha:]` 的 params 仅写「部分引擎支持」，过于含糊；node 复核 `/[[:alpha:]]/.test('abc')===false` —— JS 中该语法按字面字符类匹配，完全不工作。

## 根因
速查表同时收录 ECMA-262 与 POSIX ERE 语法，但未逐条区分引擎支持性，页面顶部「ECMA-262 / POSIX ERE」的笼统标注不足以指导 JS 用户。

## 修复位点
两条 COMMANDS 的 `params` 字段：
- `\A \Z`：`""` → `JS 不支持（按字面 A/Z 匹配；PCRE/Python 等支持）`
- `[:alpha:]`：`部分引擎支持` → `JS 不支持（按字面字符匹配；POSIX ERE/PCRE 支持）`

`cmd`/`desc`/`syntax`/`example` 与渲染、搜索、分类、复制逻辑均未改动。

## 证据
1. **独立复核**：node 实测 `/\AHello/.test('AHello')=true /\AHello/.test('Hello')=false`、`/[[:alpha:]]/.test('abc')=false`，作为标注的事实依据。
2. **verify 强锁**：`scripts/verify_it_calc.js` 新增 2 条，搜索「字符串首」/「POSIX 字符类」后经 clicks 探针读 `#cmdList.innerHTML` 中 `JS 不支持` 出现次数（各应为 1）；regex-cheatsheet 4/4、it 全量 **1499/1499**。
   - **踩坑**：该页无全局 `calcTool()`（渲染由 `renderCommands()` + input 事件驱动），clicks 里调 `calcTool` 会 `not defined`；改为只注入后读 `#cmdList`。另 expect 不能用固定文案（默认全表也含新文案 ⇒ 逃生），必须用 clicks 探针。
3. **旧源码差分**：换回 `HEAD` 旧 HTML → regex-cheatsheet 2/4 红（两条新锁失败）；恢复修好版 → 4/4 绿。
4. **JSDOM 真机**（`scripts/_verify_it_batch170.mjs`）：**9/9 PASS**，覆盖 JS 行为复核、默认全表两处标注、两条过滤各命中 1 项且标注正确、`git` 搜索与清空回归。
5. **门禁辅助**：单文件判别 1498 已检 / 1497 正确变红 / 逃生 1（既有 `it/vector-magnitude`，无新增）/ 跳过 1；audit 10293 用例 / 僵尸 id 0 / 缺页 0；`_en_i18n_probe --check it/regex-cheatsheet` 残留 0 页。

## 备注
- 本批只改源码数据 + verify + 清单条目 + 真机脚本 + 本移交档；攒批后统一跑全站门禁。
- 该页 COMMANDS 为动态渲染的中文数据，英文态命令列表未逐条英译属既有历史问题（非本批引入），未扩大范围处理。
