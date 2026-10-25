# 土木/能源 · tools/{civil,construction,structural,energy,fire-rescue,safety,urban,bridge,road,tunnel,architecture}（~200 页）

## 已知问题
## 功能缺陷
- 混凝土配比页缺「强度等级↔水灰比对照」联动表。
- 消防页缺「疏散宽度计算」（商店/观众厅指标）高频项。

## 优化点
- S7 引据：GB 50010/50016 标准徽标。
- S3 分步：土压力/承载力分步图解。

## 受影响范围
- tools/civil/、tools/construction/、tools/structural/、tools/energy/（41）、tools/fire-rescue/、tools/safety/、tools/urban/、tools/bridge/、tools/road/、tools/tunnel/（~200 页）

## 进度
- 🔴 待开发

### E2. bridge/load-calc 车道荷载 Pk 内插基线用 270 kN，L<50m 段高估（批20）
- 描述：页面自称按 JTG D60 公路-Ⅰ/Ⅱ级车道荷载（qk=10.5 kN/m ✓），但集中荷载 Pk 用 `L≤5m→270、L≥50m→360` 线性内插；JTG D60-2015 表 4.3.1-2 为 **L≤5m→180 kN、L≥50m→360 kN**。L<50m 段 Pk 系统性高估（5m 处 1.5 倍、27.5m 处 315 vs 应 270）。
- 方案：基线改 180：`L<=5→180, L>=50→360, else 180+(360-180)*(L-5)/45`；Ⅱ级仍用 ×factor；公式框/深度解读同步（G03）。
- 受影响：tools/bridge/load-calc.html
- 置信度：高（JTG D60-2015 明表值 180~360）
