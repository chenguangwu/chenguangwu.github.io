# Nginx 速查：示例标明指令上下文

- 受影响工具：`tools/it/nginx-cheatsheet.html`
- 问题：`limit_req_zone` 和 `limit_conn_zone` 示例直接与 `location` 并列，未说明前者须放在 `http` 上下文、后者位于 `server` 下的 `location`；用户直接复制到同一位置可能导致配置检测失败。源码分析，需对照目标 Nginx 版本文档和配置检测复核。
- 解决方案：提供包含 `http`、`server`、`location` 的最小完整示例，并标注每条指令支持的上下文和 `nginx -t` 验证方式；同步复制示例及中英文说明。
