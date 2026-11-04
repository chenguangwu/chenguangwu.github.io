# G04 · verify 用例与判别力债务（全站质量基建）

## 现状基线（2026-10-25）
- 判别力：7731 用例全绿（逃生项 0）；false-pass 弱用例 no_inputs=10 / all_default=4（=基线）。

## 遗留问题
### P1. beer-gravity 用例缺失
- 描述：页 OG 公式无 verify 覆盖；麦芽行为动态 id（malt-wt-N），stub 注入不可靠。
- 方案：用 clicks 驱动（页面 window 导出的 addMalt/updateMaltWeight）重建用例；或为页面补静态汇总 id。
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

## 进度
- 🟡 规则固化完成；P1-P4 🔴 待开发

## 2026-11-03 审计补充（只读审计）

### 疑似待验证 G04-A：用例总数可能存在口径或时间差异（中）
- 两个数字对应不同时间点或集合的可能性尚未排除，不能单凭数字不同确认门禁错误。
- 问题：本文件「现状基线（2026-10-25）」写「7731 用例全绿」，但仓库基线文件 `scripts/falsepass_baseline.json` 的 `total_cases` 为 **4970**，两者相差 2761，无法判断哪一个可信。
- 证据：`plan/G04-verify用例与判别力债务.md:4`（7731）；`scripts/falsepass_baseline.json` 字段 `total_cases = 4970`；`scripts/verify_*_calc.js` 共 207 个文件、静态 `runCase(` 调用 209 处（循环展开后才会得到数千用例）。
- 影响：全站门禁口径；后续「用例只增不减」的历史基线不可判定。
- 方案：以实际运行 `run_gates.py` 输出为准重建 `total_cases`，并在本文件写「口径定义（是否为循环展开后的用例数、是否含逃生项）」，禁止再用两个数字并存。**本轮只读，未实际运行门禁。**

### 疑似待验证 G04-B：预设批可能未同步 verify 用例
- 问题：近期 107 个 `feat(preset)` 提交多为页面注入预设按钮（不改 calc），但部分提交描述含「回调改渲染」（如 `tcm-chemistry` 两批）。若预设值或回调改变了默认态输出，既有 verify 用例的「默认态失配」判别锚可能失效（变成逃生项）。
- 证据：`plan/categories/...` 与 git log 提交信息；未逐一比对 107 个提交的 `scripts/verify_*` 改动。
- 影响：分类级；需第二轮抽查。
- 方案：按分类抽样 10 个「回调改渲染」页面，运行 `selfcheck_false_pass` 与 `discriminate_check`（由修复方在可运行环境执行）；发现默认态命中即重写锚点。

### 复核纪律（第二轮起执行）
- 「已修复」条目不采信提交说明，按可观察证据复核：① 源码关键串/值确已变更；② 页面默认态与注入态行为符合预期；③ 对应 `scripts/verify_*` 用例通过且非逃生；④ 若改动进入构建产物，`json/tools.json` / `sw.js` 版本戳已刷新；⑤ 线上抽样（部署后）关键内容命中。
- 复核不通过 → 在本文件与对应分类文件重新打开，写明失败证据与复现方式。


## 2026-11-05 空态重扫后的用例口径补充

- **可交换输入会让「互异值」失效**：`tax/excise-tax` 的 T = p×q×r 对任意字段置换结果不变，仅把 42 改成 7/250/0.15 仍测不出「值↔字段」错配。解法是把结果与分项（计税金额=p×q、综合税率=r%）合并成**一条** expect。
- **expect 数组是「任一命中即通过」**（OR），不是全部命中：把多个分项拆成多条 expect 等于没加约束，必须拼成单条串。
- **守卫顺序漂移在计算上不可见**：探针按 `getEl(id)` 注入，`__tbReq` 的 `getElementById` 顺序只改快照拼接顺序，不改取值；验证「值错配」要用**字段间轮转注入**（12/12 变红），不能用「调换守卫顺序」。
- 本轮基线调整：`discriminate_baseline.json` 的 `skipped 54→51`、`checked 9113`（3 条原不可判用例现已可判）。
