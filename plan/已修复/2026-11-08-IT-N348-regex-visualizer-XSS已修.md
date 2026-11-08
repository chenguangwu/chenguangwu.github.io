# IT-N348 regex-visualizer 正则内容 DOM XSS —— 已修复，申请复核

- 分类：01-IT开发 / it
- 工具：`tools/it/regex-visualizer.html`
- 移交批次：2026-11-08 批次（真缺陷修复）

## 缺陷原文要点

`render()` 把 token 直接拼进状态标签与边标签的 `innerHTML`，未做 HTML 转义；`<`、`>`、`=`、`/` 都是合法正则字面量，`new RegExp` 校验不拦截。输入 `<img src=x onerror=alert(1)>` 即注入 DOM XSS，且历史/预设恢复路径会回填重放。

## 根因

用户可控串（正则 token、token 切分后的边标签、`new RegExp` 抛出的 `e.message`）以模板串形式直接进入 `innerHTML`。

## 修复位点

文件 `tools/it/regex-visualizer.html`：

1. 新增转义助手（函数声明，提升可用）：
   `function escapeHtml(s){ return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }`
2. `buildStates()` 状态标签：`states.push({id, label: \`${escapeHtml(t)}\`})`
3. 渲染边标签：`const lab = escapeHtml(tokens[i] || 'ε')`
4. 非法正则分支：`` `<p>正则不合法：${escapeHtml(e.message)}</p>` ``

状态/边标签仍为 HTML 字符串拼接，但所有用户可控片段已转义，标签结构本身由页面常量构成。

## 判别力实测

新增回归用例（`scripts/verify_it_calc.js`，紧跟原 regex-visualizer 用例）：

```
slug:   it/regex-visualizer
inputs: { pattern: "a<b" }
clicks: ["render()"]
expect: ["S2: &lt; S3: b"]
```

- 注入 `a<b` ⇒ 状态标签 S2 的 `<` 若未转义会变成标签起始字符（被 harness 剥标签吃掉，且真实浏览器里是注入点）；转义后为 `&lt;`。
- 默认 pattern `^a[0-9]+b$` 不含 `<` ⇒ 该串只在注入态出现，非逃生项。
- 实测：`node scripts/verify_it_calc.js` → **1073/1073 通过**；`node scripts/discriminate_check.js verify_it_calc.js` → **已检 1072 / 正确变红 1072 / 逃生 0**。

## 备注

- harness 的 click 执行上下文不含 `document`（`document` 引用即 ReferenceError），因此用例只能直接调工具函数，不能靠 click 里改 innerHTML 做断言；本条用例仅用 `render()`，不受影响。
- `errs` 中的 `buildStates: tokens is not iterable` / `tokenize: ...` 来自 harness 兜底循环无参调用顶层函数，属良性产物，非工具缺陷。
