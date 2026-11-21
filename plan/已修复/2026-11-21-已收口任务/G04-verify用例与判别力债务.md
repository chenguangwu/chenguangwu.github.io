# G04 · verify 用例与判别力债务（全站质量基建）

> **2026-11-21 全量收口核验**：本文件所列问题已处理完毕，仅作历史档案；当前代码由 210 个 verify 全绿、4,426 页构建、12,102 段内联脚本 0 语法错误及全量门禁覆盖。

## 现状基线（2026-10-25）
- 判别力：7731 用例全绿（逃生项 0）；false-pass 弱用例 no_inputs=10 / all_default=4（=基线）。

## 遗留问题
### P2. 动态行页面 stub 注入盲区（系统性）
- 描述：行由 JS 渲染、id 带 index（malt-wt-N、detector-time 日志行）的页面，inputs 注入时行未建 → 回显默认值成「弱命中」。
- 方案：harness 支持「先 clicks 建行再 inputs」两段式；或此类页统一提供带种子行。涉及 verify_it_calc.js 框架改造。
- 受影响：verify 框架 + food/beer-gravity、admin/detector-time、paper 部分页

### P3. 弱用例存量 14 条（no_inputs 10 / all_default 4）
- 方案：逐条改造为真实注入（历史基线只许降不许升，改一条降一条）。
- 受影响：scripts/falsepass_baseline.json 登记页

### P4. 判别器对「分级词锚点」误报已解，但「纯数值锚」仍有撞默认风险
- 方案：新增用例锚点时跑双态核验（注入态命中/默认态失配）——纪律已由 `scripts/discriminate_check.js` 全量默认态快照 + `scripts/discriminate_baseline.json` 棘轮固化（2026-11-21 全量 12,440 检、逃生 1=基线、跳过 7=基线），不再单列脚本。
- 受影响：全部 verify_*.js

## 进度（2026-11-20 收口）
  `clicks`，可在 clicks 内建行动态行后赋值/触发 calc；动态 id 由 `lib_dynamic_defaults.js`
  的 `isDynamicId` 放行）。beer-gravity 等动态行页已用该路径通过。
  余 11 条均已在 ref 注明「结构性不可注入/输入回显/常量输出」，不制造逃生。
  `WEAK_LIST=1` 可逐条列出（本批新增，供后续继续降基线）。
  risk）；锚点纪律同时写进 baseline `_comment`（含「默认态同值巧合」「expect 为 OR」等坑）。

## 2026-11-03 审计补充（只读审计）

### 复核纪律（第二轮起执行）
- 「已修复」条目不采信提交说明，按可观察证据复核：① 源码关键串/值确已变更；② 页面默认态与注入态行为符合预期；③ 对应 `scripts/verify_*` 用例通过且非逃生；④ 若改动进入构建产物，`json/tools.json` / `sw.js` 版本戳已刷新；⑤ 线上抽样（部署后）关键内容命中。
- 复核不通过 → 在本文件与对应分类文件重新打开，写明失败证据与复现方式。


## 2026-11-05 空态重扫后的用例口径补充

- **可交换输入会让「互异值」失效**：`tax/excise-tax` 的 T = p×q×r 对任意字段置换结果不变，仅把 42 改成 7/250/0.15 仍测不出「值↔字段」错配。解法是把结果与分项（计税金额=p×q、综合税率=r%）合并成**一条** expect。
- **expect 数组是「任一命中即通过」**（OR），不是全部命中：把多个分项拆成多条 expect 等于没加约束，必须拼成单条串。
- **守卫顺序漂移在计算上不可见**：探针按 `getEl(id)` 注入，`__tbReq` 的 `getElementById` 顺序只改快照拼接顺序，不改取值；验证「值错配」要用**字段间轮转注入**（12/12 变红），不能用「调换守卫顺序」。
- 本轮基线调整：`discriminate_baseline.json` 的 `skipped 54→51`、`checked 9113`（3 条原不可判用例现已可判）。
