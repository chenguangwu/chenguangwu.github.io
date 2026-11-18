# 长尾行业汇总（<20 页的 190+ 行业）

> 本文件只收录**已知具体问题**（来自 16 批审计备案）；长尾行业共性问题（留存/性能/EN）统一走 plan/G 系列，不在此重复。

## 2026-11-06 二手车保养静态续审（清单 650）

- `tools/usedcar/recorder-maintenance.html:314-353,356-367,385-419`：里程低于首个保养阈值时，即使没有任何记录也判完整度 100 分、估值增值 12.5%；期望项目按名称去重，一项只需历史任意一次记录即可覆盖，不检查周期或是否近期完成。输入空里程/估值被记 0；未填保养日期按 UTC 日期补，费用空按 0。残值倍数及车型保养周期须专业复核；未运行页面。

## 2026-11-06 公共安全与服务工具静态续审（清单 614–621）

- `tools/security/anti-fraud-cards.html:551-637`：搜索和分类筛选、展开、随机卡片均有代码路径；未核验防骗资料及时效，也未运行页面。
- `tools/security/virtual-safe.html:722-748`（部分修复，720 批）：明文 CSV 导出的标题/内容/时间改走 `vsEsc`，不再直接拼进 `innerHTML`；剩余：加密备份只导出 `items`（缺主盐且页面无导入），不能作为清存储后的完整恢复；自制密钥派生 + XOR 仍不适合高敏数据，未运行注入或读取用户数据。

## 2026-11-06 云属速查静态续审

- `tools/meteorology/cloud-identify.html:228-249`：搜索与云族选择共同过滤固定 `DATA`，无匹配时显示空态；本轮仅读主要交互代码，未核验云图、气象描述、导出及浏览器行为。

## 受影响范围
- tools/ 其余 190+ 长尾行业目录

## 进度
- 🟡 按需增量（新问题随批次追加于此）

## 长尾行业通用优化指引
- 留存/分享/场景预设等共性优化统一执行 `plan/G06-留存与竞争力升级.md`（S1 首屏即答案、S2 场景预设、S4 分享卡按流量数据择优覆盖长尾）。
- 文案类改动一律先查数据源（`plan/G03`）。

## 2026-11-03 审计补充

### 留存优化：保留质控复核证据（中，建议）
- 证据：同页 `:124-130,222-230` 支持批量录入和导出，并按阈值计算逐样本偏差。
- 影响：同页；方案：导出有效及拒绝行、阈值、超差原因与口径，允许一键筛选待复检样本；明确 90% 为页面采用的判定假设。

### Cpk 清空/σ=0 时数据表状态待核查（中，待运行复核）
- `tools/process/cpk-index.html:281-293,310-313`：σ>0、USL>LSL 检查已加，非法输入主结果提示并清表；仍需分别核查清空或 σ=0 经通用守卫提前返回时的数据表状态；均值超规格产生负 Cpk 本身可以成立。未做浏览器回归。

### 覆盖
- 本轮抽查地质质控及上述 10 个不同目录页面共 11 页；其余长尾行业未逐页覆盖。新增 10 条为源码及算术推导，未做浏览器、专业规范及线上验证。

## 2026-11-03 续查（并行批 G）

> 本批覆盖 8 个上文未出现的长尾行业页面（beekeeping / daily-goods / railway / stats / bridge / tunnel / seismology / bonding），均按源码逐行阅读并用 node 内存复刻页内公式取证。

### 留存优化
- `tools/beekeeping/honey-estimator.html`：保存蜂场/蜜源/气候/经验方案，导出年度产量与收入对照，支持按蜜源品种并列比较。
- `tools/daily-goods/shoe-size.html`：增加脚长→多品牌尺码预设与家庭成员脚长档案，结果附"预留 5–10 mm"说明并可分享。
- `tools/railway/power-5.html`：并列起动/持续工况与功率裕度，保存车型与编组方案，导出选型对比。
- `tools/stats/sample-size.html`：保存研究方案（置信度/误差/p/N），导出方法说明，并给 p 未知时 p=0.5 的敏感性对照。
- `tools/bridge/deflection-calc.html`：保存梁参数与荷载组合，提供短期/长期（×1.6~2.0）双结果与规范限值切换。
- `tools/tunnel/ventilation-calc.html`：双模式并排比较并给出取大值建议，保存断面与交通量方案。
- `tools/seismology/stats-attenuation.html`：保存序列与 K/c/p 参数，叠加理论衰减曲线并标注拟合区间。
- `tools/bonding/analysis-resolution.html`：把现象/基材/工艺参数/处置保存为可检索故障库，导出排查清单。

### 续查覆盖
- 本轮新增覆盖 8 页：`tools/beekeeping/honey-estimator.html`、`tools/daily-goods/shoe-size.html`、`tools/railway/power-5.html`、`tools/stats/sample-size.html`、`tools/bridge/deflection-calc.html`、`tools/tunnel/ventilation-calc.html`、`tools/seismology/stats-attenuation.html`、`tools/bonding/analysis-resolution.html`；均为上文未出现的目录/页面。
- 方法：逐页读源码，node 内存复刻页内公式与取值口径（含 `+''` 空值转 0、`Math.round` 半码、`toFixed` 对 Infinity/NaN 的表现）；证据均为"文件路径:行号 + 复现输入 → 实际输出"。
- 未做：真实浏览器点击、英文态（`?lang=en-US`）、移动端、构建与门禁（`_build.py` / `run_gates.py`）验证；G2 的美/英码品牌口径属标准层面，标待验证。

## 2026-11-03 续查（并行批 I）

> 本批覆盖 8 个上文未出现的长尾行业页面（aquaculture×2 / glass / plastic / shipping / logistics2 / project / petrochem），均按源码逐行阅读并用 node 内存复刻页内公式取证；未做浏览器、英文态、移动端与门禁验证。

### 留存优化
- `tools/aquaculture/density-7.html`：保存鱼种/水温/密度方案，导出存活率-时长曲线，并给出"目标 95% 存活的最长运输时长"。
- `tools/aquaculture/area-power.html`：保存池塘/品种/目标溶氧方案，并列 1/2/4/8 h 曝气时长下的功率与台数。
- `tools/glass/annealing-curve.html`：保存玻璃品类/厚度/终温曲线，导出阶段时间表，并支持 2–3 套退火制度对比。
- `tools/plastic/extrusion-rate.html`：保存螺杆/材料配方，按转速扫描产量并导出选型表；单位在 kg/h 与 t/月间切换。
- `tools/shipping/convert-speed-1.html`：记住常用单位对，支持批量换算及由航速/时间反算航程。
- `tools/logistics2/inventory-aging.html`：保存周期/阈值与明细快照，导出接受/拒绝行，支持按库龄与周转天数双排序。
- `tools/project/manager-cost.html`：保存项目基线（BAC/工期/各期 PV/EV/AC），支持多版本对比与 EAC 算法切换。
- `tools/petrochem/tank-capacity.html`：保存罐体参数，叠加液位-体积表与安全上限标线，导出盘点记录。

### 续查覆盖
- 本轮新增覆盖 8 页：`tools/aquaculture/density-7.html`、`tools/aquaculture/area-power.html`、`tools/glass/annealing-curve.html`、`tools/plastic/extrusion-rate.html`、`tools/shipping/convert-speed-1.html`、`tools/logistics2/inventory-aging.html`、`tools/project/manager-cost.html`、`tools/petrochem/tank-capacity.html`；均为上文未出现的页面。
- 方法：逐页读源码，node 内存复刻页内公式与取值口径（含 `parseFloat(...) || 0` 的空值转 0、`toFixed` 对 Infinity 的表现、HTML `min/max` 只管步进器不拦手输）；证据均为"文件路径:行号 + 复现输入 → 实际输出"。
- 新增 8 条，其中高优 4 条（I1–I5 中的 I1/I2/I4/I5）；I3/I6/I7/I8 为中优。管理页保存/加载行为（`d.bac || 100000`、`d.totalDays || 90`）为源码推导，未做浏览器 localStorage 实测。
- 未做：真实浏览器点击、英文态（`?lang=en-US`）、移动端、构建与门禁（`_build.py` / `run_gates.py`）验证；也未比对行业规范/厂商参数，所有结论仅基于源码与算术复算。

## 2026-11-03 续查（并行批 J）

> 本批覆盖 8 个上文未出现的长尾行业页面（express / accessibility / photo2×3 / gardening2 / chess / edu2），均逐页读源码并用 node 内存复刻页内公式取证；未做浏览器、英文态、移动端与门禁验证。

### 12-J6 视频存储分钟上限口径待确认
- 时长/码率零负与负容量已于 978 批修复并补 verify 回归锁。
- 残留：`minutes` 仅要求非负，未限制 0–59；输入 90 分钟会按 1.5 小时折算。是否应视为非法需产品口径确认，不自判。

### 留存优化
- `tools/express/insurance-fee.html`：保存常用声明价值与承运商组合，导出含保额上限/免赔说明的投保清单。
- `tools/accessibility/ramp-slope.html`：保存场景/坡度/高差方案，按 1:20、1:12、1:10 并列平台数与总斜长。
- `tools/photo2/exposure-triangle.html`：保存拍摄场景的曝光组合，等量曝光表支持"只改光圈/只改快门/只改 ISO"三模式切换并可分享。
- `tools/photo2/focal-length.html`：保存机身+镜头清单，按常用焦段批量出视角表，附"同画幅等效=原焦距"的校验提示。
- `tools/photo2/video-storage.html`：保存拍摄规格（分辨率/帧率/码率/编码），并列 32–512GB 卡与常见硬盘的可录时长。
- `tools/gardening2/fertilizer-ppm.html`：保存肥料标签（N/P/K 百分比）与目标 ppm 配方，正反算同屏并可导出配肥卡。
- `tools/chess/elo-rating.html`：保存棋手与赛程，批量模拟多局 K 值敏感性，导出升降分曲线。
- `tools/edu2/schedule-conflict.html`：保存多版本课表与教师/教室资源，导出冲突清单和可接受/拒绝行，支持单双周标记。

### 续查覆盖
- 本轮新增覆盖 8 页：`tools/express/insurance-fee.html`、`tools/accessibility/ramp-slope.html`、`tools/photo2/exposure-triangle.html`、`tools/photo2/focal-length.html`、`tools/photo2/video-storage.html`、`tools/gardening2/fertilizer-ppm.html`、`tools/chess/elo-rating.html`、`tools/edu2/schedule-conflict.html`；均为上文未出现的目录/页面。
- 新增 10 条，其中高优 2 条（J1、J3），其余 8 条为中优；无低优条目。按页面计 8 页，按问题计 10 条（曝光三角、液肥稀释各拆 2 条）。
- 方法：逐页读源码，node 内存复刻页内公式与取值口径（含 `+''` 空值转 0、`||` 默认替换、`toFixed` 对 Infinity/NaN 的表现、闭区间与半开区间重叠判定）；证据均为"文件路径:行号 + 复现输入 → 实际输出"。
- 未做：真实浏览器点击、英文态（`?lang=en-US`）、移动端、构建与门禁（`_build.py` / `run_gates.py`）验证；快递公司实际保额上限属厂商/保险条款层面，未逐条核对，相关数值标待验证。

## 2026-11-03 续查（并行批 K）

> 范围：本轮阅读 8 页——`tools/chemical/solution-concentration.html`（chemical）、`tools/mining/convert-grade-ore.html`（mining）、`tools/hvac/cooling-load.html`（hvac）、`tools/paper/roll-length.html`（paper）、`tools/fire/hydrant-pressure.html`（fire）、`tools/gas/load-1.html`（gas）、`tools/security/flood-level.html`（security）、`tools/transport/convert-volume-weight.html`（transport）。仅源码 + node 内存复算，未开浏览器，未做 EN/移动端/门禁验证。

- 本轮实读 8 页：`tools/chemical/solution-concentration.html`、`tools/mining/convert-grade-ore.html`、`tools/hvac/cooling-load.html`、`tools/paper/roll-length.html`、`tools/fire/hydrant-pressure.html`、`tools/gas/load-1.html`、`tools/security/flood-level.html`、`tools/transport/convert-volume-weight.html`；新增 11 条（高 1 / 中 9 / 低 1）；未覆盖：chemical、mining、hvac、paper、fire、gas、security、transport 各目录的其余页面，以及 dyeing、leather、safety、nutrition、usedcar、wedding、restaurant、elderly、procurement、cleaning 等长尾目录本轮未读。

## 2026-11-04 续查（并行批 L）

> 范围：本轮阅读 8 页——`tools/dyeing/calc-dosage-2.html`（dyeing）、`tools/leather/convert-area-weight.html`（leather）、`tools/safety/accident-stats.html`（safety）、`tools/nutrition/calorie-deficit.html`（nutrition）、`tools/usedcar/car-residual.html`（usedcar）、`tools/wedding/wedding-banquet.html`（wedding）、`tools/restaurant/safety-stock.html`（restaurant）、`tools/elderly/fall-risk.html`（elderly）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

### 12-L4 nutrition/calorie-deficit：低体重女性「较快减脂」目标低于 BMR，无任何下限提示（中，疑似）
- 描述：`lose2` 直接取 TDEE 的 78%~85%，不与已算出的 BMR 比较，也不设常见 1200 千卡下限；低体重、久坐用户的目标摄入可低于 BMR，页面仍照常给出「建议日摄入」。
- 证据：`tools/nutrition/calorie-deficit.html:244-247`（区间），`:236-237`（BMR/TDEE），`:257-261`（输出无下限校验）
- 复现：女/30 岁/160 cm/45 kg/久坐 1.2/较快减脂 → BMR 1,139、TDEE 1,366.8，目标 `1066 ~ 1162` 千卡/天、建议 1,114 千卡，低于 BMR（且低于常见 1,200 千卡下限）。（node 复算）
- 影响：减脂方案可能推荐长期低于基础代谢的摄入，属健康风险提示缺失；属指南层面判断，标疑似待专业复核。
- 方案：输出前校验 `targetMin >= max(bmr, 1200)`（按性别/身高可配置），低于时显式警示并给出最低安全摄入；补低体重/久坐组合用例。

### 12-L6 wedding/wedding-banquet：主桌按 100% 到场再叠加备桌，双重预留且 `expectTables` 未使用（中，确认缺陷）
- 描述：`mainTables = ceil(guests/perTable)` 按满员计算，注释与页面又说「备桌按满员率 90% 估算实际到场，预留 10% 弹性」；`expectTables` 虽算出却从未参与结果，于是 90% 到场与 10% 弹性被重复计入，订桌数偏多。
- 证据：`tools/wedding/wedding-banquet.html:283-289`（`:283` 主桌、`:285-286` 期望人数/桌数、`:287-289` 备桌与合计），`:325-330` 同步复制
- 复现：120 位宾客、圆桌 10 人、备桌「少」→ 主桌 12 桌 + 备桌 1 = `合计 13 桌`；按页面自述 90% 到场 108 人只需 11 桌，加 1 备桌应为 12 桌（多订 1 桌）。（node 复算）
- 影响：按结果预订会多订 1 桌（10 人/桌），场地费按 1500–3000 元/桌多支出；`expectTables` 成为死变量，后续维护易误改。
- 方案：主桌数改用 `expectTables`，或明确「主桌按满员、备桌为额外」并删除 90% 文案；结果同时列出「按满员/按 90%」两套桌数；补 108/120/240 人与 8/10/12 人桌用例。

- 本轮实读 8 页：`tools/dyeing/calc-dosage-2.html`、`tools/leather/convert-area-weight.html`、`tools/safety/accident-stats.html`、`tools/nutrition/calorie-deficit.html`、`tools/usedcar/car-residual.html`、`tools/wedding/wedding-banquet.html`、`tools/restaurant/safety-stock.html`、`tools/elderly/fall-risk.html`；新增 9 条（高 2 / 中 6 / 低 1）；未覆盖：上述 8 个目录的其余页面（dyeing 13、leather 15、safety 15、nutrition 18、usedcar 12、wedding 9、restaurant 10、elderly 11），以及 procurement、cleaning 等长尾目录本轮未读；L4 的「低于 BMR/1200 千卡」属专业指南判断，标疑似待复核，其余均为源码与算术复算确认。

## 2026-11-04 续查（并行批 M）

> 范围：本轮阅读 8 页（chinese、fengshui、printing、hotel、sales、procurement、stats、quality 各 1 页）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

- 本轮实读 8 页：`tools/chinese/lunar-calendar.html`、`tools/fengshui/good-day-selector.html`、`tools/printing/convert-gsm.html`、`tools/hotel/occupancy-revpar.html`、`tools/sales/commission-calculator.html`、`tools/procurement/eoq.html`、`tools/stats/regression-analysis.html`、`tools/quality/calc-cpk.html`；新增 8 条（高 2 / 中 6 / 低 0）；未覆盖：上述 8 个目录的其余页面（chinese、fengshui、printing、hotel、sales、procurement、stats、quality），以及 audit、pet-training 等已有条目页面未重复；M1、M2 为源码 + node 复算确认，M3–M8 均为源码 + 算术复算确认。

## 2026-11-04 续查（并行批 N）

> 范围：本轮阅读 8 页——`tools/bridge/foundation-calc.html`（bridge）、`tools/chess/bridge-scoring.html`（chess）、`tools/aquaculture/hardness-water-quality.html`（aquaculture）、`tools/maritime/stowage-factor.html`（maritime）、`tools/tunnel/support-design.html`（tunnel）、`tools/glass/snell-refraction.html`（glass）、`tools/petrochem/api-gravity.html`（petrochem）、`tools/accessibility/braille-translator.html`（accessibility）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

