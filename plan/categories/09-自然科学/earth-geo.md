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

### 覆盖
- 本轮抽查上述测绘、气象、地质 3 页，源码和数值推导，未做浏览器或线上验证；其余未逐页覆盖。

## 2026-11-03 续查（并行批 H）

### EG-1 三点法把直立面判成水平面、把真水平面当正常产状（高，确认源码缺陷）
- 描述：`calc()` 仅当 `|C|<1e-9` 时报「三点构成水平面，倾角 0°、无确定倾向」。但 C 是法向量的垂向分量：C≈0 表示法向量水平，即层面**直立**（倾角 90°）；真正的水平面 C=|n|，反而不会进该分支，会一路算完并输出一个确定的倾向/走向。
- 证据：`tools/geology/dip-strike.html:252-266`。node 内存复算：P1(0,0,0)、P2(10,0,0)、P3(0,0,10) → C=0、|n|=100，命中 `:260` 分支，页面提示「三点构成水平面，倾角为 0°，无确定倾向」，而三点确定的平面是 y=0 的直立面（应为倾角 90°、倾向不确定）。真水平面 P1(0,0,100)、P2(50,0,100)、P3(0,40,100) → C=2000、len=2000 不触发该分支，`:268-275` 输出「走向 270.0°、倾向 0.0°、倾角 0.0°」，把无定义方向当成确定值。
- 影响：`tools/geology/dip-strike.html`；直立面被误报为水平面，野外产状判读方向性错误；水平面给出看似确定的走向/倾向。
- 方案：改用 `C/len` 判据——`1-|C|/len ≤ 1e-9` 判水平面（走向/倾向均标「不确定」），`|C|/len ≤ 1e-9` 判直立面（倾角 90°、倾向不确定、走向取水平投影方位）；补测直立、水平、近直立、近水平四组边界用例。

### EG-2 「示例 2×」预设把相对湿度放大到 120%/140%，输出超出物理上限（高，确认源码缺陷）
- 描述：多个气象页的预设由默认值机械乘 2 生成：湿球 25→50℃、60→120%；Humidex 30→60℃、70→140%。两页均无 RH 上限校验（湿球页 `__N` 只拦负值，Humidex 页无 `__tbInputGuard`），点一次预设即得到湿球高于气温、Humidex 210 的荒谬结果，且 `max="100"` 只约束表单、不约束 JS 读取。
- 证据：`tools/meteorology/wet-bulb-temperature.html:321`（T=50、RH=120）、`:251-261`（`__N={"RH":...}` 仅判 <0）；node 复算 `Tw(50,120)=53.85℃` > 气温 50℃（该页 `:124`/`:163` 自述适用 RH≤95%/99%）。`tools/meteorology/humidex.html:256`（T=60、RH=140）、`:213-219`（无守卫）；node 复算 e=280.32 hPa、Humidex=210.2。同类机械 ×2 另见 `tools/meteorology/dew-point.html:319`、`tools/meteorology/absolute-humidity.html:256`（T=50/RH=120）、`tools/meteorology/apparent-temperature.html:262`（T=60/RH=140）、`tools/meteorology/wind-direction.html:250`（deg=450）——这 4 页仅据预设行确认，未逐页复算，记为待验证。
- 影响：`wet-bulb-temperature.html`、`humidex.html`（并波及上述 4 页）；用户一键示例即得到非法输入与失真结果。
- 方案：取消机械 ×2，改为逐页手设合法示例；所有 RH 输入统一校验 0–100（含程序化赋值），湿球页把 5–95% 写成适用范围提示；饱和 100% 处单独说明公式外推误差。

### EG-3 Humidex / 绝对湿度 / 云底高度无输入守卫，空值按 0 参与计算（高，确认源码缺陷）
- 描述：三页共用 `num()` 把 NaN 归 0，`calcTool()` 不做必填校验，清空任一输入仍显示看似正常的主结果；而 `Extras` 在非有限值处提前 return，明细表保留上一次数值，主结果与表互相矛盾，导出用的也是旧表。
- 证据：`tools/meteorology/humidex.html:210,213-219,230-233,248-251`：T 清空、RH=70 → Humidex=−3.2、e=4.28 hPa；RH 清空、T=30 → Humidex=24.4。`tools/meteorology/absolute-humidity.html:210,213-219,230-232,248-251`：T 清空、RH=60 → AH=2.90 g/m³（本应无法计算）；RH 清空、T=25 → AH=0.00 g/m³。`tools/meteorology/cloud-base-height.html:213-219,230-232,248-251`：T 清空、Td=15 → H=−1875 m；两框全空 → H=0 m。
- 影响：上述 3 页；缺测值被当作实测 0，且主结果与可导出的明细表不一致。
- 方案：统一必填校验（空/非数即报错），失败时清空结果与明细并把导出按钮置灰；`num()` 保留 NaN，由校验层处理。

