# 全站真实浏览器运行时错误扫描

- 扫描时间：2026/11/5 03:28:01
- 覆盖页数：**4912**
- 有运行时错误的页数：**1923**
- 错误类型聚合条数：**1**
- 导航超时/崩溃页：**4912**
- 填充输入后点击：**0** 页（fill 阶段）

> 口径：console error（已剔除资源 404 / net::ERR 等环境噪音）+ 未捕获 pageerror（含首个堆栈帧）；`requestfailed` 仅记录不算缺陷。触发方式：load=页面加载、click=默认值直接点主按钮、fill=填充空输入后点主按钮。点击后结果区无变化**只作线索**（页面可能在 load 时已自动执行同名初始化）。

## 按影响页数降序

| # | 页数 | 触发 | 错误文本 | 代表页面 |
|---|---|---|---|---|
| 1 | 1923 | load | `FILL is not defined` | `tools/accessibility/accessible-restroom.html`<br>`tools/accessibility/braille-translator.html`<br>`tools/accessibility/index.html`<br>`tools/accessibility/ramp-slope.html`<br>`tools/accessibility/sign-language.html` |

