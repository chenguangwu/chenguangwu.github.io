# G04 · verify 用例与判别力债务（全站质量基建）

## 现状基线（2026-10-25）
- 判别力：7731 用例全绿（逃生项 0）；false-pass 弱用例 no_inputs=10 / all_default=4（=基线）。
- 本轮已修 6 组失效用例（口径同步）、1 个判别器实锤逃生项（wells「高度」）、删除 1 条模板串坏用例（beer-gravity）。

## 遗留问题
### P1. beer-gravity 用例缺失
- 描述：坏用例已删，页 OG 公式已修（×2.20462）但无 verify 覆盖；麦芽行为动态 id（malt-wt-N），stub 注入不可靠。
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
