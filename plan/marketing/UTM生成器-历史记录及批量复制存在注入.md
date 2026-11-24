# UTM 生成器：历史记录和批量复制拼接未转义内容

受影响工具：`tools/marketing/utm-builder.html`

## 问题描述
`renderHistory()` 将用户填写的 source、medium、campaign 直接插入 `innerHTML`；包含 HTML 标签和事件属性的输入可在打开历史记录时被浏览器解析。历史及批量的复制按钮还把 URL 拼进双引号包裹的 `onclick` 属性，仅转义单引号，基础 URL 中的双引号等字符可能破坏属性边界。这是基于代码的注入风险，需用本地无害样例复核。

## 解决方案
使用 DOM 创建节点、`textContent` 和事件监听器，避免把用户内容嵌入 HTML 或脚本属性；同时安全处理已存历史数据。以含引号、标签、反斜杠及特殊字符的输入验证显示和复制，确认不会执行输入内容。
