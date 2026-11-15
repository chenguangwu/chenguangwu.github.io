# 地学 · tools/{geology,surveying,meteorology,eco,hydraulic 水文}（~150 页）

## 功能缺陷
- 气象页缺「体感温度综合判据」整合页（现有分散单页）。

## 受影响范围
- tools/geology/（36）、tools/surveying/（44）、tools/meteorology/（41）、tools/eco/（39）、tools/hydraulic/（55）

## 进度
- 🔴 待开发

## 2026-11-03 第一轮抽样补充

### 覆盖
- 本轮抽查上述测绘、气象、地质 3 页，源码和数值推导，未做浏览器或线上验证；其余未逐页覆盖。

## 2026-11-03 续查（并行批 H）

### 留存优化
- 公式框把内部校验备注直接写给用户：`humidex.html:120`、`absolute-humidity.html:120`、`cloud-base-height.html:120` 的「校验：无强校验，空值按 0 兜底」；`soil-sample.html:120`、`estimate-grade-reserve.html:120` 的「（本页代码口径）」。建议改写为面向用户的适用范围与精度说明。
- 湿球页适用域三处不一致：`wet-bulb-temperature.html:124`「5–95%RH」、`:163`「RH 5–99%」、`:134` 占位「0–100」；`:362` 深度解析称「饱和时湿球=气温」，而 node 复算 `Tw(35,100)=35.12℃`（高于气温）。建议统一口径并注明 Stull 式在 100% 附近的外推偏差。
- Humidex 深度解析 `:297-298` 先称 40.9 属「极高不适」，紧接着写 40.9 落「痛苦级」。按加拿大环境部分级 40–44 为「极大不适／痛苦」，建议统一术语。
- 矿物硬度 `:135`、`:224` 的经验参照值可加「≈」，避免把经验值写成精确等级。

### 续查覆盖
- 本轮读源码并用 node 内存复算 8 页：`tools/meteorology/{wet-bulb-temperature,humidex,absolute-humidity,cloud-base-height}.html`、`tools/geology/{dip-strike,soil-sample,estimate-grade-reserve,mineral-hardness}.html`。
- 本批新编号 EG-1…EG-7；首轮条目无编号，未重号。
- 仅静态源码与数值推导，未做浏览器、英文态（`?lang=en-US`）、移动端、构建/门禁（`_build.py` / `run_gates.py`）及线上验证；既有 3 页（`bearing-from-coordinates`、`relative-humidity`、`richter-scale`）未复查；EG-2 列出的另外 4 个气象页（dew-point / apparent-temperature / wind-direction 等预设行）记为待验证。
