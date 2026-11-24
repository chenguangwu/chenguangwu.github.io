# BMR：缺少剪贴板接口时复制无法降级

受影响工具：`tools/healthcare/bmr-calculator.html`

## 问题描述
`copyResult()` 直接调用 `navigator.clipboard.writeText()`，只有该调用返回的 Promise 被拒绝时才进入降级逻辑。若浏览器或非安全上下文没有 `navigator.clipboard`，会在调用时同步抛错，降级路径不会执行；错误提示文本也可能被当作结果复制。

## 解决方案
先检测接口并捕获同步和异步失败，使用可靠的备用复制方式或提供手动复制提示；仅在计算结果有效时允许复制，并分别验证成功、拒绝和接口缺失。
