# 表单名称兜底未覆盖仅有 placeholder 的控件

来源：已修复第 675 批。`js/tool-ux.js:417` 仅查询 `select[title],input[title],textarea[title]`，虽然读取时回退 `placeholder`，但无 title 的控件根本不会进入循环。例 `tools/it/css-minifier.html:182` 的输入框只有 placeholder，缺少关联 label 和可访问名称，不能实现记录声称的 placeholder 兜底。

修复方案：让候选选择器覆盖 placeholder-only 的相关控件，继续跳过已有显式名称和关联标签的控件；验证动态添加与中英文切换，使用无 title 的真实页面及 axe/无障碍树覆盖。