### EG-4 云底高度接受露点高于气温并输出负高度（中，确认源码缺陷）
- 描述：H=(T−Td)×125 无物理约束，Td>T 时得到负云底高度并照常显示与导出。
- 证据：`tools/meteorology/cloud-base-height.html:213-219`：T=10、Td=20 → `-1250 m`（(10−20)×125），同卡英尺值 `-4101.0 ft`（node 复算）。同页 `:162` 只说明「差值 >20℃ 误差增大」，未提 Td>T 非法。
- 影响：`cloud-base-height.html`；笔误即产出负高度，用户无法从页面察觉参数矛盾。
- 方案：要求 T ≥ Td，否则报「露点不得高于气温」并清空；差值 >20℃ 时标注「近似式置信度下降」。

### EG-5 采样设计接受负成本、非法输入后仍可复制旧结果（中，确认源码缺陷）
- 描述：`calc()` 只校验面积与密度，每点成本未校验，负值直接进入总成本；校验失败分支只替换提示文字，不清空 `lastResult`，复制按钮仍取上一次的合法结果。
- 证据：`tools/geology/soil-sample.html:138,188-190,193,202,205`：A=20、D=4、cost=−100 → 估算成本 `-8000 元`（node: (20×4)×(−100)）；把面积清空后结果区显示「请输入有效面积…」，但 `lastResult` 未清，`copyRes()` 仍复制上一组数据。
- 影响：`soil-sample.html`；成本可为负，且错误态下可复制过期结果。
- 方案：成本要求 >0（0 需明示含义）并同步标红；失败分支清空 `lastResult` 并禁用复制；在提示中说明 N 为期望点数、显示值向上取整。

### EG-6 品位储量页接受 >100% 品位并输出金属量大于矿石量（中，确认源码缺陷）
- 描述：品位只校验非负，未设上限。C=150% 时金属量 P=708750 t 大于矿石量 Q=472500 t，页面仍显示「平均品位 150.000%」；校验失败分支同样不清 `lastResult`。
- 证据：`tools/geology/estimate-grade-reserve.html:144-148,162-166,169`。node 复算 S=50000、M=3.5、D=2.7、C=150 → V=175000、Q=472500.00 t、P=708750.00 t、平均品位 150.000%；`:148` 报错后 `:169` 的 `copyRes()` 仍返回上一条 `lastResult`。
- 影响：`estimate-grade-reserve.html`；非物理品位得到自洽但荒谬的储量，且错误态可复制旧值。
- 方案：品位限制 0–100%（g/t 贵金属由提示引导换算），越界报错；失败清空结果与 `lastResult`；增加「金属量 ≤ 矿石量」自检。

### EG-7 矿物硬度表参照物口径前后不一致（低，确认文本缺陷）
- 描述：同页铜币硬度出现三个值：卡内提示与 `REFS` 数据为 3，深度解析写 3.5；输入框声明 0–10 但手输 15 仍按金刚石(10) 输出「可刻划全部参照物」。
- 证据：`tools/geology/mineral-hardness.html:141`（铜币约 3）、`:224`（`{n:'铜币',h:3}`）、`:190`（铜币约 3.5）；`:135`（min=0 max=10）、`:227-244`（无范围校验，hv=15 → 最接近金刚石(10)、可刻划列表含全部参照物）。
- 影响：`mineral-hardness.html`；刻划互检时 0.5 级差会改变「相当／可划」判定；越界输入给出超出莫氏标尺的结论。
- 方案：铜币参照值择一（3 或 3.5）并在卡内提示、深度解析、`REFS` 三处同步；输入限制 0–10，越界提示并回落最近有效级。

### 留存优化
- 公式框把内部校验备注直接写给用户：`humidex.html:120`、`absolute-humidity.html:120`、`cloud-base-height.html:120` 的「校验：无强校验，空值按 0 兜底」；`soil-sample.html:120`、`estimate-grade-reserve.html:120` 的「（本页代码口径）」。建议改写为面向用户的适用范围与精度说明。
- 湿球页适用域三处不一致：`wet-bulb-temperature.html:124`「5–95%RH」、`:163`「RH 5–99%」、`:134` 占位「0–100」；`:362` 深度解析称「饱和时湿球=气温」，而 node 复算 `Tw(35,100)=35.12℃`（高于气温）。建议统一口径并注明 Stull 式在 100% 附近的外推偏差。
- Humidex 深度解析 `:297-298` 先称 40.9 属「极高不适」，紧接着写 40.9 落「痛苦级」。按加拿大环境部分级 40–44 为「极大不适／痛苦」，建议统一术语。
- 矿物硬度 `:135`、`:224` 的经验参照值可加「≈」，避免把经验值写成精确等级。

### 续查覆盖
- 本轮读源码并用 node 内存复算 8 页：`tools/meteorology/{wet-bulb-temperature,humidex,absolute-humidity,cloud-base-height}.html`、`tools/geology/{dip-strike,soil-sample,estimate-grade-reserve,mineral-hardness}.html`。
- 本批新编号 EG-1…EG-7；首轮条目无编号，未重号。
- 仅静态源码与数值推导，未做浏览器、英文态（`?lang=en-US`）、移动端、构建/门禁（`_build.py` / `run_gates.py`）及线上验证；既有 3 页（`bearing-from-coordinates`、`relative-humidity`、`richter-scale`）未复查；EG-2 列出的另外 4 个气象页（dew-point / apparent-temperature / wind-direction 等预设行）记为待验证。