- 本轮实读 8 页：`tools/bridge/foundation-calc.html`、`tools/chess/bridge-scoring.html`、`tools/aquaculture/hardness-water-quality.html`、`tools/maritime/stowage-factor.html`、`tools/tunnel/support-design.html`、`tools/glass/snell-refraction.html`、`tools/petrochem/api-gravity.html`、`tools/accessibility/braille-translator.html`；新增 12 条（高 1 / 中 8 / 低 3）；未覆盖：上述 8 个目录各仅读 1 页（每目录 6 页，共余 40 页未读），以及 audit、pet-training 等长尾目录；N1 为源码 + node 复算确认的承载力/桩数偏差，N5、N10、N11、N12 的“期望值”按页面自身公式与标准换算复算。

## 2026-11-04 续查（并行批 O）

> 范围：本轮阅读 8 页——`tools/beauty/skincare-routine.html`（beauty）、`tools/forensic-medicine/death-time-estimation.html`（forensic-medicine）、`tools/metallurgy/hardness-conversion.html`（metallurgy）、`tools/urology/psa-density.html`（urology）、`tools/ent/lund-mackay-score.html`（ent）、`tools/pulmonology/curb65.html`（pulmonology）、`tools/nephrology/ckd-staging.html`（nephrology）、`tools/acupuncture/acupoint-location.html`（acupuncture）。仅源码 + `node -e` 内存复算，未开浏览器、未做 EN/移动端/门禁验证。

**留存/优势（forensic-medicine/death-time-estimation）**
- 报告式输出：输入、两法结果、区间、角膜分期、警示合成一段可复制/打印的鉴定参考。
- 增加“角膜 vs 尸温差异”一致性徽标，冲突时自动提示复核。
- 提供教学预设与本地历史对比，便于课堂演示不同温度/体重曲线。

**留存/优势（metallurgy/hardness-conversion）**
- 批量换算：支持粘贴一列硬度值，一次输出 HRC/HBW/HV 与 σb，可导出 CSV。
- 结果卡显示“有效范围/超界警告”，避免端点钳制被当成真实值。
- 对照表支持打印/导出，便于车间张贴。

**留存/优势（urology/psa-density）**
- 输出结构化报告：PSA、体积、PSAD、年龄上限、穿刺指征逐条勾选，便于门诊记录。
- 本地保存 PSAD 历史并画趋势，复诊时直接看变化。
- 把 DRE/MRI 复选框状态回显到报告与复制文本中。

**留存/优势（ent/lund-mackay-score）**
- 一键复制“右侧 8 + 左侧 8 = 16/24 重度”的结构化报告。
- 增加快捷预设（全 0/全 2/上颌窦+筛窦），减少 12 次点击。
- 保存历次评分并画趋势，便于术后/用药前后对比。

**留存/优势（nephrology/ckd-staging）**
- 随访日程支持导出 `.ics` 或打印，直接进患者日程。
- 风险热图点击可定位当前 G/A 格，增强“我处在哪”的感知。
- 本地保存历次 eGFR/UACR 并画趋势，复诊时对比。

**留存/优势（acupuncture/acupoint-location）**
- 增加常用穴位预设（内关/足三里/三阴交），直接定位分段与目标寸数。
- 报告导出含分段、实测长度、1 寸折算、目标距离，便于教学与带教。
- 增加“cm→寸”反算输入与体表示意，补齐双向换算闭环。

- 本轮实读 8 页（8 个目录各 1 页）：`tools/beauty/skincare-routine.html`、`tools/forensic-medicine/death-time-estimation.html`、`tools/metallurgy/hardness-conversion.html`、`tools/urology/psa-density.html`、`tools/ent/lund-mackay-score.html`、`tools/pulmonology/curb65.html`、`tools/nephrology/ckd-staging.html`、`tools/acupuncture/acupoint-location.html`；新增 28 条（高 4 / 中 13 / 低 11）；未覆盖：上述 8 个目录的其余页面，以及 audit、pet-training 等长尾目录；未做浏览器、EN、移动端与门禁验证。N19、N23、N27、N33 的关键数值经 `node -e` 内存复算；N29 为静态加载时序推断（未开浏览器）；N19、N20、N27、N31、N33、N34、N38 的医学阈值仅判“实现/页面引据是否一致”，均需临床/法医/针灸复核。

## 2026-11-04 续查（并行批 P）

> 范围：本轮实读 8 页——`tools/dermatology/pasi-score.html`（dermatology）、`tools/urology/ipss-score.html`（urology）、`tools/obstetrics/bishop-score.html`（obstetrics）、`tools/hematology/dic-scoring.html`（hematology）、`tools/endocrinology/homa-ir.html`（endocrinology）、`tools/dentistry/caries-risk.html`（dentistry）、`tools/rehabilitation/fim-scale.html`（rehabilitation）、`tools/neurology/nihss.html`（neurology）。每页完整读 HTML（含内联 JS、公式框、deep-dive、FAQ）。仅源码 + `node -e` 内存复算，未开浏览器、未做 EN/移动端/门禁验证；医学量表阈值只判「实现与页面引据是否一致」，均需临床复核。

**留存/优势（dermatology/pasi-score）**
- 四区域色块分栏 + 区域权重标签，输入路径清晰。
- 提供轻/中/重预设与一键重置，便于教学演示。
- 结果支持复制、CSV 导出与历史趋势，可做疗效随访。

**留存/优势（urology/ipss-score）**
- 7 症状 + QoL 双区块，贴近临床问诊顺序。
- 分级（轻/中/重）与 QoL 建议联动，可直接给患者看。
- 历史与趋势可追踪治疗效果。

**留存/优势（obstetrics/bishop-score）**
- 五项评分逐项下拉，避免了口述换算。
- 结果同时给成熟度、成功率与下一步策略，可直接用于产房沟通。
- “宫颈成熟/未成熟”预设覆盖典型场景，便于教学。

**留存/优势（hematology/dic-scoring）**
- ISTH 四项目标表 + 明细逐条计分，透明度高。
- 基础疾病前提做成显式复选框，提醒评分适用条件。
- 预设覆盖显性/早期/非 DIC 对照，便于带教。

**留存/优势（rehabilitation/fim-scale）**
- 18 项按运动/认知分区，选项即分值，录入快。
- 运动/认知/总分/独立率四卡 + 单项条形图，结构清楚。
- 本地历史 + CSV 明细 + 门诊记录文本，适合康复随访。

**留存/优势（neurology/nihss）**
- 13 个条目按 NIHSS 顺序排列，选项即分值，床旁录入快。
- 总分 + 严重度 + 治疗建议 + 参考标尺四层解读，信息密度高。
- 预设、历史趋势、EMR 门诊记录文本，适合溶栓/取栓前后对比。

- 本轮实读 8 页（8 个目录各 1 页）：`tools/dermatology/pasi-score.html`、`tools/urology/ipss-score.html`、`tools/obstetrics/bishop-score.html`、`tools/hematology/dic-scoring.html`、`tools/endocrinology/homa-ir.html`、`tools/dentistry/caries-risk.html`、`tools/rehabilitation/fim-scale.html`、`tools/neurology/nihss.html`；新增 35 条（高 3 / 中 25 / 低 7）。未覆盖：上述 8 个目录的其余页面，以及 audit、pet-training 等长尾目录；未做浏览器、EN、移动端与门禁验证。N41、N42、N47、N48、N50、N52、N55、N59、N60、N65、N70、N73 的关键数值经 `node -e` 内存复算；N41、N50、N70 为可复现高优。医学阈值（PASI/Bishop/ISTH DIC/HOMA-IR/Cariogram/FIM/NIHSS）仅判「实现与页面引据是否一致」，均需临床复核。

**留存建议（pediatrics/ddst-screening）**
- 按能区分组的批量勾选/全选，减少 72–96 项逐项点击。
- 生成可打印/PDF 的筛查单（含月龄、题组、逐项结果、总体结论），便于门诊归档。
- 自动矫正胎龄并显示「实际/矫正月龄」双行，早产儿随访可直接复用。

**留存建议（fluid/bernoulli-pressure）**
- 增加 z1/z2 与「同一水平/有高差」开关，覆盖管道、机翼、文丘里三类场景。
- 预设改为真实工况（文丘里喉部、渐缩管、机翼上表面），并显示对应雷诺数与适用条件。
- 一键生成「P₁/v₁ → P₂/v₂/ΔP/动压」的对照表与 CSV，便于实验报告直接引用。

**留存建议（dynamics/rotational-kinetic-energy）**
- 增加 ω 单位切换（rad/s ↔ rpm ↔ 转/秒），避免用户把转速直接填进 rad/s。
- 增加常见刚体转动惯量预设（圆盘、圆环、细杆、球体），输入质量/半径自动算 I。
- 结果区同时给出 E、2E、L、转速与「飞轮储能时长」估算，并支持报告式复制。

### 12-N89 urology/stone-size-assessment：把输尿管排石率模型套到膀胱结石（5 mm→60%），适用性存疑（中，待验证）
- 问题：基础概率表标题明确「输尿管结石」（`:156`），但 `bladder` 系数取 1.0（`:267`），于是 5 mm 膀胱结石得到 60%「自发排石概率」；肾结石也用输尿管通过率×0.7。膀胱结石通常不会经尿道自行排出，模型语义不成立。
- 证据：`:156-162`、`:267-269`、`:284`
- 复现（node 复算）：loc=膀胱结石、size=5 → base 60×1.0=60%；loc=肾结石、size=5 → 60×0.7=42%（下段 75%）。期望膀胱结石提示「不适用排石概率，建议泌尿外科评估」。
- 影响：`tools/urology/stone-size-assessment.html` 膀胱结石患者被给出「60% 可自行排出」的错误预期。需泌尿外科复核。
- 方案：按部位限定模型适用范围：仅输尿管结石输出排石概率；肾/膀胱结石改为「仅作大小风险分层」，或单独建模型并注明证据等级。

**留存建议（urology/stone-size-assessment）**
- 结果区展示完整推导链「大小分档 base → 部位系数 → 上限 95%」，让医生可逐项核对。
- 增加「结石成分/CT 值/Hounsfield」可选输入，给出尿酸/胱氨酸等成分推测与溶石提示（需专业复核）。
- 导出结构化报告（大小、位置、概率、急诊指征、随访节点），并支持打印。

**留存建议（tcm-chemistry/metabolite-prediction）**
- 按「类别 → 化合物 → 关键产物」展开树状通路，支持一键展开/折叠，便于教学与论文附图。
- 增加批量模式：粘贴多个成分名，一次输出类别、主要 I/II 相反应与 MW 估算，导出 CSV。
- 生成可引用的报告片段（含类别、途径、反应酶、产物），并标注「经验规则，非 LC-MS 定性结论」。

**留存建议（nephrology/aki-kdigo）**
- 增加「变化时间窗（48h/7d）」与「已开始 RRT」两个字段，先判 AKI 再分期。
- 输出「肌酐比值/增量/尿量分期」三联推导，并给出血肌酐 mg/dL 与 μmol/L 双单位换算。
- 支持连续肌酐/尿量趋势录入，自动画 KDIGO 分期随时间变化，便于病程记录。

### 12-N103 ent/tonsil-grading：IV 度单独即判手术，与公式框「III–IV 度伴 OSAHS」不一致（低，待专业复核）
- 问题：`grade===4` 单独即 `surgIndication=true`，而表格/公式框写「III–IV 度伴 OSAHS 建议手术」；单纯 IV 度是否都需手术存疑。复制结果只复制分度的问题已在第1106批修复，本条仅剩手术指征阈值。
- 影响：可能对无 OSA/气道症状的 IV 度过度提示手术。需耳鼻喉科复核后再决定是否改为「建议评估 OSA/气道后再定」。

**留存建议（ent/tonsil-grading）**
- 输出「分度 + 症状矩阵 + 指征」一页式报告，支持打印/PDF 归档。
- 增加「对吻性扁桃体/气道梗阻」图示或口咽宽度百分比输入，减少肉眼分度主观性。
- 预设补 III 度+OSA、IV 度对吻、反复扁桃体炎三类，并支持一键复制结论。

**留存建议（astronomy/atmospheric-refraction）**
- 增加「真高度 ↔ 视高度」双向换算开关，并显示迭代收敛值与差值，避免口径混淆。
- 批量输入一列高度角，一次输出 R（角分/度/角秒）与修正后视高度，导出 CSV 供观测计划使用。
- 增加气压/温度/湿度修正选项（或至少给「标准大气」与「实测气象」两档提示），提升精密指向可用性。

### 承诺 vs 实际（Q 批专项）
| 页面 | 简介/FAQ/文案宣称 | 代码实际 | 证据 |
|---|---|---|---|
| `tools/pediatrics/ddst-screening.html` | 「125 个项目、约 20 分钟」「通过/未通过/拒绝」「早产儿按矫正胎龄」「任一项警示或 ≥2 项 caution 需转介」 | 题库仅 12 月龄组×2 项×4 能区=96 项；只有「通过/未通过」两个按钮（无拒绝）；`correctGA` 不参与任何计算；无 caution/警示概念 | `:130`、`:324`、`:336-337`、`:143`、`:373` |
| `tools/fluid/bernoulli-pressure.html` | 「输入流体速度、高度与压强」「p+½ρv²+ρgh=常量」 | 无高度字段，公式按「同一水平流线」只算 ½ρ(v₁²−v₂²) | `:13`、`:16`、`:122`、`:127-141`、`:120` |
| `tools/urology/stone-size-assessment.html` | 预设「肾结石 8mm 伴积水」；「基于权威医学标准」 | `renal` 实际是「孤立肾/肾功能不全」，直接触发急诊指征；部位系数 0.7/0.9/1.25/1.4/1.0 未在引据中逐项给出 | `:469`、`:145`、`:276-281`、`:127`、`:224-234` |
| `tools/tcm-chemistry/metabolite-prediction.html` | 「输入中药成分结构」「具体化合物（可选）/自动匹配」「给药途径」 | 无结构/SMILES 输入；`compound` 选中值从不读取；route 仅加提示框，topical 无分支 | `:10`、`:137-139`、`:337-344`、`:349-353` |
| `tools/nephrology/aki-kdigo.html` | 「输入…48 小时与 7 天变化」「需透析」「RRT 即归 3 期」 | UI 无时间窗、无 RRT 字段，calc 从不读取；26.5/1.5× 任意间隔生效 | `:10`、`:127-148`、`:165`、`:205`、`:271-273` |
| `tools/ent/tonsil-grading.html` | 「III–IV 度伴 OSA、吞咽障碍多建议手术」「预设」 | `s3` 吞咽困难不参与指征；预设函数空壳；`grade===4` 单独判手术 | `:217`、`:282`、`:286-292`、`:480-482` |
| `tools/astronomy/atmospheric-refraction.html` | 「Bennett 近似」「输入天体真高度角」「地平线约 34′」 | 系数实为 Saemundsson；公式参数为视高度；h=0 实算 28.98′ | `:122`、`:158`、`:129`、`:298`、`:210` |
| `tools/dynamics/rotational-kinetic-energy.html` | 公式与联动量说明 | 与实现一致，未见未兑现能力 | `:120`、`:211-218` |

说明：医疗相关结论（DDST 判定方向/早产儿矫正、结石排石模型与急诊指征、AKI 时间窗与 3 期阈值、扁桃体手术指征）仅判「实现与页面引据/文案是否一致」，均需临床/专业复核；本批 8 页未发现「限时、核验、ROI、难度」类宣称与代码不符的情况（这些模板化词条未出现在本批页面）。

### 覆盖
- 实读页数：8（`tools/pediatrics/ddst-screening.html`、`tools/fluid/bernoulli-pressure.html`、`tools/dynamics/rotational-kinetic-energy.html`、`tools/urology/stone-size-assessment.html`、`tools/tcm-chemistry/metabolite-prediction.html`、`tools/nephrology/aki-kdigo.html`、`tools/ent/tonsil-grading.html`、`tools/astronomy/atmospheric-refraction.html`）。
- 新增条数：32 条，编号 12-N76–12-N107（高 5 / 中 18 / 低 9）。
- 高优：N76、N77（DDST 判定方向与空报告）、N96、N97（AKI 时间窗与 3 期阈值）、N104（折射单位差 60 倍）。
- 未覆盖：8 个长尾目录的其余页面（如 pediatrics、fluid、dynamics、urology、tcm-chemistry、nephrology、ent、astronomy 目录内其他工具）；未做浏览器实机、英文态、移动端与门禁验证，也未运行 `_build.py`/git 写操作。
- 数值口径：N76–N78、N87–N90、N92–N93、N96–N97、N104–N106 的关键数值均用 `node -e` 内存复算；纯逻辑/文案项按源码逐行核对。医学类结论需专业复核。

## 2026-11-04 审计补充（R 批）

**留存建议（urology/bladder-capacity）**
- 支持连续多次排尿记录（排尿日记：时间、尿量、饮水量、残余尿），输出日均单次尿量与昼夜分布，而非只算单次总和。
- 记录残余尿测量方式（经腹超声/导尿）与测量时点，避免把不同方法的值直接相加比较。
- 保存患者档案（年龄、性别、诊断）并生成可打印的容量随访趋势表。

