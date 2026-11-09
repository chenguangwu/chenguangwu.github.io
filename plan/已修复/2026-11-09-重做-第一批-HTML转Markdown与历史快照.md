# 复核失败重做批次 · 申请再次复核

- 来源：`plan/复核失败/2026-11-09-第一批.md` 中 2 条：IT-N401 / N403（HTML 转 Markdown 空格与硬换行）、「IT 历史复用：文本清理器未保存原文」。
- 修复日期：2026-11-09；仅本地提交，**未 push、未跑 `_build.py` / `run_gates.py` / 全站判别力 / CI**（老板本回合指令）。
- 清单已整条删除这 2 项，第一批由 23 条收敛为 **21 条**。

## 逐条：失败点 → 根因 → 修复位点 → 证据

### IT-N401 / N403 HTML 转 Markdown 仍丢失空格与列表硬换行

- 失败点：① `<ul><li>a<br>b</li></ul>` 输出 `- a\n  b`（BR 对应的 Markdown 硬换行丢失）；② `<p>Hello <strong>world </strong>again</p>` 输出 `Hello **world**again`；③ `<p><em> italic </em>next</p>` 输出 `_italic_next`。
- 根因：① BR 返回「行尾两空格 + 换行」，但列表逐行 `replace(/\s+$/,'')` 把这两个空格删掉；②③ 行内格式分支统一用 `innerMarkdown(node,depth).trim()`，把标记内的边界空白吃掉，既造成单词粘连，又让强调标记紧跟非空白字符而无法形成斜体。
- 修复位点（`tools/it/html-to-markdown.html`）：
  1. BR 改为返回私有控制字符 `\u0001` + 换行；该字符不属于 `\s`，所有中间 `trim()` / 尾空白清理都碰不到，`convert()` 末尾统一 `.replace(/\u0001/g, '  ')` 还原成硬换行的两个空格。
  2. 新增 `inlineMark(mark,node,depth)`：分别提取 `lead` / `trail` 空白与 `core`，输出 `lead + mark + core + mark + trail`；`STRONG/B`、`EM/I`、`DEL/S/STRIKE` 三个分支统一改走它（避免只修被点名的两分支而留同类缺陷）。
  3. 给 `inlineMark` / `innerMarkdown` 加无参守卫，消除 harness 兜底调用抛错。
- 证据：`ULBR=1 FLAT=0`（页面内判 `v` 含 `- a(两空格)\n(两空格)b`、不含无硬换行的普通换行）、`STRONG=Hello **world** again q=1`、`EM=_italic_ next q=1`、`DEL=x ~~gone~~ y q=1`。既有 7 条 IT-N401~N404 用例全部保持通过（含 `<p>a<br>b</p>` 的硬换行、嵌套列表层级、表格内加粗、脚本丢弃）。

### IT 历史复用：文本清理器未保存原文

- 失败点：输入 `  OLD TEXT  ` 清理产生历史，改成 `  NEW TEXT  ` 后点击历史，仍清理 NEW TEXT，未恢复原文。
- 根因：`__text_cleanerSnap()` 按 `querySelectorAll` 的 DOM 顺序收集，复选框全在前、`textarea#input-text` 在后；`__text_cleanerExtras()` 里 `keys.slice(0,12)` 这一个被截断的数组被**同时**用于「历史记录保存」「同值去重」「表格渲染」，导致 rec 里根本没有原文。
- 修复位点（`tools/it/text-cleaner.html`）：拆成 `allKeys`（全量，用于去重比较与 `rec` 写入）与 `showKeys`（前 12，仅用于表格展示列 / 导出列），`__text_cleanerRender(showKeys,...)`。导出路径的截断加注释明确其只影响展示，不影响保存。
- 证据：桩构造 14 个复选框 + `input-text`（共 15 字段），捕获 `TBKit.history.record(rec)` 得 `TC=17 HAS=Y VAL=~~NEW~TEXT~~ CB0=1`（17 = 15 字段 + 结果 + `__tbScore`；原文两空格前后缀用 `~` 标记防 blob 折叠）。旧实现下为 `TC=14 HAS=N`，本例在旧代码上必然 FAIL。

## 证据汇总

- 同批补 **5 条**回归用例到 `scripts/verify_it_calc.js` 顶部（`复核失败·第一批重做·续批2` 区块）；HTML→Markdown 用例带 `htmlDom: true`，因 blob 会折叠空白，判据全部在页面内计算后写入独立探针 `__tbProbe`（不写 `mdOutput`，避免被页面重算覆盖 —— 本批踩过这个坑）。
- `verify_it_calc.js 1410/1410`；两 slug 分类 21/21；单文件 `discriminate_check.js verify_it_calc.js` → 已检 1409 / 正确变红 1409 / **逃生项 0** / 跳过 1（基线固有）；`audit_verify_input_ids.js` → 9902 条用例 / 30119 注入键 / **缺页 0**。
- 2 页内联脚本 `node --check` 全绿；本批未改任何 i18n 字典 / 构建源。

## 待复核提示

- 真机复现：① `/tools/it/html-to-markdown.html` 依次输入三条复核用例的 HTML，确认输出分别含硬换行两空格、`Hello **world** again`、`_italic_ next`；② `/tools/it/text-cleaner.html` 输入 `  OLD TEXT  ` 清理 → 改成 `  NEW TEXT  ` → 点击历史第一条，应恢复并重新清理 OLD TEXT。
- 本批只处理被点名的 2 项；`IT-N396/N397`（json-diff）与 `IT-N380/N382/N384`（json-to-code）仍在清单中，尚未处理。
- 依老板本回合指令：本批未 push、未跑全量门禁 / CI；全量门禁与再次复核在攒批后一并发起。
