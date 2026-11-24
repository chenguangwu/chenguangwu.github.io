# Markdown 转 HTML：文本中的 Infinity 和 NaN 被替换

## 问题描述

输入 Markdown 正文 `Infinity and NaN` 并转换，结果渲染前对整段 HTML 执行全局替换，预览及 HTML 代码面板中的两个词均变为破折号。代码块、链接地址或普通文字包含这些合法字符串时也会受到影响，复制生成的 HTML 会改变原文。

## 解决方案

对文本转换结果只做必要的 HTML 转义，不对生成的整段 HTML 替换数值关键词；若需检测数值异常，应在对应数值计算处处理。验证普通正文、代码块、链接地址中的 `Infinity` 和 `NaN` 与输入一致。

## 受影响工具路径

- `tools/it/markdown-to-html.html`：`calcTool()` 的结果渲染。
