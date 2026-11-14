# 442–443 批：EN 名称英文化（machinery 55 页 + general 38 页）

日期：2026-11-15
范围：`i18n/tools/_en_override.json`

## 一、问题

`json/tools.json` 的 `en` 字段仍有 838 页为中文原名，英文态标题、搜索与卡片直接显示中文。
按行业集中度从高到低逐批处理。

## 二、修复

| 批次 | 行业 | 页数 | 典型改名 |
| --- | --- | ---: | --- |
| 442 | machinery | 55 | 螺纹加工参数 → Thread Machining Parameters Calculator；轴承额定寿命 → Bearing Rating Life Calculator |
| 443 | general | 38 | 3D打印时间估算 → 3D Printing Time Estimator；检测（张力/长度/寿命）服务 → Strip Tension, Length and Lifespan Inspection Tool |

命名统一遵循：`<对象> <功能> Calculator/Tool/Estimator/Checker`，不使用尾部括号，
与既有英文名不重复。

## 三、验证

- machinery 残留 **55 → 0**；general 残留 **38 → 0**；全站 `en` 含中文 **838 → 745**。
- 英文重名组 0；`audit_en_meta_degenerate.py --check` 无新增退化。
- `_build.py` 两次构建通过（本次按老板指示不跑全量门禁、不推送）。
