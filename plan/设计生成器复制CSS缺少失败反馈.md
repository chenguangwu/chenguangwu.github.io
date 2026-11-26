# 多个设计生成器复制 CSS 失败时无反馈

- 受影响工具：`tools/design/dot-pattern.html`、`tools/design/checkerboard-generator.html`、`tools/design/isometric-grid.html`、`tools/design/blueprint-grid.html`、`tools/design/stripe-pattern.html`、`tools/design/card-generator.html`、`tools/design/button-generator.html`、`tools/design/badge-generator.html`
- 问题：这些页面直接调用 `navigator.clipboard.writeText()`，只处理成功分支；浏览器接口不可用或权限拒绝时，用户无法获得明确的失败提示。依据源码，具体浏览器行为待复核。
- 解决方案：复用统一复制能力，检查接口并捕获同步异常及异步拒绝；失败时提供中英文提示和手动选中代码的方式。覆盖成功、拒绝权限和接口不可用场景。
