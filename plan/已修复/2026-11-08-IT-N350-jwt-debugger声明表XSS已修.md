# IT-N350 jwt-debugger 声明表 DOM XSS —— 已修复，申请复核

- 分类：01-IT开发 / it
- 工具：`tools/it/jwt-debugger.html`
- 移交批次：2026-11-08 批次（真缺陷修复）

## 缺陷原文要点

`decodeJwt()` 用模板串把 payload 的键 `k` 与值 `displayVal` 直接拼进 `claimsHtml`，最后 `claimsDiv.innerHTML = claimsHtml`；payload 完全来自粘贴 token 的解码结果。构造 payload `{"name":"<img src=x onerror=alert(1)>"}` 即执行脚本，可读取 localStorage 里的解析历史。

## 根因

以下四处均为「用户可控串直拼 innerHTML」：

- token 三段可视化：`parts[0]` / `parts[1]` / `parts[2]`
- 校验结论 `issues[].msg`（含 token 内 exp/iat/nbf 格式化时间）
- 声明表 `<code>${k}</code>` 与 `<td>${displayVal}</td>`
- 解析失败分支 `e.message`
- 解析历史列表 `x.time` / `x.token`

## 修复位点

文件 `tools/it/jwt-debugger.html`：

1. 新增转义助手（函数声明，提升可用）：
   `function escapeHtml(s){ return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }`
2. 分段可视化：`escapeHtml(parts[0]) / escapeHtml(parts[1]) / escapeHtml(parts[2].substring(0,40))`
3. 校验结论：`${escapeHtml(i.msg)}`（颜色参数由页面常量决定，不涉用户输入）
4. 声明表：`<code>${escapeHtml(k)}</code>` 与 `<td>${escapeHtml(displayVal)}</td>`；时间字段先格式化成字符串再整体转义（其 `<span>` 变成实体，按纯文本显示，语义不变）
5. 解析失败：`${escapeHtml(e.message)}`
6. 历史列表：`escapeHtml(x.time)` / `escapeHtml(x.token)`

## 验证与判别力说明（harness 限制，须复核方知悉）

- 该页存在顶层样例加载函数，会在「首屏自跑/兜底循环」阶段把 `token-input` 重置为内置样例并重跑 `decodeJwt()`；加上 harness 的 click 上下文不含 `document`，**任何依赖点击注入 token 的断言都会被覆盖**，无法构造稳定的 click 型回归用例。
- 因此本条**未新增 verify 用例**（避免塞入必然假绿的逃生项）。改用探针实跑取证：
  - 注入 payload `{"name":"<img src=x onerror=alert(1)>"}` 的合法 base64url token；
  - 修复后声明表 `claims-info` 的实际 innerHTML 中是 `&lt;img` / `&quot;` 实体，不再是裸标签；
  - 默认样例 token 的渲染结果不变（回归无差异）。
- 既有 `it/jwt-debugger` 用例（header-json 锚、exp=0 已过期）全部 PASS：`node scripts/verify_it_calc.js` → **1073/1073**。

## 备注

若复核方要求必须有自动化护栏，建议方向：给 harness 增加「不跑页面顶层样例函数」的开关，或提供可在 click 上下文中访问的 `document` 代理；在具备该能力前，本条以源码审查 + 探针证据为准。
