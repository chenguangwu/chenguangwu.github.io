# 验证优先清理归档（仅含已验证修复记录）

来源：05-生活消费/sports-fitness.md

- **处置（2026-11-06 A批·真修复）**：已修复。`tools/fitness/calc.html` `calc()` 加年龄/身高/体重范围校验（10–100/100–230/30–300），越界即 return 提示、不再按 0 代入渲染负热量。verify 因 `calc()` 有 1s 节流、harness 同步采集拿不到拦截提示（盲区），改走 `scripts/_verify_fitness_batch_a.mjs` 运行时断言（5/5，HEAD 回退 2/5 证有效）。移交 `plan/已修复/2026-11-06-SF-N7-N12-体育健身A.md`。


---

## 2026-11-11 第二批追加（05-生活消费/sports-fitness.md 的 INLINE/FEATURE 验证记录）

- ✅ 配速页「比赛目标反推」已落地（2026-10-27）：fitness/pace-calculator 新增「🎯 目标完赛时间反推」card（goalDist 距离按钮 + goalH/M/S 目标时间 → 所需平均配速、等效速度、与目标配速输入对比（可慢/需提速 + 百分比）、五等分分段达成表），分段沿用既有策略模型（even/positive/negative，各段配速均值 = 所需平均配速 ⇒ 总时间守恒）；__pcIsEn 三重回退双语。顺带修 splitDist 按钮误绑 selectRace（点分段区距离只改主区、不重算分段表）→ 改绑 selectSplitRace，并把 quickDist/splitDist/goalDist 三处渲染改为直接赋值（原 `innerHTML + html` 追加写法会在 setUnit 切换时重复堆叠按钮）。verify fitness 78→80（+2：4:00:00 主用例、负分段分支）；判别器 79 检/逃生 0；EN --container=paceGoalTable BAD=0。

---

- **处置（2026-11-06 复核）**：源码已修复（公式框与实现均为公制常数，男 +30.30、女 −104.91）。属审计快照（2026-11-04）陈旧条目，仅复核锁定，未改源码。英文 i18n map 旧常数 +36.76/−78.387 残留已清理（`i18n/tools/en/fitness/calc-3.json`，残留 0、JSON 有效）。

---

- **处置（2026-11-06 复核）**：源码已修复（`waist<=neck` 前置拦截 + `Number.isFinite` 守卫）。属审计快照陈旧条目，复核锁定，未改源码。

---

- **处置（2026-11-06 复核）**：源码已修复（`/25` 已改为 `/6`）。属审计快照陈旧条目，复核锁定，未改源码。

---

- **处置（2026-11-06 复核）**：源码已修复（`减脂保肌` 与 `增肌` 已设独立附加值）。属审计快照陈旧条目，复核锁定，未改源码。
