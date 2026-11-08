# 验证优先清理归档（仅含已验证修复记录）

来源：02-金融财务/tax-accounting-audit.md

- **已修复 2026-11-07**：`calcTool()` 改为**先算满 n 年完整计划再取值**——第 `n-1` 年 `d = (期末账面 − 残值)/2`、第 `n` 年结转余额，实现页面声明的「最后两年改为直线调至残值」；结果区新增「会计政策」行（前 n-2 年双倍余额递减 + 年折旧率，最后两年直线平均分摊、各 X 元）与「逐年折旧」序列（n ≤ 12 时列全，含合计）。
  - 实测（1000000/100000/5 年）：第 4 年 **58000.00**、第 5 年 **58000.00**、第 5 年末账面 **100000.00**、累计 900000.00（旧版 4/5 年分别 86400 / 29600）。
  - 判别力：`scripts/_verify_fin_batch_tn1_tn4.mjs`（当前 PASS / HEAD FAIL）。既有 verify 用例（yr=2 ⇒ 48000.00）不受影响，accounting **74/74**。
- **已修复 2026-11-07**：两页 `__*Extras()` 的无效分支改为**清空旧表**并写占位提示（非数/空值 + 负数都算无效）；`__*Export()` 前置守卫「附表无 `<tr>` ⇒ showToast 并返回」，堵死旧数据导出；`cash-conversion-cycle` 明细表补输入三行（DSO/DIO/DPO）使 CSV 自带输入口径；该页 `formula-eq` 与英文 map 同步新口径（占比 = DPO ÷ 营业周期，营业周期 0 时显示 —，天数须非负）。
  - 判别力（`scripts/_verify_tax_batch_tn2.mjs`，JSDOM + 真实渲染桩数 `tbody tr`）：清空已纳税后明细表 **0 行**（PASS）/ HEAD **5 行**（FAIL）；负数拒绝态 **0 行**（PASS）/ HEAD **5 行**（FAIL）；CCC 有效态 **6 行含输入**（PASS）/ HEAD **3 行无输入**（FAIL）；清空 DSO 后 **0 行**（PASS）/ HEAD **3 行**（FAIL）。
  - 余项：运行时明细表行标签未过 i18n（全站矩阵表同形态）；CSV 未写公式口径行。
- **已修复 2026-11-07**：`calcTool()` 引入 `over=Math.max(ft-lim,0)` / `unused=Math.max(lim-ft,0)`，结果卡片「超出限额部分」改用 `over` 并新增「未使用限额 (元)」行；`__foreign_tax_creditExtras()` 明细表两行同步（导出 CSV 随之为正确口径）；`formula-eq` 文案改为 `max(...,0)` 双口径并同步英文 map（`i18n/tools/en/tax/foreign-tax-credit.json`，文本级替换不重排）。另补金额非负守卫（`ft<0||lim<0` ⇒ 「⚠ 境外已纳税额与抵免限额都不能为负数」并拒绝计算）。
  - 判别力（`scripts/_verify_tax_batch_tn3_tn5.mjs`）：1800/2500 超出限额 **0.00**（PASS）/ HEAD **−700.00**（FAIL）；未使用限额 **700.00**（PASS）/ HEAD 无此行（FAIL）；2000/1500 未使用限额 **0.00**（PASS）/ HEAD 无此行（FAIL）；ft=−100 拒绝计算（PASS）/ HEAD 输出「可抵扣额 −100.00」（FAIL）。可抵扣额与超限态 `500.00` 为守护断言两态同值。
- **已修复（部分）2026-11-07**：越界与负折旧守卫当前已在位（`c>0`、`0 ≤ s ≤ c`、`n` 正整数、`yr` 为 1–n 整数，3.5 年会被拒绝而非向下取整；残值>原值不再产出 −100）。本批补掉残留的「错误态入历史」：`__depreciation_decliningResText()` 的关键词过滤加入 `⚠`，错误/警告文案不再被当成结果写进 TBKit 历史（该页所有错误提示均以 `⚠` 开头）。
  - 判别力（同锁脚本）：残值 200 > 原值 100 时当前记录数 **0**（PASS）/ HEAD 记录数 **1**（FAIL，错误文案入历史）；有效计算两态均落库（守护断言）。
  - 余项：仍无独立的「成功状态」标志位，导出与历史共用结果区文本；导出改为逐年明细（而非复用历史表）未做，留待后续批次。
- **已修复 2026-11-07**：删掉 `(DSO+DIO||1)` 伪分母，改为 `opCycle=DSO+DIO`、`payRatio = opCycle>0 ? DPO/opCycle*100 : null`；`null` 时结果卡片显示 `—` + 标签「应付占营业周期比 (%) · 营业周期为 0，占比无定义」，明细表同步 `—（营业周期为 0，占比无定义）`；CCC 与营业周期本身照常输出（负现金周期保留）。另补非负天数校验（`__N` 填入 DSO/DIO/DPO ⇒ 「⚠ 「应收天数 DSO」不能为负值。」）；空值仍由 `__tbInputGuard` 首段区分。
  - 判别力（`scripts/_verify_tax_batch_tn3_tn5.mjs`）：0/0/30 输出 **—（占比无定义）**（PASS）/ HEAD **3000.00%**（FAIL）；DSO=−5 拒绝计算（PASS）/ HEAD 输出 CCC 15.00（FAIL）；50/100/60 的 150.00 与 40.00 为守护断言两态同值。
