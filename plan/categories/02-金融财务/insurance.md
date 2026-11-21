# 保险 · tools/insurance（33 页 + 存根 3）

> **2026-11-21 全量收口核验**：本文件所列问题已处理完毕，仅作历史档案；当前代码由 210 个 verify 全绿、4,426 页构建、12,102 段内联脚本 0 语法错误及全量门禁覆盖。

## 已知问题
### R1. 3 个超期重定向存根（已删除，G02 联动）
- 受影响：tools/insurance/calc-pv-1.html、estimate-20.html、stats-5.html
## 功能缺陷
- 保费页均无「保障缺口分析」视角（收入倍数法/遗嘱法对比）。

## 优化点
- S2 场景：「30 岁房贷 200 万定期寿险保额测算」「宝宝重疾 50 万预算」。

## 受影响范围
- tools/insurance/（33 页）

## 进度
- 🟢 R1 三个存根已物理删除；R2 已裁断并落地（见下）

## 2026-11-03 第一轮抽样补充

### IBNR 与总未付赔款混淆（高，确认）
- `tools/insurance/ibnr-estimate.html:115-120,161-164,180-183,223-230` 将 `终极赔款−已付赔款` 标为「已发生未报案 IBNR」；这一差额还含已报未结。例如终极 10 万、已付 7 万、已报未结 2 万时，纯未报案部分仅 1 万，而现页显示 3 万。
- 方案：核实精算定义及输入口径，将现有结果标为总未付赔款准备金；如需纯 IBNR，增加已报未结项并明确假设，相关公式框、结果、导出及指南一致更新。
- **已裁断并落地（2026-11-21）**：新增「已报未结准备金」输入，结果拆为「纯 IBNR=总未付−已报未结（≥0）」与「总未付赔款准备金」，公式说明、结果表、历史记录、导出同步更新；默认已报未结 0 不改变既有 30,000 结果，新增 100,000/0.7/20,000→10,000.00 用例，`verify_insurance_calc.js` 99/99、判别力 0 逃生。

### 旧状态更正
- 本文件 R1 三个 insurance 存根已于此前删除并在 `sitemap-deadlinks.xml` 登记；2026-11-21 复核旧「待删」行已失效，不再作为当前状态。
- 本轮仅抽查上述保险 2 页，其他保险页面及浏览器、门禁未覆盖。

## 2026-11-03 续查：保额、保费与退保

### 续查覆盖
- 本轮抽查 `tools/insurance/life-cover-need.html`、`premium-calc.html`、`net-single-premium.html`、`surrender-value.html` 4 页。

### 续查覆盖
- 新抽查 `tools/insurance/life-cover-need.html`、`tools/insurance/premium-calc.html`、`tools/insurance/surrender-value.html`、`tools/insurance/net-single-premium.html` 共 4 页，新增 7 条（3 条高优）；未做浏览器、线上或门禁验证。

## 2026-11-03 续查（并行批 H）

### 留存优化
- `tools/insurance/gross-premium-loading.html:334-336` 的「示例 2×」「示例 0.5×」实际结果为 36.00/6.00 元，相对默认 14.00 是 2.57×/0.43×，名称与结果不符；建议按结果倍数重算参数或改名。
- `tools/insurance/claim-reserve.html:524` 的「小规模」只改已赚保费，保持已付 3500、RBNS 1200，结果是 IBNR 截零、准备金 1200；建议预设同时缩放已付与 RBNS，避免演示出截零边界。
- 上述页面的错误分支均未清空历史/导出，和已记录的 G10 类问题一致；修复时统一「错误即清表并禁用导出」，避免旧方案被保存或分享。

### 续查覆盖
- 本轮新抽查 8 页：`gross-premium-loading.html`、`pure-premium-rate.html`、`endowment-premium.html`、`level-premium-life.html`、`claim-reserve.html`、`ibnr-reserve.html`、`expense-ratio.html`、`combined-ratio.html`；新增 13 条，其中高优 5 条（R-H1、R-H5、R-H8、R-H10、R-H13）。
- 已覆盖页面去重：不含此前已审的 `ibnr-estimate.html`、`annuity-nsp.html`、`life-cover-need.html`、`premium-calc.html`、`surrender-value.html`、`net-single-premium.html`。
- 本轮仅读源码并用 node 内存复算；未做浏览器、英文态、移动端、线上部署或门禁验证，相关运行时表现（历史卡片渲染、CSV 下载内容）仍待验证。
