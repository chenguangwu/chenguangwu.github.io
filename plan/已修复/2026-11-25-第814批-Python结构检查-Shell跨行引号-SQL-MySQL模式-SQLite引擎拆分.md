# 第814批：Python 结构检查 / Shell 跨行引号 / SQL MySQL 模式 / SQLite 引擎拆分

日期：2026-11-25

## 修复内容

### Python 格式化（`tools/it/python-formatter.html`）

- 新增 `pythonScanLine()`：逐字符剥离注释、单/双引号字符串（含转义）与三引号字符串，返回只含代码的文本与跨行状态。
- 纯注释行不再参与缩进层级与“冒号后必须缩进”的判断；注释夹在 `if True:` 与 `pass` 之间不再误报。
- 括号由单一计数改为栈：区分 `(` `[` `{`，报“括号类型不匹配”与“多余的右括号”；文件末尾仍有未闭合括号时列出起始行。
- 字符串/注释内的括号不再进入括号栈，`print("(")` 不再误报未闭合。
- 三引号未闭合明确报“三引号字符串未闭合”；校验提示补充“启发式检查，不能替代 Python 语法解析”。

### Shell 脚本格式化（`tools/it/shell-script-formatter.html`）

- 新增 `shellQuoteStep()` 与 `shellHeredoc()`：
  - here-doc 定界符支持 `<<'EOF'`、`<<"EOF"`、`<<\EOF` 与 `<<-`；
  - 跨行单/双引号字符串维护状态，格式化与压缩都逐字保留字符串内部行，不再 `trim()` 改变字符串值；
  - 字符串与注释里的 `<<` 不触发 heredoc。
- `formatShell()`、`minifyShell()`、`doValidate()` 均接入跨行状态；无法安全分析时提示“引号未闭合”，不再输出“校验通过”的矛盾结论。
- 补充 here-doc 引号定界符、跨行引号、压缩保留、未闭合引号的回归用例。

### SQL 转义（`tools/it/sql-escape.html`）

- 新增“MySQL 模式”下拉：`backslash`（默认）/ `no_backslash`（`NO_BACKSLASH_ESCAPES`）。
- `NO_BACKSLASH_ESCAPES` 下：单引号改为双写 `''`，反斜杠保持原样，不再输出会被当作字面反斜杠的 `\'`；反转义只还原 `''`。
- 工具条下方增加模式说明：反斜杠模式与 `NO_BACKSLASH_ESCAPES` 的差异，并继续强调优先参数化查询。
- 方言差异说明同步补充两种 MySQL 模式。

### SQLite 运行器（`tools/it/sqlite-runner.html`）

- 删除手写 `splitSQL()` 与按分号切分逻辑，改用 sql.js 的 `db.iterateStatements(raw)`，由 SQLite 自身逐条 prepare/step。
- `CREATE TRIGGER ... BEGIN ...; ...; END;` 不再被拆坏；方括号/反引号标识符中的分号也不再误拆。
- 每条语句通过 `stmt.getSQL()` 回显，`getColumnNames()` + `step()` 取结果行，`getRowsModified()` 显示影响行数；单条错误仍单独展示并继续后续语句。
- 工作原理文案改为“交给 SQLite 自身逐条 prepare/step，不手写分号切分”。

## 验证

- 定向：`node scripts/verify_it_calc.js it/python-formatter it/shell-script-formatter it/sql-escape it/sqlite-runner` ⇒ 28/28 通过。
- 全量 IT：`node scripts/verify_it_calc.js` ⇒ 2439/2439 通过。
- 真机（Puppeteer，Chrome headless）：Python 注释/字符串括号/类型错配/三引号；Shell 引号 heredoc/跨行引号/压缩/未闭合；SQL 两种 MySQL 模式与方言切换；SQLite 触发器与含分号引号标识符，全部通过。
- 门禁：
  - `python3 _test_static.py`：4654 通过 / 0 失败 / 0 告警；
  - `python3 _audit_links.py --check`：16795 文件 / 167642 内链 / 0 死链；
  - `python3 _audit_assets.py --check`：0 资产死链 / 0 lang 缺失 / 0 重复 id；
  - `node scripts/audit_inline_marker_placement.js`：全部加固标记在整块替换区之外。
