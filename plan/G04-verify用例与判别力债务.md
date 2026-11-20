# G04 · verify 用例与判别力债务（全站质量基建）

> **2026-11-21 全量收口核验**：本文件所列问题已处理完毕，仅作历史档案；当前代码由 210 个 verify 全绿、4,426 页构建、12,102 段内联脚本 0 语法错误及全量门禁覆盖。

## 现状基线（2026-10-25）
- 判别力：7731 用例全绿（逃生项 0）；false-pass 弱用例 no_inputs=10 / all_default=4（=基线）。

## 遗留问题
### P1. beer-gravity 用例缺失 —— 已修复并复核（2026-11-18）
- 原问题：麦芽行为动态 id，原 inputs 注入不可靠；已有测试曾把错误 FG 和 ABV 作为预期。
- 当前 `scripts/verify_food_calc.js` 用 clicks 设置非默认麦芽，分别验证 8 kg、75% 时 FG 1.023 和 ABV 9.1%，以及 10 kg、23 L、50% 时 FG 1.048；拒绝旧错误值 0.931 和 21.3%。计算关系为 FG = OG − (OG − 1) × 表观发酵度。
- 2026-11-18 复测 `node scripts/verify_food_calc.js`：35/35；该结果覆盖上述案例，不代表覆盖所有原料和输入。
- 受影响：scripts/verify_food_calc.js、tools/food/beer-gravity-estimator.html

### P2. 动态行页面 stub 注入盲区（系统性）
- 描述：行由 JS 渲染、id 带 index（malt-wt-N、detector-time 日志行）的页面，inputs 注入时行未建 → 回显默认值成「弱命中」。
- 方案：harness 支持「先 clicks 建行再 inputs」两段式；或此类页统一提供带种子行。涉及 verify_it_calc.js 框架改造。
- 受影响：verify 框架 + food/beer-gravity、admin/detector-time、paper 部分页

### P3. 弱用例存量 14 条（no_inputs 10 / all_default 4）
- 方案：逐条改造为真实注入（历史基线只许降不许升，改一条降一条）。
- 受影响：scripts/falsepass_baseline.json 登记页

### P4. 判别器对「分级词锚点」误报已解，但「纯数值锚」仍有撞默认风险
- 方案：新增用例锚点时跑双态核验（注入态命中/默认态失配）——纪律已在 baseline note，建议固化成脚本 `scripts/check_anchor_two_state.js`（待开发）。
- 受影响：全部 verify_*.js

## 进度（2026-11-20 收口）
- 🟢 P1 ✅、P2 ✅、P3 ✅（存量已从 14 降到 11 且全部为结构性不可注入，ref 写明理由；基线 `no_inputs` 10→7 已收紧）、P4 ✅
- P2 ✅：harness 已支持 `clicks` 两段式（`verify_it_calc.js` 先注入 `inputs`，再按序执行
  `clicks`，可在 clicks 内建行动态行后赋值/触发 calc；动态 id 由 `lib_dynamic_defaults.js`
  的 `isDynamicId` 放行）。beer-gravity 等动态行页已用该路径通过。
- P3 ✅：`node scripts/selfcheck_false_pass.js scripts` 实测 no_inputs=7 / all_default=4；
  余 11 条均已在 ref 注明「结构性不可注入/输入回显/常量输出」，不制造逃生。
  `WEAK_LIST=1` 可逐条列出（本批新增，供后续继续降基线）。
- P4 ✅：双态核验已固化为 `selfcheck_false_pass.js --exec`（无参兜底命中即记 `default-hit`
  risk）；锚点纪律同时写进 baseline `_comment`（含「默认态同值巧合」「expect 为 OR」等坑）。

## 2026-11-03 审计补充（只读审计）

### G04-A ✅ 已关闭（2026-11-20）：用例总数口径统一
- 结论：旧 `total_cases=4925` 是早期「截断采集」口径；当前 `selfcheck_false_pass.js` 全站实测
  `checked=12446`（207 文件、0 skip）。已把 baseline 的 `total_cases` 同步为 12446 并在
  `_comment` 记录口径来源；该字段仅作记录、不参与门禁判定（门禁判 `no_inputs`/`all_default` 棘轮）。

### G04-B ✅ 已关闭（2026-11-20）：feat(preset) 未破坏默认态锚
- 抽样 10 个近期 `feat(preset)` 分类（startup / edu2 / medical2 / pediatrics / ceramics /
  martial / legal / image / encode / safety）逐个跑 verify，全部全绿（17/17、29/29、5/5、41/41、
  5/5、11/11、112/112、42/42、73/73、14/14）；全站判别力由门禁 `discriminate_check` 每轮覆盖，
  若预设回调改变了默认态输出导致锚点失效，会以「逃生项」形式直接判红。
### 复核纪律（第二轮起执行）
- 「已修复」条目不采信提交说明，按可观察证据复核：① 源码关键串/值确已变更；② 页面默认态与注入态行为符合预期；③ 对应 `scripts/verify_*` 用例通过且非逃生；④ 若改动进入构建产物，`json/tools.json` / `sw.js` 版本戳已刷新；⑤ 线上抽样（部署后）关键内容命中。
- 复核不通过 → 在本文件与对应分类文件重新打开，写明失败证据与复现方式。


## 2026-11-05 空态重扫后的用例口径补充

- **可交换输入会让「互异值」失效**：`tax/excise-tax` 的 T = p×q×r 对任意字段置换结果不变，仅把 42 改成 7/250/0.15 仍测不出「值↔字段」错配。解法是把结果与分项（计税金额=p×q、综合税率=r%）合并成**一条** expect。
- **expect 数组是「任一命中即通过」**（OR），不是全部命中：把多个分项拆成多条 expect 等于没加约束，必须拼成单条串。
- **守卫顺序漂移在计算上不可见**：探针按 `getEl(id)` 注入，`__tbReq` 的 `getElementById` 顺序只改快照拼接顺序，不改取值；验证「值错配」要用**字段间轮转注入**（12/12 变红），不能用「调换守卫顺序」。
- 本轮基线调整：`discriminate_baseline.json` 的 `skipped 54→51`、`checked 9113`（3 条原不可判用例现已可判）。
