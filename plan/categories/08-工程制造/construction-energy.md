# 土木/能源 · tools/{civil,construction,structural,energy,fire-rescue,safety,urban,bridge,road,tunnel,architecture}（~200 页）

## 已知问题
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

## 2026-11-03 第一轮抽样补充

### 地基承载力校验与旧复制结果不一致（高，确认源码缺陷）
- 问题与证据：`tools/civil/dijichengzailijisuan.html:159-179,192-195` 对负黏聚力和负摩擦角标红，但主退出条件不含二者，仍继续计算。有效参数 c=15、φ=0、γ=18、B=2、Df=1.5、K=2 得 52.05 kPa；随后清空 B，主结果提示错误但 `lastResult` 未清空，复制仍使用旧值。
- 影响：`tools/civil/dijichengzailijisuan.html`，非法工况仍出结果、错误状态可能复制旧设计数据。
- 方案：统一校验条件并同步清空或禁用旧复制结果；提供工况历史并排对比时明确模型和适用条件。

### 风电功率的零 Cp 被默认为 0.4（高，确认源码缺陷）
- 问题与证据：`tools/energy/wind-power-estimator.html:269-281,295-307` 使用 `parseFloat(...) || 0.4`，用户输入 Cp=0 被代入 0.4；风速 12 m/s、半径 40 m、密度 1.225 kg/m³ 时页面按约 2.128 MW 输出，而公式按 Cp=0 应为 0。
- 影响：`tools/energy/wind-power-estimator.html`，结果与输入不符。
- 方案：区分零、空值与非法输入，显示实际采用的参数；年发电量明确容量系数与功率基准假设，可允许用户设置容量系数并对照工况。

### 覆盖
- 本轮抽查上述 2 页，仅源码及算术推导，未进行真实浏览器、专业标准及线上验证；其余页面未逐页覆盖。
