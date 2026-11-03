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
