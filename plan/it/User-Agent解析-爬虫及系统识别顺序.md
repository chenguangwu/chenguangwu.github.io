# User-Agent 解析：爬虫及系统识别顺序

## 问题
浏览器识别先匹配 Chrome，后匹配 Googlebot，包含 Chrome 标记的 Googlebot UA 因此被识别成 Chrome；系统识别先匹配 Linux，后匹配 CrOS，若同时包含两者则会误判成 Linux。

## 解决方案
优先识别特定爬虫和更具体的操作系统标记，建立包含 Chrome 的 Googlebot UA、同时包含 Linux 与 CrOS 的 UA 等回归样例。

## 受影响的工具路径
- `tools/it/user-agent-parser.html`
