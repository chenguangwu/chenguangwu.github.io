# Tailwind 色板键盘操作缺失

## 问题
色块使用带 tabindex 的 div 并只绑定点击，键盘聚焦后无法用 Enter 或空格激活；详情浮层缺少 Escape 关闭和焦点管理。

## 解决方案
使用原生按钮，并为详情提供焦点进入、Escape 关闭和关闭后焦点返回。

## 受影响工具路径
- `tools/design/tailwind-colors.html`
