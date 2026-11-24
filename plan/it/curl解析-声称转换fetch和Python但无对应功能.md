# curl 解析说明声称可生成代码但页面缺少入口

- 受影响工具：`tools/it/curl-parser.html`
- 问题：页面说明声称可转换为 fetch 或 Python requests 代码，但当前解析输出只有方法、URL、请求头、请求体和结构化 JSON，未见生成或复制这两种代码的入口，用户预期落空。源码分析，需在页面复核。
- 解决方案：优先补充纯前端 fetch 和 Python requests 代码生成、语法高亮和复制，并明确无法安全还原的 curl 选项；如暂不支持，修正中英文页面说明、指南和 SEO 文案。
