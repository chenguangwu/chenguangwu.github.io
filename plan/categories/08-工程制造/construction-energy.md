# 土木/能源 · tools/{civil,construction,structural,energy,fire-rescue,safety,urban,bridge,road,tunnel,architecture}（~200 页）

## 功能缺陷
- 混凝土配比页缺「强度等级↔水灰比对照」联动表。
- 消防页缺「疏散宽度计算」（商店/观众厅指标）高频项。

## 优化点
- S7 引据：GB 50010/50016 标准徽标。→ civil 24 页全量收口（批34/62），structural 13 页（批35），energy 14 页（批57），construction 38 页全量收口（批66/67/68，GB 50010/JGJ 55/GB 50500-2013/JGJ 130-2011/GB 50009-2012 等）。本文件 S7 全部收口。
- S3 分步：土压力/承载力分步图解。

## 受影响范围
- tools/civil/、tools/construction/、tools/structural/、tools/energy/（41）、tools/fire-rescue/、tools/safety/、tools/urban/、tools/bridge/、tools/road/、tools/tunnel/（~200 页）

## 进度
- 🔴 待开发

### 留存优化
- 朗金页：补土压力沿深度折线图（标注 z0）与 φ/c 敏感性表；先修 φ 上限与预设再扩展。
- 简支梁页：增加「按 b×h 反算 I」或截面库选择；补充「自重是否已计入 q」的提示。
- 热泵页：补 SCOP/SEER 与部分负荷说明；对比区按模式切换基准；运行时长 0 的边界提示。
- 三相/功率因数：两页互加「线电压/相电压」「pf 上限」提示，避免同源输入口径混用。
- 回收期/LCOE：可把动态回收期、NPV/IRR 与折现敏感性作为可选扩展，不改变现有主结果。

### 续查覆盖
- 已覆盖 8 页：`tools/civil/active-earth-rankine.html`、`tools/civil/pile-capacity.html`、`tools/civil/beam-udl.html`、`tools/energy/heat-pump-cop.html`、`tools/energy/power-factor-calc.html`、`tools/energy/three-phase-power.html`、`tools/energy/energy-payback.html`、`tools/energy/lcoe.html`。
- 未覆盖：civil/energy 其余页面，以及 construction/structural/fire-rescue 等目录本批未逐页审计。
- 验证声明：仅源码阅读 + node 内存复算，未做真实浏览器、英文态（`?lang=en-US`）、移动端、门禁或线上验证；专业标准取值亦未逐条核对。第一轮与 CE-N1–N9 所列计算缺陷经源码复核均已修复，980 批整段删除；热泵公式框文案同步修正。
