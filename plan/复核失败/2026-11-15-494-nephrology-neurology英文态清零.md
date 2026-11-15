# 第 494 批复核失败：神经科两页英文态深览未译

- 原要求：nephrology 和 neurology 两行业英文态残留清零，包括 TWSTRS 量表说明与算例。
- 未落实：`neurology/rater-21` 与 `neurology/twstrs` 的深度解析标题、场景、算例及问答仍显示中文，应按现有页面文本补充准确译文并复测。
- 验证证据：`node scripts/_en_i18n_probe.mjs --check neurology` 当前 25 页中 2 页有残留，分别 12 处及 11 处；`--check nephrology` 23 页残留 0。
