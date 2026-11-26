# 第807批：Properties 转义与 TOML/TSV 结构保真

关闭 `plan/it/` 7 项：

- Properties解析-反转义遗漏字符且私有区字符被替换
- Properties解析-序列化键名未转义空格及注释符
- Properties解析-压缩丢失转义和换行语义
- TOML格式化-引用表名被拆成多级路径
- TOML转JSON-非法语法被静默跳过
- TOML转YAML-带点的引用键被错误拆分
- TSV转JSON-重复表头和多余列丢失

## Properties（`tools/it/properties-parser.html`）

- `__ppUni()` 改为逐字符状态机：
  - 支持 `\t`、`\n`、`\r`、`\f`、`\\`、`\=`、`\:`、空格、`#`、`!` 与 `\uXXXX`；
  - 未知转义按 Java 语义丢弃反斜杠、保留字符；
  - 去掉 U+E000 占位符，输入自带的私有区字符不再被替换。
- `escapeKey()` / `escapeVal()` 完整转义：
  - 键：反斜杠、空格、`=`、`:`、`#`、`!`、控制字符；
  - 值：前导空白、反斜杠、换行、回车、制表、换页、控制字符。
- `toProps()` 统一用于美化与压缩；`doMinify()` 也复用同一序列化器，不再直接拼 `key=value`。

## TOML 格式化（`tools/it/toml-formatter.html`）

- `tomlStringify()` 递归时保留键路径数组；表头与数组表头逐级 `formatTomlKey()` 后以点号连接：
  - `["a.b"]` 保持 `["a.b"]`；
  - `[["a.b"]]` 保持 `[["a.b"]]`。

## TOML 转 JSON（`tools/it/toml-to-json.html`）

- `parseToml()` 增加严格错误：
  - 缺等号、空键名、表头未闭合、表头闭合后多余内容、重复键、值/表路径冲突、多行值未闭合；
  - 错误信息带行号；页面捕获后显示 `❌ TOML 解析失败：…`，不再静默跳过。
- 根与子表使用无原型对象，`__proto__` 等键可安全保留；排序输出同样无原型。

## TOML 转 YAML（`tools/it/toml-to-yaml.html`）

- 新增 `tPathParts()`：只在引号外的点号处拆分键路径，`"a.b"` 作为一个字面量键。
- 表头改为严格匹配并区分 `[[…]]` 数组表；不合法表头报行号错误。
- 页面捕获解析错误并显示，不再把未解析结构当成功转换。

## TSV 转 JSON（`tools/it/json-to-tsv.html`）

- 新增 `buildTsvRows()`：
  - 空表头补 `columnN`，重复表头改为 `name (2)` 并提示；
  - 行内超出表头的列补 `columnN` 保留，不再丢弃；
  - 缺列按空串补齐，并在统计区提示宽度不一致；
  - 行对象使用无原型对象，`__proto__` 作为自有键完整输出。
- `tsvToJson()` 与 `parseTsvData()` 共用该构建器，数字/布尔转换仍保留原有的前导零保护。

## 验证

- 定向：Properties 9/9、TOML 格式化 7/7、TOML→JSON 13/13、TOML→YAML 14/14、TSV 13/13。
- 全量 IT：2396/2396。
- Puppeteer 真机：14/14，覆盖转义/私有区、键值往返、压缩往返、引用表名、数组表、TOML 错误行号、YAML 引用键、TSV 重复/额外/特殊/缺列。
- 门禁：static 0 失败 0 告警；links 0 死链；assets 0 死链 / 0 lang 缺失 / 0 重复 id；inline marker 通过。
