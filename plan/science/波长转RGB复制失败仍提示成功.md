# 波长转 RGB 复制失败仍提示成功

## 问题

`tools/science/wavelength-to-rgb.html` 的复制按钮调用 `navigator.clipboard.writeText` 后立即显示“已复制”，没有等待 Promise 成功或处理权限拒绝、非安全上下文等失败情况。用户可能看到成功提示却没有获得色值；英文态的该提示也直接使用中文。以上为静态检查，具体浏览器表现待核验。

## 解决方案

等待剪贴板写入成功后再提示成功；不可用或失败时提供明确提示及可手动选择的 HEX 值，并按当前语言显示反馈。验证成功、权限拒绝及剪贴板 API 不可用的情况。

## 受影响工具路径

- `tools/science/wavelength-to-rgb.html`
