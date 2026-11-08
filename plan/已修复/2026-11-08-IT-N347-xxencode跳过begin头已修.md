# IT-N347 xxencode 把 begin 头当数据行解码 —— 已修复，申请复核

- 分类：01-IT开发 / it
- 工具：`tools/it/xxencode.html`
- 移交批次：2026-11-08 批次（真缺陷修复）

## 缺陷

`decodeXx()` 用 `let started = !document.getElementById('withHeader').checked;` 决定是否跳过 `begin` 行。默认未勾选 ⇒ 视为纯数据 ⇒ 粘贴含 `begin 644 file.txt` 的标准全文时，该行首字符 `b` 命中字母表（长度=38），被当数据行解码，输出前几字节乱码且无提示。

## 修复

`tools/it/xxencode.html` `decodeXx()`：

```js
let started = !lines.some((l) => /^begin\s+\d+\s+\S*/.test(l.trim()));
```

只要文本中出现 `begin` 头就无条件跳过它；勾选项只保留「编码时是否输出 begin/end 头」的语义。纯数据段（无头行）仍按数据行解析，不破坏原有用法。

## 判别力实测

新增回归用例：

```
slug: it/xxencode
inputs: { input: "begin 644 z.txt\n4Ka3kQ4Jm\n+\nend" }
clicks: ["dec()"]
expect: ["Zapper"]
```

向量手算可复算：Zapper = 5A 61 70 70 65 72；
- 长度字符 XX[6] = `4`
- 组1 22/38/5/48 → `Ka3k`
- 组2 28/6/21/50 → `Q4Jm`

修复前头行被当数据行 ⇒ 正文错位、输出脏字节，`Zapper` 不出现；默认勾选态为未勾（即本条走的就是出问题的默认路径），默认样例内容不同 ⇒ 非逃生项。

既有 `Hi → 0G4Y+` 编码用例仍 PASS（编码侧未改）。

`node scripts/verify_it_calc.js` → **1076/1076 通过**；`discriminate_check.js verify_it_calc.js` → **逃生 0**。
