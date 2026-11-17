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

### 年金期数 0 被静默改为 1（中，确认源码缺陷）
- 证据：`tools/audit/npv-discount.html:147-161,308-320,327-334` 年金模式初始 100、折现率 0%、每期 50、期数 0，`parseInt(...) || 1` 按 1 期输出 NPV -50，输入仍显示 0。
- 影响：`tools/audit/npv-discount.html`，输出依赖用户看不到的参数替换。
- 方案：明确校验正整数和上限，不把零或空改默认；导出初始投资、利率、期数及现金流明细。

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

### 12-K2 chemical/solution-concentration：深度解析宣称的「w%↔mol/L」跨换算无密度输入，示例无法复现（中，确认缺陷）
- 描述：深度解析把"给定密度与分子量，在 w% 与 mol/L 间换算"列为核心场景，并给出"输入 w%=10、密度 1.07 g/mL、M=58.44 → 约 1.83 mol/L"的算例；但页面四个模式（molar/mass/ppm/dilute）均无密度或质量分数联合输入，mass 模式只输出 `%` 与 `ppm`，molar 模式只接受溶质质量/摩尔质量/体积，用户无法在界面复现该算例。
- 证据：`tools/chemical/solution-concentration.html:209,213`（场景与算例）、`:274-296`（四个模式的输入项）、`:322-343`（mass 模式仅输出 %/质量比/ppm）。
- 复现：按算例只能分别算 10% 与 1.83 mol/L，页面没有任何"w% + 密度 + M"入口；node：1000×1.07×0.10/58.44 = 1.831 mol/L，说明示例数值本身正确、但功能缺失。
- 影响：简介/深度解析承诺的核心互算能力缺失，用户按示例找不到入口，也影响搜索词与内容一致性。
- 方案：新增"质量分数↔摩尔浓度"模式（输入 w%、密度 g/mL、摩尔质量），或把深度解析算例改写成页面可实现的两步（先算质量浓度 g/L，再除以 M）。

### 12-K11 transport/convert-volume-weight：缺实际重输入与计费重量输出，与标题/meta/引据表承诺不符（中，确认缺陷）
- 描述：标题、meta description、引据表与深度解析算例都承诺"实际重 vs 体积重，取较大者作为计费重量"，深度解析还给出"实重 8 kg → 计费重 12 kg"的算例；但页面只有长/宽/高/除数四个输入，`calc` 只算体积重（及 lb、6000 系数对照），没有实重输入，也没有 `max(实重, 体积重)` 结果。`formula-box` 末尾虽注明"本工具输出体积重"，但标题/meta/算例仍按"对比取大"宣传。
- 证据：`tools/transport/convert-volume-weight.html:10`（meta 承诺）、`:120-124`（四个输入与除数下拉）、`:150`（引据表 Chargeable=max）、`:169`（`calc` 仅输出体积重）、`:181`（公式框注明仅输出体积重）、`:209`（算例含实重 8 kg）。
- 复现：50×40×30 cm、系数 5000 → 12.00 kg；页面无法输入实重 8 kg，无法得到算例所写的计费重 12 kg，也无"计费重量"字段。
- 影响：工具名与搜索词承诺的核心对比功能缺失，用户按描述无法得到计费重量，只能自行再比大小。
- 方案：增加"实际重量 (kg)"输入，输出 `max(实重, 体积重)` 并同时列出 5000/6000 两系数的计费重；实重为空/负时报错；同步 meta 与公式说明。

- 本轮实读 8 页：`tools/chemical/solution-concentration.html`、`tools/mining/convert-grade-ore.html`、`tools/hvac/cooling-load.html`、`tools/paper/roll-length.html`、`tools/fire/hydrant-pressure.html`、`tools/gas/load-1.html`、`tools/security/flood-level.html`、`tools/transport/convert-volume-weight.html`；新增 11 条（高 1 / 中 9 / 低 1）；未覆盖：chemical、mining、hvac、paper、fire、gas、security、transport 各目录的其余页面，以及 dyeing、leather、safety、nutrition、usedcar、wedding、restaurant、elderly、procurement、cleaning 等长尾目录本轮未读。

## 2026-11-04 续查（并行批 L）

> 范围：本轮阅读 8 页——`tools/dyeing/calc-dosage-2.html`（dyeing）、`tools/leather/convert-area-weight.html`（leather）、`tools/safety/accident-stats.html`（safety）、`tools/nutrition/calorie-deficit.html`（nutrition）、`tools/usedcar/car-residual.html`（usedcar）、`tools/wedding/wedding-banquet.html`（wedding）、`tools/restaurant/safety-stock.html`（restaurant）、`tools/elderly/fall-risk.html`（elderly）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