### 12-N111 tcm-chemistry/solubility-guide：溶解性等级「4 级说明/5 级 FAQ/药典 7 级」三套口径，且阈值把「略溶」并入「微溶」（中，待验证）
- 问题：页面说明只有易溶/溶解/微溶/难溶 4 级，并把「微溶」定为 ≥0.01 g/mL、难溶 <0.01（`:145-147`）；FAQ 却称「五级」（`:180`）；引据写「药典五级」（`:194`）。中国药典实际为极易溶解/易溶/溶解/略溶/微溶/极微溶解/几乎不溶或不溶，其中略溶 0.01–0.033 g/mL、微溶 0.002–0.01 g/mL，页面的「微溶 ≥0.01」把略溶档整体并入微溶。另 `tagClass` 把「溶解」与「易溶」都映射为 `tag-easy`（`:274-275`），视觉上无法区分。
- 证据：`tools/tcm-chemistry/solubility-guide.html:145-147`、`:180`、`:194`、`:274-275`
- 复现：按页面阈值，0.02 g/mL 应标「微溶」；按 ChP 应为「略溶」。表格中「溶解」与「易溶」同色，用户无法按颜色快速分级。
- 影响：`tools/tcm-chemistry/solubility-guide.html` 提取溶剂选择所依据的溶解等级与药典口径不符。等级划分与阈值需中药化学/药典专业复核。
- 方案：统一采用 ChP 七级（或明确声明只取 4 档并给出合并规则）；为「溶解」单独配色；在说明中标明数据为整理值、以实测/药典为准。

**留存建议（tcm-chemistry/solubility-guide）**
- 增加溶剂极性/logP 对照表，并支持按「溶剂 + 等级」反向查询（如「氯仿 易溶」列出成分）。
- 点选某成分后给出提取工艺建议（水提/醇提/酸碱转溶、温度与料液比），并注明为经验规则。
- 支持勾选多行导出为结构化 CSV（含分子量、来源、各溶剂等级、备注、数据出处）。

### 12-N113 nephrology/edema-grading：4+ 深度门槛表格 ≥8 mm 与公式/代码 >6 mm 不一致（中，待专业复核）
- 问题：深度分档为 ≤2/≤4/≤6/>6，表格写「4+ ≥8 mm」，公式写「4+ ≥6 mm」，6–8 mm 区间口径冲突。输入守卫（空值/负值拦截）经源码核对已生效，不属于本条剩余问题。
- 影响：`tools/nephrology/edema-grading.html` 6–8 mm 区间文字标准与计算分级不一致，需医学专业复核后再定门槛。
- 方案：明确采用 ≥6 或 ≥8 单一口径并同步公式框、表格与代码；不得自行猜测医学阈值。

**留存建议（nephrology/edema-grading）**
- 按日期保存同部位（踝/胫前/骶尾）的深度、恢复时间、体重与利尿剂剂量，生成趋势图与「本次 vs 上次」对比。
- 增加水肿范围/对称性的结构化记录，并导出可贴入病程记录的文本（含检查方法、按压时长）。
- 提供治疗反应小结（体重变化、尿量、利尿剂），帮助随访判断容量状态。

**留存建议（ent/tdi-score）**
- 按年龄/性别显示本地常模参考区间（页面已提示年龄影响，但未落为可对比的数值）。
- 记录嗅棒套件版本（如 Sniffin' Sticks 12/16 项、中文版卡片）与测试环境，便于纵向随访。
- 保存多次 TDI（含 T/D/I 分项）并生成趋势图，支持打印/复制到嗅觉随访记录。

**留存建议（pediatrics/neonatal-jaundice）**
- 在同一图上绘制 P40/P75/P95、光疗与换血阈值及当前点，直观显示「分区」与「治疗线」的距离。
- 提供 mg/dL ↔ µmol/L 双向输入（FAQ 已给 17.1 换算，但界面无换算入口），减少手算错误。
- 保存一次评估的完整参数与风险因素，生成可复制/打印的随访记录（含复测时间建议）。

**留存建议（dentistry/periodontal-pocket）**
- 按牙位/位点组织记录，自动生成牙周袋深度图表（每颗牙 6 点），支持全口一览。
- 增加 BOP、松动度、根分叉受累与影像骨丧失字段，向 2017 分期/分级靠拢（需专业复核）。
- 保存多次探诊结果并对比 CAL/PD 变化，导出可打印的牙周检查表。

**留存建议（rehabilitation/physiotherapy-dose）**
- 增加禁忌症/慎用清单（妊娠、心脏起搏器、恶性肿瘤、感觉障碍、急性感染、金属植入等）并在结果区强提示。
- 保存常用参数组合（设备、频率、ERA、强度、时间）为一键方案，便于同科室复用。
- 治疗记录保存完整参数而非仅处方文本，支持按患者/部位导出疗程表与剂量累计。

**留存建议（endocrinology/pcos-diagnosis）**
- 增加年龄、BMI/腰围、AMH、OGTT/HOMA-IR、血脂与血压字段，把「代谢风险分层」落为可计算的分层结果而非固定文案。
- 记录检验单位与实验室参考范围（睾酮、17-OHP、TSH、PRL），避免单位混用；支持 ng/dL ↔ nmol/L 切换。
- 保存多次评估（症状、激素、超声、代谢指标）并导出表型随访表，按 A–D 型给出个体化复查间隔。

### 承诺 vs 实际（R 批专项）
| 页面 | 简介/公式/文案宣称 | 代码实际 | 证据 |
|---|---|---|---|
| `tools/urology/bladder-capacity.html` | 「比值 <0.7 偏小、>1.5 偏大」；FAQ「<50% 显著下降」 | 代码用 0.7/1.5；0+0 仍判偏小与排空障碍 | `:128`、`:199`、`:261-262`、`:249-250` |
| `tools/tcm-chemistry/solubility-guide.html` | 「易溶/溶解/微溶/难溶」四级；FAQ「五级」 | 四级说明 + 五级 FAQ + 药典七级；导出只按名称筛选 | `:145-147`、`:180`、`:194`、`:296-327` |
| `tools/nephrology/edema-grading.html` | 表格「4+ ≥8 mm」；公式「4+ ≥6 mm」；恢复时间参与分级 | 原审计记录：代码 >6 mm 即 4+；refBar 分带错位。恢复时间不参与分级已于 2026-11-06 复核修复，见 12-N112；其他问题未在本次复核 | `:121`、`:173`、`:298-310`、`:368` |
| `tools/ent/tdi-score.html` | 每项 0–16；引据「>30 正常」；T 提示 1–16 | 代码截断 0–16 但复制不截断；分级 >30.5；T 输入 min=1 | `:128`、`:230`、`:235`、`:132`、`:257-293` |
| `tools/pediatrics/neonatal-jaundice.html` | 引用 AAP 2022；48h 光疗 11–13；示例 40–75 分位/阈值 12 | 引据表写 AAP 2004；代码 48h 阈值 15；默认 14 判高危险区却「暂无需光疗」 | `:179`、`:183-186`、`:247`、`:298-304`、`:379-385` |
| `tools/dentistry/periodontal-pocket.html` | 引据「2017 WWP staging」；表格/FAQ 中度 4–5、重度 ≥6 | 代码 ≤5 中度/>5 重度；引据写重度 ≥5；CAL 可为负 | `:237`、`:169-170`、`:212`、`:266-269`、`:264` |
| `tools/rehabilitation/physiotherapy-dose.html` | 强度 0.3「亚急性」、0.5「慢性」；每 cm² 约 1 分钟 | 0.3→急性、0.5→亚急性；小面积强制 3 分钟 | `:149-151`、`:374`、`:247`、`:365-371` |
| `tools/endocrinology/pcos-diagnosis.html` | 睾酮 >60 nmol/L；PCOM 卵泡 ≥20（2023） | 代码按 >60 ng/dL；引据/示例仍 ≥12；NIH/AES 未排除直接判不符合 | `:134`、`:165`、`:340`、`:274`、`:246`、`:370-382` |

说明：以上医疗相关结论（水肿分档、TDI 常模、新生儿黄疸阈值、牙周 CAL 分期、PCOS 高雄阈值/PCOM 版本）仅判「实现与页面引据/文案是否一致」，均需临床/专业复核；N111 的溶解性分级需药典复核。本批未做浏览器、英文态、移动端、线上或门禁验证。

### 覆盖
- 实读页数：8（`tools/urology/bladder-capacity.html`、`tools/tcm-chemistry/solubility-guide.html`、`tools/nephrology/edema-grading.html`、`tools/ent/tdi-score.html`、`tools/pediatrics/neonatal-jaundice.html`、`tools/dentistry/periodontal-pocket.html`、`tools/rehabilitation/physiotherapy-dose.html`、`tools/endocrinology/pcos-diagnosis.html`）。
- 新增条数：22 条，编号 12-N108–12-N129（高 4 / 中 16 / 低 2），另附 8 组留存建议与 1 节「承诺 vs 实际」。
- 高优：N112（水肿恢复时间不参与分级）、N118（新生儿默认结果自相矛盾）、N119（光疗阈值表与代码差 2–3 mg/dL）、N127（PCOS 睾酮单位差约 29 倍）。
- 未覆盖：8 个长尾目录的其余页面；未做浏览器实机、英文态、移动端与门禁验证，也未运行 `_build.py`/git 写操作。
- 数值口径：N108、N112–N120、N124–N129 的关键数值（比值、阈值差、能量、TDI 总分、单位换算、表型计数）均用 `node -e` 内存复算；纯逻辑/文案项按源码逐行核对。

**留存建议（food/food-calculator）**
- 六个页签各配独立公式与算例（烘焙/热量/咖啡/盐度/辣度/保质期），当前公式框只讲保质期（`:170`）。
- 咖啡模块按冲煮方式维护「粉液比、注水量、萃取时间、液量」参数表，避免意式与手冲共用粉水比。
- 建立食物「储藏条件适用性」表，明确鸡蛋/酱油等不建议冷冻，并给冷藏替代值。

**留存建议（engineering/heat-transfer）**
- 四种模式共用统一的「正数/有限值」校验与错误高亮，禁止用 `||0` 掩盖空值。
- 辐射模块补充 ε 范围、开尔文温度下限与净辐射方向说明。
- 复合热阻在 R 非有限时给出「热阻无穷大/无法传热」的显式结论，而非「—」。

**留存建议（seismology/assessor-31）**
- 建筑总数与五类破坏栋数做一致性校验（合计≤总数），并拒绝 0/负值。
- 把已算出的 `displacedPop`、倒塌率、严重破坏率一并输出，形成完整的损失估算表。
- 提供可调阈值/权重或明确声明固定口径，避免「可微调」的空承诺。

**留存建议（mining/excavation-volume）**
- 明确「上口宽」与「边坡系数」谁是输入、谁是派生，杜绝字段失效。
- 统一 box/pool 的边坡公式并同步公式框、深度解析与结果标签。
- 预设按工程场景维护合理松散系数区间（土 1.2–1.3、岩 1.5–2.0），不跨出输入范围。

**留存建议（tcm-chemistry/hplc-optimization）**
- 梯度/等度结果分区展示，并在梯度模式下移除「在等度洗脱模式下」的固定结论文案。
- 增加参数合理性校验（tR>t0、W>0、流速/柱长>0），错误时阻止结果输出。
- 重写简介为色谱方法开发定位，删除医疗/临床话术。

**留存建议（property/rater-performance）**
- 深度解析算例改为工具真实六维，并提供默认参数可复算的分数。
- 权重合计显示归一前后的两种口径，避免 >100% 的误读。
- 等级说明与代码五级同源，附每级对应的处置动作。

**留存建议（food-processing/sterilization-f-value）**
- 区分 F(Tref) 与 F₀，Tref≠121.1℃ 时禁止用 F₀≥3 判据并显式提示。
- 模式切换即重算/清空结果，三个模式各自保留输入与结果状态。
- 重写工具简介为工业热杀菌定位，补充工艺验证与法规免责声明。

### 承诺 vs 实际（S 批专项）
| 页面 | 简介/公式/文案宣称 | 代码实际 | 证据 |
|---|---|---|---|
| `tools/food/food-calculator.html` | 「工作原理」公式框应覆盖 6 个页签 | 公式框只写保质期推算，烘焙/热量/咖啡/盐度/辣度均无公式说明 | `:170`、`:176-181` |
| `tools/printing/estimate-ink.html` | 公式框 ÷1000；校验覆盖率 0–100% | 信息框 ÷100000；CMYK 覆盖率无任何校验 | `:118`、`:177`、`:301-322` |
| `tools/engineering/heat-transfer.html` | 公式框列「核心计算公式」 | 仅列辐射/复合热阻片段，导热/对流公式未列入 | `:166`、`:317-351` |
| `tools/seismology/assessor-31.html` | 需安置人口粗估；阈值可在工具内按地方标准微调 | `displacedPop` 算了但未渲染；无阈值/权重控件 | `:128`、`:283-290`、`:338` |
| `tools/mining/excavation-volume.html` | 方坑含 0.6×深 边坡；基坑模式含 0.6·深 | box 模式为纯 `L×W×D`，仅 pool 用 0.6 边坡 | `:162`、`:223`、`:320-326`、`:356` |
| `tools/tcm-chemistry/hplc-optimization.html` | 医疗专业工具、临床参数、权威医学标准 | 色谱保留时间/柱效/分离度计算，无临床模型 | `:459`、`:463`、`:469` |
| `tools/property/rater-performance.html` | 算例五维（含成本控制）；<70 待改进 | 工具六维无成本控制；五级含 D 60–69、E<60 | `:132-152`、`:203`、`:237-241`、`:312-313` |
| `tools/food-processing/sterilization-f-value.html` | 美食烹饪/食材配比；F₀≥3（121.1℃ 基准） | 工业热杀菌；任意 Tref 都套 F₀≥3 判定 | `:383-395`、`:130`、`:289` |

### 覆盖
- 实读页数：8（`tools/food/food-calculator.html`、`tools/printing/estimate-ink.html`、`tools/engineering/heat-transfer.html`、`tools/seismology/assessor-31.html`、`tools/mining/excavation-volume.html`、`tools/tcm-chemistry/hplc-optimization.html`、`tools/property/rater-performance.html`、`tools/food-processing/sterilization-f-value.html`），覆盖 8 个不同目录（页数 24/7/11/5/12/22/20/20，均 <25），8 页均未出现在既有 plan 文档中。
- 新增条数：24 条，编号 12-N130–12-N153（高 7 / 中 12 / 低 5），另附 8 组留存建议与 1 节「承诺 vs 实际」。
- 高优：N133（油墨公式除数差 100 倍）、N142（上口宽字段失效）、N139（建筑总数 0 判特大震害）、N151（任意 Tref 套 F₀≥3）、N130（法压壶 240 分钟）、N131（意式注水 270 ml）、N145（梯度 tR 小于死时间）。
- 未覆盖：8 个长尾目录的其余页面；未做浏览器实机、英文态、移动端、线上或门禁验证，也未运行 `_build.py`、git 或任何构建/写操作。
- 数值口径：N130–N135、N139–N145、N147、N151 的关键数值（秒/分换算、100 倍除数、负墨量、负传热、零除、边坡体积、梯度保留时间、F₀ 换算）均用 `node -e` 内存复算；纯逻辑/文案项按源码逐行核对。
- 专业复核：本批无医疗结论；地震震害分级、土方边坡、热力杀菌 F₀、传热与色谱参数均属工程/食品工艺估算，正式使用需由相应专业复核。

## T 批长尾行业覆盖（2026-11-04）

### 覆盖
- 本轮审计 10 页：`tools/metallurgy/steel-profile-weight.html`、`tools/obstetrics/fetal-weight-hadlock.html`、`tools/travel/road-trip-gas-cost.html`、`tools/sales/stacked-discount.html`、`tools/printing/sheet-calc.html`、`tools/welding/weld-strength.html`、`tools/fluid/poiseuille-flow.html`、`tools/process/sigma-level.html`、`tools/hvac/duct-calculator.html`、`tools/gardening/compost-calculator.html`；均为上文未出现的页面。
- 新增 13 条（高 7 / 中 6），编号 12-N154–12-N166；假工具候选 0 页。
- 高优：N154（圆管按实心圆钢、壁厚死输入）、N156（缺 FL 落单腹围 340 g）、N157（单 FL 多乘 10）、N158（宫高腹围 0.3 系数 912 g）、N159（电动车按油耗计价）、N160（折扣 8/80 量纲冲突）、N161（优惠百分比当折数）。
- 无高优页面：`tools/gardening/compost-calculator.html`（默认 4 kg 混合 C:N 26.7、理想区间判定与加料反算公式均复算一致，未发现量纲/阈值缺陷）。
- 未做浏览器实机、门禁、`_build.py`、git 与线上验证；数值均用 `node` 在 `/tmp` 内存复算，页面行号按当前工作区源码核对。

## T 批 长尾行业覆盖（2026-11-04）

> 本批只读审计 8 页（每目录 1 页），均未出现在既有 plan 条目中（已 Grep 确认 slug 零命中）。编号续接 12-N166。

