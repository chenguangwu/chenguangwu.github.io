# JWT 解析器：无效头部后定时刷新恢复声明

## 问题

头部解析失败时页面会清空声明检查，但每秒的 `refreshJwtClock()` 只要输入非空便调用 `checkClaims()`；后者只解析第二段 payload，不检查头部是否有效。因此输入 `!.eyJleHAiOjQxMDI0NDQ4MDB9.x` 后，页面先显示头部解析错误，约一秒后仍出现该 payload 的过期状态，容易让用户误以为无效 Token 已通过完整解析。此为源码分析，需浏览器复核。

## 解决方案

仅在当前 Token 的头部与 payload 均成功解析且状态有效时刷新声明；输入变化和解析失败应使刷新状态失效。验证无效头部、有效 payload、修正输入与语言切换，并继续明确声明检查不等于验签。

## 受影响工具路径

- `tools/it/jwt-parser.html`
