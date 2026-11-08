# IT-N362 csv-to-yaml 引号内换行 / 表头键加引号 —— 已修（既往批次），本次补护栏

- 分类：01-IT开发 / it
- 工具：`tools/it/csv-to-yaml.html`
- 移交批次：2026-11-08 批次（已修未删清理 + 补护栏用例）

## 结论

条目描述的两处缺陷在当前源码中**均已不存在**，属「已修未删」陈旧项：

1. **引号内换行**：`parseCsvRows()` 已是 RFC 4180 字符级状态机（同时处理 `"`、`,`、`\n`），不再「先按 `\n` 切行」。
2. **表头键不加引号**：`yamlKey()` 已按 YAML 规则决定是否加引号 —— 非安全标识符或 YAML 保留字（`y/n/yes/no/true/false/null/on/off`）一律 `JSON.stringify`。

## 实测取证（harness 实跑）

```
csv "a:b,c\n1,2"                     → YAML 输出 - "a:b": "1"  c: "2"
csv 'name,note\nAlice,"line1\nline2"' → YAML 输出 - name: "Alice"  note: "line1\nline2"   （多行字段为一条记录）
csv "y,on\n1,2"                      → YAML 输出 - "y": "1"  "on": "2"
```

## 本次新增的护栏用例

既有 IT-N26 用例只覆盖「表头含空格」，本次补一条覆盖**含冒号表头**：

```
slug:   it/csv-to-yaml
inputs: { csv: "a:b,c\n1,2" }
clicks: ["calcTool()"]
expect: ['"a:b": "1"']
```

不加引号时 YAML 会把 `a:b: "1"` 解析成键 `a`、值 `b: 1` ⇒ 语义错乱；默认表头 name/age/city 不含冒号，不命中，非逃生项。

`node scripts/verify_it_calc.js` → **1083/1083 通过**；`discriminate_check.js verify_it_calc.js` → **已检 1082 / 正确变红 1082 / 逃生 0**。
