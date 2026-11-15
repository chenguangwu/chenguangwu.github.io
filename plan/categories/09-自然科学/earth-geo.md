# 地学 · tools/{geology,surveying,meteorology,eco,hydraulic 水文}（~150 页）

## 功能缺陷
- 气象页缺「体感温度综合判据」整合页（现有分散单页）。

## 受影响范围
- tools/geology/（36）、tools/surveying/（44）、tools/meteorology/（41）、tools/eco/（39）、tools/hydraulic/（55）

## 进度
- 🔴 待开发

## 2026-11-03 第一轮抽样补充

### 湿度过饱和时错误提示与明细表矛盾（高，确认源码缺陷）
- 2026-11-06 复核：`tools/meteorology/relative-humidity.html:212-216,230-245,263-264` 已对空值报错并清空表；但 Td>T 时主函数清空表并报错，外层仍调用明细函数，后者只检查有限数值，重新填入过饱和结果。
- 证据：Node 模拟页面实际函数与表格接口，T=10、Td=20 时主结果报错，明细仍写入 RH 190.3%；表格导出仍可调用。未做浏览器验证。
- 影响：`tools/meteorology/relative-humidity.html`，无效输入仍产生可导出数值。
- 方案：主结果与明细共用验证结果，非法时不重建表，并禁用导出；说明适用温度范围与过饱和情形。

### 覆盖
- 本轮抽查上述测绘、气象、地质 3 页，源码和数值推导，未做浏览器或线上验证；其余未逐页覆盖。

## 2026-11-03 续查（并行批 H）

### EG-1 水平面和直立面结果不能复制（中，确认源码缺陷）
- 2026-11-06 复核：`tools/geology/dip-strike.html:259-277` 已分别按归一化法向量识别直立面与水平面，原误判已修；但两分支的详情不含「产状结果」字样，`copyResult()`（`:296-300`）只接受包含该字样的详情，故已计算出的特殊面结果不能通过复制按钮复制。
- 影响：`tools/geology/dip-strike.html`；水平面和直立面的有效结果无法复制。
- 方案：复制按钮支持特殊面结果，并分别覆盖普通面、水平面及直立面；尚未浏览器验证。

### EG-2 湿度越界时主结果报错但明细仍计算（高，确认源码缺陷）
- 2026-11-06 复核：`wet-bulb-temperature.html:281-285,297-308,321-328`、`humidex.html:212-216,230-245,255-264` 的示例已替换为合法值，主结果已校验 RH 上限；`dew-point`、`absolute-humidity`、`apparent-temperature`、`wind-direction` 的原机械倍增预设也已替换。
- 残留：明细函数只判断有限数值，外层在主函数报错后仍调用明细。Node 模拟实际函数与表格接口，`humidex.html` 在 T=30、RH=140 时主结果报错而表中写入 57.4；`absolute-humidity.html` 在 T=25、RH=120 时主结果报错而表中写入 27.55 g/m³。湿球页源码同样存在此路径，Node 桩运行失败，尚未实测。
- 影响：湿球、Humidex、绝对湿度页的非法输入表格仍可导出；露点、体感温度等页面是否存在同样残留尚未核验。
- 方案：统一主计算和明细校验，非法时不渲染表格或记录历史；覆盖越界及恢复有效输入。

### EG-4 云底高度主结果报错但明细输出负高度（中，确认源码缺陷）
- 2026-11-06 复核：`tools/meteorology/cloud-base-height.html:212-216,230-245,263-264` 已在主结果拦截 Td>T，但包装函数随后仍调用仅检查有限值的明细函数。
- 证据：Node 模拟页面实际函数与表格接口，T=10、Td=20 时主结果报错，表中仍写入 `-1250 m` 和 `-4101.0 ft`，导出函数仍可调用；未做浏览器验证。
- 影响：`cloud-base-height.html`；非法参数仍生成可导出负高度。
- 方案：主结果和明细统一校验，错误时清空并禁用导出；差值 >20℃ 时标注近似式的适用限制。

### 留存优化
- 公式框把内部校验备注直接写给用户：`humidex.html:120`、`absolute-humidity.html:120`、`cloud-base-height.html:120` 的「校验：无强校验，空值按 0 兜底」；`soil-sample.html:120`、`estimate-grade-reserve.html:120` 的「（本页代码口径）」。建议改写为面向用户的适用范围与精度说明。
- 湿球页适用域三处不一致：`wet-bulb-temperature.html:124`「5–95%RH」、`:163`「RH 5–99%」、`:134` 占位「0–100」；`:362` 深度解析称「饱和时湿球=气温」，而 node 复算 `Tw(35,100)=35.12℃`（高于气温）。建议统一口径并注明 Stull 式在 100% 附近的外推偏差。
- Humidex 深度解析 `:297-298` 先称 40.9 属「极高不适」，紧接着写 40.9 落「痛苦级」。按加拿大环境部分级 40–44 为「极大不适／痛苦」，建议统一术语。
- 矿物硬度 `:135`、`:224` 的经验参照值可加「≈」，避免把经验值写成精确等级。

### 续查覆盖
- 本轮读源码并用 node 内存复算 8 页：`tools/meteorology/{wet-bulb-temperature,humidex,absolute-humidity,cloud-base-height}.html`、`tools/geology/{dip-strike,soil-sample,estimate-grade-reserve,mineral-hardness}.html`。
- 本批新编号 EG-1…EG-7；首轮条目无编号，未重号。
- 仅静态源码与数值推导，未做浏览器、英文态（`?lang=en-US`）、移动端、构建/门禁（`_build.py` / `run_gates.py`）及线上验证；既有 3 页（`bearing-from-coordinates`、`relative-humidity`、`richter-scale`）未复查；EG-2 列出的另外 4 个气象页（dew-point / apparent-temperature / wind-direction 等预设行）记为待验证。