### 覆盖清单（T 批 长尾行业，2026-11-04）
- 审计页数：8（`tools/metallurgy/alloy-ratio.html`、`tools/leather/calc-dosage-4.html`、`tools/gardening/soil-ph.html`、`tools/chemical/reaction-yield.html`、`tools/nutrition/generator-glucose-load.html`、`tools/process/cpk-with-shift.html`、`tools/transport/calculator-calc-fuel.html`、`tools/usedcar/usedcar-valuation.html`），8 个不同目录各 1 页，均为既有 plan 未覆盖页（Grep 上述 8 个 slug 在 `_others.md` 零命中）。
- 新增条数：15 条，编号 12-N167–12-N181（高 5 / 中 10）。
- 高优：N167（合金配料忽略自身质量，18% Cr 实得 13.68%）、N169（脱毛默认浓度 60% → 120 kg，20 倍过量）、N171（空 pH 被当 0，输出强酸结论）、N174（放大把小试实际产量当理论量，预计产量低 1/y1）、N177（每份克重当碳水，白米饭 GL 124.5）。
- 中优集中模式：编辑参数不重算（N168）、非法输入仅红框仍出数（N170/N180/N181）、同屏两个差值口径或阈值口径（N172/N178）、承诺的区间/差值未实现（N173/N179）、模式切换残留旧结果（N176）、>100% 仍评最优（N175）。
- 无缺陷页：`tools/transport/calculator-calc-fuel.html`（里程/油耗/油价三维均参与计算，`fuel=d/100×c`、`cost=fuel×p`、`perKm=cost/d`、往返×2 与 60 L 占比均复算一致；仅 `Math.min(100,…)` 进度条封顶而文案可显示 >100%，属展示层夸张，未列条）。
- 局限：仅源码逐行核对 + `node` 在 `/tmp` 内存复算关键数值；**未开浏览器、未跑 `run_gates.py`/`_test_static.py`、未跑 `_build.py`、未做 git 或线上验证**，英文态/移动端/繁体页均未实测。专业复核：冶金配料、制革硫化钠投料、土壤改良用量、化工放大与过程能力指数均需现场/专业确认，本批结论不构成工艺指令。

## U 批 · 长尾 8 目录（2026-11-04）

### 12-N184 leather/colorfast：累积辐照量直接映射等级，照射越久评级越高（方向倒置）（高，确认缺陷）
- 问题：`energy=h×3600×ir/1000`（`:207`）后按 `energy` 单调递增给 1-8 级（`:209-216`），即曝晒剂量越大等级越高、文案越「几乎不褪色」；但输入含义是「照射时间/辐照度」（`:133`），真实耐光测试中照射越久应褪色越严重。页面自己的算例也矛盾：2 h→432 kJ「4 级（轻度褪色）」，5 h→1080 kJ 反而「5 级（良好）」。
- 证据：`tools/leather/colorfast.html:207-216`、`:133`、`:367`、`:371`（FAQ 又称「等级越高说明在越高辐照量下仍稳定」）
- 复现（node 复算）：默认 20 h × 42 W/m² → 3024 kJ/m² → **7 级「优秀，几乎不褪色」**；改为 1 h × 42 → 151.2 kJ/m² → **3 级「一般，中等褪色」**；30 h × 50 → 5400 kJ/m² → **8 级「极佳」**。即「照得越久越好」。
- 影响：`tools/leather/colorfast.html` 用户做加速老化时，把长时曝晒当成高耐光性，得到与事实相反的结论；该「等级」并不能由曝晒量单独推出（还需褪色观察/灰卡或蓝标比对）。
- 方案：输入改为「达到褪色阈值的累积辐照量」并在标题/标签/说明中明示；或增加「褪色程度（灰卡级/蓝标级）」输入后再评级；至少删除「照射时间越长等级越高」的单调映射。
- 严重度：高；是否假工具：否（计算本身成立，评级模型方向倒置）

### 覆盖清单（U 批 长尾行业，2026-11-04）
- 审计页数：11（`tools/metallurgy/steel-calc-1.html`、`tools/metallurgy/energy-1.html`、`tools/leather/yield-rate-1.html`、`tools/leather/colorfast.html`、`tools/gardening/plant-calendar.html`、`tools/gardening/watering-schedule.html`、`tools/chemical/convert-density-crude.html`、`tools/chemical/calc-pipeline-pressure-drop.html`、`tools/process/cp-index.html`、`tools/process/dpmo-calc.html`、`tools/usedcar/car-purchase-cost.html`），覆盖 6 个目录。
- 新增条数：17 条，编号 12-N182–12-N198（高 2 / 中 15）。
- 高优：N182（种植日历月份视图漏 2-3 倍条目且 1/2 月串月）、N184（耐光色牢度按曝晒量递增评级，方向倒置）。
- 中优集中模式：字符串区间不展开（N182/N183）、非法输入仅红框或兜底仍出数（N186/N189/N191/N193/N194）、口径/单位/评级模型问题（N184/N197）、承诺未实现（N188/N190/N192）。
- 无缺陷页：`tools/metallurgy/energy-1.html` 的折标煤/CO₂/GJ 四式复算与默认值一致（8.805 tce / 23.42 t / 258.0 GJ / 8805.0 kgce），仅标题口径未落地（N190）；`tools/process/cp-index.html` 默认 Cp=1.667 正确（问题仅在校验缺失）；`tools/chemical/convert-density-crude.html` 默认 API 35↔SG 0.8498↔849.8 kg/m³ 换算正确（问题仅在非正输入与高亮）。
- 局限：仅逐行读源码 + `node` 在 `/tmp` 复算，**未开浏览器、未跑 `_build.py`/`run_gates.py`/`_test_static.py`、未做 git 或线上验证**；英文态/繁体页/移动端未实测。专业复核：焊缝强度（GB 50017）、耐光色牢度评级、原油 API 分类与购车税口径均需专业/法务确认，本批结论不构成工艺或报价指令。

## V 批 · 冶金/皮革/园艺（2026-11-04）

### 覆盖清单（V 批 长尾行业，2026-11-04）
- 审计页数：8（`tools/metallurgy/analysis-price-1.html`、`decarburization.html`、`convert-hardness.html`、`solidification-time.html`、`tools/leather/strength-8.html`、`area-20.html`、`tools/gardening/balcony-sunlight.html`、`pot-capacity.html`），覆盖 3 个目录。
- 新增条数：13 条，编号 12-N199–12-N211（高 3 / 中 10）。
- 高优：N200（`erfInv` /π 误写致脱碳层低估 4.6 倍）、N201（HV→HBW 用 ÷0.9544 与同页公式相反，三路径互差 10%）、N206（阳台三个下拉原有选项缺失，已于早期 fake-tools Batch 6-1 补齐，2026-11-16 第 678 批复核销账）。
- 中优集中模式：非法/空值兜底仍出数（N202；N199 已于 2026-11-16 第 675 批修复、N208 已于第 679 批修复、N211 已于第 680 批修复）、同页公式与代码/文案两套口径（N204 已于第 677 批修复、N209 已于第 679 批修复、N210 已于第 680 批修复）、承诺未实现（N203 已于第 676 批修复、N207 已于第 679 批补齐圆台）、参数联动失效（N205）。
- 无缺陷页：`tools/leather/strength-8.html` 的抗张（负荷/宽×厚，240N/10×1.5→16.00 MPa）与撕裂（45N/1.5→30.00 N/mm）复算与页面公式一致，仅空值兜底为 0 并加红框（同类问题未单列）；`tools/metallurgy/analysis-price-1.html` 的总体标准差 25.2042、CV 50.92%、区间 [24.30,74.70] 与算例一致，输入解析问题（N199）已修；`tools/gardening/balcony-sunlight.html` 的查表/楼层修正/分级逻辑本身正确（南向春 6.0、北向高冬 0.5），控件缺失问题（N206）已复核修复。
- 模板预设残留（已修）：`analysis-price-1` 空预设已补三组行情序列；`convert-hardness` 的 HRC 15 改为 HRC 20/30/55（均在 20–67）；`decarburization` 的 1650/2200℃ 改为 1300/1400℃（在 500–1400 内）。均于 2026-11-16 第 676 批处理。
- 局限：初审计仅逐行读源码 + `node` 在 `/tmp` 复算；N199 已于 2026-11-16 第 675 批修复（千分位识别、严格数字校验、拒绝项列出、价格 >0）、N203 与三处预设残留已于第 676 批修复（深解重写为三标尺拟合与实际适用范围、预设改有效值）、N204 已于第 677 批修复（深解系数表统一为 min/cm² 的 2.0/2.5/1.8 与 0.8/1.0/0.6）、N207–N209 已于第 679 批修复（新增圆台盆与上下口输入、排水层按盆高分档、盆高过小停算）、N210/N211 已于第 680 批修复（公式框统一 ft² 分级并改为实际综合定级口径、空/负输入停算），并通过 `_build.py` 与 `_test_static.py`。英文态/繁体页/移动端仍未实测；专业复核：硬度换算（ASTM E140）、脱碳扩散模型与 Chvorinov 系数量纲均需材料专业确认，本批结论不构成工艺指令。

## W 批 · 化工/营养/工艺/运输（2026-11-04）

### 覆盖清单（W 批 化工/营养/工艺/运输，2026-11-04）
- 审计页数：8（`tools/chemical/convert-capacity-tank.html`、`mixture-ratio.html`、`tools/nutrition/food-calorie-lookup.html`、`generator-nutrition-label.html`、`tools/process/tolerance-worst-case.html`、`tolerance-rss.html`、`tools/transport/convert-fuel-oil.html`、`calculator-calc-tire.html`），覆盖 4 个目录。
- 新增条数：10 条，编号 12-N212–12-N221（高 3 / 中 7）。
- 高优：N217（燃油同单位换算输出倒数，已于第 683 批核验并新增 UK 用例）。N212 已于 2026-11-16 第 682 批修复（补卧式圆柱弓形面积、容积→液位二分反算、满罐容积与充装率）；N213/N214 已于第 681 批修复；N215/N216 已于第 683 批核验销账（现为逐项输入 + Atwater 17/37/17/8 kJ + NRV% 表格）；N218 已于第 683 批补「加仑制式 US/UK」与 282.4809 常数。
- 中优集中模式：空值/负值兜底仍出数（N221，已于 2026-11-16 第 685 批补负公差拦截并销账）；N214 已于第 681 批修复，N216/N218 已于第 683 批修复，N219/N220 已于第 684 批修复（导出改指向可见速查表、深解数值与表内数据对齐）。
- 无缺陷页：`tools/transport/calculator-calc-tire.html` 复算 225/45R17→634.3 mm、225/50R17→656.8 mm（+22.5 mm / +3.55%）、235/40R18→645.2 mm（+1.72%），外径差/间隙变化/表显 100 实际车速与公式一致，仅规格串正则不接受带载重/速度级别（如 225/45R17 91W），页面已明示该格式限制。
- 未单列：`convert-capacity-tank.html` 公式行重复两遍已于第 682 批去重并按新能力重写；`mixture-ratio.html` 的 formula-desc 模板占位串已于第 681 批改为酒精降度公式说明；`convert-fuel-oil.html` 的多余 `</div>` 已于第 683 批修正（「到」下拉与结果区回到卡片内）；`food-calorie-lookup.html` 的 `<table>` 内嵌 `<div>` 已于第 684 批移出（导出按钮与历史容器回到表格之后，不再触发 foster-parent）。
- 局限：仅逐行读源码 + `node` 在 `/tmp` 复算，**未开浏览器、未跑 `_build.py`/`run_gates.py`/`_test_static.py`、未做 git 或线上验证**；英文态/繁体页/移动端未实测。营养条目（N215/N216/N220）的营养素值、NRV 与能量口径**需临床复核**，本批结论不构成膳食或标签合规指令。

## X 批 · 冶金/皮革/园艺/化工（2026-11-04）

### 覆盖清单（X 批 冶金/皮革/园艺/化工，2026-11-04）
- 审计页数：8（`tools/metallurgy/analysis-grade.html`、`stats-10.html`、`analysis-34.html`、`tools/leather/xueyunhoudukongzhi.html`、`assessor-21.html`、`tools/gardening/pruning-calendar.html`、`lawn-mowing.html`、`tools/chemical/checker-15.html`），覆盖 4 个目录。
- 新增条数：8 条，编号 12-N222–12-N229（高 2 / 中 6）；假工具 1（N222）；安全条目 0。
- 高优：N222（评分/偏差为常量、目标厚度不参与，等同无评估能力）、N223（公示的综合得分与 A/B/C 分级从未实现，实际规则另成一套）。
- 中优集中模式：输入留空仍出判定（N224）、导出指向历史/搜索表（N225）、推荐档位与自身说明相反（N226）、文案区间与数据表双口径（N227）、算例把综合指标当分项指标（N228）、算例档位差一档（N229）。
- 无缺陷页：`tools/metallurgy/analysis-grade.html` 复算 A=0.85、B=22、T=0.09、Q=1000 → γ=3.469%、精矿 34.69 t、ε=89.78%、流失 10.22%、尾矿金属 0.869 t（回收率+流失率=100%），与 `:220-232` 一致；deep-dive 算例 100 t 铜、200 t 精矿 20% → 尾矿品位 0.612%、回收率 40% 亦自洽。`tools/metallurgy/analysis-34.html` 除 N224 外，RSD 3.16%（n−1）/2.83%（n）、加标 95%（0.69−0.50）/0.20 均与 `:238-246` 复算一致。
- 未单列（低）：`tools/chemical/checker-15.html:120` 公式框句子截断（「60-74% 合格，」后缺「<60% 不合格」）；`checker-15`、`assessor-21` 的 h2/副标题仍是占位串「Checker 15」「Assessor 21」，`analysis-34`/`stats-10`/`analysis-grade` 副标题在英文态为「Analysis 34」「Stats 10 - online utility on ToolBox.」「Analysis Grade」；`pruning-calendar.html:288` 栀子花 `icon:' white'`（带前导空格的非 emoji，渲染成「 white 栀子花」）；多页 TBKIT 注入的 `P` 映射漏掉 `*Diff` 容器，切换页签时差分块常驻可见。
- 局限：仅逐行读源码 + `node`/手算在本地复算，**未开浏览器、未跑 `_build.py`/`run_gates.py`/`_test_static.py`、未做 git 或线上验证**；英文态/繁体页/移动端未实测。园艺与皮革的档位判定属经验规则，N226/N227 的「正确档位」需按所在气候带与草种/品种复核。

## Y 批 · 长尾·汽车/通用（2026-11-04）

**逐页结论**
- `tools/automotive/shipping-cost-compare.html`：首重 + 续重与保价公式正确；自定义首/续重只改「经济快递」一行，且表格不标注自定义。
- `tools/automotive/fuel-economy.html`：百公里油耗、单次油费、续航、月费计算正确；「油箱容量」为死输入，承诺的碳排放没有输出。
- `tools/automotive/parking-fee-calculator.html`：首段 + 进一法 + 封顶公式正确；跨天数与免费时长的口径和自身说明冲突。
- `tools/automotive/driver-license-validator.html`：只做正则白名单，无校验位与发证年份；`<input>` 未闭合吞掉导出按钮；输入直入 `innerHTML`。
- `tools/automotive/voltage-2.html`：三条公式与公式框一致；24V 预设仍套 12V SOC 阈值，末端电压未采用实际发电电压。

| 页面 | 问题（含 tools/automotive/<slug>.html:NN） | 编号 |
|---|---|---|
| shipping-cost-compare | 自定义首/续重只在 `i===0`（经济快递）生效（`:367-368`），但输入标签未说明作用渠道（`:201-202`），表格也不渲染 `ref`（`:371`）；用户的自报价被当成「经济快递」报价参与比价，最低价归属会误读。 | 12-N232 |
| parking-fee-calculator | 跨天与停放时长重复计入：`total=cappedDay*d`（`:339`）把已按 `parkMin` 算出的单日费再乘天数；若 `parkMin=4320`（3 天全程）、`cap=0`，会按 3×720=2160 元收（应按 720）；机场预设又用 `parkMin=480 + days=3`（`:465`），两种语义混用；另 `days=0.5` 被 `Math.floor` 成 0（`:338`）直接 0 元。 | 12-N238 |
| parking-fee-calculator | 免费时长口径与自身 FAQ 冲突：代码 `pay=max(0, parkMin-freeMin)` 从免费结束起算（`:330`），FAQ 写「超时按规则从进场起算，非从免费结束起算」（`:82`、`:243`），引据表写「超时后按全额或分段计取」（`:271`）；例 free 30、park 100、首 60 分钟 5 元、续 30 分钟 5 元 → 页面 10 元，按 FAQ 15 元。 | 12-N239 |
| driver-license-validator | 名不副实：描述/简介/引据承诺「校验位、发证年份、地区」（`:10`、`:154-156`、`:220`），实现只有 16 条正则首匹配（`:237-259`，筛选在 `:267`），无加权模 11 或年份解析；公式框自己也写「无校验位算法」（`:153`）。 | 12-N242 |
| voltage-2 | 末端电压基准错：`endV=volt-dU`（`:331`）用「系统标称 12V」，未用实际发电电压 14.4V；默认 10A/5m/2.5mm²/铜算得 11.30V（`:338`），实际应为 14.4−0.70=13.70V，偏低 2.4V，deep-dive 也沿用 11.30V（`:220`）。 | 12-N243 |