- **已修复 2026-11-07**：`calc()` 顶部新增 `__npvParse()`（`parseFloat` + `isFinite`，空值返回 NaN 而不再 `||0`）与 `__npvBlock(msg)`（写入错误卡片、清空 `#detailBody` 与 `#npvChart`、置 `window.__npvBlocked`）；校验链：折现率必填 → 折现率 > -100% → 初始投资必填 → 年金模式每期金额必填 + 期数须为 1–1000 整数（原 `parseInt||1` 兜底删除）→ 自定义模式至少一期且每期现金流不得为空（`updateFlow` 改为空值存 NaN 而非 0，`renderList` 回显 NaN 时留空）。`__npvChartDraw()` 增加 `__npvBlocked` 早退，错误态不再留下基于非法参数画的曲线。逐期折现与累计现值明细表原本已有，无需新增。
  - 判别力（`scripts/_verify_audit_batch_tn6_tn8.mjs`）：空折现率 → **「请填写折现率」**（PASS）/ HEAD **按 0% 算出 NPV 60,000.00**（FAIL）；-150% → **拒绝**（PASS）/ HEAD **NPV −630,000.00**（FAIL）；-100% → **拒绝**（PASS）/ HEAD 显示 `--` 但仍给 ROI（FAIL）；空初始投资 → **拒绝**（PASS）/ HEAD 当 0 处理算出 126,471.13（FAIL）；期数 0 → **拒绝**（PASS）/ HEAD 兜底为 1 期（FAIL）；期数 2.5 → **拒绝**（PASS）/ HEAD `parseInt` 成 0 再兜底 1 期（FAIL）；清空第 2 期 → **拒绝**（PASS）/ HEAD 按 0 兜底（FAIL）。
  - 余项：导出按钮未加「参数非法即禁用」的前置钩子（错误态下 `#detailBody` 已为空，`exportTable` 取不到行只会静默失败），留待与 `__npvExport()` 一并整理。
- **已修复 2026-11-07**：动态行补 `id="cf{i}"`、模式单选补 `id="mode_custom"/"mode_annuity"`；保存器对 radio 增加同组兄弟键清理（修「切过去又切回 → 两组键都命中 → 按 DOM 顺序误判模式」）；新增 `__npvLS/__npvSaveFlows/__npvRestoreFlows`（持久化 `cfCount` + 逐期 `cf{i}`，恢复时补齐/裁剪 `flows` 并重算，上限 60 期防脏数据）；`addFlow/removeFlow/loadDemo` 落库，`updateFlow` **单点落库**（动态新增行不被加载时的一次性扫描绑定，否则第 6 期以后仍存不住——本轮实测第二坑）；启动顺序改为 `__npvRestoreFlows() → renderList() → calc()`。
  - 判别力（`scripts/_verify_audit_batch_tn7.mjs`，两段式 JSDOM：交互产出快照 → 快照注入新实例重开）：交互后持久化键数 **9**（PASS）/ HEAD **0**（FAIL）；恢复后期数 **7**（PASS）/ HEAD **5**（FAIL）；第 7 期金额 **77777**（PASS）/ HEAD 无 `cf6` 元素（FAIL）；模式 **annuity**（PASS）/ HEAD **custom**（FAIL）。
  - 余项：「带输入与结果的本地历史面板」未做；期数 60 上限只用于恢复防脏，按钮侧无上限校验。
- **已修复 2026-11-07**：示例算例原文「系数 0.9259…（4 位）→ 现值 23148+25719+27783+22050+13612 = 112312 → NPV 12312」与页面公式不符（页面按全精度因子算现值，仅显示 4 位）。改为：「各期折现因子 1/(1.08)^t 全精度依次为 0.925926、0.857339、0.793832、0.735030、0.680583（页面表格按 4 位显示 0.9259、0.8573、0.7938、0.7350、0.6806）；按全精度因子算得各期现值 23148.15、25720.16、27784.13、22050.90、13611.66，合计 **112315.00** 元；NPV=**12315.00** 元」。真源三处同批改：`i18n/tools/content_deepdive.json`（`/audit/npv-discount/examples/0/body`）、`i18n/tools/en/audit/npv-discount.json`（中文键 + 英文值）、`i18n/guides/npv-discount-guide.json`（键带前导「：」+ 英文值）；全部文本级替换、未重排 JSON，`audit_deepdive_source_sync.py --check` 4573 页不一致 0。
  - 判别力（同锁脚本，读渲染后 DOM 全文）：当前页面含 **112315.00 / 12315.00** 且无 112312（PASS）/ HEAD 仍为 **112312 / 12312**（3 条全 FAIL）。
