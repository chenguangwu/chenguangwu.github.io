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
