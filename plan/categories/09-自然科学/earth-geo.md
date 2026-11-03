# 地学 · tools/{geology,surveying,meteorology,eco,hydraulic 水文}（~150 页）

## 已知问题
## 功能缺陷
- 气象页缺「体感温度综合判据」整合页（现有分散单页）。

## 优化点
- S7 引据：标准/常数出处标注。→ 已落地 10 页（2026-10-27 批14）：气象 7（isa-temperature / pressure-altitude / beaufort-scale / dew-point / saturation-vapor-pressure / wind-chill / heat-index；引 ISO 2533 + ICAO Doc 7488、WMO 蒲福表、GB/T 35227、GB/T 19201、GB/T 27962、Alduchov-Eskridge 1996 与 Bolton 1980、Rothfusz 1990 NWS SR 90-23）+ 水文 3（manning-flow / hazen-williams-headloss / darcy-head-loss；引 Chow 1959、GB 50286、Williams-Hazen 1920、Colebrook-White 1939、Nikuradse/Moody、IAPWS-95）。剩余：geology / surveying / eco / hydraulic 其余页未覆盖。

## 受影响范围
- tools/geology/（36）、tools/surveying/（44）、tools/meteorology/（41）、tools/eco/（39）、tools/hydraulic/（55）

## 进度
- 🔴 待开发

## 2026-11-03 第一轮抽样补充

### 方位角西北象限的数值与文字不一致（高，确认源码缺陷）
- 证据：`tools/surveying/bearing-from-coordinates.html:261-274` ΔN=100、ΔE=-100 时方位角 315°，文字为 N45°W，但「象限角值」计算为 315−180=135°；该值写入可导出的表。
- 影响：`tools/surveying/bearing-from-coordinates.html`，测量明细及导出出现矛盾角度。
- 方案：西北象限改用 360°−方位角，覆盖四象限和坐标轴边界；保留方位角与象限角并排核对。

### 湿度空露点被当作 0℃ 并保留旧表（高，确认源码缺陷）
- 证据：`tools/meteorology/relative-humidity.html:210-219,227-250` 温度 25℃、露点 16.7℃ 后清空露点，主结果按 0℃ 计算约 19.3%，辅助表因空输入提前退出仍保留约 60.0%。
- 影响：`tools/meteorology/relative-humidity.html`，缺测值被当测量值、导出与主结果不一致。
- 方案：空值报错而不替换为零，同步清除明细并禁用导出；说明适用温度范围与过饱和情形。

### 地震分级与矩震级参考单位不一致（高，确认源码文本缺陷）
- 证据：`tools/geology/richter-scale.html:161-163,218-224,240-248` M=4.2 动态结果为「微震」，同页表将 4–4.9 列为「有感地震」；参考表写 Mw=(2/3)lg M₀−10.7 且标 M₀ 单位 N·m，而 N·m 常用常数约为 −6.03。该参考公式不是页面震级转能量程序。
- 影响：`tools/geology/richter-scale.html`，同页等级矛盾，照参考式计算矩震级将严重偏差。
- 方案：核对权威来源后统一分级范围、单位及常数；提供可复制的带单位算例和引用来源。

### 覆盖
- 本轮抽查上述测绘、气象、地质 3 页，源码和数值推导，未做浏览器或线上验证；其余未逐页覆盖。
