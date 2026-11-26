# 第764批修复记录（2026-11-24）

## 1. ASCII 目录树：标准树形前缀被误判为根节点
- **问题**：缩进模式只取连接符之前的空白算层级。标准 tree 输出 `src/` 后接行首 `├── a.js`、`└── b.js` 时，连接符前缩进为 0，两个文件被当成与 `src` 同级；与页面宣称支持树形前缀不符。
- **修复**（`tools/it/ascii-tree-generator.html`）：解析时保留去掉缩进后的 `leadText`，检测行首 `├──/└──/+--/`--/--` 连接符，并把连接符自身计入一级：`depth = 缩进级 + (connector ? 1 : 0)`。`src/ + ├── a.js + └── b.js` 重新生成同构树；`    └── u.js` 这类 4 空格 + 连接符正确落到二级。

## 2. ASCII 码表：DEL 未列入控制字符分类
- **问题**：说明与详情都把 127 定义为 DEL 控制字符，但控制字符筛选只返回 0–31；筛选后找不到 DEL，可打印也不含它。
- **修复**（`tools/it/ascii-table.html`）：控制字符范围改为 `[0,128)` 并在循环内跳过 32–126，分类只含 0–31 与 127；按钮文案改为「控制字符 (0-31, 127)」；搜索增加 `DEL` 名称匹配（十进制 127、0x7F 本就可命中）。

## 3. ASCII 码表：Latin-1 字符 URL 编码按单字节误导
- **问题**：详情把码值直接拼成 `%XX`，例如 `é` 显示 `%E9`；现代 URL 用 UTF-8 百分号编码，正确结果是 `%C3%A9`，复制即错。
- **修复**：
  - 详情拆分两行：「Latin-1 字节」显示 `0xE9`（ISO-8859-1 单字节）；「URL 编码（UTF-8）」用 `encodeURIComponent(String.fromCharCode(code))` 输出 `%C3%A9`。
  - 公式区与说明新增「编码口径」，明确两者区别；ASCII 字符按浏览器实际编码展示（字母保持字面、空格 `%20`、控制符 `%XX`）。
  - 覆盖 ASCII、Latin-1（é、ÿ）与控制字符。

## 4. AST 查看器：BigInt 节点无法导出 JSON
- **问题**：`const n = 1n` 的 AST `value` 是 BigInt，`JSON.stringify` 抛错后回退 `String(ast)`，JSON 视图与复制只剩 `[object Object]`；树视图标量也用 `JSON.stringify`，BigInt 同样失败。
- **修复**（`tools/it/ast-viewer.html`）：
  - 新增 `astJsonStringify(value)`：replacer 把 bigint 转成 `{"__type":"BigInt","value":"…"}`，全程字符串保存、无精度丢失；JSON 视图与「复制 JSON」共用同一函数。
  - 失败时不再回退 `[object Object]`，而是明确显示「JSON 序列化失败：…」。
  - 树视图新增 `astPrimitiveText`，BigInt 显示 `1n`，字符串仍带引号。
  - 测试覆盖正大整数、负大整数、普通数字与嵌套节点。

## 5. Atbash 密码：历史截断与清空竞态
- **问题**：历史把输入/输出截到 200 字符，加载时直接回填截断内容且无提示；前 200 字符相同的长文本被当作同一条。转换后 500ms 延迟写入，清空输入/历史时未取消定时器，刚清掉的记录会重新出现。
- **修复**（`tools/it/atbash-cipher.html`）：
  - 历史保存完整 `input/output`，不再 `substring(0,200)`；去重按完整输入，同前缀长文本可共存；记录附 `truncated:false`。
  - 新增 `cancelHistory()`；`clearAll()`、`clearHistory()`、输入清空分支都先取消待写定时器。
  - 历史列表标题带完整输入，列表仍只展示前 60 字符摘要。

## 验证
- `python3 _build.py` exit 0；四页关键改动构建后存活。
- 定向 `node scripts/verify_it_calc.js it/ascii-tree-generator it/ascii-table it/ast-viewer it/atbash-cipher`：**25/25**（新增 7 条：标准 tree 一级/多级、控制字符含 127、搜索 DEL、é UTF-8、BigInt 类型标记、长文本两条、清空取消定时器）。
- 全量 IT：**2105/2105**。
- 真机 Puppeteer `/tmp/test764.js`：**9/9**（标准 tree 一级/多级、DEL 筛选与搜索、é `%C3%A9`、真实 acorn 8.19 解析 `1n`/负数 BigInt JSON、260 字符两条完整历史、清空后 700ms 无写入、正常写入仍生效）。
- 英文探针 4 页 **0 残留**；`audit_inline_marker_placement.js` exit 0；`_audit_assets.py --check` 0 资产死链 / 0 lang 缺失 / 0 重复 id。