**统计**
- 审计页数：8（全部为 `tools/automotive/` 下指定页面）。
- 原 15 条（12-N230–12-N245）：第 1060 批清 7 条（N230/N231/N233/N234/N235/N240/N245），第 1061 批清 2 条（N236 油箱容量死输入、N237 碳排放承诺未实现），第 1062 批清 1 条（N244 24V SOC 按 2×12V 单块折算），余 5 条。
- 剩余 5 条：N232（shipping 自定义渠道）、N238/N239（parking 跨天/免费口径）、N242（driver 名不副实）、N243（voltage 末端电压基准）。N232/N238/N239 属设计/业务口径需明确裁断；N242 涉 SEO description 多源同步（7+ 文件）、措辞层面非功能错误，暂缓；N243 涉末端电压基准专业口径（标称 12V vs 实际发电 14.4V），待裁断。
- 原 N241 DOM XSS 已修复（第 956 批清账）。
- 假工具数：0。
- 安全条目：0 条（原 N241 反射型 DOM XSS 已由 `ToolBox.escHtml` 修复）。
- 局限：仅逐行读源码并做静态复算，未开浏览器、未跑 `_build.py`/`run_gates.py`/`_test_static.py`、未执行 git 或线上验证。

## Y 批 · 长尾·通用计算（2026-11-04）

**逐页结论**
- **calc-14**：年龄/总天数/生肖/星座主算正确（1990-05-15→2026-09-08 复算 36 岁 3 月 24 天、13265 天），但默认“今天”取 UTC 日期、闰日处理与自身承诺不符。
- **power-focal**：线能量、切深、光斑、功率密度公式可复算（默认 2.52mm、0.10mm、127.3kW/mm²），但“建议速度”、功率密度卡片与历史深度有错。
- **lifespan-5**：Q10 五因子与算例复算一致（25℃/60%/pH7/UV0→120 月；40℃/80%/pH5/UV200→18.4 月），未发现高/中问题。
- **detector-corrosion-1**：三项阈值判定可算，默认 190/250/1 级→合格；但重置/清空误判不合格、预设“通用锂基脂”自相矛盾。
- **detector-200**：三项阈值判定可算，默认 30/0.03/0.05→合格；但重置/清空误判不合格、预设“新变压器油”被 28~32 阈值误杀。
- **nianjieqiangdujisuan**：F=τA、许用载荷/许用应力换算正确（默认 20MPa×500mm²、SF3→10000N/3333N/339.8kg）；仅“估算抗拉强度”术语/量纲不符。
- **ratio-fuel-oil**：体积加权密度、质量加权热值、能量密度与算例全部一致（873 kg/m³、41.98 MJ/kg、36.65 GJ/m³、10034 kcal/kg），未发现高/中问题。
- **calc-stats-1**：正态/泊松/二项 PMF/CDF 数值与算例一致（Φ(1.96)=0.975002、P(2;3)=0.224042、P(5;10,0.5)=0.246094）；仅大 k/n 的 CDF 复杂度问题。

| 页面 | 问题（含 `tools/general/<slug>.html:NN`） | 编号 |
|---|---|---|
| calc-14 | 默认日期取 UTC 日：`today.toISOString().slice(0,10)`（`tools/general/calc-14.html:261-263`、`:310-312`）在 UTC+8 的 00:00–07:59 返回前一天，页面加载即把“计算日期”填成昨天，年龄/总天数少 1 天；引据表 `:158` 却写“跨时区以当地日期为准 / Use local date”。 | 12-N246 |
| calc-14 | 闰日未按 2/29→2/28：`new Date(y,1,29)`（`tools/general/calc-14.html:235-236`）在非闰年滚到 3/1，`calcAge` 的借位（`:213-217`）也按前月实际天数算；2000-02-29 生、2026-02-28 计算得 25 岁 11 月 30 天（应为 26 岁 0 月 0 天），下次生日显示 2027-03-01（应为 02-28），与引据表 `:157` 的承诺相反。 | 12-N247 |
| power-focal | “建议速度（按目标深度 80% 反推）”量纲/算法错：`recSpeed=(0.8*LE)/(mat.e*1)`（`tools/general/power-focal.html:244`）算出的 2.13 实际是 `0.8×dMax/fEff`（长度 mm），却被标成 mm/s 渲染（`:260`）；切深与速度成反比，取 80% 深度应把速度提到 `V/0.8=18.75 mm/s`（默认 1000W/127mm/15mm/s/碳钢），页面给 2.1，deep-dive 算例也照抄（`:470`）。 | 12-N248 |
| power-focal | 历史摘要深度未乘焦距效率：主结果 `dMax=(LE/mat.e)*fEff`（`tools/general/power-focal.html:233`），历史用 `dm=le/mat.e`（`:300`）；默认 fEff=94.6% 时主结果 2.52mm、历史显示 2.67mm，同一组输入出现两个深度。 | 12-N250 |
| power-focal | 材料比切割能 e 两套量纲：公式框/注释/结果表写 J/mm²（`tools/general/power-focal.html:158`、`:199`、`:258`），FAQ 写“熔穿单位体积材料所需能量（J/mm³）”（`:474`）；`d=LE/e` 只有在 e 为 J/mm²（或按 1mm 缝宽折算）时才得 mm，读者无法判断该信哪套。 | 12-N251 |
| detector-corrosion-1 | 重置/清空后直接判“不合格”：`calc()` 把空值当 0（`parseFloat(...)||0`，`tools/general/detector-corrosion-1.html:226`），`resetForm()` 清空后立刻 `calc()`（`:244-246`）；滴点 0<180、锥入度 0 不在 220~295，页面给出红色“综合判定：不合格”，而不是提示补填。 | 12-N252 |
| detector-corrosion-1 | 预设与阈值自相矛盾且单牌号写死：预设“通用锂基脂”给 190/265/2 级（`tools/general/detector-corrosion-1.html:407`），2 级>1 级→综合“不合格”；阈值固定为 NLGI 2 锂基脂的 220~295、≥180、≤1（`:220`），却把 GB/T 4929/269/21621（均为测定方法）写成限值来源（`:132-134`），其他稠度等级/脂种会被误判。 | 12-N253 |
| detector-200 | 同构重置误判：空值经 `parseFloat(...)||0`（`tools/general/detector-200.html:226`）变 0，`resetForm()` 清空后 `calc()`（`:244-247`）；运动粘度 0 不在 28~32→“综合判定：不合格”，水分/酸值 0 反而通过。 | 12-N254 |
| detector-200 | 预设“新变压器油”被判不合格：该预设给 12/0.02/0.02（`tools/general/detector-200.html:406`），运动粘度 12 不在写死的 28~32（`:220`）→不合格；“运行 5 年油”18 同样不合格。28~32 只对应某一粘度牌号，页面却以 GB/T 265（运动粘度测定法）作为限值依据（`:132`），其他牌号新油会被误杀。 | 12-N255 |
| detector-200 / detector-corrosion-1 | “检测服务/质量验收报告”承诺未实现且与免责声明冲突：两页标题/描述称“检测（…）服务”、结果称“检测报告可用于质量验收”（`tools/general/detector-200.html:239`、`tools/general/detector-corrosion-1.html:239`），实际只是把用户输入的实测值与固定阈值比较、无检测过程/无报告生成；同一页注意事项又写“正式检测请以权威机构报告为准”（两页 `:213`）。 | 12-N256 |
| nianjieqiangdujisuan | “估算抗拉强度”量纲不符：简介称输出“估算抗拉强度”（`tools/general/nianjieqiangdujisuan.html:495`），结果卡/复制文本输出 `tensileKg` 的 kg 值（`:228`、`:232`），公式定义为“估算抗拉 = F×1.5”（`:128`、`:448`）——这是 1.5 倍最大载荷，不是应力（MPa）；抗拉强度应为 σ=F/A 的应力。 | 12-N257 |
| calc-stats-1 | 大 k/n 会长时间卡死：`poisCdf` 每次循环都重算 `logFact(i)`（`tools/general/calc-stats-1.html:224-226`）→O(k²)，`binomCdf` 每个 pmf 重算 `logFact(n)`（`:228`）→O(k·n)；`kp`/`nn` 无上限（`:140`、`:144`），node 复算泊松 k=5 万已 5.1s、k=10 万约 20s，二项 n=1e5/k=5e4 更慢，浏览器主线程会假死。 | 12-N258 |

**统计**
- 审计页数：8（全部为 `tools/general/` 下指定页面）。
- 新增条数：13 条，编号 12-N246–12-N258（高 2 / 中 11）。
- 高优 2 条：N246（默认日期 UTC 错位）、N248（建议速度量纲/算法错）。
- 假工具数：0。
- 安全条目：0 条（未发现本批页面引入的 XSS/eval/`allow-same-origin`/明文存密/用户数据外传；各页数值输入未直入 `innerHTML`）。
- 局限：仅逐行读源码 + `node` 在 `/tmp` 复算关键数值；未开浏览器、未跑 `_build.py`/`run_gates.py`/`_test_static.py`、未做 git 或线上验证；英文态/繁体页/移动端未实测。

## Z 批 · 长尾·汽车工程/保养（2026-11-04）

**逐页结论**
- **analysis-strength**：弯曲应力/挠度公式正确（默认 b60×h120、F5000、L1000 → σ 8.68MPa、δ 0.059mm），但扭转常数把长边立方，J 放大 4 倍。
- **brake-pad-life**：主流程可算（默认 6mm/3 万 km → 剩余 15000km、12 个月），但空值兜底与预测表口径会造成假警报与同屏矛盾。
- **calc-72**：单缸/总排量与压缩比公式、deep-dive 算例（86×86×4、Vc56 → 9.92:1）复算一致，未发现高/中问题。
- **catalyst**：效率 η=(前−后)/前 与默认 85%/92.5%/85% 复算一致，但空输入被判“疑似失效”。
- **cheshenkongqizulixishu**：风阻 F=½ρCdAv²、功率 P=Fv、mph/kmh 换算（默认 312N/8.7kW）复算一致，未发现高/中问题。
- **container-loading**：体积/重量双约束与装载率公式正确，但“体积主导”模式下主结果箱数可能与表内“取大”矛盾并少算箱数。
- **countdown-engine-oil**：里程倒计时可算，但“上次换油日期”为死输入，“里程与时间先到为准”未实现。
- **current-3**：Pin=U·I、η=Pout/Pin 可算（默认 72.4%），但效率结论区间写死，50–85% 一律报“60%~75% 典型区间正常”。

| 页面 | 问题（tools/automotive/<slug>.html:NN） | 编号 |
|---|---|---|
| analysis-strength | 负输入仍判“合格”：`F` 的 `min=0`（`:146`）只约束步进按钮，键入 −5000 后 σ=−8.68MPa，`sigma<=allow`（`:328`）成立 → 绿色“合格”，实际安全系数 −27.02、挠度 −0.059mm 照常渲染。 | 12-N260 |
| brake-pad-life | 当前厚度留空/归零即假警报：`+value||0`（`brake-pad-life.html:257`）把空值当 0mm，`currentThick<3`（`:281`）直接输出“需立即更换”与“制动距离大幅增加”，不区分“未填写”；清空输入即触发。 | 12-N261 |
| brake-pad-life | 预测表与实测厚度自相矛盾：表内按 `useRate=max(实测,基础)` 从新片外推（`:325-326`），实测率低于基础率时不回填实测厚度；新片12、当前8、已行驶3万km（实测1.33、基础1.56 mm/万km）时结果卡显示 8.0mm，而“30000km ←”行显示 7.3mm，两个当前厚度同屏并存。 | 12-N262 |
| brake-pad-life | deep-dive 算例与页面极限口径不符：算例写“磨损极限 2mm（可用 10mm）”并得剩余 30000km（`:217`），代码 `minThickness=3`（`:271`）同输入只剩 4mm、约 24000km（新片12/当前7/3万km）；读者按算例复算必对不上。 | 12-N263 |
| catalyst | 空输入被判“疑似失效”：`eff(a,b)` 在前值 ≤0 或 NaN 时返回 0（`catalyst.html:296`），`judge(0,90/80)` 得 bad（`:300-303`），清空任一“催化前”浓度即输出红色“催化器效率过低，疑似失效”“需更换”，无补填提示。 | 12-N264 |
| container-loading | 主结果箱数可少于可行箱数：`mode=vol` 时 `need=byVol`（`container-loading.html:347`），而表内取 `max(bv,bw)`（`:374`）；0.6×0.5×0.5m、100 件、单件 300kg、40HQ 时总体积 15m³→主结果“1 个”，表内“取大”为 2 个、单柜 30t 超 26t 限重，advice（`:392`）只说“必须增加箱数”却不给应加到的数量。 | 12-N265 |
| countdown-engine-oil | 死输入 + 承诺未实现：`#odate`“上次换油日期”（`countdown-engine-oil.html:163`）只被 `saveCar` 存档（`:327`），`calc()`（`:374-434`）与车库 `kmLeftOf`（`:344-349`）全程未读；因而页面“里程与时间先到为准”（`:277`）、“时间上限 … 与里程先到为准”（`:403`）均未实现——上次换油 18 个月前、只跑 3000km 仍判“正常”，剩余月数恒由剩余里程÷年均里程反推。 | 12-N266 |
| current-3 | 效率结论区间写死：仅用 `eff<ref`、`eff>85` 两分支（`current-3.html:315-316`），其余一律报“处于直流起动机典型区间（60%~75%）…状态正常”（`:317`）；ref 默认 50，故 55%、80% 也被判为落在 60–75% 区间，与自身 FAQ“典型 60%–75%”（`:53`）矛盾。 | 12-N268 |
| current-3 | U/I 当成回路电阻：`res=volt/cur`（`current-3.html:298`）标注“等效回路电阻 (Ω)”（`:306`）并写入公式框“R=U÷I”（`:154`、`:312`）；起动机旋转时 U/I 含反电动势，默认 11.5V/180A 的 0.0639Ω 是等效阻抗而非线缆/电枢电阻，据此判“回路电阻升高”会误导。 | 12-N269 |
| current-3 | 输出大于输入时发热损耗为负：无 `pout<=pin` 校验（`current-3.html:295-297`），如 11.5V/180A、Pout=2500W 时效率 120.8%、损耗 −430W 仍照常渲染并只提示“核对输入”。 | 12-N270 |

**统计**
- 审计页数：8（全部为 `tools/automotive/` 下指定页面）。
- 新增条数：10 条，编号 12-N259–12-N270（高 2 / 中 8 / 安全 0；原 N267 存储型 XSS 已修复第 956 批清账，N259 扭转常数立方错边已于 969 批修复销账）。
- 高优 3 条：N259（扭转常数取错边，J/刚度 4 倍、切应力 1/4）、N266（odate 死输入且时间先到未实现）、N268（效率区间写死误判“状态正常”）。
- 中优 8 条：N260（负输入判合格）、N261（空厚度假警报）、N262（预测表与实测矛盾）、N263（算例与 3mm 极限不符）、N264（空输入假失效）、N265（体积主导箱数少算）、N269（U/I 当回路电阻）、N270（负损耗）。
- 假工具数：0。
- 安全条目：1 条 —— `tools/automotive/countdown-engine-oil.html:360`（车库车辆名直入 `innerHTML`/`onclick` 的存储型自 XSS）。
- 局限：仅逐行读源码 + `node` 复算关键数值；未开浏览器、未跑 `_build.py`/`run_gates.py`/`_test_static.py`、未做 git 或线上验证；英文态/繁体页/移动端未实测。

## Z 批 · 长尾·通用计算 II（2026-11-04）

**逐页结论（8 页）**
- `air-1`：AQI 计算器，六项污染物中 SO₂/NO₂/CO/O₃ 的 IAQI 分段表取错（用了 24h 表 / O₃ 8h 首档），IAQI 与 AQI 系统性偏高；另有空输入按 0、首要污染物与 AQI>500 外推问题。
- `assessor-20`：微加工评分，激光功率读取后未参与任何计算（死输入）；清空/重置后按 0 计得 85 分 B 级（精密），为空输入假结果。
- `calc-203`：ISO 286 配合计算，H 孔系与 d/e/f/g/h/k/n/p/r/s 轴系数值正确；孔 F/G/E 名义支持实为不可用，预设 ϕ120 K7/h6 无法计算，>500mm 静默套末档。
- `calculator-calc-10`：最小二乘线性回归，斜率/截距/R²/r/RMSE 与算例均复核一致，未发现高/中问题。
- `checker-2`：污水检查井间距分档判定正确；跌水高度固定按 40m 井距扣坡降，与同页“实际井间距”输入脱节。
- `checker-spacing`：雨水检查井分档与收水口间距公式量纲、算例均复核一致，未发现高/中问题。
- `color-temp-2`：流明法配灯，公式与两处算例复核正确；单灯光通量为 0/留空时仍输出“建议灯具数量 0 盏”。
- `concentration-22`：涂料用量，V=A×DFT×0.1/SV、实际用量、质量、涂布率、湿膜厚度均复核正确，未发现高/中问题。

**问题清单**

