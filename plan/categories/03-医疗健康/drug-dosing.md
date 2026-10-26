# 医疗 · 药物剂量类（health/medical/clinical-nursing 剂量页 ~40 页）

## 已知问题
## 功能缺陷
- 儿童剂量页均无「年龄→体重默认填充」（WHO 中位体重表，静态可行）。
- 无「肝肾功能调整提示」（剂量页联动 eGFR 结果给出减量建议文案）。

## 优化点
- S8 空态教育化最适合本类：每个输入框 placeholder 给「典型值+范围」。
- 药品库数据集中 json 化（当前散在页内 JS），便于审校与后续扩充。

## 受影响范围
- tools/health/（child-medication-dose/weight-dosage 等 40 页）、tools/medical/dosage-calculator 系、tools/healthcare/（parkland/ibw 等）、tools/clinical-nursing/ 输液类（~40 页合计）

## 进度
- 🟡 进行中（2026-10-26 批次 03-2）：两条功能缺陷已在 2 个代表页落地
  - `health/child-medication-dose`：新增「同年龄参考体重（WHO 生长标准 P50，0–18 岁男/女）」+ 输入值与中位体重偏差百分比；
    新增「肝肾功能减量提示」（两 select：肾功能 Ccr 四级 / 肝功能 Child-Pugh 四级），8 种药标注主要清除途径（肝/肾/局部肠道），
    药物参考表新增「主要清除途径」列。
  - `medical/dosage-calculator`：同样两套能力接入；儿童（≤18 岁）显示参考体重核对并**偏差 >40% 时红字提示核对单位（kg/斤）**；
    15 种药按清除途径给出肝/肾分级减量建议（阿莫西林/头孢氨苄/万古霉素→肾，对乙酰氨基酚/布洛芬/苯妥英钠等→肝，头孢曲松/环磷酰胺→肝+肾）。
  - 数据源：WHO weight-for-age P50（0–18 岁）；清除途径按各药说明书主要消除途径归类，提示文案统一附「以说明书与药师核定为准」。
- 🟢 批次 03-47（2026-10-26 · 剂量页模板铺开首批续）：`healthcare/antipyretic-dose`：
  ① 年龄（0–18）+ 性别输入 + WHO P50 中位体重提示（refWeightBox，男/女分表线性插值）；② calc 内输出「同年龄中位体重 X kg，当前体重偏差 Y%」，偏差 >40% 红字提示核对 kg/斤；③ 肝功能四档 select（正常/Child-Pugh A/B/C）→ C 级红字「对乙酰氨基酚以肝清除为主，应避免使用」、B 级黄字减量提示。
  **两坑**：① refWeightBox 静态提示「16.3 kg」含子串「6.3」，老用例裸数字锚被误伤 → 锚改「单次药量： 6.3」派生串；② 在 weight/dose 间插入新输入会打断老用例的「值序列」锚（42\n42\n42）→ 同批改锚。verify 74/74、判别器 0 逃生。
- 🟢 批次 03-48（2026-10-26 · 剂量页模板铺开二）：`healthcare/weight-dosage`：
  年龄/性别输入（置于 freq 之后）+ WHO P50 中位体重提示 + calc 内偏差% + >40% 红字核对 kg/斤。老用例值序列锚「42\n42\n42\n日剂量： 1764」同批改「日剂量： 1764」派生串；新增偏差强用例（weight=18 → 10%）。verify 75/75、判别器 0 逃生、门禁 218/218。
- 🟢 批次 03-49（2026-10-26 · S8 空态教育化首批）：3 页 13 处输入框补 placeholder（典型值+范围）：
  `medical/calculator-calc-infusion`（4）、`medical/convert-time-infusion`（3）、`health/insulin-dose`（6）。
  只加 placeholder 不改 value ⇒ calc 与 verify 用例零影响；medical 17/17、health 73/73、门禁 218/218。
- 🟢 批次 03-72（2026-10-26 · S8 placeholder 收口）：最后一处缺 placeholder 输入框 `medical/calculator-calc-2` 的 age 补「如 6（选填，0–18）」。
  placeholder-only 改动不改 value ⇒ calc 与 verify 用例零影响（medical 17/17）。**S8 空态教育化至此全类收口**。
- 🔴 待续：剩余剂量页（clinical-nursing 输液类等）按同一模板铺开——已扫：clinical-nursing 输液类页无年龄输入（评分/操作型为主），
  health/healthcare/medical/pediatrics 含「年龄+剂量」且未铺 WHO 中位体重的页仅剩 `health/body-surface-area`（非剂量页），
  「同年龄参考体重」模板可铺页已全部铺完（03-2/47/48 三批）；
  「药品库 json 化（散在页内 JS → 集中 json）」涉及 40 页大重构且 fetch json 在 verify harness 不可达，暂缓待裁。
