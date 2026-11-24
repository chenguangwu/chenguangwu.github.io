# KDIGO 急性肾损伤：两套历史记录并存

受影响工具：`tools/nephrology/jixingshensunshang-kdigo-fenqi.html`

页面每次成功计算会通过 `saveHistory()` 写入独立 localStorage 键；该历史的 `renderHistory()` 因页面不存在 `#historyBox` 而直接退出。页面另有 `TBKit.history` 面板及清除按钮，两套存储不同，因此清空可见历史不一定清除前者保存的肌酐、体重与分期。源码已确认写入与缺失容器，本地隔离浏览器实测一次计算后两套键均存在；点击可见历史的清空按钮后，`tb_history_/tools/nephrology/jixingshensunshang-kdigo-fenqi.html` 仍存在。

解决方案：统一为一套可见、可管理的本地历史，制定旧键迁移或删除方案；清空历史时覆盖所有旧键，确保提示真实。测试计算、刷新、恢复、清空和重新打开页面，并确认不影响其他工具的数据。历史恢复字段不完整的共性问题另见 `plan/历史恢复遗漏空字段.md`。