| 页面 | 问题（tools/general/<slug>.html:NN） | 编号 |
| --- | --- | --- |
| air-1 | SO₂/NO₂/CO 输入标注为“1h均值”，但 `BP` 用的是 24h 分指数表（`so2:[[0,50,…]]`、`no2:[[0,40,…]]`、`co:[[0,2,…]]`，`:198-200`），O₃ 首档又用 8h 表的 100 断点（`:201`），`calcIAQI` 直接查表（`:205-216`）。实测 NO₂ 200 μg/m³→IAQI 160（应 100）、CO 5 mg/m³→105（应 50）、SO₂ 500 μg/m³→154（应 100）、O₃ 80 μg/m³→40（应 25），AQI 随之系统性偏高；页内算例又写 O₃ IAQI=25（`:484`），与实际输出 40 自相矛盾。 | 12-N271 |
| air-1 | `readInputs()` 算出的 `valid`（`:229-231`）在 `calc()` 中从未使用（`:234-246`）：任一浓度留空即按 0 参与 IAQI，仍照常输出一个偏低的 AQI，只给输入框描红。 | 12-N272 |
| air-1 | AQI 评价口径偏差：`maxIAQI>0` 即指定首要污染物（`:237-248`），AQI≤50 时标准规定不发布首要污染物；浓度超过表末限值后按最后一段线性外推（`:214-216`），如 PM2.5=2000 输出 AQI=1500，而 HJ 633 规定 AQI>500 不再评价。 | 12-N273 |
| assessor-20 | 激光功率为死输入：`pwr` 读入后（`:214`）未参与 `accScore/hazScore/effScore` 或综合分（`:215-218`），但标题与简介宣称按“切割速度与激光功率”评估（`:10-11`），四项输入实为三项评分。 | 12-N274 |
| assessor-20 | 空输入得高分：`parseFloat(...)||0` 使清空后 acc=0、haz=0（`:211-213`），而 0 落入 `acc<=2→100`、`haz<=5→100`（`:215-216`），速度 0→40，综合 100×0.4+100×0.35+40×0.25=85，输出“85 分 · B级（精密）”；重置按钮正是清空全部输入后调 `calc()`（`:232`）。 | 12-N275 |
| calc-203 | 孔 F/G/E 名义支持、实际全不可用：`:225` 先把孔字母 `toUpperCase()`，`:207` 却用大写字母查小写键表 `ES_NEG`（`:193`），恒为 undefined→`return null`，随后 `:230` 报“暂不支持”；而错误提示与说明均称“支持孔 H/F/G/E”，如 F7/h6 必失败。 | 12-N276 |
| calc-203 | 预设“ϕ120 K7/h6 过渡配合”（`:366`）不可计算：孔字母 K 既非 H 也不在 `ES_NEG`（`:193`）中，`parseDev` 返回 null，直接落到“暂不支持”分支（`:230`），预设按钮点了只出错误提示。 | 12-N277 |
| calc-203 | 尺寸越界静默套末档：`sizeIdx` 对 D>500 直接返回最后一档（`:196`），`:226` 据此取 400-500mm 的 IT 值与偏差；如输入 D=600 仍按 400-500 档给出公差且无任何越界提示，页面却宣称范围 0~500mm。 | 12-N278 |
| checker-2 | 跌水高度写死井间距 40m：`var L=40`（`:274`）计算坡降（`:273-276`），而同页已有“实际井间距 L”输入（`:147`）且完全未参与该页计算；实际井距 60~100m 时坡降被低估、跌水高度偏大，1m/2m 分档可能翻转。页内算例也直接用总落差 0.70m 未扣坡降（`:376`），与工具输出不一致。 | 12-N279 |
| color-temp-2 | 单灯光通量留空/填 0 时仍出结果：`lamp>0?ceil(...):0`（`:218`）使数量记 0，`:223` 照常显示“建议灯具数量 0”，`:231` 文案为“按单灯 0 lm 配置约 0 盏”，无校验或警告，易被当作“无需灯具”的有效结论。 | 12-N280 |

**统计**
- 审计页数：8（全部为 `tools/general/` 下指定页面）。
- 新增条数：10 条，编号 12-N271–12-N280（高 6 / 中 4 / 假工具与承诺未实现 3 / 安全 0）。
- 高优 6 条：N271（SO₂/NO₂/CO/O₃ 分指数表取错，IAQI 成倍偏高）、N274（激光功率死输入）、N275（清空输入得 85 分 B 级）、N276（孔 F/G/E 不可用）、N277（K7/h6 预设死按钮）、N279（跌水固定 40m 井距）。
- 中优 4 条：N272（空浓度按 0 计入）、N273（≤50 标首要污染物 + >500 外推）、N278（>500mm 静默套末档）、N280（单灯 0 lm 输出 0 盏）。
- 假工具数：0（无整页空壳）；承诺未实现 3 条 —— N274、N276、N277。
- 安全条目：0 条 —— 未见 XSS/eval/allow-same-origin/明文存密/第三方外传；各页历史记录均经 `escHtml` 或仅写数值，未发现可利用注入。
- 局限：仅逐行读源码 + `node` 复算关键数值；未开浏览器、未跑 `_build.py`/`run_gates.py`/`_test_static.py`、未做 git 或线上验证；英文态/繁体页/移动端未实测。

## AA 批 · 长尾·汽车周期/油耗/轮胎（2026-11-04）

**逐页结论（8 页）**
- `cycle-13`：雨刷台账，周期与状态判定逻辑成立，但卡片“已使用 N 个月（X 天）”取用 `calcWiper` 未返回的 `daysPassed`，恒渲染 `undefined 天`。
- `cycle-belt`：皮带剩余里程/进度/天数复核正确；但“自定义车型（手动输入周期）”没有周期输入框、恒按 8 万 km；车型表把正时链条的 EA888 标为皮带且是默认选中项。
- `detector-recorder-fuel`：均值/σ/正态区间与页内算例（8.22 L、0.74、6.73~9.70）逐项一致，默认记录量级合理，未发现高/中问题。
- `estimate-distance-1`：反应距离、v²/(2g(μ+坡度)) 制动距离与总停公式正确；速度对照表“总停”列漏加制动协调距离，而结果卡与公式含该项。
- `estimate-wear-tire`：磨损率 0.1mm/千km、剩余 24000km、总寿命 64000km 均正确；但把 4 条轮胎寿命相加报“合计约 256000 km”。
- `fuel-anomaly`：区间油耗/阈值算法正确，但默认 5 条记录为每 1500km 加 38~45L，折算 2.53~3.00 L/100km（均值 2.73）并被判“油耗表现优秀”，量级明显失真。
- `fuel-converter`：235.214583 / 282.480936 / 100 三个系数与 7 L/100km≈33.6 mpgUS≈14.3 km/L 等算例逐项复核一致，未发现高/中问题。
- `fuel-cost-calculator`：300km/7L/8元→168 元、人均 42 元、对比 216 元、预算 536km 均复核正确；清空“对比车型油耗”或“预算”时按 0 计并输出虚假对比结论。

**问题清单**

| 页面 | 问题（tools/automotive/<slug>.html:NN） | 编号 |
|---|---|---|
| cycle-13 | 已使用天数恒为 undefined：`calcWiper` 返回对象只含 `monthsPassed`/`remainDays`（`cycle-13.html:396`），卡片却渲染 `${r.daysPassed}`（`:448`），任何车辆记录都显示“已使用 N 个月（undefined 天）”；且 `remainDays` 用 `cycleMonths*30−daysPassed`（`:390`）与日历月差（`:387`）不同源，两处剩余时间会互相矛盾。 | 12-N281 |
| cycle-belt | “自定义车型（手动输入周期）”为死功能：MODELS 备注写“请根据保养手册填写更换里程”（`cycle-belt.html:293`），但页面没有周期输入框，`onModelChange` 的 custom 分支为空注释（`:311-313`），恒用 `interval:80000`（`:293`）；无论手册写 6 万还是 15 万都只能得到 8 万的结果与提示。 | 12-N282 |
| cycle-belt | 车型表错项且为默认项：EA888（1.8T/2.0T）为链条机型，表中却标 `type:'belt',interval:100000`（`cycle-belt.html:281`）并备注“皮带+张紧轮+水泵”，且 `initModelSel` 首项即默认选中（`:302-305`），打开页面就把链条车判成“正时皮带剩余 15000km”，未换过（lastKm=0）还按 0 起算（`:319-344`）；同一表内 HR16 也标 belt（`:284`）。 | 12-N283 |
| fuel-anomaly | 默认数据量级错误导致虚假“优秀”：默认 5 条记录里程 40000→46000（每条 +1500km）配 38/40/45/41L（`fuel-anomaly.html:234-240`），折算仅 2.53/2.67/3.00/2.73 L/100km、均值 2.73、每公里 0.21 元；`avgConsumption<6` 直接判“油耗表现优秀，属于节油水平”（`:369`）。真实乘用车 40L 约跑 500km，默认里程间隔应为 500km 左右，现数据把油耗压低约 3 倍。 | 12-N284 |
| estimate-wear-tire | 多胎寿命相加无意义：`totalLife*cnt` 输出“单条轮胎总寿命约 64000 km（4 条合计约 256000 km 里程）”（`estimate-wear-tire.html:358`），四胎同时磨损并不串行累加；`cnt` 选择（`:154-159`、`:300`）除此之外不参与任何计算，等于只为这句错值服务。 | 12-N285 |
| estimate-distance-1 | 对照表漏算制动协调距离：结果总停 = 反应 + 协调 + 制动（`:309`、`:343-346`），而速度表“总停 μ=”列只算 `r1+bdAt(mu)`（`:337-341`），未加 `v*bt`；输入框标注“通常 0.2”（`:160`）而默认为 0，用户按提示填 0.2 后 100km/h 处表格比结果卡少 5.6m，两处同屏不一致。 | 12-N286 |
| fuel-cost-calculator | 清空对比项/预算即按 0 计并给结论：`cost2` 在 `fc2` 为空时取 0（`fuel-cost-calculator.html:299`），`diff=cost2-cost`（`:300`）随之输出“对比车型差额 −168 元”“对比车型油费 0 元”（`:306-307`）及“本车油费比对比车型高 168 元”（`:317`）；`budget` 为空时 `range=0`（`:301`）显示“预算可行驶 0 km”，均无“未填写”区分。 | 12-N287 |

**统计**
- 审计页数：8（全部为 `tools/automotive/` 下指定页面）。
- 新增条数：7 条，编号 12-N281–12-N287（高 4 / 中 3 / 假工具 0 / 安全 0）。
- 高优 4 条：N281（`daysPassed` 未返回恒 undefined）、N282（自定义车型无周期输入、写死 8 万）、N283（EA888 链条误标皮带且为默认项）、N284（默认记录折算 2.73 L/100km 被判“优秀”，量级差约 3 倍）。
- 中优 3 条：N285（4 胎寿命相加 256000km）、N286（速度表漏算协调距离）、N287（清空对比油耗/预算按 0 计）。
- 假工具数：0（无整页空壳）；承诺未实现 1 条 —— N282。
- 安全条目：0 条 —— 8 页未发现 XSS/eval/allow-same-origin/明文存密/第三方外传；`cycle-13` 的车辆名与品牌、`cycle-belt` 的记录车型名均经 `ToolBox.escHtml`，`fuel-anomaly`/`fuel-cost-calculator` 仅拼数值。
- 局限：仅逐行读源码 + `node` 复算关键数值；未开浏览器、未跑 `_build.py`/`run_gates.py`/`_test_static.py`、未做 git 或线上验证；英文态/繁体页/移动端未实测。

## AA 批 · 长尾·通用检测/寿命 III（2026-11-04）

**逐页结论（8 页）**
- `convert-22`：SI 词头换算公式 `v×f/t` 与 `toPrecision(12)` 本身正确，速查表 19 档齐全；但**下拉只有 11 档**（缺 T/P/E/Z/Y 与 p/f/a），标题宣称的「皮 p 至 尧 Y 共 19 档」在主功能里做不到。
- `detector-118`：权重 0.35/0.35/0.20 + 认证加分 5/5/10/0 的算术与 A~E 分级复核一致；但清空/重置后按 0 计仍给「5 分 · E 级」，且百分比无值域校验。
- `detector-126`：三项阈值与算例（1.5/85/93→合格）复核正确；但预设「常规合格批」给 78%/88%，点选即判不合格。
- `detector-128`：黏度/水分/闪点三项比较逻辑正确；闪点口径在输入说明（开口 GB/T 3536）与引据表（闭口 ISO 2719）之间自相矛盾，黏度则只有单一 30~50 窗口、无牌号可选。
- `detector-16`：覆盖面积公式多乘了一次检测距离（`π×h×tan30°×dist`），默认 2.5m/5m 得 22.7m²（正确约 6.6m²），且「推荐传感器类型」只是回显下拉选项。
- `detector-205`：盐雾 480h / 湿热 1000h 判定可运行；吸附量以 mg/g 判 ≥100，但引据表公式写的是「×100%」，且涂层件三项捆绑吸附容量后汽车件/户外件预设必然不合格。
- `detector-207`：脱模力 ≤50N、残留 ≤10 的判定正确；残留单位 mg/dm² 与引据表 mg/cm² 差 100 倍，预设「残留偏高」实际失败项是环保 82%。
- `detector-aging-1`：耐热 ≥150℃、保持率 ≥80% 判定正确；「安全等级 1~5 级」是页面自造刻度（GB 8624 用 A1/A2/B1/B2/B3、UL 94 用 V-0/V-1/V-2），阈值无从核验。

**问题清单**

| 页面 | 问题（tools/general/<slug>.html:NN） | 编号 |
|---|---|---|
| convert-22 | 主功能缺 8 档词头：两个下拉只有 `1/10/100/1000/1e6/1e9/0.1/0.01/0.001/1e-6/1e-9` 共 11 档（`:130-131`），而 `<title>`/meta/深度解析宣称「皮 p 至 尧 Y 共 19 档」（`:11`、`:10`、`:171`、`:175`），速查表 `SI_PREFIX` 也有 19 档（`:217`）；tera/peta/exa/zetta/yotta 与 pico/femto/atto 全部无法参与换算，宣称的最高/最低量级在下拉里不存在。 | 12-N288 |
| convert-22 | 批量默认值与页内算例不符：默认选「无→无」（`:131`），批量框预填 1000/0.001/1e-6（`:141-143`），打开页面「换算结果」列全是原值；而深度解析算例写明「从『毫』到『微』」应得 1000000/1/0.001（`:176`），用户按算例复现必对不上（需手动改两个下拉）。 | 12-N289 |
| detector-16 | 「推荐传感器类型」纯回显：输出行直接取 `modes[mode]`（`:225`，mode 来自下拉 `:219-220`），与用户所选完全相同，无任何按距离/高度/温度的选型逻辑；按钮却叫「选型计算」（`:134`）。 | 12-N291 |
| detector-16 | 空输入反向判「满足」：`parseFloat(...)||0`（`:216-218`）使清空后 dist=0、hgt=0、temp=0，`coverage=0`、`suitable=0<=8` 为真、`tempOk` 为真（`:222-224`），结果卡输出「✅ 参数满足要求」并渲染「约 0.0 m²」；重置按钮正是清空后 `calc()`（`:239`）。负距离还会输出负面积。 | 12-N292 |
| detector-118 | 重置得「5 分 · E 级」：`parseFloat(...)||0`（`:215-217`）把清空值当 0，`resetForm()` 又把 select 复位到首项 ISO 9001（`:236`），`certBonus=+5`，`total=Math.round(0+0+0+5)=5`（`:219-221`）→ 红字「E级（不合格）」，不提示补填；默认/预设的「三体系认证标杆」实际也只能选到「双体系」（`:391`），名称多一体系。 | 12-N293 |
| detector-118 | 百分比无值域校验：三项输入缺 `min/max`，`std/qual/env` 直接入式（`:215-222`）；填 150/150/150 且双体系得 `Math.round(52.5+52.5+30+10)=145` 分仍判「A级（卓越）」，填负值则可得负分 E 级，均无越界提示。 | 12-N294 |
| detector-126 | 预设与结论自相矛盾：预设「常规合格批」给 `v1=9.5, v2=78, v3=88`（`:403`），而阈值是 老化≥80、环保≥90（`:216`），点选后两项判红、综合「❌ 综合判定：不合格」；名字承诺的合格批次实际不合格（`v3` 88 与环保阈值 90 仅差 2 点，最易被误读）。 | 12-N295 |
| detector-128 | 闪点开/闭口口径打架：输入说明写「GB/T 3536 开口闪点≥200℃」（`:130`），引据表却写「按闭口杯法测定 / ISO 2719」（`:200`），判定阈值 200 直接来自开口杯口径（`:216`）；同一指标开口与闭口结果通常差 20~30℃，按闭口杯送检的油会被系统性误判。 | 12-N296 |
| detector-128 | 黏度单一窗口、无牌号选择：判定固定 `range 30~50`（`:216`），页面无黏度等级/牌号下拉；VG68（68 mm²/s）、VG100 等完全合法的工业油一律判「不合格」，而深度解析自认「对应 ISO VG46 附近」（`:174`）。另把 GB/T 265（运动黏度**测定法**）写成限值来源（`:128`、`:190`）。 | 12-N297 |
| detector-205 | 吸附量与涂层耐候捆绑、单位口径不一：输入/判定用 mg/g 且阈值 ≥100（`:130`、`:216`），引据表公式却写「质量增量/样品质量 ×100%」（无量纲 %，`:199`）；三个场景预设的吸附量给 45/80/15（`:402-404`），汽车件、户外件、室内件因此必然「不合格」——涂层盐雾/湿热与吸附容量属两类材料体系，任一项都无法同时成立。 | 12-N298 |
| detector-207 | 残留量单位差 100 倍：输入与判定用 `mg/dm²`、阈值 ≤10（`:129`、`:216`），引据表公式却写「残留质量/面积 mg/cm²」（`:194`）；1 dm²=100 cm²，同一数值在两处相差 100 倍，读者无法判断 10 是 10 mg/dm² 还是 10 mg/cm²。 | 12-N299 |
| detector-207 | 预设名与失败项不符：预设「残留偏高」给 `v1=48, v2=9.5, v3=82`（`:404`），残留 9.5 与脱模力 48 均在限值内，实际判不合格的是环保达标率 82%（<90，`:216`）；用户会以为「残留 9.5 已超标」。 | 12-N300 |
| detector-aging-1 | 「安全等级 1~5 级」为自造刻度：下拉 `1级最安全`~`5级最低`（`:130`），FAQ 称其为「材料燃烧安全分级」（`:174`），但真实分级为 GB 8624 的 A1/A2/B1/B2/B3 或 UL 94 的 V-0/V-1/V-2，页面未给任何标准、等级映射或判定依据，「≤2 级」（`:216`）无法核验，也无法与检测报告对接。 | 12-N301 |
| detector-118 / 126 / 128 / 205 / 207 / aging-1 | 同源模板的空值/重置误判：`parseFloat(...)||0`（`:215-217` 等）把清空值当 0，`resetForm()` 清空后立即 `calc()`（`:236`/`:240`），126/128/205/207/aging-1 直接红字「❌ 综合判定：不合格」、118 给「5 分 · E 级」（见 N293），均不区分「未填写」。 | 12-N302 |
| detector-126 / 128 / 205 / 207 / aging-1 | 六页 `formula-desc` 均为模板串味文案：「本工具用于检测（…）服务的合法性校验，依据对应数据格式与语法规范实时检查并定位错误」（各页 `:125`），与三项实测值对照阈值的判定逻辑完全无关，属承诺了不存在的「格式/语法校验」。 | 12-N303 |
| detector-126 / 128 / 205 / 207 / aging-1 | 把测定方法标准当限值来源：GB/T 7124（胶粘剂拉伸剪切强度测定）、GB/T 265（运动黏度测定法）、GB/T 3536（开口杯闪点）、GB/T 1740（漆膜耐湿热测定法）、GB/T 7141（热老化试验方法）、GB/T 10125（盐雾试验方法）均只规定试验方法，不给出本页的 1.0MPa/30~50/200℃/1000h/150℃/480h 阈值；另「环保达标率≥90%」（126/207）是把达标项占比当指标，GB 18583 规定的是有害物质限量，并非「达标率」阈值。 | 12-N304 |