### 12-L3 nutrition/calorie-deficit：减脂提示「300~500 千卡缺口」与页面自身目标区间不一致（中，确认缺陷）
- 描述：`lose` 目标按 TDEE 的 85%~90% 计算（缺口 10%~15%），提示文案却写「保持 300~500 千卡缺口」；默认参数下实际缺口仅约 217~325 千卡，文案与实际输出不符，且未随 TDEE 缩放。
- 证据：`tools/nutrition/calorie-deficit.html:240-243`（`:241-242` 区间、`:243` 提示），`:257-261`（输出）
- 复现：默认 男/28 岁/170 cm/65 kg/轻量活动 1.375（`:135` selected）→ BMR 1,577.5、TDEE 2,169、目标 `1844 ~ 1952` 千卡/天，实际缺口 217~325 千卡；提示仍为「300~500 千卡缺口，周减重约 0.25~0.5kg」。（node 复算）
- 影响：低 TDEE 人群按提示追求 300~500 缺口会落到目标区间之外；高 TDEE 人群则被提示低估，减脂速度预期错位。
- 方案：提示改为动态文案（如「当前缺口约 X 千卡/天，约合每周 Y kg」），或把目标改为「TDEE − 固定缺口」并同时给出百分比校验；补 1500/2500/3500 TDEE 三组用例。

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

### 12-L8 elderly/fall-risk：引据表 Morse「>45 高危」与本页 12 题 25 分制百分比分级不可对应（中，确认缺陷）
- 描述：页面自建 12 题问卷（环境 6 题各 0–2 分、身体 6 题最高 3 分），`maxScore` 实为 25，并按 `total/maxScore` 的 25%/50%/75% 分为低/中/高/极高；但「公式与标准引据」表却列「Morse 评分 / 条目加权求和 / Morse 2009」与「>45 高危」，该阈值在本页 0–25 分体系内永远无法达到，且分级名称（极高风险）也不属于 Morse 口径。
- 证据：`tools/elderly/fall-risk.html:204-211`（引据表），`:263-267`（`maxScore` 求和），`:308-313`（百分比分级）
- 复现：12 题全选最差 → 总分 25、风险占比 100%、判「极高风险」；按引据表「>45 高危」则 25 分连高危门槛都不到，两套口径互斥。（node 复算 maxScore=25）
- 影响：用户按引据表把得分与 Morse 阈值对照会得出相反结论；对外宣称 Morse 2009 但实际未采用其条目与权重，可信度受损。
- 方案：要么改为真正的 Morse 量表（6 项、0–15/0–20/0–25 权重、>45 高危），要么删掉 Morse 引用、改标「自建问卷（0–25 分，按百分比分级）」并给出分级依据；补全对/全错两组用例。

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

### 12-N173 gardening/soil-ph：调节剂用量固定不随差值缩放，差 1.5 个 pH 仍只给 100–300 g/m²（中，确认缺陷）
- 问题：深度解析 `:280` 承诺「按差值给调节剂与用量（升 1 单位约石灰粉 100-300 g/m²，降 1 单位约硫磺粉 100-200 g/m²）」，但 `ADJUSTERS` 每项 `dose` 是固定字符串（`:375-390`），`calc` 只把整表原样渲染（`:437-449`），没有任何乘 `diff` 的处理。
- 证据：`tools/gardening/soil-ph.html:280`、`:375-390`、`:437-449`
- 复现：蓝莓 4.5–5.5：实测 4.4（差 0.1）与实测 3.0（差 1.5）得到完全相同的「石灰粉 · 用量 100-300 g · 升 1 个 pH」清单；按承诺 1.5 单位应为 150–450 g/m²。
- 影响：`tools/gardening/soil-ph.html` 按页面表格 100–300 g 对应「升 1 个 pH」，差 1.5 个单位应给 150–450 g，页面只给 100–300 g（仅覆盖所需区间的约 2/3），用户按清单补一次仍差 0.5–1.0 个 pH，误判「已按工具加足」。
- 方案：结果区按 `diff` 计算建议区间（`dose×diff`）并显示「按差值 Z 个单位」，保留「分次、每次 ≤0.5–1.0」的提示；调酸同理乘硫磺粉 100–200 g。

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
