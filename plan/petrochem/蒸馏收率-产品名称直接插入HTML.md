# 蒸馏收率-产品名称直接插入HTML

受影响工具：`tools/petrochem/distillation-yield.html`

问题：产品名称来自输入框，直接插入结果的 innerHTML；含 HTML 标记的名称会被浏览器解析为节点，而不是按文字展示。

解决方案：用 textContent 创建名称节点或正确转义文本，验证尖括号、引号及事件属性等输入按原文显示。
