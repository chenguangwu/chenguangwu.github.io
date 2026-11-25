# Plist 转换：普通字典与类型标记冲突

## 问题

工具用 `{"__plistType":"date","value":"..."}` 等普通 JSON 对象表示 plist 专有类型，反向转换时只检查对象键数及 `__plistType`，无法区分用户本来就有的字典。例：合法 plist 字典含 `__plistType` 为 `date`、`value` 为 `2026-01-01T00:00:00Z` 两个字符串字段，转 JSON 再转回 plist 后会变成单个 `<date>`，字典结构和字段丢失。直接输入同形状 JSON 也会发生相同误转换。

## 解决方案

设计明确且无歧义的类型封装与转义机制，对与保留标记冲突的普通字典进行转义；或提供用户可见的类型选择并在冲突时拒绝静默转换。覆盖四类标记、嵌套同名字段及普通字典的完整往返。

## 受影响工具路径

- `tools/it/plist-parser.html`（`plistTyped`、`isPlistTyped`、`toPlistNode`）