**统计**
- 审计页数：8（全部为 `tools/general/` 下指定页面）。
- 新增条数：16 条，编号 12-N288–12-N304（高 3 / 中 11 / 承诺未实现与假功能 3 / 安全 0；N290 覆盖面积多乘距离已于 970 批修复销账）。
- 高优 3 条：N288（下拉缺 8 档、19 档宣称做不到）、N290（覆盖面积多乘检测距离，默认高估 3.5 倍）、N291（「推荐传感器类型」纯回显）。
- 中优 12 条：N289（批量默认与算例不符）、N292（空输入判「满足」）、N293（重置 5 分 E 级）、N294（百分比无值域）、N295（预设合格批实际不合格）、N296（闪点开/闭口冲突）、N297（黏度单窗口）、N298（吸附量捆绑+单位）、N299（残留单位差 100 倍）、N300（预设名与失败项不符）、N301（自造安全等级）、N302（同源空值误判）。
- 承诺未实现与假功能：3 条 —— N288（19 档）、N291（选型回显）、N303（不存在的格式/语法校验文案）；N301 亦属无标准支撑的自造维度。
- 安全条目：0 条 —— 8 页未发现 XSS/eval/allow-same-origin/明文存密/第三方外传；判定结果仅拼接数值与固定中文文案，历史/趋势由 `TBKit` 渲染，未见用户输入直入 `innerHTML`。
- 局限：仅逐行读源码 + `node` 复算关键数值；未开浏览器、未跑 `_build.py`/`run_gates.py`/`_test_static.py`、未做 git 或线上验证；英文态/繁体页/移动端未实测。

## AB 批 · 长尾·汽车保养周期族（2026-11-04）

> 页面名后的「（死键 N）」= 该页第三层英文词典（`i18n/tools/en/<ind>/<slug>.json`）高优先死键数（来源 `plan/i18n-dead-keys.md`）；各线改本页时顺手清理，本批不修英文。

**族矩阵**（汽车保养周期族，12 页，全部 `tools/automotive/`）

| 页面 | 实现方式 | 是否可逆或可验证 | 结论 |
|---|---|---|---|
| insurance-premium-estimator（死键 0） | 自写（费率表 × 地区/NCD 系数） | 交强/三者可核；车损混用「万元/元」不可核 | 车损险少算约 1 万倍 |
| lifespan-brake（死键 0） | 自写（剩余厚度 ÷ 月磨损） | 可反算（月数 × 速率 = 厚度） | 真实现，缺「当前 > 新品」校验 |
| lux-1（死键 0） | 自写（立体角 + 平方反比） | 可反算（I = E·d²，节点自洽） | 真实现，但法规承诺落空 |
| maintenance-schedule（死键 0） | 自写（周期整倍数滚动） | 可反算（⌈km/T⌉·T） | 真实现，「已逾期」维度恒空 |
| oil-change（死键 0） | 自写（基础周期 × 工况/涡轮） | 可反算 | 真实现，「下次里程」口径错 |
| oil-change-countdown（死键 0） | 自写（上次里程 + 上次日期双阈值） | 可反算（里程/日历两路） | 真实现，**本族唯一真正双阈值** |
| pressure-fuel-oil（死键 7） | 自写（喷油量 ↔ 进气质量 → AFR） | 可独立交叉校核（第二条路径算 λ） | **本组唯一闭环自洽页**，默认 14.2 AFR 合理 |
| qichekongtiaoxuanxing（死键 0） | 自写（经验冷负荷系数） | 部分可核（分项与总量可加和） | 真实现，默认 3.66 kW/1.31 kW 自洽 |
| recommender-6（死键 0） | 自写（基准 + 载荷/季节 + 理想气体折算） | 可反算（折算后偏差 = 实测 − 推荐） | 真实现，TPMS 报警分支恒不触发 |
| resistance-1（死键 0） | 自写（温度折算 + 匝数比 √(R2/R1)） | 可反算（默认 0.8Ω/8kΩ = 100:1） | 真实现，默认与深度算例一致 |
| scheduler-cycle-maintenance（死键 0） | 自写（周期整倍数 + 完成日志） | 可反算 | 真实现，「逾期」恒空、`上次保养里程` 空转 |
| shachepiangenghuanzhouqi（死键 0） | 自写（剩余厚度 ÷ 磨损速率） | 可反算 | 真实现，**本族唯一校验「当前 > 新品」**，但剩余比例口径与他页不一 |

**逐页结论**

- `insurance-premium-estimator`：交强/三者/人员三项量级可用，**车损险把万元当元**，默认合计 1335 元实际应约 2415 元。
- `lifespan-brake`：默认 8 个月（12→6mm、0.5mm/月、极限 2mm）正确；当前厚度填大于新品时不报错反而给负磨损与超长寿命。
- `lux-1`：默认 4467 cd / 44.7 lx 与深度算例一致，光强—照度可互算；但「对照 GB 4599 判断符合性」在页内未实现。
- `maintenance-schedule`：默认「最近到期 机油 5000 km」正确，但默认 45000 km 恰为 15000/45000 周期整倍数，空气/空调滤与火花塞正到期却被判「正常」。
- `oil-change`：半合成 7500 km 口径正确，但「下次换油里程 = 当前 + 整周期」未扣已行驶 3000 km，默认报 37500 而非 34500。
- `oil-change-countdown`：默认 3000 km / 72 天双阈值判断合理，是本族唯一把「上次换油日期」真正参与计算的页。
- `pressure-fuel-oil`：默认 350 cc/min、3.5ms、2500rpm、35% 充气效率得 AFR 14.2、λ 0.97，与独立进气质量路径一致，未见算错。
- `qichekongtiaoxuanxing`：默认 5 m³/2 人/35℃/温降 15℃ → 3.66 kW、1.31 kW、600 g，分项可加和，属真实现。
- `recommender-6`：默认 2.3 bar/25℃ 折算 2.26 bar、偏差 −0.04 bar 正确；报警下限只显示不参与判定。
- `resistance-1`：默认 0.8Ω/8kΩ/25℃ → 0.78Ω/7.85kΩ/100:1，与算例一致；清空则直接判「断路」。
- `scheduler-cycle-maintenance`：默认 9 项全「正常」；因下次到期恒按当前里程重算，已逾期与「上次保养里程」都无实际作用。
- `shachepiangenghuanzhouqi`：默认 62500 km / 已行 50000 km 正确；「剩余比例 66.7%」按新品总厚算，而非可磨区间。

**问题清单**

| 页面 | 问题（tools/automotive/<slug>.html:NN） | 编号 |
|---|---|---|
| maintenance-schedule | **【高】**「已逾期」永远为空：`next=Math.ceil(km/cyc)*cyc` 后紧跟 `if(next<=km) next=km+cyc`（`:350-351`），故 `left=next-km` 恒 ≥ 周期 >0，`:355` 的 `if(left<=0)` 永不成立；无论实际超期多少（当前 45000、上次 20000）都只显示「正常/即将到期」，`:379` 的已逾期卡片恒为「无」。 | 12-N306 |
| scheduler-cycle-maintenance | **【高】**同上「逾期」维度结构性失效：`:384-385` 强制 `next>km`，`:402` 的 `left<=0` 不可达；`上次保养里程` 输入（`:168`）只用于 `:414` 的「距上次保养」展示，从不参与排程，页面宣称的「到期/超期清单」（`:164`）实际只能出「正常/即将」两态。 | 12-N307 |
| maintenance-schedule | **【高】**默认态即误判「正到期」为「正常」：默认 45000 km 同时是空气滤 15000、空调滤 15000、火花塞 45000 的整倍数（`:335-340`），`:351` 把整倍数点强行跳到下一周期，输出「剩余 15000 / 45000 km、正常」，而这三项此刻正到期；另「新能源（纯电/插混）」仅乘 0.9（`:162`、`:348`），仍排「机油 + 机滤 / 火花塞 / 正时皮带」，纯电车型不应有机油与正时项。 | 12-N316 |
| lux-1 | **【②承诺未实现】**标题/meta/正文均称「对照 GB 4599 法规判断符合性」（`:10`、`:138`），但判定只用自设中心照度阈值 20/40/10 lx @10 m（`:152-154`、`:328-331`），未实现 GB 4599 的 75R/50R/50L 等测试点；页内 `:192` 又自认「正式结论须以标准测试点为准」，属承诺与实现不一致（引据表还混用 ECE R112 / GB 25991，`:245`、`:250`）。 | 12-N308 |
| maintenance-schedule | **【②承诺未实现】**「时间上限」列（12/24/48/60 月，`:200-211`）与 `monBase` 全部空转：循环只按里程算 `left`（`:347`、`:353`），8 项时间维度从未参与判定；且「上次保养日期」`sdate` 只在 `:399` 原样回显，不做日期差，「距上次保养已过 8 个月」需用户手动另填（`:155`），日期输入形同虚设。 | 12-N309 |
| scheduler-cycle-maintenance | **【②承诺未实现】**同样的时间维度空转：`raw` 每项第 3 列 12/24/48/60 月（`:370-378`）写入后被丢弃，`calc` 只读 `o.left`（`:400-411`），「时间上限」表（`:200-211`）对结果零影响，刹车油/防冻液到期只看里程。 | 12-N310 |
| insurance-premium-estimator | **【中】**交强险误用商业险 NCD：`:366` 对交强同样乘 0.85/0.7/0.6，而交强费率浮动上限仅 −30%（最低 0.7）；默认 950×0.6=570 元，应为 950×0.7=665 元，2 年未出险 665 应为 760，全档系统性少算 95 元。 | 12-N311 |
| lifespan-brake | **【中】**缺「当前厚度 > 新品厚度」校验：`:297` 只判 `cu<0`，填 13/12/2mm 时 `left=11`、`months=22`、`wornPct=-10%`，仍提示「剩余 22 个月、状态良好」；且「用车工况」系数 `:301` 又乘在**实测**月均磨损上，高速 ×0.8 会把已实测的 0.5mm/月再打折成 0.4，寿命虚高 25%。 | 12-N312 |
| lux-1 | **【中】**清空输入即红字误判：无空值守卫，`lm/ang` 为 NaN 时 `omega>0` 与 `d>0` 均假（`:315-316`），`I=E=0`、`E10=0`，`:331` 落到「明显不足」并提示「须检修或更换灯具总成」，清空/重置后即显示灯具不合格。 | 12-N313 |
| resistance-1 | **【中】**清空输入即判「断路」：`:317-329` 对 NaN 的所有区间比较都为假，初级落入末支「断路或严重氧化」、次级落入「电阻过高，接近断路」，均标 `bad`；没有「请输入」区分态。 | 12-N314 |
| recommender-6 | **【中】**TPMS 低压报警分支恒不触发：`stOf` 内判据是 `rec<=alarm*1.02`（`:334`），`rec` 是推荐值、`alarm=rec*0.75`，该式永远为假；实测 1.0~1.6 bar（已低于 1.73 bar 报警下限）仍只报「偏低，需补气」黄色，`:340` 的 `bad` 状态不可达，与该页「TPMS 报警下限」卖点不符。 | 12-N315 |
| scheduler-cycle-maintenance | **【中】**整倍数越界 + 空输入假绿：`km` 恰为周期倍数时 `:385` 跳到 +1 周期（60000 对应 60000km 防冻液 → 剩 60000km「正常」）；清空里程得 NaN，所有 `left<=ahead` 为假、`:404` 全落「正常」，输出「9 项正常、最近一项尚有 -- km」；`Math.min` 亦为 NaN。 | 12-N317 |
| oil-change | **【中】**「下次换油里程」未扣已行驶里程：`next=cur+km`（`:361`）、`months=km/(yearKm/12)`（`:363`）、公式行「下次约在 … km」（`:375`）均按整周期算，而 `left=km-done` 已是剩余量；默认 30000+7500=37500，实际应为 30000+4500=34500，同页同时显示「剩余 4500 km」，自相矛盾。 | 12-N318 |
| oil-change-countdown | **【中】**清空日期后 `null<=0` 为真：`leftDay` 为 null 时 `:342` 的 `leftDay<=0` 仍成立（JS 把 null 转 0），里程超期会被标成「里程与时间均已超期」，而 `:346` 的 `cls` 又正确区分——同一状态两种口径，文案误导。 | 12-N319 |
| shachepiangenghuanzhouqi | **【中】**「剩余比例」口径不符：`wearPct=wornThick/newT`、`remainPct=100-wearPct`（`:222-223`）按新品总厚算，默认 8/12mm 显示「剩余 66.7%」，但可磨损区间是 12→3mm，实际剩余 5/9=55.6%（`lifespan-brake` 用的正是后者），两个刹车页同名指标差 11 个百分点；另 `:243` 参考标尺末段 10000+ 统一标「注意观察」，62500 km 落橙区与「状态良好」结论矛盾。 | 12-N320 |

**统计**
- 审计页数：12（`tools/automotive/` 指定 12 页，只读）。
- 新增条数：15 条，编号 12-N305–12-N320（高 3 / 中 9 / 承诺未实现与假功能 3 / 安全 0）；N305 车损险万元量纲已于 969 批修复销账。
- 高优 4 条：N305（车损险万元当元，默认少算约 1080 元）、N306/N307（两张排程页「已逾期」结构性不可达）、N316（默认里程整倍数时正到期项被判正常）。
- 承诺未实现 3 条：N308（GB 4599 符合性未实现）、N309/N310（时间上限列与「上次保养日期」未接入计算）。
- 中优 9 条：N311（交强 NCD）、N312（厚度越界+工况重复计入）、N313/N314（清空即误判）、N315（TPMS 报警死分支）、N317（整倍数/空输入）、N318（下次里程口径）、N319（null≤0）、N320（剩余比例口径+标尺）。
- 真实现且默认自洽（无问题）：`pressure-fuel-oil`、`qichekongtiaoxuanxing` 两页。
- 「同类唯一」差异：里程+时间双阈值仅 `oil-change-countdown` 真做（两张排程页只有里程整倍数）；「当前厚度 > 新品」拦截仅 `shachepiangenghuanzhouqi` 有（`lifespan-brake` 缺失）；独立第二路径校核（AFR/λ）仅 `pressure-fuel-oil`。
- 安全条目：0 条 —— 12 页未发现 XSS/eval/allow-same-origin/明文存密/第三方外传；用户输入仅以数值参与运算后拼入固定文案，`sdate` 取自 `<input type="date">`（浏览器已限定格式），历史记录走 `ToolBox.escHtml`/`TBKit`。
- 局限：仅逐行读源码 + 手算复算；未开浏览器、未跑 `_build.py`/`run_gates.py`/`_test_static.py`、未做 git 或线上验证；英文态/繁体页/移动端未实测。

## AB 批 · 长尾·寿命/老化检测族（2026-11-04）
> 页面名后的「（死键 N）」= 该页第三层英文词典（`i18n/tools/en/<ind>/<slug>.json`）高优先死键数（来源 `plan/i18n-dead-keys.md`）；各线改本页时顺手清理，本批不修英文。

本波 12 页全部位于 `tools/general/`，均为「自写 JS 计算/判定」，无第三方计算库、无回显页、无空壳；其中 6 页 `detector-*` 是同一份「三项阈值判定」模板批量派生（仅换文案与阈值），另 6 页为独立算法页。审计方式：只读源码 + 按默认值手算复算，未执行页面。

**族矩阵**

