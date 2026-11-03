# 运动/健身 · tools/{sports,fitness}（~116 页）

## 已知问题
## 功能缺陷
- ✅ 配速页「比赛目标反推」已落地（2026-10-27）：fitness/pace-calculator 新增「🎯 目标完赛时间反推」card（goalDist 距离按钮 + goalH/M/S 目标时间 → 所需平均配速、等效速度、与目标配速输入对比（可慢/需提速 + 百分比）、五等分分段达成表），分段沿用既有策略模型（even/positive/negative，各段配速均值 = 所需平均配速 ⇒ 总时间守恒）；__pcIsEn 三重回退双语。顺带修 splitDist 按钮误绑 selectRace（点分段区距离只改主区、不重算分段表）→ 改绑 selectSplitRace，并把 quickDist/splitDist/goalDist 三处渲染改为直接赋值（原 `innerHTML + html` 追加写法会在 setUnit 切换时重复堆叠按钮）。verify fitness 78→80（+2：4:00:00 主用例、负分段分支）；判别器 79 检/逃生 0；EN --container=paceGoalTable BAD=0。
- ✅ 1RM 百分比训练表（2026-10-26）：health/one-rep-max 加「💪 训练周期处方表」(programTable)，基于算出的 1RM 自动换算 5×5/3×5/3×8/4×10 等方案的实际负重区间（80-85%/75-80%/65-70%/60-65%），__T 双语；verify health +1、判别器 0 逃生。
- 无「训练负荷周报」（localStorage 聚合，G06-S5 联动）。

## 优化点
- ✅ S2 场景（2026-10-26）：macro-ratio 加 3 预设（增肌 70kg 重训 / 减脂 80kg 中度 / 维持 65kg 轻度，labelEn 双语）；pace-calculator 加 3 比赛目标预设（5km 破 25 / 10km 破 50 / 全马破 4，labelEn 双语）。verify fitness 72→78（6 条预设等价注入锚，probe 采集）；判别器逃生 1→修复（蛋白锚只依赖 weight 不判别，删除）→ 0；门禁 218/218。
- S4 分享卡：跑步成绩卡（社交传播最强的品类之一）。

## 受影响范围
- tools/sports/（77）、tools/fitness/（39）

## 进度
- 🟡 续批中（S2 场景、1RM 百分比训练表已落地；剩余：比赛目标反推 / 训练负荷周报 / S4 分享卡）

## 2026-11-03 第一轮抽样补充

### 配速分段表与总时间不守恒（高，确认函数缺陷）
- 问题与证据：`tools/sports/calculator-calc-time.html:277-325` 用当前位置配速乘累计距离；原函数内存执行 10 km、50 分钟、负分段 10%、爬升 0 时摘要 50:00，而终点行 45:00。
- 影响：`tools/sports/calculator-calc-time.html`，训练或比赛配速计划前后矛盾。
- 方案：先确定分段策略的精确定义，按距离积分或累加各段耗时，并确保最终时间与摘要一致；覆盖跨半程的分段。修复后可主动本地保存比赛目标和策略，比较本次与上次方案。

### 跑步整小时时被增加 30 分钟（高，确认函数缺陷）
- 问题与证据：`tools/fitness/running-calories.html:414-459` 的 `timeMin2` 使用 `parseInt(...) || 30`，合法 0 被代为 30；配速 6 分/km、1 小时 0 分钟时原函数得 90 分钟、15 km，应为 60 分钟、10 km。
- 影响：`tools/fitness/running-calories.html`，距离和热量估算被放大。
- 方案：区分空值和合法 0，验证 1:00、0:30 与空值。

### 覆盖与文档冲突
- 本次抽查上述 2 页，使用内存 DOM 桩，未实测浏览器或其他运动页。原进度仍列比赛目标反推待做，与上方已落地记录冲突；保留待独立复核。

## 2026-11-03 续查（并行批）：运动与健身

### SF-N1 心率区间倒挂（高，确认）
- 证据：`calc-heart-rate.html:189-202`。age=120、rest=120 → hrmax=100、hrr=−20，Zone1「110-108」；清空年龄仍按 0 出 220/143-158。
- 影响：反物理区间。方案：hrr≤0 停算提示，空值必填。

### SF-N2 BIA 极端值假结果（高，确认）
- 证据：`resistance.html:244-257`。age 未进公式（245 仅校验）；h=230、w=30、z=200 → FFM 171.6 钳成 28.5、体脂 5.0%。
- 影响：误判「必需脂肪」。方案：FFM>W 或 TBW/W>100% 判无效。

### SF-N3 训练容量自重与导出（中，确认）
- 证据：`training-volume.html:352` 仅 weight>0 可存，引体/俯卧撑填 0 无法保存；139 行「导出记录」实为 488-497 `copyText`；英文态 confirm/canvas 仍中文（287/414/468）。
- 影响：徒手训练被排除、导出名不副实。方案：weight=0 体重倍数、Blob 下载、canvas/confirm 走 i18n。

### SF-N4 攀岩 V 级只取首行（中，确认）
- 证据：`climbing-grade-converter.html:285-308`。V1 占 10/11（5.10c/5.10d）、V3 占 14/15；364-370 行 `break`：V1→5.10c、V3→5.11c。
- 影响：对照丢半档。方案：同 grade 聚合输出区间。

### SF-N5 步幅页默认 65kg 与零速热量（中，确认）
- 证据：`step-stride.html:319` `||65`，清空体重仍写「体重65kg」；cadence=0 速度 0、配速 `--`，但 330-337 行输出 2.3 kcal/min。
- 影响：默认体重冒充输入、静止计消耗。方案：空值停算热量、零速归零、范围对齐。

### SF-N6 12 分钟跑公式与阈值（中，确认）
- 证据：`vo2max-12min.html:347` 男女同为 `483/min+3.5`，T=12 均 43.8；322 行 `<10→10`，400 m 原式 −2.3 显示 10.0。
- 影响：性别无效、低值被当正常。方案：女性独立系数、低值提示、表头共用阈值。

### 留存优化（按页落点）
- `calc-heart-rate`：历史存完整五区＋本周区间卡。
- `resistance`：历史加趋势/测量标签。
- `training-volume`：动作周容量/PR；真 CSV；自重倍数。
- `step-stride`/`vo2max-12min`：存上次值对比，补配速-距离表。

### 续查覆盖
实读 `tools/fitness/`：calc-heart-rate、resistance、training-volume、step-stride、vo2max-12min；`tools/sports/`：climbing-grade-converter；另抽查 heart-rate-2。
