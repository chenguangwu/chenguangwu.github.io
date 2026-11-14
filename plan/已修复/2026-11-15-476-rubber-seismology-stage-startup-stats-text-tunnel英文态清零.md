# 476 · rubber / seismology / stage / startup / stats / text / tunnel 英文态清零（20 页 71 条）

## 问题
- 橡胶：阿伦尼乌斯等效硫化时间、邵氏硬度换算、phr 配料、拉伸强度。
- 地震：震源机制解、中国地震烈度表（PGA/PGV/震害指数/宏观现象四路）、应急响应分级、G-R 与大森公式。
- 舞台：光束角覆盖、调光曲线 placeholder、灯位角度、负载配电、色温滤片。
- 创业：启动资金、股权分配与稀释。
- 文本/统计/隧道：统计口径说明与 4 个 placeholder。

## 处理
只改源 `i18n/tools/en/<ind>/<slug>.json` 的 `map`，共 71 条。
`seismology/analysis-stress`（`输入：`→`Input:`）、`stage/power-load`（`输入：`→`Input:`）被 `_prefix` 半译，
按 zh 源文作键；地震烈度表保留罗马数字等级与 `→` 符号。

## 验证
- 7 个行业 `--check` 全部 **残留 0**（20 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