| 页面 | 实现方式（库/自写/回显/伪） | 可验证性 | 结论 |
|---|---|---|---|
| detector-aging-2（死键 0） | 自写：3 个用户输入逐项与固定阈值比较（无表、无公式运算） | 可验证（纯比较，手算即得） | 真实现，但是「判定器」而非「测量/检测服务」 |
| detector-composition-1（死键 0） | 同上模板（≥95 / ≥95 / ≥85） | 可验证 | 真实现（模板推导） |
| detector-composition-aging（死键 0） | 同上模板（≥85 / ≥80 / ≥95） | 可验证 | 真实现（模板推导） |
| detector-length-lifespan（死键 0） | 同上模板（≥500N / ≤2% / ≥5×10⁵） | 可验证 | 真实现，但「长度偏差」缺绝对值判据（见 N321） |
| detector-water-pressure（死键 0） | 同上模板（≥99% / ≥30min / ≤0.01%） | 可验证 | 真实现，但只判保压时长、未判承压（见 N324） |
| detector-lifespan（死键 0） | 自写查表：`baseLife[tool]×matFactor[mat]` + 磨损/次数双判据 | 可验证到算术；表值为自设经验值 | 真实现，剩余寿命只由次数决定（见 N330） |
| estimate-36（死键 1） | 自写瑞利判据 `R=k1λ/NA`、`DOF=k2λ/NA²` | 可验证（解析式） | 真实现，但焦深展示与公式自相矛盾（见 N325） |
| frequency-15（死键 1） | 自写：ω→v/a→声强→功率，MRR 为经验式，Hv 查表 | 可验证到算术；K=0.5、Hv 表无出处 | 真实现，F 缺空值拦截仍出评级（见 N326） |
| jiguangrongfuhoudujisuan（死键 0） | 自写质量守恒（g/min→g/mm→mm²）+ 抛物线截面系数 0.74 | 可验证（单位链可逐步复算） | 真实现，百分比输入超范围未拦（见 N327） |
| lifespan-10（死键 1） | 自写材料参数表 + 温度/载荷/腐蚀/使用四因子加权 | 部分（表值与权重自设，无标准出处） | 真实现，默认自洽（无问题） |
| lifespan-corrosion（死键 1） | 自写：`(厚−裕量)/修正速率`、环境系数表 [1,1.5,2.5,4] | 可验证（除法+查表） | 真实现，参考标尺与文案阈值错位（见 N328） |
| lifespan-wear-2（死键 1） | 自写：`允许量/(速率×日运行/24×类型因子)` | 可验证到算术；类型因子表自设 | 真实现，但「已运行小时→年」基准错配（见 N322） |

**每页结论（默认态）**

- `detector-aging-2`：默认 0.4MPa / 38% / 3% 三项全合格，综合「✅ 合格」，判定与阈值一致；属纯阈值判定、不做任何运算，也无「请输入」空态，清空后 ≤ 项按 0 判合格。
- `detector-composition-1`：默认 96% / 97% / 88 分全合格，正确；阈值与正文示例一致，但清空后三项按 0 计算直接判「不合格」，未区分「未输入」。
- `detector-composition-aging`：默认 88% / 82% / 96% 对 85 / 80 / 95 全合格，正确；与同族另两页仅阈值不同。
- `detector-length-lifespan`：默认 550N / 1.5% / 6 全合格，正确；但「≤±2%」被实现成单侧 `val<=2`，输入 −1.5%（或 −10%）同样判合格。
- `detector-water-pressure`：默认 99.5% / 35min / 0.005% 全合格，正确；水压项只比保压分钟数，页面引据表里的「试验压力 ≥1.5 倍设计压力」无对应输入与判定。
- `detector-lifespan`：默认 车刀/硬质合金/0.1mm/500 次 → 总寿命 2000、剩余 1500、磨损 33%、「继续使用」，与算例一致；磨损量与剩余寿命互不参与彼此判定。
- `estimate-36`：默认 193nm / NA1.35 / k1 0.25 → 分辨率 R=35.74nm 正确；焦深显示「±52.9nm、总焦深 105.9nm」，而本页公式写 `DOF=k2λ/NA²`（=52.9nm，总焦深口径应为 ±52.9 / 105.9 之一，二者混用）。
- `frequency-15`：默认 20kHz / 25μm / 10mm / 15N / 玻璃 → v=3141.59mm/s、a≈40243g、I≈730.35W/cm²、P≈573.4W、MRR≈340.9mm³/min「高效」，与页面公式逐项一致（MRR 量级偏高但属其经验式）；清空静压力 F 仍算出 MRR=0 并给「极低效」。
- `jiguangrongfuhoudujisuan`：默认 15g/min / 480mm/min / 2000W / 光斑 3mm / 效率 85% / ρ7.85 / 搭接 30% → 单位长度质量 0.02656g/mm、A=3.38mm²、宽 3.60mm、高 1.27mm、步距 2.52mm、沉积 12.75g/min，单位链正确。
- `lifespan-10`：默认 碳钢 / 60℃ / 50MPa / 轻度腐蚀 / 4000h → 回收分 89、寿命 10.2 年、综合 60 分 B 级，四因子与公式逐项吻合，默认态自洽。
- `lifespan-corrosion`：默认 0.1mm/年 / 10mm / 裕量 2mm / 0 年 / 常规大气 → 总寿命 80.0 年、剩余 80.0 年、周期 26.7 年、「寿命充裕」，算术正确；但参考标尺把 0–1 年标成「已超寿命」，且 5 年以上统一「寿命正常」，与文案「充裕」档不对应。
- `lifespan-wear-2`：默认 0.05mm/年 / 1.5mm / 16h/天 / 0h / 磨粒 → 修正速率 0.0333mm/年、总寿命 45 年、剩余 45 年、周期 15 年、「磨损轻微」，算术与公式一致；「已运行小时」换算成年的分母用 8760，与「日运行 16h」的折算口径不闭合。

**问题清单**

| 页面 | 问题（tools/general/<slug>.html:NN） | 编号 |
|---|---|---|
| detector-length-lifespan | **【高】**「长度偏差 ≤±2%」只判上界：`stdItems` 写 `op:"<=",threshold:2`（`:216`），比较式 `pass=val<=item.threshold`（`:224`），未取绝对值；输入 −1.5%（短 1.5%，合格）与 −10%（短 10%，严重超差）都被判「合格」并计入综合合格。同页 `:222` 又把空值 `parseFloat(...)||0` 当 0，清空后该行显示「0% 合格」。 | 12-N321 |
| lifespan-wear-2 | **【高】**时间基准错配导致已磨损量与剩余寿命整体失真：`adjRate` 已按 `日运行/24` 折算为「日历年磨损」（`:218-220`），但已磨损 `worn=adjRate*(used/8760)`（`:224`）、剩余 `remainLife=totalLife-used/8760`（`:226`）仍把「实际运行小时」当 24h/年÷8760；16h/天工况下 1 个日历年（5840h）只被算成 0.667 年，已磨损少算 1.5 倍、剩余寿命偏乐观 1.5 倍（8h/天时为 3 倍）。默认值 used=0 掩盖了该偏差。 | 12-N322 |
| detector-aging-2、detector-composition-1、detector-composition-aging、detector-length-lifespan、detector-water-pressure、detector-lifespan | **【②承诺未实现】** 6 页 `formula-desc` 均为同一句模板残留：「本工具用于检测…服务的**合法性校验**，依据对应数据格式与**语法规范**实时检查并定位错误」（对应行 `:125`×5、`detector-lifespan:126`）。页面实际只做 3 个数值与固定阈值的大小比较（或刀具寿命乘算），既无任何格式/语法校验，也不产出「检测报告」；各页 meta 与结果文案还统一称「检测报告可用于质量验收」，与「判定器」实质不符。 | 12-N323 |
| detector-water-pressure | **【②承诺未实现】** 标题与引据表宣称「水压试验 试验压力 ≥ 1.5 倍设计压力」（`:194`），但页面只有「水压保压时间 (min)」一个输入、只判 `≥30min`（`:216`），没有设计压力/试验压力输入，也未做 1.5 倍比值校验；即「水压」维度只验证了时长，未验证承压。 | 12-N324 |
| estimate-36 | **【中】**焦深口径自相矛盾、结果翻倍：公式框写 `DOF = k2 × λ / NA²`（`:128`），代码同时算 `halfDof=k2*λ/NA²`（`:204`）与 `dof=2*k2*λ/NA²`（`:203`），结果卡把 `halfDof` 标成「± 焦深」、`dof` 标成「总焦深」（`:210-211`），默认输出 ±52.9nm / 总 105.9nm，相对本页公式（52.9nm）放大了 2 倍；另 `:195-198` 只校验波长/NA>0，k1、k2 的 min 属性拦不住键入负值，负 k1 会直接输出负分辨率。 | 12-N325 |
| frequency-15 | **【中】**静压力 F 缺拦截却仍出评级：`:203` 把四个数字输入都标红并置 `valid=false`，但 `calc` 的早退条件只查 `f<=0||A<=0||D<=0`（`:216`），F 为空时按 0 继续算 `mrr`（`:235`），落入 `mrr>0.1` 之外显示「极低效」（`:241`）；用户看到红框却得到「加工效率极低」的错误结论，且「四个数字输入非数标红」的承诺与「仅三项报错」不一致。 | 12-N326 |
| jiguangrongfuhoudujisuan | **【中】**百分比输入超范围未拦截，直接产出物理上不可能的结果：送粉效率、搭接率只有 `max="100"`/`max="90"` 属性（`:136`、`:138`），键入 150% 时 `eff=150` 参与 `massPerLen`（`:203`）使截面积虚高 1.5 倍，`ov=150` 使 `step=width*(1-ov/100)` 得负值（默认宽 3.6 → −1.80mm，`:208`）；`readInputs`（`:191-196`）只判非数，不判上下界。 | 12-N327 |
| lifespan-corrosion | **【中】**参考标尺与判定文案口径错位：文案阈值是 `remainLife<=0` 超命、`<2` 极短、`<5` 有限、`<10` 正常、其余充裕（`:221-225`），但 `refBar` 分带写成 0–1「已超寿命」、1–2「剩余极短」、2–5「剩余有限」、5+「寿命正常」（`:238`）；默认 80 年被标为「寿命正常」而文案为「寿命充裕」，0.8 年被标为「已超寿命」而文案为「剩余寿命极短」，且 10 年档在标尺上不存在。 | 12-N328 |
| detector-aging-2 | **【中】**老化质量变化率只看上界、不看绝对值：`stdItems` 项 `op:"<=",threshold:5`（`:216`），输入 −10%（增重/异常挥发）时 0 比较通过判「合格」，而「质量变化率 ≤5%」按标准应取质量变化量的绝对值；负值区间无任何提示。 | 12-N329 |
| detector-lifespan | **【中】**剩余寿命与磨损量两条口径互不相干：`remain=Math.max(0,Math.round(maxLife-uses))`（`:226`）完全不含 `wear`，故 0.1mm 磨损 + 1900 次（剩 100）仍「继续使用」、而 0.01mm 磨损 + 2001 次即「报废」；另 `wearPct=wear/0.3*100`（`:227`）对负磨损输出负百分比（如 −33%）并仍判「继续使用」，`:219` 无 `<0` 校验。 | 12-N330 |
| detector-aging-2、detector-composition-1、detector-composition-aging、detector-length-lifespan、detector-water-pressure | **【中】**5 页均无「空输入」态，`parseFloat(value)||0`（各页 `:222`）把空值当 0 参与判定：三页 ≥ 型（aging 的压缩/回弹、composition 三项、composition-aging 三项）全空即输出「❌ 综合判定：不合格 0 / 0 / 0」；两页 ≤ 型（aging 的老化变化率、water-pressure 的泄漏率）空值显示「0 合格」。点「重置」后页面立刻给出上述结论，未提示「请先输入实测值」。 | 12-N331 |

**统计**

- 审计页数：12（`tools/general/` 指定 12 页，只读；`detector-*` 6 页为同模板派生）。
- 新增条数：11 条，编号 12-N321–12-N331（高 2 / 中 7 / 承诺未实现 2 / 安全 0）。
- 高优 2 条：N321（「±2%」缺绝对值，−10% 偏差判合格）、N322（wear 页小时→年基准错配，剩余寿命虚高 1.5–3 倍）。
- 承诺未实现 2 条：N323（6 页模板残留「格式/语法合法性校验」+「检测报告可用于验收」）、N324（水压页未实现 1.5 倍设计压力判定）。
- 中优 7 条：N325（DOF 翻倍+负 k1/k2 未校验）、N326（F 空值仍出「极低效」）、N327（效率/搭接率超出 0–100% 未拦）、N328（寿命标尺与文案档位错位）、N329（老化变化率缺绝对值）、N330（剩余寿命只用次数+负磨损）、N331（5 页空输入按 0 下结论）。
- 真实现且默认自洽（无问题）：`lifespan-10`（四因子加权默认 60 分 B 级自洽）；`detector-composition-1` / `detector-composition-aging` 的默认判定亦正确（问题只在空态与模板文案）。
- 「同类唯一」差异：唯一带查表寿命乘算的是 `detector-lifespan`（baseLife×matFactor）；唯一带材料参数表的综合评分是 `lifespan-10`；唯一做「百分比查表 + 质量守恒」双层换算的是 `jiguangrongfuhoudujisuan`（其余均为单式除乘）；唯一提供参考区间标尺（`refBar`）的 3 页分别是 `lifespan-10` / `lifespan-corrosion` / `lifespan-wear-2`。
- 单位/时区/默认值：12 页均不使用日期/时区，无 UTC 与本地时间混淆风险（历史记录仅存 `toLocaleString` 文本）；单位均在 label 标注（nm/kHz/μm/mm/N/g·min⁻¹/mm·年⁻¹/h），未发现量纲写错；`frequency-15` 的 kHz 与 Hz、`estimate-36` 的 nm 与 μm 在代码内显式换算，口径正确。
- 表取值/寿命倍率：`detector-lifespan` 的 `matFactor`（HSS 0.5 / 陶瓷 1.5 / CBN 2.5 / PCD 3.0）与 `lifespan-wear-2` 的 `typeData.factor`（磨粒 1.0 / 粘着 0.8 / 疲劳 1.2 / 腐蚀 1.5）均为无出处的自设经验值；后者把「粘着磨损」定为比「磨粒磨损」更慢（0.8 < 1.0），与常见磨损失效排序存疑，但因页面已注明「加速因子」，本次只按「表值×算术」口径核验，不计为算错。
- 安全条目：0 条 —— 12 页未发现 `eval` / `new Function` / `document.write` / `allow-same-origin` / 明文存密 / 向第三方回传输入；用户输入仅作为数值参与运算后拼入固定文案，历史记录一律经 `ToolBox.escHtml` 转义，持久化仅用 `localStorage`。页头沿用的 `bytegoofy`（TTZZ）第三方脚本为全站模板既有项，非本族新增，不单独计条。
- 局限：仅逐行读源码 + 手算复算；未开浏览器、未跑 `_build.py`/`run_gates.py`/`_test_static.py`、未做 git 或线上验证；英文态/繁体页/移动端未实测，默认态结论均按代码推演而非真机截图。

### 2026-11-06 租赁、橡胶及安全工具静态续审

- `safety/manager`（高风险）：固定明文 `TB_VAULT_VERIFY_v1` 用重复主密码字节 XOR 后 Base64 存储（`:258`、`:264-269`、`:319-327`）；备份同时导出验证值及同密钥加密的口令库（`:429-432`）。拿到本机存储或备份者可用已知明文恢复至少验证串长度内的重复密钥流，短主密码尤其容易完整恢复；该方案并非安全加密。页面虽注明基础混淆（`:248`），仍宣称用于保管口令；应优先停用实际密码并由用户迁移、轮换，方案需使用带随机盐的密码派生与认证加密。这里是静态分析，未读取任何真实用户数据。
- 同页账号只在可见文本处转义，却把原始账号插入双引号包围的内联 `onclick`（`:415-420`），仅替换单引号而不转义 HTML 属性；含双引号的账号可破坏属性并形成注入点。明文 CSV 拼接网站、账号、密码、备注后赋给 `innerHTML`（`:435-452`），含 HTML 的条目也可被解析；未执行注入。
- `safety/ppe-replacement`：日期输入缺 `onchange`（`:155-160`），预览只由周期或类型变更触发（`:266-275`）。修改日期后预览仍显示旧日期；添加后清空日期也未隐藏预览（`:291-307`）。名称虽用于正文时转义，却未经 HTML 属性转义地嵌入删除按钮（`:335`），双引号可破坏属性，属静态注入点。
- `safety/reminder-cycle-protection`：周期读取 `parseInt(...) || 0`，只校验日期（`:438-445`），状态函数将负周期与零都当作「按需检查」（`:385-387`、`:402-404`）。负数可让本应按期更换的用品不出现到期提醒；按需的合法零周期应保留，负值需单独拒绝。
- `rubber/hardness-calc`：空硬度由 `|| 0` 当作零继续给出等级及模量（`:256-260`、`:304-311`）；100 HA 会除以零，结果被替换为破折号但复制函数独立输出 `Infinity MPa`（`:311-320`、`:323-335`）。
- `rental/reminder-4`：日期字符串经 `new Date(dateStr)` 按 UTC 解析，再按本地时区截断（`:280-285`）；UTC 负偏移地区会提前一天计算到期。`safety/self-test` 的开始、选答、上一题和评分路径已读（`:182-246`），题库及法规准确性未作专业核验。
- 本批仅按当前源码推演，未运行浏览器或注入；安全防护、更换周期及法规需专业复核。
