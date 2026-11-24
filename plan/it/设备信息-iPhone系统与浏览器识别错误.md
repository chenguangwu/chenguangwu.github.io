# 设备信息：修正 iPhone 系统和浏览器识别

- 受影响工具：`tools/it/device-info.html`
- 问题：系统识别先匹配 `Mac OS X` 再检查 `iPhone`，常见 iPhone User-Agent 同时含两者，会被识别为 macOS，触摸点大于 1 时还可能被识别为 iPadOS。浏览器识别只匹配 `Chrome/`、`Firefox/`、`Edg/`，iOS 版浏览器的 `CriOS/`、`FxiOS/`、`EdgiOS/` 因而会误识别或显示未知。依据源码分析，待真机或模拟 UA 验证。
- 解决方案：优先判定显式 iPhone/iPod/iPad，再谨慎处理桌面模式 iPad；补充 iOS 浏览器标识并明确 UA 冻结、伪装和无法区分时的限制。用 iPhone Safari、Chrome、Firefox、iPad 桌面 UA 和 macOS 触摸设备样例验证。
