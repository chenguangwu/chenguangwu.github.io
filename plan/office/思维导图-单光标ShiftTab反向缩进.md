# 思维导图：单光标 Shift+Tab 增加缩进

受影响工具：`tools/office/mindmap.html`

问题：无选区时 Tab 与 Shift+Tab 均插入两个空格，与页面“Shift+Tab 减少层级”的提示相反，容易误改结构。

解决方案：根据 Shift 状态处理当前行的缩进或退缩，并保持光标位置；验证无选区、跨行选区、行首及无可退缩空格。
