# 474 · pet-training / petrochem / photo2 / plastic 英文态清零（19 页 53 条）

## 问题
- 宠物训练：点击时机、命令重复记忆保持率、排泄预测、牵引绳安全距离公式。
- 石化：API 比重与原油分类、催化剂装填、蒸馏塔物料平衡、管道压降（Swamee-Jain）、卧式罐液位。
- 摄影：视频文件大小与录制时长、白平衡色温 placeholder。
- 塑料：吹胀比、注塑周期、成型收缩率。

## 处理
只改源 `i18n/tools/en/<ind>/<slug>.json` 的 `map`，共 53 条。
`petrochem/distillation-yield` 的「平衡状态：…」在 EN 态被 `_prefix` 半译为 `Balance state：…`，
按 zh 源文作键；`tank-capacity` 的公式被拆成两个文本节点，分别按完整 zh 片段作键。

## 验证
- pet-training / petrochem / photo2 / plastic 四行业 `--check` 全部 **残留 0**（19 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
